#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to create documentation for project settings.
"""
from __future__ import print_function, division, absolute_import, unicode_literals


import os
import shutil
import sys
import argparse
import tempfile

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

from dr2xml.settings_interface.py_project_interface import initialize_project_settings
from dr2xml.settings_interface.py_settings_interface import initialize_dict


target_directory = os.sep.join([current_dir, "sphinx", "source", "userguide"])

parser = argparse.ArgumentParser()
parser.add_argument("--target_directory", default=target_directory, help="Directory in which the outputs will be created.")
args = parser.parse_args()


def write_documentation(output_directory, package_directory):
	projects_list = os.listdir(os.sep.join([package_directory, "dr2xml", "projects"]))
	projects_list = [elt.replace(".py", "") for elt in projects_list if elt.endswith(".py")]
	projects_list = sorted(projects_list)
	projects_list.remove("dr2xml")
	projects_list.insert(0, "dr2xml")
	projects_list.remove("basics")
	projects_list.insert(1, "basics")
	projects_list.remove("projects_interface_definitions")


	project_target_dir = os.sep.join([output_directory, "projects"])
	if os.path.exists(project_target_dir):
		shutil.rmtree(project_target_dir)
	os.makedirs(project_target_dir)

	lset = dict()
	sset = dict()

	for project in projects_list:
		lset["project"] = project
		initialize_dict(new_lset=lset, new_sset=sset)
		initialize_project_settings(project_target_dir, doc_writer=True)

	content = list()
	content.append("Parameters available in settings")
	content.append("================================")
	content.append("")
	content.append(".. toctree::")
	content.append("   :maxdepth: 1")
	content.append("   :caption: Settings by project:")
	content.append("   ")
	for project in projects_list:
		content.append("   %s project <projects/%s>" % (project, project))
	content.append("")

	with open(os.sep.join([output_directory, "parameters.rst"]), "w") as fic:
		fic.write(os.linesep.join(content))


if args.target_directory in ["test", ]:
	with tempfile.TemporaryDirectory() as output_directory:
		write_documentation(output_directory=output_directory, package_directory=current_dir)
else:
	write_documentation(output_directory=args.target_directory, package_directory=current_dir)
