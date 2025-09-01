#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CMIP6 python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.projects.projects_interface_definitions import ParameterSettings, ValueSettings, FunctionSettings, \
    TagSettings, ConditionSettings

parent_project_settings = "basics"


internal_values = dict(
	configuration=ParameterSettings(
		key="configuration",
		default_values=[None, ]
	),
	source_id=ParameterSettings(
		key="source_id",
		default_values=[None, ]
	),
	experiment_id=ParameterSettings(
		key="experiment_id",
		default_values=[None, ]
	),
	experiment_for_requests=ParameterSettings(
		key="experiment_for_requests",
		default_values=[None, ]
	),
	grid_choice=ParameterSettings(
		key="grid_choice",
		default_values=[[None, ], ]
	),
	grid_policy=ParameterSettings(
		key="grid_policy",
		default_values=[None, ]
	),
	grids=ParameterSettings(
		key="grids",
		default_values=[[None, ], ]
	),
	orphan_variables=ParameterSettings(
		key="orphan_variables",
		default_values=[list(), ]
	),
	sampling_timestep=ParameterSettings(
		key="sampling_timestep",
		default_values=[None, ]
	),
	sizes=ParameterSettings(
		key="sizes",
		default_values=[None, ]
	),
	source_type=ParameterSettings(
		key="source_type",
		default_values=[None, ]
	),
	path_special_defs=ParameterSettings(
		key="path_special_defs",
		default_values=[ValueSettings(key_type="laboratory", keys="path_special_defs")]
	)
)

common_values = dict()

project_settings = dict()