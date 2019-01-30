#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Configuration variables and associated tools.
"""

from utils import dr2xml_error


context_index = None


def set_config_variable(variable, value):
    if variable == "context_index":
        global context_index
        context_index = value
    else:
        raise dr2xml_error("Unknown configuration variable %s.", variable)


def get_config_variable(variable):
    if variable == "context_index":
        return context_index
    else:
        raise dr2xml_error("Unknown configuration variable %s.", variable)
