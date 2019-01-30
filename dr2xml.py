#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
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
from config import get_config_variable, set_config_variable
from grids import get_grid_def, guess_simple_domain_grid_def, create_grid_def, create_axis_def, change_domain_in_grid, \
    get_grid_def_with_lset, change_axes_in_grid, isVertDim, scalar_vertical_dimension
from postprocessing import process_vertical_interpolation, process_zonal_mean, process_diurnal_cycle
from vars_selection import endyear_for_CMORvar, RequestItem_applies_for_exp_and_year, select_CMORvars_for_lab, \
    gather_AllSimpleVars, get_sc, initialize_sn_issues

version = "1.16"
print "\n", 50 * "*", "\n*"
print "* %29s" % "dr2xml version: ", version

conventions = "CF-1.7 CMIP-6.2"
# The current code should comply with this version of spec doc at
# https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit
CMIP6_conventions_version = "v6.2.4"
print "* %29s" % "CMIP6 conventions version: ", CMIP6_conventions_version

import json

import datetime
import re
import collections
import sys, os, glob
import xml.etree.ElementTree as ET

# mpmoine_merge_dev2_v0.12: posixpath.dirname ne marche pas chez moi
# TBS# from os import path as os_path
# TBS# prog_path=os_path.abspath(os_path.split(__file__)[0])

# Local packages
from vars import simple_CMORvar, simple_Dim, process_homeVars, complement_svar_using_cmorvar, \
    multi_plev_suffixes, single_plev_suffixes, get_simplevar
from grids_selection import decide_for_grids
from split_frequencies import split_frequency_for_variable, timesteps_per_freq_and_duration
from Xparse import init_context, id2grid, id2gridid, idHasExprWithAt

# Time settings
from settings import freq2datefmt, analyze_cell_time_method, Cmip6Freq2XiosFreq, longest_possible_period, \
    initialize_cell_method_warnings, get_cell_method_warnings, DRgrid2gridatts

# Statistics module
from stats import print_SomeStats

# Simulations and laboratory settings dictionnaries interface
from dict_interface import initialize_dict, get_variable_from_lset_with_default, get_variable_from_lset_without_default, \
    is_key_in_sset, get_variable_from_sset_without_default, is_sset_not_None, get_source_id_and_type, \
    get_variable_from_sset_and_lset_without_default, get_variable_from_sset_with_default_in_sset, \
    get_variable_from_sset_with_default, is_key_in_lset, get_variable_from_sset_else_lset_with_default, \
    get_lset_iteritems, get_sset_iteritems

# Utilities
from utils import dr2xml_error

# Data request interface
from dr_interface import get_DR_version, initialize_sc, get_collection, get_uid, get_request_by_id_by_sect, \
    get_experiment_label

# A auxilliary tables

# CFsites handling has its own module
from cfsites import cfsites_domain_id, cfsites_grid_id, cfsites_input_filedef, add_cfsites_in_defs

print_DR_errors = True

print "* %29s" % "CMIP6 Data Request version: ", get_DR_version()
print "\n*\n", 50 * "*"

warnings_for_optimisation = []

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
        "LR": {'AerChemMIP', 'C4MIP', 'CFMIP', 'DAMIP', 'FAFMIP', 'GeoMIP', 'GMMIP', 'ISMIP6', \
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
        "60mi": ['parasolRefl', 'clhcalipso', 'cltcalipso', 'cllcalipso', 'clmcalipso', \
                 'cfadLidarsr532', 'clcalipso', 'clcalipso2', 'cfadDbze94', \
                 'jpdftaureliqmodis', 'clisccp', 'jpdftaureicemodis', 'clmisr'],
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
        "AGCM": ["ch4", "co2", "co", "concdust", "ec550aer", "h2o", "hcho", "hcl", \
                 "hno3", "mmrbc", "mmrdust", "mmroa", "mmrso4", "mmrss", \
                 "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", "so2"],
        "AOGCM": ["ch4", "co2", "co", "concdust", "ec550aer", "h2o", "hcho", "hcl", \
                  "hno3", "mmrbc", "mmrdust", "mmroa", "mmrso4", "mmrss", \
                  "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", "so2"],
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
                       "data regridded to a T127 gaussian grid (128x256 latlon) from a native atmosphere T127l reduced gaussian grid"],
            "trip": ["gn", "", "", "50 km", "regular 1/2 deg lat-lon grid"],
            "nemo": ["gn", "", "", "100 km", "native ocean tri-polar grid with 105 k ocean cells"], },

        "HR": {
            "surfex": ["gr", "complete", "glat", "50 km",
                       "data regridded to a 359 gaussian grid (180x360 latlon) from a native atmosphere T359l reduced gaussian grid"],
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
                    'Bare_soil Rock Permanent_snow Temperate_broad-leaved_decidus Boreal_needleaf_evergreen Tropical_broad-leaved_evergreen C3_crop C4_crop Irrigated_crop C3_grass C4_grass Wetland Tropical_broad-leaved_decidus Temperate_broad-leaved_evergreen Temperate_needleaf_evergreen Boreal_broad-leaved_decidus Boreal_needleaf_decidus Tundra_grass Shrub'),

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
                           "HR": "areacella_HR", }}},

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
    # "branch_time_in_parent": "365.0D0", # a double precision value, in days, used if branch_year_in_parent is not applicable
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
        'tas': 'this is a dummy comment, placeholder for describing a special, simulation dependent, scheme for a given variable',
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


# def hasCMORVarName(hmvar):
#    for cmvar in get_collection('CMORvar').items:
#        if (cmvar.label==hmvar.label): return True


def wr(out, key, dic_or_val=None, num_type="string", default=None):
    global print_wrv
    if not print_wrv: return
    """
    Short cut for a repetitive pattern : writing in 'out' 
    a string variable name and value
    If dic_or_val is not None 
      if  dic_or_val is a dict, 
        if key is in value is dic_or_val[key], 
        otherwise use default as value , except if default is False
      otherwise, use arg dic_or_val as value if not None nor False,
    otherwise use value of local variable 'key'
    """
    val = None
    if type(dic_or_val) == type({}):
        if key in dic_or_val:
            val = dic_or_val[key]
        else:
            if default is not None:
                if default is not False: val = default
            else:
                print 'error : %s not in dic and default is None' % key
    else:
        if dic_or_val is not None:
            val = dic_or_val
        else:
            print 'error in wr,  no value provided for %s' % key
    if val:
        if num_type == "string":
            # val=val.replace(">","&gt").replace("<","&lt").replace("&","&amp").replace("'","&apos").replace('"',"&quot").strip()
            val = val.replace(">", "&gt").replace("<", "&lt").strip()
            # CMIP6 spec : no more than 1024 char
            val = val[0:1024]
        if num_type != "string" or len(val) > 0:
            out.write('  <variable name="%s"  type="%s" > %s ' % (key, num_type, val))
            out.write('  </variable>\n')


def write_xios_file_def(sv, year, table, lset, sset, out, cvspath,
                        field_defs, axis_defs, grid_defs, domain_defs, scalar_defs, file_defs,
                        dummies, skipped_vars_per_table, actually_written_vars,
                        prefix, context, grid, pingvars=None, enddate=None,
                        attributes=[], debug=[]):
    """
    Generate an XIOS file_def entry in out for :
      - a dict for laboratory settings
      - a dict of simulation settings
      - a 'simplifed CMORvar' sv
      - which all belong to given table
      - a path 'cvs' for Controlled Vocabulary

    Lenghty code, but not longer than the corresponding specification document

    1- After a prologue, attributes valid for all variables are
    written as file-level metadata, in the same order than in
    WIP document;
    2- Next, field-level metadata are written
    3- For 3D variables in model levels or half-levels, also write the auxilliary
    variables requested by CF convention (e.g. for hybrid coordinate, surface_pressure field
    plus AP and B arrays and their bounds, and lev + lev_bnds with formula attribute)
    """
    #
    # If list of included vars has size 1, activate debug on the corresponding variable
    inc = get_variable_from_lset_with_default('included_vars', [])
    if len(inc) == 1: debug = inc

    # gestion des attributs pour lesquels on a recupere des chaines vides (" " est Faux mais est ecrit " "")
    # --------------------------------------------------------------------
    # Put a warning for field attributes that shouldn't be empty strings
    # --------------------------------------------------------------------
    # if not sv.stdname       : sv.stdname       = "missing" #"empty in DR "+get_DR_version()
    if not sv.long_name:
        sv.long_name = "empty in DR " + get_DR_version()
    # if not sv.cell_methods  : sv.cell_methods  = "empty in DR "+get_DR_version()
    # if not sv.cell_measures : sv.cell_measures = "cell measure is not specified in DR "+get_DR_version()
    if not sv.units:
        sv.units = "empty in DR " + get_DR_version()

    # --------------------------------------------------------------------
    # Define alias for field_ref in file-def file
    # - may be replaced by alias1 later
    # - this is not necessarily the alias used in ping file because of
    #   intermediate field id(s) due to union/zoom
    # --------------------------------------------------------------------
    # We use a simple convention for variable names in ping files :
    if sv.type == 'perso':
        alias = sv.label
    else:
        # MPM : si on a defini un label non ambigu alors on l'utilise comme alias (i.e. le field_ref)
        # et pour l'alias seulement (le nom de variable dans le nom de fichier restant svar.label)
        if sv.label_non_ambiguous:
            alias = get_variable_from_lset_without_default("ping_variables_prefix") + sv.label_non_ambiguous
        else:
            # 'tau' is ambiguous in DR 01.00.18 : either a variable name (stress)
            # or a dimension name (optical thickness). We choose to rename the stress
            if sv.label != "tau":
                alias = get_variable_from_lset_without_default("ping_variables_prefix") + sv.label
            else:
                alias = get_variable_from_lset_without_default("ping_variables_prefix") + "tau_stress"
        if (sv.label in debug):
            print "write_xios_file_def ... processing %s, alias=%s" % (sv.label, alias)

        # suppression des terminaisons en "Clim" pour l'alias : elles concernent uniquement les cas
        # d'absence de variation inter-annuelle sur les GHG. Peut-etre genant pour IPSL ?
        # Du coup, les simus avec constance des GHG (picontrol) sont traitees comme celles avec variation
        split_alias = alias.split("Clim")
        alias = split_alias[0]
        if pingvars is not None:
            # Get alias without pressure_suffix but possibly with area_suffix
            alias_ping = ping_alias(sv, pingvars)
    #
    # process only variables in pingvars
    if not alias_ping in pingvars:
        # print "+++ =>>>>>>>>>>>", alias_ping, " ", sv.label
        table = sv.mipTable
        if table not in skipped_vars_per_table: skipped_vars_per_table[table] = []
        skipped_vars_per_table[table].append(sv.label + "(" + str(sv.Priority) + ")")
        return
    #
    # --------------------------------------------------------------------
    # Set global CMOR file attributes
    # --------------------------------------------------------------------
    #
    project = get_variable_from_sset_with_default('project', "CMIP6")
    source_id, source_type = get_source_id_and_type()
    experiment_id = get_variable_from_sset_without_default('experiment_id')
    institution_id = get_variable_from_lset_without_default('institution_id')
    #
    contact = get_variable_from_sset_else_lset_with_default('contact', default=None)
    #
    # Variant matters
    realization_index = get_variable_from_sset_with_default('realization_index', 1)
    initialization_index = get_variable_from_sset_with_default('initialization_index', 1)
    physics_index = get_variable_from_sset_with_default('physics_index', 1)
    forcing_index = get_variable_from_sset_with_default('forcing_index', 1)
    variant_label = "r%di%dp%df%d" % (realization_index, initialization_index, \
                                      physics_index, forcing_index)
    variant_info_warning = ". Information provided by this attribute may in some cases be flawed. " + \
                           "Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute."
    #
    # WIP Draft 14 july 2016
    mip_era = get_variable_from_lset_with_default(sv.mip_era)
    #
    # WIP doc v 6.2.0 - dec 2016
    # <variable_id>_<table_id>_<source_id>_<experiment_id >_<member_id>_<grid_label>[_<time_range>].nc
    member_id = variant_label
    sub_experiment_id = get_variable_from_sset_with_default('sub_experiment_id', 'none')
    if sub_experiment_id != 'none':
        member_id = sub_experiment_id + "-" + member_id
    #
    # --------------------------------------------------------------------
    # Set grid info
    # --------------------------------------------------------------------
    if grid == "":
        # either native or close-to-native
        grid_choice = get_variable_from_lset_without_default('grid_choice', source_id)
        grid_label, target_hgrid_id, zgrid_id, grid_resolution, grid_description = \
            get_variable_from_lset_without_default('grids', grid_choice, context)
    else:
        if grid == 'cfsites':
            target_hgrid_id = cfsites_domain_id
            zgrid_id = None
        else:
            target_hgrid_id = get_variable_from_lset_without_default("ping_variables_prefix") + grid
            zgrid_id = "TBD : Should create zonal grid for CMIP6 standard grid %s" % grid
        grid_label, grid_resolution, grid_description = DRgrid2gridatts(grid)

    if table[-1:] == "Z":  # e.g. 'AERmonZ','EmonZ', 'EdayZ'
        grid_label += "z"
        # Below : when reduction was done trough a two steps sum, we needed to divide afterwards
        # by the nmber of longitudes
        #
        # if is_key_in_lset("nb_longitudes_in_model") and get_variable_from_lset_without_default("nb_longitudes_in_model", context):
        #     # Get from settings the name of Xios variable holding number of longitudes and set by model
        #     nlonz=get_variable_from_lset_without_default("nb_longitudes_in_model", context) # e.g.: nlonz="ndlon"
        # elif context_index.has_key(target_hgrid_id):
        #     # Get the number of longitudes from xml context_index
        #     # an integer if attribute of the target horizontal grid, declared in XMLs: nlonz=256
        #     nlonz=context_index[target_hgrid_id].attrib['ni_glo']
        # else:
        #     raise dr2xml_error("Fatal: Cannot access the number of longitudes (ni_glo) for %s\
        #                 grid required for zonal means computation "%target_hgrid_id)
        # print ">>> DBG >>> nlonz=", nlonz

    if "Ant" in table:
        grid_label += "a"
    if "Gre" in table:
        grid_label += "g"
    #
    with open(cvspath + project + "_experiment_id.json", "r") as json_fp:
        CMIP6_CV_version_metadata = json.loads(json_fp.read())['version_metadata']
        CMIP6_CV_latest_tag = CMIP6_CV_version_metadata.get('latest_tag_point', 'no more value in CMIP6_CV')
    #
    with open(cvspath + project + "_experiment_id.json", "r") as json_fp:
        CMIP6_experiments = json.loads(json_fp.read())['experiment_id']
        if not CMIP6_experiments.has_key(get_variable_from_sset_without_default('experiment_id')):
            raise dr2xml_error("Issue getting experiment description in CMIP6 CV for %20s" % sset['experiment_id'])
        expid = get_variable_from_sset_without_default('experiment_id')
        expid_in_filename = get_variable_from_sset_with_default('expid_in_filename', expid)
        if "_" in expid_in_filename:
            raise dr2xml_error("Cannot use character '_' in expid_in_filename (%s)" % expid_in_filename)
        exp_entry = CMIP6_experiments[expid]
        experiment = exp_entry['experiment']
        description = exp_entry['description']
        activity_id = get_variable_from_lset_with_default('activity_id', exp_entry['activity_id'])
        parent_activity_id = get_variable_from_lset_with_default('parent_activity_id', lset.get('activity_id', exp_entry['parent_activity_id']))
        if type(parent_activity_id) == type([]):
            parent_activity_id = reduce(lambda x, y: x+" "+y, parent_activity_id)
        if is_key_in_sset('parent_experiment_id'):
            parent_experiment_id = get_variable_from_sset_with_default('parent_experiment_id')
        else:
            parent_experiment_id = reduce(lambda x, y: x+" "+y, exp_entry['parent_experiment_id'])
        required_components = exp_entry['required_model_components']  # .split(" ")
        allowed_components = exp_entry['additional_allowed_model_components']  # .split(" ")
    #
    # Check model components re. CV components
    actual_components = source_type.split(" ")
    ok = True
    for c in required_components:
        if c not in actual_components:
            ok = False
            print "Model component %s is required by CMIP6 CV for experiment %s and not present (present=%s)" % \
                  (c, experiment_id, `actual_components`)
    for c in actual_components:
        if c not in allowed_components and c not in required_components:
            ok = False or get_variable_from_sset_with_default('bypass_CV_components', False)
            print "Warning: Model component %s is present but not required nor allowed (%s)" % \
                  (c, `allowed_components`)
    if not ok: raise dr2xml_error("Issue with model components")
    #
    # --------------------------------------------------------------------
    # Set NetCDF output file name according to the DRS
    # --------------------------------------------------------------------
    #
    date_range = "%start_date%-%end_date%"  # XIOS syntax
    operation, detect_missing, foo = analyze_cell_time_method(sv.cell_methods, sv.label, table, printout=False)
    # print "--> ",sv.label, sv.frequency, table
    date_format, offset_begin, offset_end = freq2datefmt(sv.frequency, operation, table)
    #
    if "fx" in sv.frequency:
        filename = "%s%s_%s_%s_%s_%s_%s" % \
                   (prefix, sv.label, table, source_id, expid_in_filename, member_id, grid_label)
    else:
        varname_for_filename = sv.mipVarLabel
        if get_variable_from_lset_with_default('use_cmorvar_label_in_filename', False):
            varname_for_filename = sv.label
        # DR21 has a bug with tsland : the MIP variable is named "ts"
        if sv.label == "tsland":
            varname_for_filename = "tsland"
        # WIP doc v6.2.3 : a suffix "-clim" should be added if climatology
        # if False and "Clim" in sv.frequency: suffix="-clim"
        if sv.frequency in ["1hrCM", "monC"]:
            suffix = "-clim"
        else:
            suffix = ""
        filename = "%s%s_%s_%s_%s_%s_%s_%s%s" % \
                   (prefix, varname_for_filename, table, source_id, expid_in_filename,
                    member_id, grid_label, date_range, suffix)
    #
    if is_key_in_lset('mip_era'):
        further_info_url = "https://furtherinfo.es-doc.org/%s.%s.%s.%s.%s.%s" % (
            mip_era, institution_id, source_id, expid_in_filename,
            sub_experiment_id, variant_label)
    else:
        further_info_url = ""
    #
    # --------------------------------------------------------------------
    # Compute XIOS split frequency
    # --------------------------------------------------------------------
    sc = get_sc()
    resolution = get_variable_from_lset_without_default('grid_choice', source_id)
    split_freq = split_frequency_for_variable(sv, resolution, sc.mcfg, context)
    # Cap split_freq by setting max_split_freq (if expressed in years)
    if split_freq[-1] == 'y':
        max_split_freq = get_variable_from_sset_with_default('max_split_freq', None)
        if max_split_freq is None:
            max_split_freq = get_variable_from_lset_with_default('max_split_freq', None)
        if max_split_freq is not None:
            if max_split_freq[0:-1] != "y":
                dr2xml_error("max_split_freq must end with an 'y' (%s)" % max_split_freq)
            split_freq = "%dy" % min(int(max_split_freq[0:-1]), int(split_freq[0:-1]))
    # print "split_freq: %-25s %-10s %-8s"%(sv.label,sv.mipTable,split_freq)
    #
    # --------------------------------------------------------------------
    # Write XIOS file node:
    # including global CMOR file attributes
    # --------------------------------------------------------------------
    out.write(' <file id="%s_%s_%s" name="%s" ' % (sv.label, table, grid_label, filename))
    freq = longest_possible_period(Cmip6Freq2XiosFreq(sv.frequency, table), get_variable_from_lset_with_default("too_long_periods", []))
    out.write(' output_freq="%s" ' % freq)
    out.write(' append="true" ')
    out.write(' output_level="%d" ' % get_variable_from_lset_with_default("output_level", 10))
    out.write(' compression_level="%d" ' % get_variable_from_lset_with_default("compression_level", 0))
    if not "fx" in sv.frequency:
        out.write(' split_freq="%s" ' % split_freq)
        out.write(' split_freq_format="%s" ' % date_format)
        #
        # Modifiers for date parts of the filename, due to silly KT conventions.
        if offset_begin is not False:
            out.write(' split_start_offset="%s" ' % offset_begin)
        if offset_end is not False:
            out.write(' split_end_offset="%s" ' % offset_end)
        lastyear = None
        # Try to get enddate for the CMOR variable from the DR
        if sv.cmvar is not None:
            # print "calling endyear_for... for %s, with year="%(sv.label), year
            lastyear = endyear_for_CMORvar(sv.cmvar, expid, year, sv.label in debug)
            # print "lastyear=",lastyear," enddate=",enddate
        if lastyear is None or (enddate is not None and lastyear >= int(enddate[0:4])):
            # DR doesn't specify an end date for that var, or a very late one
            if get_variable_from_lset_with_default('dr2xml_manages_enddate', True):
                # Use run end date as the latest possible date
                # enddate must be 20140101 , rather than 20131231
                if enddate is not None:
                    endyear = enddate[0:4]
                    endmonth = enddate[4:6]
                    endday = enddate[6:8]
                    out.write(' split_last_date="%s-%s-%s 00:00:00" ' % (endyear, endmonth, endday))
                else:
                    out.write(' split_last_date=10000-01-01 00:00:00" ')
        else:
            # Use requestItems-based end date as the latest possible date when it is earlier than run end date
            if (sv.label in debug):
                print "split_last_date year %d derived from DR for variable %s in table %s for year %d" % (
                lastyear, sv.label, table, year)
            endyear = "%04d" % (lastyear + 1)
            if lastyear < 1000:
                dr2xml_error(
                    "split_last_date year %d derived from DR for variable %s in table %s for year %d does not make sense except maybe for paleo runs; please set the right value for 'end_year' in experiment's settings file" % (
                    lastyear, sv.label, table, year))
            endmonth = "01"
            endday = "01"
            out.write(' split_last_date="%s-%s-%s 00:00:00" ' % (endyear, endmonth, endday))
    #
    # out.write('timeseries="exclusive" >\n')
    out.write(' time_units="days" time_counter_name="time"')
    out.write(' time_counter="exclusive"')
    out.write(' time_stamp_name="creation_date" ')
    out.write(' time_stamp_format="%Y-%m-%dT%H:%M:%SZ"')
    out.write(' uuid_name="tracking_id" uuid_format="hdl:21.14100/%uuid%"')
    out.write(' convention_str="%s"' % conventions)
    # out.write(' description="A %s result for experiment %s of %s"'%
    #            (lset['source_id'],sset['experiment_id'],sset.get('project',"CMIP6")))
    out.write(' >\n')
    #
    if type(activity_id) == type([]):
        activity_idr = reduce(lambda x, y: x + " " + y, activity_id)
    else:
        activity_idr = activity_id
    wr(out, 'activity_id', activity_idr)
    #
    if contact and contact is not "": wr(out, 'contact', contact)
    wr(out, 'data_specs_version', get_DR_version())
    wr(out, 'dr2xml_version', version)
    #
    wr(out, 'experiment_id', expid_in_filename)
    if experiment_id == expid_in_filename:
        wr(out, 'description', description)
        wr(out, 'title', description)
        wr(out, 'experiment', experiment)
    #
    # Fixing cell_measures is done in vars.py
    #
    dynamic_comment = ""
    if "seaIce" in sv.modeling_realm and 'areacella' in sv.cell_measures and sv.label != "siconca":
        dynamic_comment = '. Due an error in DR01.00.21 and to technical constraints, this variable may have  attribute cell_measures set to area: areacella, while it actually is area: areacello'

    #
    # When remapping occurs to a regular grid -> CF does not ask for cell_measure
    # but CMIP6 do ask for it !
    # if grid_label[0:2]=='gr': sv.cell_measures=""
    # TBD : find a way to provide an areacella field for variables which are remapped to a 'CMIP6' grid such as '1deg'

    #
    # CF rule : if the file variable has a cell_measures attribute, and
    # the corresponding 'measure' variable is not included in the file,
    # it must be quoted as external_variable
    external_variables = ''
    if "area:" in sv.cell_measures:
        external_variables += " " + re.sub(".*area: ([^ ]*).*", r'\1', sv.cell_measures)
    if "volume:" in sv.cell_measures:
        external_variables += " " + re.sub(".*volume: ([^ ]*).*", r'\1', sv.cell_measures)
    if 'fx' in table:
        external_variables = ""
    if external_variables:
        wr(out, 'external_variables', external_variables)
    #
    #
    wr(out, 'forcing_index', forcing_index, num_type="int")
    wr(out, 'frequency', sv.frequency)
    #
    if further_info_url:
        wr(out, 'further_info_url', further_info_url)
    #
    wr(out, 'grid', grid_description);
    wr(out, 'grid_label', grid_label);
    wr(out, 'nominal_resolution', grid_resolution)
    comment = get_variable_from_lset_with_default('comment', '') + " " + get_variable_from_sset_with_default('comment', '') + dynamic_comment
    wr(out, 'comment', comment)
    wr(out, 'history', sset, default='none')
    wr(out, "initialization_index", initialization_index, num_type="int")
    wr(out, "institution_id", institution_id)
    if is_key_in_lset('institution'):
        inst = get_variable_from_lset_without_default('institution')
    else:
        with open(cvspath + project + "_institution_id.json", "r") as json_fp:
            try:
                inst = json.loads(json_fp.read())['institution_id'][institution_id]
            except:
                raise dr2xml_error("Fatal: Institution_id for %s not found " + \
                                   "in CMIP6_CV at %s" % (institution, cvspath))
    wr(out, "institution", inst)
    #
    with open(cvspath + project + "_license.json", "r") as json_fp:
        license = json.loads(json_fp.read())['license'][0]
    # mpmoine_cmor_update: 'licence' est trop long... passe pas le CMIP6-Checker => 'institution_id' au lieu de inst='institution'
    license = license.replace("<Your Centre Name>", institution_id)
    license = license.replace("[NonCommercial-]", "NonCommercial-")
    license = license.replace("[ and at <some URL maintained by modeling group>]",
                              " and at " + get_variable_from_lset_without_default("info_url"))
    wr(out, "license", license)
    wr(out, 'mip_era', mip_era)
    #
    if parent_experiment_id and parent_experiment_id != 'no parent' and parent_experiment_id != ['no parent']:
        wr(out, 'parent_experiment_id', parent_experiment_id)
        wr(out, 'parent_mip_era', sset, default=mip_era)
        wr(out, 'parent_activity_id', parent_activity_id)
        wr(out, 'parent_source_id', sset, default=source_id)
        # TBD : syntaxe XIOS pour designer le time units de la simu courante
        parent_time_ref_year = get_variable_from_sset_with_default('parent_time_ref_year', "1850")
        parent_time_units = "days since %s-01-01 00:00:00" % parent_time_ref_year
        wr(out, 'parent_time_units', sset, default=parent_time_units)
        wr(out, 'parent_variant_label', sset, default=variant_label)
        wr(out, 'branch_method', sset, default='standard')
        # Use branch year in parent if available
        if is_key_in_sset("branch_year_in_parent") and source_id in get_variable_from_lset_without_default('branching'):
            if experiment_id in get_variable_from_lset_without_default('branching', source_id) and \
                    get_variable_from_sset_without_default("branch_year_in_parent") not in get_variable_from_lset_without_default('branching', source_id, experiment_id, 1):
                dr2xml_error(
                    "branch_year_in_parent (%d) doesn't belong to the list of branch_years declared for this experiment %s" \
                    % (get_variable_from_sset_without_default("branch_year_in_parent"), get_variable_from_lset_without_default('branching', source_id, experiment_id, 1)))
            date_branch = datetime.datetime(get_variable_from_sset_without_default("branch_year_in_parent"), get_variable_from_sset_with_default("branch_month_in_parent", 1), 1)
            date_ref = datetime.datetime(int(parent_time_ref_year), 1, 1)
            nb_days = (date_branch - date_ref).days
            wr(out, 'branch_time_in_parent', "%d.0D" % nb_days, "double")
        else:
            wr(out, 'branch_time_in_parent', sset, "double")
        # Use branch year in child if available
        if is_key_in_sset("branch_year_in_parent"):
            date_branch = datetime.datetime(get_variable_from_sset_without_default("branch_year_in_child"), 1, 1)
            date_ref = datetime.datetime(get_variable_from_sset_without_default("child_time_ref_year"), 1, 1)
            nb_days = (date_branch - date_ref).days
            wr(out, 'branch_time_in_child', "%d.0D" % nb_days, "double")
        else:
            wr(out, 'branch_time_in_child', sset, "double")
    #
    wr(out, "physics_index", physics_index, num_type="int")
    wr(out, 'product', 'model-output')
    wr(out, "realization_index", realization_index, num_type="int")
    # Patch for an issue id DR01.0021 -> 01.00.24
    crealm = sv.modeling_realm
    if crealm == "ocnBgChem":
        crealm = "ocnBgchem"
    wr(out, 'realm', crealm)
    wr(out, 'references', lset, default=False)
    #
    try:
        with open(cvspath + project + "_source_id.json", "r") as json_fp:
            sources = json.loads(json_fp.read())['source_id']
            source = make_source_string(sources, source_id)
    except:
        if is_key_in_lset('source'):
            source = get_variable_from_lset_without_default('source')
        else:
            raise dr2xml_error("Fatal: source for %s not found in CMIP6_CV at" + \
                               "%s, nor in lset" % (source_id, cvspath))
    wr(out, 'source', source)
    wr(out, 'source_id', source_id)
    if type(source_type) == type([]):
        source_type = reduce(lambda x, y: x + " " + y, source_type)
    wr(out, 'source_type', source_type)
    #
    wr(out, 'sub_experiment_id', sub_experiment_id)
    wr(out, 'sub_experiment', sset, default='none')
    #
    wr(out, "table_id", table)
    #
    if not is_key_in_sset('expid_in_filename'):
        wr(out, "title", "%s model output prepared for %s / " % ( \
            source_id, project) + activity_idr + " " + experiment_id)
    else:
        wr(out, "title", "%s model output prepared for %s and " % ( \
            source_id, project) + activity_idr + " / " + expid_in_filename + " simulation")
    #
    # DR21 has a bug with tsland : the MIP variable is named "ts"
    if sv.label != "tsland":
        wr(out, "variable_id", sv.mipVarLabel)
    else:
        wr(out, "variable_id", "tsland")
    #
    variant_info = get_variable_from_sset_with_default('variant_info', "none")
    if variant_info != "none" and variant_info != "": variant_info += variant_info_warning
    if variant_info != "": wr(out, "variant_info", variant_info)
    wr(out, "variant_label", variant_label)
    for name, value in attributes: wr(out, name, value)
    non_stand_att = get_variable_from_lset_with_default("non_standard_attributes", dict())
    for name in non_stand_att: wr(out, name, non_stand_att[name])
    #
    # --------------------------------------------------------------------
    # Build all XIOS auxilliary elements (end_file_defs, field_defs, domain_defs, grid_defs, axis_defs)
    # ---
    # Write XIOS field entry
    # including CF field attributes
    # --------------------------------------------------------------------
    end_field = create_xios_aux_elmts_defs(sv, alias, table, field_defs, axis_defs, grid_defs, domain_defs, scalar_defs,
                                           dummies, context, target_hgrid_id, zgrid_id, pingvars)
    out.write(end_field)
    if sv.spatial_shp[0:4] == 'XY-A' or sv.spatial_shp[0:3] == 'S-A':  # includes half-level cases
        # create a field_def entry for surface pressure
        # print "Searching for ps for var %s, freq %s="%(alias,freq)
        sv_psol = get_simplevar("ps", table, sv.frequency)

        if sv_psol:
            # if not sv_psol.cell_measures : sv_psol.cell_measures = "cell measure is not specified in DR "+get_DR_version()
            psol_field = create_xios_aux_elmts_defs(sv_psol, get_variable_from_lset_without_default("ping_variables_prefix") + "ps", table, field_defs,
                                                    axis_defs, grid_defs, domain_defs, scalar_defs, dummies, context,
                                                    target_hgrid_id, zgrid_id, pingvars)
            out.write(psol_field)
        else:
            print "Warning: Cannot complement model levels with psol for variable %s and table %s" % \
                  (sv.label, sv.frequency)

    #
    names = {}
    if sv.spatial_shp == 'XY-A' or sv.spatial_shp == 'S-A':
        # add entries for auxilliary variables : ap, ap_bnds, b, b_bnds
        names = {"ap": "vertical coordinate formula term: ap(k)",
                 "ap_bnds": "vertical coordinate formula term: ap(k+1/2)",
                 "b": "vertical coordinate formula term: b(k)",
                 "b_bnds": "vertical coordinate formula term: b(k+1/2)"}
    if sv.spatial_shp == 'XY-AH' or sv.spatial_shp == 'S-AH':
        # add entries for auxilliary variables : ap, ap_bnds, b, b_bnds
        names = {"ahp": "vertical coordinate formula term: ap(k)",
                 "ahp_bnds": "vertical coordinate formula term: ap(k+1/2)",
                 "bh": "vertical coordinate formula term: b(k)",
                 "bh_bnds": "vertical coordinate formula term: b(k+1/2)"}
    for tab in names:
        out.write('\t<field field_ref="%s%s" name="%s" long_name="%s" operation="once" prec="8" />\n' % \
                  (get_variable_from_lset_without_default("ping_variables_prefix"), tab, tab.replace('h', ''), names[tab]))
    out.write('</file>\n\n')
    actually_written_vars.append((sv.label, sv.long_name, sv.mipTable, sv.frequency, sv.Priority, sv.spatial_shp))


def wrv(name, value, num_type="string"):
    global print_wrv
    if not print_wrv: return ""
    if type(value) == type(""): value = value[0:1024]  # CMIP6 spec : no more than 1024 char
    # Format a 'variable' entry
    return '     <variable name="%s" type="%s" > %s ' % (name, num_type, value) + \
           '</variable>\n'


def create_xios_aux_elmts_defs(sv, alias, table, field_defs, axis_defs, grid_defs, domain_defs, scalar_defs, dummies,
                               context, target_hgrid_id, zgrid_id, pingvars):
    """
    Create a field_ref string for a simplified variable object sv (with
    lab prefix for the variable name) and returns it

    Add field definitions for intermediate variables in dict field_defs
    Add axis  definitions for interpolations in dict axis_defs
    Use pingvars as the list of variables actually defined in ping file

    """
    # By convention, field references are built as prefix_<MIP_variable_name>
    # Such references must be fulfilled using a dedicated field_def
    # section implementing the match between legacy model field names
    # and such names, called 'ping section'
    #
    # Identify which 'ping' variable ultimatley matches the requested
    # CMOR variable, based on shapes. This may involve building
    # intermediate variables, in order to  apply corresponding operations

    # The preferred order of operation is : vertical interp (which
    # is time-dependant), time-averaging, horizontal operations (using
    # expr=@this)
    #
    # --------------------------------------------------------------------
    # Build XIOS axis elements (stored in axis_defs)
    # Proceed with vertical interpolation if needed
    # ---
    # Build XIOS auxilliary field elements (stored in field_defs)
    # --------------------------------------------------------------------
    ssh = sv.spatial_shp
    prefix = get_variable_from_lset_without_default("ping_variables_prefix")

    # The id of the currently most downstream field is last_field_id
    last_field_id = alias

    alias_ping = ping_alias(sv, pingvars)
    context_index = get_config_variable("context_index")
    grid_id_in_ping = id2gridid(alias_ping, context_index)
    last_grid_id = grid_id_in_ping
    # last_grid_id=None
    #
    grid_with_vertical_interpolation = None

    # translate 'outermost' time cell_methods to Xios 'operation')
    operation, detect_missing, clim = analyze_cell_time_method(sv.cell_methods, sv.label, table, printout=False)
    #
    # --------------------------------------------------------------------
    # Handle vertical interpolation, both XY-any and Y-P outputs
    # --------------------------------------------------------------------
    #
    # if ssh[0:4] in ['XY-H','XY-P'] or ssh[0:3] == 'Y-P' or \
    # must exclude COSP outputs which are already interpolated to height or P7 levels
    if (ssh[0:4] == 'XY-P' and ssh != 'XY-P7') or \
            ssh[0:3] == 'Y-P' or \
            ((ssh[0:5] == 'XY-na' or ssh[0:4] == 'Y-na') and
             prefix + sv.label not in pingvars and sv.label_without_psuffix != sv.label):  # TBD check - last case is for singleton
        last_grid_id, last_field_id = process_vertical_interpolation(sv, alias, pingvars, last_grid_id, field_defs,
                                                                     axis_defs, grid_defs, domain_defs, table)

    #
    # --------------------------------------------------------------------
    # Handle the case of singleton dimensions
    # --------------------------------------------------------------------
    #
    if has_singleton(sv):
        last_field_id, last_grid_id = process_singleton(sv, last_field_id, pingvars, field_defs, grid_defs, scalar_defs,
                                                        table)
    #
    # TBD : handle explicitly the case of scalars (global means, shape na-na) : enforce <scalar name="sector" standard_name="region" label="global" >, or , better, remove the XIOS-generated scalar introduced by reduce_domain
    #
    # --------------------------------------------------------------------
    # Handle zonal means
    # --------------------------------------------------------------------
    #
    if ssh[0:2] == 'Y-':  # zonal mean and atm zonal mean on pressure levels
        last_field_id, last_grid_id = \
            process_zonal_mean(last_field_id, last_grid_id, target_hgrid_id, zgrid_id, field_defs, axis_defs, grid_defs,
                               domain_defs, operation, sv.frequency)

    #
    # --------------------------------------------------------------------
    # Build a construct for computing a climatology (if applicable)
    # --------------------------------------------------------------------
    if clim:
        if sv.frequency == "1hrCM":
            last_field_id, last_grid_id = process_diurnal_cycle(last_field_id, \
                                                                field_defs, grid_defs, axis_defs)
        else:
            raise dr2xml_error("Cannot handle climatology cell_method for frequency %s and variable " % \
                               sv.frequency, sv.label)
    #
    # --------------------------------------------------------------------
    # Create intermediate field_def for enforcing operation upstream
    # --------------------------------------------------------------------
    #
    but_last_field_id = last_field_id
    last_field_id = last_field_id + "_" + operation
    field_defs[last_field_id] = '<field id="%-25s field_ref="%-25s operation="%-10s/>' \
                                % (last_field_id + '"', but_last_field_id + '"', operation + '"')
    #
    # --------------------------------------------------------------------
    # Change horizontal grid if requested
    # --------------------------------------------------------------------
    #
    if target_hgrid_id:
        # This does not apply for a series of shapes
        if ssh[0:2] == 'Y-' or ssh == 'na-na' or ssh == 'TR-na' or ssh == 'TRS-na' or ssh[
                                                                                      0:3] == 'YB-' or ssh == 'na-A':
            pass
        else:
            if target_hgrid_id == cfsites_domain_id:
                add_cfsites_in_defs(grid_defs, domain_defs)
            # Apply DR required remapping, either toward cfsites grid or a regular grid
            last_grid_id = change_domain_in_grid(target_hgrid_id, grid_defs, src_grid_id=last_grid_id)
    #
    # --------------------------------------------------------------------
    # Change axes in grid to CMIP6-compliant ones
    # --------------------------------------------------------------------
    #
    last_grid_id = change_axes_in_grid(last_grid_id, grid_defs, axis_defs)
    #
    # --------------------------------------------------------------------
    # Create <field> construct to be inserted in a file_def, which includes re-griding
    # --------------------------------------------------------------------
    #
    if last_grid_id != grid_id_in_ping:
        gref = 'grid_ref="%s"' % last_grid_id
    else:
        gref = ""

    rep = '  <field field_ref="%s" name="%s" %s ' % (last_field_id, sv.mipVarLabel, gref)
    #
    #
    # --------------------------------------------------------------------
    # Add offset if operation=instant for some specific variables defined in lab_settings
    # --------------------------------------------------------------------
    #
    if operation == 'instant':
        for ts in get_variable_from_lset_with_default('special_timestep_vars', []):
            if sv.label in get_variable_from_lset_without_default('special_timestep_vars', ts):
                xios_freq = Cmip6Freq2XiosFreq(sv.frequency, table)
                # works only if units are different :
                rep += ' freq_offset="%s-%s"' % (xios_freq, ts)
    #
    # --------------------------------------------------------------------
    # handle data type and missing value
    # --------------------------------------------------------------------
    #
    detect_missing = "True"
    missing_value = "1.e+20"
    if sv.prec.strip() in ["float", "real", ""]:
        prec = "4"
    elif sv.prec.strip() == "double":
        prec = "8"
    elif sv.prec.strip() == "integer" or sv.prec.strip() == "int":
        prec = "2";
        missing_value = "0"  # 16384"
    else:
        raise dr2xml_error("prec=%s for sv=%s" % (sv.prec, sv.label))
    rep += ' detect_missing_value="%s" \n\tdefault_value="%s" prec="%s"' % (detect_missing, missing_value, prec)
    #
    # TBD : implement DR recommendation for cell_method : The syntax is to append, in brackets,
    # TBD    'interval: *amount* *units*', for example 'area: time: mean (interval: 1 hr)'.
    # TBD    The units must be valid UDUNITS, e.g. day or hr.
    rep += ' cell_methods="%s" cell_methods_mode="overwrite"' % sv.cell_methods
    # --------------------------------------------------------------------
    # enforce time average before remapping (when there is one) except if there
    # is an expr, set in ping for the ping variable of that field, and which
    # involves time operation (using @)
    # --------------------------------------------------------------------
    if operation == 'once':
        freq_op = ""
    else:
        freq_op = 'freq_op="%s"' % \
                  longest_possible_period(Cmip6Freq2XiosFreq(sv.frequency, table),
                                          get_variable_from_lset_with_default("too_long_periods", []))
    #
    rep += ' operation="%s"' % operation
    if not idHasExprWithAt(alias, context_index):
        # either no expr, or expr without an @  ->
        # may use @ for optimizing operations order (average before re-gridding)
        if last_grid_id != grid_id_in_ping:
            if operation == 'average':
                # do use @ for optimizing :
                rep += ' %s>\n\t\t@%s' % (freq_op, last_field_id)
            elif operation == 'instant':
                # must set freq_op (this souldn't be necessary, but is needed with Xios 1442)
                if get_variable_from_lset_with_default("useAtForInstant", False):
                    rep += ' %s>\n\t\t@%s' % (freq_op, last_field_id)
                else:
                    rep += ' %s>' % (freq_op)
            else:
                # covers only case once , already addressed by freq_op value='' ?
                rep += ' >'
        else:
            # No remap
            rep += ' >'
    else:  # field has an expr, with an @
        # Cannot optimize
        if operation == 'instant':
            # must reset expr (if any) if instant, for using arithm. operation defined in ping.
            # this allows that the type of operation applied is really 'instant', and not the one
            # that operands did inherit from ping_file
            rep += ' expr="_reset_"'
        if (operation == 'average'):
            warnings_for_optimisation.append(alias)
        rep += ' %s>' % (freq_op)
    rep += '\n'
    #
    # --------------------------------------------------------------------
    # Add Xios variables for creating NetCDF attributes matching CMIP6 specs
    # --------------------------------------------------------------------
    comment = None
    # Process experiment-specific comment for the variable
    if sv.label in get_variable_from_sset_without_default('comments').keys():
        comment = get_variable_from_sset_without_default('comments', sv.label)
    else:  # Process lab-specific comment for the variable
        if sv.label in get_variable_from_lset_without_default('comments').keys():
            comment = get_variable_from_lset_without_default('comments', sv.label)
    if comment:
        rep += wrv('comment', comment)  # TBI
    #
    if sv.stdname:
        rep += wrv("standard_name", sv.stdname)
    #
    desc = sv.description
    # if desc : desc=desc.replace(">","&gt;").replace("<","&lt;").replace("&","&amp;").replace("'","&apos;").replace('"',"&quot;")
    if desc:
        desc = desc.replace(">", "&gt;").replace("<", "&lt;").strip()
    rep += wrv("description", desc)
    #
    rep += wrv("long_name", sv.long_name)
    if sv.positive != "None" and sv.positive != "":
        rep += wrv("positive", sv.positive)
    rep += wrv('history', 'none')
    if sv.units:
        rep += wrv('units', sv.units)
    if sv.cell_methods:
        rep += wrv('cell_methods', sv.cell_methods)
    if sv.cell_measures:
        rep += wrv('cell_measures', sv.cell_measures)
    #
    if sv.struct is not None:
        fmeanings = sv.struct.flag_meanings
        if fmeanings is not None and fmeanings.strip() != '':
            rep += wrv('flag_meanings', fmeanings.strip())
        fvalues = sv.struct.flag_values
        if fvalues is not None and fvalues.strip() != '':
            rep += wrv('flag_values', fvalues.strip())
    #
    # We override the Xios value for interval_operation because it sets it to
    # the freq_output value with our settings (for complicated reasons)
    if grid_with_vertical_interpolation:
        interval_op = get_variable_from_lset_without_default("vertical_interpolation_sample_freq")
    else:
        source, source_type = get_source_id_and_type()
        grid_choice = get_variable_from_lset_without_default("grid_choice", source)
        interval_op = `int(get_variable_from_lset_without_default('sampling_timestep', grid_choice, context))` + " s"
    if operation != 'once':
        rep += wrv('interval_operation', interval_op)

    # mpmoine_note: 'missing_value(s)' normalement plus necessaire, a verifier
    # TBS# rep+=wrv('missing_values',sv.missing,num_type="double")
    rep += '     </field>\n'
    #
    return rep


def is_singleton(sdim):
    if sdim.axis == '':
        # Case of non-spatial dims. Singleton only have a 'value' (except Scatratio has a lot (in DR01.00.21))
        return sdim.value != '' and len(sdim.value.strip().split(" ")) == 1
    else:
        # Case of space dimension singletons. Should a 'value' and no 'requested'
        return ((sdim.value != '') and (sdim.requested.strip() == '')) \
               or (sdim.label == "typewetla")  # The latter is a bug in DR01.00.21 : typewetla has no value tehre


def has_singleton(sv):
    rep = any([is_singleton(sv.sdims[k]) for k in sv.sdims])
    return rep


def process_singleton(sv, alias, pingvars, field_defs, grid_defs, scalar_defs, table):
    """
    Based on singleton dimensions of variable SV, and assuming that this/these dimension(s)
    is/are not yet represented by a scalar Xios construct in corresponding field's grid,
    creates a further field with such a grid, including creating the scalar and
    re-using the domain of original grid

    """

    printout = False
    # get grid for the variable , before vertical interpo. if any
    # (could rather use last_grid_id and analyze if it has pressure dim)
    alias_ping = ping_alias(sv, pingvars)
    context_index = get_config_variable("context_index")
    input_grid_id = id2gridid(alias_ping, context_index)
    input_grid_def = get_grid_def_with_lset(input_grid_id, grid_defs)
    if printout:
        print "process_singleton : ", "processing %s with grid %s " % (alias, input_grid_id)
    #
    further_field_id = alias
    further_grid_id = input_grid_id
    further_grid_def = input_grid_def
    #
    # for each sv's singleton dimension, create the scalar, add a scalar
    # construct in a further grid, and convert field to a further field
    for dimk in sv.sdims:
        sdim = sv.sdims[dimk]
        if is_singleton(sdim):  # Only one dim should match
            #
            # Create a scalar for singleton dimension
            # sdim.label is non-ambiguous id, thanks to the DR, but its value may be
            # ambiguous w.r.t. a dr2xml suffix for interpolating to a single pressure level
            scalar_id = "Scal" + sdim.label
            if sdim.units == '':
                unit = ''
            else:
                unit = ' unit="%s"' % sdim.units
            #
            if sdim.type == 'character':
                value = ' label="%s"' % sdim.label
            else:
                value = ' value="%s"' % sdim.value
                types = {'double': ' prec="8"', 'float': ' prec="4"', 'integer': ' prec="2"'}
                value = types[sdim.type] + " " + 'value="%s"' % sdim.value
            if sdim.axis != '':
                # Space axis, probably Z
                axis = ' axis_type="%s"' % (sdim.axis)
                if sdim.positive: axis += ' positive="%s"' % (sdim.positive)
            else:
                axis = ""
            if sdim.bounds == "yes":
                try:
                    bounds = sdim.boundsValues.split()
                    bounds_value = ' bounds="(0,1)[ %s %s ]" bounds_name="%s_bounds"' % \
                                   (bounds[0], bounds[1], sdim.out_name)
                except:
                    if sdim.label == "lambda550nm":
                        bounds_value = ''
                    else:
                        raise dr2xml_error("Issue for var %s with dim %s bounds=%s" % (sv.label, sdim.label, bounds))
            else:
                bounds_value = ""
            #
            name = sdim.out_name
            # These dimensions are shared by some variables with another sdim with same out_name ('type'):
            if sdim.label in ["typec3pft", "typec4pft"]: name = "pfttype"
            #
            if sdim.stdname.strip() == '' or sdim.label == "typewetla":
                stdname = ""
            else:
                stdname = 'standard_name="%s"' % sdim.stdname
            #
            scalar_def = '<scalar id="%s" name="%s" %s long_name="%s"%s%s%s%s />' % \
                         (scalar_id, name, stdname, sdim.title, value, bounds_value, axis, unit)
            scalar_defs[scalar_id] = scalar_def
            if printout:
                print "process_singleton : ", "adding scalar %s" % scalar_def
            #
            # Create a grid with added (or changed) scalar
            glabel = further_grid_id + "_" + scalar_id
            further_grid_def = add_scalar_in_grid(further_grid_def, glabel, scalar_id, \
                                                  name, sdim.axis == "Z")
            if printout:
                print "process_singleton : ", " adding grid %s" % further_grid_def
            grid_defs[glabel] = further_grid_def
            further_grid_id = glabel

    # Compare grid definition (in case the input_grid already had correct ref to scalars)
    if further_grid_def != input_grid_def:
        #  create derived_field through an Xios operation (apply all scalars at once)
        further_field_id = alias + "_" + further_grid_id.replace(input_grid_id + '_', '')
        # Must init operation and detect_missing when there is no field ref
        field_def = '<field id="%s" grid_ref="%s" operation="instant" detect_missing_value="true" > %s </field>' % \
                    (further_field_id, further_grid_id, alias)
        field_defs[further_field_id] = field_def
        if printout:
            print "process_singleton : ", " adding field %s" % field_def
    return further_field_id, further_grid_id


def create_output_grid(ssh, grid_defs, domain_defs, target_hgrid_id, margs):
    # Build output grid (stored in grid_defs) by analyzing the spatial shape
    # Including horizontal operations. Can include horiz re-gridding specification
    # --------------------------------------------------------------------
    grid_ref = None

    # Compute domain name, define it if needed
    if ssh[0:2] == 'Y-':  # zonal mean and atm zonal mean on pressure levels
        # Grid normally has already been created upstream
        grid_ref = margs['src_grid_id']
    elif (ssh == 'S-na'):
        # COSP sites. Input field may have a singleton dimension (XIOS scalar component)
        grid_ref = cfsites_grid_id
        add_cfsites_in_defs(grid_defs, domain_defs)
        #
    elif ssh[0:3] == 'XY-' or ssh[0:3] == 'S-A':
        # this includes 'XY-AH' and 'S-AH' : model half-levels
        if (ssh[0:3] == 'S-A'):
            add_cfsites_in_defs(grid_defs, domain_defs)
            target_hgrid_id = cfsites_domain_id
        if target_hgrid_id:
            # Must create and a use a grid similar to the last one defined
            # for that variable, except for a change in the hgrid/domain
            grid_ref = change_domain_in_grid(target_hgrid_id, grid_defs)
            if grid_ref is False or grid_ref is None:
                raise dr2xml_error("Fatal: cannot create grid_def for %s with hgrid=%s" % (alias, target_hgrid_id))
    elif ssh == 'TR-na' or ssh == 'TRS-na':  # transects,   oce or SI
        pass
    elif ssh[0:3] == 'YB-':  # basin zonal mean or section
        pass
    elif ssh == 'na-na':  # TBD ? global means or constants - spatial integration is not handled
        pass
    elif ssh == 'na-A':  # only used for rlu, rsd, rsu ... in Efx ????
        pass
    else:
        raise dr2xml_error(
            "Fatal: Issue with un-managed spatial shape %s for variable %s in table %s" % (ssh, sv.label, table))
    return grid_ref


def generate_file_defs(lset, sset, year, enddate, context, cvs_path, pingfiles=None,
                       dummies='include', printout=False, dirname="./", prefix="", attributes=[],
                       select="on_expt_and_year"):
    # A wrapper for profiling top-level function : generate_file_defs_inner
    import cProfile, pstats, StringIO
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
    global print_wrv
    print_wrv = get_variable_from_lset_with_default("print_variables", True)
    cmvk = "CMIP6_CV_version"
    if cmvk in attributes: print "* %s: %s" % (cmvk, attributes[cmvk])
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
        if realm in processed_realms: continue
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
                        if reason not in excludedv: excludedv[reason] = []
                        excludedv[reason].append((svar.label, svar.mipTable))
        if printout and len(excludedv.keys()) > 0:
            print "The following pairs (variable,table) have been excluded for these reasons :"
            for reason in excludedv: print "\t", reason, ":", excludedv[reason]
    if (debug): print "For table AMon: ", [v.label for v in svars_per_table["Amon"]]
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
    if (debug):
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
                            if v not in pingvars: print v,
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
        out.write('<!-- dr2xml version %s --> \n' % version)
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
                if get_variable_from_lset_with_default("allow_duplicates_in_same_table", False) or svar.mipVarLabel not in count:
                    if not get_variable_from_lset_with_default("use_cmorvar_label_in_filename", False) and svar.mipVarLabel in count:
                        form = "If you really want to actually produce both %s and %s in table %s, " + \
                               "you must set 'use_cmorvar_label_in_filename' to True in lab settings"
                        raise dr2xml_error(form % (svar.label, count[svar.mipVarLabel].label, table))
                    count[svar.mipVarLabel] = svar
                    for grid in svar.grids:
                        a, hgrid, b, c, d = get_variable_from_lset_without_default('grids', grid_choice, context)
                        check_for_file_input(svar, hgrid, pingvars, field_defs, grid_defs, domain_defs, file_defs)
                        write_xios_file_def(svar, year, table, lset, sset, out, cvs_path,
                                            field_defs, axis_defs, grid_defs, domain_defs, scalar_defs, file_defs,
                                            dummies, skipped_vars_per_table, actually_written_vars,
                                            prefix, context, grid, pingvars, enddate, attributes)
                else:
                    print "Duplicate variable %s,%s in table %s is skipped, preferred is %s" % \
                          (svar.label, svar.mipVarLabel, table, count[svar.mipVarLabel].label)

        if cfsites_grid_id in grid_defs: out.write(cfsites_input_filedef())
        for file_def in file_defs: out.write(file_defs[file_def])
        out.write('\n</file_definition> \n')
        #
        # --------------------------------------------------------------------
        # End writing XIOS file_def file:
        # field_definition, axis_definition, grid_definition
        # and domain_definition auxilliary nodes
        # --------------------------------------------------------------------
        # Write all domain, axis, field defs needed for these file_defs
        out.write('<field_definition> \n')
        if get_variable_from_lset_with_default("nemo_sources_management_policy_master_of_the_world", False) and context == 'nemo':
            out.write('<field_group freq_op="_reset_" freq_offset="_reset_" >\n')
        for obj in sorted(field_defs.keys()): out.write("\t" + field_defs[obj] + "\n")
        if get_variable_from_lset_with_default("nemo_sources_management_policy_master_of_the_world", False) and context == 'nemo':
            out.write('</field_group>\n')
        out.write('\n</field_definition> \n')
        #
        out.write('\n<axis_definition> \n')
        out.write('<axis_group prec="8">\n')
        for obj in sorted(axis_defs.keys()): out.write("\t" + axis_defs[obj] + "\n")
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
        for w in warn: print "\t", w, " for vars : ", warn[w]
    if len(warnings_for_optimisation) > 0:
        print "Warning for fields which cannot be optimised (i.e. average before remap) because of an expr with @\n\t",
        for w in warnings_for_optimisation:
            print w.replace(get_variable_from_lset_without_default('ping_variables_prefix'), ""),
        print


def add_scalar_in_grid(gridin_def, gridout_id, scalar_id, scalar_name, remove_axis, change_scalar=True):
    """
    Returns a grid_definition with id GRIDOUT_ID from an input grid definition
    GRIDIN_DEF, by adding a reference to scalar SCALAR_ID

    If CHANGE_SCALAR is True and GRIDIN_DEF has an axis with an extract_axis child,
    remove it (because it is assumed to be a less well-defined proxy for the DR scalar

    If such a reference is already included in that grid definition, just return
    input def

    if REMOVE_AXIS is True, if GRIDIN_DEF already includes an axis, remove it for output grid

    Note : name of input_grid is not changed in output_grid

    """
    format = '< *scalar *([^>]*)scalar_ref=["\']%s["\']'
    expr = format % scalar_id
    if re.search(expr, gridin_def):
        return gridin_def
    gridin_def = gridin_def.replace("\n", "")
    # TBD : in change_scalar : discard extract_axis only if really relevant (get the right axis)
    # TBD : in change_scalar : preserve ordering of domains/axes...
    if change_scalar:
        extract_pattern = "<scalar *>.*<extract_axis.*/> *</scalar *>"
        gridin_def, count = re.subn(extract_pattern, "", gridin_def)
    pattern = '< *grid *([^> ]*) *id=["\']([^"\']*)["\'] *(.*)</ *grid *>'
    replace = r'<grid \1 id="%s" \3<scalar scalar_ref="%s" name="%s"/>  </grid>' % (gridout_id, scalar_id, scalar_name)
    (rep, count) = re.subn(pattern, replace, gridin_def.replace("\n", ""))
    if count == 0: raise dr2xml_error("No way to add scalar '%s' in grid '%s'" % (scalar_id, gridin_def))
    #
    # Remove any axis if asked for
    if remove_axis:
        axis_pattern = '< *axis *[^>]*>'
        (rep, count) = re.subn(axis_pattern, "", rep)
        # if count==1 :
        #    print "Info: axis has been removed for scalar %s (%s)"%(scalar_name,scalar_id)
        #    print "grid_def="+rep
    return rep + "\n"


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
        if not sv.modeling_realm: print "Warning: no modeling_realm associated to:", \
            sv.label, sv.mipTable, sv.mip_era
        for sd in sv.sdims.values():
            # couvre les dimensions verticales de type 'plev7h' ou 'p850'
            if sd.label.startswith("p") and any(sd.label.endswith(s) for s in plev_sfxs) and sd.label != 'pl700':
                lwps = sv.label_without_psuffix
                if lwps:
                    present_in_ping = ping_refs.has_key(prefix + lwps)
                    dummy_in_ping = None
                    if present_in_ping: dummy_in_ping = ("dummy" in ping_refs[prefix + lwps])

                    if present_in_ping and (not dummy_in_ping or dummies == 'include'):
                        sv.sdims[sd.label].is_zoom_of = "union_plevs_" + lwps
                        if not dict_plevs.has_key(lwps):
                            dict_plevs[lwps] = {sd.label: {sv.label: sv}}
                        else:
                            if not dict_plevs[lwps].has_key(sd.label):
                                dict_plevs[lwps].update({sd.label: {sv.label: sv}})
                            else:
                                if sv.label not in dict_plevs[lwps][sd.label].keys():
                                    dict_plevs[lwps][sd.label].update({sv.label: sv})
                                else:
                                    # TBS# print sv.label,"in table",sv.mipTable,"already listed for",sd.label
                                    pass
                    else:
                        if printout:
                            print "Info: ", lwps, "not taken into account for building plevs union axis because ", prefix + lwps,
                            if not present_in_ping:
                                print  "is not an entry in the pingfile"
                            else:
                                print "has a dummy reference in the pingfile"

                    # svar will be expected on a zoom axis of the union. Corresponding vertical dim must
                    # have a zoom_label named plevXX_<lwps> (multiple pressure levels) or pXX_<lwps> (single pressure level)
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
                    if sdsv.stdname:   sdim_union.stdname = sdsv.stdname
                    if sdsv.long_name: sdim_union.long_name = sdsv.long_name
                    if sdsv.positive:  sdim_union.positive = sdsv.positive
                    if sdsv.out_name:  sdim_union.out_name = sdsv.out_name
                    if sdsv.units:     sdim_union.units = sdsv.units
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
                    if printout: print "    -- on", plev, ":", plev_values
                if printout: print "       *", sv.label, "(", sv.mipTable, ")"
        list_plevs_union = list(plevs_union)
        list_plevs_union_num = [float(lev) for lev in list_plevs_union]
        list_plevs_union_num.sort(reverse=True)
        list_plevs_union = [str(lev) for lev in list_plevs_union_num]
        for lev in list_plevs_union: plevs_union_xios += " " + lev
        if printout: print ">>> XIOS plevs union:", plevs_union_xios
        sdim_union.label = "union_plevs_" + lwps
        if len(list_plevs_union) > 1: sdim_union.requested = plevs_union_xios
        if len(list_plevs_union) == 1: sdim_union.value = plevs_union_xios
        if printout: print "creating axis def for union :%s" % sdim_union.label
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
    name = "";
    for r in lrealms: name += "_" + r.replace(" ", "%")
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
    uniques = [];
    best_prio = dict()
    for v in lvars:
        lna = v.label_non_ambiguous
        lwps = v.label_without_psuffix
        if (not lna in best_prio) or (lna in best_prio and v.Priority < best_prio[lna].Priority):
            best_prio[lna] = v
        elif (not lwps in best_prio) or (lwps in best_prio and v.Priority < best_prio[lwps].Priority):
            best_prio[lwps] = v
        # elif not v.label_without_psuffix in labels :
        #    uniques.append(v); labels.append(v.label_without_psuffix)

    # lvars=uniques
    lvars = best_prio.values()
    lvars.sort(key=lambda x: x.label_without_psuffix)
    #
    if filename is None: filename = "ping" + name + ".xml"
    if filename[-4:] != ".xml": filename += ".xml"
    #
    if path_special:
        specials = read_special_fields_defs(lrealms, path_special)
    else:
        specials = False
    with open(filename, "w") as fp:
        fp.write('<!-- Ping files generated by dr2xml %s using Data Request %s -->\n' % (version, get_DR_version()))
        fp.write('<!-- lrealms= %s -->\n' % `lrealms`)
        fp.write('<!-- exact= %s -->\n' % `exact`)
        fp.write('<!-- ')
        for s in settings: fp.write(' %s : %s\n' % (s, settings[s]))
        fp.write('--> \n\n')
        fp.write('<context id="%s">\n' % context)
        fp.write("<field_definition>\n")
        if settings.get("nemo_sources_management_policy_master_of_the_world", False) and context == 'nemo':
            out.write('<field_group freq_op="_reset_ freq_offset="_reset_" >\n')
        if exact:
            fp.write("<!-- for variables which realm intersects any of " \
                     + name + "-->\n")
        else:
            fp.write("<!-- for variables which realm equals one of " \
                     + name + "-->\n")
        for v in lvars:
            if v.label_non_ambiguous:
                label = v.label_non_ambiguous
            else:
                label = v.label_without_psuffix
            if (v.label in debug): print "pingFile ... processing %s in table %s, label=%s" % (
            v.label, v.mipTable, label)

            if specials and label in specials:
                line = ET.tostring(specials[label]).replace("DX_", prefix)
                # if 'ta' in label : print "ta is special : "+line
                line = line.replace("\n", "").replace("\t", "")
                fp.write('   ');
                fp.write(line)
            else:
                fp.write('   <field id="%-20s' % (prefix + label + '"') + \
                         ' field_ref="')
                if dummy:
                    shape = highest_rank(v)
                    if v.label_without_psuffix == 'clcalipso': shape = 'XYA'
                    if dummy is True:
                        dummys = "dummy"
                        if dummy_with_shape: dummys += "_" + shape
                    else:
                        dummys = dummy
                    fp.write('%-18s/>' % (dummys + '"'))
                else:
                    fp.write('?%-16s' % (label + '"') + ' />')
            if comments:
                # Add units, stdname and long_name as a comment string
                if type(comments) == type(""): fp.write(comments)
                fp.write("<!-- P%d (%s) %s : %s -->" \
                         % (v.Priority, v.units, v.stdname, v.description))
            fp.write("\n")
        if 'atmos' in lrealms or 'atmosChem' in lrealms or 'aerosol' in lrealms:
            for tab in ["ap", "ap_bnds", "b", "b_bnds"]:
                fp.write('\t<field id="%s%s" field_ref="dummy_hyb" /><!-- One of the hybrid coordinate arrays -->\n' % (
                prefix, tab))
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
            if subrealm in subrealms_seen: continue
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
        for child in elt: rep.extend(get_xml_childs(child, tag))
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
    if printout: print "processing file %s :" % filename,
    if os.path.exists(filename):
        if printout: print "OK", filename
        root = ET.parse(filename).getroot()
        defs = get_xml_childs(root, tag)
        if defs:
            for field in defs:
                if printout: print ".",
                key = field.attrib['id']
                if attrib is None:
                    value = field
                else:
                    value = field.attrib.get(attrib, None)
                rep[key] = value
            if printout: print
            return rep
    else:
        if printout: print "No file "
        return None


def read_special_fields_defs(realms, path_special, printout=False):
    special = dict()
    subrealms_seen = []
    for realm in realms:
        for subrealm in realm.split():
            if subrealm in subrealms_seen: continue
            subrealms_seen.append(subrealm)
            d = read_xml_elmt_or_attrib(DX_defs_filename("field", subrealm, path_special), \
                                        tag='field', printout=printout)
            if d: special.update(d)
    rep = dict()
    # Use raw label as key
    for r in special: rep[r.replace("DX_", "")] = special[r]
    return rep


def highest_rank(svar):
    """Returns the shape with the highest needed rank among the CMORvars
    referencing a MIPvar with this label
    This, assuming dr2xml would handle all needed shape reductions
    """
    # mipvarlabel=svar.label_without_area
    mipvarlabel = svar.label_without_psuffix
    shapes = [];
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
        if shape: shapes.append(shape)
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


def make_source_string(sources, source_id):
    """
    From the dic of sources in CMIP6-CV, Creates the string representation of a
    given model (source_id) according to doc on global_file_attributes, so :

    <modified source_id> (<year>): atmosphere: <model_name> (<technical_name>, <resolution_and_levels>); ocean: <model_name> (<technical_name>, <resolution_and_levels>); sea_ice: <model_name> (<technical_name>); land: <model_name> (<technical_name>); aerosol: <model_name> (<technical_name>); atmospheric_chemistry <model_name> (<technical_name>); ocean_biogeochemistry <model_name> (<technical_name>); land_ice <model_name> (<technical_name>);

    """
    # mpmoine_correction:make_source_string: pour lire correctement le fichier 'CMIP6_source_id.json'
    source = sources[source_id]
    components = source['model_component']
    rep = source_id + " (" + source['release_year'] + "): "
    for realm in ["aerosol", "atmos", "atmosChem", "land", "ocean", "ocnBgchem", "seaIce"]:
        component = components[realm]
        description = component['description']
        if description != "none": rep = rep + "\n" + realm + ": " + description
    return rep


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
           '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute" write_weight="true" /> ' + \
           '</domain>  '
    # return '<domain id="CMIP6_%s" ni_glo="%d" nj_glo="%d" type="rectilinear"  prec="8" lat_name="lat" lon_name="lon" > '%(resol,ni,nj) +\
    #    '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute" write_weight="true" /> '+\
    #    '</domain>  '


def ping_alias(svar, pingvars, error_on_fail=False):
    # dans le pingfile, grace a la gestion des interpolations
    # verticales, on n'attend pas forcement les alias complets des
    # variables (CMIP6_<label>), on peut se contenter des alias
    # reduits (CMIP6_<lwps>)

    # par ailleurs, si on a defini un label non ambigu alors on l'utilise
    # comme ping_alias (i.e. le field_ref)

    pref = get_variable_from_lset_without_default("ping_variables_prefix")
    if svar.label_non_ambiguous:
        # print "+++ non ambiguous", svar.label,svar.label_non_ambiguous
        alias_ping = pref + svar.label_non_ambiguous  # e.g. 'CMIP6_tsn_land' and not 'CMIP6_tsn'
    else:
        # print "+++ ambiguous", svar.label
        # Ping file may provide the variable on the relevant pressure level - e.g. CMIP6_rv850
        alias_ping = pref + svar.label
        if alias_ping not in pingvars:
            # if not, ping_alias is supposed to be without a pressure level suffix
            alias_ping = pref + svar.label_without_psuffix  # e.g. 'CMIP6_hus' and not 'CMIP6_hus7h'
        # print "+++ alias_ping = ", pref, svar.label_without_psuffix, alias_ping
    if alias_ping not in pingvars:
        if error_on_fail:
            raise dr2xml_error("Cannot find an alias in ping for variable %s" % svar.label)
        else:
            return None
    return alias_ping


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
    if realm == "atmosChem" and 'CHEM' not in components: return False
    if realm == "aerosol" and 'AER' not in components: return False
    if realm == "ocnBgChem" and 'BGC' not in components: return False
    #
    with_ocean = ('OGCM' in components or 'AOGCM' in components)
    if 'seaIce' in realm and not with_ocean: return False
    if 'ocean' in realm and not with_ocean: return False
    #
    with_atmos = ('AGCM' in components or 'AOGCM' in components)
    if 'atmos' in realm and not with_atmos: return False
    if 'atmosChem' in realm and not with_atmos: return False
    if realm == '' and not with_atmos: return False  # In DR 01.00.15 : some atmos variables have realm=''
    #
    with_land = with_atmos or ('LAND' in components)
    if 'land' in realm and not with_land: return False
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
        if printout: print domain_defs[file_domain_id]
        if printout: print grid_defs[file_grid_id]

        # Create xml for reading the variable
        filename = externs[sv.label][hgrid][grid_choice]
        file_id = "remapped_%s_file" % sv.label
        field_in_file_id = "%s_%s" % (sv.label, hgrid)
        # field_in_file_id=sv.label
        file_def = '\n<file id="%s" name="%s" mode="read" output_freq="1ts" enabled="true" >' % \
                   (file_id, filename)
        file_def += '\n\t<field id="%s" name="%s" operation="instant" freq_op="1ts" freq_offset="1ts" grid_ref="%s"/>' % \
                    (field_in_file_id, sv.label, file_grid_id)
        file_def += '\n</file>'
        file_defs[file_id] = file_def
        if printout: print file_defs[file_id]
        #
        # field_def='<field id="%s" grid_ref="%s" operation="instant" >%s</field>'%\
        field_def = '<field id="%s" grid_ref="%s" field_ref="%s" operation="instant" freq_op="1ts" freq_offset="0ts" />' % \
                    (pingvar, grid_id, field_in_file_id)
        field_defs[field_in_file_id] = field_def
        context_index = get_config_variable("context_index")
        context_index[pingvar] = ET.fromstring(field_def)

        if printout:
            print field_defs[field_in_file_id]
        #
