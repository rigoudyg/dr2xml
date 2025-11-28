#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface to project settings from dr2xml
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import os
from importlib.machinery import SourceFileLoader

from .py_settings_interface import get_variable_from_lset_with_default_in_lset, get_variable_from_lset_with_default, \
    get_variable_from_lset_without_default
from dr2xml.projects.projects_interface_definitions import ParameterSettings


def initialize_project_settings(dirname, doc_writer=False):
    # Read content from json file
    project_filename = get_variable_from_lset_with_default_in_lset(key="project_settings", key_default="project",
                                                                   default="CMIP6")
    # Merge with parent if needed
    project_filename, init_values, internal_values, common_values, project_settings = merge_project_settings(project_filename)
    # Complete and clean project settings
    project_settings = solve_settings(project_settings)
    # If asked, save the settings into a dedicated file
    save_project_settings = get_variable_from_lset_with_default("save_project_settings", None)
    if save_project_settings is not None:
        write_project_content(save_project_settings, init_values, internal_values, common_values, project_settings, dirname)
    if doc_writer:
        write_project_documentation(init_values, internal_values, common_values, project_settings, dirname,
                                    get_variable_from_lset_without_default("project"))
    return init_values, internal_values, common_values, project_settings, ""


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


def write_project_content(target, init_values, internal_values, common_values, project_settings, dirname):
    with open(os.sep.join([dirname, target]), "w") as target_fic:
        target_fic.write(os.linesep.join([
            "from dr2xml.projects.projects_interface_definitions import *",
            "init_values = %s" % init_values,
            "internal_values = %s" % internal_values,
            "common_values = %s" % common_values,
            "project_settings = %s" % project_settings]))


def merge_project_settings(project_filename):
    # Initialize settings from current filename
    project_filename, parent_project_filename, init_values, internal_values, common_values, project_settings = \
        read_project_settings(filename=project_filename)
    if parent_project_filename is not None:
        # Merge parent settings
        parent_project_filename, parent_init_values, parent_internal_values, parent_common_values, parent_project_settings = \
            merge_project_settings(project_filename=parent_project_filename)
        if project_filename != parent_project_filename:
            init_values = update_settings(init_values, parent_init_values)
            internal_values = update_settings(internal_values, parent_internal_values)
            common_values = update_settings(common_values, parent_common_values)
            project_settings = update_settings(project_settings, parent_project_settings)
        else:
            raise ValueError("The settings %s reference itself as parent settings. Stop" % project_filename)
    return project_filename, init_values, internal_values, common_values, project_settings


def update_settings(current_settings, parent_settings):
    for value in current_settings:
        if value in parent_settings:
            parent_settings[value].update(current_settings[value])
        else:
            parent_settings[value] = current_settings[value]
    return parent_settings


def read_project_settings(filename):
    if not os.path.isfile(filename):
        filename = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "..", "projects",
                                "{}.py".format(filename)])
    file_module = SourceFileLoader(os.path.basename(filename), filename).load_module(os.path.basename(filename))
    if "parent_project_settings" in file_module.__dict__:
        parent_project_filename = file_module.__getattribute__("parent_project_settings")
    else:
        parent_project_filename = None
    if "init_values" in file_module.__dict__:
        init_values = file_module.__getattribute__("init_values")
    else:
        init_values = dict()
    if "internal_values" in file_module.__dict__:
        internal_values = file_module.__getattribute__("internal_values")
    else:
        internal_values = dict()
    if "common_values" in file_module.__dict__:
        common_values = file_module.__getattribute__("common_values")
    else:
        common_values = dict()
    if "project_settings" in file_module.__dict__:
        project_settings = file_module.__getattribute__("project_settings")
    else:
        project_settings = dict()
    return filename, parent_project_filename, init_values, internal_values, common_values, project_settings


def solve_values(values, init_dict=dict(), internal_dict=dict(), common_dict=dict(), additional_dict=dict(),
                 allow_additional_keytypes=True, only_init=False, project_funcs=""):
    if only_init and values not in ["internal", ]:
        raise ValueError("Only_init can be True only for internal dict resolution")
    if values in ["init", ]:
        args_dict = dict(additional_dict=additional_dict, raise_on_error=False,
                         allow_additional_keytypes=allow_additional_keytypes, project_funcs=project_funcs)
        dict_name = "init_dict"
        current_dict = init_dict
    elif values in ["internal", ]:
        args_dict = dict(init_dict=init_dict, additional_dict=additional_dict, raise_on_error=False,
                         allow_additional_keytypes=allow_additional_keytypes, project_funcs=project_funcs)
        dict_name = "internal_dict"
        current_dict = internal_dict
    elif values in ["common", ]:
        args_dict = dict(init_dict=init_dict, internal_dict=internal_dict, additional_dict=additional_dict, raise_on_error=False,
                         allow_additional_keytypes=allow_additional_keytypes, project_funcs=project_funcs)
        dict_name = "common_dict"
        current_dict = common_dict
    else:
        raise ValueError("Could not solve values for setting %s" % values)
    rep = dict()
    if only_init is False and values in ["internal", ]:
        items_to_treat = [elt for (elt, val) in current_dict.items() if not isinstance(val, ParameterSettings)]
        for item in items_to_treat:
            rep[item] = current_dict.pop(item)
    else:
        rep = dict()

    items_to_treat = sorted(list(current_dict))
    if only_init:
        items_to_treat = [elt for elt in items_to_treat if (isinstance(current_dict[elt], ParameterSettings) and current_dict[elt].init is True)]
    test = True
    while len(items_to_treat) > 0 and test:
        resolved_items = list()
        for item in items_to_treat:
            val = current_dict[item]
            if isinstance(val, ParameterSettings):
                found, value = val.find_value(**{dict_name: rep}, **args_dict)
                if found:
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
    if only_init:
        for item in sorted(list(current_dict)):
            if item in rep:
                raise ValueError("Case should not happened")
            else:
                rep[item] = current_dict.pop(item)
    if not test:
        raise ValueError("Could not evaluate all %s values: the following are missing %s" % (values, items_to_treat))
    return rep


def solve_settings(settings):
    for tag in settings:
        settings[tag].complete_and_clean()
    return settings
