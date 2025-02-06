#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between the C3S data request (C3S_DR.py) and dr2xml.
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import os
from collections import OrderedDict, defaultdict
from importlib.machinery import SourceFileLoader

from .definition import ListWithItems
from .definition import Scope as ScopeBasic
from .definition import DataRequest as DataRequestBasic
from .definition import SimpleObject
from .definition import SimpleCMORVar as SimpleCMORVarBasic
from .definition import SimpleDim as SimpleDimBasic
from dr2xml.settings_interface import get_settings_values

data_request_path = get_settings_values("internal", "data_request_path")
if data_request_path is not None:
    data_request_filename = os.path.basename(data_request_path)
    data_request_module = SourceFileLoader(data_request_filename, data_request_path).load_module(data_request_filename)
    c3s_nc_dims = data_request_module.__getattribute__("c3s_nc_dims")
    c3s_nc_coords = data_request_module.__getattribute__("c3s_nc_coords")
    c3s_nc_comvars = data_request_module.__getattribute__("c3s_nc_comvars")
    c3s_nc_vars = data_request_module.__getattribute__("c3s_nc_vars")
else:
    from .C3S_DR import c3s_nc_dims, c3s_nc_coords, c3s_nc_comvars, c3s_nc_vars


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

    def get_element_uid(self, id=None, elt_type=None, **kwargs):
        if elt_type in ["dim", ]:
            input_data = c3s_nc_coords
        elif elt_type in ["variable", ]:
            input_data = c3s_nc_vars
        elif elt_type in ["common_variable", ]:
            input_data = c3s_nc_comvars
        else:
            input_data = dict()
        if id is None:
            return sorted(list(input_data))
        else:
            rep = input_data.get(id, None)
            if rep is not None:
                if elt_type in ["dim", ]:
                    rep = SimpleDim.get_from_dr(rep, id=id, **kwargs)
                elif elt_type in ["variable", "common_variable"]:
                    rep = SimpleCMORVar.get_from_dr(rep, id=id, **kwargs)
            return rep

    def get_request_by_id_by_sect(self, id, request):
        return list()

    def get_single_levels_list(self):
        return list()

    def get_grids_dict(self):
        return OrderedDict()

    def get_dimensions_dict(self):
        return OrderedDict()

    def get_cmorvars_list(self, sizes=None, **kwargs):
        rep = defaultdict(set)
        for id in self.get_element_uid(elt_type="variable"):
            for grid in self.get_element_uid(id=id, elt_type="variable").grids:
                rep[id].add(grid)
        return rep, list()


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
    def get_from_dr(cls, input_var, id=None, **kwargs):
        input_var_dict = dict()
        input_var_dict["type"] = "cmor"
        input_var_dict["modeling_realm"] = input_var["globattrs"]["modeling_realm"]
        input_var_dict["mipVarLabel"] = id
        input_var_dict["label"] = id
        input_var_dict["label_without_psuffix"] = id
        input_var_dict["label_non_ambiguous"] = id
        input_var_dict["frequency"] = input_var["globattrs"]["frequency"]
        input_var_dict["stdname"] = input_var["attributes"]["standard_name"]
        input_var_dict["long_name"] = input_var["attributes"]["long_name"]
        input_var_dict["units"] = input_var["attributes"]["units"]
        sdims_dict = OrderedDict()
        product_of_other_dims = 1
        for sdim_id in input_var["dimensions"] + input_var["auxcoords"]:
            if sdim_id in input_var["modify"]:
                modify_dict = copy.deepcopy(input_var["modify"][sdim_id])
            else:
                modify_dict = dict()
            sdim = data_request.get_element_uid(sdim_id, elt_type="dim", modify_value=modify_dict)
            product_of_other_dims *= sdim.dimsize
            sdims_dict[sdim_id] = sdim
        input_var_dict["sdims"] = copy.deepcopy(sdims_dict)
        input_var_dict["other_dims_size"] = product_of_other_dims
        input_var_dict["cell_methods"] = input_var["attributes"]["cell_methods"]
        input_var_dict["coordinates"] = input_var["attributes"]["coordinates"]
        if "_FillValue" in input_var["attributes"]:
            input_var_dict["missing"] = input_var["attributes"]["_FillValue"]
        spatial_shape = input_var["globattrs"]["level_type"]
        spatial_shape_conversion = dict(surface="XY-na", pressure="XY-A")
        input_var_dict["spatial_shp"] = spatial_shape_conversion.get(spatial_shape, spatial_shape)
        input_var_dict["mipTable"] = "C3S"
        return cls(from_dr=True, **input_var_dict)


class SimpleDim(SimpleDimBasic):
    @classmethod
    def get_from_dr(cls, input_dim, id=None, modify_value=dict(), **kwargs):
        input_dim_dict = dict()
        if "axis" in input_dim["attributes"]:
            input_dim_dict["axis"] = input_dim["attributes"]["axis"]
        input_dim_dict["stdname"] = input_dim["attributes"]["standard_name"]
        input_dim_dict["long_name"] = input_dim["attributes"]["long_name"]
        input_dim_dict["units"] = input_dim["attributes"]["units"]
        if "bounds" in input_dim["attributes"]:
            input_dim_dict["bounds"] = input_dim["attributes"]["bounds"]
        if "boundsValues" in input_dim:
            input_dim_dict["boundsValues"] = input_dim["boundsValues"]
        input_dim_dict["label"] = id
        if len(modify_value) > 0:
            input_dim_dict["label"] = "_".join([input_dim_dict["label"], str(modify_value["values"])])
        input_dim_dict["value"] = modify_value.get("values", input_dim["values"])
        if len(modify_value) > 0 and "positive" in modify_value["attributes"]:
            input_dim_dict["positive"] = modify_value["attributes"]["positive"]
        elif "positive" in input_dim["attributes"]:
            input_dim_dict["positive"] = input_dim["attributes"]["positive"]
        input_dim_dict["name"] = id
        input_dim_dict["type"] = "float"
        return cls(from_dr=True, **input_dim_dict)
