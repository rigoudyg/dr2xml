#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between data request and dr2xml
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.settings_interface import get_settings_values


def defaultfunction():
    raise NotImplementedError()


class DefaultClass(object):
    def __init__(self, *args, **kwargs):
        defaultfunction()


scope = None
data_request = None
DataRequest = DefaultClass
initialize_data_request = defaultfunction
get_data_request = defaultfunction
initialize_scope = defaultfunction
get_scope = defaultfunction
set_scope = defaultfunction
normalize_grid = defaultfunction
SimpleObject = DefaultClass
SimpleCMORVar = DefaultClass
SimpleDim = DefaultClass


def load_correct_dr():
    global scope, data_request, DataRequest, initialize_data_request, get_data_request, initialize_scope, get_scope, \
        set_scope, normalize_grid, SimpleDim, SimpleObject, SimpleCMORVar

    data_request_version = get_settings_values("internal", "data_request_used")

    if data_request_version in ["CMIP6", ]:
        from .CMIP6 import scope, data_request, DataRequest, initialize_data_request, get_data_request, \
            initialize_scope, get_scope, set_scope, normalize_grid, SimpleDim, SimpleObject, SimpleCMORVar
    elif data_request_version in ["no", "none", "None", None]:
        from .no import scope, data_request, DataRequest, initialize_data_request, get_data_request, initialize_scope, \
            get_scope, set_scope, normalize_grid, SimpleDim, SimpleObject, SimpleCMORVar
    else:
        raise ValueError("The data request specified (%s) is not known." % data_request_version)
