# -*- coding: utf-8 -*-

# An example of settings for a CMIP6 experiment/simulation, for use by dr2xml
# It complies with dr2xml v1.00. It complements another settings file, relevant
# for laboratory and model settings
# See refs at bottom

from tests.tests_config import path_homedr, path_table
import os

aladin_path_table = "/".join([path_table, "..", "Tables_RCSM"])

simulation_settings = {
	'listof_home_vars': '{}/home_data_request_aladin_RCM.SP.txt {}/home_data_request_aladin_aerosols_RCM.SP.txt '
	                    '{}/home_data_request_trip_RCM.SP.txt {}/home_data_request_nemomed12.txt'.format(
		path_homedr, path_homedr, path_homedr, path_homedr
	),
	'comment': '',
	'driving_model_id': 'CNRM-ESM2-1',
	'driving_experiment': 'CNRM-ESM2-1, historical, r1i1p1f2',
	'Lambert_conformal_latitude_of_projection_origin': '37.f',
	'rcm_version_id': 'V1',
	'variant_info': '',
	'excluded_pairs': [
		('ua', '6hrPlevPt'),
		('va', '6hrPlevPt'),
		('ta', '6hrPlevPt')
	],
	'driving_experiment_name': 'historical',
	'physics_index': 1,
	'parent_time_ref_year': 1850,
	'excluded_vars': [],
	'sub_experiment': 'none',
	'path_extra_tables': aladin_path_table,
	'Lambert_conformal_standard_parallel': '37.f',
	'child_time_ref_year': 1979,
	'realization_index': 1,
	'comments': {},
	'forcing_index': 2,
	'branch_year_in_child': 1979,
	'driving_model_ensemble_member': 'r1i1p1f2',
	'activity_id': 'CORDEX',
	'expid_in_filename': 'historical',
	'configuration': 'AORCM',
	'sub_experiment_id': 'none',
	'Lambert_conformal_longitude_of_central_meridian': '10.f',
	'branch_method': 'standard',
	'bypass_CV_components': True,
	'CORDEX_domain': {
		'nemo': 'MED-06',
		'surfex': 'MED-11',
		'trip': 'MED-50'
	},
	'initialization_index': 1,
	'experiment_id': 'historical',
	'branch_year_in_parent': 'N/A',
	'history': 'none',
	'max_split_freq': "1m"
}
