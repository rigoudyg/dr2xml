#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
General json settings interface to internal settings
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import re
from collections import OrderedDict
from importlib.machinery import SourceFileLoader

import six

from logger import get_logger
from .py_settings_interface import get_variable_from_lset_with_default_in_lset, get_variable_from_lset_with_default
from dr2xml.utils import write_json_content, read_json_content, Dr2xmlError


def initialize_json_settings():
    # Read content from json file
    project_filename = get_variable_from_lset_with_default_in_lset(key="project_settings", key_default="project",
                                                                   default="CMIP6")
    project_filename, project_settings = read_project_settings(project_filename)
    # Merge with parent if needed
    project_settings = merge_project_settings(project_filename, project_settings)
    # Reformat
    project_settings = reformat_settings(project_settings)
    # If asked, save the settings into a dedicated file
    save_project_settings = get_variable_from_lset_with_default("save_project_settings", None)
    if save_project_settings is not None:
        write_json_content(save_project_settings, project_settings)
    internal_settings = project_settings.pop("__internal_values__")
    common_settings = project_settings.pop("__common_values__")
    return internal_settings, common_settings, project_settings


def read_project_settings(filename):
    if not os.path.isfile(filename):
        filename = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "..", "projects",
                                "{}.json".format(filename)])
    return filename, read_json_content(filename)


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
    for tag in ["__internal_values__", "__common_values__"]:
        if tag not in dict_settings:
            dict_settings[tag] = dict()
        for key in dict_settings[tag]:
            dict_settings[tag][key] = reformat_constraints(key, dict_settings[tag][key])
    for tag in [tag for tag in dict_settings if tag not in ["__common_values__", "__internal_values__"]]:
        for att in ["vars", "attrs", "comments"]:
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


def update_settings(current_settings, new_settings):
    for tag in ["__internal_values__", "__common_values__"]:
        if tag in new_settings:
            if tag not in current_settings:
                current_settings[tag] = dict()
            for key in new_settings[tag]:
                current_settings[tag][key] = update_constraints(current_settings[tag].get(key), new_settings[tag][key])
    for tag in [tag for tag in new_settings if tag not in ["__common_values__", ]]:
        if tag not in current_settings:
            current_settings[tag] = dict()
        for att in ["attrs_list", "vars_list", "comments_list"]:
            if att in new_settings[tag]:
                current_settings[tag][att] = new_settings[tag][att]
        for att in ["attrs_constraints", "vars_constraints", "comments_constraints"]:
            if att in new_settings[tag]:
                if att not in current_settings[tag]:
                    current_settings[tag][att] = dict()
                for key in new_settings[tag][att]:
                    current_settings[tag][att][key] = \
                        update_constraints(current_settings[tag][att].get(key), new_settings[tag][att][key])
    return current_settings


def reformat_constraints(key, dict_settings):
    logger = get_logger()
    # Create default types
    for attr in [att for att in ["skip_values", "forbidden_patterns", "conditions", "default_values", "cases"]
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


def solve_complete_settings(settings, name, func_to_call, additional_settings=dict(), additional_kwargs=dict()):
    rep = dict()
    items_to_treat = sorted(list(settings))
    test = True
    args_dict = dict(tag=name, value=None, is_default_value=True, fatal=False, additional_dict=additional_kwargs,
                     is_default=True)
    if name in ["common", ]:
        args_dict["internal_dict"] = additional_settings
        current_name = "common_dict"
    else:
        args_dict["common_dict"] = dict()
        current_name = "internal_dict"
    while len(items_to_treat) > 0 and test:
        for item in items_to_treat:
            args_dict.update({"key": item,
                              "conditions": settings[item]["conditions"],
                              "skip_values": settings[item]["skip_values"],
                              "authorized_types": settings[item]["authorized_types"],
                              "authorized_values": settings[item]["authorized_values"],
                              "forbidden_patterns": settings[item]["forbidden_patterns"],
                              "default_values": settings[item]["default_values"],
                              "corrections": settings[item]["corrections"],
                              "cases": settings[item]["cases"],
                              current_name: rep
                              })
            found, value, _ = func_to_call.__call__(**args_dict)
            if found:
                rep[item] = value
                del settings[item]
        test = len(settings) < len(items_to_treat)
        items_to_treat = sorted(list(settings))
    if not test:
        for item in items_to_treat:
            if not settings[item]["fatal"]:
                del settings[item]
        items_to_treat = sorted(list(settings))
        test = len(items_to_treat) == 0
    if not test:
        raise ValueError("Could not evaluate all common values: the following are missing %s" % items_to_treat)
    return rep


def get_func_from_add_module(filename, funcname):
    if not os.path.isfile(filename):
        filename = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "..", "projects", "{}.py".format(filename)])
    add_module = SourceFileLoader(os.path.basename(filename), filename).load_module()
    return add_module.__getattribute__(funcname)


def correct_value_generic(get_key_value_func, value, corrections=list(), additional_dict=dict(), common_dict=dict(),
                          internal_dict=dict()):
    if isinstance(value, six.string_types):
        value = value.strip()
    if isinstance(value, (int, float, six.string_types)) and value in corrections:
        correction = corrections[value]
        if isinstance(correction, dict):
            # case value to evaluate
            test, correction = get_key_value_func.__call__(correction, common_dict=common_dict,
                                                           additional_dict=additional_dict, internal_dict=internal_dict)
            if test:
                value = correction
        elif isinstance(correction, list):
            # case conditions to evaluate
            condition, new_value = correction
            relevant, condition = check_conditions_generic(get_key_value_func, condition,
                                                           additional_dict=additional_dict,
                                                           common_dict=common_dict, internal_dict=internal_dict)
            if relevant and condition:
                relevant, new_value = get_key_value_func.__call__(new_value, common_dict=common_dict,
                                                                  additional_dict=additional_dict,
                                                                  internal_dict=internal_dict)
                if relevant:
                    value = new_value
        else:
            value = correction
    return value


def find_value_generic(get_key_value_func, tag, key, value, is_default_value=True, conditions=list(),
                       skip_values=list(), authorized_types=False, authorized_values=False, forbidden_patterns=list(),
                       default_values=list(), fatal=False, is_default=False, common_dict=dict(), additional_dict=dict(),
                       corrections=list(), cases=list(), output_key=None, num_type="str", internal_dict=dict()):
    output_dict = dict(output_key=output_key, num_type=num_type)
    found, conditions = check_conditions_generic(get_key_value_func, conditions, common_dict=common_dict,
                                                 additional_dict=additional_dict, internal_dict=internal_dict)
    if found:
        if not is_default_value:
            value = correct_value_generic(get_key_value_func, value, corrections=corrections,
                                          additional_dict=additional_dict, common_dict=common_dict,
                                          internal_dict=internal_dict)
            found = check_value_generic(get_key_value_func, value, skip_values=skip_values,
                                        authorized_types=authorized_types, authorized_values=authorized_values,
                                        forbidden_patterns=forbidden_patterns, conditions=conditions,
                                        common_dict=common_dict, additional_dict=additional_dict,
                                        internal_dict=internal_dict)
        else:
            found = False
        if not found and len(cases) > 0:
            i = 0
            while not found and i < len(cases):
                condition, value = cases[i]
                found, condition = check_conditions_generic(get_key_value_func, condition, common_dict=common_dict,
                                                            additional_dict=additional_dict,
                                                            internal_dict=internal_dict)
                if found:
                    found, value = get_key_value_func.__call__(value, common_dict=common_dict,
                                                               additional_dict=additional_dict,
                                                               internal_dict=internal_dict)
                    if found:
                        found = check_value_generic(get_key_value_func, value, skip_values=skip_values,
                                                    authorized_types=authorized_types,
                                                    authorized_values=authorized_values,
                                                    forbidden_patterns=forbidden_patterns, conditions=condition,
                                                    common_dict=common_dict, additional_dict=additional_dict,
                                                    internal_dict=internal_dict)
                if not found:
                    i += 1
        if not found and is_default:
            i = 0
            while not found and i < len(default_values):
                found, value = get_key_value_func.__call__(default_values[i], common_dict=common_dict,
                                                           additional_dict=additional_dict, internal_dict=internal_dict)
                if found:
                    value = correct_value_generic(get_key_value_func, value, corrections=corrections,
                                                  additional_dict=additional_dict, common_dict=common_dict,
                                                  internal_dict=internal_dict)
                    found = check_value_generic(get_key_value_func, value, skip_values=skip_values,
                                                authorized_types=authorized_types, authorized_values=authorized_values,
                                                forbidden_patterns=forbidden_patterns, conditions=conditions,
                                                common_dict=common_dict, additional_dict=additional_dict,
                                                internal_dict=internal_dict)
                i += 1
        if fatal and conditions and not found:
            raise Dr2xmlError("Could not find a proper value for tag %s and key %s (values tested: %s)"
                              % (tag, key, " ".join([str(value), str(default_values)])))
    else:
        if fatal:
            raise Dr2xmlError("Could not find a proper value for tag %s and key %s (values tested: %s)"
                              % (tag, key, " ".join([str(value), str(default_values)])))
    return found, value, output_dict


def check_conditions_generic(get_key_value_func, conditions, common_dict=dict(), additional_dict=dict(),
                             keep_not_found=False, internal_dict=dict()):
    if isinstance(conditions, bool):
        relevant = True
        test = conditions
    elif isinstance(conditions, six.string_types) and conditions in ["True", ]:
        relevant = True
        test = True
    elif isinstance(conditions, six.string_types) and conditions in ["False", ]:
        relevant = True
        test = False
    else:
        conditions_checked = [check_condition_generic(get_key_value_func, conditions[i], common_dict=common_dict,
                                                      additional_dict=additional_dict, internal_dict=internal_dict)
                              for i in range(len(conditions))]
        relevant_checked = [elt[0] for elt in conditions_checked]
        conditions_checked = [elt[1] for elt in conditions_checked]
        if all(relevant_checked):
            relevant = True
            test = all(conditions_checked)
        elif keep_not_found and any(relevant_checked):
            relevant = False
            i = 0
            for c in range(relevant_checked.count(True)):
                i = relevant_checked.index(True, i + 1)
                conditions[i] = conditions_checked[i]
            test = conditions
        elif keep_not_found:
            relevant = False
            test = conditions_checked
        else:
            relevant = False
            test = False
    return relevant, test


def check_condition_generic(get_key_value_func, condition, common_dict=dict(), additional_dict=dict(),
                            internal_dict=dict()):
    if isinstance(condition, bool):
        relevant = True
        test = condition
    elif isinstance(condition, six.string_types) and condition in ["True", ]:
        relevant = True
        test = True
    elif isinstance(condition, six.string_types) and condition in ["False", ]:
        relevant = True
        test = False
    else:
        test = True
        relevant = True
        first_val, check, second_val = condition
        found_first, first_val = get_key_value_func.__call__(first_val, common_dict=common_dict,
                                                             additional_dict=additional_dict,
                                                             internal_dict=internal_dict)
        if not isinstance(second_val, list):
            second_val = [second_val, ]
        second_val = [get_key_value_func.__call__(val, common_dict=common_dict, additional_dict=additional_dict,
                                                  internal_dict=internal_dict)
                      for val in second_val]
        found_second = all([elt[0] for elt in second_val])
        second_val = [str(elt[1]) for elt in second_val]
        if found_first and found_second:
            if check in ["eq", ]:
                test = test and str(first_val) in second_val
            elif check in ["neq", ]:
                test = test and str(first_val) not in second_val
            elif check in ["match", ]:
                test = test and all([re.compile(val).match(str(first_val)) is not None for val in second_val])
            elif check in ["nmatch", ]:
                test = test and not any([re.compile(val).match(str(first_val)) is not None for val in second_val])
            else:
                raise ValueError("Conditions can have 'eq' or 'neq' as operator, found: %s" % check)
        else:
            relevant = False
    return relevant, test


def check_value_generic(get_key_value_func, value, skip_values=list(), authorized_types=False, authorized_values=False,
                        forbidden_patterns=list(), conditions=False, common_dict=dict(), additional_dict=dict(),
                        internal_dict=dict()):
    is_allowed = str(value) not in skip_values
    if is_allowed and authorized_types:
        is_allowed = isinstance(value, authorized_types)
    if is_allowed and authorized_values:
        if isinstance(authorized_values, dict):
            found, authorized_values = get_key_value_func.__call__(authorized_values, common_dict=common_dict,
                                                                   additional_dict=additional_dict,
                                                                   internal_dict=internal_dict)
        else:
            found = True
        if found and not isinstance(authorized_values, list):
            authorized_values = [authorized_values, ]
            is_allowed = str(value) in authorized_values
    if is_allowed:
        is_allowed = not(any([re.compile(pattern).match(value) for pattern in forbidden_patterns]))
    is_allowed = is_allowed and conditions
    return is_allowed


def apply_function_generic(get_key_value_func, mod, func, options, value=None, is_value=False, additional_dict=dict(),
                           common_dict=dict(), internal_dict=dict()):
    test = True
    func = get_func_from_add_module(mod, func)
    for key in sorted(list(options)):
        key_test, val = get_key_value_func.__call__(options[key], additional_dict=additional_dict,
                                                    common_dict=common_dict, internal_dict=internal_dict)
        if key_test:
            options[key] = val
        else:
            del options[key]
    try:
        if is_value:
            value = func(value, **options)
        else:
            value = func(**options)
    except:
        test = False
    return test, value
