#!/usr/bin/python
# -*- coding: utf-8 -*-


simulation_settings = {
    'comment': '',
    'listof_home_vars': '{path_homedr}/home_data_request_arpege_GCM.txt '
                        '{path_homedr}/home_data_request_surfex_GCM.txt '
                        '{path_homedr}/home_data_request_trip_GCM.txt '
                        '{path_homedr}/home_data_request_nemo_GCM.txt '
                        '{path_homedr}/home_data_request_arpege_ESM_AddOn.txt '
                        '{path_homedr}/home_data_request_surfex_ESM_AddOn.txt '
                        '{path_homedr}/home_data_request_trip_ESM_AddOn.txt '
                        '{path_homedr}/home_data_request_nemo_ESM_AddOn.txt ',
    'sub_experiment': 'none',
    'branch_method': 'standard',
    'excluded_vars': ['rlut4co2', 'rlutcs4co2', 'rsut4co2', 'rsutcs4co2', 'rld4co2', 'rldcs4co2', 'rlu4co2',
                      'rlucs4co2', 'rsd4co2', 'rsdcs4co2', 'rsu4co2', 'rsucs4co2', 'rlutaf', 'rlutcsaf', 'rsutaf',
                      'rsutcsaf', 'rldsaf', 'rldscsaf', 'rlusaf', 'rluscsaf', 'rsdsaf', 'rsdscsaf', 'rsusaf',
                      'rsuscsaf', 'clcalipso', 'albisccp', 'clhcalipso', 'cllcalipso', 'clmcalipso', 'cltcalipso',
                      'cltisccp', 'pctisccp', 'clisccp', 'parasolRefl'],
    'child_time_ref_year': 1850,
    'variant_info': '',
    'path_extra_tables': "{path_tables}",
    'realization_index': 1,
    'comments': {},
    'sub_experiment_id': 'none',
    'forcing_index': 2,
    'initialization_index': 1,
    'experiment_id': 'esm-piControl',
    'physics_index': 1,
    'branch_year_in_parent': 1950,
    'branch_year_in_child': 1850,
    'parent_time_ref_year': 1850,
    'configuration': 'AOESM',
    'excluded_tables': ['E1hr', '3hr', 'CF3hr', 'CFday', '6hrPlevPt', '6hrPlev', 'CFsubhr', '6hrLev'],
    'history': 'none'
}
