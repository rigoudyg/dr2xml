#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilities specific to common settings
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import six

from dr2xml.config import get_config_variable
from dr2xml.dr_interface import get_scope, get_DR_version
from .general_json_project_interface import solve_complete_settings, find_value_generic, apply_function_generic, \
    check_conditions_generic
from .py_settings_interface import get_variable_from_sset_without_default, is_key_in_sset, format_dict_for_printing, \
    get_variable_from_lset_without_default, is_key_in_lset
from dr2xml.utils import read_json_content, Dr2xmlError


def solve_common_settings(common_settings, additional_kwargs=dict(), internal_settings=dict()):
    return solve_complete_settings(settings=common_settings, name="common", func_to_call=find_value,
                                   additional_kwargs=additional_kwargs, additional_settings=internal_settings)


def solve_project_settings(project_settings, additional_kwargs=dict(), internal_settings=dict(),
                           common_settings=dict()):
    for tag in project_settings:
        project_settings[tag] = evaluate_tag_values(tag, project_settings[tag], common_dict=common_settings,
                                                    internal_dict=internal_settings,
                                                    additional_dict=additional_kwargs)
    return project_settings


def evaluate_tag_values(tag, tag_dict, common_dict=dict(), additional_dict=dict(), internal_dict=dict()):
    attrs_dict = dict(tag=tag, is_default_value=False, fatal=False, conditions=list(), default_values=list(),
                      common_dict=common_dict, additional_dict=additional_dict, is_default=False,
                      internal_dict=internal_dict)
    for section in ["attrs_constraints", "vars_constraints"]:
        for item in sorted(list(tag_dict[section])):
            found, conditions = check_conditions_generic(get_key_value, tag_dict[section][item]["conditions"],
                                                         common_dict=common_dict, additional_dict=additional_dict,
                                                         internal_dict=internal_dict, keep_not_found=True)
            tag_dict[section][item]["conditions"] = conditions
            for (i, value) in enumerate(list(tag_dict[section][item]["default_values"])):
                attrs_dict.update(dict(key=item, value=value, skip_values=tag_dict[section][item]["skip_values"],
                                       authorized_types=tag_dict[section][item]["authorized_types"],
                                       authorized_values=tag_dict[section][item]["authorized_values"],
                                       forbidden_patterns=tag_dict[section][item]["forbidden_patterns"],
                                       corrections=tag_dict[section][item]["corrections"],
                                       cases=tag_dict[section][item]["cases"]))
                found, value, _ = find_value(**attrs_dict)
                if found:
                    tag_dict[section][item]["default_values"][i] = value
    return tag_dict


def find_value(tag, key, value, is_default_value=True, conditions=list(), skip_values=list(), authorized_types=False,
               authorized_values=False, forbidden_patterns=list(), default_values=list(), fatal=False, is_default=False,
               common_dict=dict(), additional_dict=dict(), corrections=list(), cases=list(), output_key=None,
               num_type="str", internal_dict=dict()):
    return find_value_generic(get_key_value_func=get_key_value, tag=tag, key=key, value=value,
                              is_default_value=is_default_value, conditions=conditions, skip_values=skip_values,
                              authorized_types=authorized_types, authorized_values=authorized_values,
                              forbidden_patterns=forbidden_patterns, default_values=default_values, fatal=fatal,
                              is_default=is_default, common_dict=common_dict, additional_dict=additional_dict,
                              corrections=corrections, cases=cases, output_key=output_key, num_type=num_type,
                              internal_dict=internal_dict)


def get_key_value(key_value, common_dict=dict(), additional_dict=dict(), internal_dict=dict()):
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
                keys_resolve = [get_key_value(key_value=key, common_dict=common_dict, additional_dict=additional_dict,
                                              internal_dict=internal_dict)
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
                                                 additional_dict=additional_dict, internal_dict=internal_dict)
                        i = 0
                        while found and i < len(keys_values):
                            if value is None:
                                found = False
                            elif isinstance(value, (list, tuple)):
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
                                         additional_dict=additional_dict, internal_dict=internal_dict)
            # Take into account format
            if found and key_type not in ["combine", ]:
                if fmt is not None and isinstance(value, list):
                    value = fmt.format(*value)
                elif isinstance(value, list) and len(value) == 1:
                    value = value[0]
                elif fmt is not None:
                    value = fmt.format(value)
            if found and isinstance(value, six.string_types):
                value = value.strip()
            if found and func is not None:
                found, value = apply_function_generic(get_key_value, *func, is_value=True, value=value,
                                                      additional_dict=additional_dict, common_dict=common_dict,
                                                      internal_dict=internal_dict)
        else:
            if key_type is not None:
                found, value = get_value(key_type, key=None, src=None, common_dict=common_dict,
                                         additional_dict=additional_dict, internal_dict=internal_dict)
            else:
                found = False
                value = None
            if func is not None:
                found, value = apply_function_generic(get_key_value, *func, value=None, is_value=False,
                                                      additional_dict=additional_dict, common_dict=common_dict,
                                                      internal_dict=internal_dict)
                found = True
            if found:
                if fmt is None and isinstance(value, list):
                    value = value[0]
                elif fmt is not None and isinstance(value, list):
                    value = fmt.format(*value)
                elif fmt is not None:
                    value = fmt.format(value)
        return found, value
    elif isinstance(key_value, six.string_types):
        if key_value in ["True", ]:
            key_value = True
        elif key_value in ["False", ]:
            key_value = False
        elif key_value in ["dict()", ]:
            key_value = dict()
        elif key_value in ["list()", ]:
            key_value = list()
        elif key_value in ["None", ]:
            key_value = None
        return True, key_value
    else:
        return True, key_value


def get_value(key_type, key, src, common_dict=dict(), additional_dict=dict(), internal_dict=dict()):
    found = False
    value = None
    if key_type in ["common", ] and key in common_dict:
        value = common_dict[key]
        found = True
    elif key_type in ["internal", ] and key in internal_dict:
        value = internal_dict[key]
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
    elif key_type in ["scope", ]:
        value = get_scope()
        found = True
        if key is not None and key in value.__dict__:
            value = value.__getattribute__(key)
        elif key is not None:
            found = False
    elif key_type in ["variable", ] and "variable" in additional_dict and \
            key in additional_dict["variable"].__dict__:
        value = additional_dict["variable"].__getattribute__(key)
        found = True
    elif key_type in ["laboratory", ]:
        if key is None:
            value = format_dict_for_printing("lset")
            found = True
        elif is_key_in_lset(key):
            value = get_variable_from_lset_without_default(key)
            found = True
    elif key_type in ["simulation", ]:
        if key is None:
            value = format_dict_for_printing("sset")
            found = True
        elif is_key_in_sset(key):
            value = get_variable_from_sset_without_default(key)
            found = True
    elif key_type in ["json", ]:
        found, value = get_key_value(key_value=src, common_dict=common_dict, additional_dict=additional_dict,
                                     internal_dict=internal_dict)
        if found:
            value = read_json_content(value)
            if key in value:
                value = value[key]
            elif key is not None:
                found = False
    elif key_type in ["combine", ]:
        raise Exception("Should not pass here")
    return found, value
