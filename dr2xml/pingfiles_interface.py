#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ping files variables tools.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict

import os
import sys

# Utilities
from .settings_interface import get_settings_values
from .utils import Dr2xmlError

# Logger
from logger import get_logger

# Global variables and configuration tools
from .config import get_config_variable, add_value_in_dict_config_variable, set_config_variable, \
    add_value_in_list_config_variable

# Interface to Data Request
# Interface to xml tools
from .xml_interface import get_root_of_xml_file, DR2XMLElement

# Variables tools
from .vars_interface.generic_data_request import get_grid_choice


def read_pingfiles_variables(pingfiles, dummies):
    """
    Read variables defined in the ping files.
    """
    logger = get_logger()
    pingvars = list()
    all_ping_refs = OrderedDict()
    if pingfiles is not None:
        all_pingvars = list()
        # print "pingfiles=",pingfiles
        for pingfile in pingfiles.split():
            ping_refs = read_xml_elmt_or_attrib(pingfile, tag='field', attrib='field_ref')
            # ping_refs=read_xml_elmt_or_attrib(pingfile, tag='field')
            if ping_refs is None:
                logger.error("Error: issue accessing pingfile %s" % pingfile)
                return
            all_ping_refs.update(ping_refs)
            if dummies == "include":
                pingvars = list(ping_refs)
            else:
                pingvars = [v for v in ping_refs if 'dummy' not in ping_refs[v]]
                if dummies == "forbid":
                    if len(pingvars) != len(ping_refs):
                        for v in ping_refs:
                            if v not in pingvars:
                                logger.info(v)
                        logger.info("")
                        raise Dr2xmlError("They are still dummies in %s , while option is 'forbid' :" % pingfile)
                    else:
                        pingvars = list(ping_refs)
                elif dummies == "skip":
                    pass
                else:
                    logger.error("Forbidden option for dummies : %s" % dummies)
                    sys.exit(1)
            all_pingvars.extend(pingvars)
        pingvars = all_pingvars
    set_config_variable("pingvars", pingvars)
    set_config_variable("ping_refs", all_ping_refs)


def read_xml_elmt_or_attrib(filename, tag='field', attrib=None):
    """
    Returns a dict of objects tagged TAG in FILENAME, which
    - keys are ids
    - values depend on ATTRIB
          * if ATTRIB is None : object (elt)
          * else : values of attribute ATTRIB  (None if field does not have attribute ATTRIB)
    Returns None if filename does not exist
    """
    #
    logger = get_logger()
    rep = OrderedDict()
    logger.info("processing file %s:" % filename,)
    if os.path.exists(filename):
        logger.info("OK %s" % filename)
        root = get_root_of_xml_file(filename)
        defs = get_xml_childs(root, tag)
        if defs:
            for field in defs:
                logger.debug(".")
                key = field.attrib['id']
                if attrib is None:
                    value = field
                else:
                    value = field.attrib.get(attrib, None)
                rep[key] = value
            logger.debug("")
            return rep
    else:
        logger.info("No file ")
        return None


def get_xml_childs(elt, tag='field', groups=['context', 'field_group',
                                             'field_definition', 'axis_definition', 'axis', 'domain_definition',
                                             'domain', 'grid_definition', 'grid', 'interpolate_axis']):
    """
        Returns a list of elements in tree ELT
        which have tag TAG, by digging in sub-elements
        named as in GROUPS
        """
    rep = list()
    if elt.tag in groups:
        for child in elt:
            rep.extend(get_xml_childs(child, tag))
    elif elt.tag == tag:
        rep.append(elt)
    return rep


def check_for_file_input(sv, hgrid):
    """
    Add an entry in pingvars
    """
    logger = get_logger()
    internal_dict = get_settings_values("internal")
    externs = internal_dict['fx_from_file']
    # print "/// sv.label=%s"%sv.label, sv.label in externs ,"hgrid=",hgrid
    if sv.label in externs and \
            any([d == hgrid for d in externs[sv.label]]):
        pingvar = internal_dict['ping_variables_prefix'] + sv.label
        add_value_in_list_config_variable(variable="pingvars", value=pingvar)
        # Add a grid made of domain hgrid only
        grid_id = "grid_" + hgrid
        grid_def = DR2XMLElement(tag="grid", id=grid_id)
        grid_def.append(DR2XMLElement(tag="domain", domain_ref=hgrid))

        # Add a grid and domain for reading the file (don't use grid above to avoid reampping)
        file_domain_id = "remapped_%s_file_domain" % sv.label
        domain_def = DR2XMLElement(tag="domain", id=file_domain_id, type="rectilinear")
        domain_def.append(DR2XMLElement(tag="generate_rectilinear_domain"))
        add_value_in_dict_config_variable(variable="domain_defs", key=file_domain_id, value=domain_def)
        file_grid_id = "remapped_{}_file_grid".format(sv.label)
        remap_grid_def = DR2XMLElement(tag="grid", id=file_grid_id)
        remap_grid_def.append(DR2XMLElement(tag="domain", domain_ref=file_domain_id))
        add_value_in_dict_config_variable(variable="grid_defs", key=file_grid_id, value=remap_grid_def)
        logger.debug(domain_def)
        logger.debug(remap_grid_def)

        # Create xml for reading the variable
        filename = externs[sv.label][hgrid][get_grid_choice()]
        file_id = "remapped_{}_file".format(sv.label)
        field_in_file_id = "_".join([sv.label, hgrid])
        # field_in_file_id=sv.label
        file_def = DR2XMLElement(tag="file", id=file_id, name=filename, mode="read", output_freq="1ts", enabled="true")
        file_def.append(DR2XMLElement(tag="field", id=field_in_file_id, name=sv.label, operation="instant",
                                      freq_op="1ts", freq_offset="1ts", grid_ref=file_grid_id))
        add_value_in_dict_config_variable(variable="file_defs", key=file_id, value=file_def)
        logger.debug(file_def)
        #
        # field_def='<field id="%s" grid_ref="%s" operation="instant" >%s</field>'%\
        field_def = DR2XMLElement(tag="field", id=pingvar, grid_ref=grid_id, field_ref=field_in_file_id,
                                  operation="instant", freq_op="1ts", freq_offset="0ts")
        add_value_in_dict_config_variable(variable="field_defs", key=field_in_file_id, value=field_def)
        context_index = get_config_variable("context_index", to_change=True)
        context_index[pingvar] = field_def

        logger.debug(field_def)
