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
from scope import dreqQuery
import dreq

# 2- CMIP6 Controled Vocabulary (available from 
# https://github.com/WCRP-CMIP/CMIP6_CVs). You will provide its path 
# as argument to functions defined here

# 3- XIOS release must be 1442 or above (to be fed with the outputs)
#  see https://forge.ipsl.jussieu.fr/ioserver/wiki

####################################
# End of pre-requisites
####################################

version="1.11"
print "\n",50*"*","\n*"
print "* %29s"%"dr2xml version: ", version

conventions="CF-1.7 CMIP-6.2" 
# The current code should comply with this version of spec doc at
# https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit
CMIP6_conventions_version="v6.2.4"
print "* %29s"%"CMIP6 conventions version: ",CMIP6_conventions_version

import json
 


import datetime
import re
import collections
import sys,os,glob
import xml.etree.ElementTree as ET

# mpmoine_merge_dev2_v0.12: posixpath.dirname ne marche pas chez moi
#TBS# from os import path as os_path
#TBS# prog_path=os_path.abspath(os_path.split(__file__)[0])

# Local packages
from vars import simple_CMORvar, simple_Dim, process_homeVars, complement_svar_using_cmorvar, \
                multi_plev_suffixes, single_plev_suffixes, get_simplevar, scalar_vertical_dimension
from grids import decide_for_grids, DRgrid2gridatts,\
    split_frequency_for_variable, timesteps_per_freq_and_duration
from Xparse import init_context, id2grid, id2gridid, idHasExprWithAt


# A auxilliary tables
from table2freq import Cmip6Freq2XiosFreq, longest_possible_period

# CFsites handling has its own module
from cfsites import cfsites_domain_id, cfsites_grid_id, cfsites_input_filedef, add_cfsites_in_defs

print_DR_errors=True
print_multiple_grids=False

dq = dreq.loadDreq()
print "* %29s"%"CMIP6 Data Request version: ", dq.version
print "\n*\n",50*"*"

cell_method_warnings=[]
warnings_for_optimisation=[]
sn_issues=dict()

context_index=None

# global variable : the list of Request Links which apply for 'our' MIPS and which are not explicitly excluded using settings
# It is set in select_CMORvars_for_lab and used in endyear_for_CMORvar
global_rls=None
rls_for_all_experiments=None
sc=None

# Next variable is used to circumvent an Xios 1270 shortcoming. Xios
# should read that value in the datafile. Actually, it did, in some
# earlier version ...
axis_count=0


""" An example/template  of settings for a lab and a model"""
example_lab_and_model_settings={

    'institution_id': "CNRM-CERFACS", # institution should be read in CMIP6_CV, if up-to-date

    # We describe the "CMIP6 source type" (i.e. components assembly) which is the default
    # for each model. This value can be changed on a per experiment basis, in experiment_settings file
    # However, using a 'configuration' is finer (see below)
    # CMIP6 component conventions are described at
    #          https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_source_type.json
    'source_types' : { "CNRM-CM6-1" : "AOGCM AER", "CNRM-CM6-1-HR" : "AOGCM AER", 
                       "CNRM-ESM2-1": "AOGCM BGC AER CHEM"  , "CNRM-ESM2-1-HR": "AOGCM BGC AER" },

    # Optional : 'configurations' are shortcuts for a triplet (model, source_type, unused_contexts)
    'configurations' : {
        "AGCM":   ("CNRM-CM6-1"   ,"AGCM"               , ['nemo']),
        "AESM":   ("CNRM-ESM2-1"  ,"AGCM BGC AER CHEM"  , ['nemo']),
        "AOGCM":  ("CNRM-CM6-1"   ,"AOGCM"              , []      ),
        "AOESM":  ("CNRM-ESM2-1"  ,"AOGCM BGC AER CHEM" , []      ),
        "AGCMHR": ("CNRM-CM6-1-HR","AGCM"               , ['nemo']),
        "AESMHR": ("CNRM-ESM2-1"  ,"AGCM BGC AER"       , []      ),
        "AOGCMHR":("CNRM-CM6-1-HR","AOGCM"              , []      ),
        "AOESMHR":("CNRM-ESM2-1"  ,"AOGCM BGC AER"      , []      ),
        "LGCM":   ("CNRM-CM6-1"   ,"LAND"               , ['nemo']),
        "LESM":   ("CNRM-ESM2-1"  ,"LAND BGC"           , ['nemo']),
        "OGCM":   ("CNRM-CM6-1"   ,"OGCM"               , ['surfex','trip']),
        "OESM":   ("CNRM-ESM2-1"  ,"OGCM BGC"           , ['surfex','trip']) },

    #'source'         : "CNRM-CM6-1", # Useful only if CMIP6_CV is not up to date
    'references'    :  "A character string containing a list of published or web-based "+\
        "references that describe the data or the methods used to produce it."+\
        "Typically, the user should provide references describing the model"+\
        "formulation here",
    'info_url'      : "http://www.umr-cnrm.fr/cmip6/",
    'contact'       : 'contact.cmip@meteo.fr',
    
    # We account for the list of MIPS in which the lab takes part.
    # Note : a MIPs set limited to {'C4MIP'} leads to a number of tables and 
    # variables which is manageable for eye inspection
    'mips_for_test': {'C4MIP', 'SIMIP', 'OMIP', 'CFMIP', 'RFMIP'} , 
    'mips' : {
        "LR" : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
                      'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP','CMIP6', 'CMIP'},
        "HR" : {'OMIP','ScenarioMIP','CORDEX','CMIP6', 'CMIP'},
        },

    # A character string containing additional information about the models. Will be complemented
    # with the experiment's specific comment string
    "comment"              : "",

    # Max variable priority level to be output (you may set 3 when creating ping_files while
    # being more restrictive at run time); values in simulation_settings may override the one below
    'max_priority' : 1,
    'tierMax'      : 1,

    # The ping file defines variable names, which are constructed using CMIP6 "MIPvarnames" 
    # and a prefix which must be set here, and can be the empty string :
    "ping_variables_prefix" : "CMIP6_",

    # We account for a list of variables which the lab does not want to produce , 
    # Names must match DR MIPvarnames (and **NOT** CMOR standard_names)
    # excluded_vars_file="../../cnrm/non_published_variables"
    "excluded_vars" : ['pfull', 'phalf', "zfull" ], # because we have a pressure based hydrid coordinate,
                                                    # and no fixed height levels
    
    # Vars computed with a period which is not the basic timestep must be declared explictly,
    # with that period, in order that 'instant' sampling works correctly
    # (the units for period should be different from the units of any instant ouput frequency
    # for those variables - 'mi' loooks fine, 'ts' may work)
    "special_timestep_vars" : {
        "60mi" : ['parasolRefl','clhcalipso','cltcalipso','cllcalipso','clmcalipso', \
                'cfadLidarsr532','clcalipso','clcalipso2','cfadDbze94', \
                'jpdftaureliqmodis','clisccp','jpdftaureicemodis','clmisr'],
        },

    # You can specifically exclude some pairs (vars,tables), here in lab_settings 
    # and also (in addition) in experiment_settings
    "excluded_pairs" : [ ('fbddtalk','Omon') ] ,

    # For debugging purpose, if next list has members, this has precedence over
    # 'excluded_vars' and over 'excluded_vars_per_config'
    #"included_vars" : [ 'ccb' ],

    # When atmospheric vertical coordinate implies putting psol in model-level output files, we
    # must avoid creating such file_def entries if the model does not actually send the 3D fields
    # (because this leads to files full of undefined values)
    # We choose to describe such fields as a list of vars dependant on the model configuration
    # because the DR is not in a good enough shape about realms for this purpose
    "excluded_vars_per_config" : {
        "AGCM":   [ "ch4", "co2", "co", "concdust", "ec550aer", "h2o", "hcho", "hcl", \
                    "hno3", "mmrbc", "mmrdust", "mmroa", "mmrso4", "mmrss", \
                    "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", "so2" ],
        "AOGCM":   [ "ch4", "co2", "co", "concdust", "ec550aer", "h2o", "hcho", "hcl", \
                    "hno3", "mmrbc", "mmrdust", "mmroa", "mmrso4", "mmrss", \
                    "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", "so2" ],
        },
    #
    "excluded_spshapes": ["XYA-na","XYG-na", # GreenLand and Antarctic grids we do not want to produce
                          "na-A", # RFMIP.OfflineRad : rld, rlu, rsd, rsu in table Efx ?????
                          "Y-P19","Y-P39", "Y-A","Y-na" # Not yet handled by dr2xml
    ],

    "excluded_tables"  : ["Oclim" , "E1hrClimMon" , "ImonAnt", "ImonGre" ] , # Clims are not handled by Xios yet

    # For debugging purpose : if next list has members, only those tables will be processed 
    #"included_tables"  : ["AMon" ] , # If not empty, has priority over excluded_tables 

    "excluded_request_links"  : [
        "RFMIP-AeroIrf" # 4 scattered days of historical, heavy output -> please rerun model for one day
         # for each day of this request_link 
    ],
    # For debugging purpose : if next list has members, only those requestLinks will be processed 
    "included_request_links"  : [ ],
    
    # We account for a default list of variables which the lab wants to produce in most cases
    # This can be changed at the experiment_settings level
    #"listof_home_vars":"../../cnrm/listof_home_vars.txt",

    # If we use extra tables, we can set it here (and supersed it in experiment settings)
    #'path_extra_tables'=
    
    # Each XIOS  context does adress a number of realms
    'realms_per_context' : { 
        'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'] ,
        'arpsfx' : ['atmos', 'atmos atmosChem', 'atmosChem', 'aerosol', 'atmos land', 'land',
                    'landIce land',  'aerosol','land landIce',  'landIce', ],
        'trip'   : [],
    }, 
    # Some variables, while belonging to a realm, may fall in another XIOS context than the 
    # context which hanldes that realm
    'orphan_variables' : {
        'trip'    : ['dgw', 'drivw', 'fCLandToOcean', 'qgwr', 'rivi', 'rivo', 'waterDpth', 'wtd'],
    },
    # A per-variable dict of comments valid for all simulations
    'comments'     : {
        'rld' : 'nothing special about this variable'
        },
    #
    'grid_choice' : { "CNRM-CM6-1" : "LR", "CNRM-CM6-1-HR" : "HR",
                      "CNRM-ESM2-1": "LR"  , "CNRM-ESM2-1-HR": "HR" },
    # if you want to produce the same variables set for all members, set next parameter to False
    "filter_on_realization" : True,
    # Sizes for atm and oce grids (cf DR doc); Used for computing file split frequency
    "sizes"  : { "LR" : [292*362  , 75, 128*256, 91, 30, 14, 128],
                 "HR" : [1442*1021, 75, 720*360, 91, 30, 14, 128] },

    # What is the maximum duration of data period in a single file (integer, in years)
    "max_split_freq"          : None,
    
    # What is the maximum size of generated files, in number of float values
    "max_file_size_in_floats" : 2000.*1.e+6 , # 2 Giga octets
    # Required NetCDF compression level
    "compression_level"  :  0,
    # Estimate of number of bytes per floating value, given the chosen compresssion level
    "bytes_per_float" : 2.0,
    
    # grid_policy among None, DR, native, native+DR, adhoc- see docin grids.py 
    "grid_policy" : "adhoc",
    
    # Grids : per model resolution and per context :
    #              - CMIP6 qualifier (i.e. 'gn' or 'gr') for the main grid chosen (because you
    #                 may choose has main production grid a regular one, when the native grid is e.g. unstructured)
    #              - Xios id for the production grid (if it is not the native grid),
    #              - Xios id for the latitude axis used for zonal means (mist match latitudes for grid above)
    #              - resolution of the production grid (using CMIP6 conventions),
    #              - grid description
    "grids" : {
        
      "LR"    : {
        "surfex" : [ "gr","complete" , "glat", "250 km", "data regridded to a T127 gaussian grid (128x256 latlon) from a native atmosphere T127l reduced gaussian grid"] ,
          "trip" : [ "gn", ""        ,  ""   , "50 km" , "regular 1/2 deg lat-lon grid" ],
          "nemo" : [ "gn", ""        ,  ""   , "100 km" , "native ocean tri-polar grid with 105 k ocean cells" ],},
        
      "HR"    : {
        "surfex" : [ "gr","complete" , "glat", "50 km", "data regridded to a 359 gaussian grid (180x360 latlon) from a native atmosphere T359l reduced gaussian grid"] ,
          "trip" : [ "gn", ""        ,  ""   , "50 km" , "regular 1/2 deg lat-lon grid" ],
          "nemo" : [ "gn", ""        ,  ""   , "25 km" , "native ocean tri-polar grid with 1.47 M ocean cells" ],},
    },
    # "nb_longitudes_in_model": { "surfex" :"ndlon", "nemo": "" },
    #        
    # Basic sampling timestep set in your field definition (used to feed metadata 'interval_operation')
    "sampling_timestep" : {
              "LR"    : { "surfex":900., "nemo":1800. },
              "HR"    : { "surfex":900., "nemo":1800. },
    },

    # We create sampled time-variables for controlling the frequency of vertical interpolations
    "vertical_interpolation_sample_freq" : "3h",
    "vertical_interpolation_operation"   : "instant", # LMD prefers 'average'

    #--- Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR
    "use_union_zoom" : False,

    # The CMIP6 frequencies that are unreachable for a single model run. Datafiles will
    # be labelled with dates consistent with content (but not with CMIP6 requirements).
    # Allowed values are only 'dec' and 'yr'
    "too_long_periods" : ["dec", "yr" ] ,

    # Describe the branching scheme for experiments involved in some 'branchedYears type' tslice
    # (for details, see: http://clipc-services.ceda.ac.uk/dreq/index/Slice.html )
    # Just put the as key the common start year in child and as value the list of start years in parent for all members
    "branching" : {
        "CNRM-CM6-1"  : {"historical" : (1850, [ 1850, 1883, 1941, 1960, 1990, 2045, 2079, 2108, 2214, 2269 ]) },
        "CNRM-ESM2-1" : {"historical" : (1850, [ 1850, 1883, 1941 ]) },
        },

    # We can control the max output level set for all output files, 
    "output_level"       : 10,

    # For debug purpose, you may slim down xml files by setting next entry to False
    "print_variables" : True ,

    # Set that to True if you use a context named 'nemo' and the
    # corresponding model unduly sets a general freq_op AT THE
    # FIELD_DEFINITION GROUP LEVEL. Due to Xios rules for inheritance,
    # that behavior prevents inheriting specific freq_ops by reference
    # from dr2xml generated field_definitions
    "nemo_sources_management_policy_master_of_the_world" : False,
    
    # You may add a series of NetCDF attributes in all files for this simulation
    "non_standard_attributes" : { "model_minor_version" : "6.1.0" },

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
    'non_standard_axes' : {
        # Space dimensions - Arpege :
        'klev' : 'alevel' , 'klev_half' : 'alevel' ,
    
        # COSP
        'effectRadIc'  :'effectRadIc' , 'effectRadL'   :'effectRadL',
        'sza5'         :'sza5' ,
        'dbze'         :'dbze' ,
        
        # Land dimensions
        'soilpools'    :('soilpools', 'fast medium slow'),
        #'landUse'      :'landUse' ,
        'vegtype'      : ('vegtype','Bare_soil Rock Permanent_snow Temperate_broad-leaved_decidus Boreal_needleaf_evergreen Tropical_broad-leaved_evergreen C3_crop C4_crop Irrigated_crop C3_grass C4_grass Wetland Tropical_broad-leaved_decidus Temperate_broad-leaved_evergreen Temperate_needleaf_evergreen Boreal_broad-leaved_decidus Boreal_needleaf_decidus Tundra_grass Shrub') ,
        
        # Space dimensions - Nemo
        'depthw' : 'olevel','deptht':'olevel','depthu':'olevel','depthv':'olevel',
        'j-mean' : 'latitude',
    
        # Ocean transects and basins
        #'oline'        :'oline' ,
        #'siline'       :'siline',
        'basin '       :('basin','global_ocean atlantic_arctic_ocean indian_pacific_ocean dummy dummy'),
    
        # toy_cnrmcm, for oce (Note : for atm, there is adhoc code)
        'axis_oce' :'olevel' , 'lat_oce' : 'latitude', 'transect_axis' : 'oline',
        'basin_oce_3' :('basin','global_ocean atlantic_arctic_ocean indian_pacific_ocean dummy dummy'),
    },

    # A smart workflow will allow you to extend a simulation during it
    # course and to complement the output files accordingly, by
    # managing the 'end date' part in filenames. You can then set next
    # setting to False (default is True)
    'dr2xml_manages_enddate' : True,

    # You may provide some variables already horizontally remapped 
    # to some grid (i.e. Xios domain) in external files. The varname in file 
    # must match the referenced id in pingfile. Tested only for fixed fields 
    'fx_from_file_vars' : {
        "areacella" : { "complete" :
                        { "LR" : "areacella_LR",
                          "HR" : "areacella_HR",}}},
    
    # The path of the directory which, at run time, contains the root XML file (iodef.xml)
    'path_to_parse': "./",

    # Should we allow for duplicate vars : two vars with same
    # frequency, shape and realm , which differ only by the table.
    # In DR01.00.21, this actually applies to very few fields (ps-Aermon,
    # tas-ImonAnt, areacellg-IfxAnt). Defaults to True
    'allow_duplicates' : True,

    # Should we allow for another type of duplicate vars : two vars
    # with same name in same table (usually with different
    # shapes). This applies to e.g. CMOR vars 'ua' and 'ua7h' in
    # 6hPlevPt. Default to False, because CMIP6 rules does not allow
    # to name output files differently in that case. If set to True,
    # you should also set 'use_cmorvar_label_in_filename' to True to
    # overcome the said rule
    'allow_duplicates_in_same_table' : False,

    # CMIP6 rule is that filenames includes the variable label, and
    # that this variable label is not the CMORvar label, but 'MIPvar'
    # label. This may lead to conflicts, e.g. for 'ua' and 'ua7h' in
    # table 6hPlevPt; next setting allows to avoid that, if set to True
    'use_cmorvar_label_in_filename' : False,

    # DR01.00.21 does not include Gibraltar strait, which is requested by OMIP
    # Can include it, if model provides it as last value of array. Defaults to false
    'add_Gribraltar' : False,

    # In order to identify which xml files generates a problem, you can use this flag
    'debug_parsing' : False,

    # DR has sn attributes for MIP variables. They can be real,CF-compliant, standard_names or
    # pseudo_standard_names, i.e. not yet approved labels. Default is to use only CF ones
    'allow_pseudo_standard_names' : False,

    # For an extended printout of selected CMOR variables, grouped by variable label
    'print_stats_per_var_label' : False,

    # When using select='no', Xios may enter an endless loop, which is solved if next setting is False
    'allow_tos_3hr_1deg' : True
}


""" An example/template of settings for a simulation """

example_simulation_settings={    
    # Dictionnary describing the necessary attributes for a given simulation

    # Warning : some lines are commented out in this example but should be 
    # un-commented in some cases. See comments

    # DR experiment name to process. See http://clipc-services.ceda.ac.uk/dreq/index/experiment.html
    "experiment_id"  : "historical",
    # Experiment label to use in file names and attribute, (default is experiment_id)
    #"expid_in_filename"   : "myexpe", 

    # If there is no configuration in lab_settings which matches you case, please rather
    # use next or next two entries : source_id and, if needed, source_type
    'configuration'   : 'AOGCM',

    # For some experiments (e.g. concentration-driven historical in AESM config), the only way to 
    # avoid producing useless fields is to explictly exclude variables (in addition to those in lab_settings)
    'excluded_vars' : [],

    # It can be handy to exclude some Tables at the experiment level. They are added to the lab-level set
    #"excluded_tables"  : [ ] , 

    #'source_id'      : "CNRM-CM6-1", 
    #'source_type'    : "OGCM" ,# If the default source-type value for your source (from lab settings)
    # does not fit, you may change it here.
    # "This should describe the model most directly responsible for the
    # output.  Sometimes it is appropriate to list two (or more) model types here, among
    # AER, AGCM, AOGCM, BGC, CHEM, ISM, LAND, OGCM, RAD, SLAB "
    # e.g. amip , run with CNRM-CM6-1, should quote "AGCM AER"
    # Also see note 14 of https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit

    #"contact"        : "", set it only if it is specific to the simualtion
    #"project"        : "CMIP6",  #CMIP6 is the default

    #'max_priority' : 1,  # a simulation may be run with a max_priority which overrides the one in lab_settings
    #'tierMax'      : 1,  # a simulation may be run with a Tiermax overrides the one in lab_settings

    # It is recommended that some description be included to help
    # identify major differences among variants, but care should be
    # taken to record correct information.  dr2xml will add in all cases:
    #  'Information provided by this attribute may in some cases be
    #  flawed. Users can find more comprehensive and up-to-date
    #  documentation via the further_info_url global attribute.'
    "variant_info"      : "Start date after 300 years of control run",
    #
    "realization_index"    : 1, # Value may be omitted if = 1
    "initialization_index" : 1, # Value may be omitted if = 1
    "physics_index"        : 1, # Value may be omitted if = 1
    "forcing_index"        : 3, # Value may be omitted if = 1
    #
    # All about the branching scheme from parent
    "branch_method"        : "standard", # default value='standard' meaning ~ "select a start date" 
                                        # (this is not necessarily the parent start date)
    'parent_time_ref_year' : 1850,      # MUST BE CONSISTENT WITH THE TIME UNITS OF YOUR MODEL(S) !!!
    "branch_year_in_parent": 2150,      # if your calendar is Gregorian, you can specify the branch year in parent directly
                                        # This is an alternative to using "branch_time_in_parent".
    #"branch_month_in_parent": 1,        # You can then also set the month. Default to 1
    #"branch_time_in_parent": "365.0D0", # a double precision value, in days, used if branch_year_in_parent is not applicable
                                         # This is an alternative to using "branch_year_in_parent"
    #'parent_time_units'    : "" #in case it is not the same as child time units

    # In some instances, the experiment start year is not explicit or is doubtful in DR. See
    # file doc/some_experiments_starty_in_DR01.00.21. You should then specifiy it, using next setting
    # in order that requestItems analysis work in all cases
    
    # In some other cases, DR requestItems which apply to the experiment form its start does not 
    # cover its whole duration and have a wrong duration (computed based on a wrong start year); 
    # They necessitate to fix the start year 
    #'branch_year_in_child' : 1950,

    # If you want to carry on the experiment beyond the duration set in DR, and that all
    # requestItems that apply to DR end year also apply later on, set 'end_year'
    # You can also set it if you don't know if DR has a wrong value
    #'end_year' : 2014,

    'child_time_ref_year'  : 1850,      # MUST BE CONSISTENT WITH THE TIME UNITS OF YOUR MODEL(S) !!!
                                        # (this is not necessarily the parent start date)
                                        # the ref_year for a scenario must be the same as for the historical
    #"branch_time_in_child" : "0.0D0",   # a double precision value in child time units (days),
                                        # This is an alternative to using "branch_year_in_child"
    
    #'parent_variant_label' :""  #Default to 'same variant as child'. Other cases should be exceptional
    #"parent_mip_era"       : 'CMIP5'   # only in special cases (as e.g. PMIP warm 
                                        # start from CMIP5/PMIP3 experiment)
    #'parent_source_id'     : 'CNRM-CM5.1' # only in special cases, where parent model 
                                           # is not the same model
    #
    "sub_experiment_id"    : "None", # Optional, default is 'none'; example : s1960. 
    "sub_experiment"       : "None", # Optional, default in 'none'
    "history"              : "None", #Used when a simulation is re-run, an output file is modified ...

    # A character string containing additional information about this simulation
    "comment"              : "",

    # You can specifically exclude some pairs (vars,tables), here in experiment settings
    # They wil be added to the lab-settings list of excluded pairs 
    # "excluded_pairs" : [ ('fbddtalk','Omon') ]

    # A per-variable dict of comments which are specific to this simulation. It will replace  
    # the all-simulation comment
    'comments'     : {
        'tas' : 'this is a dummy comment, placeholder for describing a special, simulation dependent, scheme for a given variable',
        },
    # We can supersede the default list of variables of lab_settings, which tells
    # which additionnal variables/frequecny are to produce
    #"listof_home_vars":"../../cnrm/home_vars_historical.txt",

    # If we use extra tables, we can here supersede the value set it in lab settings
    #'path_extra_tables'=

    # If the CMIP6 Controlled Vocabulary doesn't allow all the components you activate, you can set
    # next toggle to True
    'bypass_CV_components' : False,
    
    # What is the maximum duration of data period in a single file, for this experiment (integer, in years)
    "max_split_freq"          : None,
    
    'unused_contexts'    : [  ]        # If you havn't set a 'configuration', you may fine tune here 
}

#def hasCMORVarName(hmvar):
#    for cmvar in dq.coll['CMORvar'].items:
#        if (cmvar.label==hmvar.label): return True

def RequestItem_applies_for_exp_and_year(ri,experiment,lset,sset,year=None,debug=False):
    """ 
    Returns True if requestItem 'ri' in data request 'dq' (global) is relevant 
    for a given 'experiment' and 'year'. Toggle 'debug' allow some printouts 
    """
    # Returns a couple : relevant, endyear.
    # RELEVANT is True if requestItem RI applies to EXPERIMENT and
    #   has a timeslice wich includes YEAR, either implicitly or explicitly
    # ENDYEAR is meaningful if RELEVANT is True, and is the
    #   last year in the timeslice (or None if timeslice ==
    #   the whole experiment duration)

    # Acces experiment or experiment group for the RequestItem
    #if (ri.label=='C4mipC4mipLandt2') : debug=True
    if (debug) : print "In RIapplies.. Checking ","% 15s"%ri.title,
    item_exp=dq.inx.uid[ri.esid]
    ri_applies_to_experiment=False
    endyear=None
    # esid can link to an experiment or an experiment group
    if item_exp._h.label== 'experiment' :
        if (debug) : print "%20s"%"Simple Expt case", item_exp.label,
        if item_exp.label==experiment : 
            if (debug) : print " OK",
            ri_applies_to_experiment=True
    elif item_exp._h.label== 'exptgroup' :
        if (debug)  : print "%20s"%"Expt Group case ",item_exp.label,
        exps_id=dq.inx.iref_by_sect[ri.esid].a['experiment']
        for e in [ dq.inx.uid[eid] for eid in exps_id ] :
            if e.label==experiment : 
                if (debug) :  print " OK for experiment based on group"+\
                   item_exp.label,
                ri_applies_to_experiment=True
    elif item_exp._h.label== 'mip' :
        if (debug)  : print "%20s"%"Mip case ",dq.inx.uid[item_exp.label].label,
        exps_id=dq.inx.iref_by_sect[ri.esid].a['experiment']
        for e in [ dq.inx.uid[eid] for eid in exps_id ] :
            if (debug) :  print e.label,",",
            if e.label==experiment : 
                if (debug) :  print " OK for experiment based on mip"+ item_exp.label,
                ri_applies_to_experiment=True
    else :
        if (debug)  :
            print "Error on esid link for ri : %s uid=%s %s"%\
                           ( ri.title, ri.uid, item_exp._h.label)
    #print "ri=%s"%ri.title,
    #if year is not None :
    #    print "Filtering for year %d"%year
    if lset.get('filter_on_realization',True) :
        if ri.nenmax != -1 and (sset["realization_index"] > ri.nenmax) :
            ri_applies_to_experiment = False
    
    if ri_applies_to_experiment :
        if year is None :
            rep=True ; endyear=None
            if (debug) : print " ..applies because arg year is None"
        else :
            exp=dq.inx.uid[dq.inx.experiment.label[experiment][0]]
            rep,endyear=year_in_ri(ri,exp,lset,sset,year,debug=debug)
            if (debug) : print " ..year in ri returns :",rep,endyear
            #if (ri.label=="AerchemmipAermonthly3d") :
            #    print "reqItem=%s,experiment=%s,year=%d,rep=%s,"%(ri.label,experiment,year,rep)
        #print " rep=",rep
        return rep,endyear
    else :
        #print
        return False,None


def year_in_ri(ri,exp,lset,sset,year,debug=False):
    if ri.label=="CfmipCf3hrSimNew" :
        return (year==2008),2008
    if "HighResMIP, HighResMIP-6hrPlevExtr, amip" in ri.title:
        return True,2018
    if 'tslice' in ri.__dict__ :
        if (debug) : print "calling year_in_ri_tslice"
        rep,endyear=year_in_ri_tslice(ri,exp,sset,lset,year,debug=debug)
        return rep,endyear
    try :
        ny=int(ri.nymax)
    except:
        print "Warning : Cannot tell if reqItem %s applies to year %d  (ny=%s) -> assumes yes"%(ri.title,year,`ny`)
        return True,None
    # 
    # From now, this the case of a RequestItem which starts from experiment's start
    actual_first_year=experiment_start_year(exp,sset)  # The start year, possibly fixed by the user
    actual_end_year  =experiment_end_year(exp,sset)  # = the end year requested by the user if any
    DR_first_year    =experiment_start_year(exp,False,debug=debug)  
    DR_end_year      =experiment_end_year(exp,False)  
    if debug : print "year_in_ri : start DR : %s actual : %s | end DR : %s actual : %s | ny=%d"%\
       (DR_first_year,actual_first_year, DR_end_year ,actual_end_year,ny)
    #
    ri_is_for_all_experiment=False
    if (ny <= 0) :
        ri_is_for_all_experiment=True
        if debug : print "year_in_ri : RI applies systematically"
    else :
        if DR_first_year and DR_end_year and ny==(DR_end_year - DR_first_year +1):
            ri_is_for_all_experiment=True
            if debug : print "year_in_ri : RI applies because ny=end-start"
    if ri_is_for_all_experiment : return True,None
    #
    # From now, we know that requestItem duration is less than experiment duration
    # We may have errors in requestItem duration ny, because of an error in DR for start year
    # So, we add to ny the difference between DR and actual start_years, if the DR value is meaningful
    if DR_first_year  :
        ny += DR_first_year - actual_first_year  # Will be 0 if end is defined in DR and not by the user
        if debug and actual_first_year != DR_first_year :
            print "year_in_ri : compensating ny for diff in first year"
    RI_end_year=actual_first_year+ny-1
    # For these kind of requestItem of limited duration, no need to extend it, whatever the actual end date
    applies=(year <= RI_end_year)
    if debug : print "year_in_ri : returning ",applies,RI_end_year
    return applies,RI_end_year
    
def experiment_start_year(exp,sset=None,debug=False):
    if sset and "branch_year_in_child" in sset :
        return sset["branch_year_in_child"]
    else:
        try:
            return int(float(exp.starty))
        except:
            if sset is False :
                if debug : print "start_year : starty=",exp.starty
                return None
            form="Cannot guess first year for experiment %s : DR says :'%s' "
            if sset :
                form += "and 'branch_year_in_child' is not provided in experiment's settings"
            raise dr2xml_error(form%(exp.label,exp.starty))
        
        
def experiment_end_year(exp,sset=None):
    if sset and "end_year" in sset :
        return sset["end_year"]
    else:
        try: return int(float(exp.endy))
        except: return None
        
        
def year_in_ri_tslice(ri,exp,sset,lset,year,debug=False):
    # Returns a couple : relevant, endyear.
    # RELEVANT is True if requestItem RI applies to
    #   YEAR, either implicitly or explicitly (e.g. timeslice)
    # ENDYEAR, which is meaningful if RELEVANT is True, and is the
    #   last year in the timeslice (or None if timeslice ==
    #   the whole experiment duration)
    if 'tslice' not in ri.__dict__ :
        if (debug)  : print "No tslice for reqItem %s -> OK for any year"%ri.title
        return True, None
    if ri.tslice == '__unset__' :
        if (debug) : print "tslice is unset for reqItem %s "%ri.title
        return True, None
    #
    relevant=False
    endyear=None
    tslice=dq.inx.uid[ri.tslice]
    if (debug) :
        print "tslice label/type is %s/%s for reqItem %s "%(tslice.label,tslice.type,ri.title)
    if tslice.type=="simpleRange" : # e.g. _slice_DAMIP20
        if tslice.start < 1800 :
        # to manage _slice_abrupt*
            first_year=experiment_start_year(exp,sset)
            #first_year=sset["branch_year_in_child"]
            relevant = (year >= tslice.start + first_year - 1 and year <= tslice.end + first_year - 1)
            endyear = first_year + tslice.end - 1
        else :
            relevant = (year >= tslice.start and year<=tslice.end)
            endyear=tslice.end
    elif tslice.type=="sliceList": # e.g. _slice_DAMIP40
        for start in range(tslice.start,int(tslice.end-tslice.sliceLen+2),int(tslice.step)) :
            if year >= start and year < start+tslice.sliceLen :
                relevant = True
                endyear=start+tslice.sliceLen-1
    elif tslice.type=="dayList": # e.g. _slice_RFMIP2
        # e.g. startList[i]: [1980, 1, 1, 1980, 4, 1, 1980, 7, 1, 1980, 10, 1, 1992, 1, 1, 1992, 4, 1]
        years= [ tslice.startList[3*i] for i in range(len(tslice.startList)/3)]
        if year in years :
            relevant=True
            endyear=year
    elif tslice.type=="startRange": # e.g. _slice_VolMIP3
        # used only for VolMIP : _slice_VolMIP3 
        start_year=experiment_start_year(exp,sset)
        relevant= (year >= start_year and year < start_year+nyear)
        endyear=start_year + nyear - 1
    elif tslice.type=="monthlyClimatology": # e.g. _slice_clim20
        relevant = (year >= tslice.start and year<=tslice.end)
        endyear=tslice.end
    elif tslice.type=="branchedYears" : # e.g. _slice_piControl020
        source,source_type=get_source_id_and_type(sset,lset)
        if tslice.child in lset["branching"][source] :
            endyear=False
            (refyear,starts)=lset["branching"][source][tslice.child]
            for start in starts :
                if ((year - start >= tslice.start - refyear) and \
                    (year - start < tslice.start - refyear + tslice.nyears )):
                    relevant=True
                    lastyear=start+tslice.nyears-1
                    if endyear is False : endyear=lastyear
                    else : endyear=max(endyear,lastyear)
        else : raise dr2xml_error("For tslice %s, child %s start year is not documented"%\
                                (tslice.title, tslice.child))
    else :
        raise dr2xml_error("type %s for time slice %s is not handled"%(tslice.type,tslice.title))
    if (debug) :
        print "for year %d and experiment %s, relevant is %s for tslice %s of type %s, endyear=%s"%\
            (year,exp.label,`relevant`,ri.title,tslice.type,`endyear`)
    return relevant,endyear


def select_CMORvars_for_lab(lset, sset=None, year=None,printout=False):
    """
    A function to list CMOR variables relevant for a lab (and also, 
    optionnally for an experiment and a year)
    
    Args:
      lset (dict): laboratory settings; used to provide the list of MIPS,  
                   the max Tier, and a list of excluded variable names
      sset (dict): simulation settings, used for indicating source_type, 
                   max priority (and for filtering on the simulation)
                   If sset is None, use union of mips among all grid choices 
      year (int,optional) : simulation year - used when sset is not None, 
                   to additionally filter on year

    Returns:
      A list of 'simplified CMOR variables'
    
    """
    #
    debug=False
    # From MIPS set to Request links
    global sc,global_rls,grid_choice,rls_for_all_experiments
    if sset and 'tierMax' in sset : tierMax=sset['tierMax']
    else: tierMax=lset['tierMax']
    if sc is None :
        sc = dreqQuery(dq=dq, tierMax=tierMax)

    # Set sizes for lab settings, if available (or use CNRM-CM6-1 defaults)
    mcfg = collections.namedtuple( 'mcfg', \
                ['nho','nlo','nha','nla','nlas','nls','nh1'] )
    if sset : 
        source,source_type=get_source_id_and_type(sset,lset)
        grid_choice=lset["grid_choice"][source]
        mips_list=set(lset['mips'][grid_choice])
        sizes=lset["sizes"][grid_choice] #sizes=lset.get("sizes",[259200,60,64800,40,20,5,100])
        sc.mcfg = mcfg._make( sizes )._asdict()
    else :
        mips_list= set()
        for grid in lset['mips']  : mips_list=mips_list.union(set(lset['mips'][grid]))
        grid_choice="LR"
    #
    if rls_for_all_experiments is None :
        rls_for_mips=sc.getRequestLinkByMip(mips_list)
        if printout :
            print "Number of Request Links which apply to MIPS",
            print mips_list," is: ", len(rls_for_mips)
        #
        excluded_rls=[]
        for rl in rls_for_mips :
            if rl.label in lset.get("excluded_request_links",[]) :
                excluded_rls.append(rl)
        for rl in excluded_rls : rls_for_mips.remove(rl)
        if printout :
            print "Number of Request Links after filtering by excluded_request_links is: ", len(rls_for_mips)
        #
        excluded_rls=[]
        inclinks=lset.get("included_request_links",[])
        if len(inclinks) > 0 :
            for rl in rls_for_mips :
                if rl.label not in inclinks : excluded_rls.append(rl)
            for rl in excluded_rls :
                print "RequestLink %s is not included"%rl.label
                rls_for_mips.remove(rl)
        if printout :
            print "Number of Request Links after filtering by included_request_links is: ", len(rls_for_mips)
        rls_for_all_experiments=[ rl for rl in rls_for_mips ]
    else:
        rls_for_mips=rls_for_all_experiments
    #
    if sset  :
        experiment_id=sset['experiment_id']
        exp=dq.inx.uid[dq.inx.experiment.label[experiment_id][0]]
        if printout : print "Filtering for experiment %s, covering years [ %s , %s ] in DR"%\
           (experiment_id,exp.starty,exp.endy)
        #print "Request links before filter :"+`[ rl.label for rl in rls_for_mips ]`
        filtered_rls=[]
        for rl in rls_for_mips :
            # Access all requesItems ids which refer to this RequestLink
            ri_ids=dq.inx.iref_by_sect[rl.uid].a['requestItem']
            for ri_id in ri_ids :
                ri=dq.inx.uid[ri_id]
                #debug=(ri.label=='C4mipC4mipLandt2')
                if debug : print "Checking requestItem ",ri.title,
                applies,endyear= RequestItem_applies_for_exp_and_year(ri,
                                       experiment_id, lset,sset,year,debug)
                if applies:
                    if debug : print " applies "
                    filtered_rls.append(rl)
                else :
                    if debug : print " does not apply "

        rls=filtered_rls
        if printout :
            print "Number of Request Links which apply to experiment ", \
                experiment_id," member ", sset['realization_index']," and MIPs", mips_list ," is: ",len(rls)
        #print "Request links that apply :"+`[ rl.label for rl in filtered_rls ]`
    else :
        rls=rls_for_mips

    global_rls=rls
       
    # From Request links to CMOR vars + grid
    #miprl_ids=[ rl.uid for rl in rls ]
    #miprl_vars=sc.varsByRql(miprl_ids, pmax=lset['max_priority'])
    if sset and 'max_priority' in sset :
        pmax=sset['max_priority']
    else :
        pmax=lset['max_priority']
    miprl_vars_grids=[]
    for rl in rls :
        if debug :
            print "processing RequestLink %s"%rl.title
        rl_vars=sc.varsByRql([rl.uid], pmax=pmax)
        for v in rl_vars :
            # The requested grid is given by the RequestLink except if spatial shape matches S-*
            gr=rl.grid
            cmvar=dq.inx.uid[v]
            st=dq.inx.uid[cmvar.stid]
            sp=dq.inx.uid[st.spid]
            if sp.label[0:2]=="S-" : gr='cfsites'
            if (v,gr) not in miprl_vars_grids :
                miprl_vars_grids.append((v,gr))
                #if 'ua' in cmvar.label : print "adding %s %s"%(cmvar.label,dq.inx.uid[cmvar.vid].label)
            #else:
            #    print "Duplicate pair var/grid : ",cmvar.label,cmvar.mipTable,gr
    if printout :
        print 'Number of (CMOR variable, grid) pairs for these requestLinks is :%s'%len(miprl_vars_grids)

    #for (v,g) in miprl_vars_grids :
    #    if dq.inx.uid[v].label=="ps" : print "step 1 : ps in table",dq.inx.uid[v].mipTable,g

    #
    inctab=lset.get("included_tables",[])
    exctab=lset.get("excluded_tables",[])
    if sset : exctab.extend(sset.get("excluded_tables",[]))
    incvars=lset.get('included_vars',[])
    excvars=lset.get('excluded_vars',[])
    if sset : 
        excvars_for_expes=sset.get('excluded_vars',[])
        excvars.extend(excvars_for_expes)
    
    excpairs=lset.get('excluded_pairs',[])
    if sset :
        config=sset['configuration']
        if ('excluded_vars_per_config' in lset) and \
           (config in lset['excluded_vars_per_config']):
            excvars.extend(lset['excluded_vars_per_config'][config])
        excpairs.extend(sset.get('excluded_pairs',[]))
    
    filtered_vars=[]
    for (v,g) in miprl_vars_grids : 
        cmvar=dq.inx.uid[v]
        ttable=dq.inx.uid[cmvar.mtid]
        mipvar=dq.inx.uid[cmvar.vid]
        if ((len(incvars) == 0 and mipvar.label not in excvars) or\
            (len(incvars) > 0 and mipvar.label in incvars))\
            and \
           ((len(inctab)>0 and ttable.label in inctab) or \
            (len(inctab)==0 and ttable.label not in exctab))\
            and \
            ((mipvar.label,ttable.label) not in excpairs) :
             filtered_vars.append((v,g))
             if debug :
                 print "adding var %s, grid=%s, ttable=%s="%(cmvar.label,g,ttable.label) #,exctab,excvars
        else:
            #if (ttable.label=="Ofx") : print "discarding var %s, ttable=%s, exctab="%(cmvar.label,ttable.label),exctab
            pass

    if printout :
        print 'Number once filtered by excluded/included vars and tables and spatial shapes is : %s'%len(filtered_vars)

    # Filter the list of grids requested for each variable based on lab policy
    d=dict()
    for (v,g) in filtered_vars :
        if v not in d : d[v]=set()
        d[v].add(g)
    if printout :
        print 'Number of distinct CMOR variables (whatever the grid) : %d'%len(d)
    multiple_grids=[]
    for v in d:
        d[v]=decide_for_grids(v,d[v],lset,dq)
        if printout and len(d[v]) > 1 :
            multiple_grids.append(dq.inx.uid[v].label)
            if print_multiple_grids :
                print "\tVariable %s will be processed with multiple grids : %s"%(dq.inx.uid[v].label,`d[v]`)
    if not print_multiple_grids :
        if printout : 
            multiple_grids.sort()
            if len(multiple_grids)>0 :
                print "\tThese variables will be processed with multiple grids "+\
                "(rerun with print_multiple_grids set to True for details) :"+`multiple_grids`
    #
    # Print a count of distinct var labels
    if printout :
        varlabels=set()
        for v in d : varlabels.add(dq.inx.uid[v].label)
        print 'Number of distinct var labels is :',len(varlabels)

    # Translate CMORvars to a list of simplified CMORvar objects
    simplified_vars = []
    allow_pseudo=lset.get('allow_pseudo_standard_names',False)
    for v in d :
        svar = simple_CMORvar()
        cmvar = dq.inx.uid[v]
        complement_svar_using_cmorvar(svar,cmvar,dq,sn_issues,[],allow_pseudo)
        svar.Priority=analyze_priority(cmvar,mips_list)
        svar.grids=d[v]
        if debug :
            if "tas" == dq.inx.uid[v].label :
                print "When complementing, tas is included , grids are %s"%svar.grids
        simplified_vars.append(svar)
    if printout : print 'Number of simplified vars is :',len(simplified_vars)
    if printout :
        print "Issues with standard names are :",
        lissues=sn_issues.keys()
        lissues.sort()
        print lissues
    
    return simplified_vars

def analyze_priority(cmvar,lmips):
    """ 
    Returns the max priority of the CMOR variable, for a set of mips
    """
    prio=cmvar.defaultPriority
    rv_ids=dq.inx.iref_by_sect[cmvar.uid].a['requestVar']
    for rv_id in rv_ids :
        rv=dq.inx.uid[rv_id]
        vg=dq.inx.uid[rv.vgid]
        if vg.mip in lmips :
            if rv.priority < prio : prio=rv.priority
    return prio
                     
def wr(out,key,dic_or_val=None,num_type="string",default=None) :
    global print_wrv
    if not print_wrv : return 
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
    val=None
    if type(dic_or_val)==type({}) :  
        if key in dic_or_val : val=dic_or_val[key]
        else : 
            if default is not None :
                if default is not False : val=default
            else :                 
                print 'error : %s not in dic and default is None'%key
    else : 
        if dic_or_val is not None : val=dic_or_val
        else :
            print 'error in wr,  no value provided for %s'%key
    if val :
        if num_type == "string" :
            #val=val.replace(">","&gt").replace("<","&lt").replace("&","&amp").replace("'","&apos").replace('"',"&quot").strip()
            val=val.replace(">","&gt").replace("<","&lt").strip()
            #CMIP6 spec : no more than 1024 char
            val=val[0:1024]
        if num_type != "string" or len(val) > 0 :
            out.write('  <variable name="%s"  type="%s" > %s '%(key,num_type,val))
            out.write('  </variable>\n')

def freq2datefmt(in_freq,operation,lset):
    # WIP doc v6.2.3 - Apr. 2017: <time_range> format is frequency-dependant 
    datefmt=False
    offset=None
    freq=in_freq
    if freq == "dec" or freq == "10y":
        if not any( "dec" in f for f in lset.get("too_long_periods",[])) :
            datefmt="%y"
            if operation in ["average","minimum","maximum"] : offset="5y"
            else : offset="10y"
        else : freq="yr" #Ensure dates in filenames are consistent with content, even if not as required
    if freq == "yr" or freq == "yrPt" or freq == "1y":
        if not any( "yr" in f for f in lset.get("too_long_periods",[])) :
            datefmt="%y"
            if operation in ["average","minimum","maximum"] : offset=False
            else : offset="1y"
        else : freq="mon" #Ensure dates in filenames are consistent with content, even if not as required
    if freq in ["mon","monC","monPt", "1mo"]:
        datefmt="%y%mo"
        if operation in ["average","minimum","maximum"] : offset=False
        else : offset="1mo"
    elif freq=="day" or freq=="1d":
        datefmt="%y%mo%d"
        if operation in ["average","minimum","maximum"] : offset="12h"
        else : offset="1d"
    elif freq=="10day" or freq=="10d":
        datefmt="%y%mo%d"
        if operation in ["average","minimum","maximum"] : offset="30h"
        else : offset="2.5d"
    elif freq=="5day" or freq=="5d":
        datefmt="%y%mo%d"
        if operation in ["average","minimum","maximum"] : offset="60h"
        else : offset="5d"
    elif freq in ["6hr","6hrPt","3hr","3hrPt","3hrClim","1hr","1hrPt","hr","6h", "3h", "1h"]: 
        datefmt="%y%mo%d%h%mi"
        if freq=="6hr" or freq=="6hrPt" or freq=="6h":
            if operation in ["average","minimum","maximum"] : offset="3h"
            else : offset="6h"
        elif freq in [ "3hr", "3hrPt", "3hrClim","3h"] :
            if operation in ["average","minimum","maximum"] : offset="90mi"
            else : offset="3h"
        elif freq in ["1hr","1h", "hr", "1hrPt"]: 
            if operation in ["average","minimum","maximum"] : offset="30mi"
            else : offset="1h"
    elif freq in ["1hrClimMon" , "1hrCM" ]: 
        return "%y%mo%d%h%mi","0s","0s"
        offset="0s"
    elif freq=="subhr" or freq=="subhrPt" or freq=="1ts":
        datefmt="%y%mo%d%h%mi%s"
        # assume that 'subhr' means every timestep
        if operation in ["average","minimum","maximum"] :
            # Does it make sense ??
            offset="0.5ts"
        else : offset="1ts"
    elif "fx" in freq :
        pass ## WIP doc v6.2.3 - Apr. 2017: if frequency="fx", [_<time_range>] is ommitted
    if offset is not None:
        if operation in ["average","minimum","maximum"] :
            if offset is not False : offset_end="-"+offset
            else: offset_end=False
        else : offset_end="0s"
    else:
        offset="0s"; offset_end="0s"
        if not "fx" in freq :
            raise dr2xml_error("Cannot compute offsets for freq=%s and operation=%s"%(freq,operation))
    return datefmt,offset,offset_end

def write_xios_file_def(sv,year,table,lset,sset,out,cvspath,
                        field_defs,axis_defs,grid_defs,domain_defs,scalar_defs,file_defs,
                        dummies,skipped_vars_per_table,actually_written_vars,
                        prefix,context,grid,pingvars=None,enddate=None,
                        attributes=[],debug=[]) :
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
    global sc #,nlonz
    # If list of included vars has size 1, activate debug on the corresponding variable
    inc=lset.get('included_vars',[])
    if len(inc)==1 : debug=inc
    
    # gestion des attributs pour lesquels on a recupere des chaines vides (" " est Faux mais est ecrit " "")
    #--------------------------------------------------------------------
    # Put a warning for field attributes that shouldn't be empty strings
    #--------------------------------------------------------------------
    #if not sv.stdname       : sv.stdname       = "missing" #"empty in DR "+dq.version
    if not sv.long_name     : sv.long_name     = "empty in DR "+dq.version
    #if not sv.cell_methods  : sv.cell_methods  = "empty in DR "+dq.version
    #if not sv.cell_measures : sv.cell_measures = "cell measure is not specified in DR "+dq.version
    if not sv.units      : sv.units      = "empty in DR "+dq.version

    #--------------------------------------------------------------------
    # Define alias for field_ref in file-def file 
    # - may be replaced by alias1 later
    # - this is not necessarily the alias used in ping file because of
    #   intermediate field id(s) due to union/zoom
    #--------------------------------------------------------------------
    # We use a simple convention for variable names in ping files : 
    if sv.type=='perso' : alias=sv.label
    else:
        # MPM : si on a defini un label non ambigu alors on l'utilise comme alias (i.e. le field_ref) 
        # et pour l'alias seulement (le nom de variable dans le nom de fichier restant svar.label)
        if sv.label_non_ambiguous: alias=lset["ping_variables_prefix"]+sv.label_non_ambiguous
        else:
            # 'tau' is ambiguous in DR 01.00.18 : either a variable name (stress)
            # or a dimension name (optical thickness). We choose to rename the stress
            if sv.label != "tau" :
                alias=lset["ping_variables_prefix"]+sv.label
            else:
                alias=lset["ping_variables_prefix"]+"tau_stress"
        if (sv.label in debug) : print "write_xios_file_def ... processing %s, alias=%s"%(sv.label,alias)
        
        # suppression des terminaisons en "Clim" pour l'alias : elles concernent uniquement les cas
        # d'absence de variation inter-annuelle sur les GHG. Peut-etre genant pour IPSL ?
        # Du coup, les simus avec constance des GHG (picontrol) sont traitees comme celles avec variation
        split_alias=alias.split("Clim")
        alias=split_alias[0]
        if pingvars is not None :
            # Get alias without pressure_suffix but possibly with area_suffix
            alias_ping=ping_alias(sv,lset,pingvars)
    #
    # process only variables in pingvars
    if not alias_ping in pingvars:
        #print "+++ =>>>>>>>>>>>", alias_ping, " ", sv.label
        table=sv.mipTable
        if table not in skipped_vars_per_table: skipped_vars_per_table[table]=[]
        skipped_vars_per_table[table].append(sv.label+"("+str(sv.Priority)+")")
        return
    #
    #--------------------------------------------------------------------
    # Set global CMOR file attributes
    #--------------------------------------------------------------------
    #
    project=sset.get('project',"CMIP6")
    source_id,source_type=get_source_id_and_type(sset,lset)
    experiment_id=sset['experiment_id']
    institution_id=lset['institution_id']
    #
    contact=sset.get('contact',lset.get('contact',None))
    #
    # Variant matters
    realization_index=sset.get('realization_index',1) 
    initialization_index=sset.get('initialization_index',1)
    physics_index=sset.get('physics_index',1)
    forcing_index=sset.get('forcing_index',1)
    variant_label="r%di%dp%df%d"%(realization_index,initialization_index,\
                                  physics_index,forcing_index)
    variant_info_warning=". Information provided by this attribute may in some cases be flawed. "+\
                         "Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute."
    #
    # WIP Draft 14 july 2016
    if 'mip_era' in lset : mip_era=lset['mip_era']
    else: mip_era=sv.mip_era
    #
    # WIP doc v 6.2.0 - dec 2016 
    # <variable_id>_<table_id>_<source_id>_<experiment_id >_<member_id>_<grid_label>[_<time_range>].nc
    member_id=variant_label
    sub_experiment_id=sset.get('sub_experiment_id','none')
    if sub_experiment_id != 'none': member_id = sub_experiment_id+"-"+member_id
    #
    #--------------------------------------------------------------------
    # Set grid info
    #--------------------------------------------------------------------
    if grid == "" :
        # either native or close-to-native
        grid_choice=lset['grid_choice'][source_id]
        grid_label,target_hgrid_id,zgrid_id,grid_resolution,grid_description=\
                lset['grids'][grid_choice][context]
    else:
        if grid == 'cfsites' :
            target_hgrid_id=cfsites_domain_id
            zgrid_id=None
        else:
            target_hgrid_id=lset["ping_variables_prefix"]+grid
            zgrid_id="TBD : Should create zonal grid for CMIP6 standard grid %s"%grid
        grid_label,grid_resolution,grid_description=DRgrid2gridatts(grid)
        

    if table[-1:] == "Z" : # e.g. 'AERmonZ','EmonZ', 'EdayZ'
        grid_label+="z"
        # Below : when reduction was done trough a two steps sum, we needed to divide afterwards
        # by the nmber of longitudes
        #
        # if lset.has_key("nb_longitudes_in_model") and lset["nb_longitudes_in_model"][context]:
        #     # Get from settings the name of Xios variable holding number of longitudes and set by model
        #     nlonz=lset["nb_longitudes_in_model"][context] # e.g.: nlonz="ndlon"
        # elif context_index.has_key(target_hgrid_id):
        #     # Get the number of longitudes from xml context_index
        #     # an integer if attribute of the target horizontal grid, declared in XMLs: nlonz=256
        #     nlonz=context_index[target_hgrid_id].attrib['ni_glo'] 
        # else: 
        #     raise dr2xml_error("Fatal: Cannot access the number of longitudes (ni_glo) for %s\
        #                 grid required for zonal means computation "%target_hgrid_id)
        # print ">>> DBG >>> nlonz=", nlonz

        
    if "Ant" in table : grid_label+="a"
    if "Gre" in table : grid_label+="g"
    #
    with open(cvspath+project+"_experiment_id.json","r") as json_fp :
        CMIP6_CV_version_metadata=json.loads(json_fp.read())['version_metadata']
        CMIP6_CV_latest_tag=CMIP6_CV_version_metadata.get('latest_tag_point','no more value in CMIP6_CV')
    #
    with open(cvspath+project+"_experiment_id.json","r") as json_fp :
        CMIP6_experiments=json.loads(json_fp.read())['experiment_id']
        if not CMIP6_experiments.has_key(sset['experiment_id']):
            raise dr2xml_error("Issue getting experiment description in CMIP6 CV for %20s"%sset['experiment_id'])
        expid=sset['experiment_id']
        expid_in_filename=sset.get('expid_in_filename',expid)
        if "_" in expid_in_filename:
            raise dr2xml_error("Cannot use character '_' in expid_in_filename (%s)"%expid_in_filename)
        exp_entry=CMIP6_experiments[expid]
        experiment=exp_entry['experiment']
        description=exp_entry['description']
        activity_id=lset.get('activity_id',exp_entry['activity_id'])
        parent_activity_id=lset.get('parent_activity_id',lset.get('activity_id',exp_entry['parent_activity_id']))
        parent_experiment_id=exp_entry['parent_experiment_id']
        required_components=exp_entry['required_model_components']#.split(" ")
        allowed_components=exp_entry['additional_allowed_model_components']#.split(" ")                                
    #
    # Check model components re. CV components
    actual_components=source_type.split(" ")
    ok=True
    for c in required_components :
        if c not in actual_components :
            ok=False
            print "Model component %s is required by CMIP6 CV for experiment %s and not present (present=%s)"%\
                (c,experiment_id,`actual_components`)
    for c in actual_components :
        if c not in allowed_components and c not in required_components :
            ok=False or sset.get('bypass_CV_components',False) 
            print "Warning: Model component %s is present but not required nor allowed (%s)"%\
                (c,`allowed_components` )
    if not ok : raise dr2xml_error("Issue with model components")
    #
    #--------------------------------------------------------------------
    # Set NetCDF output file name according to the DRS
    #--------------------------------------------------------------------
    #
    date_range="%start_date%-%end_date%" # XIOS syntax
    operation,detect_missing,foo = analyze_cell_time_method(sv.cell_methods,sv.label,table,printout=False)
    #print "--> ",sv.label, sv.frequency, table
    date_format,offset_begin,offset_end=freq2datefmt(sv.frequency,operation,lset)
    #
    if "fx" in sv.frequency:
        filename="%s%s_%s_%s_%s_%s_%s"%\
                   (prefix,sv.label,table,source_id,expid_in_filename, member_id,grid_label)
    else:
        varname_for_filename=sv.mipVarLabel
        if lset.get('use_cmorvar_label_in_filename',False) : varname_for_filename=sv.label
        # WIP doc v6.2.3 : a suffix "-clim" should be added if climatology
        #if False and "Clim" in sv.frequency: suffix="-clim"
        if sv.frequency in [ "1hrCM", "monC" ]: suffix="-clim"
        else: suffix=""
        filename="%s%s_%s_%s_%s_%s_%s_%s%s"%\
            (prefix,varname_for_filename,table,source_id,expid_in_filename,
             member_id,grid_label,date_range,suffix)
    #
    if 'mip_era' not in lset : 
        further_info_url="https://furtherinfo.es-doc.org/%s.%s.%s.%s.%s.%s"%(
            mip_era,institution_id,source_id,expid_in_filename,
            sub_experiment_id,variant_label)
    else:
        further_info_url=""
    #
    #--------------------------------------------------------------------
    # Compute XIOS split frequency
    #--------------------------------------------------------------------
    resolution=lset['grid_choice'][source_id]
    split_freq=split_frequency_for_variable(sv, lset, resolution, sc.mcfg, context)
    # Cap split_freq by setting max_split_freq (if expressed in years)
    if split_freq[-1]=='y' :
        max_split_freq=sset.get('max_split_freq',None)
        if max_split_freq is None: max_split_freq=lset.get('max_split_freq',None)
        if max_split_freq is not None:
            if max_split_freq[0:-1] != "y" :
                dr2xml_error("max_split_freq must end with an 'y' (%s)"%max_split_freq)
            split_freq="%dy"%min(int(max_split_freq[0:-1]),int(split_freq[0:-1]))
    #print "split_freq: %-25s %-10s %-8s"%(sv.label,sv.mipTable,split_freq)
    #
    #--------------------------------------------------------------------
    # Write XIOS file node:
    # including global CMOR file attributes
    #--------------------------------------------------------------------
    out.write(' <file id="%s_%s_%s" name="%s" '%(sv.label,table,grid_label,filename))
    freq=longest_possible_period(Cmip6Freq2XiosFreq[sv.frequency],lset.get("too_long_periods",[]))
    out.write(' output_freq="%s" '%freq)
    out.write(' append="true" ')
    out.write(' output_level="%d" '%lset.get("output_level",10))
    out.write(' compression_level="%d" '%lset.get("compression_level",0))
    if not "fx" in sv.frequency :
        out.write(' split_freq="%s" '%split_freq)
        out.write(' split_freq_format="%s" '%date_format)
        #
        # Modifiers for date parts of the filename, due to silly KT conventions. 
        if offset_begin is not False :
            out.write(' split_start_offset="%s" ' %offset_begin)
        if offset_end is not False  :
            out.write(' split_end_offset="%s" '%offset_end)
        lastyear=None
        # Try to get enddate for the CMOR variable from the DR
        if sv.cmvar is not None :
            #print "calling endyear_for... for %s, with year="%(sv.label), year
            lastyear=endyear_for_CMORvar(dq,sv.cmvar,expid,year,lset,sset,sv.label in debug)
            #print "lastyear=",lastyear," enddate=",enddate
        if lastyear is None or (enddate is not None and lastyear >= int(enddate[0:4]) ) :
            # DR doesn't specify an end date for that var, or a very late one
            if lset.get('dr2xml_manages_enddate',True) :
                # Use run end date as the latest possible date
                # enddate must be 20140101 , rather than 20131231
                if enddate is not None :
                    endyear=enddate[0:4]
                    endmonth=enddate[4:6]
                    endday=enddate[6:8]
                    out.write(' split_last_date="%s-%s-%s 00:00:00" '%(endyear,endmonth,endday))
                else :
                    out.write(' split_last_date=10000-01-01 00:00:00" ')
        else:
            # Use requestItems-based end date as the latest possible date when it is earlier than run end date
            if (sv.label in debug) :
                print "split_last_date year %d derived from DR for variable %s in table %s for year %d"%(lastyear,sv.label,table,year)
            endyear="%04s"%(lastyear+1)
            if lastyear < 1000 :
                dr2xml_error("split_last_date year %d derived from DR for variable %s in table %s for year %d does not make sense except maybe for paleo runs; please set the right value for 'end_year' in experiment's settings file"%(lastyear,sv.label,table,year))
            endmonth="01"
            endday="01"
            out.write(' split_last_date="%s-%s-%s 00:00:00" '%(endyear,endmonth,endday))
    #
    #out.write('timeseries="exclusive" >\n')
    out.write(' time_units="days" time_counter_name="time"')
    out.write(' time_counter="exclusive"')
    out.write(' time_stamp_name="creation_date" ')
    out.write(' time_stamp_format="%Y-%m-%dT%H:%M:%SZ"')
    out.write(' uuid_name="tracking_id" uuid_format="hdl:21.14100/%uuid%"')
    out.write(' convention_str="%s"'%conventions) 
    #out.write(' description="A %s result for experiment %s of %s"'%
    #            (lset['source_id'],sset['experiment_id'],sset.get('project',"CMIP6"))) 
    out.write(' >\n')
    #
    if type(activity_id)==type([]) :
        activity_idr=reduce(lambda x,y : x+" "+y, activity_id)
    else:
        activity_idr=activity_id
    wr(out,'activity_id',activity_idr)
    #
    if contact and contact is not "" : wr(out,'contact',contact) 
    wr(out,'data_specs_version',dq.version) 
    wr(out,'dr2xml_version',version)
    #
    wr(out,'experiment_id',expid_in_filename)
    if experiment_id == expid_in_filename :
        wr(out,'description',description)
        wr(out,'title',description)
        wr(out,'experiment',experiment)
    #
    # Fixing cell_measures is done in vars.py 
    #
    dynamic_comment=""
    if "seaIce" in sv.modeling_realm and 'areacella' in sv.cell_measures and sv.label != "siconca" : 
        dynamic_comment='. Due an error in DR01.00.21 and to technical constraints, this variable may have  attribute cell_measures set to area: areacella, while it actually is area: areacello'

    #
    # When remapping occurs to a regular grid -> CF does not ask for cell_measure
    # but CMIP6 do ask for it !
    # if grid_label[0:2]=='gr': sv.cell_measures=""
    # TBD : find a way to provide an areacella field for variables which are remapped to a 'CMIP6' grid such as '1deg'
    
    #
    # CF rule : if the file variable has a cell_measures attribute, and
    # the corresponding 'measure' variable is not included in the file, 
    # it must be quoted as external_variable
    external_variables=''
    if "area:" in sv.cell_measures :
        external_variables+=" "+re.sub(".*area: ([^ ]*).*",r'\1',sv.cell_measures)
    if "volume:" in sv.cell_measures :
        external_variables+=" "+re.sub(".*volume: ([^ ]*).*",r'\1',sv.cell_measures)
    if 'fx' in table : external_variables= "" 
    if external_variables : wr(out,'external_variables',external_variables)
    #
    #
    wr(out,'forcing_index',forcing_index,num_type="int") 
    wr(out,'frequency',sv.frequency)
    #
    if further_info_url : wr(out,'further_info_url',further_info_url)
    #
    wr(out,'grid',grid_description) ; wr(out,'grid_label',grid_label) ;
    wr(out,'nominal_resolution',grid_resolution)
    comment=lset.get('comment','')+" "+sset.get('comment','')+dynamic_comment
    wr(out,'comment',comment) 
    wr(out,'history',sset,default='none') 
    wr(out,"initialization_index",initialization_index,num_type="int")
    wr(out,"institution_id",institution_id)
    if "institution" in lset :
        inst=lset['institution']
    else:
        with open(cvspath+project+"_institution_id.json","r") as json_fp :
            try:
                inst=json.loads(json_fp.read())['institution_id'][institution_id]
            except :
                raise dr2xml_error("Fatal: Institution_id for %s not found "+\
                        "in CMIP6_CV at %s"%(institution,cvspath))
    wr(out,"institution",inst)
    #
    with open(cvspath+project+"_license.json","r") as json_fp :
        license=json.loads(json_fp.read())['license'][0]
    # mpmoine_cmor_update: 'licence' est trop long... passe pas le CMIP6-Checker => 'institution_id' au lieu de inst='institution'
    license=license.replace("<Your Centre Name>",institution_id)
    license=license.replace("[NonCommercial-]","NonCommercial-")
    license=license.replace("[ and at <some URL maintained by modeling group>]",
                            " and at "+lset["info_url"])
    wr(out,"license",license)
    wr(out,'mip_era',mip_era)
    #
    if parent_experiment_id and parent_experiment_id != 'no parent' and parent_experiment_id != ['no parent']:
        wr(out,'parent_experiment_id',reduce(lambda x,y : x+" "+y, parent_experiment_id))
        wr(out,'parent_mip_era',sset,default=mip_era)
        wr(out,'parent_activity_id',reduce(lambda x,y : x+" "+y, parent_activity_id))
        wr(out,'parent_source_id',sset,default=source_id)
        # TBD : syntaxe XIOS pour designer le time units de la simu courante
        parent_time_ref_year=sset.get('parent_time_ref_year',"1850")
        parent_time_units="days since %s-01-01 00:00:00"%parent_time_ref_year
        wr(out,'parent_time_units',sset,default=parent_time_units)
        wr(out,'parent_variant_label',sset,default=variant_label)
        wr(out,'branch_method',sset,default='standard')
        # Use branch year in parent if available
        if "branch_year_in_parent" in sset and source_id in lset['branching'] :
           if experiment_id in lset['branching'][source_id] and \
              sset["branch_year_in_parent"] not in lset['branching'][source_id][experiment_id][1] :
               dr2xml_error("branch_year_in_parent (%d) doesn't belong to the list of branch_years declared for this experiment %s"\
                            %(sset["branch_year_in_parent"],lset['branching'][source_id][experiment_id][1]))
           date_branch=datetime.datetime(sset["branch_year_in_parent"],sset.get("branch_month_in_parent",1),1)
           date_ref=datetime.datetime(int(parent_time_ref_year),1,1)
           nb_days=(date_branch-date_ref).days
           wr(out,'branch_time_in_parent',"%d.0D"%nb_days,"double") 
        else:
            wr(out,'branch_time_in_parent',sset,"double") 
        # Use branch year in child if available
        if "branch_year_in_parent" in sset :
           date_branch=datetime.datetime(sset["branch_year_in_child"],1,1)
           date_ref=datetime.datetime(sset["child_time_ref_year"],1,1)
           nb_days=(date_branch-date_ref).days
           wr(out,'branch_time_in_child',"%d.0D"%nb_days,"double") 
        else:
            wr(out,'branch_time_in_child',sset,"double")
    #
    wr(out,"physics_index",physics_index,num_type="int") 
    wr(out,'product','model-output')
    wr(out,"realization_index",realization_index,num_type="int")
    # Patch for an issue id DR01.0021 -> 01.00.24
    if sv.modeling_realm=="ocnBgChem" : sv.modeling_realm=="ocnBgchem" 
    wr(out,'realm',sv.modeling_realm)
    wr(out,'references',lset,default=False) 
    #
    try:
        with open(cvspath+project+"_source_id.json","r") as json_fp :
            sources=json.loads(json_fp.read())['source_id']
            source=make_source_string(sources,source_id)
    except :
        if "source" in lset : source=lset['source']
        else:
            raise dr2xml_error("Fatal: source for %s not found in CMIP6_CV at"+\
                               "%s, nor in lset"%(source_id,cvspath))
    wr(out,'source',source) 
    wr(out,'source_id',source_id)
    if type(source_type)==type([]) :
        source_type=reduce(lambda x,y : x+" "+y, source_type)
    wr(out,'source_type',source_type)
    #
    wr(out,'sub_experiment_id',sub_experiment_id) 
    wr(out,'sub_experiment',sset,default='none') 
    #
    wr(out,"table_id",table)
    #
    if 'expid_in_filename' not in sset :
        wr(out,"title","%s model output prepared for %s / "%(\
                        source_id,project)+activity_idr+" "+experiment_id)
    else:
        wr(out,"title","%s model output prepared for %s and "%(\
                        source_id,project)+activity_idr+" / "+expid_in_filename+" simulation")
    #
    wr(out,"variable_id",sv.mipVarLabel)
    #
    variant_info=sset.get('variant_info',"none")
    if variant_info!="none" and variant_info!="" : variant_info+=variant_info_warning
    if variant_info!="" : wr(out,"variant_info",variant_info)
    wr(out,"variant_label",variant_label)
    for name,value in attributes : wr(out,name,value)
    non_stand_att=lset.get("non_standard_attributes",dict())
    for name in non_stand_att : wr(out,name,non_stand_att[name])
    #
    #--------------------------------------------------------------------
    # Build all XIOS auxilliary elements (end_file_defs, field_defs, domain_defs, grid_defs, axis_defs)
    #---
    # Write XIOS field entry
    # including CF field attributes 
    #--------------------------------------------------------------------
    end_field=create_xios_aux_elmts_defs(sv,alias,table,lset,sset,
                               field_defs,axis_defs,grid_defs,domain_defs,scalar_defs,
                               dummies,context,target_hgrid_id,zgrid_id,pingvars)
    out.write(end_field)
    if sv.spatial_shp[0:4]=='XY-A' or sv.spatial_shp[0:3]=='S-A': # includes half-level cases
        # create a field_def entry for surface pressure 
        #print "Searching for ps for var %s, freq %s="%(alias,freq)
        sv_psol=get_simplevar(dq,"ps",table,sv.frequency)
        
        if sv_psol :
            #if not sv_psol.cell_measures : sv_psol.cell_measures = "cell measure is not specified in DR "+dq.version
            psol_field=create_xios_aux_elmts_defs(sv_psol,lset["ping_variables_prefix"]+"ps",table,lset,sset,
                                                  field_defs,axis_defs,grid_defs,domain_defs,scalar_defs,
                                       dummies,context,target_hgrid_id,zgrid_id,pingvars)
            out.write(psol_field)
        else:
            print "Warning: Cannot complement model levels with psol for variable %s and table %s"%\
                (sv.label,sv.frequency)


    #
    names={}
    if sv.spatial_shp=='XY-A' or sv.spatial_shp=='S-A':
        # add entries for auxilliary variables : ap, ap_bnds, b, b_bnds
        names={"ap": "vertical coordinate formula term: ap(k)",
               "ap_bnds": "vertical coordinate formula term: ap(k+1/2)",
               "b": "vertical coordinate formula term: b(k)",
               "b_bnds" : "vertical coordinate formula term: b(k+1/2)"  }
    if sv.spatial_shp=='XY-AH' or sv.spatial_shp=='S-AH':
        # add entries for auxilliary variables : ap, ap_bnds, b, b_bnds
        names={"ahp": "vertical coordinate formula term: ap(k)",
               "ahp_bnds": "vertical coordinate formula term: ap(k+1/2)",
               "bh": "vertical coordinate formula term: b(k)",
               "bh_bnds" : "vertical coordinate formula term: b(k+1/2)"  }
    for tab in names :
        out.write('\t<field field_ref="%s%s" name="%s" long_name="%s" operation="once" prec="8" />\n'%\
                  (lset["ping_variables_prefix"],tab,tab.replace('h',''),names[tab]))
    out.write('</file>\n\n')
    actually_written_vars.append((sv.label,sv.long_name,sv.mipTable,sv.frequency,sv.Priority,sv.spatial_shp))
    

def wrv(name, value, num_type="string"):
    global print_wrv
    if not print_wrv : return ""
    if type(value)==type("") : value=value[0:1024] #CMIP6 spec : no more than 1024 char
    # Format a 'variable' entry
    return '     <variable name="%s" type="%s" > %s '%(name,num_type,value)+\
        '</variable>\n'

def create_xios_aux_elmts_defs(sv,alias,table,lset,sset,
                               field_defs,axis_defs,grid_defs,domain_defs,scalar_defs,
                               dummies,context,target_hgrid_id,zgrid_id,pingvars) :
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
    #--------------------------------------------------------------------
    # Build XIOS axis elements (stored in axis_defs)
    # Proceed with vertical interpolation if needed
    #---
    # Build XIOS auxilliary field elements (stored in field_defs)
    #--------------------------------------------------------------------
    ssh=sv.spatial_shp
    prefix=lset["ping_variables_prefix"]

    # The id of the currently most downstream field is last_field_id
    last_field_id=alias 

    alias_ping=ping_alias(sv,lset,pingvars)
    grid_id_in_ping=id2gridid(alias_ping,context_index)
    last_grid_id=grid_id_in_ping
    #last_grid_id=None
    #
    grid_with_vertical_interpolation=None

    # translate 'outermost' time cell_methods to Xios 'operation')
    operation,detect_missing,clim = analyze_cell_time_method(sv.cell_methods,sv.label,table, printout=False)
    #
    #--------------------------------------------------------------------
    # Handle vertical interpolation, both XY-any and Y-P outputs
    #--------------------------------------------------------------------
    #
    #if ssh[0:4] in ['XY-H','XY-P'] or ssh[0:3] == 'Y-P' or \
    # must exclude COSP outputs which are already interpolated to height or P7 levels 
    if (ssh[0:4] == 'XY-P' and ssh != 'XY-P7') or \
       ssh[0:3] == 'Y-P' or \
       ((ssh[0:5]=='XY-na' or ssh[0:4]=='Y-na') and
        prefix+sv.label not in pingvars and sv.label_without_psuffix != sv.label ): #TBD check - last case is for singleton
        last_grid_id,last_field_id= process_vertical_interpolation(\
             sv,alias, lset,pingvars,last_grid_id,field_defs,axis_defs,grid_defs,domain_defs,table)

    #
    #--------------------------------------------------------------------
    # Handle the case of singleton dimensions
    #--------------------------------------------------------------------
    #
    if has_singleton(sv) :
        last_field_id,last_grid_id= process_singleton(sv,last_field_id,lset,pingvars,
                      field_defs,grid_defs,scalar_defs,table)
    #
    # TBD : handle explicitly the case of scalars (global means, shape na-na) : enforce <scalar name="sector" standard_name="region" label="global" >, or , better, remove the XIOS-generated scalar introduced by reduce_domain
    #
    #--------------------------------------------------------------------
    # Handle zonal means
    #--------------------------------------------------------------------
    #
    if ssh[0:2] == 'Y-' : #zonal mean and atm zonal mean on pressure levels
        last_field_id,last_grid_id=\
            process_zonal_mean(last_field_id,last_grid_id, target_hgrid_id,
                               zgrid_id, field_defs,axis_defs,grid_defs,
                               domain_defs, operation,sv.frequency,lset)

    #
    #--------------------------------------------------------------------
    # Build a construct for computing a climatology (if applicable)
    #--------------------------------------------------------------------
    if clim :
        if sv.frequency == "1hrCM" :
            last_field_id,last_grid_id=process_diurnal_cycle(last_field_id,\
                                                          field_defs,grid_defs,axis_defs)
        else :
            raise dr2xml_error("Cannot handle climatology cell_method for frequency %s and variable "%\
                               sv.frequency,sv.label)
    # 
    #--------------------------------------------------------------------
    # Create intermediate field_def for enforcing operation upstream
    #--------------------------------------------------------------------
    #
    but_last_field_id=last_field_id
    last_field_id=last_field_id+"_"+operation
    field_defs[last_field_id]='<field id="%-25s field_ref="%-25s operation="%-10s/>'\
                            %(last_field_id+'"',but_last_field_id+'"',operation+'"')
    #
    #--------------------------------------------------------------------
    # Change horizontal grid if requested 
    #--------------------------------------------------------------------
    #
    if target_hgrid_id :
        # This does not apply for a series of shapes 
        if ssh[0:2]=='Y-' or ssh=='na-na' or ssh=='TR-na' or ssh=='TRS-na' or ssh[0:3]=='YB-' or ssh=='na-A' :
            pass
        else:
            if target_hgrid_id==cfsites_domain_id : add_cfsites_in_defs(grid_defs,domain_defs)
            # Apply DR required remapping, either toward cfsites grid or a regular grid 
            last_grid_id=change_domain_in_grid(target_hgrid_id, grid_defs,lset,src_grid_id=last_grid_id)
    #
    #--------------------------------------------------------------------
    # Change axes in grid to CMIP6-compliant ones
    #--------------------------------------------------------------------
    #
    last_grid_id=change_axes_in_grid(last_grid_id, grid_defs,axis_defs,lset)
    #
    #--------------------------------------------------------------------
    # Create <field> construct to be inserted in a file_def, which includes re-griding
    #--------------------------------------------------------------------
    #
    if last_grid_id != grid_id_in_ping  : gref='grid_ref="%s"'% last_grid_id
    else : gref=""
  
    rep='  <field field_ref="%s" name="%s" %s '% (last_field_id,sv.mipVarLabel,gref)
    #
    # 
    #--------------------------------------------------------------------
    # Add offset if operation=instant for some specific variables defined in lab_settings
    #--------------------------------------------------------------------
    #
    if operation == 'instant' :
        for ts in lset.get('special_timestep_vars',[]) :
            if sv.label in lset['special_timestep_vars'][ts] :
                xios_freq = Cmip6Freq2XiosFreq[sv.frequency]
                # works only if units are different :
                rep += ' freq_offset="%s-%s"'%(xios_freq,ts) 
    #
    #--------------------------------------------------------------------
    # handle data type and missing value
    #--------------------------------------------------------------------
    #
    detect_missing="True"
    missing_value="1.e+20"
    if   sv.prec.strip() in ["float","real",""] : prec="4"
    elif sv.prec.strip() =="double"  : prec="8"
    elif sv.prec.strip() =="integer" or sv.prec.strip() =="int" :
        prec="2" ; missing_value="0" #16384"
    else :
        raise dr2xml_error("prec=%s for sv=%s"%(sv.prec,sv.label))
    rep+=' detect_missing_value="%s" \n\tdefault_value="%s" prec="%s"'%(detect_missing,missing_value,prec)
    #
    # TBD : implement DR recommendation for cell_method : The syntax is to append, in brackets,
    # TBD    'interval: *amount* *units*', for example 'area: time: mean (interval: 1 hr)'.
    # TBD    The units must be valid UDUNITS, e.g. day or hr.
    rep+=' cell_methods="%s" cell_methods_mode="overwrite"'% sv.cell_methods
    #--------------------------------------------------------------------
    # enforce time average before remapping (when there is one) except if there 
    # is an expr, set in ping for the ping variable of that field, and which 
    # involves time operation (using @)
    #--------------------------------------------------------------------
    if operation == 'once' : freq_op=""
    else : freq_op='freq_op="%s"'% longest_possible_period(Cmip6Freq2XiosFreq[sv.frequency],lset.get("too_long_periods",[]))
    #
    rep+=' operation="%s"'%operation
    if not idHasExprWithAt(alias,context_index) : 
        # either no expr, or expr without an @  ->
        # may use @ for optimizing operations order (average before re-gridding)
        if last_grid_id != grid_id_in_ping :
            if operation=='average' :
                # do use @ for optimizing :
                rep+=' %s>\n\t\t@%s'%(freq_op,last_field_id)
            elif operation=='instant':
                # must set freq_op (this souldn't be necessary, but is needed with Xios 1442)
                if lset.get("useAtForInstant",False):
                    rep+=' %s>\n\t\t@%s'%(freq_op,last_field_id)
                else: 
                    rep+=' %s>'%(freq_op)
            else:
                # covers only case once , already addressed by freq_op value='' ?
                rep+=' >'
        else :
            # No remap 
            rep+=' >'
    else: # field has an expr, with an @
        # Cannot optimize
        if operation == 'instant':
            # must reset expr (if any) if instant, for using arithm. operation defined in ping.
            # this allows that the type of operation applied is really 'instant', and not the one
            # that operands did inherit from ping_file
            rep+=' expr="_reset_"'
        if (operation=='average') :
            warnings_for_optimisation.append(alias)
        rep+=' %s>'%(freq_op)
    rep+='\n'
    #
    #--------------------------------------------------------------------
    # Add Xios variables for creating NetCDF attributes matching CMIP6 specs
    #--------------------------------------------------------------------
    comment=None
    # Process experiment-specific comment for the variable
    if sv.label in sset['comments'].keys() :
        comment=sset['comments'][sv.label] 
    else: # Process lab-specific comment for the variable
        if sv.label in lset['comments'].keys() : 
            comment=lset['comments'][sv.label] 
    if comment : rep+=wrv('comment',comment) #TBI 
    #
    if sv.stdname : rep+=wrv("standard_name",sv.stdname)
    #
    desc=sv.description
    #if desc : desc=desc.replace(">","&gt;").replace("<","&lt;").replace("&","&amp;").replace("'","&apos;").replace('"',"&quot;")
    if desc : desc=desc.replace(">","&gt;").replace("<","&lt;").strip()
    rep+=wrv("description",desc)
    #
    rep+=wrv("long_name",sv.long_name)
    if sv.positive != "None" and sv.positive != "" : rep+=wrv("positive",sv.positive) 
    rep+=wrv('history','none')
    if sv.units : rep+=wrv('units',sv.units)
    if sv.cell_methods  : rep+=wrv('cell_methods',sv.cell_methods)
    if sv.cell_measures : rep+=wrv('cell_measures',sv.cell_measures)
    #
    if sv.struct is not None :
        fmeanings=sv.struct.flag_meanings
        if fmeanings is not None and fmeanings.strip() != '' :
                    rep+=wrv('flag_meanings',fmeanings.strip())
        fvalues=sv.struct.flag_values
        if fvalues is not None and fvalues.strip() != '' :
                    rep+=wrv('flag_values',fvalues.strip())
    #
    # We override the Xios value for interval_operation because it sets it to
    # the freq_output value with our settings (for complicated reasons)
    if grid_with_vertical_interpolation :
        interval_op=lset["vertical_interpolation_sample_freq"]
    else:
        source,source_type=get_source_id_and_type(sset,lset)
        grid_choice=lset["grid_choice"][source]
        interval_op=`int(lset['sampling_timestep'][grid_choice][context])`+" s"
    if operation != 'once' :
        rep+=wrv('interval_operation',interval_op)

    # mpmoine_note: 'missing_value(s)' normalement plus necessaire, a verifier
    #TBS# rep+=wrv('missing_values',sv.missing,num_type="double")
    rep+='     </field>\n'
    #
    return rep

def is_singleton(sdim):
    if sdim.axis=='' :
        # Case of non-spatial dims. Singleton only have a 'value' (except Scatratio has a lot (in DR01.00.21))
        return sdim.value!= '' and len(sdim.value.strip().split(" ")) == 1
    else:
        # Case of space dimension singletons. Should a 'value' and no 'requested'
        return ((sdim.value!='') and (sdim.requested.strip()== '' )) \
            or (sdim.label=="typewetla") # The latter is a bug in DR01.00.21 : typewetla has no value tehre

def has_singleton(sv):
    rep=any([ is_singleton(sv.sdims[k]) for k in sv.sdims ])
    return rep


def process_singleton(sv,alias,lset,pingvars,
                      field_defs,grid_defs,scalar_defs,table):
    """
    Based on singleton dimensions of variable SV, and assuming that this/these dimension(s) 
    is/are not yet represented by a scalar Xios construct in corresponding field's grid, 
    creates a further field with such a grid, including creating the scalar and 
    re-using the domain of original grid

    """
    
    printout=False
    # get grid for the variable , before vertical interpo. if any
    # (could rather use last_grid_id and analyze if it has pressure dim)
    alias_ping=ping_alias(sv,lset,pingvars)
    input_grid_id=id2gridid(alias_ping,context_index)
    input_grid_def=get_grid_def(input_grid_id,grid_defs,lset)
    if printout:
        print "process_singleton : ","processing %s with grid %s "%(alias,input_grid_id)
    #
    further_field_id=alias
    further_grid_id=input_grid_id
    further_grid_def=input_grid_def
    #
    # for each sv's singleton dimension, create the scalar, add a scalar
    # construct in a further grid, and convert field to a further field
    for dimk in sv.sdims :
        sdim=sv.sdims[dimk]
        if is_singleton(sdim) : #Only one dim should match
            #
            # Create a scalar for singleton dimension
            # sdim.label is non-ambiguous id, thanks to the DR, but its value may be
            # ambiguous w.r.t. a dr2xml suffix for interpolating to a single pressure level
            scalar_id="Scal"+sdim.label 
            if sdim.units =='' : unit=''
            else  : unit=' unit="%s"'%sdim.units
            #
            if sdim.type=='character' :
                value=' label="%s"'%sdim.label
            else:
                value=' value="%s"'%sdim.value
                types={'double':' prec="8"','float':' prec="4"', 'integer':' prec="2"'}
                value=types[sdim.type]+" "+'value="%s"'%sdim.value
            if sdim.axis!='' :
                # Space axis, probably Z
                axis=' axis_type="%s"'%(sdim.axis)
                if sdim.positive : axis+=' positive="%s"'%(sdim.positive)
            else: axis=""
            if sdim.bounds=="yes":
                try :
                    bounds=sdim.boundsValues.split()
                    bounds_value=' bounds="(0,1)[ %s %s ]" bounds_name="%s_bounds"'%\
                        (bounds[0],bounds[1],sdim.out_name)
                except :
                    if sdim.label=="lambda550nm" : bounds_value=''
                    else : raise dr2xml_error("Issue for var %s with dim %s bounds=%s"%(sv.label,sdim.label,bounds))
            else:
                bounds_value=""
            #
            name=sdim.out_name
            # These dimensions are shared by some variables with another sdim with same out_name ('type'):
            if sdim.label in [ "typec3pft", "typec4pft" ] : name="pfttype"
            #
            if sdim.stdname.strip()=='' or sdim.label=="typewetla" : stdname=""
            else: stdname='standard_name="%s"'%sdim.stdname
            #
            scalar_def='<scalar id="%s" name="%s" %s long_name="%s"%s%s%s%s />'%\
                   (scalar_id,name,stdname,sdim.title,value,bounds_value,axis,unit)
            scalar_defs[scalar_id]=scalar_def
            if printout:
                print "process_singleton : ","adding scalar %s"%scalar_def
            #
            # Create a grid with added (or changed) scalar
            glabel=further_grid_id+"_"+scalar_id
            further_grid_def=add_scalar_in_grid(further_grid_def,glabel,scalar_id,\
                                                name,sdim.axis=="Z")
            if printout:
                print "process_singleton : "," adding grid %s"%further_grid_def
            grid_defs[glabel]=further_grid_def
            further_grid_id=glabel
            
    # Compare grid definition (in case the input_grid already had correct ref to scalars)
    if further_grid_def != input_grid_def :
        #  create derived_field through an Xios operation (apply all scalars at once)
        further_field_id=alias+"_"+further_grid_id.replace(input_grid_id+'_','')
        # Must init operation and detect_missing when there is no field ref 
        field_def='<field id="%s" grid_ref="%s" operation="instant" detect_missing_value="true" > %s </field>'%\
            (further_field_id,further_grid_id,alias)
        field_defs[further_field_id]=field_def
        if printout:
            print "process_singleton : "," adding field %s"%field_def
    return further_field_id,further_grid_id
    
def process_vertical_interpolation(sv,alias,lset,pingvars,src_grid_id,
                                   field_defs,axis_defs,grid_defs,domain_defs,table):
    """
    Based on vertical dimension of variable SV, creates the intermediate fields 
    for triggering vertical interpolation with the required levels; also includes 
    creating axes as necessary, and re-constructing a grid which combines the required 
    vertical dimension and the horizontal domain of variable's original grid

    Also includes creating an intermediate field for time-sampling before vertical interpolation

    Two flavors : using or not the vertical level union scheme (and if yes, create as
    vertical axis a zoom of the union axis)
    """
    #
    vdims=[ sd  for sd in sv.sdims.values() if isVertDim(sd) ]
    if len(vdims) == 1 : sd=vdims[0]
    elif len(vdims) > 1 : raise dr2xml_error("Too many vertical dims for %s (%s)"%(sv.label,`vdims`))
    if len(vdims)==0 :
        # Analyze if there is a singleton vertical dimension for the variable
        #sd=scalar_vertical_dimension(sv,dq)
        #if sd is not None :
        #    print "Single level %s for %s"%(sv,sv.label),vdims
        #else:
        raise dr2xml_error("Not enough vertical dims for %s (%s)"%(sv.label,[ (s.label,s.out_name) for s in sv.sdims.values()]))
    #
    #
    #sd=vdims[0]
    alias_with_levels=alias+"_"+sd.label   # e.g. 'CMIP6_hus7h_plev7h'
    if alias_with_levels in pingvars:
        print "No vertical interpolation for %s because the pingfile provides it"%alias_with_levels
        return src_grid_id,alias_with_levels
        #raise dr2xml_error("Finding an alias with levels (%s) in pingfile is unexpected")
    #
    prefix=lset["ping_variables_prefix"]
    lwps=sv.label_without_psuffix
    alias_in_ping=prefix+lwps      # e.g. 'CMIP6_hus' and not 'CMIP6_hus7h'; 'CMIP6_co2' and not 'CMIP6_co2Clim'
    if not alias_in_ping in pingvars:       # e.g. alias_in_ping='CMIP6_hus'
        raise dr2xml_error("Field id "+alias_in_ping+" expected in pingfile but not found.")
    #
    # Create field alias_for_sampling for enforcing the operation before time sampling
    operation=lset.get("vertical_interpolation_operation","instant")
    alias_for_sampling=alias_in_ping+"_with_"+operation 
    # <field id="CMIP6_hus_instant" field_ref="CMIP6_hus" operation="instant" />
    field_defs[alias_for_sampling]=\
               '<field id="%-25s field_ref="%-25s operation="%s" />'\
               %(alias_for_sampling+'"',alias_in_ping+'"',operation)
    #
    vert_freq=lset["vertical_interpolation_sample_freq"]
    #
    # Construct an axis for interpolating to this vertical dimension
    # e.g. for zoom_case :
    #    <axis id="zoom_plev7h_hus" axis_ref="union_plevs_hus"> <zoom_axis index="(0,6)[  3 6 11 13 15 20 28 ]"/>
    create_axis_def(sd,lset,axis_defs,field_defs)

    # Create field 'alias_sample' which time-samples the field at required freq
    # before vertical interpolation
    alias_sample=alias_in_ping+"_sampled_"+vert_freq # e.g.  CMIP6_zg_sampled_3h
    # <field id="CMIP6_hus_sampled_3h" field_ref="CMIP6_hus_instant" freq_op="3h" expr="@CMIP6_hus_instant"/>
    field_defs[alias_sample]=\
               '<field id="%-25s field_ref="%-25s freq_op="%-10s detect_missing_value="true" > @%s </field>'\
               %(alias_sample+'"',alias_for_sampling+'"',vert_freq+'"',alias_for_sampling)
    
    # Construct a field def for the vertically interpolated variable
    if sd.is_zoom_of: # cas d'une variable definie grace a 2 axis_def (union+zoom)
        
        # Construct a grid using variable's grid and target vertical axis
        # e.g. <grid id="FULL_klev_zoom_plev7h_hus"> <domain domain_ref="FULL" /> <axis axis_ref="zoom_plev7h_hus" />

        # cas d'une variable definie grace a 2 axes verticaux (zoom+union)
        # Must first create grid for levels union, e.g.:
        # <grid id="FULL_klev_union_plevs_hus"> <domain domain_ref="FULL" /> <axis axis_ref="union_plevs_hus" />
        grid_id=create_grid_def(grid_defs,axis_defs[sd.is_zoom_of],sd.out_name,src_grid_id)
        #
        union_alias=prefix+lwps+"_union" # e.g. 'CMIP6_hus_union'
	# Ss e.g.: <field id="CMIP6_hus_union" field_ref="CMIP6_hus_sampled_3h" grid_ref="FULL_klev_union_plevs_hus"/>
        field_defs[union_alias]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
            %(union_alias+'"',alias_sample+'"',grid_id+'"')
        
        # SS : first create grid for levels subset zoom, e.g.:
    	# <grid id="FULL_klev_zoom_plev7h_hus"> <domain domain_ref="FULL" /> <axis axis_ref="zoom_plev7h_hus" /
        # e.g. zoom_label : 'zoom_plev7h_hus'
        grid_id=create_grid_def(grid_defs,axis_defs[sd.zoom_label],sd.out_name,src_grid_id)
	# SS: e.g.: <field id="CMIP6_hus7h_plev7h" field_ref="CMIP6_hus_union" grid_ref="FULL_klev_zoom_plev7h_hus"
        field_defs[alias_with_levels]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
            %(alias_with_levels+'"',union_alias+'"',grid_id+'"')
        
    else: # cas d'une variable definie grace a seul axis_def (non union+zoom)
        # Construct a grid using variable's grid and target vertical axis
        union_alias=False 
        axis_key=sd.label           # e.g. 'plev7h'
        grid_id=create_grid_def(grid_defs,axis_defs[axis_key],sd.out_name,src_grid_id)
        field_defs[alias_with_levels]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
            %(alias_with_levels+'"',alias_sample+'"',grid_id+'"')
        #if "hus" in alias :
        #    print "--->",alias, alias_with_levels,sd
        #    print "field_def=",field_defs[alias_with_levels]

    #
    return grid_id,alias_with_levels

def create_output_grid(ssh, lset,grid_defs,domain_defs,target_hgrid_id,margs):
    # Build output grid (stored in grid_defs) by analyzing the spatial shape
    # Including horizontal operations. Can include horiz re-gridding specification
    #--------------------------------------------------------------------
    grid_ref=None

    # Compute domain name, define it if needed
    if ssh[0:2] == 'Y-' : #zonal mean and atm zonal mean on pressure levels
        # Grid normally has already been created upstream
        grid_ref=margs['src_grid_id']
    elif (ssh == 'S-na')  :
        # COSP sites. Input field may have a singleton dimension (XIOS scalar component)
        grid_ref=cfsites_grid_id
        add_cfsites_in_defs(grid_defs,domain_defs)
        # 
    elif ssh[0:3] == 'XY-' or ssh[0:3] == 'S-A' :
        # this includes 'XY-AH' and 'S-AH' : model half-levels
        if (ssh[0:3] == 'S-A') :
            add_cfsites_in_defs(grid_defs,domain_defs)
            target_hgrid_id=cfsites_domain_id
        if target_hgrid_id :
            # Must create and a use a grid similar to the last one defined 
            # for that variable, except for a change in the hgrid/domain
            grid_ref=change_domain_in_grid(target_hgrid_id, grid_defs,lset=lset,**margs)
            if grid_ref is False or grid_ref is None : 
                raise dr2xml_error("Fatal: cannot create grid_def for %s with hgrid=%s"%(alias,target_hgrid_id))
    elif ssh == 'TR-na' or ssh == 'TRS-na' : #transects,   oce or SI
        pass
    elif ssh[0:3] == 'YB-'  : #basin zonal mean or section
        pass
    elif ssh      == 'na-na'  : # TBD ? global means or constants - spatial integration is not handled 
        pass 
    elif ssh      == 'na-A'  : # only used for rlu, rsd, rsu ... in Efx ????
        pass 
    else :
        raise dr2xml_error("Fatal: Issue with un-managed spatial shape %s for variable %s in table %s"%(ssh,sv.label,table))
    return grid_ref

def process_zonal_mean(field_id, grid_id, target_hgrid_id,zgrid_id,\
                       field_defs,axis_defs,grid_defs,domain_defs,\
                       operation,frequency,lset,printout=False):
    """
    Based on a field FIELD_ID defined on some grid GRID_ID, build all XIOS constructs 
    needed to derive the zonal mean of the field, by chaining the definition of 
    successive derived fields:
    field1 which sets the relevant 'operation' on input field
    field2 which applies the time operation 
    field3 which applies a regriding to an intermediate horizontal grid  TARGET_HGRID_ID
    field4 which regrids to the relevant zonal grid ZGRID_ID

    Returns field_id and  grid_id for the 4th, final, field
    Intermediate constructs are stored in dics field_defs, grid_defs, axis_defs

    For fields 1 and 2, we adopt the same naming conventions than when
    the same operations are done outside the zonal grid context; this
    is for optimzation when both contexts occur

    """
    printout=False
    global nlonz

    # e.g. <field id="CMIP6_ua_plev39_average" field_ref="CMIP6_ua_plev39" operation="average" />
    xios_freq=Cmip6Freq2XiosFreq[frequency]
    field1_id= field_id+"_"+operation     # e.g. CMIP6_hus_plev7h_instant
    field_defs[field1_id]='<field id="%-s field_ref="%-s operation="%s />'\
        %(field1_id+'"',field_id+'"',operation+'"')
    if printout :
        print "+++ field1 ",field1_id,"\n",field_defs[field1_id]
    #
    # e.g. <field id="CMIP6_ua_plev39_average_1d" field_ref="CMIP6_ua_plev39_average" freq_op="1d" >
    #              @CMIP6_ua_plev39_average </field>
    field2_id= field1_id+"_"+xios_freq 
    field_defs[field2_id]='<field id="%-s field_ref="%-s freq_op="%s > @%s </field>'\
        %(field2_id+'"',field1_id+'"',xios_freq+'"',field1_id)
    if printout :
        print "+++ field2 ",field2_id,"\n",field_defs[field2_id]
    
    if target_hgrid_id : # case where an intermediate grid is needed
        # e.g. <field id="CMIP6_ua_plev39_average_1d_complete" field_ref="CMIP6_ua_plev39_average_1d"
        #             grid_ref="FULL_klev_plev39_complete" /> 
        field3_id= field2_id+"_"+target_hgrid_id 
        # Must create and a use a grid similar to the last one defined 
        # for that variable, except for a change in the hgrid/domain (=> complete)
        grid_id3=change_domain_in_grid(target_hgrid_id, grid_defs,lset,src_grid_id=grid_id)
        if printout :
            print "+++ grid3 ",grid_id3,"\n",grid_defs[grid_id3]
        field_defs[field3_id]='<field id="%s field_ref="%s grid_ref="%s /> '\
                %(field3_id+'"',field2_id+'"',grid_id3+'"')
        if printout :
            print "+++ field3 ",field3_id,"\n",field_defs[field3_id]
    else :
        # Case where the input field is already on a rectangular grid
        print '~~~~>', "no target_hgrid_id for field=",field_id," grid=",grid_id
        field3_id=field2_id
        grid_id3=grid_id

    if not zgrid_id :
        raise dr2xml_error("Must provide zgrid_id in lab_settings, the id of a latitude axis which has "+\
                     "(initialized) latitude values equals to those of the rectangular grid used")
        
    # And then regrid to final grid
    # e.g. <field id="CMIP6_ua_plev39_average_1d_glat" field_ref="CMIP6_ua_plev39_average_1d_complete"
    #             grid_ref="FULL_klev_plev39_complete_glat" />
    field4_id= field2_id+"_"+zgrid_id 
    grid4_id=change_domain_in_grid(zgrid_id, grid_defs,lset,src_grid_id=grid_id3,turn_into_axis=True)
    if printout :
        print "+++ grid4 ",grid4_id,"\n",grid_defs[grid4_id]
    
    field_defs[field4_id]='<field id="%s field_ref="%s grid_ref="%s /> '\
        %(field4_id+'"',field3_id+'"',grid4_id+'"')
    if printout :
        print "+++ field4 ",field4_id,"\n",field_defs[field4_id]

    return field4_id, grid4_id
    
def process_diurnal_cycle(alias,field_defs,grid_defs,axis_defs,printout=False):

    """
    Based on a field id ALIAS, and gobal CONTEXT_INDEX, creates and
    stores Xios xml constructs for defining a derived variable which
    is the diurnal cycle of ALIAS

    All objects are stored in the corresponding dict (grid_defs, field_defs, axis_defs)

    Returns the field id for the derived variable, and its grid_id

    Steps : 
    0- create a construct for averaging ALIAS on 1h periods
    1- create a grid composed of ALIAS's original grid extended by a scalar; 
    2- create a construct for re-gridding 1h-averaged ALIAS on that first grid; 
    3- create an axis of 24 values having sub-construct 'time splitting'; 
    4- create a grid composed of ALIAS's original grid extended by that axis; 
    5- create a construct for re-gridding ALIAS_SCALAR on that second grid; and returns it id


    """

    printout=False
    # 0- create a clone of ALIAS with operation=average
    field_for_average_id=alias+"_for_average"
    field_defs[field_for_average_id]='<field id="%s" field_ref="%s" operation="average" />'%\
        (field_for_average_id,alias)
    if printout : print "***>",field_defs[field_for_average_id]

    # 1- create a grid composed of ALIAS's original grid extended by a scalar; id is <grid_id>_scalar_grid
    base_grid=id2grid(alias,context_index)
    base_grid_string=ET.tostring(base_grid)
    grid_id=base_grid.attrib['id']
    
    grid_scalar_id=grid_id+"_plus_scalar"
    grid_scalar=re.sub(r'(.*)grid  *id *= *"[^"]*"(.*)',r'\1grid id="%s"\2'%grid_scalar_id,base_grid_string)
    grid_scalar=re.sub("(.*)</ *grid *>(.*)",r'\1<scalar /> </grid>\2',grid_scalar)
    if printout : print "***>",grid_scalar
    grid_defs[grid_scalar_id]=grid_scalar

    # 2- create a construct for re-gridding the field with operation average on that ,
    # first grid, and also averaging over 1h ; id is ALIAS_1h_average_scalar
    averaged_field_id=alias+"_1h_average_scalar"
    field_defs[averaged_field_id]='<field id="%s" freq_op="1h" grid_ref="%s"> @%s </field>'%\
        (averaged_field_id,grid_scalar_id,field_for_average_id)
    if printout : print "***>",field_defs[averaged_field_id]
    
    # 3- create an axis of 24 values having sub-construct 'time splitting'; axis id is "24h_axis"
    axis_24h_id="hour_in_diurnal_cycle"
    name_and_units='name="time3" unit="days since ?" standard_name="time"'
    axis_24h='<axis id="%s" n_glo="24" %s value="(0,23)[ '%(axis_24h_id,name_and_units)
    for i in range(0,24) : axis_24h += '%g '%(i+0.5)
    axis_24h+=']" >\n\t<temporal_splitting /></axis>'
    axis_defs[axis_24h_id]=axis_24h
    if printout : print "***>",axis_24h
    
    # 4- create a grid composed of ALIAS's original grid extended by that axis; id is <grid_id>_24h_grid
    grid_24h_id=grid_id+"_plus_axis24h"
    grid_24h=re.sub(r'(.*)grid  *id *= *"[^"]*"(.*)',r'\1grid id="%s"\2'%grid_24h_id,base_grid_string)
    grid_24h=re.sub("</ *grid *>",'\t<axis axis_ref="%s" %s /></grid>'%(axis_24h_id,name_and_units),grid_24h)
    grid_defs[grid_24h_id]=grid_24h
    if printout : print "***>",grid_24h
    
    # 5- create a construct for re-gridding ALIAS_SCALAR on that second grid; id is ALIAS_24hcycle, which is returned
    #        <field id="field_B"  grid_ref="grid_B" field_ref="field_As" />
    alias_24h_id=alias+"_split24h"
    alias_24h='<field id="%s"  grid_ref="%s" field_ref="%s" />'%(alias_24h_id,grid_24h_id,averaged_field_id)
    field_defs[alias_24h_id]=alias_24h
    if printout : print "***>",alias_24h,"\n"
    
    return alias_24h_id,grid_24h_id


def gather_AllSimpleVars(lset,sset,year=False,printout=False,select="on_expt_and_year"):
    if select=="on_expt_and_year" or select=="" :
        mip_vars_list=select_CMORvars_for_lab(lset,sset,year,printout=printout)
    elif select=="on_expt" : 
        mip_vars_list=select_CMORvars_for_lab(lset,sset ,None,printout=printout)
    elif select=="no" :
        mip_vars_list=select_CMORvars_for_lab(lset,None ,None,printout=printout)
    else:
        raise dr2xml_errors("Choice %s is not allowed for arg 'select'"%select)
    #
    if sset.get('listof_home_vars',lset.get('listof_home_vars',None)):
        process_homeVars(lset,sset,mip_vars_list,lset["mips"][grid_choice],
                         dq,expid=sset['experiment_id'],printout=printout)
    else: print "Info: No HOMEvars list provided."
    return mip_vars_list

def generate_file_defs(lset,sset,year,enddate,context,cvs_path,pingfiles=None,
                       dummies='include',printout=False,dirname="./",prefix="",attributes=[],select="on_expt_and_year") :
    # A wrapper for profiling top-level function : generate_file_defs_inner
    import cProfile, pstats, StringIO
    pr = cProfile.Profile()
    pr.enable()
    generate_file_defs_inner(lset,sset,year,enddate,context,cvs_path,pingfiles=pingfiles,
                             dummies=dummies,printout=printout,dirname=dirname,
                             prefix=prefix,attributes=attributes,select=select) 
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    # Just un-comment next line to get the profile on stdout
    #print s.getvalue()

    
def generate_file_defs_inner(lset,sset,year,enddate,context,cvs_path,pingfiles=None,
                             dummies='include',printout=False,dirname="./",prefix="",
                             attributes=[],select="on_expt_and_year") :
    """
    Using global DR object dq, a dict of lab settings LSET, and a dict 
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
    debug=False
    global print_wrv
    print_wrv=lset.get("print_variables",True)
    cmvk="CMIP6_CV_version"
    if cmvk in  attributes : print "* %s: %s"%(cmvk,attributes[cmvk])
    #--------------------------------------------------------------------
    # Parse XIOS settings file for the context
    #--------------------------------------------------------------------
    global context_index
    print "\n",50*"*","\n"
    print "Processing context ",context
    print "\n",50*"*","\n"
    context_index=init_context(context,lset.get("path_to_parse","./"),
                               printout=lset.get("debug_parsing",False))
    if context_index is None : sys.exit(1)
    cell_method_warnings=[]
    warnings_for_optimisation=[]
    sn_issues=dict()

    #
    #--------------------------------------------------------------------
    # Extract CMOR variables for the experiment and year and lab settings
    #--------------------------------------------------------------------
    skipped_vars_per_table={}
    actually_written_vars=[]
    mip_vars_list=gather_AllSimpleVars(lset,sset,year,printout,select)
    # Group CMOR vars per realm
    svars_per_realm=dict()
    for svar in mip_vars_list :
        realm=svar.modeling_realm
        if realm not in svars_per_realm :
            svars_per_realm[realm]=[]
        if svar not in svars_per_realm[realm]:
            add=True
            for ovar in svars_per_realm[realm]:
                if ovar.label==svar.label and ovar.spatial_shp==svar.spatial_shp \
                   and ovar.frequency==svar.frequency and ovar.cell_methods==svar.cell_methods:
                    add=False
            # Settings may allow for duplicate var in two tables. In DR01.00.21, this actually
            # applies to very few fields (ps-Aermon, tas-ImonAnt, areacellg)
            if lset.get('allow_duplicates',True) or add : 
                svars_per_realm[realm].append(svar)
            else :
                print "Not adding duplicate %s (from %s) for realm %s"%(svar.label,svar.mipTable,realm)
        else:
            old=svars_per_realm[realm][0]
            print "Duplicate svar %s %s %s %s"%(old.label,old.grid,svar.label,svar.grid)
            pass
    if printout :
        print "\nRealms for these CMORvars :",svars_per_realm.keys()
    #
    #--------------------------------------------------------------------
    # Select on context realms, grouping by table
    # Excluding 'excluded_vars' and 'excluded_spshapes' lists
    #--------------------------------------------------------------------
    svars_per_table=dict()
    context_realms=lset['realms_per_context'][context]
    processed_realms=[]
    for realm in context_realms :
        if realm in processed_realms : continue
        processed_realms.append(realm)
        excludedv=dict()
        print "Processing realm '%s' of context '%s'"%(realm,context)
        #print 50*"_"
        excludedv=dict()
        if realm in svars_per_realm:
            for svar in svars_per_realm[realm] :
                # exclusion de certaines spatial shapes (ex. Polar Stereograpic Antarctic/Groenland)
                if svar.label not in lset['excluded_vars'] and \
                   svar.spatial_shp and \
                   svar.spatial_shp not in lset["excluded_spshapes"]:  
                    if svar.mipTable not in svars_per_table : 
                        svars_per_table[svar.mipTable]=[]
                    svars_per_table[svar.mipTable].append(svar)
                else:
                    if printout:
                        reason="unknown reason"
                        if svar.label in lset['excluded_vars']: reason= "They are in exclusion list "
                        if not svar.spatial_shp: reason= "They have no spatial shape "
                        if svar.spatial_shp in lset["excluded_spshapes"]:
                            reason="They have excluded spatial shape : %s"%svar.spatial_shp
                        if reason not in excludedv : excludedv[reason]=[]
                        excludedv[reason].append((svar.label,svar.mipTable))
        if printout and len(excludedv.keys())>0:
            print "The following pairs (variable,table) have been excluded for these reasons :"
            for reason in excludedv : print "\t",reason,":",excludedv[reason]
    if (debug ) : print "For table AMon: ",[ v.label for v in svars_per_table["Amon"] ]
    #      
    #--------------------------------------------------------------------
    # Add svars belonging to the orphan list
    #--------------------------------------------------------------------
    if context in lset['orphan_variables']:
        orphans=lset['orphan_variables'][context]
        for svar in mip_vars_list :
            if svar.label in orphans:
                if svar.label not in lset['excluded_vars'] and svar.spatial_shp and \
                   svar.spatial_shp not in lset["excluded_spshapes"]:  
                    if svar.mipTable not in svars_per_table : svars_per_table[svar.mipTable]=[]
                    svars_per_table[svar.mipTable].append(svar)
    #      
    #--------------------------------------------------------------------
    # Remove svars belonging to other contexts' orphan lists
    #--------------------------------------------------------------------
    for other_context in lset['orphan_variables']:
        if other_context != context:
            orphans=lset['orphan_variables'][other_context]
            for table in svars_per_table :
                toremove=[]
                for svar in svars_per_table[table] :
                    if svar.label in orphans: toremove.append(svar)
                for svar in toremove : svars_per_table[table].remove(svar)
    if (debug ) : print "Pour table AMon: ",[ v.label for v in svars_per_table["Amon"] ]
    #
    #--------------------------------------------------------------------
    # Read ping_file defined variables
    #--------------------------------------------------------------------
    pingvars=[] 
    all_ping_refs={} 
    if pingfiles is not None:
        all_pingvars=[]
        #print "pingfiles=",pingfiles
        for pingfile in pingfiles.split() :
            ping_refs=read_xml_elmt_or_attrib(pingfile, tag='field', attrib='field_ref')
            #ping_refs=read_xml_elmt_or_attrib(pingfile, tag='field')
            if ping_refs is None :
                print "Error: issue accessing pingfile "+pingfile
                return
            all_ping_refs.update(ping_refs)
            if dummies=="include" :
                pingvars=ping_refs.keys()
            else :
                pingvars=[ v for v in ping_refs if 'dummy' not in ping_refs[v] ]
                if dummies=="forbid" :
                    if len(pingvars) != len(ping_refs) :
                        for v in ping_refs :
                            if v not in pingvars : print v,
                        print
                        raise dr2xml_error("They are still dummies in %s , while option is 'forbid' :"%pingfile)
                    else :
                        pingvars=ping_refs.keys()
                elif dummies=="skip" : pass
                else:
                    print "Forbidden option for dummies : "+dummies
                    sys.exit(1)
            all_pingvars.extend(pingvars)
        pingvars=all_pingvars
    #
    field_defs=dict()
    axis_defs=dict()
    grid_defs=dict()
    file_defs=dict()
    scalar_defs=dict()
    #
    #--------------------------------------------------------------------
    # Build all plev union axis and grids
    #--------------------------------------------------------------------
    if lset.get('use_union_zoom',False):
        svars_full_list=[]
        for svl in svars_per_table.values(): svars_full_list.extend(svl)
        create_xios_axis_and_grids_for_plevs_unions(svars_full_list,
                                        multi_plev_suffixes.union(single_plev_suffixes),
                                        lset, dummies, axis_defs,grid_defs,field_defs,
                                        all_ping_refs, printout=False )
    #
    #--------------------------------------------------------------------
    # Start writing XIOS file_def file: 
    # file_definition node, including field child-nodes
    #--------------------------------------------------------------------
    #filename=dirname+"filedefs_%s.xml"%context
    filename=dirname+"dr2xml_%s.xml"%context
    with open(filename,"w") as out :
        out.write('<context id="%s"> \n'%context)
        out.write('<!-- CMIP6 Data Request version %s --> \n'%dq.version)
        out.write('<!-- CMIP6-CV version %s --> \n'%"??")
        out.write('<!-- CMIP6_conventions_version %s --> \n'%CMIP6_conventions_version)
        out.write('<!-- dr2xml version %s --> \n'%version)
        out.write('<!-- Lab_and_model settings : \n')        
        for s,v in sorted(lset.iteritems()) : out.write(' %s : %s\n'%(s,v))
        out.write('-->\n')
        out.write('<!-- Simulation settings : \n')        
        for s,v in sorted(sset.iteritems()) : out.write(' %s : %s\n'%(s,v))
        out.write('-->\n')
        out.write('<!-- Year processed is  %s --> \n'%year)
        #
        domain_defs=dict()
        #for table in ['day'] :    
        out.write('\n<file_definition type="one_file" enabled="true" > \n')
        foo,sourcetype=get_source_id_and_type(sset,lset)
        for table in sorted(svars_per_table.keys()) :
            count=dict()
            for svar in sorted(svars_per_table[table],key = lambda x: (x.label + "_" + table)):
                if lset.get("allow_duplicates_in_same_table",False) or svar.mipVarLabel not in count :
                    if not lset.get("use_cmorvar_label_in_filename",False) and svar.mipVarLabel in count :
                        form="If you really want to actually produce both %s and %s in table %s, "+\
                            "you must set 'use_cmorvar_label_in_filename' to True in lab settings"
                        raise dr2xml_error(form%(svar.label, count[svar.mipVarLabel].label,table))
                    count[svar.mipVarLabel]=svar
                    for grid in svar.grids :
                        a,hgrid,b,c,d=lset['grids'][grid_choice][context]
                        check_for_file_input(svar,lset,hgrid,pingvars,field_defs,
                                             grid_defs,domain_defs,file_defs)
                        write_xios_file_def(svar,year,table, lset,sset,out,cvs_path,
                                            field_defs,axis_defs,grid_defs,domain_defs,scalar_defs,file_defs,
                                            dummies, skipped_vars_per_table,actually_written_vars,
                                            prefix,context,grid,pingvars,enddate,attributes)
                else:
                    print "Duplicate variable %s,%s in table %s is skipped, preferred is %s"%\
                        (svar.label, svar.mipVarLabel,table,count[svar.mipVarLabel].label)
                        
        if cfsites_grid_id in grid_defs : out.write(cfsites_input_filedef())
        for file_def in file_defs : out.write(file_defs[file_def])
        out.write('\n</file_definition> \n')
        #
        #--------------------------------------------------------------------
        # End writing XIOS file_def file: 
        # field_definition, axis_definition, grid_definition 
        # and domain_definition auxilliary nodes
        #--------------------------------------------------------------------
        # Write all domain, axis, field defs needed for these file_defs
        out.write('<field_definition> \n')
        if lset.get("nemo_sources_management_policy_master_of_the_world",False) and context=='nemo':
            out.write('<field_group freq_op="_reset_" freq_offset="_reset_" >\n')
        for obj in sorted(field_defs.keys()): out.write("\t"+field_defs[obj]+"\n")
        if lset.get("nemo_sources_management_policy_master_of_the_world",False) and context=='nemo':
            out.write('</field_group>\n')
        out.write('\n</field_definition> \n')
        #
        out.write('\n<axis_definition> \n')
        out.write('<axis_group prec="8">\n')
        for obj in sorted(axis_defs.keys()): out.write("\t"+axis_defs[obj]+"\n")
        if False and lset.get('use_union_zoom',False):
            for obj in sorted(union_axis_defs.keys()): out.write("\t"+union_axis_defs[obj]+"\n")
        out.write('</axis_group>\n')
        out.write('</axis_definition> \n')
        #
        out.write('\n<domain_definition> \n')
        out.write('<domain_group prec="8">\n')
        if lset['grid_policy'] != "native" : create_standard_domains(domain_defs)
        for obj in sorted(domain_defs.keys()): out.write("\t"+domain_defs[obj]+"\n")
        out.write('</domain_group>\n')
        out.write('</domain_definition> \n')
        #
        out.write('\n<grid_definition> \n')
        for obj in grid_defs.keys(): out.write("\t"+grid_defs[obj])
        if False and lset.get('use_union_zoom',False):
            for obj in sorted(union_grid_defs.keys()): out.write("\t"+union_grid_defs[obj]+"\n")
        out.write('</grid_definition> \n')
        #
        out.write('\n<scalar_definition> \n')
        for obj in sorted(scalar_defs.keys()): out.write("\t"+scalar_defs[obj]+"\n")
        out.write('</scalar_definition> \n')
        #
        out.write('</context> \n')
    if printout :
        print "\nfile_def written as %s"%filename
    
    # mpmoine_petitplus:generate_file_defs: pour sortir des stats sur ce que l'on sort reelement
    # SS - non : gros plus
    if printout: print_SomeStats(context,svars_per_table,skipped_vars_per_table,
                                 actually_written_vars,lset.get("print_stats_per_var_label", False))

    warn=dict()
    for warning,label,table in cell_method_warnings:
        if warning not in warn : warn[warning]=set()
        warn[warning].add(label)
    if len(warn) > 0 :
        print "\nWarnings about cell methods (with var list)"
        for w in warn  : print "\t",w," for vars : ",warn[w]
    if len(warnings_for_optimisation) > 0 :
        print "Warning for fields which cannot be optimised (i.e. average before remap) because of an expr with @\n\t",
        for w in warnings_for_optimisation  : print w.replace(lset['ping_variables_prefix'],""),
        print
        

# mpmoine_petitplus: nouvelle fonction print_SomeStats (plus d'info sur les skipped_vars, nbre de vars / (shape,freq) )
# SS - non : gros plus
def print_SomeStats(context,svars_per_table,skipped_vars_per_table,actually_written_vars,extended=False):

  if False:
    #--------------------------------------------------------------------
    # Print Summary: list of  considered variables per table 
    # (i.e. not excuded_vars and not excluded_shapes)
    #--------------------------------------------------------------------
    print "\nTables concerned by context %s : "%context, svars_per_table.keys()
    print "\nVariables per table :" 
    for table in svars_per_table.keys():
    	print "\n>>> TABLE:",
        print "%15s %02d ---->"%(table,len(svars_per_table[table])),
        for svar in svars_per_table[table]: 
        	print svar.label+"("+str(svar.Priority)+")",
    print

  if True :
    #--------------------------------------------------------------------
    # Print Summary: list of skipped variables per table
    # (i.e. not in the ping_file)
    #--------------------------------------------------------------------
    if skipped_vars_per_table:
	print "\nSkipped variables (i.e. whose alias is not present in the pingfile):"
        for table,skipvars in skipped_vars_per_table.items():
    	    print ">>> TABLE:",
            print "%15s %02d/%02d ---->"%(table,len(skipvars),len(svars_per_table[table])),
            #TBS# print "\n\t",table ," ",len(skipvars),"--->",
            for skv in skipvars: 
            	print skv, #already contains priority info
            print
        print

    #--------------------------------------------------------------------
    # Print Summary: list of variables really written in the file_def
    # (i.e. not excluded and not skipped)
    #--------------------------------------------------------------------
    stats_out={}
    for table in svars_per_table:
    	for sv in svars_per_table[table]:
    		dic_freq={}
    		dic_shp={}
    		if table not in skipped_vars_per_table  or \
    		   sv.label+"("+str(sv.Priority)+")" not in skipped_vars_per_table[table]  :
    			freq=sv.frequency
    			shp=sv.spatial_shp
    			prio=sv.Priority
    			var=sv.label
    			if stats_out.has_key(freq):
    				dic_freq=stats_out[freq]
    				if dic_freq.has_key(shp):
    					dic_shp=dic_freq[shp]
    			dic_shp.update({var:table+"-P"+str(prio)})
    			dic_freq.update({shp:dic_shp})
    			stats_out.update({freq:dic_freq})

    print "\n\nSome Statistics on actually written variables per frequency+shape..."

    #    ((sv.label,sv.table,sv.frequency,sv.Priority,sv.spatial_shp))
    dic=dict()
    for label,long_name,table,frequency,Priority,spatial_shp in actually_written_vars :
        if frequency not in dic : dic[frequency]=dict()
        if spatial_shp not in dic[frequency] : dic[frequency][spatial_shp]=dict()
        if table not in dic[frequency][spatial_shp] : dic[frequency][spatial_shp][table]=dict()
        if Priority not in dic[frequency][spatial_shp][table] : dic[frequency][spatial_shp][table][Priority]=[]
        dic[frequency][spatial_shp][table][Priority].append(label)
    tot_among_freqs=0
    for frequency in dic :
        tot_for_freq_among_shapes=0
        for spatial_shp in dic[frequency] :
            tot_for_freq_and_shape_among_tables=0
            for table in dic[frequency][spatial_shp] :
                for Priority in dic[frequency][spatial_shp][table] :
                    print "%10s"%" ", " %8s"%" ", "% 12s"%table,"P%1d"%Priority,
                    l=dic[frequency][spatial_shp][table][Priority]
                    print "% 3d : "%len(l),l
                    tot_for_freq_and_shape_among_tables+=len(l)
            print "%10s"%frequency," %8s"%spatial_shp,"% 11s"%"--------","---","%3d"%tot_for_freq_and_shape_among_tables
            tot_for_freq_among_shapes+=tot_for_freq_and_shape_among_tables
            print
        print "%10s"%frequency," %8s"%"--------","% 11s"%"--------","---","%3d"%tot_for_freq_among_shapes
        tot_among_freqs+=tot_for_freq_among_shapes
        print; print
    print "%10s"%"----------"," %8s"%"--------","% 11s"%"--------","---","%3d"%tot_among_freqs
    
    if extended :
        print "\n\nSome Statistics on actually written variables per variable..."
        dic=dict()
        dic_ln=dict()
        for label,long_name,table,frequency,Priority,spatial_shp in actually_written_vars :
            if not dic.has_key(label): 
                dic[label]=[]
                dic_ln.update({label:long_name})
            dic[label].append(frequency+'_'+table+'_'+spatial_shp+'_'+str(Priority))
            
        list_labels=dic.keys()
        list_labels.sort()
        print ">>> DBG >>>",list_labels
    
        for label in list_labels:
            print (14+len(label))*"-"
            print "--- VARNAME: ",label,":", dic_ln[label]
            print (14+len(label))*"-"
            for val in dic[label]:
                print 14*" "+"* ",val
                
    return True


def create_axis_def(sdim,lset,axis_defs,field_defs):
    """

    From a simplified Dim object SDIM representing a vertical dimension,
    creates and stores an Xios axis definition in AXIS_DEFS

    If the dimension implies vertical interpolation (on air_pressure
    or altitude levels), creates and stores (in FIELD_DEFS) two
    intermediate fields for the sampling of that coordinate field at
    the vert_frequency and with the type of operation indicated by LSET

    If the dimension is a zoom of another one, analyzes its 'requested'
    field against the list of values declared for the other one, for
    defining the zoom in XIOS syntax

    """

    prefix=lset["ping_variables_prefix"]
    # nbre de valeurs de l'axe determine aussi si on est en dim singleton
    if sdim.requested: glo_list=sdim.requested.strip(" ").split()
    else: glo_list=sdim.value.strip(" ").split()
    glo_list_num=[float(v) for v in glo_list]
    glo_list_num.sort(reverse=True)
    n_glo=len(glo_list)

    if not sdim.is_zoom_of: # pure interpolation
        # Axis is not a zoom of another, write axis_def normally (with value, interpolate_axis,etc.)
        rep='<axis id="%s" '%sdim.label
        if not sdim.positive in [ None, "" ] :
            rep+='positive="%s" '%sdim.positive
        if n_glo > 1 :
            # Case of a non-degenerated vertical dimension (not a singleton)
            rep+='n_glo="%g" '%n_glo
            rep+='value="(0,%g)[ %s ]"'%(n_glo-1,sdim.requested)
        else:
            if n_glo!=1: 
                print "Warning: axis for %s is singleton but has %d values"%(sdim.label,n_glo)
                return None
            # Singleton case (degenerated vertical dimension)
            rep+='n_glo="%g" '%n_glo
            rep+='value="(0,0)[ %s ]"'%sdim.value
        rep+=' name="%s"'%sdim.out_name
        rep+=' standard_name="%s"'%sdim.stdname
        rep+=' long_name="%s"'%sdim.long_name
        rep+=' unit="%s"'%sdim.units
        rep+='>'
        if sdim.stdname=="air_pressure" : coordname=prefix+"pfull"
        if sdim.stdname=="altitude"     : coordname=prefix+"zg"
        #
        # Create an intemediate field for coordinate , just adding time sampling
        operation=lset.get("vertical_interpolation_operation","instant")
        coordname_with_op=coordname+"_"+operation # e.g. CMIP6_pfull_instant
        coorddef_op='<field id="%-25s field_ref="%-25s operation="%s" detect_missing_value="true"/>'\
            %(coordname_with_op+'"',coordname+'"', operation)
        field_defs[coordname_with_op]=coorddef_op
        #
        # Create and store a definition for time-sampled field for the vertical coordinate
        vert_frequency=lset["vertical_interpolation_sample_freq"]
        coordname_sampled=coordname_with_op+"_sampled_"+vert_frequency # e.g. CMIP6_pfull_instant_sampled_3h
        rep+='<interpolate_axis type="polynomial" order="1"'
        rep+=' coordinate="%s"/>\n\t</axis>'%coordname_sampled
        # Store definition for the new axis
        axis_defs[sdim.label]=rep
        coorddef='<field id="%-25s field_ref="%-25s freq_op="%-10s detect_missing_value="true"> @%s</field>'\
            %(coordname_sampled+'"',coordname_with_op+'"', vert_frequency+'"',coordname)
        field_defs[coordname_sampled]=coorddef
    else: # zoom case
        # Axis is subset of another, write it as a zoom_axis
        rep='<axis id="%s"'%sdim.zoom_label
        rep+=' axis_ref="%s" name="plev"'%sdim.is_zoom_of
        rep+=' axis_type="%s">'%sdim.axis
        rep+='\t<zoom_axis index="(0,%g)[ '%(n_glo-1)
        values=re.sub(r'.*\[ *(.*) *\].*',r'\1',axis_defs[sdim.is_zoom_of])
        values=values.split("\n")[0]
        union_vals=values.strip(" ").split()
        union_vals_num=[float(v) for v in union_vals]
        for val in glo_list_num : rep+=' %g'%union_vals_num.index(val)
        rep+=' ]"/>'
        rep+='</axis>'
        # Store definition for the new axis
        axis_defs[sdim.zoom_label]=rep
    return rep 

def add_scalar_in_grid(gridin_def,gridout_id,scalar_id,scalar_name,remove_axis, change_scalar=True):
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
    format='< *scalar *([^>]*)scalar_ref=["\']%s["\']'
    expr=format%scalar_id
    if re.search(expr,gridin_def) :
        return gridin_def
    gridin_def=gridin_def.replace("\n","")
    # TBD : in change_scalar : discard extract_axis only if really relevant (get the right axis)
    # TBD : in change_scalar : preserve ordering of domains/axes...
    if change_scalar :
        extract_pattern="<scalar *>.*<extract_axis.*/> *</scalar *>"
        gridin_def,count=re.subn(extract_pattern,"",gridin_def)
    pattern= '< *grid *([^> ]*) *id=["\']([^"\']*)["\'] *(.*)</ *grid *>'
    replace=r'<grid \1 id="%s" \3<scalar scalar_ref="%s" name="%s"/>  </grid>'%(gridout_id,scalar_id,scalar_name)
    (rep,count)=re.subn(pattern,replace,gridin_def.replace("\n",""))
    if count==0 : raise dr2xml_error("No way to add scalar '%s' in grid '%s'"%(scalar_id,gridin_def))
    #
    # Remove any axis if asked for
    if remove_axis:
        axis_pattern='< *axis *[^>]*>'
        (rep,count)=re.subn(axis_pattern,"",rep)
        #if count==1 :
        #    print "Info: axis has been removed for scalar %s (%s)"%(scalar_name,scalar_id)
        #    print "grid_def="+rep
    return rep+"\n"
                               
    

def change_axes_in_grid(grid_id, grid_defs,axis_defs,lset):
    """
    Create a new grid based on GRID_ID def by changing all its axis references to newly created 
    axis which implement CMIP6 axis attributes
    Works only on axes which id match the labels of DR dimensions (e.g. sdepth, landUSe ...)
    Stores the definitions in GRID_DEFS and AXIS_DEFS
    Returns the new grid_id
    """
    global axis_count
    grid_def=get_grid_def(grid_id,grid_defs)
    grid_el=ET.fromstring(grid_def)
    output_grid_id=grid_id
    axes_to_change=[]
    #print "in change_axis for %s "%(grid_id)

    # Get settings info about axes normalization  
    aliases=lset.get('non_standard_axes',dict())

    # Add cases where dim name 'sector' should be used,if needed
    # sectors = dims which have type charcter and are not scalar
    if 'sectors' in lset : sectors=lset['sectors']
    else:
        sectors=[ dim.label for dim in dq.coll['grids'].items if \
                  dim.type=='character' and dim.value=='' ]
    if 'typewetla'in sectors : sectors.remove('typewetla') # Error in DR 01.00.21
    #print "sectors=",sectors
    for sector in sectors: 
        found=False
        for aid in aliases :
            if aliases[aid]==sector :
                found=True ; continue
            if type(aliases[aid])==type(()) and aliases[aid][0]==sector :
                found=True ; continue
        if not found :
            #print "\nadding sector : %s"%sector
            aliases[sector]=sector

    for sub in grid_el :
        if sub.tag=='axis' :
            #print "checking grid %s"%grid_def
            if 'axis_ref' not in sub.attrib :
                # Definitely don't want to change an unnamed axis. Such an axis is
                # generated by vertical interpolation
                if any ([ ssub.tag=='interpolate_axis' for ssub in sub ]) : continue
                else:
                    print "Cannot normalize an axis in grid %s : no axis_ref for axis %s"%(grid_id,ET.tostring(sub))
                    continue
                    #raise dr2xml_error("Grid %s has an axis without axis_ref : %s"%(grid_id,grid_def))
            axis_ref=sub.attrib['axis_ref']
            #
                    
            # Just quit if axis doesn't have to be processed
            if axis_ref not in aliases.keys() :
                #print "for grid ",grid_id,"axis ",axis_ref, " is not in aliases"
                continue
            #
            dr_axis_id=aliases[axis_ref] ; alt_labels=None
            if type(dr_axis_id)==type(()) : dr_axis_id,alt_labels=dr_axis_id
            dr_axis_id=dr_axis_id.replace('axis_','') # For toy_cnrmcm, atmosphere part
            #print ">>> axis_ref=%s, dr_axis_id=%s,alt_labels=%s"%(axis_ref,dr_axis_id,alt_labels),aliases[axis_ref]
            #
            dim_id='dim:%s'%dr_axis_id
            #print "in change_axis for %s %s"%(grid_id,dim_id)
            if dim_id not in dq.inx.uid : # This should be a dimension !
                raise dr2xml_error("Value %s in 'non_standard_axes' is not a DR dimension id"%dr_axis_id)
            dim=dq.inx.uid[dim_id]
            # We don't process scalars here
            if dim.value=='' or dim.label=="scatratio" :
                axis_id,axis_name=create_axis_from_dim(dim,alt_labels,axis_ref,axis_defs,lset)
                # cannot use ET library which does not guarantee the ordering of axes
                axes_to_change.append((axis_ref,axis_id,axis_name))
                output_grid_id+="_"+dim.label
            else:
                raise dr2xml_error("Dimension %s is scalar and shouldn't be quoted in 'non_standard_axes'"%dr_axis_id)
    if len(axes_to_change) == 0 : return grid_id
    for old,new,name in axes_to_change :
        axis_count+=1
        grid_def=re.sub("< *axis[^>]*axis_ref= *.%s. *[^>]*>"%old,
                        '<axis axis_ref="%s" name="%s" id="ref_to_%s_%d"/>'%(new,name,new,axis_count), grid_def)
    grid_def=re.sub("< *grid([^>]*)id= *.%s.( *[^>]*)>"%grid_id,
                        r'<grid\1id="%s"\2>'%output_grid_id, grid_def)
    grid_defs[output_grid_id]=grid_def
    return output_grid_id
            
def create_axis_from_dim(dim,labels,axis_ref,axis_defs,lset):
    """
    Create an axis definition by translating all DR dimension attributes to XIos 
    constructs generating CMIP6 requested attributes
    """
    axis_id="DR_"+dim.label+"_"+axis_ref
    if dim.type=="character" : axis_name="sector"
    else : axis_name=dim.altLabel
    if axis_id in axis_defs : return axis_id,axis_name
    
    rep='<axis id="%s" name="%s" axis_ref="%s"'%(axis_id,axis_name,axis_ref)
    if type(dim.standardName)==type(""):
        rep+=' standard_name="%s"'%(dim.standardName)
    rep+=' long_name="%s"'%(dim.title)
    #
    if dim.type=="double": rep+=' prec="8"'
    elif dim.type in [ "integer", "int" ]: rep+=' prec="2"'
    elif dim.type=="float": rep+=' prec="4"'
    #
    if dim.units != '' : 
        rep+=' unit="%s"'%dim.units
    if dim.type!="character" :
        if dim.requested!="": 
            nb=len(dim.requested.split())
            rep+=' value="(0,%d)[ '%nb + dim.requested + ' ]"'
        if  type(dim.boundsRequested)==type([]) :
            vals=[ " %s"%v for v in dim.boundsRequested ]
            valsr=reduce(lambda x,y : x+y, vals)
            rep+=' bounds="(0,1)x(0,%d)[ '%(nb-1) + valsr +' ]"'
    else:
        rep+=' dim_name="%s" '%dim.altLabel
        if labels is None : labels=dim.requested
        if dim.label=="oline" and lset.get('add_Gibraltar',False) :
            labels+=" gibraltar"
        labels=labels.replace(', ',' ').replace(',',' ')
        length=len(labels.split())
        #print 'labels=',labels.split()
        strings=" "
        for s in labels.split() : strings+="%s "%s
        if length > 0 : rep+=' label="(0,%d)[ %s ]"'%(length-1,strings)
    rep+="/>"
    axis_defs[axis_id]=rep
    #print "new DR_axis :  %s "%rep
    return axis_id,axis_name


def change_domain_in_grid(domain_id,grid_defs,lset,ping_alias=None,src_grid_id=None,\
                          turn_into_axis=False,printout=False):
    """ 
    Provided with a grid id SRC_GRID_ID or alertnatively a variable name (ALIAS),
    (SRC_GRID_STRING) 
     - creates ans stores a grid_definition where the domain_id has been changed to DOMAIN_ID
    -  returns its id, which is 
    """
    if src_grid_id is None: raise dr2xml_error("deprecated")
    else : src_grid_string=get_grid_def(src_grid_id,grid_defs,lset)
    target_grid_id=src_grid_id+"_"+domain_id
    # Change domain
    domain_or_axis="domain" ; axis_name=""
    if turn_into_axis :
        domain_or_axis="axis" ; axis_name=' name="lat"'
    # sequence below was too permissive re. assumption that all grid definition use refs rather than ids
    #(target_grid_string,count)=re.subn('domain *id= *.([\w_])*.','%s id="%s" %s'%(domain_or_axis,domain_id,axis_name),\
    #                                   src_grid_string,1) 
    #if count != 1 :
    (target_grid_string,count)=re.subn('domain *domain_ref= *.([\w_])*.','%s %s_ref="%s" %s'%\
                            (domain_or_axis,domain_or_axis,domain_id,axis_name),src_grid_string,1) 
    if count != 1 :
        raise dr2xml_error("Fatal: cannot find a domain to replace by %s in src_grid_string %s, count=%d "%\
                           (domain_id,src_grid_string,count))
    target_grid_string=re.sub('grid *id= *.([\w_])*.','grid id="%s"'%target_grid_id,target_grid_string)
    grid_defs[target_grid_id]=target_grid_string
    #print "target_grid_id=%s : %s"%(target_grid_id,target_grid_string)
    return target_grid_id

def create_grid_def(grid_defs,axis_def,axis_name,src_grid_id):
    """
    Create and store a grid definition by changing in SRC_GRID_ID grid def
    its only axis member (either def or ref) with AXIS_DEF (where any id 
    has been removed)

    Returned grid_id = input grid_id + suffix '_AXIS_NAME'

    raises error if there is not exactly one axis def or reg in input grid

    """
    src_grid_def=get_grid_def(src_grid_id,grid_defs)
    #
    # Retrieve axis key from axis definition string
    axis_key=re.sub(r'.*id= *.([\w_]*).*',r'\1',axis_def.replace('\n',' '))
    target_grid_id=src_grid_id+"_"+axis_key
    #
    # Remove id= from axis definition string
    axis_def=re.sub(r'id= *.([\w_]*).','',axis_def)
    #
    # Change only first instance of axis_ref, which is assumed to match the vertical dimension
    # Enforce axis_name in axis_def :  TBD
    (target_grid_def,count)=re.subn('<axis[^\>]*>',axis_def,src_grid_def,1)
    if count != 1 :
        raise dr2xml_error("Fatal: cannot find an axis ref in grid %s : %s "%(src_grid_id,src_grid_def))
    target_grid_def=re.sub('grid id= *.([\w_])*.','grid id="%s"'%target_grid_id,target_grid_def)
    grid_defs[target_grid_id]=target_grid_def
    return target_grid_id

def create_xios_axis_and_grids_for_plevs_unions(svars,plev_sfxs,lset, dummies,
                                                axis_defs,grid_defs,field_defs, ping_refs, printout=False): 
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
    global context_index
    prefix=lset["ping_variables_prefix"]
    #First, search plev unions for each label_without_psuffix and build dict_plevs
    dict_plevs={}
    for sv in svars:
        if not sv.modeling_realm: print "Warning: no modeling_realm associated to:", \
                                            sv.label, sv.mipTable, sv.mip_era
        for sd in sv.sdims.values():
            # couvre les dimensions verticales de type 'plev7h' ou 'p850'
            if sd.label.startswith("p") and any(sd.label.endswith(s) for s in plev_sfxs) and sd.label != 'pl700' : 
                lwps=sv.label_without_psuffix
                if lwps:
                    present_in_ping=ping_refs.has_key(prefix+lwps) 
                    dummy_in_ping=None
                    if present_in_ping: dummy_in_ping=("dummy" in ping_refs[prefix+lwps]) 

                    if  present_in_ping and ( not dummy_in_ping or dummies=='include' ): 
                        sv.sdims[sd.label].is_zoom_of="union_plevs_"+lwps
                        if not dict_plevs.has_key(lwps):
                            dict_plevs[lwps]={sd.label:{sv.label:sv}}
                        else:
                            if not dict_plevs[lwps].has_key(sd.label):
                                dict_plevs[lwps].update({sd.label:{sv.label:sv}})
                            else:    
                                if sv.label not in dict_plevs[lwps][sd.label].keys(): 
                                    dict_plevs[lwps][sd.label].update({sv.label:sv})
                                else:
                                    #TBS# print sv.label,"in table",sv.mipTable,"already listed for",sd.label
                                    pass
                    else:
                        if printout: 
                            print "Info: ", lwps, "not taken into account for building plevs union axis because ",prefix+lwps,
                            if not present_in_ping : print  "is not an entry in the pingfile"
                            else : print "has a dummy reference in the pingfile"

                    # svar will be expected on a zoom axis of the union. Corresponding vertical dim must
                    # have a zoom_label named plevXX_<lwps> (multiple pressure levels) or pXX_<lwps> (single pressure level)
                    sv.sdims[sd.label].zoom_label='zoom_'+sd.label+"_"+lwps 
                else:
                    print "Warning: dim is pressure but label_without_psuffix=", lwps, \
                            "for",sv.label, sv.mipTable, sv.mip_era
            #else :
            #    print "for var %s/%s, dim %s is not related to pressure"%(sv.label,sv.label_without_psuffix,sd.label)
    #
    # Second, create xios axis for union of plevs
    union_axis_defs=axis_defs
    union_grid_defs=grid_defs
    #union_axis_defs={}
    #union_grid_defs={}
    for lwps in dict_plevs.keys():
        sdim_union=simple_Dim()
        plevs_union_xios=""
        plevs_union=set()
        for plev in dict_plevs[lwps].keys():  
            plev_values=[]
            for sv in dict_plevs[lwps][plev].values(): 
                if not plev_values:
                    # svar is the first one with this plev => get its level values
                    # on reecrase les attributs de sdim_union a chaque nouveau plev. Pas utile mais
                    # c'est la facon la plus simple de faire
                    sdsv=sv.sdims[plev]
                    if sdsv.stdname:   sdim_union.stdname=sdsv.stdname
                    if sdsv.long_name: sdim_union.long_name=sdsv.long_name
                    if sdsv.positive:  sdim_union.positive=sdsv.positive
                    if sdsv.out_name:  sdim_union.out_name=sdsv.out_name
                    if sdsv.units:     sdim_union.units=sdsv.units
                    if sdsv.requested: 
                        # case of multi pressure levels
                        plev_values=set(sdsv.requested.split())
                        sdim_union.is_union_for.append(sv.label+"_"+sd.label)
                    elif sdsv.value:
                        # case of single pressure level
                        plev_values=set(sdsv.value.split())
                        sdim_union.is_union_for.append(sv.label+"_"+sd.label)
                    else:
                        print "Warning: No requested nor value found for",svar.label,"with vertical dimesion",plev
                    plevs_union=plevs_union.union(plev_values)
                    if printout: print "    -- on",plev,":",plev_values 
                if printout: print "       *",sv.label,"(",sv.mipTable,")"
        list_plevs_union=list(plevs_union)
        list_plevs_union_num=[float(lev) for lev in list_plevs_union]
        list_plevs_union_num.sort(reverse=True)
        list_plevs_union=[str(lev) for lev in list_plevs_union_num]
        for lev in list_plevs_union: plevs_union_xios+=" "+lev
        if printout: print ">>> XIOS plevs union:", plevs_union_xios
        sdim_union.label="union_plevs_"+lwps
        if len(list_plevs_union)>1: sdim_union.requested=plevs_union_xios
        if len(list_plevs_union)==1: sdim_union.value=plevs_union_xios
        if printout : print "creating axis def for union :%s"%sdim_union.label
        axis_def=create_axis_def(sdim_union,lset,union_axis_defs,field_defs)
        create_grid_def(union_grid_defs,axis_def,sdim_union.out_name,
                        id2gridid(prefix+lwps,context_index))
    #
    #return (union_axis_defs,union_grid_defs)

def isVertDim(sdim):
    """
    Returns True if dim represents a dimension for which we want 
    an Xios interpolation. 
    For now, a very simple logics for interpolated vertical 
    dimension identification:
    """
    # SS : p840, p220 sont des couches de pression.  On les detecte par l'attribut value
    #test=(sdim.stdname=='air_pressure' or sdim.stdname=='altitude') and (sdim.value == "")
    test=(sdim.axis=='Z')
    return test

def analyze_cell_time_method(cm,label,table,printout=False):
    """
    Depending on cell method string CM, tells / returns
    - which time operation should be done 
    - if missing value detection should be set
    - if some cimatology has to be done (and its name - e.g. )

    We rely on the missing value detection to match the requirements like
    "where sea-ice", "where cloud" since we suppose fields required in this way
    are physically undefined oustide of "where something".
    """
    operation=None
    detect_missing=False
    clim=False
    #
    if cm is None : 
        if print_DR_errors :
            print "DR Error: cell_time_method is None for %15s in table %s, averaging" %(label,table)
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean (with samples weighted by snow mass)" in cm : 
        #[amnla-tmnsn]: Snow Mass Weighted (LImon : agesnow, tsnLi)
        cell_method_warnings.append(('Cannot yet handle time: mean (with samples weighted by snow mass)',label,table))
        if printout : 
            print "Will not explicitly handle time: mean (with samples weighted by snow mass) for "+\
                "%15s in table %s -> averaging"%(label,table)
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where cloud"  in cm : 
        #[amncl-twm]: Weighted Time Mean on Cloud (2 variables ISSCP 
        # albisccp et pctisccp, en emDay et emMon)
        cell_method_warnings.append(('Will not explicitly handle time: mean where cloud',label,table))
        if printout :
            print "Note : assuming that  "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #-------------------------------------------------------------------------------------
    elif "time: mean where sea_ice_melt_pound" in cm :
        #[amnnsimp-twmm]: Weighted Time Mean in Sea-ice Melt Pounds (uniquement des 
        #variables en SImon)
        cell_method_warnings.append(('time: mean where sea_ice_melt_pound',label,table))
        if printout :
            print "Note : assuming that 'time: mean where sea_ice_melt_pound' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #-------------------------------------------------------------------------------------------------
    elif "time: mean where sea_ice" in cm :
        #[amnsi-twm]: Weighted Time Mean on Sea-ice (presque que des 
        #variables en SImon, sauf sispeed et sithick en SIday)
        cell_method_warnings.append(('time: mean where sea_ice',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where sea_ice' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    elif "time: mean where sea"  in cm :#[amnesi-tmn]: 
        #Area Mean of Ext. Prop. on Sea Ice : pas utilisee
        print "time: mean where sea is not supposed to be used (%s,%s)"%(label,table)
    #-------------------------------------------------------------------------------------
    elif "time: mean where sea"  in cm :#[amnesi-tmn]: 
        #Area Mean of Ext. Prop. on Sea Ice : pas utilisee
        print "time: mean where sea is not supposed to be used (%s,%s)"%(label,table)
    #-------------------------------------------------------------------------------------
    elif "time: mean where floating_ice_shelf" in cm :
        #[amnfi-twmn]: Weighted Time Mean on Floating Ice Shelf (presque que des 
        #variables en Imon, Iyr, sauf sftflt en LImon !?)
        cell_method_warnings.append(('time: mean where floating_ice_shelf',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where floating_ice_shelf' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where grounded_ice_sheet" in cm :
        #[amngi-twm]: Weighted Time Mean on Grounded Ice Shelf (uniquement des 
        #variables en Imon, Iyr)
        cell_method_warnings.append(('time: mean where grounded_ice_sheet',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where grounded_ice_sheet' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where ice_sheet" in cm :
        #[amnni-twmn]: Weighted Time Mean on Ice Shelf (uniquement des 
        #variables en Imon, Iyr)
        cell_method_warnings.append(('time: mean where ice_sheet',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where ice_sheet' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where landuse" in cm :
        #[amlu-twm]: Weighted Time Mean on Land Use Tiles (uniquement des 
        #variables suffixees en 'Lut')
        cell_method_warnings.append(('time: mean where land_use',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where landuse' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where crops" in cm :
        #[amc-twm]: Weighted Time Mean on Crops (uniquement des 
        #variables suffixees en 'Crop')
        cell_method_warnings.append(('time: mean where crops',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where crops' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where natural_grasses" in cm :
        #[amng-twm]: Weighted Time Mean on Natural Grasses (uniquement des 
        #variables suffixees en 'Grass')
        cell_method_warnings.append(('time: mean where natural_grasses',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where natural_grasses' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where shrubs" in cm :
        #[ams-twm]: Weighted Time Mean on Shrubs (uniquement des 
        #variables suffixees en 'Shrub')
        cell_method_warnings.append(('time: mean where shrubs',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where shrubs' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where trees" in cm :
        #[amtr-twm]: Weighted Time Mean on Bare Ground (uniquement des 
        #variables suffixees en 'Tree')
        cell_method_warnings.append(('time: mean where trees',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where trees' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where vegetation" in cm :
        #[amv-twm]: Weighted Time Mean on Vegetation (pas de varibles concernees)
        cell_method_warnings.append(('time: mean where vegetation',label,table))
        if printout: 
            print "Note : assuming that 'time: mean where vegetation' "+\
                " for %15s in table %s is well handled by 'detect_missing'"\
                %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    elif "time: maximum within days time: mean over days" in cm :
        #[dmax]: Daily Maximum : tasmax Amon seulement
        if label != 'tasmax' and label != 'sfcWindmax' : 
            print "Error: issue with variable %s in table %s "%(label,table)+\
                "and cell method time: maximum within days time: mean over days"
        # we assume that pingfile provides a reference field which already implements "max within days" 
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: minimum within days time: mean over days" in cm :
        #[dmin]: Daily Minimum : tasmin Amon seulement
        if label != 'tasmin' : 
            print "Error: issue with variable %s in table %s  "%(label,table)+\
                "and cell method time: minimum within days time: mean over days"
        # we assume that pingfile provides a reference field which already implements "min within days" 
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean within years time: mean over years" in cm: 
        #[aclim]: Annual Climatology
        cell_method_warnings.append(('Cannot yet compute annual climatology - must do it as a postpro',label,table))
        if printout: 
            print "Cannot yet compute annual climatology for "+\
                "%15s in table %s -> averaging"%(label,table)
        # Could transform in monthly fields to be post-processed
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean within days time: mean over days"  in cm: 
        #[amn-tdnl]: Mean Diurnal Cycle
        cell_method_warnings.append(('File structure for diurnal cycle is not yet CF-compliant',label,table))
        operation="average"
        clim=True
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas 'Maximum Hourly Rate'
    elif "time: mean within hours time: maximum over hours"  in cm: 
        cell_method_warnings.append(('Cannot yet compute maximum hourly rate',label,table))
        if printout: 
            print "TBD: Cannot yet compute maximum hourly rate for "+\
                " %15s in table %s -> averaging"%(label,table)
            # Could output a time average of 24 hourly fields at 01 UTC, 2UTC ...
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: minimum" in cm :    
        #[tmin]: Temporal Minimum : utilisee seulement dans table daily
        operation="minimum"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: maximum" in cm :   
        #[tmax]: Time Maximum  : utilisee seulement dans table daily
        operation="maximum"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: sum"  in cm :
        # [tsum]: Temporal Sum  : pas utilisee !
        #print "Error: time: sum is not supposed to be used - Transformed to 'average' for %s in table %s"%(label,table)
        operation="accumulate"
    elif "time: mean" in cm :  #    [tmean]: Time Mean  
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: point" in cm:
        operation="instant"
    elif table=='fx' or table=='Efx' or table=='Ofx':
        operation="once"
    #----------------------------------------------------------------------------------------------------------------
    else :
        print "Warning: issue when analyzing cell_time_method "+\
            "%s for %15s in table %s, assuming it is once" %(cm,label,table)
        operation="once"
        
    if not operation: 
        #raise dr2xml_error("Fatal: bad xios 'operation' for %s in table %s: %s (%s)"%(sv.label,table,operation,sv.cell_methods))
        print("Fatal: bad xios 'operation' for %s in table %s: %s (%s)"%(label,table,operation,cm))
        operation="once"
    if not type(detect_missing)==type(bool()): 
        #raise dr2xml_error("Fatal: bad xios 'detect_missing_value' for %s in table %s: %s (%s)"%(sv.label,table,detect_missing,sv.cell_methods))
        print("Fatal: bad xios 'detect_missing_value' for %s in table %s: %s (%s)"%(label,table,detect_missing,cm))

    return (operation, detect_missing, clim)

#
def pingFileForRealmsList(settings, context,lrealms,svars,path_special,dummy="field_atm",
                          dummy_with_shape=False, exact=False,
                          comments=False,prefix="CV_",filename=None, debug=[]):
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
    name="" ; 
    for r in lrealms : name+="_"+r.replace(" ","%")
    lvars=[]
    for v in svars : 
        if exact :
            if any([ v.modeling_realm == r for r in lrealms]) : 
                lvars.append(v)
        else:
            var_realms=v.modeling_realm.split(" ")
            if any([ v.modeling_realm == r or r in var_realms
                     for r in lrealms]) :
                lvars.append(v)
        if context in settings['orphan_variables'] and \
           v.label in settings['orphan_variables'][context] :
            lvars.append(v)
    lvars.sort(key=lambda x:x.label_without_psuffix)

    # Remove duplicates : want to get one single entry for all variables having
    # the same label without psuffix, and one for each having different non-ambiguous label
    # Keep the one with the best piority
    uniques=[] ; best_prio=dict()
    for v in lvars :
        lna=v.label_non_ambiguous
        lwps=v.label_without_psuffix
        if (not lna in best_prio) or (lna in best_prio and v.Priority < best_prio[lna].Priority) :
            best_prio[lna]=v
        elif (not lwps in best_prio) or (lwps in best_prio and v.Priority < best_prio[lwps].Priority) :
            best_prio[lwps]=v
        #elif not v.label_without_psuffix in labels :
        #    uniques.append(v); labels.append(v.label_without_psuffix)
            
    #lvars=uniques
    lvars=best_prio.values()
    lvars.sort(key=lambda x:x.label_without_psuffix)
    #
    if filename is None : filename="ping"+name+".xml"
    if filename[-4:] != ".xml" : filename +=".xml"
    #
    if path_special: 
        specials=read_special_fields_defs(lrealms,path_special)
    else: 
        specials=False
    with open(filename,"w") as fp:
        fp.write('<!-- Ping files generated by dr2xml %s using Data Request %s -->\n'%(version,dq.version))
        fp.write('<!-- lrealms= %s -->\n'%`lrealms`)
        fp.write('<!-- exact= %s -->\n'%`exact`)
        fp.write('<!-- ')
        for s in settings : fp.write(' %s : %s\n'%(s,settings[s]))
        fp.write('--> \n\n')
        fp.write('<context id="%s">\n'%context)
        fp.write("<field_definition>\n")
        if settings.get("nemo_sources_management_policy_master_of_the_world",False) and context=='nemo':
            out.write('<field_group freq_op="_reset_ freq_offset="_reset_" >\n')
        if exact : 
            fp.write("<!-- for variables which realm intersects any of "\
                     +name+"-->\n")
        else:
            fp.write("<!-- for variables which realm equals one of "\
                     +name+"-->\n")
        for v in lvars :
            if v.label_non_ambiguous: 
                label=v.label_non_ambiguous
            else:
                label=v.label_without_psuffix
            if (v.label in debug) : print "pingFile ... processing %s in table %s, label=%s"%(v.label,v.mipTable,label)
                
            if specials and label in specials :
                line=ET.tostring(specials[label]).replace("DX_",prefix)
                #if 'ta' in label : print "ta is special : "+line
                line=line.replace("\n","").replace("\t","")
                fp.write('   '); fp.write(line)
            else:
                fp.write('   <field id="%-20s'%(prefix+label+'"')+\
                         ' field_ref="')
                if dummy : 
                    shape=highest_rank(v)
                    if v.label_without_psuffix=='clcalipso' : shape='XYA'
                    if dummy is True :
                        dummys="dummy"
                        if dummy_with_shape : dummys+="_"+shape
                    else : dummys=dummy
                    fp.write('%-18s/>'%(dummys+'"'))
                else : fp.write('?%-16s'%(label+'"')+' />')
            if comments :
                # Add units, stdname and long_name as a comment string
                if type(comments)==type("") : fp.write(comments)
                fp.write("<!-- P%d (%s) %s : %s -->"\
                         %(v.Priority,v.units, v.stdname, v.description)) 
            fp.write("\n")
        if 'atmos' in lrealms or 'atmosChem' in lrealms or 'aerosol' in lrealms :
            for tab in ["ap","ap_bnds","b","b_bnds" ] :
                fp.write('\t<field id="%s%s" field_ref="dummy_hyb" /><!-- One of the hybrid coordinate arrays -->\n'%(prefix,tab))
        if settings.get("nemo_sources_management_policy_master_of_the_world",False) and context=='nemo':
            out.write('</field_group>\n')
        fp.write("</field_definition>\n")
        #
        print "%3d variables written for %s"%(len(lvars),filename)
        #
        # Write axis_defs, domain_defs, ... read from relevant input/DX_ files
        if path_special:
            for obj in [ "axis", "domain", "grid" , "field" ] :
                copy_obj_from_DX_file(fp,obj,prefix,lrealms,path_special)
        fp.write('</context>\n')

def copy_obj_from_DX_file(fp,obj,prefix,lrealms,path_special) :
    # Insert content of DX_<obj>_defs files (changing prefix)
    #print "copying %s defs :"%obj,
    subrealms_seen=[]
    for realm in lrealms :
        for subrealm in realm.split() :
            if subrealm in subrealms_seen : continue
            subrealms_seen.append(subrealm)
            #print "\tand realm %s"%subrealm, 
            defs=DX_defs_filename(obj,subrealm,path_special)
            if os.path.exists(defs) :
                with open(defs,"r") as fields :
                    #print "from %s"%defs
                    fp.write("\n<%s_definition>\n"%obj)
                    lines=fields.readlines()
                    for line in lines :
                        if not obj+"_definition" in line:
                            fp.write(line.replace("DX_",prefix))
                    fp.write("</%s_definition>\n"%obj)
            else:
                pass
                print " no file :%s "%defs

def DX_defs_filename(obj,realm,path_special):
    #TBS# return prog_path+"/inputs/DX_%s_defs_%s.xml"%(obj,realm)
    return path_special+"/DX_%s_defs_%s.xml"%(obj,realm)

def get_xml_childs(elt, tag='field', groups=['context', 'field_group',
    'field_definition', 'axis_definition','axis', 'domain_definition',
    'domain', 'grid_definition', 'grid' , 'interpolate_axis'  ]) :
        """ 
        Returns a list of elements in tree ELT 
        which have tag TAG, by digging in sub-elements 
        named as in GROUPS 
        """
        if elt.tag in groups :
            rep=[]
            for child in elt : rep.extend(get_xml_childs(child,tag))
            return rep
        elif elt.tag==tag : return [elt]
        else :
            #print 'Syntax error : tag %s not allowed'%elt.tag
            # Case of an unkown tag : don't dig in
            return []

def read_xml_elmt_or_attrib(filename, tag='field', attrib=None, printout=False) :
    """ 
    Returns a dict of objects tagged TAG in FILENAME, which 
    - keys are ids
    - values depend on ATTRIB 
          * if ATTRIB is None : object (elt)
          * else : values of attribute ATTRIB  (None if field does not have attribute ATTRIB)
    Returns None if filename does not exist
    """
    #    
    rep=dict()
    if printout : print "processing file %s :"%filename,
    if os.path.exists(filename) :
        if printout : print "OK",filename
        root = ET.parse(filename).getroot()
        defs=get_xml_childs(root,tag) 
        if defs :
            for field in defs :
                if printout : print ".",
                key=field.attrib['id']
                if attrib is None: value=field
                else : value=field.attrib.get(attrib,None)
                rep[key]=value
            if printout : print
            return rep
    else :
        if printout : print "No file "
        return None

def read_special_fields_defs(realms,path_special,printout=False) :
    special=dict()
    subrealms_seen=[]
    for realm in realms  :
        for subrealm in realm.split() :
            if subrealm in subrealms_seen : continue
            subrealms_seen.append(subrealm)
            d=read_xml_elmt_or_attrib(DX_defs_filename("field",subrealm,path_special),\
                                        tag='field',printout=printout)
            if d: special.update(d)
    rep=dict()
    # Use raw label as key
    for r in special : rep[r.replace("DX_","")]=special[r]
    return rep

def highest_rank(svar):
    """Returns the shape with the highest needed rank among the CMORvars
    referencing a MIPvar with this label
    This, assuming dr2xml would handle all needed shape reductions
    """
    #mipvarlabel=svar.label_without_area
    mipvarlabel=svar.label_without_psuffix
    shapes=[];
    altdims=set()
    for  cvar in dq.coll['CMORvar'].items : 
        v=dq.inx.uid[cvar.vid]
        if v.label==mipvarlabel:
            try :
                st=dq.inx.uid[cvar.stid]
                try :
                    sp=dq.inx.uid[st.spid]
                    shape=sp.label
                except :
                    if print_DR_errors:
                        print "DR Error: issue with spid for "+\
                        st.label+" "+v.label+string(cvar.mipTable)
                    # One known case in DR 1.0.2: hus in 6hPlev
                    shape="XY"
                if "odims" in st.__dict__ :
                    try :
                        map(altdims.add,st.odims.split("|"))
                    except :
                        print "Issue with odims for "+v.label+" st="+st.label
            except :
                print "DR Error: issue with stid for :"+v.label+" in table section :"+str(cvar.mipTableSection)
                shape="?st"
        else:
            # Pour recuperer le spatial_shp pour le cas de variables qui n'ont
            # pas un label CMORvar de la DR (ex. HOMEvar ou EXTRAvar)
            shape=svar.spatial_shp
        if shape: shapes.append(shape)
    #if not shapes : shape="??"
    if len(shapes)==0 : shape="XY"
    elif any([ "XY-A"  in s for s in shapes]) : shape="XYA"
    elif any([ "XY-O" in s for s in shapes]) : shape="XYO"
    elif any([ "XY-AH" in s for s in shapes]) : shape="XYAh" # Zhalf
    elif any([ "XY-SN" in s for s in shapes]) : shape="XYSn" #snow levels
    elif any([ "XY-S" in s for s in shapes]) : shape="XYSo" #soil levels
    elif any([ "XY-P" in s for s in shapes]) : shape="XYA"
    elif any([ "XY-H" in s for s in shapes]) : shape="XYA"
    #
    elif any([ "XY-na" in s for s in shapes]) : shape="XY" # analyser realm, pb possible sur ambiguite singleton
    #
    elif any([ "YB-na" in s for s in shapes]) :shape="basin_zonal_mean"
    elif any([ "YB-O" in s for s in shapes]) : shape="basin_merid_section"
    elif any([ "YB-R" in s for s in shapes]) :
        shape="basin_merid_section_density"
    elif any([ "S-A" in s for s in shapes]) :  shape="COSP-A"
    elif any([ "S-AH" in s for s in shapes]) : shape="COSP-AH"
    elif any([ "na-A" in s for s in shapes]) : shape="site-A"
    elif any([ "Y-A"  in s for s in shapes]) : shape="XYA" #lat-A
    elif any([ "Y-P"  in s for s in shapes]) : shape="XYA" #lat-P
    elif any([ "Y-na" in s for s in shapes]) : shape="lat"
    elif any([ "TRS-na" in s for s in shapes]): shape="TRS"
    elif any([ "TR-na" in s for s in shapes]) : shape="TR"
    elif any([ "L-na" in s for s in shapes]) :  shape="COSPcurtain"
    elif any([ "L-H40" in s for s in shapes]) : shape="COSPcurtainH40"
    elif any([ "S-na" in s for s in shapes]) :  shape="XY" # fine once remapped
    elif any([ "na-na" in s for s in shapes]) : shape="0d" # analyser realm
    #else : shape="??"
    else : shape="XY"
    #
    for d in altdims:
        dims=d.split(' ')
        for dim in dims:
            shape+="_"+dim
    #
    return shape

def make_source_string(sources,source_id):
    """ 
    From the dic of sources in CMIP6-CV, Creates the string representation of a 
    given model (source_id) according to doc on global_file_attributes, so :

    <modified source_id> (<year>): atmosphere: <model_name> (<technical_name>, <resolution_and_levels>); ocean: <model_name> (<technical_name>, <resolution_and_levels>); sea_ice: <model_name> (<technical_name>); land: <model_name> (<technical_name>); aerosol: <model_name> (<technical_name>); atmospheric_chemistry <model_name> (<technical_name>); ocean_biogeochemistry <model_name> (<technical_name>); land_ice <model_name> (<technical_name>);

    """
    # mpmoine_correction:make_source_string: pour lire correctement le fichier 'CMIP6_source_id.json'
    source=sources[source_id] 
    components=source['model_component']
    rep=source_id+" ("+source['release_year']+"): "
    for realm in ["aerosol","atmos","atmosChem","land","ocean","ocnBgchem","seaIce"]:
        component=components[realm]
        description=component['description']
        if description!="none": rep=rep+"\n"+realm+": "+description
    return rep

def create_standard_domains(domain_defs):
    """
    Add to dictionnary domain_defs the Xios string representation for DR-standard horizontal grids, such as '1deg'

    """
    # Next definition is just for letting the workflow work when using option dummy='include'
    # Actually, ping_files for production run at CNRM do not activate variables on that grid (IceSheet vars)
    domain_defs['25km'] =create_standard_domain('25km',1440, 720)
    domain_defs['50km'] =create_standard_domain('50km', 720, 360)
    domain_defs['100km']=create_standard_domain('100km',360, 180)
    domain_defs['1deg'] =create_standard_domain('1deg', 360, 180)
    domain_defs['2deg'] =create_standard_domain('2deg', 180,  90)
    
def create_standard_domain(resol,ni,nj):
    return '<domain id="CMIP6_%s" ni_glo="%d" nj_glo="%d" type="rectilinear"  prec="8"> '%(resol,ni,nj) +\
        '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute" write_weight="true" /> '+\
        '</domain>  '
    #return '<domain id="CMIP6_%s" ni_glo="%d" nj_glo="%d" type="rectilinear"  prec="8" lat_name="lat" lon_name="lon" > '%(resol,ni,nj) +\
    #    '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute" write_weight="true" /> '+\
    #    '</domain>  '

    
def ping_alias(svar,lset,pingvars,error_on_fail=False):
    # dans le pingfile, grace a la gestion des interpolations
    # verticales, on n'attend pas forcement les alias complets des
    # variables (CMIP6_<label>), on peut se contenter des alias
    # reduits (CMIP6_<lwps>)

    # par ailleurs, si on a defini un label non ambigu alors on l'utilise
    # comme ping_alias (i.e. le field_ref)
    
    pref=lset["ping_variables_prefix"]
    if svar.label_non_ambiguous:
        #print "+++ non ambiguous", svar.label,svar.label_non_ambiguous
        alias_ping=pref+svar.label_non_ambiguous # e.g. 'CMIP6_tsn_land' and not 'CMIP6_tsn'
    else:
        #print "+++ ambiguous", svar.label
        # Ping file may provide the variable on the relevant pressure level - e.g. CMIP6_rv850
        alias_ping=pref+svar.label 
        if alias_ping not in pingvars :
            # if not, ping_alias is supposed to be without a pressure level suffix
            alias_ping=pref+svar.label_without_psuffix # e.g. 'CMIP6_hus' and not 'CMIP6_hus7h'
        #print "+++ alias_ping = ", pref, svar.label_without_psuffix, alias_ping
    if alias_ping not in pingvars :
        if error_on_fail :
            raise dr2xml_error("Cannot find an alias in ping for variable %s"%svar.label)
        else : return None
    return alias_ping

    
        
def RequestItemInclude(ri,var_label,freq) :
    """ 
    test if a variable is requested by a requestItem at a given freq
    """
    varGroup=dq.inx.uid[dq.inx.uid[ri.rlid].refid]
    reqVars=dq.inx.iref_by_sect[varGroup.uid].a['requestVar']
    cmVars=[ dq.inx.uid[dq.inx.uid[reqvar].vid] for reqvar in reqVars ]
    return any( [ cmv.label==var_label and cmv.frequency==freq for cmv in cmVars ])

def endyear_for_CMORvar(dq,cv,expt,year,lset,sset,printout=False): 
    """ 
    For a CMORvar, returns the largest year in the time slice(s)  
    of those requestItems which apply for experiment EXPT and which 
    include YEAR. If no time slice applies, returns None 
    """ 
    # 1- Get the RequestItems which apply to CmorVar 
    # 2- Select those requestItems which include expt,
    #    and retain their endyear if larger than former one
 
    global global_rls

    # Some debug material
    if False and (cv.label=="clc" ) : printout=True
    if printout  : print "In end_year for %s %s"%(cv.label,cv.mipTable)
    pmax=sset.get('max_priority',lset.get('max_priority'))
    
    # 1- Get the RequestItems which apply to CmorVar
    rVarsUid=dq.inx.iref_by_sect[cv.uid].a['requestVar']
    rVars=[ dq.inx.uid[uid] for uid in rVarsUid if dq.inx.uid[uid].priority <= pmax ]
    if printout : print "les requestVars:" , [ rVar.title for rVar in rVars ]
    VarGroups=[ dq.inx.uid[rv.vgid] for rv in rVars ] 
    if printout : print "les requestVars groups:" , [ rVg.label for rVg in VarGroups ]
    RequestLinksId=[]
    for vg in VarGroups: 
        RequestLinksId.extend(dq.inx.iref_by_sect[vg.uid].a['requestLink'])
    FilteredRequestLinks=[ ]
    for rlid in RequestLinksId :
        rl=dq.inx.uid[rlid] 
        if rl in global_rls :
            FilteredRequestLinks.append(rl)
    if printout : print "les requestlinks:" , [ dq.inx.uid[rlid].label for rlid in RequestLinksId ]
    if printout : print "les FilteredRequestlinks:" , [ rl.label for rl in FilteredRequestLinks ]
    RequestItems=[] 
    for rl in FilteredRequestLinks : 
        RequestItems.extend(dq.inx.iref_by_sect[rl.uid].a['requestItem']) 
    if printout : print "les requestItems:" , [ dq.inx.uid[riid].label for riid in RequestItems ]
 
    # 2- Select those request links which include expt and year
    larger=None
    for riid in RequestItems : 
        ri=dq.inx.uid[riid] 
        applies,endyear=RequestItem_applies_for_exp_and_year(ri,expt,lset,sset,year,debug=printout)
        if printout :
            print "For var and freq selected for debug and year %d, for ri %s, applies=%s, endyear=%s"%\
                (year,ri.title, `applies`,`endyear`)
        if applies :
            if endyear is None:  return None # One of the timeslices cover the whole expt
            else : larger=max(larger,endyear)
    return larger


def get_source_id_and_type(sset,lset):
    if "configuration" in sset and "configurations" in lset :
        if sset["configuration"] in lset["configurations"]: 
            source_id,source_type,unused=lset["configurations"][sset["configuration"]]
        else:
            raise dr2xml_error("configuration %s is not known (allowed values are :)"%\
                         sset["configuration"]+`lset["configurations"]`)
    else:
        source_id=sset['source_id']
        if 'source_type' in sset :
            source_type=sset['source_type']
        else:
            if 'source_types' in lset :
                source_type=lset['source_types'][source_id] 
            else:
                raise dr2xml_error("Fatal: No source-type found - Check inputs")
    return source_id,source_type

def realm_is_processed(realm, source_type) :
    """ 
    Tells if a realm is definitely not processed by a source type 

    list of source-types : AGCM BGC AER CHEM LAND OGCM AOGCM
    list of known realms : ['seaIce', '', 'land', 'atmos atmosChem', 'landIce', 'ocean seaIce', 
                            'landIce land', 'ocean', 'atmosChem', 'seaIce ocean', 'atmos', 
                             'aerosol', 'atmos land', 'land landIce', 'ocnBgChem']
    """
    components=source_type.split(" ")
    rep=True
    #
    if realm=="atmosChem" and 'CHEM' not in components : return False
    if realm=="aerosol"   and 'AER'  not in components : return False
    if realm=="ocnBgChem" and 'BGC'  not in components : return False
    #
    with_ocean= ('OGCM' in components or 'AOGCM' in components)
    if 'seaIce' in realm and not with_ocean : return False
    if 'ocean'  in realm and not with_ocean : return False
    #
    with_atmos= ('AGCM' in components or 'AOGCM' in components)
    if 'atmos'  in realm and not with_atmos : return False 
    if 'atmosChem' in realm and not with_atmos : return False 
    if realm=='' and not with_atmos : return False #In DR 01.00.15 : some atmos variables have realm=''
    #
    with_land= with_atmos or ('LAND' in components)
    if 'land'   in realm and not with_land  : return False
    #
    return rep

def guess_simple_domain_grid_def(grid_id,lset):
    # dr2xml sometimes must be able to restconstruct the grid def for a grid which has
    # just a domain, from the grid_id, using a regexp with a numbered group that matches
    # domain_name in grid_id. Second item is group number
    regexp=lset["simple_domain_grid_regexp"]
    domain_id,n=re.subn(regexp[0],r'\%d'%regexp[1],grid_id)
    if n != 1 :
        raise dr2xml_error("Cannot identify domain name in grid_id %s using regexp %s"%\
                     (grid_id,regexp[0]))
    grid_def='<grid id="%s" ><domain domain_ref="%s"/></grid>'% (grid_id,domain_id)
    print("Warning: Guess that structure for grid %s is : %s"%(grid_id,grid_def))
    #raise dr2xml_error("Warning: Guess that structure for grid %s is : %s"%(grid_id,grid_def))
    return grid_def

def get_grid_def(grid_id,grid_defs,lset=None):
    if grid_id in grid_defs :
        # Simple case : already stored
        grid_def=grid_defs[grid_id]
    else:
        if grid_id in context_index :
            # Grid defined through xml  
            grid_def=ET.tostring(context_index[grid_id])
        else:
            if lset is not None :
                # Try to guess a grid_def from its id
                grid_def=guess_simple_domain_grid_def(grid_id,lset)
                grid_defs[grid_id]=grid_def
            else:
                raise dr2xml_error("Cannot guess a grid def for %s"%grid_id)
                grid_def=None
    return grid_def

def check_for_file_input(sv,lset,hgrid,pingvars,field_defs,grid_defs,\
                         domain_defs,file_defs, printout=False):
    """
    

    Add an entry in pingvars
    """
    externs=lset.get('fx_from_file',[])
    #print "/// sv.label=%s"%sv.label, sv.label in externs ,"hgrid=",hgrid
    if sv.label in externs and \
       any( [ d==hgrid for d in externs[sv.label] ]) :
        pingvar=lset['ping_variables_prefix']+sv.label
        pingvars.append(pingvar)
        # Add a grid made of domain hgrid only
        grid_id="grid_"+hgrid
        grid_def='<grid id="%s"><domain domain_ref="%s"/></grid>\n'%(grid_id,hgrid)
        #grid_defs[grid_id]=grid_def
        #context_index[grid_id]=ET.fromstring(grid_def)

        # Add a grid and domain for reading the file (don't use grid above to avoid reampping)
        file_domain_id="remapped_%s_file_domain"%sv.label
        domain_defs[file_domain_id]='<domain id="%s" type="rectilinear" >'%file_domain_id +\
            '<generate_rectilinear_domain/></domain>'
        file_grid_id="remapped_%s_file_grid"%sv.label
        grid_defs[file_grid_id]='<grid id="%s"><domain domain_ref="%s"/></grid>\n'%(file_grid_id,file_domain_id)
        if printout : print domain_defs[file_domain_id]
        if printout : print grid_defs[file_grid_id]
        
        # Create xml for reading the variable
        filename=externs[sv.label][hgrid][grid_choice]
        file_id="remapped_%s_file"%sv.label
        field_in_file_id="%s_%s"%(sv.label,hgrid)
        #field_in_file_id=sv.label
        file_def='\n<file id="%s" name="%s" mode="read" output_freq="1ts" enabled="true" >'%\
              (         file_id,filename)
        file_def+= '\n\t<field id="%s" name="%s" operation="instant" freq_op="1ts" freq_offset="1ts" grid_ref="%s"/>'%\
              ( field_in_file_id,        sv.label,                     file_grid_id)
        file_def+='\n</file>'
        file_defs[file_id]=file_def
        if printout : print file_defs[file_id]
        #
        #field_def='<field id="%s" grid_ref="%s" operation="instant" >%s</field>'%\
        field_def='<field id="%s" grid_ref="%s" field_ref="%s" operation="instant" freq_op="1ts" freq_offset="0ts" />'%\
            (             pingvar,grid_id,       field_in_file_id)
        field_defs[field_in_file_id]=field_def
        context_index[pingvar]=ET.fromstring(field_def)

        if printout : print field_defs[field_in_file_id]
        #

       

class dr2xml_error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
    def __str__(self):
        return "\n\n"+`self.valeur`+"\n\n"
    #""" just for test"""
