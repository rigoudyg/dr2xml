#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Home data request tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import os
from collections import defaultdict

from dr2xml.config import get_config_variable, set_config_variable
from utilities.logger import get_logger
from dr2xml.settings_interface import get_settings_values
from dr2xml.utils import VarsError
from .cmor import read_home_var_cmor, check_cmor_variable
from .dev import read_home_var_dev, check_dev_variable
from .extra import read_home_var_extra, check_extra_variable
from .perso import read_home_var_perso, check_perso_variable


def read_home_vars_list(hmv_file, expid, mips, path_extra_tables=None):
    """
    A function to get HOME variables that are not planned in the CMIP6 DataRequest but
    the lab want to outpuut anyway

    Args:
      hmv_file (string) : a text file containing the list of home variables
      expid (string) : if willing to filter on a given experiment
      mips (string)  : if willing to filter on  given mips
      path_extra_tables (string): path where to find extra Tables. Mandatory only if
                                  there is'extra' lines in list of home variables.

    Returns:
      A list of 'simplified CMOR variables'
    """
    logger = get_logger()
    #
    homevars_list = get_config_variable("homevars_list")
    #
    if hmv_file is None:
        return list()
    elif homevars_list is not None:
        return homevars_list
    else:
        data = list()
        file_list = [f for f in hmv_file.split(" ") if len(f) > 0]
        for fil in file_list:
            if not os.path.exists(fil):
                raise VarsError("Abort: file for home variables does not exist: %s" % fil)
            else:
                # Read file
                with open(fil, "r") as fp:
                    data.extend(fp.readlines())
        data = [l.rstrip("\n\t ") for l in data if not l.startswith("#")]
        data = [l for l in data if len(l) > 0]
        # Build list of home variables
        homevars = list()
        extravars = list()
        extra_vars_per_table = defaultdict(list)
        for line in data:
            line_split = line.split(";")
            line_split = [elt.strip(" ").lstrip("\n\t").strip(" ") for elt in line_split]
            line_split = [elt for elt in line_split if len(elt) > 0]
            var_type = line_split[0]
            if var_type in ["cmor", ]:
                home_var = read_home_var_cmor(line_split, mips, expid)
                if home_var is not None:
                    homevars.append(home_var)
            elif var_type in ["perso", ]:
                home_var = read_home_var_perso(line_split, mips, expid)
                if home_var is not None:
                    homevars.append(home_var)
            elif var_type in ["extra", ]:
                home_var = read_home_var_extra(line_split, expid, mips, path_extra_tables=path_extra_tables,
                                               extra_vars_per_table=extra_vars_per_table)
                extravars.extend(home_var)
            elif var_type in ["dev", ]:
                home_var = read_home_var_dev(line_split, mips, expid)
                if home_var is not None:
                    homevars.append(home_var)
            else:
                raise ValueError("Unknown type for var: %s (%s)" % (var_type, line))
        logger.info("Number of 'cmor', 'dev' and 'perso' among home variables: %d" % len(homevars))
        logger.info("Number of 'extra' among home variables: %d" % len(extravars))
        homevars.extend(extravars)
        set_config_variable("homevars_list", homevars)
        return homevars


def process_home_vars(mip_vars_list, mips, expid="False"):
    """
    Deal with home variables
    :param mip_vars_list:
    :param mips:
    :param expid:
    :return:
    """
    logger = get_logger()
    internal_dict = get_settings_values("internal")
    # Read HOME variables
    homevars = internal_dict['listof_home_vars']
    path_extra_tables = internal_dict['path_extra_tables']
    logger.info("homevars file: %s" % homevars)
    home_vars_list = read_home_vars_list(homevars, expid, mips, path_extra_tables)
    logger.info("homevars list: %s" % " ".join([sv.label for sv in home_vars_list]))
    #
    for hv in home_vars_list:
        hv_info = {"varname": hv.label, "realm": hv.modeling_realm, "freq": hv.frequency, "table": hv.mipTable}
        logger.debug(hv_info)
        if hv.type in ["cmor", ]:
            new_hv = check_cmor_variable(hv, mip_vars_list, hv_info)
        elif hv.type in ["perso", ]:
            new_hv = check_perso_variable(hv, hv_info)
        elif hv.type in ["dev", ]:
            new_hv = check_dev_variable(hv, hv_info)
        elif hv.type in ["extra", ]:
            new_hv = check_extra_variable(hv, hv_info)
        else:
            logger.error("%s HOMEVar type %s")
            raise VarsError("Error: %s HOMEVar type %s does not correspond to any known keyword. "
                            "=> Not taken into account." % (hv_info, hv.type))
        if new_hv:
            mip_vars_list.append(new_hv)
    return mip_vars_list
