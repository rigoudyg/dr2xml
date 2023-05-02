#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface if no data request should be used.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from .definition import Scope, ListWithItems
from .definition import DataRequest as DataRequestBasic


scope = None
data_request = None


class DataRequest(DataRequestBasic):
    def get_version(self):
        return "No Data Request"

    def get_list_by_id(self, collection):
        return ListWithItems()

    def get_sectors_list(self):
        return self.get_list_by_id("grids")

    def get_experiment_label(self, experiment):
        return ""

    def get_cmor_var_id_by_label(self, label):
        return list()

    def get_element_uid(self, id=None, **kwargs):
        if id is None:
            return list()
        else:
            return None

    def get_request_by_id_by_sect(self, id, request):
        return list()


def initialize_data_request():
    global data_request
    if data_request is None:
        data_request = DataRequest(print_DR_errors=False, print_DR_stdname_errors=False)
    return data_request


def get_data_request():
    if data_request is None:
        return initialize_data_request()
    else:
        return data_request


def initialize_scope(tier_max):
    global scope
    dq = get_data_request()
    if scope is None:
        scope = Scope()
    return scope


def get_scope(tier_max=None):
    if scope is None:
        return initialize_scope(tier_max)
    else:
        return scope


def set_scope(sc):
    if sc is not None:
        global scope
        scope = sc


def normalize_grid(grid):
    return grid


def correct_data_request_dim(dim):
    pass


def correct_data_request_variable(variable):
    pass
