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


data_request = None
DataRequest = DefaultClass
initialize_data_request = defaultfunction
get_data_request = defaultfunction
normalize_grid = defaultfunction
SimpleObject = DefaultClass
SimpleCMORVar = DefaultClass
SimpleDim = DefaultClass


def get_dr_object(key):
    if key in ["get_data_request", ]:
        return get_data_request()
    elif key in ["normalize_grid", ]:
        return normalize_grid
    elif key in ["SimpleCMORVar", ]:
        return SimpleCMORVar()
    elif key in ["SimpleDim", ]:
        return SimpleDim()
    else:
        raise ValueError("Unknown data request object %s from interface" % key)


def load_correct_dr():
    global data_request, DataRequest, initialize_data_request, get_data_request, \
        normalize_grid, SimpleDim, SimpleObject, SimpleCMORVar

    data_request_version = get_settings_values("internal", "data_request_used")

    if data_request_version in ["CMIP6", ]:
        from .CMIP6 import data_request, DataRequest, initialize_data_request, get_data_request, \
            normalize_grid, SimpleDim, SimpleObject, SimpleCMORVar
    elif data_request_version in ["CMIP7", ]:
        from .CMIP7 import data_request, DataRequest, initialize_data_request, get_data_request, \
            normalize_grid, SimpleDim, SimpleObject, SimpleCMORVar
    elif data_request_version in ["no", "none", "None", None]:
        from .no import data_request, DataRequest, initialize_data_request, get_data_request, \
            normalize_grid, SimpleDim, SimpleObject, SimpleCMORVar
    elif data_request_version in ["C3S", ]:
        from .C3S import data_request, DataRequest, initialize_data_request, get_data_request, \
            normalize_grid, SimpleDim, SimpleObject, SimpleCMORVar
    else:
        raise ValueError("The data request specified (%s) is not known." % data_request_version)
