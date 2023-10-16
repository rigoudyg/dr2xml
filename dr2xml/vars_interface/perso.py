#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perso variables
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.dr_interface import get_data_request
from logger import get_logger
from dr2xml.utils import VarsError
from .generic import read_home_var, fill_homevar, check_homevar, tcmName2tcmValue, get_correspond_cmor_var

home_attrs = ['type', 'label', 'modeling_realm', 'frequency', 'mipTable', 'temporal_shp', 'spatial_shp',
              'experiment', 'mip']


def read_home_var_perso(line_split, mips, expid):
    home_var = read_home_var(line_split, home_attrs)
    home_var.set_attributes(label_with_area=home_var.label, mip_era="PERSO", label_without_psuffix=home_var.label,
                            cell_measures="",
                            cell_methods=tcmName2tcmValue[home_var.temporal_shp])
    home_var = fill_homevar(home_var)
    if check_homevar(home_var, mips, expid):
        return home_var
    else:
        return None


def check_perso_variable(home_var, hv_info):
    logger = get_logger()
    is_cmor = get_correspond_cmor_var(home_var)
    if not is_cmor:
        if home_var.mipVarLabel is None:
            home_var.set_attributes(mipVarLabel=home_var.label)
        data_request = get_data_request()
        if any([cmvar.label == home_var.label for cmvar in data_request.get_list_by_id("CMORvar").items]):
            raise VarsError("Error: %s "
                            "HOMEVar is announced  as perso, is not a CMORVar, but has a cmor name. "
                            "=> Not taken into account." % hv_info)
        else:
            logger.debug("Info: %s HOMEVar is purely personnal. => Taken into account." % hv_info)
            return home_var
    else:
        raise VarsError("Error: %s "
                        "HOMEVar is announced as perso, but in reality is cmor => Not taken into account." %
                        hv_info)
