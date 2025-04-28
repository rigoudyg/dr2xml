#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface if no data request should be used.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict, defaultdict
import sys
import os

from utilities.logger import get_logger
from .definition import ListWithItems
from .definition import DataRequest as DataRequestBasic
from .definition import SimpleObject
from .definition import SimpleCMORVar as SimpleCMORVarBasic
from .definition import SimpleDim as SimpleDimBasic
from dr2xml.settings_interface import get_settings_values
from ..utils import Dr2xmlError, is_elt_applicable

data_request_path = get_settings_values("internal", "data_request_path")
sys.path.append(data_request_path)
os.environ["CMIP7_DR_API_CONFIGFILE"] = get_settings_values("internal", "data_request_config")
from data_request_api.query.data_request import DataRequest as CMIP7DataRequest
from data_request_api.content.dump_transformation import get_transformed_content


data_request = None


class DataRequest(DataRequestBasic):
    def get_version(self):
        return self.data_request.version

    def get_list_by_id(self, collection, **kwargs):
        logger = get_logger()
        if collection in ["CMORvar", "var"]:
            rep = self.get_element_uid(id=None, elt_type="variable")
        elif collection in ["structure_title", "spatial_shape", "coordinates_and_dimensions"]:
            rep = self.get_element_uid(id=None, elt_type=collection)
        else:
            logger.error(f"Unable to find out collection {collection}")
            raise ValueError(f"Unable to find out collection {collection}")
        if rep not in ["CMORvar", ]:
            new_rep, rep = rep, ListWithItems()
            rep.extend(new_rep)
        return rep

    def get_variables_per_label(self, debug=list()):
        logger = get_logger()
        rep = OrderedDict()
        for v in self.get_list_by_id("var"):
            if v.label not in rep:
                rep[v.label] = []
                if v.label in debug:
                    logger.debug("Adding %s" % v.label)
            refs = self.get_request_by_id_by_sect(v.id, 'CMORvar')
            for r in refs:
                ref = self.get_element_uid(r, elt_type="variable")
                rep[v.label].append(ref)
                if v.label in debug:
                    logger.debug("Adding CmorVar %s(%s) for %s" % (v.label, ref.mipTable, ref.label))
        return rep

    def get_sectors_list(self):
        return ListWithItems()

    def get_experiment_label(self, experiment):
        return self.data_request.find_element("experiment", experiment).label

    def get_cmor_var_id_by_label(self, label):
        return self.data_request.find_element("variable", label).id

    def get_element_uid(self, id=None, elt_type=None, error_msg=None, raise_on_error=False, check_print_DR_errors=True,
                        check_print_stdnames_error=False, **kwargs):
        logger = get_logger()
        if elt_type is None:
            raise ValueError("Unable to find out uid with elt_type None")
        if id is None:
            return self.data_request.get_elements_per_kind(elt_type)
        else:
            if elt_type in ["dim", ]:
                elt_type = "dimension"
            rep = self.data_request.find_element(element_type=elt_type, value=id, default=None)
            if rep is None:
                if error_msg is None:
                    error_msg = "DR Error: issue with %s" % id
                if raise_on_error:
                    raise Dr2xmlError(error_msg)
                elif check_print_DR_errors and self.print_DR_errors:
                    logger.error(error_msg)
                elif check_print_stdnames_error and self.print_DR_stdname_errors:
                    logger.error(error_msg)
            else:
                if elt_type in ["variable", ]:
                    rep = SimpleCMORVar.get_from_dr(rep, id=id, **kwargs)
                elif elt_type in ["dimension", ]:
                    rep = SimpleDim.get_from_dr(rep, id=id)
            return rep

    def get_request_by_id_by_sect(self, id, request):
        logger = get_logger()
        if request in ["CMORvar", ]:
            return [self.get_element_uid(id=id, elt_type="variable").id, ]
        else:
            logger.error(f"Unable to find out collection {request}")
            raise ValueError(f"Unable to find out collection {request}")

    def get_single_levels_list(self):
        rep = self.get_list_by_id("coordinates_and_dimensions")
        rep = [elt for elt in rep if elt.cf_category in ["coordinate", ] and elt.axis_flag in ["Z", ]]
        return sorted(rep)

    def get_grids_dict(self):
        return OrderedDict()

    def get_dimensions_dict(self):
        rep = OrderedDict()
        for spshp in self.get_list_by_id("spatial_shape"):
            dims = [elt.name for elt in spshp.dimensions]
            new_dims = list()
            for key in ["longitude", "latitude"]:
                if key in dims:
                    dims.remove(key)
                    new_dims.append(key)
            new_dims.extend(sorted(dims))
            rep[new_dims] = spshp.name
        return rep

    def get_cmorvars_list(self, select_mips, select_max_priority, select_included_vars, select_excluded_vars,
                          select_included_tables, select_excluded_tables, select_excluded_pairs,
                          experiment_filter=False, **kwargs):
        rep = defaultdict(set)
        var_list = self.data_request.filter_elements_per_request("variables", operation="all", skip_if_missing=False,
                                                                 requests=dict(max_priority_level=select_max_priority))
        if len(select_mips) > 0:
            var_list = self.data_request.filter_elements_per_request(var_list, operation="any",
                                                                     skip_if_missing=False,
                                                                     requests=dict(mips=list(select_mips)))
        for var in var_list:
            dr_var = SimpleCMORVar.get_from_dr(var, **kwargs)
            if is_elt_applicable(dr_var.mipTable, excluded=select_excluded_tables, included=select_included_tables) and\
                    is_elt_applicable(dr_var.mipVarLabel, excluded=select_excluded_vars, included=select_included_vars) \
                    and is_elt_applicable((dr_var.mipVarLabel, dr_var.mipTable), excluded=select_excluded_pairs):
                rep[dr_var.id] = rep[dr_var.id] | set(dr_var.grids)
        return rep


def initialize_data_request():
    global data_request
    if data_request is None:
        internal_dict = get_settings_values("internal")
        data_request_content_version = internal_dict["data_request_content_version"]
        content = get_transformed_content(version=data_request_content_version,
                                          force_retrieve=False)
        data_request = DataRequest(CMIP7DataRequest.from_separated_inputs(**content))
    return data_request


def get_data_request():
    if data_request is None:
        return initialize_data_request()
    else:
        return data_request


def normalize_grid(grid):
    return grid


class SimpleCMORVar(SimpleCMORVarBasic):
    @classmethod
    def get_from_dr(cls, input_var, **kwargs):
        sdims = OrderedDict()
        product_of_other_dims = 1
        spatial_shape_dimensions = input_var.spatial_shape.dimensions
        if not isinstance(spatial_shape_dimensions, list):
            spatial_shape_dimensions = list()
        for sdim in spatial_shape_dimensions:
            sdim = SimpleDim.get_from_dr(sdim, **kwargs)
            sdims[sdim.name] = sdim
            product_of_other_dims *= sdim.dimsize
        cell_measures = input_var.cell_measures
        if isinstance(cell_measures, list):
            cell_measures = [elt if isinstance(elt, str) else elt.name for elt in cell_measures]
        elif isinstance(cell_measures, str):
            cell_measures = [cell_measures, ]
        else:
            cell_measures = [cell_measures.name, ]
        cell_methods = str(input_var.cell_methods.cell_methods)
        logger = get_logger()
        logger.debug(f"Variable considered: {input_var.name}")
        return cls(from_dr=True,
                   type=str(input_var.type),
                   modeling_realm=[str(realm.id) for realm in input_var.modelling_realm],
                   label=str(input_var.physical_parameter.name),
                   mipVarLabel=str(input_var.physical_parameter.name),
                   label_without_psuffix=str(input_var.physical_parameter.name),
                   label_non_ambiguous=str(input_var.name),
                   frequency=str(input_var.cmip7_frequency.name),
                   mipTable=str(input_var.cmip6_tables_identifier.name),
                   description=str(input_var.description),
                   stdname=str(input_var.physical_parameter.cf_standard_name.name),
                   units=str(input_var.physical_parameter.units),
                   long_name=str(input_var.physical_parameter.title),
                   sdims=sdims,
                   other_dims_size=product_of_other_dims,
                   cell_methods=cell_methods,
                   cm=input_var.cell_methods.cell_methods,
                   cell_measures=cell_measures,
                   spatial_shp=str(input_var.spatial_shape.name),
                   temporal_shp=str(input_var.temporal_shape.name),
                   id=input_var.id,
                   cmvar=input_var,
                   Priority=data_request.data_request.find_priority_per_variable(input_var)
                   )


class SimpleDim(SimpleDimBasic):
    @classmethod
    def get_from_dr(cls, input_dim, **kwargs):
        return cls(
            from_dr=True,
            label=str(input_dim.name),
            stdname=str(input_dim.cf_standard_name),
            long_name=str(input_dim.title),
            positive=str(input_dim.positive_direction),
            requested=str(input_dim.requested_values),
            value=str(input_dim.value),
            out_name=str(input_dim.output_name),
            units=str(input_dim.units),
            boundsRequested=input_dim.requested_bounds,
            axis=str(input_dim.axis_flag),
            type=str(input_dim.type),
            coords=input_dim,
            title=str(input_dim.title),
            name=str(input_dim.name)
        )
