#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface to project settings
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import os
import re
from collections import OrderedDict

import six
import argparse
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dr2xml.config import get_config_variable
from dr2xml.settings_interface.py_settings_interface import format_dict_for_printing, is_key_in_lset, \
    get_variable_from_lset_without_default, is_key_in_sset, get_variable_from_sset_without_default
from dr2xml.utils import Dr2xmlError
from utilities.json_tools import read_json_content, write_json_content
from utilities.logger import get_logger


parser = argparse.ArgumentParser(description='Interface to project settings')
parser.add_argument("--input", required=True, help="Input json file")
parser.add_argument("--output", required=True, help="Output json file")
parser.add_argument("--config", required=True, help="Config json file")

args = parser.parse_args()

config = read_json_content(args.config)
content = read_json_content(args.input)

# Get information from parent if any
def merge_parent(content, config):
    # Create default input if not found
    for element in config:
        default = copy.deepcopy(config[element]["default"])
        if element not in content:
            content[element] = copy.deepcopy(default)

    # Merge content
    if content["parent_project_settings"] is not None:
        parent_content = content["parent_project_settings"]
        if len(os.path.dirname(parent_content)) == 0:
            parent_content = os.sep.join([os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dr2xml", "projects", parent_content])
            parent_content += ".json"
        parent_content = read_json_content(parent_content)
        parent_content = merge_parent(parent_content, config)
        new_content = copy.deepcopy(parent_content)
        for (element, value) in content.items():
            if element in ["parent_project_settings", ]:
                pass
            elif element in ["functions_file", ]:
                new_content[element] = value
            elif element in ["init", "internal", "common"]:
                for (subelt, subval) in value.items():
                    if subelt not in new_content[element]:
                        new_content[element][subelt] = dict()
                    new_content[element][subelt].update(subval)
            else:
                for (subelt, subval) in value.items():
                    if subelt not in new_content[element]:
                        new_content[element][subelt] = dict()
                    for (subsubelt, subsubval) in subval.items():
                        if subsubelt in ["help", ] or subsubelt.endswith("list"):
                            new_content[element][subelt][subsubelt] = subsubval
                        else:
                            if subsubelt not in new_content[element][subelt]:
                                new_content[element][subelt][subsubelt] = dict()
                            for (subsubsubelt, subsubsubval) in subsubval.items():
                                if subsubsubelt not in new_content[element][subelt][subsubelt]:
                                    new_content[element][subelt][subsubelt][subsubsubelt] = dict()
                                new_content[element][subelt][subsubelt][subsubsubelt].update(subsubsubval)
        content = new_content
    return content

content = merge_parent(content, config)

# Fill default values
for element in config:
    default_config = copy.deepcopy(config[element].get("default_config", dict()))
    default_constraints = copy.deepcopy(config[element].get("default_constraint", dict()))

    if element in ["init", "internal", "common", "project_settings"]:
        for (content_elt, content_value) in content[element].items():
            new_content_value = copy.deepcopy(default_config)
            new_content_value.update(content_value)
            content[element][content_elt] = new_content_value

    if element in ["project_settings", ]:
        for (content_elt, content_value) in content[element].items():
            for key in ["attrs_constraints", "comments_constraints", "vars_constraints"]:
                if key in content_value:
                    for (subkey, subval) in content_value[key].items():
                        new_subval = copy.deepcopy(default_constraints)
                        new_subval.update(subval)
                        content_value[key][subkey] = new_subval
                else:
                    content_value[key] = dict()

            for key in ["attrs", "comments", "vars"]:
                list_expected_keywords = copy.deepcopy(content_value[key + "_list"])
                list_current_keywords = copy.deepcopy(list(content_value[key + "_constraints"]))
                for keyword in sorted(list(set(list_current_keywords) - set(list_expected_keywords))):
                    del content_value[key + "_constraints"][keyword]
                for keyword in sorted(list(set(list_expected_keywords) - set(list_current_keywords))):
                    content_value[key + "_constraints"][keyword] = default_constraints

            content[element][content_elt] = content_value

write_json_content(args.output, content)
