#!/usr/bin/python
# -*- coding: utf-8 -*-


simulation_settings ={
	'comment': '',
	'listof_home_vars': '{path_homedr}/home_data_request_arpege_GCM.txt '
	                    '{path_homedr}/home_data_request_surfex_GCM.txt '
	                    '{path_homedr}/home_data_request_trip_GCM.txt '
	                    '{path_homedr}/home_data_request_arpege_ESM_AddOn.txt '
	                    '{path_homedr}/home_data_request_surfex_ESM_AddOn.txt '
	                    '{path_homedr}/home_data_request_trip_ESM_AddOn.txt '
	                    '{path_homedr}/home_data_request_amip.txt ',
	'child_time_ref_year': 1850,
	'variant_info': '',
	'parent_time_ref_year': 1850,
	'physics_index': 1,
	'excluded_vars': [],
	'excluded_tables': ['3hr', '6hrLev', '6hrPlev', '6hrPlevPt', 'AERhr', 'CF3hr', 'CFsubhr', 'E1hr', 'E3hr'],
	'sub_experiment': 'none',
	'path_extra_tables': "{path_tables}",
	'realization_index': 1,
	'comments': {},
	'forcing_index': 3,
	'branch_year_in_child': 1850,
	'expid_in_filename': 'amip',
	'configuration': 'AESM',
	'sub_experiment_id': 'none',
	'branch_method': 'standard',
	'initialization_index': 1,
	'experiment_id': 'amip',
	'branch_year_in_parent': 1850,
	'history': 'none'
}