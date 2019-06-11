#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
CFsites-related elements (CFMIP)
A file named cfsites_grid_file_name must be provided at runtime, which
includes a field named cfsites_grid_field_id, defined on an unstructured
grid which is composed of CF sites
"""

from __future__ import print_function, division, absolute_import, unicode_literals


from xml_interface import create_xml_element, create_xml_sub_element


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
    file_dict = dict(id=cfsites_grid_file_id, name=cfsites_grid_file_name, mode="read", output_freq="1y")
    file_xml = create_xml_element(tag="file", attrib=file_dict)
    field_dict = dict(id=cfsites_grid_field_id, operation="instant", grid_ref=cfsites_grid_id)
    create_xml_sub_element(xml_element=file_xml, tag="field", attrib=field_dict)
    return file_xml


def add_cfsites_in_defs(grid_defs, domain_defs):
    """
    Add grid_definition and domain_definition for cfsites in relevant dicts
    """
    grid_xml = create_xml_element(tag="grid", attrib=dict(id=cfsites_grid_id))
    create_xml_sub_element(xml_element=grid_xml, tag="domain", attrib=dict(domain_ref=cfsites_domain_id))
    grid_defs[cfsites_grid_id] = grid_xml

    domain_dict = dict(id=cfsites_domain_id, type="unstructured", prec=8, lat_name="latitude", lon_name="longitude",
                       dim_i_name="site")
    domain_xml = create_xml_element(tag="domain", attrib=domain_dict)
    create_xml_sub_element(xml_element=domain_xml, tag="generate_rectilinear_domain")
    create_xml_sub_element(xml_element=domain_xml, tag="interpolate_domain", attrib=dict(order=1, renormalize="true",
                                                                                         mode="read_or_compute",
                                                                                         write_weight="true"))
    domain_defs[cfsites_radix] = domain_xml
