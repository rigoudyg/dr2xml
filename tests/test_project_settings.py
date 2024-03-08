#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests project settings tools.
"""
from __future__ import division, print_function, unicode_literals, absolute_import

import unittest
from collections import OrderedDict
from copy import copy
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dr2xml.config import initialize_config_variables
from dr2xml.settings_interface import initialize_settings, get_settings_values


class TestProjectSettings(unittest.TestCase):

	def setUp(self):
		initialize_config_variables()
		self.maxDiff = None

	def test_ping_settings(self):
		lset = {
	        'institution_id': "CNRM-CERFACS",
	        'project': "ping",
	        # 'mips' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
	        #                  'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
	        # If you want to get comprehensive ping files; use :
	        'mips': {"CMIP6", "AerChemMIP", "C4MIP", "CFMIP", "DAMIP", "DCPP", "FAFMIP", "GeoMIP", "GMMIP",
	                 "HighResMIP", "ISMIP6", "LS3MIP", "LUMIP", "OMIP", "PDRMIP", "PMIP", "RFMIP", "ScenarioMIP",
	                 "SolarMIP", "VolMIP", "CORDEX", "DynVar", "SIMIP", "VIACSAB", "SPECS", "CCMI", "CMIP5",
	                 "CMIP", "DECK"},
	        'max_priority': 3,
	        'tierMax': 3,
	        # Each XIOS  context does adress a number of realms
	        'realms_per_context': {'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'],
	                               'arpsfx': ['atmos', 'atmos atmosChem', 'aerosol', 'atmos land', 'land',
	                                          'landIce land', 'aerosol land', 'land landIce', 'landIce', ],
	                               },
	        "ping_variables_prefix": "CMIP6_",
	        # We account for a file listing the variables which the lab does not want to produce
	        # Format : MIP varname as first column, comment lines begin with '#'
	        # "excluded_vars_file":"/cnrm/est/USERS/senesi/public/CMIP6/data_request/cnrm/excluded_vars.txt",
	        "excluded_vars_file": [],
	        "excluded_vars": [],
	        # We account for a list of variables which the lab wants to produce in some cases
	        "listof_home_vars": None,
	        # "listof_home_vars": None,
	        "path_extra_tables": None,
	        # mpmoine_correction: Path for special XIOS defs files
	        "path_special_defs": "./input/special_defs"
		}
		sset = dict()
		config = dict(context="arpsfx", dirname=None, prefix="CMIP6_", year=0, root="__init__.py")
		initialize_settings(lset=lset, sset=sset, **config)
		internal = get_settings_values("internal")
		ref_internal = {'CFsubhr_frequency': '1ts',
		                'add_Gibraltar': False,
		                'additional_allowed_model_components': [],
		                'adhoc_policy_do_add_1deg_grid_for_tos': False,
		                'allow_duplicates': True,
		                'allow_duplicates_in_same_table': False,
		                'allow_pseudo_standard_names': False,
		                'allow_tos_3hr_1deg': True,
		                'branching': {},
		                'bypass_CV_components': False,
		                'bytes_per_float': 2,
		                'configuration': None,
		                'context': 'arpsfx',
		                'data_request_path': None,
		                'data_request_used': 'CMIP6',
		                'debug_parsing': False,
		                'dr2xml_manages_enddate': True,
		                'end_year': False,
		                'excluded_pairs_lset': [],
		                'excluded_pairs_sset': [],
		                'excluded_request_links': [],
		                'excluded_spshapes_lset': [],
		                'excluded_tables_lset': [],
		                'excluded_tables_sset': [],
		                'excluded_vars_lset': [],
		                'excluded_vars_per_config': [],
		                'excluded_vars_sset': [],
		                'experiment_for_requests': None,
		                'experiment_id': None,
		                'filter_on_realization': True,
		                'fx_from_file': [],
		                'grid_choice': [None],
		                'grid_policy': None,
		                'grid_prefix': 'CMIP6_',
		                'grids': [None],
		                'grids_dev': {},
		                'grouped_vars_per_file': [],
		                'included_request_links': [],
		                'included_tables': [],
		                'included_tables_lset': [],
		                'included_vars': [],
		                'included_vars_lset': [],
		                'institution_id': 'CNRM-CERFACS',
		                'laboratory_used': None,
		                'listof_home_vars': None,
		                'max_file_size_in_floats': 500000000.0,
		                'max_priority': 3,
		                'max_priority_lset': 3,
		                'max_split_freq': None,
		                'mips': {'AerChemMIP', 'C4MIP', 'CCMI', 'CFMIP', 'CMIP', 'CMIP5', 'CMIP6', 'CORDEX', 'DAMIP',
		                         'DCPP', 'DECK', 'DynVar', 'FAFMIP', 'GMMIP', 'GeoMIP', 'HighResMIP', 'ISMIP6',
		                         'LS3MIP', 'LUMIP', 'OMIP', 'PDRMIP', 'PMIP', 'RFMIP', 'SIMIP', 'SPECS', 'ScenarioMIP',
		                         'SolarMIP', 'VIACSAB', 'VolMIP'},
		                'nemo_sources_management_policy_master_of_the_world': False,
		                'non_standard_attributes': {},
		                'non_standard_axes': {},
		                'orography_field_name': 'orog',
		                'orphan_variables': [],
		                'path_extra_tables': None,
		                'path_to_parse': './',
		                'perso_sdims_description': {},
		                'ping_variables_prefix': 'CMIP6_',
		                'prefixed_orography_field_name': 'CMIP6_orog',
		                'print_stats_per_var_label': False,
		                'print_variables': True,
		                'project': 'ping',
		                'project_settings': 'ping',
		                'realization_index': '1',
		                'realms_per_context': ['atmos', 'atmos atmosChem', 'aerosol', 'atmos land', 'land',
		                                       'landIce land', 'aerosol land', 'land landIce', 'landIce'],
		                'required_model_components': [],
		                'sampling_timestep': None,
		                'save_project_settings': None,
		                'sizes': None,
		                'source_id': None,
		                'source_type': None,
		                'special_timestep_vars': [],
		                'split_frequencies': 'splitfreqs.dat',
		                'tierMax': 3,
		                'tierMax_lset': 3,
		                'too_long_periods': [],
		                'useAtForInstant': False,
		                'use_cmorvar_label_in_filename': False,
		                'use_union_zoom': False,
		                'vertical_interpolation_operation': 'instant',
		                'xios_version': 2,
		                'zg_field_name': 'zg'}
		self.assertDictEqual(internal, ref_internal)
		common = get_settings_values("common")
		ref_common = {'branch_method': 'standard',
		              'branch_month_in_parent': '1',
		              'comment_lab': '',
		              'comment_sim': '',
		              'compression_level': '0',
		              'contact': 'None',
		              'convention_str': 'CF-1.7 CMIP-6.2',
		              'data_specs_version': '01.00.21.post1',
		              'date_range': '%start_date%-%end_date%',
		              'dr2xml_version': '3.1',
		              'expid_in_filename': None,
		              'forcing_index': '1',
		              'history': 'none',
		              'initialization_index': '1',
		              'list_perso_dev_file': 'dr2xml_list_perso_and_dev_file_names',
		              'output_level': '10',
		              'parent_time_ref_year': '1850',
		              'physics_index': '1',
		              'prefix': 'CMIP6_',
		              'sub_experiment': 'none',
		              'sub_experiment_id': 'none',
		              'year': 0}
		self.assertDictEqual(common, ref_common)

