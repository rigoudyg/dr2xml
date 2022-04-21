#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CFsites-related elements (CFMIP)
A file named cfsites_grid_file_name must be provided at runtime, which
includes a field named cfsites_grid_field_id, defined on an unstructured
grid which is composed of CF sites
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from .config import add_value_in_dict_config_variable
from .xml_interface import DR2XMLElement


cfsites_radix = "cfsites"
cfsites_domain_id = cfsites_radix + "_domain"
cfsites_grid_id = cfsites_radix + "_grid"
cfsites_grid_file_name = cfsites_radix + "_grid"
cfsites_grid_file_id = cfsites_radix + "_file"
cfsites_grid_field_id = cfsites_radix + "_field"


def cfsites_input_filedef():
    """
    Returns a file definition for defining a COSP site grid by reading a field named
    'cfsites_grid_field' in a file named 'cfsites_grid.nc'
    """
    # rep='<file id="%s" name="%s" mode="read" >\n'%\
    file_xml = DR2XMLElement(tag="file", id=cfsites_grid_file_id, name=cfsites_grid_file_name, mode="read",
                             output_freq="1y")
    file_xml.append(DR2XMLElement(tag="field", id=cfsites_grid_field_id, operation="instant", grid_ref=cfsites_grid_id))
    return file_xml


def add_cfsites_in_defs():
    """
    Add grid_definition and domain_definition for cfsites in relevant dicts
    """
    grid_xml = DR2XMLElement(tag="grid", id=cfsites_grid_id)
    grid_xml.append(DR2XMLElement(tag="domain", domain_ref=cfsites_domain_id))
    add_value_in_dict_config_variable(variable="grid_defs", key=cfsites_grid_id, value=grid_xml)

    domain_xml = DR2XMLElement(tag="domain", id=cfsites_domain_id, type="unstructured", prec="8", lat_name="latitude",
                               lon_name="longitude", dim_i_name="site")
    domain_xml.append(DR2XMLElement(tag="generate_rectilinear_domain"))
    domain_xml.append(DR2XMLElement(tag="interpolate_domain", order="1", renormalize="true", mode="read_or_compute",
                                    write_weight="true"))
    add_value_in_dict_config_variable(variable="domain_defs", key=cfsites_radix, value=domain_xml)
