#!/usr/bin/python
# -*- coding: utf-8 -*-

from tests.tests_config import path_table, path_homedr

simulation_settings ={
	'comment': '',
	'listof_home_vars': '{}/home_data_request_arpege_GCM.txt '
	                    '{}/home_data_request_surfex_GCM.txt '
	                    '{}/home_data_request_trip_GCM.txt '
	                    '{}/home_data_request_arpege_ESM_AddOn.txt '
	                    '{}/home_data_request_surfex_ESM_AddOn.txt '
	                    '{}/home_data_request_trip_ESM_AddOn.txt '
	                    '{}/home_data_request_amip.txt '.format(path_homedr, path_homedr, path_homedr, path_homedr,
	                                                            path_homedr, path_homedr, path_homedr),
	'child_time_ref_year': 1850,
	'variant_info': '',
	'parent_time_ref_year': 1850,
	'physics_index': 1,
	'excluded_vars': [],
	'excluded_tables': ['3hr', '6hrLev', '6hrPlev', '6hrPlevPt', 'AERhr', 'CF3hr', 'CFsubhr', 'E1hr', 'E3hr'],
	'sub_experiment': 'none',
	'path_extra_tables': path_table,
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