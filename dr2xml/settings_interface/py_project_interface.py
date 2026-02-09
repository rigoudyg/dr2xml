#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface to project settings from dr2xml
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import os
import six

from utilities.json_tools import write_json_content, read_json_content
from utilities.logger import get_logger
from .py_settings_interface import get_variable_from_lset_with_default_in_lset, get_variable_from_lset_with_default, \
    get_variable_from_lset_without_default
from dr2xml.projects.projects_interface_definitions import ParameterSettings, TagSettings


def initialize_project_settings(dirname, doc_writer=False):
    # Read content from json file
    project_filename = get_variable_from_lset_with_default_in_lset(key="project_settings", key_default="project",
                                                                   default="CMIP6")
    config = read_json_content(os.sep.join([os.path.dirname(os.path.abspath(__file__)), "..", "projects",
                                            "projects_default_settings.json"]))
    # Merge with parent if needed
    _, project_content = merge_project_settings(project_filename, config=config)
    # Complete and clean project settings
    project_content = solve_settings(project_content, config=config)
    # If asked, save the settings into a dedicated file
    save_project_settings = get_variable_from_lset_with_default("save_project_settings", None)
    if save_project_settings is not None:
        if not save_project_settings.endswith(".json"):
            save_project_settings += ".json"
        if len(os.path.dirname(save_project_settings)) == 0:
            save_project_settings = os.path.sep.join([dirname, save_project_settings])
        write_json_content(save_project_settings, project_content)
    # Transform json dictionary into settings objects
    init_values = turn_dict_to_settings("init", project_content["init"],
                                        project_funcs=project_content["functions_file"])
    internal_values = turn_dict_to_settings("internal", project_content["internal"],
                                            project_funcs=project_content["functions_file"])
    common_values = turn_dict_to_settings("common", project_content["common"],
                                          project_funcs=project_content["functions_file"])
    project_settings = turn_dict_to_settings("project", project_content["project_settings"],
                                             project_funcs=project_content["functions_file"])
    # Write documentations
    if doc_writer:
        write_project_documentation(init_values, internal_values, common_values, project_settings, dirname,
                                    get_variable_from_lset_without_default("project"))
    return init_values, internal_values, common_values, project_settings, project_content["functions_file"]


def write_project_documentation(init_values, internal_values, common_values, project_settings, dirname, project):
    target_filename = os.sep.join([dirname, project + ".rst"])
    content = list()
    content.append("Parameters available for project %s" % project)
    content.append("=" * len(content[0]))
    content.append("")
    content.append("Init values")
    content.append("---------------")
    content.append(".. glossary::")
    content.append("   :sorted:")
    content.append("   ")
    for value in sorted(list(init_values)):
        content.extend(init_values[value].dump_doc())
    content.append("Internal values")
    content.append("---------------")
    content.append(".. glossary::")
    content.append("   :sorted:")
    content.append("   ")
    for value in sorted(list(internal_values)):
        content.extend(internal_values[value].dump_doc())
    content.append("Common values")
    content.append("-------------")
    content.append(".. glossary::")
    content.append("   :sorted:")
    content.append("   ")
    for value in sorted(list(common_values)):
        content.extend(common_values[value].dump_doc())
    content.append("Project settings")
    content.append("----------------")
    content.append(".. glossary::")
    content.append("   :sorted:")
    content.append("   ")
    for value in sorted(list(project_settings)):
        content.extend(project_settings[value].dump_doc())
    with open(target_filename, "w") as fic:
        fic.write(os.linesep.join(content))


def merge_project_settings(project_filename, config):
    # Initialize settings from current filename
    project_filename, project_content = read_project_settings(filename=project_filename)
    parent_project_filename = project_content.get("parent_project_settings")
    if parent_project_filename is not None:
        # Merge parent settings
        parent_project_filename, parent_content = merge_project_settings(project_filename=parent_project_filename,
                                                                         config=config)
        if project_filename != parent_project_filename:
            new_content = copy.deepcopy(parent_content)
            for (element, value) in project_content.items():
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
            project_content = new_content
        else:
            raise ValueError("The settings %s reference itself as parent settings. Stop" % project_filename)
    for element in config:
        default = copy.deepcopy(config[element]["default"])
        if element not in project_content:
            project_content[element] = copy.deepcopy(default)
    if project_content["functions_file"] is not None:
        if not os.path.isfile(project_content["functions_file"]):
            project_content["functions_file"] = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "..", "projects", project_content["functions_file"]])
    return project_filename, project_content


def read_project_settings(filename):
    if not os.path.isfile(filename):
        filename = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "..", "projects", filename])
        if not filename.endswith(".json"):
            filename += ".json"

    content = read_json_content(filename)
    return filename, content


def solve_settings(content, config):
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
                for key in ["attrs_constraints", "comments_constraints", "vars_constraints", "common_constraints"]:
                    if key in content_value:
                        for (subkey, subval) in content_value[key].items():
                            new_subval = copy.deepcopy(default_constraints)
                            new_subval.update(subval)
                            content_value[key][subkey] = new_subval
                    else:
                        content_value[key] = dict()

                for key in ["attrs", "comments", "vars", "common"]:
                    list_expected_keywords = copy.deepcopy(content_value[key + "_list"])
                    list_current_keywords = copy.deepcopy(list(content_value[key + "_constraints"]))
                    for keyword in sorted(list(set(list_current_keywords) - set(list_expected_keywords))):
                        del content_value[key + "_constraints"][keyword]
                    for keyword in sorted(list(set(list_expected_keywords) - set(list_current_keywords))):
                        content_value[key + "_constraints"][keyword] = default_constraints

                content[element][content_elt] = content_value

    return content


def solve_values(values, init_dict=dict(), internal_dict=dict(), common_dict=dict(), additional_dict=dict(),
                 allow_additional_keytypes=True, project_funcs=None, common_tag_dict=dict()):
    if values in ["init", ]:
        args_dict = dict(internal_dict=internal_dict, common_dict=common_dict, additional_dict=additional_dict,
                         raise_on_error=False, allow_additional_keytypes=allow_additional_keytypes)
        dict_name = "init_dict"
        current_dict = init_dict
    elif values in ["internal", ]:
        args_dict = dict(init_dict=init_dict, common_dict=common_dict, additional_dict=additional_dict,
                         raise_on_error=False, allow_additional_keytypes=allow_additional_keytypes,
                         project_funcs=project_funcs)
        dict_name = "internal_dict"
        current_dict = internal_dict
    elif values in ["common", ]:
        args_dict = dict(init_dict=init_dict, internal_dict=internal_dict, additional_dict=additional_dict,
                         raise_on_error=False, allow_additional_keytypes=allow_additional_keytypes,
                         project_funcs=project_funcs)
        dict_name = "common_dict"
        current_dict = common_dict
    elif values in ["common_tag", ]:
        args_dict = dict(init_dict=init_dict, internal_dict=internal_dict, additional_dict=additional_dict,
                         raise_on_error=False, allow_additional_keytypes=allow_additional_keytypes,
                         project_funcs=project_funcs, common_dict=common_dict)
        dict_name = "common_tag"
        current_dict = common_tag_dict
    else:
        raise ValueError("Could not solve values for setting %s" % values)
    rep = dict()

    items_to_treat = sorted(list(current_dict))

    test = True
    while len(items_to_treat) > 0 and test:
        resolved_items = list()
        for item in items_to_treat:
            val = current_dict[item]
            if isinstance(val, ParameterSettings):
                found, value = val.find_value(**{dict_name: rep}, **args_dict)
                if found:
                    if isinstance(value, six.string_types) and "__package-root__" in value:
                        value = value.replace("__package-root__", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                    rep[item] = value
                    del current_dict[item]
                    resolved_items.append(item)
            else:
                raise TypeError("Can only treat ParameterSettings type objects, not %s." % type(val))
        test = len(resolved_items) > 0
        items_to_treat = sorted(list(set(items_to_treat) - set(resolved_items)))
    if not test:
        not_to_solve_items = list()
        for item in items_to_treat:
            if not current_dict[item].fatal:
                del current_dict[item]
                not_to_solve_items.append(item)
        items_to_treat = sorted(list(set(items_to_treat) - set(not_to_solve_items)))
        test = len(items_to_treat) == 0

    if not test:
        raise ValueError("Could not evaluate all %s values: the following are missing %s" % (values, items_to_treat))
    return rep


def turn_dict_to_settings(settings_type, settings, project_funcs=None):
    logger = get_logger()
    rep = dict()
    if settings_type in ["init", "internal", "common"]:
        for (key, val) in settings.items():
            rep[key] = ParameterSettings.from_dict(key, val, additional_keys=False, project_funcs=project_funcs)
    elif settings_type in ["project", ]:
        for (key, val) in settings.items():
            rep[key] = TagSettings.from_dict(key, val, project_funcs=project_funcs)
    else:
        logger.error("Unknown settings type %s" % settings_type)
        raise ValueError("Unknown settings type %s" % settings_type)
    return rep