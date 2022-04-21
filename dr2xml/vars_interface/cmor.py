#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CMOR variables
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.dr_interface import get_list_of_elements_by_id
from logger import get_logger
from dr2xml.settings_interface import get_settings_values
from dr2xml.utils import Dr2xmlError
from .definitions import SimpleCMORVar
from .generic import read_home_var, fill_homevar, check_homevar, get_correspond_cmor_var, \
    complement_svar_using_cmorvar
from .. import get_config_variable

home_attrs = ['type', 'label', 'modeling_realm', 'frequency', 'mipTable', 'temporal_shp', 'spatial_shp',
              'experiment', 'mip']


def read_home_var_cmor(line_split, mips, expid):
    home_var = read_home_var(line_split, home_attrs)
    home_var.set_attributes(label_with_area=home_var.label)
    home_var = fill_homevar(home_var)
    if check_homevar(home_var, mips, expid):
        return home_var
    else:
        return None


def check_cmor_variable(home_var, mip_vars_list, hv_info):
    logger = get_logger()
    updated_homevar = get_correspond_cmor_var(home_var)
    if updated_homevar:
        already_in_dr = any([updated_homevar == cmv for cmv in mip_vars_list])
        if not already_in_dr:
            # Append HOME variable only if not already selected with the DataRequest
            logger.debug("Info: %s HOMEVar is not in DR. => Taken into account." % hv_info)
            return updated_homevar
        else:
            logger.debug("Info: %s HOMEVar is already in DR. => Not taken into account." % hv_info)
            return None
    else:
        logger.warning("Error: %s HOMEVar announced as cmor but no corresponding CMORVar found "
                       "=> Not taken into account." % hv_info)
        return None


def get_cmor_var(label, table):
    """
    Returns CMOR variable for a given label in a given table
    (could be optimized using inverse index)
    """
    cmvar = [cmvar for cmvar in get_list_of_elements_by_id("CMORvar").items
             if cmvar.mipTable == table and cmvar.label == label]
    if len(cmvar) > 0:
        return cmvar[0]
    else:
        return None


def ping_alias(svar, error_on_fail=False):
    """
    Dans le pingfile, grace a la gestion des interpolations
    verticales, on n'attend pas forcement les alias complets des
    variables (CMIP6_<label>), on peut se contenter des alias
    reduits (CMIP6_<lwps>)

    par ailleurs, si on a defini un label non ambigu alors on l'utilise
    comme ping_alias (i.e. le field_ref)
    """
    pingvars = get_config_variable("pingvars")
    pref = get_settings_values("internal", "ping_variables_prefix")
    if svar.label_non_ambiguous:
        # print "+++ non ambiguous", svar.label,svar.label_non_ambiguous
        alias_ping = pref + svar.label_non_ambiguous  # e.g. 'CMIP6_tsn_land' and not 'CMIP6_tsn'
    else:
        # print "+++ ambiguous", svar.label
        # Ping file may provide the variable on the relevant pressure level - e.g. CMIP6_rv850
        alias_ping = pref + svar.ref_var
        if alias_ping not in pingvars:
            # if not, ping_alias is supposed to be without a pressure level suffix
            alias_ping = pref + svar.label_without_psuffix  # e.g. 'CMIP6_hus' and not 'CMIP6_hus7h'
        # print "+++ alias_ping = ", pref, svar.label_without_psuffix, alias_ping
    if alias_ping not in pingvars:
        if error_on_fail:
            raise Dr2xmlError("Cannot find an alias in ping for variable %s" % svar.label)
        else:
            return None
    return alias_ping


def get_simplevar(label, table, freq=None):
    """
    Returns 'simplified variable' for a given CMORvar label and table
    """
    svar = SimpleCMORVar()
    psvar = get_cmor_var(label, table)
    #
    # Try to get a var for 'ps' when table is only in Home DR
    if psvar is None and label in ["ps", ] and freq is not None:
        # print "\tSearching for alternate ps "
        if freq in ["3h", "3hr", "3hrPt"]:
            psvar = get_cmor_var('ps', 'E3hrPt')
        elif freq in ["6h", "6hr"]:
            psvar = get_cmor_var('ps', '6hrLev')
        elif freq in ["day"]:
            psvar = get_cmor_var('ps', 'CFday')
        elif freq in ["mon", "1mo"]:
            psvar = get_cmor_var('ps', 'Emon')
        elif freq in ["subhr"]:
            if table in ["CFsubhr", ]:
                psvar = get_cmor_var('ps', 'CFsubhr')
            else:
                psvar = get_cmor_var('ps', 'Esubhr')
    if psvar:
        complement_svar_using_cmorvar(svar, psvar, None, [], False)
        return svar
