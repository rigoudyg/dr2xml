#!/usr/bin/python
# -*- coding: utf-8 -*-

from tests.tests_config import path_table, path_homedr

simulation_settings = {'comment': 'Simulation a4SST (after a 10-yr spin up) et test accents en tout genre',# éèêë',
                       'listof_home_vars': '{}/home_data_request_levels.txt '.format(path_homedr),
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
                       'experiment_id': 'a4SST',
                       'physics_index': 1,
                       'branch_year_in_parent': 1960,
                       'branch_year_in_child': 1960,
                       'excluded_vars': [],
                       'configuration': 'AGCM',
                       'excluded_tables': [],
                       'history': 'none',
                       'perso_sdims_description':{
                           'zg50':{
                               'HG50':{
                                   'value':'50',
                                   'axis':"Z",
                                   'positive':'true',
                                   'out_name':'HG50'
                               }
                           }
                       },
                       }
