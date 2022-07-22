#!/usr/bin/python
# -*- coding: utf-8 -*-

from .config import path_table, path_homedr

simulation_settings = {
	'comment': '',
	'listof_home_vars': '{}/my_home_data_request.txt'.format(path_homedr),
	'activity_id': 'CORDEX',
	'bypass_CV_components': True,
	'expid_in_filename': 'historical',
	'excluded_vars': [],
	'driving_experiment': 'CNRM-ESM2-1, historical, r1i1p1f2',
	'rcm_version_id': 'v1',
	'realization_index': 1,
	'variant_info': '',
	'CORDEX_domain': {'nemo': 'MED-06', 'surfex': 'MED-11', 'trip': 'MED-50'},
	'excluded_pairs': [('ua', '6hrPlevPt'), ('va', '6hrPlevPt'), ('ta', '6hrPlevPt')],
	'driving_experiment_name': 'historical',
	'physics_index': 1,
	'parent_time_ref_year': 1850,
	'configuration': 'AORCM',
	'sub_experiment_id': 'none',
	'Lambert_conformal_longitude_of_central_meridian': '10.f',
	'sub_experiment': 'none',
	'branch_method': 'standard',
	'path_extra_tables': path_table,
	'Lambert_conformal_standard_parallel': '37.f',
	'child_time_ref_year': 1979,
	'Lambert_conformal_latitude_of_projection_origin': '37.f',
	'max_split_freq': '1mo',
	'comments': {},
	'driving_model_ensemble_member': 'r1i1p1f2',
	'forcing_index': 2,
	'initialization_index': 1,
	'experiment_id': 'historical',
	'branch_year_in_parent': 'N/A',
	'branch_year_in_child': 1979,
	'driving_model_id': 'CNRM-ESM2-1',
	'history': 'none'
}