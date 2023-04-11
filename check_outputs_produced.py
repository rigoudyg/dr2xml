#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Take in entry xml files designed for xios and return the list of netcdf file names that should be produced.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import os
import re
from argparse import ArgumentParser
from xml_writer.utils import decode_if_needed
from xml_writer.element import Element
from xml_writer.parser import xml_file_parser


def find_filenames(xml_element):
	rep = list()
	if isinstance(xml_element, Element):
		if xml_element.tag in ["file", ] and xml_element.get_attrib("enabled", use_default=True, default=True) in [True, "true", "True"]:
			rep.append(xml_element.attrib["name"])
		elif len(xml_element) > 0:
			for xml_child in xml_element:
				rep.extend(find_filenames(xml_child))
	return rep


def find_netcdf_filenames_from_xml(xml_filename):
	_, _, _, root = xml_file_parser(xml_file=xml_filename, follow_src=True)
	filenames_list = find_filenames(root)
	return filenames_list


def find_netcdf_filenames_from_xmls(xml_files, start_date_pattern, end_date_pattern, ioxdir, ioxdir_pattern):
	netcdf_filenames_list = list()
	for filename in xml_files:
		netcdf_filenames_list.extend(find_netcdf_filenames_from_xml(filename))
	netcdf_filenames_list = [
		f.replace(start_date_pattern, "(?P<start_date>\d+)").replace(end_date_pattern, "(?P<end_date>\d+)").replace(
			ioxdir_pattern, ioxdir) + ".nc" for f in netcdf_filenames_list]
	netcdf_filenames_list = sorted(list(set(netcdf_filenames_list)))
	return netcdf_filenames_list


def check_if_pattern_match(netcdf_list, dr2xml_pattern):
	dr2xml_regexp = re.compile(dr2xml_pattern)
	to_delete = [elt for elt in netcdf_list if dr2xml_regexp.match(elt)]
	if len(to_delete) > 0:
		return True, sorted(list(set(netcdf_list) - set(to_delete)))
	else:
		return False, netcdf_list


def check_consistency(netcdf_list, dr2xml_list):
	dr2xml_not_found = list()
	for patt in dr2xml_list:
		found, netcdf_list = check_if_pattern_match(netcdf_list, patt)
		if not found:
			dr2xml_not_found.append(patt)
	return len(dr2xml_not_found) == 0 and len(netcdf_list) == 0, dr2xml_not_found, netcdf_list


def list_content(target_dir):
	content = os.listdir(target_dir)
	content = [f for f in content if not os.path.isdir(os.path.sep.join([ioxdir, f])) and f.endswith(".nc")]
	return content


def parse_args():
	parser = ArgumentParser()
	parser.add_argument("xml_files", nargs="+", help="XML input files to parse")
	parser.add_argument("--out", required=True, help="Output filename")
	parser.add_argument("--ioxdir", required=True,
	                    help="Directory in which outputs can be found (can be a directory in which there is only "
	                         "subdirectories, in this case each subdirectory will be checked).")
	parser.add_argument("--ioxdir_pattern", default="IOXDIR", help="Pattern for ioxdir in filename")
	parser.add_argument("--start_date_pattern", default="%start_date%", help="Pattern for start date in filename")
	parser.add_argument("--end_date_pattern", default="%end_date%", help="Pattern for end date in filename")
	return parser.parse_args().__dict__


def make_check(find_dict, ioxdir, output):
	dr2xml_netcdf_filenames_list = find_netcdf_filenames_from_xmls(**find_dict)
	dr2xml_netcdf_filenames_list = [os.path.basename(elt) for elt in dr2xml_netcdf_filenames_list]

	rep = True

	with open(output, "w", encoding="utf-8") as out:
		if not os.path.isdir(ioxdir):
			raise OSError("IOX directory %s does not exist" % ioxdir)
		else:
			output_list = list_content(ioxdir)
			is_output_here = len(output_list) > 0
			if is_output_here:
				out.write(decode_if_needed("Deal with directory %s\n" % ioxdir))
				rep2, dr2xml_not_found, outputs_not_found = check_consistency(output_list, copy.deepcopy(dr2xml_netcdf_filenames_list))
				if not rep2:
					if len(dr2xml_not_found) > 0:
						out.write(decode_if_needed("The following dr2xml patterns were not found in directory:\n%s\n" % os.linesep.join(dr2xml_not_found)))
					if len(outputs_not_found) > 0:
						out.write(decode_if_needed("The following files were not found in dr2xml patterns:\n%s\n" % os.linesep.join(outputs_not_found)))
				else:
					out.write(decode_if_needed("All match\n"))
				rep = rep and rep2
			else:
				for d in sorted([elt for elt in os.listdir(ioxdir) if os.path.isdir(os.path.sep.join([ioxdir, elt]))]):
					current_dir = os.path.sep.join([ioxdir, d])
					out.write(decode_if_needed("Deal with directory %s\n" % current_dir))
					output_list = list_content(current_dir)
					rep2, dr2xml_not_found, outputs_not_found = check_consistency(output_list, copy.deepcopy(
						dr2xml_netcdf_filenames_list))
					if not rep2:
						if len(dr2xml_not_found) > 0:
							out.write(decode_if_needed("The following dr2xml patterns were not found in directory:\n%s\n" % os.linesep.join(dr2xml_not_found)))
						if len(outputs_not_found) > 0:
							out.write(decode_if_needed("The following files were not found in dr2xml patterns:\n%s\n" % os.linesep.join(outputs_not_found)))
					else:
						out.write(decode_if_needed("All match\n"))
					rep = rep and rep2

	if not rep:
		raise ValueError("The dr2xml and directory contents does not match")


if __name__ == "__main__":
	find_dict = parse_args()
	output = find_dict.pop("out")
	ioxdir = find_dict["ioxdir"]
	find_dict["ioxdir"] = ""
	make_check(find_dict, ioxdir, output)
