#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface to get and set laboratory and simulations dictionaries.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import copy
from collections import OrderedDict

from logger import get_logger

# Internal settings for dr2xml
internal_settings = None
# Common settings
common_settings = None
# Project settings
project_settings = None
# Internal values used everywhere in dr2xml
internal_values = None


def initialize_settings(lset=None, sset=None, force_reset=False, **kwargs):
    global internal_settings, common_settings, project_settings
    if force_reset:
        internal_settings = None
        common_settings = None
        project_settings = None
    # Initialize python settings dictionaries
    from .py_settings_interface import initialize_dict
    initialize_dict(new_lset=lset, new_sset=sset)
    # Read, merge and format complete settings linked to project
    from .py_project_interface import initialize_project_settings, solve_values, solve_settings
    internal_settings, common_settings, project_settings = initialize_project_settings(kwargs["dirname"])
    # Solve internal settings
    internal_settings = solve_values("internal", internal_dict=internal_settings, additional_dict=kwargs,
                                     allow_additional_keytypes=False)
    from dr2xml.dr_interface import load_correct_dr
    load_correct_dr()
    # Initialize laboratory sources
    from dr2xml.laboratories import initialize_laboratory_settings
    initialize_laboratory_settings()
    # Solve common settings
    common_settings = solve_values("common", common_dict=common_settings, internal_dict=internal_settings,
                                   additional_dict=kwargs)
    # Solve project_settings
    project_settings = solve_settings(project_settings, internal_dict=internal_settings,
                                      common_dict=common_settings, additional_dict=kwargs)
    # Initialize internal values
    initialize_internal_values()


def initialize_internal_values():
    set_internal_value(key="rls_for_all_experiments", value=None)
    set_internal_value(key="global_rls", value=None)
    set_internal_value(key="sn_issues", value=OrderedDict())
    set_internal_value(key="print_multiple_grids", value=False)
    set_internal_value(key="grid_choice", value=None)


def set_internal_value(key, value, action=False):
    global internal_values
    if not isinstance(internal_values, dict):
        internal_values = dict()
    if action in ["append", ]:
        if key in internal_values:
            internal_values[key].append(copy.deepcopy(value))
        else:
            internal_values[key] = [copy.deepcopy(value), ]
    elif action in ["update", ]:
        if key in internal_values:
            internal_values[key].update(copy.deepcopy(value))
        else:
            internal_values[key] = copy.deepcopy(value)
    else:
        internal_values[key] = copy.deepcopy(value)


def get_settings_values(*args, **kwargs):
    is_default = kwargs.get("is_default", False)
    default = kwargs.get("default", None)
    must_copy = kwargs.get("must_copy", False)
    setting = args[0]
    if len(args) > 1:
        args = args[1:]
    else:
        args = list()
    logger = get_logger()
    if setting in ["internal", ]:
        settings = internal_settings
    elif setting in ["common", ]:
        settings = common_settings
    elif setting in ["project", ]:
        settings = project_settings
    elif setting in ["internal_values", ]:
        settings = internal_values
    else:
        logger.error("Unknown settings %s" % setting)
        raise ValueError("Unknown settings %s" % setting)
    test = True
    i = 0
    while test and i < len(args):
        if args[i] in settings:
            settings = settings[args[i]]
            i += 1
        else:
            test = False
    if test and must_copy:
        return copy.deepcopy(settings)
    elif test:
        return settings
    elif not is_default:
        logger.error("Could not find a proper value: %s not in %s" % (args[i], settings))
        raise ValueError("Could not find a proper value: %s not in %s" % (args[i], settings))
    else:
        return default
