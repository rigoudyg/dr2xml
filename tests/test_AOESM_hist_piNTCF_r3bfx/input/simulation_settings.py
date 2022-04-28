#!/usr/bin/python
# -*- coding: utf-8 -*-

from tests.tests_config import path_table, path_homedr

simulation_settings = {
    'comment': '',
    'listof_home_vars': '{}/home_data_request_arpege_GCM.txt '
                        '{}/home_data_request_surfex_GCM.txt '
                        '{}/home_data_request_trip_GCM.txt '
                        '{}/home_data_request_nemo_GCM.txt '
                        '{}/home_data_request_arpege_ESM_AddOn.txt '
                        '{}/home_data_request_surfex_ESM_AddOn.txt '
                        '{}/home_data_request_trip_ESM_AddOn.txt '
                        '{}/home_data_request_nemo_ESM_AddOn.txt '.format(path_homedr, path_homedr, path_homedr,
                                                                          path_homedr, path_homedr, path_homedr,
                                                                          path_homedr, path_homedr),
    'sub_experiment': 'none',
    'branch_method': 'standard',
    'excluded_vars': [],
    'child_time_ref_year': 1850,
    'variant_info': '',
    'path_extra_tables': path_table,
    'realization_index': 3,
    'comments': {},
    'sub_experiment_id': 'none',
    'forcing_index': 2,
    'initialization_index': 1,
    'experiment_id': 'hist-piNTCF',
    'physics_index': 1,
    'branch_year_in_parent': 1941,
    'branch_year_in_child': 1850,
    'parent_time_ref_year': 1850,
    'configuration': 'AOESM',
    'excluded_tables': [],
    'history': 'none'
}
