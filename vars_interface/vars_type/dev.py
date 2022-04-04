#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dev variables
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr_interface import get_list_of_elements_by_id
from logger import get_logger
from utils import VarsError
from vars_interface.vars_type.generic import read_home_var, fill_homevar, check_homevar, tcmName2tcmValue, \
	get_correspond_cmor_var

home_attrs = ['type', 'label', 'modeling_realm', 'frequency', 'mipTable', 'temporal_shp', 'spatial_shp',
              'experiment', 'mip', 'units', 'long_name', 'stdname', "description"]


def read_home_var_dev(line_split, mips, expid):
	if len(line_split) < len(home_attrs) + 1:
		raise VarsError("Missing geometry description for dev variable {}.".format(line_split[1]))
	else:
		additional_args = line_split[-2:]
		line_split = line_split[:-1]
		line_split[-1] = "|".join(additional_args)
		home_var = read_home_var(line_split, home_attrs)
		if home_var.frequency in ["fx", ]:
			cell_methods = None
		else:
			cell_methods = tcmName2tcmValue[home_var.temporal_shp]
		home_var.set_attributes(label_with_area=home_var.label, mip_era="DEV", mipVarLabel=home_var.label,
		                        cell_methods=cell_methods, label_without_psuffix=home_var.label, cell_measures="")
		home_var = fill_homevar(home_var)
		if check_homevar(home_var, mips, expid):
			return home_var
		else:
			return None


def check_dev_variable(home_var, hv_info):
	logger = get_logger()
	is_cmor = get_correspond_cmor_var(home_var)
	if not is_cmor:
		if home_var.mipVarLabel is None:
			home_var.set_attributes(mipVarLabel=home_var.label)
		if any([cmvar.label == home_var.label for cmvar in get_list_of_elements_by_id("CMORvar").items]):
			raise VarsError("Error: %s "
			                "HOMEVar is announced  as dev, is not a CMORVar, but has a cmor name. "
			                "=> Not taken into account." % hv_info)
		else:
			logger.debug("Info: %s HOMEVar is purely dev. => Taken into account." % hv_info)
			return home_var
	else:
		raise VarsError("Error: %s "
		                "HOMEVar is announced as dev, but in reality is cmor => Not taken into account." %
		                hv_info)
