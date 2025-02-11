#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools for tests.
"""

import cProfile
import codecs
import copy
import io
import pstats
import shutil
import subprocess
import time
import sys
import os
import unittest
from collections import OrderedDict

from importlib.machinery import SourceFileLoader

import six

from utilities.logger import get_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dr2xml import generate_file_defs, create_ping_files
from dr2xml.config import version


def format_with_values(rep, **kwargs):
	if isinstance(rep, six.string_types):
		rep = rep.format(**kwargs)
	elif isinstance(rep, (dict, OrderedDict)):
		for elt in rep:
			rep[elt] = format_with_values(rep[elt], **kwargs)
	elif isinstance(rep, list):
		rep = [format_with_values(elt, **kwargs) for elt in rep]
	elif isinstance(rep, tuple):
		rep = tuple([format_with_values(elt, **kwargs) for elt in rep])
	elif isinstance(rep, set):
		rep = set([format_with_values(elt, **kwargs) for elt in rep])
	return rep


def read_element_from_python_file(current_dir, element, simulation):
	rep = SourceFileLoader(element + ".py",
	                       os.path.sep.join([current_dir, "test_{}".format(simulation), "input", element + ".py"])
	                       ).load_module(element + ".py").__dict__[element]
	return rep


def test_reference_init(func):
	def test_reference(self, simulation, config_dict, contexts, log="dr2xml_log", stats="dr2xml_stats",
	                   add_profile=False, check_time_file=None, **kwargs):
		print("Test:", simulation)
		old_stdout = sys.stdout
		try:
			dirname = config_dict["dirname"]
			log = os.path.sep.join([dirname, log])
			stats = os.path.sep.join([dirname, "..", stats])
			time_stats = dict()
			with codecs.open(log, 'w', encoding="utf-8") as logfile:
				with codecs.open(stats, "w", encoding="utf-8") as statfile:
					for context in contexts:
						print("Execute context %s" % context)
						sys.stdout = logfile
						if add_profile:
							pr = cProfile.Profile()
							pr.enable()
						start_time = time.time()
						rep = func.__call__(context=context, force_reset=context == contexts[0], **config_dict, **kwargs)
						end_time = time.time()
						if add_profile:
							pr.disable()
						sys.stdout = statfile
						total_time = end_time - start_time
						print("It took %d s to execute context %s" % (total_time, context))
						if add_profile:
							s = io.StringIO()
							sortby = 'cumulative'
							ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
							ps.print_stats()
							print(s.getvalue())
						time_stats[context] = total_time
						sys.stdout = old_stdout

			if check_time_file is not None:
				dr2xml_version = subprocess.check_output('git log -n 1 --pretty=format:"%H"', shell=True)
				with open(check_time_file, "a") as check_time_fic:
					check_time_fic.writelines(["%s;%s;%s%s" % (str(dr2xml_version), context, time_stats[context],
					                                           os.linesep) for context in contexts])
		finally:
			sys.stdout = old_stdout
		return rep
	return test_reference


@test_reference_init
def test_reference_ping(context, lset, sset, filename, **kwargs):
	return create_ping_files(context=context, lset=lset, sset=dict(), filename=filename.format(content=context), **kwargs)


@test_reference_init
def test_reference_simulation(context, lset, sset, force_reset=False, **config_dict):
	return generate_file_defs(context=context, lset=lset, sset=sset, force_reset=force_reset, **config_dict)


def read_file_content(filename, anonymize=dict()):
	with open(filename, "r", encoding="utf-8") as fic:
		content = fic.read()
	for elt in anonymize:
		content = content.replace(anonymize[elt], elt)
	content = content.splitlines(keepends=True)
	return content


def list_comparison_to_do(test, reference):
	print("Compare test %s against reference %s" % (test, reference))
	list_references = os.listdir(reference)
	if len(list_references) == 0:
		raise ValueError("Should be at least one comparison to do, none found")
	list_tests = os.listdir(test)
	rep = list()
	missing = list()
	for f in list_references:
		if f not in list_tests:
			missing.append(os.path.sep.join([test, f]))
		else:
			rep.append([os.path.sep.join([reference, f]), os.path.sep.join([test, f])])
	if len(missing) > 0:
		raise OSError("The following files are missing for comparison: {}".format(", ".join(missing)))
	return rep


def create_config_elements(simulation="my_simulation", contexts=list(), add_profile=False, check_time_file=None,
                           dummies="skip", prefix="IOXDIR", select="on_expt", attributes=list(),
                           year="1980", enddate="19800131", pingfiles="", printout="1", debug=False, is_ping=False,
                           filename="ping_{content}.xml", by_realm=False):
	current_dir = os.path.dirname(os.path.abspath(__file__))
	simulation_dir = os.path.sep.join([current_dir, "test_{}".format(simulation)])
	inputs_dir = os.path.sep.join([simulation_dir, "input"])
	kwargs = dict(
		path_homedr=os.path.sep.join([inputs_dir, "home_data_request"]),
		path_tables=os.path.sep.join([inputs_dir, "tables"]),
		path_xml=os.path.sep.join([inputs_dir, "xml"]),
		path_CV=os.path.sep.join([inputs_dir, "CV", ""]),
		content="{content}"
	)
	rep = dict(
		simulation=simulation,
		contexts=contexts,
		add_profile=add_profile,
		check_time_file=check_time_file,
		lab_and_model_settings=read_element_from_python_file(element="lab_and_model_settings", simulation=simulation,
		                                                     current_dir=current_dir),
		reference_directory=os.path.sep.join([simulation_dir, "reference_outputs"]),
		current_directory=current_dir
	)
	dirname = os.path.sep.join([simulation_dir, "test_outputs", ""])
	if is_ping:
		rep["simulation_settings"] = dict()
		rep["config"] = dict(
			filename=os.sep.join([dirname, filename]),
			dirname=dirname,
			by_realm=by_realm,
			comments=True,
			exact=False,
			dummy=True,
			dummy_with_shape=True,
			year=None,
			select="no",
			printout=printout,
			debug=debug
		)
	else:
		rep["simulation_settings"] = read_element_from_python_file(element="simulation_settings", simulation=simulation,
		                                                           current_dir=current_dir)
		rep["config"] = dict(
			cvs_path="{path_CV}",
			dummies=dummies,
			prefix=prefix,
			select=select,
			dirname=dirname,
			attributes=attributes,
			year=year,
			enddate=enddate,
			pingfiles=pingfiles,
			printout=printout,
			debug=debug
		)
	rep = format_with_values(rep, **kwargs)
	return copy.deepcopy(rep)


class TestRun(object):
	"""
    Test output generation for generic simulation
    """
	simulation=None
	contexts = list()
	add_profile = None
	check_time_file = None
	config = dict()
	lab_and_model_settings = dict()
	simulation_settings = dict()
	reference_directory = None
	current_directory = None
	launch_function = None

	def test_simulation(self):
		if os.path.exists(self.config["dirname"]):
			shutil.rmtree(self.config["dirname"])
		os.makedirs(self.config["dirname"])
		current_directory = self.current_directory
		self.launch_function(simulation=self.simulation, config_dict=self.config,
		                     contexts=self.contexts, lset=self.lab_and_model_settings,
		                     sset=self.simulation_settings, add_profile=self.add_profile,
		                     check_time_file=self.check_time_file)
		to_compare = list_comparison_to_do(test=self.config["dirname"], reference=self.reference_directory)
		anonymize_dict = dict(current_directory=current_directory, current_version=version)
		for (reference_file, test_file) in to_compare:
			reference_content = read_file_content(reference_file, anonymize=anonymize_dict)
			test_content = read_file_content(test_file, anonymize=anonymize_dict)
			unittest.TestCase.assertListEqual(self, test_content, reference_content, msg="Issue comparing %s and %s" %
			                                                                         (test_file, reference_file))
		shutil.rmtree(self.config["dirname"])


class TestSimulation(TestRun):
	launch_function = test_reference_simulation


class TestPing(TestRun):
	launch_function = test_reference_ping
