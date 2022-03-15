#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between json configuration files and dr2xml.
"""
from __future__ import print_function, division, absolute_import, unicode_literals


# Generic setup function
import json
import os
import re
from collections import OrderedDict

import six

from config import get_config_variable
from dr_interface import get_DR_version
from logger import get_logger
from settings_interface import get_variable_from_lset_with_default_in_lset, is_key_in_lset, \
    get_variable_from_lset_without_default, is_key_in_sset, get_variable_from_sset_without_default, \
    get_variable_from_lset_with_default
from utils import Dr2xmlError
from importlib.machinery import SourceFileLoader


def setup_project_settings(**kwargs):
    # Read content from json file
    project_filename = get_variable_from_lset_with_default_in_lset(key="project_settings", key_default="project",
                                                                   default="CMIP6")
    project_filename, project_settings = read_project_settings(project_filename)
    # Merge with parent if needed
    project_settings = merge_project_settings(project_filename, project_settings)
    # Reformat
    project_settings = reformat_settings(project_settings)
    # If asked, save the settings into a dedicated file
    if get_variable_from_lset_with_default("save_project_settings", None) is not None:
        write_json_content(get_variable_from_lset_without_default("save_project_settings"), project_settings)
    # Evaluate common values
    project_settings["__common_values__"] = evaluate_common_values(project_settings["__common_values__"],
                                                                   additional_kwargs=kwargs)
    # Evaluate what can be done for the different tag
    for tag in [tag for tag in project_settings if tag not in ["__common_values__", ]]:
        project_settings[tag] = evaluate_tag_values(tag, project_settings[tag],
                                                    common_dict=project_settings["__common_values__"],
                                                    additional_dict=kwargs)
    return project_settings


# Function to read json content
def read_project_settings(filename):
    if not os.path.isfile(filename):
        filename = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "projects", "{}.json".format(filename)])
    return filename, read_json_content(filename)


def read_json_content(filename):
    logger = get_logger()
    if os.path.isfile(filename):
        with open(filename) as fp:
            content = json.load(fp)
            return content
    else:
        logger.error("Could not find the file containing the project's settings at %s" %
                     filename)
        raise OSError("Could not find the file containing the project's settings at %s" %
                      filename)


def write_json_content(filename, settings):
    with open(filename, "w") as fp:
        json.dump(settings, fp)


# Functions to load project additional functions
def get_func_from_add_module(filename, funcname):
    if not os.path.isfile(filename):
        filename = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "projects", "{}.py".format(filename)])
    add_module = SourceFileLoader(os.path.basename(filename), filename).load_module()
    return add_module.__getattribute__(funcname)


# Function to merge project settings with parents if applicable
def merge_project_settings(project_filename, dict_settings):
    if "parent_project_settings" in dict_settings:
        parent = dict_settings.pop("parent_project_settings")
        parent_filename, parent_settings = read_project_settings(parent)
        parent_settings = merge_project_settings(parent_filename, parent_settings)
        if parent_filename == project_filename:
            raise ValueError("The settings %s reference itself as parent settings. Stop" % project_filename)
    else:
        parent_settings = dict()
    dict_settings = update_settings(parent_settings, dict_settings)
    return dict_settings


def reformat_settings(dict_settings):
    if "__common_values__" not in dict_settings:
        dict_settings["__common_values__"] = dict()
    for key in dict_settings["__common_values__"]:
        dict_settings["__common_values__"][key] = reformat_constraints(key, dict_settings["__common_values__"][key])
    for tag in [tag for tag in dict_settings if tag not in ["__common_values__", ]]:
        for att in ["vars", "attrs"]:
            att_list = "{}_list".format(att)
            att_constraints = "{}_constraints".format(att)
            if att_list not in dict_settings[tag]:
                dict_settings[tag][att_list] = list()
            if att_constraints not in dict_settings[tag]:
                dict_settings[tag][att_constraints] = dict()
            for key in sorted(list(set(list(dict_settings[tag][att_constraints])) -
                                   set(list(dict_settings[tag][att_list])))):
                del dict_settings[tag][att_constraints][key]
            for key in dict_settings[tag][att_list]:
                if key not in dict_settings[tag][att_constraints]:
                    dict_settings[tag][att_constraints][key] = dict()
                dict_settings[tag][att_constraints][key] = \
                    reformat_constraints(key, dict_settings[tag][att_constraints][key])
    return dict_settings


def reformat_constraints(key, dict_settings):
    logger = get_logger()
    # Create default types
    for attr in [att for att in ["skip_values", "forbidden_patterns", "conditions", "default_values"]
                 if att not in dict_settings]:
        dict_settings[attr] = list()
    for attr in [att for att in ["authorized_types", "authorized_values"] if att not in dict_settings]:
        dict_settings[attr] = False
    for attr in [att for att in ["corrections"] if att not in dict_settings]:
        dict_settings[attr] = dict()
    if "output_key" not in dict_settings:
        dict_settings["output_key"] = key
    if "num_type" not in dict_settings:
        dict_settings["num_type"] = "string"
    # Is default
    if len(dict_settings["default_values"]) == 0:
        dict_settings["is_default"] = False
    elif "is_default" not in dict_settings:
        dict_settings["is_default"] = True
    # Fatal
    if "fatal" not in dict_settings:
        dict_settings["fatal"] = False
    elif dict_settings["fatal"] in ["True", ]:
        dict_settings["fatal"] = True
    else:
        dict_settings["fatal"] = False
    # Authorized types
    if dict_settings["authorized_types"]:
        dict_settings["authorized_types"] = [globals()["__builtins__"][val] for val in
                                             dict_settings["authorized_types"]]
    if dict_settings["authorized_types"] and len(dict_settings["authorized_types"]) == 1:
        dict_settings["authorized_types"] = dict_settings["authorized_types"][0]
    logger.debug("Constraints for key %s: %s" % (key, str(dict_settings)))
    return dict_settings


def update_constraints(current_settings, new_settings):
    if current_settings is None:
        return new_settings
    else:
        for key in new_settings:
            if isinstance(new_settings[key], (dict, OrderedDict)):
                if key not in current_settings:
                    current_settings[key] = dict()
                current_settings[key].update(new_settings[key])
            else:
                current_settings[key] = new_settings[key]
    return current_settings


def update_settings(current_settings, new_settings):
    if "__common_values__" in new_settings:
        if "__common_values__" not in current_settings:
            current_settings["__common_values__"] = dict()
        for key in new_settings["__common_values__"]:
            current_settings["__common_values__"][key] = \
                update_constraints(current_settings["__common_values__"].get(key),
                                   new_settings["__common_values__"][key])
    for tag in [tag for tag in new_settings if tag not in ["__common_values__", ]]:
        if tag not in current_settings:
            current_settings[tag] = dict()
        for att in ["attrs_list", "vars_list"]:
            if att in new_settings[tag]:
                current_settings[tag][att] = new_settings[tag][att]
        for att in ["attrs_constraints", "vars_constraints"]:
            if att in new_settings[tag]:
                if att not in current_settings[tag]:
                    current_settings[tag][att] = dict()
                for key in new_settings[tag][att]:
                    current_settings[tag][att][key] = \
                        update_constraints(current_settings[tag][att].get(key), new_settings[tag][att][key])
    return current_settings


def check_value(value, skip_values=list(), authorized_types=False, authorized_values=False, forbidden_patterns=list(),
                conditions=False):
    is_allowed = str(value) not in skip_values
    if is_allowed and authorized_types:
        is_allowed = isinstance(value, authorized_types)
    if is_allowed and authorized_values:
        is_allowed = value in authorized_values
    if is_allowed:
        is_allowed = not(any([re.compile(pattern).match(value) for pattern in forbidden_patterns]))
    is_allowed = is_allowed and conditions
    return is_allowed


def get_value(key_type, key, src, common_dict=dict(), additional_dict=dict()):
    found = False
    value = None
    if key_type in ["common", ] and key in common_dict:
        value = common_dict[key]
        found = True
    elif key_type in ["dict", ] and key in additional_dict:
        value = additional_dict[key]
        found = True
    elif key_type in ["config", ]:
        try:
            value = get_config_variable(key)
            found = True
        except Dr2xmlError:
            pass
    elif key_type in ["DR_version", ]:
        value = get_DR_version()
        found = True
    elif key_type in ["variable", ] and "variable" in additional_dict and \
            key in additional_dict["variable"].__dict__:
        value = additional_dict["variable"].__getattribute__(key)
        found = True
    elif key_type in ["laboratory", ] and is_key_in_lset(key):
        value = get_variable_from_lset_without_default(key)
        found = True
    elif key_type in ["simulation", ] and is_key_in_sset(key):
        value = get_variable_from_sset_without_default(key)
        found = True
    elif key_type in ["json", ]:
        found, value = get_key_value(key_value=src, common_dict=common_dict, additional_dict=additional_dict)
        if found:
            value = read_json_content(value)
            if key in value:
                value = value[key]
            elif key is not None:
                found = False
    elif key_type in ["combine", ]:
        raise Exception("Should not pass here")
    return found, value


def get_key_value(key_value, common_dict=dict(), additional_dict=dict()):
    if isinstance(key_value, dict):
        # Find elements about key_value
        key_type = key_value.get("key_type", None)
        keys = key_value.get("keys", None)
        fmt = key_value.get("fmt", None)
        src = key_value.get("src", None)
        func = key_value.get("func", None)
        # Resolve key_value
        if keys is not None:
            if key_type is None:
                raise ValueError("key_type must be defined")
            if isinstance(keys, list):
                keys_resolve = [get_key_value(key_value=key, common_dict=common_dict, additional_dict=additional_dict)
                                for key in keys]
                keys_found = [elt[0] for elt in keys_resolve]
                keys_values = [elt[1] for elt in keys_resolve]
                found = all(keys_found)
                if found:
                    if key_type in ["combine", ]:
                        value = fmt.format(*keys_values)
                    else:
                        if len(keys_values) > 0:
                            key = keys_values[0]
                            keys_values = keys_values[1:]
                        else:
                            key = None
                        found, value = get_value(key_type=key_type, key=key, src=src, common_dict=common_dict,
                                                 additional_dict=additional_dict)
                        i = 0
                        while found and i < len(keys_values):
                            if value is None:
                                found = False
                            elif isinstance(value, list):
                                value = value[keys_values[i]]
                            elif isinstance(value, dict) and keys_values[i] in value:
                                value = value[keys_values[i]]
                            elif not isinstance(value, dict) and keys_values[i] in value.__dict__:
                                value = value.__getattribute__(keys_values[i])
                            else:
                                found = False
                            i += 1
                else:
                    value = None
            else:
                found, value = get_value(key_type=key_type, key=keys, src=src, common_dict=common_dict,
                                         additional_dict=additional_dict)
            # Take into account format
            if found and key_type not in ["combine", ]:
                if fmt is None and isinstance(value, list):
                    value = value[0]
                elif fmt is not None and isinstance(value, list):
                    value = fmt.format(*value)
                elif fmt is not None:
                    value = fmt.format(value)
            if found and isinstance(value, six.string_types):
                value = value.strip()
            if found and func is not None:
                value = apply_function(is_value=True, value=value, *func, additional_dict=additional_dict,
                                       common_dict=common_dict)
        else:
            if func is not None:
                value = apply_function(*func, value=None, is_value=False, additional_dict=additional_dict,
                                       common_dict=common_dict)
                found = True
            else:
                value = None
                found = False
            if found:
                if fmt is None and isinstance(value, list):
                    value = value[0]
                elif fmt is not None and isinstance(value, list):
                    value = fmt.format(*value)
                elif fmt is not None:
                    value = fmt.format(value)
        return found, value
    else:
        return True, key_value


def apply_function(mod, func, options, value=None, is_value=False, additional_dict=dict(), common_dict=dict()):
    func = get_func_from_add_module(mod, func)
    for key in sorted(list(options)):
        test, val = get_key_value(options[key], additional_dict=additional_dict, common_dict=common_dict)
        if test:
            options[key] = val
        else:
            del options[key]
    if is_value:
        value = func(value, **options)
    else:
        value = func(**options)
    return value


def check_conditions(conditions, common_dict=dict(), additional_dict=dict(), keep_not_found=False):
    if isinstance(conditions, bool):
        relevant = True
        test = conditions
    else:
        conditions_checked = [check_condition(conditions[i], common_dict=common_dict, additional_dict=additional_dict)
                              for i in range(len(conditions))]
        relevant_checked = [elt[0] for elt in conditions_checked]
        conditions_checked = [elt[1] for elt in conditions_checked]
        if all(relevant_checked):
            relevant = True
            test = all(conditions_checked)
        elif keep_not_found:
            relevant = False
            i = 0
            for c in range(conditions_checked.count(True)):
                i = conditions_checked.index(True, i + 1)
                conditions_checked[i] = conditions[i]
            test = conditions_checked
        else:
            relevant = False
            test = False
    return relevant, test


def check_condition(condition, common_dict=dict(), additional_dict=dict()):
    if isinstance(condition, bool):
        relevant = True
        test = condition
    else:
        test = True
        relevant = True
        first_val, check, second_val = condition
        found_first, first_val = get_key_value(first_val, common_dict=common_dict, additional_dict=additional_dict)
        if not isinstance(second_val, list):
            second_val = [second_val, ]
        second_val = [get_key_value(val, common_dict=common_dict, additional_dict=additional_dict)
                      for val in second_val]
        found_second = all([elt[0] for elt in second_val])
        second_val = [elt[1] for elt in second_val]
        if found_first and found_second:
            if check in ["eq", ]:
                test = test and first_val in second_val
            elif check in ["neq", ]:
                test = test and first_val not in second_val
            else:
                raise ValueError("Conditions can have 'eq' or 'neq' as operator, found: %s" % check)
        else:
            relevant = False
    return relevant, test


def evaluate_common_values(common_dict=dict(), additional_kwargs=dict()):
    rep = dict()
    items_to_treat = sorted(list(common_dict))
    test = True
    while len(items_to_treat) > 0 and test:
        for item in items_to_treat:
            found, value, _ = find_value(tag="__common_values__", key=item, value=None, is_default_value=True,
                                         fatal=False, conditions=common_dict[item]["conditions"],
                                         skip_values=common_dict[item]["skip_values"],
                                         authorized_types=common_dict[item]["authorized_types"],
                                         authorized_values=common_dict[item]["authorized_values"],
                                         forbidden_patterns=common_dict[item]["forbidden_patterns"],
                                         default_values=common_dict[item]["default_values"],
                                         corrections=common_dict[item]["corrections"],
                                         common_dict=rep, additional_dict=additional_kwargs, is_default=True)
            if found:
                rep[item] = value
                del common_dict[item]
        test = len(common_dict) < len(items_to_treat)
        items_to_treat = sorted(list(common_dict))
    if not test:
        for item in items_to_treat:
            if not common_dict[item]["fatal"]:
                del common_dict[item]
        items_to_treat = sorted(list(common_dict))
        test = len(items_to_treat) == 0
    if not test:
        raise ValueError("Could not evaluate all common values: the following are missing %s" % items_to_treat)
    return rep


def evaluate_tag_values(tag, tag_dict, common_dict=dict(), additional_dict=dict()):
    for section in ["attrs_constraints", "vars_constraints"]:
        for item in sorted(list(tag_dict[section])):
            found, conditions = check_conditions(tag_dict[section][item]["conditions"], common_dict=common_dict,
                                                 additional_dict=additional_dict, keep_not_found=True)
            tag_dict[section][item]["conditions"] = conditions
            for (i, value) in enumerate(list(tag_dict[section][item]["default_values"])):
                found, value, _ = find_value(tag=tag, key=item, is_default_value=False, fatal=False,
                                             conditions=list(), value=value, default_values=list(),
                                             skip_values=tag_dict[section][item]["skip_values"],
                                             authorized_types=tag_dict[section][item]["authorized_types"],
                                             authorized_values=tag_dict[section][item]["authorized_values"],
                                             forbidden_patterns=tag_dict[section][item]["forbidden_patterns"],
                                             corrections=tag_dict[section][item]["corrections"],
                                             common_dict=common_dict, additional_dict=additional_dict, is_default=False)
                if found:
                    tag_dict[section][item]["default_values"][i] = value
    return tag_dict


def correct_value(value, corrections=list(), additional_dict=dict(), common_dict=dict()):
    if isinstance(value, six.string_types):
        value = value.strip()
    if isinstance(value, (int, float, six.string_types)) and value in corrections:
        correction = corrections[value]
        if isinstance(correction, dict):
            # case value to evaluate
            test, correction = get_key_value(correction, common_dict=common_dict, additional_dict=additional_dict)
            if test:
                value = correction
        elif isinstance(correction, list):
            # case conditions to evaluate
            condition, new_value = correction
            relevant, condition = check_conditions(condition, additional_dict=additional_dict, common_dict=common_dict)
            if relevant and condition:
                relevant, new_value = get_key_value(new_value, common_dict=common_dict, additional_dict=additional_dict)
                if relevant:
                    value = new_value
        else:
            value = correction
    return value


def find_value(tag, key, value, is_default_value=True, conditions=list(), skip_values=list(), authorized_types=False,
               authorized_values=False, forbidden_patterns=list(), default_values=list(), fatal=False, is_default=False,
               common_dict=dict(), additional_dict=dict(), corrections=list(), output_key=None, num_type="str"):
    output_dict = dict(output_key=output_key, num_type=num_type)
    found, conditions = check_conditions(conditions, common_dict=common_dict, additional_dict=additional_dict)
    if found:
        if not is_default_value:
            value = correct_value(value, corrections=corrections, additional_dict=additional_dict,
                                  common_dict=common_dict)
            found = check_value(value, skip_values=skip_values, authorized_types=authorized_types,
                                authorized_values=authorized_values, forbidden_patterns=forbidden_patterns,
                                conditions=conditions)
        else:
            found = False
        if not found and is_default:
            i = 0
            while not found and i < len(default_values):
                found, value = get_key_value(default_values[i], common_dict=common_dict,
                                             additional_dict=additional_dict)
                if found:
                    value = correct_value(value, corrections=corrections, additional_dict=additional_dict,
                                          common_dict=common_dict)
                    found = check_value(value, skip_values=skip_values, authorized_types=authorized_types,
                                        authorized_values=authorized_values, forbidden_patterns=forbidden_patterns,
                                        conditions=conditions)
                i += 1
    if fatal and not found:
        raise Dr2xmlError("Could not find a proper value for tag %s and key %s (values tested: %s)"
                          % (tag, key, " ".join([str(value), str(default_values)])))
    return found, value, output_dict
