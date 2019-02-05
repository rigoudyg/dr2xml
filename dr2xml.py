#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
In the context of Climate Model Intercomparison Projects (CMIP) :

A few functions for processing
  - a CMIP Data request and
  - a set of settings related to a laboratory, and a model
  - a set of settings related to an experiment (i.e. a set of numerical
      simulations),
to generate a set of xml-syntax files used by XIOS (see
https://forge.ipsl.jussieu.fr/ioserver/) for outputing geophysical
variable fields

First version (0.8) : S.Senesi (CNRM) - sept 2016

Changes :
  oct 2016 - Marie-Pierre Moine (CERFACS) - handle 'home' Data Request
                               in addition
  dec 2016 - S.Senesi (CNRM) - improve robustness
  jan 2017 - S.Senesi (CNRM) - handle split_freq; go single-var files;
                               adapt to new DRS ...
  feb 2017 - S.Senesi (CNRM) - handle grids and remapping;
                               put some func in separate module
  april-may 2017 - M-P Moine (CERFACS) : handle pressure axes ..
  june 2017 - S.Senesi (CNRM)  introduce horizontal remapping
  july 2017 - S.Senesi -CNRM)  improve efficieny in remapping; allow for
                 sampling before vert. interpolation, for filters on table, reqLink..
                 Adapt filenames to CMIP6 conventions (including date offset).
                 Handle remapping for CFsites
  Rather look at git log for identifying further changes and contriubutors....

"""
####################################
# Pre-requisites
####################################

# 1- CMIP6 Data Request package retrieved using
#    svn co http://proj.badc.rl.ac.uk/svn/exarch/CMIP6dreq/tags/01.00.21
#    (and must include 01.00.21/dreqPy in PYTHONPATH)

# 2- CMIP6 Controled Vocabulary (available from
# https://github.com/WCRP-CMIP/CMIP6_CVs). You will provide its path
# as argument to functions defined here

# 3- XIOS release must be 1442 or above (to be fed with the outputs)
#  see https://forge.ipsl.jussieu.fr/ioserver/wiki

####################################
# End of pre-requisites
####################################
import json
import datetime
import re
import collections
import sys
import os
import glob
import xml.etree.ElementTree as ET

# Utilities
from utils import dr2xml_error

# Settings and config
from config import get_config_variable, set_config_variable
from analyzer import freq2datefmt, analyze_cell_time_method, Cmip6Freq2XiosFreq, longest_possible_period, \
    initialize_cell_method_warnings, get_cell_method_warnings, DRgrid2gridatts

# Data request interface
from dr_interface import get_DR_version, initialize_sc, get_collection, get_uid, get_request_by_id_by_sect, \
    get_experiment_label, print_DR_errors

# Simulations and laboratory settings dictionnaries interface
from settings_interface import initialize_dict, get_variable_from_lset_with_default, \
    is_key_in_sset, get_variable_from_sset_without_default, is_sset_not_None, get_source_id_and_type, \
    get_variable_from_sset_and_lset_without_default, get_variable_from_sset_with_default_in_sset, \
    get_variable_from_sset_with_default, is_key_in_lset, get_variable_from_sset_else_lset_with_default, \
    get_lset_iteritems, get_sset_iteritems, get_variable_from_lset_without_default

# XIOS linked modules
from Xparse import init_context, id2grid, id2gridid, idHasExprWithAt
from Xwrite import wr, write_xios_file_def

# Grids modules
from grids import get_grid_def, guess_simple_domain_grid_def, create_grid_def, create_axis_def, change_domain_in_grid, \
    get_grid_def_with_lset, change_axes_in_grid, isVertDim, scalar_vertical_dimension
from grids_selection import decide_for_grids

# Variables modules
from vars_home import process_homeVars, complement_svar_using_cmorvar, \
    multi_plev_suffixes, single_plev_suffixes, get_simplevar
from vars_cmor import simple_CMORvar, simple_Dim
from vars_selection import endyear_for_CMORvar, RequestItem_applies_for_exp_and_year, select_CMORvars_for_lab, \
    gather_AllSimpleVars, get_sc, initialize_sn_issues, get_grid_choice

# Split frequencies module
from file_splitting import split_frequency_for_variable, timesteps_per_freq_and_duration

# Statistics module
from infos import print_SomeStats

# CFsites handling has its own module
from cfsites import cfsites_domain_id, cfsites_grid_id, cfsites_input_filedef, add_cfsites_in_defs

# Post-processing modules
from postprocessing import process_vertical_interpolation, process_zonal_mean, process_diurnal_cycle

print "\n", 50 * "*", "\n*"
print "* %29s" % "dr2xml version: ", get_config_variable("version")

# The current code should comply with this version of spec doc at
# https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit
CMIP6_conventions_version = "v6.2.4"
print "* %29s" % "CMIP6 conventions version: ", CMIP6_conventions_version

# mpmoine_merge_dev2_v0.12: posixpath.dirname ne marche pas chez moi
# TBS# from os import path as os_path
# TBS# prog_path=os_path.abspath(os_path.split(__file__)[0])

print "* %29s" % "CMIP6 Data Request version: ", get_DR_version()
print "\n*\n", 50 * "*"

""" An example/template  of settings for a lab and a model"""
example_lab_and_model_settings = {

    'institution_id': "CNRM-CERFACS",  # institution should be read in CMIP6_CV, if up-to-date

    # We describe the "CMIP6 source type" (i.e. components assembly) which is the default
    # for each model. This value can be changed on a per experiment basis, in experiment_settings file
    # However, using a 'configuration' is finer (see below)
    # CMIP6 component conventions are described at
    #          https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_source_type.json
    'source_types': {"CNRM-CM6-1": "AOGCM AER", "CNRM-CM6-1-HR": "AOGCM AER",
                     "CNRM-ESM2-1": "AOGCM BGC AER CHEM", "CNRM-ESM2-1-HR": "AOGCM BGC AER"},

    # Optional : 'configurations' are shortcuts for a triplet (model, source_type, unused_contexts)
    'configurations': {
        "AGCM": ("CNRM-CM6-1", "AGCM", ['nemo']),
        "AESM": ("CNRM-ESM2-1", "AGCM BGC AER CHEM", ['nemo']),
        "AOGCM": ("CNRM-CM6-1", "AOGCM", []),
        "AOESM": ("CNRM-ESM2-1", "AOGCM BGC AER CHEM", []),
        "AGCMHR": ("CNRM-CM6-1-HR", "AGCM", ['nemo']),
        "AESMHR": ("CNRM-ESM2-1", "AGCM BGC AER", []),
        "AOGCMHR": ("CNRM-CM6-1-HR", "AOGCM", []),
        "AOESMHR": ("CNRM-ESM2-1", "AOGCM BGC AER", []),
        "LGCM": ("CNRM-CM6-1", "LAND", ['nemo']),
        "LESM": ("CNRM-ESM2-1", "LAND BGC", ['nemo']),
        "OGCM": ("CNRM-CM6-1", "OGCM", ['surfex', 'trip']),
        "OESM": ("CNRM-ESM2-1", "OGCM BGC", ['surfex', 'trip'])},

    # 'source'         : "CNRM-CM6-1", # Useful only if CMIP6_CV is not up to date
    'references': "A character string containing a list of published or web-based " + \
                  "references that describe the data or the methods used to produce it." + \
                  "Typically, the user should provide references describing the model" + \
                  "formulation here",
    'info_url': "http://www.umr-cnrm.fr/cmip6/",
    'contact': 'contact.cmip@meteo.fr',

    # We account for the list of MIPS in which the lab takes part.
    # Note : a MIPs set limited to {'C4MIP'} leads to a number of tables and
    # variables which is manageable for eye inspection
    'mips_for_test': {'C4MIP', 'SIMIP', 'OMIP', 'CFMIP', 'RFMIP'},
    'mips': {
        "LR": {'AerChemMIP', 'C4MIP', 'CFMIP', 'DAMIP', 'FAFMIP', 'GeoMIP', 'GMMIP', 'ISMIP6',
               'LS3MIP', 'LUMIP', 'OMIP', 'PMIP', 'RFMIP', 'ScenarioMIP', 'CORDEX', 'SIMIP', 'CMIP6', 'CMIP'},
        "HR": {'OMIP', 'ScenarioMIP', 'CORDEX', 'CMIP6', 'CMIP'},
    },

    # A character string containing additional information about the models. Will be complemented
    # with the experiment's specific comment string
    "comment": "",

    # Max variable priority level to be output (you may set 3 when creating ping_files while
    # being more restrictive at run time); values in simulation_settings may override the one below
    'max_priority': 1,
    'tierMax': 1,

    # The ping file defines variable names, which are constructed using CMIP6 "MIPvarnames"
    # and a prefix which must be set here, and can be the empty string :
    "ping_variables_prefix": "CMIP6_",

    # We account for a list of variables which the lab does not want to produce ,
    # Names must match DR MIPvarnames (and **NOT** CMOR standard_names)
    # excluded_vars_file="../../cnrm/non_published_variables"
    "excluded_vars": ['pfull', 'phalf', "zfull"],  # because we have a pressure based hydrid coordinate,
    # and no fixed height levels

    # Vars computed with a period which is not the basic timestep must be declared explictly,
    # with that period, in order that 'instant' sampling works correctly
    # (the units for period should be different from the units of any instant ouput frequency
    # for those variables - 'mi' loooks fine, 'ts' may work)
    "special_timestep_vars": {
        "60mi": ['parasolRefl', 'clhcalipso', 'cltcalipso', 'cllcalipso', 'clmcalipso', 'cfadLidarsr532', 'clcalipso',
                 'clcalipso2', 'cfadDbze94', 'jpdftaureliqmodis', 'clisccp', 'jpdftaureicemodis', 'clmisr'],
    },

    # You can specifically exclude some pairs (vars,tables), here in lab_settings
    # and also (in addition) in experiment_settings
    "excluded_pairs": [('fbddtalk', 'Omon')],

    # For debugging purpose, if next list has members, this has precedence over
    # 'excluded_vars' and over 'excluded_vars_per_config'
    # "included_vars" : [ 'ccb' ],

    # When atmospheric vertical coordinate implies putting psol in model-level output files, we
    # must avoid creating such file_def entries if the model does not actually send the 3D fields
    # (because this leads to files full of undefined values)
    # We choose to describe such fields as a list of vars dependant on the model configuration
    # because the DR is not in a good enough shape about realms for this purpose
    "excluded_vars_per_config": {
        "AGCM": ["ch4", "co2", "co", "concdust", "ec550aer", "h2o", "hcho", "hcl", "hno3", "mmrbc", "mmrdust", "mmroa",
                 "mmrso4", "mmrss", "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", "so2"],
        "AOGCM": ["ch4", "co2", "co", "concdust", "ec550aer", "h2o", "hcho", "hcl", "hno3", "mmrbc", "mmrdust", "mmroa",
                  "mmrso4", "mmrss", "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", "so2"],
    },
    #
    "excluded_spshapes": ["XYA-na", "XYG-na",  # GreenLand and Antarctic grids we do not want to produce
                          "na-A",  # RFMIP.OfflineRad : rld, rlu, rsd, rsu in table Efx ?????
                          "Y-P19", "Y-P39", "Y-A", "Y-na"  # Not yet handled by dr2xml
                          ],

    "excluded_tables": ["Oclim", "E1hrClimMon", "ImonAnt", "ImonGre"],  # Clims are not handled by Xios yet

    # For debugging purpose : if next list has members, only those tables will be processed
    # "included_tables"  : ["AMon" ] , # If not empty, has priority over excluded_tables

    "excluded_request_links": [
        "RFMIP-AeroIrf"  # 4 scattered days of historical, heavy output -> please rerun model for one day
        # for each day of this request_link
    ],
    # For debugging purpose : if next list has members, only those requestLinks will be processed
    "included_request_links": [],

    # We account for a default list of variables which the lab wants to produce in most cases
    # This can be changed at the experiment_settings level
    # "listof_home_vars":"../../cnrm/listof_home_vars.txt",

    # If we use extra tables, we can set it here (and supersed it in experiment settings)
    # 'path_extra_tables'=

    # Each XIOS  context does adress a number of realms
    'realms_per_context': {
        'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'],
        'arpsfx': ['atmos', 'atmos atmosChem', 'atmosChem', 'aerosol', 'atmos land', 'land',
                   'landIce land', 'aerosol', 'land landIce', 'landIce', ],
        'trip': [],
    },
    # Some variables, while belonging to a realm, may fall in another XIOS context than the
    # context which hanldes that realm
    'orphan_variables': {
        'trip': ['dgw', 'drivw', 'fCLandToOcean', 'qgwr', 'rivi', 'rivo', 'waterDpth', 'wtd'],
    },
    # A per-variable dict of comments valid for all simulations
    'comments': {
        'rld': 'nothing special about this variable'
    },
    #
    'grid_choice': {"CNRM-CM6-1": "LR", "CNRM-CM6-1-HR": "HR",
                    "CNRM-ESM2-1": "LR", "CNRM-ESM2-1-HR": "HR"},
    # If you want to produce the same variables set for all members, set next parameter to False
    # You can anyway override this parameter in dict simulation_settings
    "filter_on_realization": True,
    # Sizes for atm and oce grids (cf DR doc); Used for computing file split frequency
    "sizes": {"LR": [292 * 362, 75, 128 * 256, 91, 30, 14, 128],
              "HR": [1442 * 1021, 75, 720 * 360, 91, 30, 14, 128]},

    # What is the maximum duration of data period in a single file (integer, in years)
    "max_split_freq": None,

    # What is the maximum size of generated files, in number of float values
    "max_file_size_in_floats": 2000. * 1.e+6,  # 2 Giga octets
    # Required NetCDF compression level
    "compression_level": 0,
    # Estimate of number of bytes per floating value, given the chosen compresssion level
    "bytes_per_float": 2.0,

    # grid_policy among None, DR, native, native+DR, adhoc- see docin grids.py
    "grid_policy": "adhoc",

    # Grids : per model resolution and per context :
    #              - CMIP6 qualifier (i.e. 'gn' or 'gr') for the main grid chosen (because you
    #                 may choose has main production grid a regular one, when the native grid is e.g. unstructured)
    #              - Xios id for the production grid (if it is not the native grid),
    #              - Xios id for the latitude axis used for zonal means (mist match latitudes for grid above)
    #              - resolution of the production grid (using CMIP6 conventions),
    #              - grid description
    "grids": {

        "LR": {
            "surfex": ["gr", "complete", "glat", "250 km",
                       "data regridded to a T127 gaussian grid (128x256 latlon)"
                       "from a native atmosphere T127l reduced gaussian grid"],
            "trip": ["gn", "", "", "50 km", "regular 1/2 deg lat-lon grid"],
            "nemo": ["gn", "", "", "100 km", "native ocean tri-polar grid with 105 k ocean cells"], },

        "HR": {
            "surfex": ["gr", "complete", "glat", "50 km",
                       "data regridded to a 359 gaussian grid (180x360 latlon)"
                       "from a native atmosphere T359l reduced gaussian grid"],
            "trip": ["gn", "", "", "50 km", "regular 1/2 deg lat-lon grid"],
            "nemo": ["gn", "", "", "25 km", "native ocean tri-polar grid with 1.47 M ocean cells"], },
    },
    # "nb_longitudes_in_model": { "surfex" :"ndlon", "nemo": "" },
    #
    # Basic sampling timestep set in your field definition (used to feed metadata 'interval_operation')
    "sampling_timestep": {
        "LR": {"surfex": 900., "nemo": 1800.},
        "HR": {"surfex": 900., "nemo": 1800.},
    },

    # CFMIP has an elaborated requirement for defining subhr frequency; by default, dr2xml uses 1 time step
    "CFsubhr_frequency": "1ts",

    # We create sampled time-variables for controlling the frequency of vertical interpolations
    "vertical_interpolation_sample_freq": "3h",
    "vertical_interpolation_operation": "instant",  # LMD prefers 'average'

    # --- Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR
    "use_union_zoom": False,

    # The CMIP6 frequencies that are unreachable for a single model run. Datafiles will
    # be labelled with dates consistent with content (but not with CMIP6 requirements).
    # Allowed values are only 'dec' and 'yr'
    "too_long_periods": ["dec", "yr"],

    # Describe the branching scheme for experiments involved in some 'branchedYears type' tslice
    # (for details, see: http://clipc-services.ceda.ac.uk/dreq/index/Slice.html )
    # Just put the as key the common start year in child and as value the list of start years in parent for all members
    "branching": {
        "CNRM-CM6-1": {"historical": (1850, [1850, 1883, 1941, 1960, 1990, 2045, 2079, 2108, 2214, 2269])},
        "CNRM-ESM2-1": {"historical": (1850, [1850, 1883, 1941])},
    },

    # We can control the max output level set for all output files,
    "output_level": 10,

    # For debug purpose, you may slim down xml files by setting next entry to False
    "print_variables": True,

    # Set that to True if you use a context named 'nemo' and the
    # corresponding model unduly sets a general freq_op AT THE
    # FIELD_DEFINITION GROUP LEVEL. Due to Xios rules for inheritance,
    # that behavior prevents inheriting specific freq_ops by reference
    # from dr2xml generated field_definitions
    "nemo_sources_management_policy_master_of_the_world": False,

    # You may add a series of NetCDF attributes in all files for this simulation
    "non_standard_attributes": {"model_minor_version": "6.1.0"},

    # If some grid is not defined in xml but by API, and is referenced by a
    # field which is considered by the DR as having a singleton dimension, then :
    #  1) it must be a grid which has only a domain
    #  2) the domain name must be extractable from the grid_id using a regexp
    #     and a group number
    # Example : using a pattern that returns full id except for a '_grid' suffix
    # "simple_domain_grid_regexp" : ("(.*)_grid$",1),

    # If your model has some axis which does not have all its attributes
    # as in DR, and you want dr2xml to fix that it, give here
    # the correspondence from model axis id to DR dim/grid id.
    # For label dimensions you should provide the list of labels, ordered
    # as in your model, as second element of a pair
    # Label-type axes will be processed even if not quoted
    # Scalar dimensions are not concerned by this feature
    'non_standard_axes': {
        # Space dimensions - Arpege :
        'klev': 'alevel', 'klev_half': 'alevel',

        # COSP
        'effectRadIc': 'effectRadIc', 'effectRadL': 'effectRadL',
        'sza5': 'sza5',
        'dbze': 'dbze',

        # Land dimensions
        'soilpools': ('soilpools', 'fast medium slow'),
        # 'landUse'      :'landUse' ,
        'vegtype': ('vegtype',
                    'Bare_soil Rock Permanent_snow Temperate_broad-leaved_decidus Boreal_needleaf_evergreen'
                    'Tropical_broad-leaved_evergreen C3_crop C4_crop Irrigated_crop C3_grass C4_grass Wetland'
                    'Tropical_broad-leaved_decidus Temperate_broad-leaved_evergreen Temperate_needleaf_evergreen'
                    'Boreal_broad-leaved_decidus Boreal_needleaf_decidus Tundra_grass Shrub'),

        # Space dimensions - Nemo
        'depthw': 'olevel', 'deptht': 'olevel', 'depthu': 'olevel', 'depthv': 'olevel',
        'j-mean': 'latitude',

        # Ocean transects and basins
        # 'oline'        :'oline' ,
        # 'siline'       :'siline',
        'basin ': ('basin', 'global_ocean atlantic_arctic_ocean indian_pacific_ocean dummy dummy'),

        # toy_cnrmcm, for oce (Note : for atm, there is adhoc code)
        'axis_oce': 'olevel', 'lat_oce': 'latitude', 'transect_axis': 'oline',
        'basin_oce_3': ('basin', 'global_ocean atlantic_arctic_ocean indian_pacific_ocean dummy dummy'),
    },

    # A smart workflow will allow you to extend a simulation during it
    # course and to complement the output files accordingly, by
    # managing the 'end date' part in filenames. You can then set next
    # setting to False (default is True)
    'dr2xml_manages_enddate': True,

    # You may provide some variables already horizontally remapped
    # to some grid (i.e. Xios domain) in external files. The varname in file
    # must match the referenced id in pingfile. Tested only for fixed fields
    'fx_from_file': {
        "areacella": {"complete":
                          {"LR": "areacella_LR",
                           "HR": "areacella_HR", }
                      }

    },

    # The path of the directory which, at run time, contains the root XML file (iodef.xml)
    'path_to_parse': "./",

    # Should we allow for duplicate vars : two vars with same
    # frequency, shape and realm , which differ only by the table.
    # In DR01.00.21, this actually applies to very few fields (ps-Aermon,
    # tas-ImonAnt, areacellg-IfxAnt). Defaults to True
    'allow_duplicates': True,

    # Should we allow for another type of duplicate vars : two vars
    # with same name in same table (usually with different
    # shapes). This applies to e.g. CMOR vars 'ua' and 'ua7h' in
    # 6hPlevPt. Default to False, because CMIP6 rules does not allow
    # to name output files differently in that case. If set to True,
    # you should also set 'use_cmorvar_label_in_filename' to True to
    # overcome the said rule
    'allow_duplicates_in_same_table': False,

    # CMIP6 rule is that filenames includes the variable label, and
    # that this variable label is not the CMORvar label, but 'MIPvar'
    # label. This may lead to conflicts, e.g. for 'ua' and 'ua7h' in
    # table 6hPlevPt; next setting allows to avoid that, if set to True
    'use_cmorvar_label_in_filename': False,

    # DR01.00.21 does not include Gibraltar strait, which is requested by OMIP
    # Can include it, if model provides it as last value of array. Defaults to false
    'add_Gribraltar': False,

    # In order to identify which xml files generates a problem, you can use this flag
    'debug_parsing': False,

    # DR has sn attributes for MIP variables. They can be real,CF-compliant, standard_names or
    # pseudo_standard_names, i.e. not yet approved labels. Default is to use only CF ones
    'allow_pseudo_standard_names': False,

    # For an extended printout of selected CMOR variables, grouped by variable label
    'print_stats_per_var_label': False,

    # When using select='no', Xios may enter an endless loop, which is solved if next setting is False
    'allow_tos_3hr_1deg': True,

    # Some scenario experiment in DR 01.00.21 do not request tos on 1 degree grid, while other do.
    # If you use grid_policy=adhoc and had not changed the mapping of function
    # grids.lab_adhoc_grid_policy to grids.CNRM_grid_policy, next setting can force any tos request
    # to also produce tos on a 1 degree grid
    "adhoc_policy_do_add_1deg_grid_for_tos": False,
}

""" An example/template of settings for a simulation """

example_simulation_settings = {
    # Dictionnary describing the necessary attributes for a given simulation

    # Warning : some lines are commented out in this example but should be
    # un-commented in some cases. See comments

    # DR experiment name to process. See http://clipc-services.ceda.ac.uk/dreq/index/experiment.html
    "experiment_id": "historical",
    # Experiment label to use in file names and attribute, (default is experiment_id)
    # "expid_in_filename"   : "myexpe",
    # Experiment id to use for driving the use of the Data Request (default is experiment_id)
    # 'experiment_for_requests' : "piControl",

    # If there is no configuration in lab_settings which matches you case, please rather
    # use next or next two entries : source_id and, if needed, source_type
    'configuration': 'AOGCM',

    # For some experiments (e.g. concentration-driven historical in AESM config), the only way to
    # avoid producing useless fields is to explictly exclude variables (in addition to those in lab_settings)
    'excluded_vars': [],

    # It can be handy to exclude some Tables at the experiment level. They are added to the lab-level set
    # "excluded_tables"  : [ ] ,

    # 'source_id'      : "CNRM-CM6-1",
    # 'source_type'    : "OGCM" ,# If the default source-type value for your source (from lab settings)
    # does not fit, you may change it here.
    # "This should describe the model most directly responsible for the
    # output.  Sometimes it is appropriate to list two (or more) model types here, among
    # AER, AGCM, AOGCM, BGC, CHEM, ISM, LAND, OGCM, RAD, SLAB "
    # e.g. amip , run with CNRM-CM6-1, should quote "AGCM AER"
    # Also see note 14 of https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit

    # "contact"        : "", set it only if it is specific to the simualtion
    # "project"        : "CMIP6",  #CMIP6 is the default

    # 'max_priority' : 1,  # a simulation may be run with a max_priority which overrides the one in lab_settings
    # 'tierMax'      : 1,  # a simulation may be run with a Tiermax overrides the one in lab_settings

    # It is recommended that some description be included to help
    # identify major differences among variants, but care should be
    # taken to record correct information.  dr2xml will add in all cases:
    #  'Information provided by this attribute may in some cases be
    #  flawed. Users can find more comprehensive and up-to-date
    #  documentation via the further_info_url global attribute.'
    "variant_info": "Start date after 300 years of control run",
    #
    "realization_index": 1,  # Value may be omitted if = 1
    "initialization_index": 1,  # Value may be omitted if = 1
    "physics_index": 1,  # Value may be omitted if = 1
    "forcing_index": 3,  # Value may be omitted if = 1
    #
    # If you want to produce the same variables set for all members, set next parameter to False
    # This value does override the value for same parameter in lab_settings
    # "filter_on_realization" : True,
    #
    # All about the branching scheme from parent
    "branch_method": "standard",  # default value='standard' meaning ~ "select a start date"
    # (this is not necessarily the parent start date)
    'parent_time_ref_year': 1850,  # MUST BE CONSISTENT WITH THE TIME UNITS OF YOUR MODEL(S) !!!
    "branch_year_in_parent": 2150,  # if your calendar is Gregorian, you can specify the branch year in parent directly
    # This is an alternative to using "branch_time_in_parent".
    # "branch_month_in_parent": 1,        # You can then also set the month. Default to 1
    # "branch_time_in_parent": "365.0D0", # a double precision value, in days, used if branch_year_in_parent
    #                                     # is not applicable
    # This is an alternative to using "branch_year_in_parent"
    # 'parent_time_units'    : "" #in case it is not the same as child time units

    # In some instances, the experiment start year is not explicit or is doubtful in DR. See
    # file doc/some_experiments_starty_in_DR01.00.21. You should then specifiy it, using next setting
    # in order that requestItems analysis work in all cases

    # In some other cases, DR requestItems which apply to the experiment form its start does not
    # cover its whole duration and have a wrong duration (computed based on a wrong start year);
    # They necessitate to fix the start year
    # 'branch_year_in_child' : 1950,

    # If you want to carry on the experiment beyond the duration set in DR, and that all
    # requestItems that apply to DR end year also apply later on, set 'end_year'
    # You can also set it if you don't know if DR has a wrong value
    # 'end_year' : 2014,

    'child_time_ref_year': 1850,  # MUST BE CONSISTENT WITH THE TIME UNITS OF YOUR MODEL(S) !!!
    # (this is not necessarily the parent start date)
    # the ref_year for a scenario must be the same as for the historical
    # "branch_time_in_child" : "0.0D0",   # a double precision value in child time units (days),
    # This is an alternative to using "branch_year_in_child"

    # 'parent_variant_label' :""  #Default to 'same variant as child'. Other cases should be exceptional
    # "parent_mip_era"       : 'CMIP5'   # only in special cases (as e.g. PMIP warm
    # start from CMIP5/PMIP3 experiment)
    # 'parent_source_id'     : 'CNRM-CM5.1' # only in special cases, where parent model
    # is not the same model
    #
    "sub_experiment_id": "None",  # Optional, default is 'none'; example : s1960.
    "sub_experiment": "None",  # Optional, default in 'none'
    "history": "None",  # Used when a simulation is re-run, an output file is modified ...

    # A character string containing additional information about this simulation
    "comment": "",

    # You can specifically exclude some pairs (vars,tables), here in experiment settings
    # They wil be added to the lab-settings list of excluded pairs
    # "excluded_pairs" : [ ('fbddtalk','Omon') ]

    # A per-variable dict of comments which are specific to this simulation. It will replace
    # the all-simulation comment
    'comments': {
        'tas': 'this is a dummy comment, placeholder for describing a special, '
               'simulation dependent, scheme for a given variable',
    },
    # We can supersede the default list of variables of lab_settings, which tells
    # which additionnal variables/frequecny are to produce
    # "listof_home_vars":"../../cnrm/home_vars_historical.txt",

    # If we use extra tables, we can here supersede the value set it in lab settings
    # 'path_extra_tables'=

    # If the CMIP6 Controlled Vocabulary doesn't allow all the components you activate, you can set
    # next toggle to True
    'bypass_CV_components': False,

    # What is the maximum duration of data period in a single file, for this experiment (integer, in years)
    "max_split_freq": None,

    'unused_contexts': []  # If you havn't set a 'configuration', you may fine tune here
}


def generate_file_defs(lset, sset, year, enddate, context, cvs_path, pingfiles=None,
                       dummies='include', printout=False, dirname="./", prefix="", attributes=[],
                       select="on_expt_and_year"):
    # A wrapper for profiling top-level function : generate_file_defs_inner
    import cProfile
    import pstats
    import StringIO
    pr = cProfile.Profile()
    pr.enable()
    # Initialize lset and sset variables for all functions
    initialize_dict(lset, sset)
    generate_file_defs_inner(lset, sset, year, enddate, context, cvs_path, pingfiles=pingfiles,
                             dummies=dummies, printout=printout, dirname=dirname,
                             prefix=prefix, attributes=attributes, select=select)
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    # Just un-comment next line to get the profile on stdout
    # print s.getvalue()


def generate_file_defs_inner(lset, sset, year, enddate, context, cvs_path, pingfiles=None,
                             dummies='include', printout=False, dirname="./", prefix="",
                             attributes=[], select="on_expt_and_year"):
    """
    Using the DR module, a dict of lab settings LSET, and a dict
    of simulation settings SSET, generate an XIOS file_defs 'file' for a
    given XIOS 'context', which content matches
    the DR for the experiment quoted in simu setting dict and a YEAR.
    Makes use of CMIP6 controlled vocabulary files found in CVS_PATH
    Reads files matching PINGFILE for analyzing dummy field_refs,
    DUMMIES='include' : include dummy refs in file_def (useful
                              demonstration run)
    DUMMIES='skip'  : don't write field with a ref to a dummy
                          (useful until ping_file is fully completed)
    DUMMIES='forbid': stop if any dummy (useful for production run)
    Output file is named <DIRNAME>filedefs_<CONTEXT>.xml
    Filedefs have a CMIP6 compliant name, with prepended PREFIX

    Structure of the two dicts is documented elsewhere. It includes the
    correspondance between a context and a few realms

    ATTRIBUTES is a list of (name,value) pairs which are to be inserted as
    additional file-level attributes. They are complemented with entry
    "non_standard__attributes" of dict sset

    """
    #
    debug = False
    cmvk = "CMIP6_CV_version"
    if cmvk in attributes:
        print "* %s: %s" % (cmvk, attributes[cmvk])
    # --------------------------------------------------------------------
    # Parse XIOS settings file for the context
    # --------------------------------------------------------------------
    print "\n", 50 * "*", "\n"
    print "Processing context ", context
    print "\n", 50 * "*", "\n"
    set_config_variable("context_index",
                        init_context(context, get_variable_from_lset_with_default("path_to_parse", "./"),
                                     printout=get_variable_from_lset_with_default("debug_parsing", False)))
    if get_config_variable("context_index") is None:
        sys.exit(1)
    initialize_cell_method_warnings([])
    warnings_for_optimisation = []
    initialize_sn_issues(dict())

    #
    # --------------------------------------------------------------------
    # Extract CMOR variables for the experiment and year and lab settings
    # --------------------------------------------------------------------
    skipped_vars_per_table = {}
    actually_written_vars = []
    mip_vars_list = gather_AllSimpleVars(year, printout, select)
    # Group CMOR vars per realm
    svars_per_realm = dict()
    for svar in mip_vars_list:
        realm = svar.modeling_realm
        if realm not in svars_per_realm:
            svars_per_realm[realm] = []
        if svar not in svars_per_realm[realm]:
            add = True
            for ovar in svars_per_realm[realm]:
                if ovar.label == svar.label and ovar.spatial_shp == svar.spatial_shp \
                        and ovar.frequency == svar.frequency and ovar.cell_methods == svar.cell_methods:
                    add = False
            # Settings may allow for duplicate var in two tables. In DR01.00.21, this actually
            # applies to very few fields (ps-Aermon, tas-ImonAnt, areacellg)
            if get_variable_from_lset_with_default('allow_duplicates', True) or add:
                svars_per_realm[realm].append(svar)
            else:
                print "Not adding duplicate %s (from %s) for realm %s" % (svar.label, svar.mipTable, realm)
        else:
            old = svars_per_realm[realm][0]
            print "Duplicate svar %s %s %s %s" % (old.label, old.grid, svar.label, svar.grid)
            pass
    if printout:
        print "\nRealms for these CMORvars :", svars_per_realm.keys()
    #
    # --------------------------------------------------------------------
    # Select on context realms, grouping by table
    # Excluding 'excluded_vars' and 'excluded_spshapes' lists
    # --------------------------------------------------------------------
    svars_per_table = dict()
    context_realms = get_variable_from_lset_without_default('realms_per_context', context)
    processed_realms = []
    for realm in context_realms:
        if realm in processed_realms:
            continue
        processed_realms.append(realm)
        excludedv = dict()
        print "Processing realm '%s' of context '%s'" % (realm, context)
        # print 50*"_"
        excludedv = dict()
        if realm in svars_per_realm:
            for svar in svars_per_realm[realm]:
                # exclusion de certaines spatial shapes (ex. Polar Stereograpic Antarctic/Groenland)
                if svar.label not in get_variable_from_lset_without_default('excluded_vars') and \
                        svar.spatial_shp and \
                        svar.spatial_shp not in get_variable_from_lset_without_default("excluded_spshapes"):
                    if svar.mipTable not in svars_per_table:
                        svars_per_table[svar.mipTable] = []
                    svars_per_table[svar.mipTable].append(svar)
                else:
                    if printout:
                        reason = "unknown reason"
                        if svar.label in get_variable_from_lset_without_default('excluded_vars'):
                            reason = "They are in exclusion list "
                        if not svar.spatial_shp:
                            reason = "They have no spatial shape "
                        if svar.spatial_shp in get_variable_from_lset_without_default("excluded_spshapes"):
                            reason = "They have excluded spatial shape : %s" % svar.spatial_shp
                        if reason not in excludedv:
                            excludedv[reason] = []
                        excludedv[reason].append((svar.label, svar.mipTable))
        if printout and len(excludedv.keys()) > 0:
            print "The following pairs (variable,table) have been excluded for these reasons :"
            for reason in excludedv:
                print "\t", reason, ":", excludedv[reason]
    if debug:
        print "For table AMon: ", [v.label for v in svars_per_table["Amon"]]
    #
    # --------------------------------------------------------------------
    # Add svars belonging to the orphan list
    # --------------------------------------------------------------------
    if context in get_variable_from_lset_without_default('orphan_variables'):
        orphans = get_variable_from_lset_without_default('orphan_variables', context)
        for svar in mip_vars_list:
            if svar.label in orphans:
                if svar.label not in get_variable_from_lset_without_default('excluded_vars') and svar.spatial_shp and \
                        svar.spatial_shp not in get_variable_from_lset_without_default("excluded_spshapes"):
                    if svar.mipTable not in svars_per_table:
                        svars_per_table[svar.mipTable] = []
                    svars_per_table[svar.mipTable].append(svar)
    #
    # --------------------------------------------------------------------
    # Remove svars belonging to other contexts' orphan lists
    # --------------------------------------------------------------------
    for other_context in get_variable_from_lset_without_default('orphan_variables'):
        if other_context != context:
            orphans = get_variable_from_lset_without_default('orphan_variables', other_context)
            for table in svars_per_table:
                toremove = []
                for svar in svars_per_table[table]:
                    if svar.label in orphans:
                        toremove.append(svar)
                for svar in toremove:
                    svars_per_table[table].remove(svar)
    if debug:
        print "Pour table AMon: ", [v.label for v in svars_per_table["Amon"]]
    #
    # --------------------------------------------------------------------
    # Read ping_file defined variables
    # --------------------------------------------------------------------
    pingvars = []
    all_ping_refs = {}
    if pingfiles is not None:
        all_pingvars = []
        # print "pingfiles=",pingfiles
        for pingfile in pingfiles.split():
            ping_refs = read_xml_elmt_or_attrib(pingfile, tag='field', attrib='field_ref')
            # ping_refs=read_xml_elmt_or_attrib(pingfile, tag='field')
            if ping_refs is None:
                print "Error: issue accessing pingfile " + pingfile
                return
            all_ping_refs.update(ping_refs)
            if dummies == "include":
                pingvars = ping_refs.keys()
            else:
                pingvars = [v for v in ping_refs if 'dummy' not in ping_refs[v]]
                if dummies == "forbid":
                    if len(pingvars) != len(ping_refs):
                        for v in ping_refs:
                            if v not in pingvars:
                                print v,
                        print
                        raise dr2xml_error("They are still dummies in %s , while option is 'forbid' :" % pingfile)
                    else:
                        pingvars = ping_refs.keys()
                elif dummies == "skip":
                    pass
                else:
                    print "Forbidden option for dummies : " + dummies
                    sys.exit(1)
            all_pingvars.extend(pingvars)
        pingvars = all_pingvars
    #
    field_defs = dict()
    axis_defs = dict()
    grid_defs = dict()
    file_defs = dict()
    scalar_defs = dict()
    #
    # --------------------------------------------------------------------
    # Build all plev union axis and grids
    # --------------------------------------------------------------------
    if get_variable_from_lset_with_default('use_union_zoom', False):
        svars_full_list = []
        for svl in svars_per_table.values():
            svars_full_list.extend(svl)
        create_xios_axis_and_grids_for_plevs_unions(svars_full_list, multi_plev_suffixes.union(single_plev_suffixes),
                                                    dummies, axis_defs, grid_defs, field_defs, all_ping_refs,
                                                    printout=False)
    #
    # --------------------------------------------------------------------
    # Start writing XIOS file_def file:
    # file_definition node, including field child-nodes
    # --------------------------------------------------------------------
    # filename=dirname+"filedefs_%s.xml"%context
    filename = dirname + "dr2xml_%s.xml" % context
    with open(filename, "w") as out:
        out.write('<context id="%s"> \n' % context)
        out.write('<!-- CMIP6 Data Request version %s --> \n' % get_DR_version())
        out.write('<!-- CMIP6-CV version %s --> \n' % "??")
        out.write('<!-- CMIP6_conventions_version %s --> \n' % CMIP6_conventions_version)
        out.write('<!-- dr2xml version %s --> \n' % get_config_variable("version"))
        out.write('<!-- Lab_and_model settings : \n')
        for s, v in sorted(get_lset_iteritems()):
            out.write(' %s : %s\n' % (s, v))
        out.write('-->\n')
        out.write('<!-- Simulation settings : \n')
        for s, v in sorted(get_sset_iteritems()):
            out.write(' %s : %s\n' % (s, v))
        out.write('-->\n')
        out.write('<!-- Year processed is  %s --> \n' % year)
        #
        domain_defs = dict()
        # for table in ['day'] :
        out.write('\n<file_definition type="one_file" enabled="true" > \n')
        foo, sourcetype = get_source_id_and_type()
        for table in sorted(svars_per_table.keys()):
            count = dict()
            for svar in sorted(svars_per_table[table], key=lambda x: (x.label + "_" + table)):
                if get_variable_from_lset_with_default("allow_duplicates_in_same_table", False) \
                        or svar.mipVarLabel not in count:
                    if not get_variable_from_lset_with_default("use_cmorvar_label_in_filename", False) \
                            and svar.mipVarLabel in count:
                        form = "If you really want to actually produce both %s and %s in table %s, " + \
                               "you must set 'use_cmorvar_label_in_filename' to True in lab settings"
                        raise dr2xml_error(form % (svar.label, count[svar.mipVarLabel].label, table))
                    count[svar.mipVarLabel] = svar
                    for grid in svar.grids:
                        a, hgrid, b, c, d = get_variable_from_lset_without_default('grids', get_grid_choice(), context)
                        check_for_file_input(svar, hgrid, pingvars, field_defs, grid_defs, domain_defs, file_defs)
                        write_xios_file_def(svar, year, table, lset, sset, out, cvs_path,
                                            field_defs, axis_defs, grid_defs, domain_defs, scalar_defs, file_defs,
                                            dummies, skipped_vars_per_table, actually_written_vars,
                                            prefix, context, grid, pingvars, enddate, attributes)
                else:
                    print "Duplicate variable %s,%s in table %s is skipped, preferred is %s" % \
                          (svar.label, svar.mipVarLabel, table, count[svar.mipVarLabel].label)

        if cfsites_grid_id in grid_defs:
            out.write(cfsites_input_filedef())
        for file_def in file_defs:
            out.write(file_defs[file_def])
        out.write('\n</file_definition> \n')
        #
        # --------------------------------------------------------------------
        # End writing XIOS file_def file:
        # field_definition, axis_definition, grid_definition
        # and domain_definition auxilliary nodes
        # --------------------------------------------------------------------
        # Write all domain, axis, field defs needed for these file_defs
        out.write('<field_definition> \n')
        if get_variable_from_lset_with_default("nemo_sources_management_policy_master_of_the_world", False) \
                and context == 'nemo':
            out.write('<field_group freq_op="_reset_" freq_offset="_reset_" >\n')
        for obj in sorted(field_defs.keys()):
            out.write("\t" + field_defs[obj] + "\n")
        if get_variable_from_lset_with_default("nemo_sources_management_policy_master_of_the_world", False) \
                and context == 'nemo':
            out.write('</field_group>\n')
        out.write('\n</field_definition> \n')
        #
        out.write('\n<axis_definition> \n')
        out.write('<axis_group prec="8">\n')
        for obj in sorted(axis_defs.keys()):
            out.write("\t" + axis_defs[obj] + "\n")
        if False and get_variable_from_lset_with_default('use_union_zoom', False):
            for obj in sorted(union_axis_defs.keys()):
                out.write("\t" + union_axis_defs[obj] + "\n")
        out.write('</axis_group>\n')
        out.write('</axis_definition> \n')
        #
        out.write('\n<domain_definition> \n')
        out.write('<domain_group prec="8">\n')
        if get_variable_from_lset_without_default('grid_policy') != "native":
            create_standard_domains(domain_defs)
        for obj in sorted(domain_defs.keys()):
            out.write("\t" + domain_defs[obj] + "\n")
        out.write('</domain_group>\n')
        out.write('</domain_definition> \n')
        #
        out.write('\n<grid_definition> \n')
        for obj in grid_defs.keys():
            out.write("\t" + grid_defs[obj])
        if False and lset.get('use_union_zoom', False):
            for obj in sorted(union_grid_defs.keys()):
                out.write("\t" + union_grid_defs[obj] + "\n")
        out.write('</grid_definition> \n')
        #
        out.write('\n<scalar_definition> \n')
        for obj in sorted(scalar_defs.keys()):
            out.write("\t" + scalar_defs[obj] + "\n")
        out.write('</scalar_definition> \n')
        #
        out.write('</context> \n')
    if printout:
        print "\nfile_def written as %s" % filename

    # mpmoine_petitplus:generate_file_defs: pour sortir des stats sur ce que l'on sort reelement
    # SS - non : gros plus
    if printout:
        print_SomeStats(context, svars_per_table, skipped_vars_per_table,
                        actually_written_vars, get_variable_from_lset_with_default("print_stats_per_var_label", False))

    warn = dict()
    for warning, label, table in get_cell_method_warnings():
        if warning not in warn:
            warn[warning] = set()
        warn[warning].add(label)
    if len(warn) > 0:
        print "\nWarnings about cell methods (with var list)"
        for w in warn:
            print "\t", w, " for vars : ", warn[w]
    if len(warnings_for_optimisation) > 0:
        print "Warning for fields which cannot be optimised (i.e. average before remap) because of an expr with @\n\t",
        for w in warnings_for_optimisation:
            print w.replace(get_variable_from_lset_without_default('ping_variables_prefix'), ""),
        print


def create_xios_axis_and_grids_for_plevs_unions(svars, plev_sfxs, dummies, axis_defs, grid_defs, field_defs, ping_refs,
                                                printout=False):
    """
    Objective of this function is to optimize Xios vertical interpolation requested in pressure levels.
    Process in 2 steps:
    * First, search pressure levels unions for each simple variable label without psuffix and build a dictionnary :
        dict_plevs is a 3-level intelaced dictionnary containing for each var (key=svar label_without_psuffix),
        the list of svar (key=svar label,value=svar object) per pressure levels set (key=sdim label):
        { "varX":
              { "plevA": {"svar1":svar1,"svar2":svar2,"svar3":svar3},
                "plevB": {"svar4":svar4,"svar5":svar5},
                "plevC": {"svar6":svar6} },
          "varY":
             { "plevA": {"svar7":svar7},
               "plevD": {"svar8":svar8,"svar9":svar9} }
        }
    * Second, create create all of the Xios union axis (axis id: union_plevs_<label_without_psuffix>)
    """
    #
    prefix = get_variable_from_lset_without_default("ping_variables_prefix")
    # First, search plev unions for each label_without_psuffix and build dict_plevs
    dict_plevs = {}
    for sv in svars:
        if not sv.modeling_realm:
            print "Warning: no modeling_realm associated to:", sv.label, sv.mipTable, sv.mip_era
        for sd in sv.sdims.values():
            # couvre les dimensions verticales de type 'plev7h' ou 'p850'
            if sd.label.startswith("p") and any(sd.label.endswith(s) for s in plev_sfxs) and sd.label != 'pl700':
                lwps = sv.label_without_psuffix
                if lwps:
                    present_in_ping = (prefix + lwps) in ping_refs
                    dummy_in_ping = None
                    if present_in_ping:
                        dummy_in_ping = ("dummy" in ping_refs[prefix + lwps])

                    if present_in_ping and (not dummy_in_ping or dummies == 'include'):
                        sv.sdims[sd.label].is_zoom_of = "union_plevs_" + lwps
                        if lwps not in dict_plevs:
                            dict_plevs[lwps] = {sd.label: {sv.label: sv}}
                        else:
                            if sd.label not in dict_plevs[lwps]:
                                dict_plevs[lwps].update({sd.label: {sv.label: sv}})
                            else:
                                if sv.label not in dict_plevs[lwps][sd.label].keys():
                                    dict_plevs[lwps][sd.label].update({sv.label: sv})
                                else:
                                    # TBS# print sv.label,"in table",sv.mipTable,"already listed for",sd.label
                                    pass
                    else:
                        if printout:
                            print "Info: ", lwps, "not taken into account for building plevs union axis because ", \
                                prefix + lwps,
                            if not present_in_ping:
                                print "is not an entry in the pingfile"
                            else:
                                print "has a dummy reference in the pingfile"

                    # svar will be expected on a zoom axis of the union. Corresponding vertical dim must
                    # have a zoom_label named plevXX_<lwps> (multiple pressure levels)
                    # or pXX_<lwps> (single pressure level)
                    sv.sdims[sd.label].zoom_label = 'zoom_' + sd.label + "_" + lwps
                else:
                    print "Warning: dim is pressure but label_without_psuffix=", lwps, \
                        "for", sv.label, sv.mipTable, sv.mip_era
            # else :
            #    print "for var %s/%s, dim %s is not related to pressure"%(sv.label,sv.label_without_psuffix,sd.label)
    #
    # Second, create xios axis for union of plevs
    union_axis_defs = axis_defs
    union_grid_defs = grid_defs
    # union_axis_defs={}
    # union_grid_defs={}
    for lwps in dict_plevs.keys():
        sdim_union = simple_Dim()
        plevs_union_xios = ""
        plevs_union = set()
        for plev in dict_plevs[lwps].keys():
            plev_values = []
            for sv in dict_plevs[lwps][plev].values():
                if not plev_values:
                    # svar is the first one with this plev => get its level values
                    # on reecrase les attributs de sdim_union a chaque nouveau plev. Pas utile mais
                    # c'est la facon la plus simple de faire
                    sdsv = sv.sdims[plev]
                    if sdsv.stdname:
                        sdim_union.stdname = sdsv.stdname
                    if sdsv.long_name:
                        sdim_union.long_name = sdsv.long_name
                    if sdsv.positive:
                        sdim_union.positive = sdsv.positive
                    if sdsv.out_name:
                        sdim_union.out_name = sdsv.out_name
                    if sdsv.units:
                        sdim_union.units = sdsv.units
                    if sdsv.requested:
                        # case of multi pressure levels
                        plev_values = set(sdsv.requested.split())
                        sdim_union.is_union_for.append(sv.label + "_" + sd.label)
                    elif sdsv.value:
                        # case of single pressure level
                        plev_values = set(sdsv.value.split())
                        sdim_union.is_union_for.append(sv.label + "_" + sd.label)
                    else:
                        print "Warning: No requested nor value found for", svar.label, "with vertical dimesion", plev
                    plevs_union = plevs_union.union(plev_values)
                    if printout:
                        print "    -- on", plev, ":", plev_values
                if printout:
                    print "       *", sv.label, "(", sv.mipTable, ")"
        list_plevs_union = list(plevs_union)
        list_plevs_union_num = [float(lev) for lev in list_plevs_union]
        list_plevs_union_num.sort(reverse=True)
        list_plevs_union = [str(lev) for lev in list_plevs_union_num]
        for lev in list_plevs_union:
            plevs_union_xios += " " + lev
        if printout:
            print ">>> XIOS plevs union:", plevs_union_xios
        sdim_union.label = "union_plevs_" + lwps
        if len(list_plevs_union) > 1:
            sdim_union.requested = plevs_union_xios
        if len(list_plevs_union) == 1:
            sdim_union.value = plevs_union_xios
        if printout:
            print "creating axis def for union :%s" % sdim_union.label
        axis_def = create_axis_def(sdim_union, union_axis_defs, field_defs)
        create_grid_def(union_grid_defs, axis_def, sdim_union.out_name,
                        id2gridid(prefix + lwps, get_config_variable("context_index")))
    #
    # return (union_axis_defs,union_grid_defs)


#
def pingFileForRealmsList(settings, context, lrealms, svars, path_special, dummy="field_atm",
                          dummy_with_shape=False, exact=False,
                          comments=False, prefix="CV_", filename=None, debug=[]):
    """Based on a list of realms LREALMS and a list of simplified vars
    SVARS, create the ping file which name is ~
    ping_<realms_list>.xml, which defines fields for all vars in
    SVARS, with a field_ref which is either 'dummy' or '?<varname>'
    (depending on logical DUMMY)

    If EXACT is True, the match between variable realm string and one
    of the realm string in the list must be exact. Otherwise, the
    variable realm must be included in (or include) one of the realm list
    strings

    COMMENTS, if not False nor "", will drive the writing of variable
    description and units as an xml comment. If it is a string, it
    will be printed before this comment string (and this allows for a
    line break)

    DUMMY, if not false, should be either 'True', for a standard dummy
    label or a string used as the name of all field_refs. If False,
    the field_refs look like ?<variable name>.

    If DUMMY is True and DUMMY_WITH_SHAPE is True, dummy labels wiill
    include the highest rank shape requested by the DR, for
    information

    Field ids do include the provided PREFIX

    The ping file includes a <field_definition> construct

    For those MIP varnames which have a corresponding field_definition
    in a file named like ./inputs/DX_field_defs_<realm>.xml (path being
    relative to source code location), this latter field_def is
    inserted in the ping file (rather than a default one). This brings
    a set of 'standard' definitions fo variables which can be derived
    from DR-standard ones

    """
    name = ""
    for r in lrealms:
        name += "_" + r.replace(" ", "%")
    lvars = []
    for v in svars:
        if exact:
            if any([v.modeling_realm == r for r in lrealms]):
                lvars.append(v)
        else:
            var_realms = v.modeling_realm.split(" ")
            if any([v.modeling_realm == r or r in var_realms
                    for r in lrealms]):
                lvars.append(v)
        if context in settings['orphan_variables'] and \
                v.label in settings['orphan_variables'][context]:
            lvars.append(v)
    lvars.sort(key=lambda x: x.label_without_psuffix)

    # Remove duplicates : want to get one single entry for all variables having
    # the same label without psuffix, and one for each having different non-ambiguous label
    # Keep the one with the best piority
    uniques = []
    best_prio = dict()
    for v in lvars:
        lna = v.label_non_ambiguous
        lwps = v.label_without_psuffix
        if (lna not in best_prio) or (lna in best_prio and v.Priority < best_prio[lna].Priority):
            best_prio[lna] = v
        elif (lwps not in best_prio) or (lwps in best_prio and v.Priority < best_prio[lwps].Priority):
            best_prio[lwps] = v
        # elif not v.label_without_psuffix in labels :
        #    uniques.append(v); labels.append(v.label_without_psuffix)

    # lvars=uniques
    lvars = best_prio.values()
    lvars.sort(key=lambda x: x.label_without_psuffix)
    #
    if filename is None:
        filename = "ping" + name + ".xml"
    if filename[-4:] != ".xml":
        filename += ".xml"
    #
    if path_special:
        specials = read_special_fields_defs(lrealms, path_special)
    else:
        specials = False
    with open(filename, "w") as fp:
        fp.write('<!-- Ping files generated by dr2xml %s using Data Request %s -->\n' % (get_config_variable("varsion"),
                                                                                         get_DR_version()))
        fp.write('<!-- lrealms= %s -->\n' % `lrealms`)
        fp.write('<!-- exact= %s -->\n' % `exact`)
        fp.write('<!-- ')
        for s in settings:
            fp.write(' %s : %s\n' % (s, settings[s]))
        fp.write('--> \n\n')
        fp.write('<context id="%s">\n' % context)
        fp.write("<field_definition>\n")
        if settings.get("nemo_sources_management_policy_master_of_the_world", False) and context == 'nemo':
            out.write('<field_group freq_op="_reset_ freq_offset="_reset_" >\n')
        if exact:
            fp.write("<!-- for variables which realm intersects any of " + name + "-->\n")
        else:
            fp.write("<!-- for variables which realm equals one of " + name + "-->\n")
        for v in lvars:
            if v.label_non_ambiguous:
                label = v.label_non_ambiguous
            else:
                label = v.label_without_psuffix
            if v.label in debug:
                print "pingFile ... processing %s in table %s, label=%s" % (v.label, v.mipTable, label)

            if specials and label in specials:
                line = ET.tostring(specials[label]).replace("DX_", prefix)
                # if 'ta' in label : print "ta is special : "+line
                line = line.replace("\n", "").replace("\t", "")
                fp.write('   ')
                fp.write(line)
            else:
                fp.write('   <field id="%-20s' % (prefix + label + '"') + ' field_ref="')
                if dummy:
                    shape = highest_rank(v)
                    if v.label_without_psuffix == 'clcalipso':
                        shape = 'XYA'
                    if dummy is True:
                        dummys = "dummy"
                        if dummy_with_shape:
                            dummys += "_" + shape
                    else:
                        dummys = dummy
                    fp.write('%-18s/>' % (dummys + '"'))
                else:
                    fp.write('?%-16s' % (label + '"') + ' />')
            if comments:
                # Add units, stdname and long_name as a comment string
                if type(comments) == type(""):
                    fp.write(comments)
                fp.write("<!-- P%d (%s) %s : %s -->" % (v.Priority, v.units, v.stdname, v.description))
            fp.write("\n")
        if 'atmos' in lrealms or 'atmosChem' in lrealms or 'aerosol' in lrealms:
            for tab in ["ap", "ap_bnds", "b", "b_bnds"]:
                fp.write('\t<field id="%s%s" field_ref="dummy_hyb" /><!-- One of the hybrid coordinate arrays -->\n'
                         % (prefix, tab))
        if settings.get("nemo_sources_management_policy_master_of_the_world", False) and context == 'nemo':
            out.write('</field_group>\n')
        fp.write("</field_definition>\n")
        #
        print "%3d variables written for %s" % (len(lvars), filename)
        #
        # Write axis_defs, domain_defs, ... read from relevant input/DX_ files
        if path_special:
            for obj in ["axis", "domain", "grid", "field"]:
                copy_obj_from_DX_file(fp, obj, prefix, lrealms, path_special)
        fp.write('</context>\n')


def copy_obj_from_DX_file(fp, obj, prefix, lrealms, path_special):
    # Insert content of DX_<obj>_defs files (changing prefix)
    # print "copying %s defs :"%obj,
    subrealms_seen = []
    for realm in lrealms:
        for subrealm in realm.split():
            if subrealm in subrealms_seen:
                continue
            subrealms_seen.append(subrealm)
            # print "\tand realm %s"%subrealm,
            defs = DX_defs_filename(obj, subrealm, path_special)
            if os.path.exists(defs):
                with open(defs, "r") as fields:
                    # print "from %s"%defs
                    fp.write("\n<%s_definition>\n" % obj)
                    lines = fields.readlines()
                    for line in lines:
                        if not obj + "_definition" in line:
                            fp.write(line.replace("DX_", prefix))
                    fp.write("</%s_definition>\n" % obj)
            else:
                pass
                print " no file :%s " % defs


def DX_defs_filename(obj, realm, path_special):
    # TBS# return prog_path+"/inputs/DX_%s_defs_%s.xml"%(obj,realm)
    return path_special + "/DX_%s_defs_%s.xml" % (obj, realm)


def get_xml_childs(elt, tag='field', groups=['context', 'field_group',
                                             'field_definition', 'axis_definition', 'axis', 'domain_definition',
                                             'domain', 'grid_definition', 'grid', 'interpolate_axis']):
    """
        Returns a list of elements in tree ELT
        which have tag TAG, by digging in sub-elements
        named as in GROUPS
        """
    if elt.tag in groups:
        rep = []
        for child in elt:
            rep.extend(get_xml_childs(child, tag))
        return rep
    elif elt.tag == tag:
        return [elt]
    else:
        # print 'Syntax error : tag %s not allowed'%elt.tag
        # Case of an unkown tag : don't dig in
        return []


def read_xml_elmt_or_attrib(filename, tag='field', attrib=None, printout=False):
    """
    Returns a dict of objects tagged TAG in FILENAME, which
    - keys are ids
    - values depend on ATTRIB
          * if ATTRIB is None : object (elt)
          * else : values of attribute ATTRIB  (None if field does not have attribute ATTRIB)
    Returns None if filename does not exist
    """
    #
    rep = dict()
    if printout:
        print "processing file %s :" % filename,
    if os.path.exists(filename):
        if printout:
            print "OK", filename
        root = ET.parse(filename).getroot()
        defs = get_xml_childs(root, tag)
        if defs:
            for field in defs:
                if printout:
                    print ".",
                key = field.attrib['id']
                if attrib is None:
                    value = field
                else:
                    value = field.attrib.get(attrib, None)
                rep[key] = value
            if printout:
                print
            return rep
    else:
        if printout:
            print "No file "
        return None


def read_special_fields_defs(realms, path_special, printout=False):
    special = dict()
    subrealms_seen = []
    for realm in realms:
        for subrealm in realm.split():
            if subrealm in subrealms_seen:
                continue
            subrealms_seen.append(subrealm)
            d = read_xml_elmt_or_attrib(DX_defs_filename("field", subrealm, path_special), tag='field',
                                        printout=printout)
            if d:
                special.update(d)
    rep = dict()
    # Use raw label as key
    for r in special:
        rep[r.replace("DX_", "")] = special[r]
    return rep


def highest_rank(svar):
    """Returns the shape with the highest needed rank among the CMORvars
    referencing a MIPvar with this label
    This, assuming dr2xml would handle all needed shape reductions
    """
    # mipvarlabel=svar.label_without_area
    mipvarlabel = svar.label_without_psuffix
    shapes = []
    altdims = set()
    for cvar in get_collection('CMORvar').items:
        v = get_uid(cvar.vid)
        if v.label == mipvarlabel:
            try:
                st = get_uid(cvar.stid)
                try:
                    sp = get_uid(st.spid)
                    shape = sp.label
                except:
                    if print_DR_errors:
                        print "DR Error: issue with spid for " + \
                              st.label + " " + v.label + string(cvar.mipTable)
                    # One known case in DR 1.0.2: hus in 6hPlev
                    shape = "XY"
                if "odims" in st.__dict__:
                    try:
                        map(altdims.add, st.odims.split("|"))
                    except:
                        print "Issue with odims for " + v.label + " st=" + st.label
            except:
                print "DR Error: issue with stid for :" + v.label + " in table section :" + str(cvar.mipTableSection)
                shape = "?st"
        else:
            # Pour recuperer le spatial_shp pour le cas de variables qui n'ont
            # pas un label CMORvar de la DR (ex. HOMEvar ou EXTRAvar)
            shape = svar.spatial_shp
        if shape:
            shapes.append(shape)
    # if not shapes : shape="??"
    if len(shapes) == 0:
        shape = "XY"
    elif any(["XY-A" in s for s in shapes]):
        shape = "XYA"
    elif any(["XY-O" in s for s in shapes]):
        shape = "XYO"
    elif any(["XY-AH" in s for s in shapes]):
        shape = "XYAh"  # Zhalf
    elif any(["XY-SN" in s for s in shapes]):
        shape = "XYSn"  # snow levels
    elif any(["XY-S" in s for s in shapes]):
        shape = "XYSo"  # soil levels
    elif any(["XY-P" in s for s in shapes]):
        shape = "XYA"
    elif any(["XY-H" in s for s in shapes]):
        shape = "XYA"
    #
    elif any(["XY-na" in s for s in shapes]):
        shape = "XY"  # analyser realm, pb possible sur ambiguite singleton
    #
    elif any(["YB-na" in s for s in shapes]):
        shape = "basin_zonal_mean"
    elif any(["YB-O" in s for s in shapes]):
        shape = "basin_merid_section"
    elif any(["YB-R" in s for s in shapes]):
        shape = "basin_merid_section_density"
    elif any(["S-A" in s for s in shapes]):
        shape = "COSP-A"
    elif any(["S-AH" in s for s in shapes]):
        shape = "COSP-AH"
    elif any(["na-A" in s for s in shapes]):
        shape = "site-A"
    elif any(["Y-A" in s for s in shapes]):
        shape = "XYA"  # lat-A
    elif any(["Y-P" in s for s in shapes]):
        shape = "XYA"  # lat-P
    elif any(["Y-na" in s for s in shapes]):
        shape = "lat"
    elif any(["TRS-na" in s for s in shapes]):
        shape = "TRS"
    elif any(["TR-na" in s for s in shapes]):
        shape = "TR"
    elif any(["L-na" in s for s in shapes]):
        shape = "COSPcurtain"
    elif any(["L-H40" in s for s in shapes]):
        shape = "COSPcurtainH40"
    elif any(["S-na" in s for s in shapes]):
        shape = "XY"  # fine once remapped
    elif any(["na-na" in s for s in shapes]):
        shape = "0d"  # analyser realm
    # else : shape="??"
    else:
        shape = "XY"
    #
    for d in altdims:
        dims = d.split(' ')
        for dim in dims:
            shape += "_" + dim
    #
    return shape


def create_standard_domains(domain_defs):
    """
    Add to dictionnary domain_defs the Xios string representation for DR-standard horizontal grids, such as '1deg'

    """
    # Next definition is just for letting the workflow work when using option dummy='include'
    # Actually, ping_files for production run at CNRM do not activate variables on that grid (IceSheet vars)
    domain_defs['25km'] = create_standard_domain('25km', 1440, 720)
    domain_defs['50km'] = create_standard_domain('50km', 720, 360)
    domain_defs['100km'] = create_standard_domain('100km', 360, 180)
    domain_defs['1deg'] = create_standard_domain('1deg', 360, 180)
    domain_defs['2deg'] = create_standard_domain('2deg', 180, 90)


def create_standard_domain(resol, ni, nj):
    return '<domain id="CMIP6_%s" ni_glo="%d" nj_glo="%d" type="rectilinear"  prec="8"> ' % (resol, ni, nj) + \
           '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  ' \
           'mode="read_or_compute" write_weight="true" /> ' + \
           '</domain>  '
    # return '<domain id="CMIP6_%s" ni_glo="%d" nj_glo="%d" type="rectilinear"  prec="8" lat_name="lat" lon_name="lon" >
    #  '%(resol,ni,nj) +\
    #    '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute"
    #  write_weight="true" /> '+\
    #    '</domain>  '


def RequestItemInclude(ri, var_label, freq):
    """
    test if a variable is requested by a requestItem at a given freq
    """
    varGroup = get_uid(get_uid(ri.rlid).refid)
    reqVars = get_request_by_id_by_sect(varGroup.uid, 'requestVar')
    cmVars = [get_uid(get_uid(reqvar).vid) for reqvar in reqVars]
    return any([cmv.label == var_label and cmv.frequency == freq for cmv in cmVars])


def realm_is_processed(realm, source_type):
    """
    Tells if a realm is definitely not processed by a source type

    list of source-types : AGCM BGC AER CHEM LAND OGCM AOGCM
    list of known realms : ['seaIce', '', 'land', 'atmos atmosChem', 'landIce', 'ocean seaIce',
                            'landIce land', 'ocean', 'atmosChem', 'seaIce ocean', 'atmos',
                             'aerosol', 'atmos land', 'land landIce', 'ocnBgChem']
    """
    components = source_type.split(" ")
    rep = True
    #
    if realm == "atmosChem" and 'CHEM' not in components:
        return False
    if realm == "aerosol" and 'AER' not in components:
        return False
    if realm == "ocnBgChem" and 'BGC' not in components:
        return False
    #
    with_ocean = ('OGCM' in components or 'AOGCM' in components)
    if 'seaIce' in realm and not with_ocean:
        return False
    if 'ocean' in realm and not with_ocean:
        return False
    #
    with_atmos = ('AGCM' in components or 'AOGCM' in components)
    if 'atmos' in realm and not with_atmos:
        return False
    if 'atmosChem' in realm and not with_atmos:
        return False
    if realm == '' and not with_atmos:  # In DR 01.00.15 : some atmos variables have realm=''
        return False
    #
    with_land = with_atmos or ('LAND' in components)
    if 'land' in realm and not with_land:
        return False
    #
    return rep


def check_for_file_input(sv, hgrid, pingvars, field_defs, grid_defs, domain_defs, file_defs, printout=False):
    """


    Add an entry in pingvars
    """
    externs = get_variable_from_lset_with_default('fx_from_file', [])
    # print "/// sv.label=%s"%sv.label, sv.label in externs ,"hgrid=",hgrid
    if sv.label in externs and \
            any([d == hgrid for d in externs[sv.label]]):
        pingvar = get_variable_from_lset_without_default('ping_variables_prefix') + sv.label
        pingvars.append(pingvar)
        # Add a grid made of domain hgrid only
        grid_id = "grid_" + hgrid
        grid_def = '<grid id="%s"><domain domain_ref="%s"/></grid>\n' % (grid_id, hgrid)

        # Add a grid and domain for reading the file (don't use grid above to avoid reampping)
        file_domain_id = "remapped_%s_file_domain" % sv.label
        domain_defs[file_domain_id] = '<domain id="%s" type="rectilinear" >' % file_domain_id + \
                                      '<generate_rectilinear_domain/></domain>'
        file_grid_id = "remapped_%s_file_grid" % sv.label
        grid_defs[file_grid_id] = '<grid id="%s"><domain domain_ref="%s"/></grid>\n' % (file_grid_id, file_domain_id)
        if printout:
            print domain_defs[file_domain_id]
        if printout:
            print grid_defs[file_grid_id]

        # Create xml for reading the variable
        filename = externs[sv.label][hgrid][get_grid_choice()]
        file_id = "remapped_%s_file" % sv.label
        field_in_file_id = "%s_%s" % (sv.label, hgrid)
        # field_in_file_id=sv.label
        file_def = '\n<file id="%s" name="%s" mode="read" output_freq="1ts" enabled="true" >' % \
                   (file_id, filename)
        file_def += '\n\t<field id="%s" name="%s" operation="instant" freq_op="1ts" freq_offset="1ts" grid_ref="%s"/>'\
                    % (field_in_file_id, sv.label, file_grid_id)
        file_def += '\n</file>'
        file_defs[file_id] = file_def
        if printout:
            print file_defs[file_id]
        #
        # field_def='<field id="%s" grid_ref="%s" operation="instant" >%s</field>'%\
        field_def = '<field id="%s" grid_ref="%s" field_ref="%s" operation="instant" freq_op="1ts" ' \
                    'freq_offset="0ts" />' % (pingvar, grid_id, field_in_file_id)
        field_defs[field_in_file_id] = field_def
        context_index = get_config_variable("context_index")
        context_index[pingvar] = ET.fromstring(field_def)

        if printout:
            print field_defs[field_in_file_id]
        #
