#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration variables and associated tools.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import sys

# Utilities
from collections import OrderedDict

from .utils import Dr2xmlError
import copy


# Python version
python_version = "python" + sys.version[0]

# General variables
version = "3.1"  # dr2xml version

# CMIP6 variables
conventions = "CF-1.7 CMIP-6.2"
# The current code should comply with this version of spec doc at
# https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit
CMIP6_conventions_version = "v6.2.4"

# Variable used for storing index of xml files
context_index = None

# Variable used to store cell method warnings
cell_method_warnings = list()

# Variable used to store compression factor
compression_factor = None

# Variable used to store split_frequencies
splitfreqs = None

# Home vars list
homevars_list = None

# Fields definitions
field_defs = OrderedDict()

# Axis definitions
axis_defs = OrderedDict()

# Grids definitions
grid_defs = OrderedDict()

# Files definitions
file_defs = OrderedDict()

# Scalars definitions
scalar_defs = OrderedDict()

# Domains definitions
domain_defs = OrderedDict()

# Ping variables list
pingvars = list()

# Ping variables references
ping_refs = OrderedDict()


# Functions to deal with those configuration variables
def initialize_config_variables():
    set_config_variable("context_index", None)
    set_config_variable("cell_method_warnings", list())
    set_config_variable("compression_factor", None)
    set_config_variable("splitfreqs", None)
    set_config_variable("homevars_list", None)
    set_config_variable("field_defs", OrderedDict())
    set_config_variable("axis_defs", OrderedDict())
    set_config_variable("grid_defs", OrderedDict())
    set_config_variable("file_defs", OrderedDict())
    set_config_variable("scalar_defs", OrderedDict())
    set_config_variable("domain_defs", OrderedDict())
    set_config_variable("pingvars", list())
    set_config_variable("ping_refs", OrderedDict())


def set_config_variable(variable, value):
    """
    Set the value of the indicated global variable
    """
    if variable in ["python_version", "version", "conventions", "CMIP6_conventions_version", "context_index",
                    "cell_method_warnings", "compression_factor", "splitfreqs", "homevars_list", "field_defs",
                    "axis_defs", "grid_defs", "file_defs", "scalar_defs", "domain_defs", "pingvars", "ping_refs"]:
        globals()[variable] = copy.deepcopy(value)
    else:
        raise Dr2xmlError("Can not set configuration variable %s." % variable)


def get_config_variable(variable, keys=list(), to_change=False):
    """
    Get the value of the indicated global variable.
    """
    if variable not in ["python_version", "version", "conventions", "CMIP6_conventions_version", "context_index",
                        "cell_method_warnings", "compression_factor", "splitfreqs", "homevars_list", "field_defs",
                        "axis_defs", "grid_defs", "file_defs", "scalar_defs", "domain_defs", "pingvars", 
                        "ping_refs"]:
        raise Dr2xmlError("Unknown configuration variable %s." % variable)
    elif to_change:
        rep = copy.deepcopy(globals()[variable])
    else:
        rep = globals()[variable]
    if len(keys) > 0 and isinstance(rep, (dict, OrderedDict)):
        for key in keys:
            rep = rep[key]
    return rep


def add_value_in_list_config_variable(variable, value):
    """
    Add a value to a list-type configuration variable.
    """
    if variable in ["cell_method_warnings", "pingvars"]:
        globals()[variable].append(value)
    else:
        raise Dr2xmlError("Could not add a value to configuration variable %s." % variable)


def add_value_in_dict_config_variable(variable, key, value):
    if variable in ["field_defs", "axis_defs", "grid_defs", "file_defs", "scalar_defs", "domain_defs", "ping_refs"]:
        globals()[variable][key] = value
    else:
        raise Dr2xmlError("Could not add a value to configuration variable %s." % variable)
