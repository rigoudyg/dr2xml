#!/usr/bin/python
# -*- coding: utf-8 -*-

from tests.tests_config import path_table, path_homedr

simulation_settings = {
    'comment': '',
    'listof_home_vars': #'{}/home_data_request_surfex_LGCM.txt {}/home_data_request_trip_LGCM.txt '
                        '{}/home_data_request_perso.txt '.format(path_homedr),#.format(path_homedr, path_homedr, path_homedr),
    'sub_experiment': 'none',
    'branch_method': 'standard',
    'child_time_ref_year': 1850,
    'variant_info': '',
    'path_extra_tables': path_table,
    'realization_index': 1,
    'comments': {},
    'parent_time_ref_year': 1850,
    'forcing_index': 2,
    'initialization_index': 1,
    'sub_experiment_id': 'none',
    'experiment_id': 'land-hist',
    'physics_index': 1,
    'branch_year_in_parent': 1850,
    'branch_year_in_child': 1850,
    'excluded_vars': ['fco2nat', 'tauu', 'tauv'],
    'configuration': 'LGCM',
    'included_tables': [""],
    'history': 'none',
}
