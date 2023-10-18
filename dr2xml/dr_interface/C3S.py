#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between the C3S data request (C3S_DR.py) and dr2xml.
"""
from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict

from .C3S_DR import c3s_nc_dims, c3s_nc_coords, c3s_nc_comvars, c3s_nc_vars
from .definition import ListWithItems
from .definition import Scope as ScopeBasic
from .definition import DataRequest as DataRequestBasic
from .definition import SimpleObject
from .definition import SimpleCMORVar as SimpleCMORVarBasic
from .definition import SimpleDim as SimpleDimBasic


scope = None
data_request = None


class DataRequest(DataRequestBasic):
    def get_version(self):
        return "No Data Request"

    def get_list_by_id(self, collection, **kwargs):
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

    def get_single_levels_list(self):
        return list()

    def get_grids_dict(self):
        return OrderedDict()

    def get_dimensions_dict(self):
        return OrderedDict()


class Scope(ScopeBasic):

    def __init__(self, scope=None):
        super().__init__(scope=scope)

    def get_request_link_by_mip(self, mips_list):
        return list()

    def get_vars_by_request_link(self, request_link, pmax):
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


class SimpleCMORVar(SimpleCMORVarBasic):
    @classmethod
    def get_from_dr(cls, input_var):
        return input_var


class SimpleDim(SimpleDimBasic):
    @classmethod
    def get_from_dr(cls, input_dim):
        return input_dim

