#!/usr/bin/python
# -*- coding: utf-8 -*-


simulation_settings = {
    'comment': '',
    'listof_home_vars': '{path_homedr}/cordex_data_request_atm_CORE.txt '
                        '{path_homedr}/cordex_data_request_aero_CORE.txt '
                        '{path_homedr}/cordex_data_request_atm_Tier1_mon.txt '
                        '{path_homedr}/cordex_data_request_atm_Tier1_day_hr.txt '
                        '{path_homedr}/cordex_data_request_atm_Tier2_mon.txt '
                        '{path_homedr}/cordex_data_request_atm_Tier2_day_hr.txt '
                        '{path_homedr}/cordex_data_request_aero_Tier1_mon.txt '
                        '{path_homedr}/cordex_data_request_aero_Tier1_day_hr.txt '
                        '{path_homedr}/cordex_data_request_aero_Tier2_mon.txt '
                        '{path_homedr}/cordex_data_request_aero_Tier2_day_hr.txt '
                        '{path_homedr}/home_data_request_aladin_cordex_atm.txt '
                        '{path_homedr}/home_data_request_aladin_cordex_aero.txt',
    'sub_experiment': 'none',
    'branch_method': 'standard',
    'excluded_vars': [],
    'child_time_ref_year': 1979,
    'variant_info': '',
    'path_extra_tables': "{path_tables}",
    'realization_index': 1,
    'comments': {},
    'sub_experiment_id': 'none',
    'forcing_index': 2,
    'initialization_index': 1,
    'experiment_id': 'historical',
    'physics_index': 1,
    'branch_year_in_parent': 'N/A',
    'branch_year_in_child': 1979,
    'parent_time_ref_year': 1850,
    'configuration': 'AORCM',
    'history': 'none',
    'bypass_CV_components': True,
    'max_split_freq': '1mo',
    'rcm_version_id': 'v1',
    'excluded_pairs': [('ua', '6hrPlevPt'), ('va', '6hrPlevPt'), ('ta', '6hrPlevPt')],
    'activity_id': 'CORDEX',
    'expid_in_filename': 'historical',
    'driving_model_id': 'CNRM-ESM2-1',
    'driving_experiment': 'CNRM-ESM2-1, historical, r1i1p1f2',
    'driving_model_ensemble_member': 'r1i1p1f2',
    'driving_experiment_name': 'historical',
    'CORDEX_domain': {
        'surfex': 'MED-11',
        'nemo': 'MED-06',
        'trip': 'MED-50'
    },
    'Lambert_conformal_longitude_of_central_meridian': '10.f',
    'Lambert_conformal_standard_parallel': '37.f',
    'Lambert_conformal_latitude_of_projection_origin': '37.f',
}