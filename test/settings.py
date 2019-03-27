#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals


rootpath = "/cnrm/est/USERS/senesi/public/CMIP6/"
my_cvspath = rootpath + "data_request/CMIP6_CVs/"

lab_and_model_settings = {
    'institution_id': "CNRM-CERFACS",  # institution should be read in CMIP6_CV, if up-to-date
    'source_types': {"CNRM-CM6-1": "AOGCM", "CNRM-CM6-1-HR": "AOGCM",
                     "CNRM-ESM2-1": "ESM", "CNRM-ESM2-1-HR": "ESM"},

    "source_id": "CNRM-CM6-1",
    "source": "CNRM-CM6-1",  # Useful only if CMIP6_CV is not up-to-date for the source_id
    'references': "ref",
    'info_url': "http://www.umr-cnrm.fr/cmip6/",
    'contact': 'contact.cmip@cnrm.fr',
    'mips_short': {'C4MIP', 'SIMIP', 'OMIP', 'CFMIP', 'RFMIP'},
    'mips': {'AerChemMIP', 'C4MIP', 'CFMIP', 'DAMIP', 'FAFMIP', 'GeoMIP', 'GMMIP', 'ISMIP6',
             'LS3MIP', 'LUMIP', 'OMIP', 'PMIP', 'RFMIP', 'ScenarioMIP', 'CORDEX', 'SIMIP'},
    'max_priority': 3,
    'tierMax': 3,
    "ping_variables_prefix": "CMIP6_",
    # excluded_vars_file="./inputs/non_published_variables.txt"
    "excluded_vars": ['pfull', 'phalf'],
    "excluded_spshapes": ["XYA-na", "XYG-na", "na-A", "Y-P19", "Y-P39", "Y-A", "Y-na"],
    # Clims are not handled by Xios yet, nor ice-sheet dedicated grids
    "excluded_tables": ["Oclim", "E1hrClimMon", 'IfxAnt', 'IfxGre', 'ImonGre', 'ImonAnt'],
    # "listof_home_vars":rootpath+"dr2xml/config_utest/utest020_listof_home_vars.txt",
    "listof_home_vars": None,
    "path_extra_tables": None,
    'realms_per_context': {'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'],
                           'arpsfx': ['atmos', 'atmos atmosChem', 'aerosol', 'atmos land', 'land',
                                      'landIce land', 'aerosol land', 'land landIce', 'landIce', ],
                           },
    'orphan_variables': {'nemo': ['dummy_variable_for_illustration_purpose'],
                         'arpsfx': [],
                         },
    'vars_OK': dict(),
    # A per-variable dict of comments valid for all simulations
    'comments': {},
    # Sizes for atm and oce grids (cf DR doc)
    "sizes": [259200, 60, 64800, 40, 20, 5, 100],
    # What is the maximum size of generated files, in number of float values
    "max_file_size_in_floats": 500. * 1.e+6,
    # grid_policy among None, DR, native, native+DR, adhoc- see docin grids.py
    "grid_policy": "DR",
    # Resolutions
    "grids": {
        "LR": {
            "arpsfx": ["gr", "complete", "250 km",
                       "data regridded to a T127 gaussian grid (128x256 latlon) "
                       "from a native atmosphere T127l reduced gaussian grid"],
            #        "arpsfx" : [ "gn","" , "250 km", "native T127 reduced gaussian grid"] ,
            "nemo": ["gn", "", "100km", "native ocean tri-polar grid with 105 k ocean cells"], },

        "HR": {
            "arpsfx": ["gr", "completeHR", "50 km",
                       "data regridded to a 359 gaussian grid (180x360 latlon) "
                       "from a native atmosphere T359l reduced gaussian grid"],
            "nemo": ["gn", "", "25km", "native ocean tri-polar grid with 1.47 M ocean cells"], },
    },
    'grid_choice': {"CNRM-CM6-1": "LR", "CNRM-CM6-1-HR": "HR", "CNRM-ESM2-1": "LR", "CNRM-ESM2-1-HR": "HR"},
    # Component Models Time steps (s)
    "model_timestep": {"arpsfx": 900., "nemo": 900., "trip": 1800.},

    # --- Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR
    "use_union_zoom": False,

    #
    "vertical_interpolation_sample_freq": "3h",

    # The CMIP6 frequencies that are unreachable for a single model run. Datafiles will
    # be labelled with dates consistent with content (but not with CMIP6 requirements).
    # Allowed values are only 'dec' and 'yr'
    "too_long_periods": ["dec", "yr"]
}

simulation_settings_old = {
    "experiment_id": "historical",
    "activity_id": "CMIP",
    "parent_experiment_id": "piControl",  # omit this setting (or set to 'no parent') if not applicable
    # (remaining parent attributes will be disregarded)
    "branch_method": "standard",  # default value='standard', meaning ~ "select a start date"
    "branch_time_in_parent": "365.0D0",  # a double precision value, in parent time units,
    "branch_time_in_child": "0.0D0",  # a double precision value, in child time units,
    "comments": {}
}

simulation_settings = {
    # Dictionnary describing the necessary attributes for a given simulation

    # Warning : some lines are commented out in this example but should be
    # un-commented in some cases. See comments

    "experiment_id": "historical",
    # "experiment_id"  : "Forced-Atmos-Land",
    # "experiment_id"  : "Coupled",
    # "experiment_id"  : "DCPP-C13",

    # "contact"        : "", set it only if it is specific to the simualtion
    # "project"        : "CMIP6",  #CMIP6 is the default

    # 'source_type'    : "ESM" # If source_type is special only for this experiment (e.g. : AMIP)
    # (i.e. not the same as in lab_and_model settings), you may tell that here

    # MIP specifying the experiment. For historical, it is CMIP6 itself
    # In a few cases it may be appropriate to include multiple activities in the activity_id
    # (with multiple activities allowed, separated by single spaces).
    # An example of this is  LUMIP AerChemMIP  for one of the land-use change experiments.
    "activity_id": "CMIP",  # examples :  PMIP ,  LS3MIP LUMIP ; defaults to "CMIP6"

    # It is recommended that some description be included to help identify major differences among variants,
    # but care should be taken to record correct information.  Prudence dictates that this attribute includes
    # a warning along the following lines:   Information provided by this attribute may in some cases be flawed.#
    # Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute.
    "variant_info": "Start date chosen so that variant r1i1p1f1 has the better fit with Krakatoa impact on tos",
    #
    "realization_index": 1,  # Value may be omitted if = 1
    "initialization_index": 1,  # Value may be omitted if = 1
    "physics_index": 1,  # Value may be omitted if = 1
    "forcing_index": 1,  # Value may be omitted if = 1
    #
    # All about the parent experiment and branching scheme
    "parent_experiment_id": "piControl",  # omit this setting (or set to 'no parent') if not applicable
    # (remaining parent attributes will be disregarded)
    "branch_method": "standard",  # default value='standard', meaning ~ "select a start date"
    "branch_time_in_parent": "365.0D0",  # a double precision value, in parent time units,
    "branch_time_in_child": "0.0D0",  # a double precision value, in child time units,
    # 'parent_time_units'    : "" #in case it is not the same as child time units
    # 'parent_variant_label' :""  #Default to 'same as child'. Other cases should be expceptional
    # "parent_mip_era"       : 'CMIP5'   # only in special cases (e.g. PMIP warm start from CMIP5/PMIP3 experiment)
    # 'parent_activity   '   : 'CMIP'    # only in special cases, defaults to CMIP
    # 'parent_source_id'     : 'CNRM-CM5.1' #only in special cases, where parent model is not the same model
    #
    "sub_experiment_id": "none",  # Optional, default is 'none'; example : s1960.
    "sub_experiment": "none",  # Optional, default in 'none'
    "history": "none",  # Used when a simulation is re-run, an output file is modified ....
    # A per-variable dict of comments which are specific to this simulation. It will replace
    # the all-simulation comment present in lab_and_model_settings
    'comments': {
        'tas': 'tas diagnostic uses a special scheme in this simulation',
    }
}
