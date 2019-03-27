#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Configuration variables and associated tools.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from utils import dr2xml_error


# General variables
version = "1.16"  # dr2xml version

# CMIP6 variables
conventions = "CF-1.7 CMIP-6.2"


context_index = None


# Functions to deal with those configuration variables
def set_config_variable(variable, value):
    if variable == "context_index":
        global context_index
        context_index = value
    else:
        raise dr2xml_error("Unknown configuration variable %s." % variable)


def get_config_variable(variable):
    if variable == "context_index":
        return context_index
    elif variable == "conventions":
        return conventions
    elif variable == "version":
        return version
    else:
        raise dr2xml_error("Unknown configuration variable %s." % variable)
