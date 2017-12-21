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
#    svn co http://proj.badc.rl.ac.uk/svn/exarch/CMIP6dreq/tags/01.00.01
#    (and must include 01.00.01/dreqPy in PYTHONPATH)
from scope import dreqQuery
import dreq

# 2- CMIP6 Controled Vocabulary (available from 
# https://github.com/WCRP-CMIP/CMIP6_CVs). You will provide its path 
# as argument to functions defined here

# 3- XIOS release must be 1242 or above (to be fed with the outputs)
#  see https://forge.ipsl.jussieu.fr/ioserver/wiki

####################################
# End of pre-requisites
####################################

version="0.25"
print "* dr2xml version: ", version

conventions="CF-1.7 CMIP-6.2" 
# The current code should comply with this version of spec doc at
# https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit
CMIP6_conventions_version="v6.2.4"
print "CMIP6 conventions version: "+CMIP6_conventions_version

import datetime
import re
import json
import collections
import sys,os
import xml.etree.ElementTree as ET

# mpmoine_merge_dev2_v0.12: posixpath.dirname ne marche pas chez moi
#TBS# from os import path as os_path
#TBS# prog_path=os_path.abspath(os_path.split(__file__)[0])

# Local packages
from vars import simple_CMORvar, simple_Dim, process_homeVars, complement_svar_using_cmorvar, \
                multi_plev_suffixes, single_plev_suffixes, get_simplevar
from grids import decide_for_grids, DRgrid2gridatts,\
    split_frequency_for_variable, timesteps_per_freq_and_duration
from Xparse import init_context, id2grid

# A auxilliary tables
from table2freq import table2freq, table2splitfreq, cmipFreq2xiosFreq

print_DR_errors=True
print_multiple_grids=False

dq = dreq.loadDreq()
print "* CMIP6 Data Request version: ", dq.version

cell_method_warnings=[]
sn_issues=dict()
context_index=None

# global variable : the list of Request Links which apply for 'our' MIPS and which are not explicitly excluded using settings
# It is set in select_CMORvars_for_lab and used in endyear_for_CMORvar
global_rls=None  

# CFsites-related elements (CFMIP)
# A file named cfsites_grid_file_name must be provided at runtime, which
# includes a field named cfsites_grid_field_id, defined on a unstructured 
# grid which is composed of CF sites
cfsites_radix         ="cfsites"
cfsites_domain_id     =cfsites_radix+"_domain"
cfsites_grid_id       =cfsites_radix+"_grid"
cfsites_grid_file_name=cfsites_radix+"_grid"
cfsites_grid_file_id  =cfsites_radix+"_file"
cfsites_grid_field_id =cfsites_radix+"_field"
# Next variable is used to circumvent an Xios 1270 shortcoming. Xios
# should read that value in the datafile. Actually, it did, in some
# earlier version ...

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
    'vars_OK' : dict(),
    # A per-variable dict of comments valid for all simulations
    'comments'     : {
        'rld' : 'nothing special about this variable'
        },
    #
    'grid_choice' : { "CNRM-CM6-1" : "LR", "CNRM-CM6-1-HR" : "HR",
                      "CNRM-ESM2-1": "LR"  , "CNRM-ESM2-1-HR": "HR" },
    # Sizes for atm and oce grids (cf DR doc); Used for computing file split frequency
    "sizes"  : { "LR" : [292*362  , 75, 128*256, 91, 30, 14, 128],
                 "HR" : [1442*1021, 75, 720*360, 91, 30, 14, 128] },
    #
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
    #              - resolution of the production grid (using CMIP6 conventions),
    #              - grid description
    "grids" : {
        
      "LR"    : {
        "surfex" : [ "gr","complete" , "250 km", "data regridded to a T127 gaussian grid (128x256 latlon) from a native atmosphere T127l reduced gaussian grid"] ,
          "trip" : [ "gn", ""        ,  "50 km" , "regular 1/2 deg lat-lon grid" ],
          "nemo" : [ "gn", ""        , "100 km" , "native ocean tri-polar grid with 105 k ocean cells" ],},
        
      "HR"    : {
        "surfex" : [ "gr","complete" , "50 km", "data regridded to a 359 gaussian grid (180x360 latlon) from a native atmosphere T359l reduced gaussian grid"] ,
          "trip" : [ "gn", ""        ,  "50 km" , "regular 1/2 deg lat-lon grid" ],
          "nemo" : [ "gn", ""        ,  "25 km" , "native ocean tri-polar grid with 1.47 M ocean cells" ],},
    },
    #        
    # Basic sampling timestep set in your field definition (used to feed metadata 'interval_operation')
    "sampling_timestep" : {
              "LR"    : { "surfex":900., "nemo":1800. },
              "HR"    : { "surfex":900., "nemo":1800. },
    },

    # We create sampled time-variables for controlling the frequency of vertical interpolations
    "vertical_interpolation_sample_freq" : "3h",

    #--- Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR
    "use_union_zoom" : False,

    # The CMIP6 frequencies that are unreachable for a single model run. Datafiles will
    # be labelled with dates consistent with content (but not with CMIP6 requirements).
    # Allowed values are only 'dec' and 'yr'
    "too_long_periods" : ["dec", "yr" ] ,

    # Describe the branching scheme for experiments involved in some 'branchedYears type' tslice
    # Just put the start year in child and the start years in parent for all members
    "branching" : { "historical" : (1850, [ 2350, 2400, 2450 ]) },

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
                                        # This is an alternative to using "branch_time_in_parent"
    #"branch_time_in_parent": "365.0D0", # a double precision value, in days, used if branch_year_in_parent is not applicable
                                         # This is an alternative to using "branch_year_in_parent"
    #'parent_time_units'    : "" #in case it is not the same as child time units

    "branch_year_in_child" : 1850,      # if your calendar is Gregorian, you can specify the branch year in child directly
                                        # This is an alternative to using "branch_time_in_child"
    'child_time_ref_year'  : 1850,      # MUST BE CONSISTENT WITH THE TIME UNITS OF YOUR MODEL(S) !!!
                                        # (this is not necessarily the parent start date)
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
    if (debug) : print "Checking ","% 15s"%ri.label,
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
                   group_id.label,
                ri_applies_to_experiment=True
    elif item_exp._h.label== 'mip' :
        if (debug)  : print "%20s"%"Mip case ",dq.inx.uid[mip_id].label,
        exps_id=dq.inx.iref_by_sect[ri.esid].a['experiment']
        for e in [ dq.inx.uid[eid] for eid in exps_id ] :
            if (debug) :  print e.label,",",
            if e.label==experiment : 
                if (debug) :  print " OK for experiment based on mip"+ mip_id.label,
                ri_applies_to_experiment=True
    else :
        if (debug)  :
            print "Error on esid link for ri : %s uid=%s %s"%\
                           ( ri.title, ri.uid, item_exp._h.label)
    if ri_applies_to_experiment :
        if year is None :
            rep=True ; endyear=None
        else :
            rep,endyear=year_in_ri(ri,experiment,lset,sset,year,debug=debug)
        return rep,endyear
    else : return False,None


def year_in_ri(ri,experiment,lset,sset,year,debug=False):
    if 'tslice' in ri.__dict__ :
        rep,endyear=year_in_ri_tslice(ri,experiment,lset,year,debug=debug)
        return rep,endyear
    try :
        ny=int(ri.nymax)
        first_year=sset["branch_year_in_child"]
        if (ny > 0) : endyear=first_year+ny-1
        else :
            # assume that it means : whole experiment duration
            # TBD : year_in_ri : endyear is not meaningful for some cases
            endyear=first_year+10000
        applies=(year <= endyear)
        return applies,endyear
    except:
        print "Cannot tell if year %d applies to reqItem %s -> assumes yes"%(year,ri.title)
        return True,None
        
    
def year_in_ri_tslice(ri,experiment,lset,year,debug=False):
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
        #start_year=experiment_start_year(experiment)
        # TBD : code experiment_start_year (used for VolMIP : _slice_VolMIP3)
        start_year=1850
        relevant= (year >= start_year and year < start_year+nyear)
        endyear=start_year + nyear - 1
    elif tslice.type=="monthlyClimatology": # e.g. _slice_clim20
        relevant = (year >= tslice.start and year<=tslice.end)
        endyear=tslice.end
    elif tslice.type=="branchedYears" : # e.g. _slice_piControl020
        if tslice.child in lset["branching"] :
            endyear=False
            (refyear,starts)=lset["branching"][tslice.child]
            for start in starts :
                if ((year - start >= tslice.start - refyear) and \
                    (year - start < tslice.start - refyear + tslice.nyears )):
                    relevant=True
                    lastyear=start+tslice.nyears-1
                    if endyear is False : endyear=lastyear
                    else : endyear=max(endyear,lastyear)
        else : dr2xml_error("For tslice %s, child %s start year is not documented"%\
                                (tslice.title, tslice.child))
    else :
        dr2xml_error("type %s for time slice %s is not handled"%(tslice.type,tslice.title))
    if (debug) :
        print "for year %d and experiment %s, relevant is %s for tslice %s of type %s, endyear=%s"%\
            (year,experiment,`relevant`,ri.title,tslice.type,`endyear`)
    return relevant,endyear


def select_CMORvars_for_lab(lset, sset=None, year=None,printout=False):
    """
    A function to list CMOR variables relevant for a lab (and also, 
    optionnally for an experiment and a year)
    
    Args:
      lset (dict): laboratory settings; used to provide the list of MIPS,  
                   the max Tier, and a list of excluded variable names
      sset (dict): simulation settings, used for indicating source_type, 
                   max priority (and for filtering on the simulation if 
                   year is notNone)
                   if sset is None, use union of mips among all grid choices 
      year (int,optional) : simulation year - used to filter the request 
                   for an experiment and a year

    Returns:
      A list of 'simplified CMOR variables'
    
    """
    #
    # From MIPS set to Request links
    global sc,global_rls,grid_choice
    if sset and 'tierMax' in sset : tierMax=sset['tierMax']
    else: tierMax=lset['tierMax']
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
    #
    excluded_rls=[]
    inclinks=lset.get("included_request_links",[])
    if len(inclinks) > 0 :
        for rl in rls_for_mips :
            if rl.label not in inclinks : excluded_rls.append(rl)
        for rl in excluded_rls :
            print "RequestLink %s is not included"%rl.label
            rls_for_mips.remove(rl)
    #
    if sset and year :
        experiment_id=sset['experiment_id']
        #print "Request links before filter :"+`[ rl.label for rl in rls_for_mips ]`
        filtered_rls=[]
        for rl in rls_for_mips :
            # Access all requesItems ids which refer to this RequestLink
            ri_ids=dq.inx.iref_by_sect[rl.uid].a['requestItem']
            for ri_id in ri_ids :
                ri=dq.inx.uid[ri_id]
                #print "Checking requestItem ",ri.label
                applies,endyear= RequestItem_applies_for_exp_and_year(ri,
                                 experiment_id, lset,sset,year,False)
                if applies:
                    #print "% 25s"%ri.label," applies "
                    filtered_rls.append(rl)
        rls=filtered_rls
        if printout :
            print "Number of Request Links which apply to experiment ", \
                experiment_id,"and MIPs", mips_list ," is: ",len(rls)
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
    if printout :
        print 'Number of (CMOR variable, grid) pairs for these requestLinks is :%s'%len(miprl_vars_grids)
    #
    inctab=lset.get("included_tables",[])
    exctab=lset.get("excluded_tables",[])
    incvars=lset.get('included_vars',[])
    excvars=lset.get('excluded_vars',[])
    if sset :
        config=sset['configuration']
        if ('excluded_vars_per_config' in lset) and \
           (config in lset('excluded_vars_per_config')):
            excvars.extend(lset['excluded_vars_per_config'][config])
    
    filtered_vars=[]
    for (v,g) in miprl_vars_grids : 
        cmvar=dq.inx.uid[v]
        ttable=dq.inx.uid[cmvar.mtid]
        mipvar=dq.inx.uid[cmvar.vid]
        if ((len(incvars) == 0 and mipvar.label not in excvars) or\
            (len(incvars) > 0 and mipvar.label in incvars))\
            and \
           ((len(inctab)>0 and ttable.label in inctab) or \
            (len(inctab)==0 and ttable.label not in exctab)):
            filtered_vars.append((v,g))
            if (ttable.label=="Oclim") : print "for var %s, ttable=%s"%(cmvar.label,ttable.label)
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
        multiple_grids.sort()
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
    for v in d :
        svar = simple_CMORvar()
        cmvar = dq.inx.uid[v]
        complement_svar_using_cmorvar(svar,cmvar,dq,sn_issues)
        svar.Priority=analyze_priority(cmvar,mips_list)
        svar.grids=d[v]
        simplified_vars.append(svar)
    print '\nNumber of simplified vars is :',len(simplified_vars)
    print "Issues with standard names are :"
    for iss in sn_issues : print "\t"+iss+" vars : "+`sn_issues[iss]`
    
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
            val=val.replace(">","&gt").replace("<","&lt").replace("&","&amp").replace("'","&apos").replace('"',"&quot").strip()
        if num_type != "string" or len(val) > 0 :
            out.write('  <variable name="%s"  type="%s" > %s '%(key,num_type,val))
            out.write('  </variable>\n')

def freq2datefmt(in_freq,operation,lset):
    # WIP doc v6.2.3 - Apr. 2017: <time_range> format is frequency-dependant 
    datefmt=False
    offset=None
    freq=in_freq
    if freq == "dec":
        if "dec" not in lset.get("too_long_periods",[]) :
            datefmt="%y"
            if operation in ["average","minimum","maximum"] : offset="5y"
            else : offset="10y"
        else : freq="yr" #Ensure dates in filenames are consistent with content, even if not as required
    if freq == "yr":
        if "yr" not in lset["too_long_periods"] :
            datefmt="%y"
            if operation in ["average","minimum","maximum"] : offset=False
            else : offset="1y"
        else : freq="mon" #Ensure dates in filenames are consistent with content, even if not as required
    if freq in ["mon","monClim"]:
        datefmt="%y%mo"
        if operation in ["average","minimum","maximum"] : offset=False
        else : offset="1mo"
    elif freq=="day":
        datefmt="%y%mo%d"
        if operation in ["average","minimum","maximum"] : offset="12h"
        else : offset="1d"
    elif freq=="5day":
        datefmt="%y%mo%d"
        if operation in ["average","minimum","maximum"] : offset="60h"
        else : offset="5d"
    elif freq in ["6hr","6hrPt","3hr","3hrPt","3hrClim","1hr","hr","1hrClimMon"]: 
        datefmt="%y%mo%d%h%mi"
        if freq=="6hr" or freq=="6hrPt":
            if operation in ["average","minimum","maximum"] : offset="3h"
            else : offset="6h"
        elif freq in [ "3hr", "3hrPt", "3hrClim"] :
            if operation in ["average","minimum","maximum"] : offset="90mi"
            else : offset="3h"
        elif freq in ["1hr", "1hrClimMon"]: 
            if operation in ["average","minimum","maximum"] : offset="30mi"
            else : offset="1h"
    elif freq=="subhr" or freq=="subhrPt":
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

def write_xios_file_def(cmv,year,table,lset,sset,out,cvspath,
                        field_defs,axis_defs,grid_defs,domain_defs,
                        dummies,skipped_vars_per_table,
                        prefix,context,grid,pingvars=None,enddate=None,
                        attributes=[],debug=[]) :
    """ 
    Generate an XIOS file_def entry in out for :
      - a dict for laboratory settings 
      - a dict of simulation settings 
      - a 'simplifed CMORvar' cmv
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
    global sc

    # gestion des attributs pour lesquels on a recupere des chaines vides (" " est Faux mais est ecrit " "")
    #--------------------------------------------------------------------
    # Set to NOT-SET field attributes that can be empty strings
    #--------------------------------------------------------------------
    if not cmv.stdname       : cmv.stdname       = "DR-ISSUE"
    if not cmv.long_name     : cmv.long_name     = "DR-ISSUE"
    if not cmv.cell_methods  : cmv.cell_methods  = "DR-ISSUE"
    if not cmv.cell_measures : cmv.cell_measures = "DR-ISSUE"
    if not cmv.stdunits      : cmv.stdunits      = "DR-ISSUE"

    #--------------------------------------------------------------------
    # Define alias for field_ref in file-def file 
    # - may be replaced by alias1 later
    # - this is not necessarily the alias used in ping file because of
    #   intermediate field id(s) due to union/zoom
    #--------------------------------------------------------------------
    # We use a simple convention for variable names in ping files : 
    if cmv.type=='perso' : alias=cmv.label
    else:
        # MPM : si on a defini un label non ambigu alors on l'utilise comme alias (i.e. le field_ref) 
        # et pour l'alias seulement (le nom de variable dans le nom de fichier restant svar.label)
        if cmv.label_non_ambiguous: alias=lset["ping_variables_prefix"]+cmv.label_non_ambiguous
        else:
            # 'tau' is ambiguous in DR 01.00.18 : either a variable name (stress)
            # or a dimension name (optical thickness). We choose to rename the stress
            if cmv.label != "tau" :
                alias=lset["ping_variables_prefix"]+cmv.label
            else:
                alias=lset["ping_variables_prefix"]+"tau_stress"
        if (cmv.label in debug) : print "write_xios_file_def ... processing %s, alias=%s"%(cmv.label,alias)
        
        # TBD mpmoine_correction: suppression des terminaisons en "Clim" pour l'alias 
        split_alias=alias.split("Clim")
        alias=split_alias[0]
        if pingvars is not None :
            # Get alias without pressure_suffix but possibly with area_suffix
            alias_ping=ping_alias(cmv,lset,pingvars)
            if not alias_ping in pingvars:
                if skipped_vars_per_table.has_key(cmv.mipTable) and skipped_vars_per_table[cmv.mipTable]:
                    list_of_skipped=skipped_vars_per_table[cmv.mipTable]
                    list_of_skipped.append(cmv.label+"("+str(cmv.Priority)+")")
                else:
                    list_of_skipped=[cmv.label]
                skipped_vars_per_table.update({cmv.mipTable:list_of_skipped})
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
    mip_era=cmv.mip_era
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
        grid_label,target_hgrid_id,grid_resolution,grid_description=\
                lset['grids'][grid_choice][context]
    else:
        if grid == 'cfsites' :
            target_hgrid_id=cfsites_domain_id
        else:
            target_hgrid_id=lset["ping_variables_prefix"]+grid
        grid_label,grid_resolution,grid_description=DRgrid2gridatts(grid)
    if table in [ 'AERMonZ',' EmonZ', 'EdayZ' ] : grid_label+="z"
    if "Ant" in table : grid_label+="a"
    if "Gre" in table : grid_label+="g"
    #
    with open(cvspath+project+"_experiment_id.json","r") as json_fp :
        CMIP6_experiments=json.loads(json_fp.read())['experiment_id']
        if not CMIP6_experiments.has_key(sset['experiment_id']):
            dr2xml_error("Issue getting experiment description in CMIP6 CV for %20s"%sset['experiment_id'])
        expname=sset['experiment_id']
        expid_in_filename=sset.get('expid_in_filename',expname) 
        exp_entry=CMIP6_experiments[expname]
        experiment=exp_entry['experiment']
        description=exp_entry['description']
        activity_id=exp_entry['activity_id']
        parent_activity_id=exp_entry['parent_activity_id']
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
                (c,experiment,`actual_components`)
    for c in actual_components :
        if c not in allowed_components and c not in required_components :
            #ok=False # TBD : restore blocking on non-allowed components
            print "Warning : Model component %s is present but not required nor allowed (%s)"%\
                (c,`allowed_components` )
    if not ok : raise dr2xml_error("Issue with model components")
    #
    #--------------------------------------------------------------------
    # Set NetCDF output file name according to the DRS
    #--------------------------------------------------------------------
    #
    date_range="%start_date%-%end_date%" # XIOS syntax
    operation,detect_missing = analyze_cell_time_method(cmv.cell_methods,cmv.label,table,printout=False)
    #print "--> ",cmv.label, cmv.frequency, table
    date_format,offset_begin,offset_end=freq2datefmt(cmv.frequency,operation,lset)
    #
    if "fx" in cmv.frequency:
        filename="%s%s_%s_%s_%s_%s_%s"%\
                   (prefix,cmv.label,table,source_id,expid_in_filename, member_id,grid_label)
    else:
        # mpmoine: WIP doc v6.2.3 : a suffix "-clim" should be added if climatology
        # TBD : for the time being, we should also have attribute 'climatology' for dimension 'time', but we cannot -> forget temporarily about this extension
        if False and "Clim" in cmv.frequency: suffix="-clim"
        else: suffix=""
        filename="%s%s_%s_%s_%s_%s_%s_%s%s"%\
            (prefix,cmv.label,table,source_id,expid_in_filename,
             member_id,grid_label,date_range,suffix)
    #
    further_info_url="https://furtherinfo.es-doc.org/%s.%s.%s.%s.%s.%s"%(
        mip_era,institution_id,source_id,expid_in_filename,
        sub_experiment_id,variant_label)
    #
    #--------------------------------------------------------------------
    # Compute XIOS split frequency
    #--------------------------------------------------------------------
    grid=lset['grid_choice'][source_id]
    split_freq=split_frequency_for_variable(cmv, lset, grid, sc.mcfg, context)
    #
    #--------------------------------------------------------------------
    # Write XIOS file node:
    # including global CMOR file attributes
    #--------------------------------------------------------------------
    out.write(' <file id="%s_%s_%s" name="%s" '%(cmv.label,table,grid_label,filename))
    out.write(' output_freq="%s" '%cmipFreq2xiosFreq[cmv.frequency])
    out.write(' append="true" ')
    out.write(' output_level="%d" '%lset.get("output_level",10))
    out.write(' compression_level="%d" '%lset.get("compression_level",0))
    if not "fx" in cmv.frequency :
        out.write(' split_freq="%s" '%split_freq)
        out.write(' split_freq_format="%s" '%date_format)
        #
        # Modifiers for date parts of the filename, due to silly KT conventions. 
        if offset_begin is not False :
            out.write(' split_start_offset="%s" ' %offset_begin)
        if offset_end is not False  :
            out.write(' split_end_offset="%s" '%offset_end)
        # Try to get enddate for the CMOR variable from the DR
        lastyear=None
        if cmv.cmvar is not None :
            lastyear=endyear_for_CMORvar(dq,cmv.cmvar,expname,year,lset)
        #print "lastyear=",lastyear," enddate=",enddate
        if lastyear is None or lastyear >= int(enddate[0:4]) :
            # Use run end date as the latest possible date
            # enddate must be 20140101 , rather than 20131231
            endyear=enddate[0:4]
            endmonth=enddate[4:6]
            endday=enddate[6:8]
        else:
            # Use requestItems-based end date as the latest possible date when it is earlier than run end date
            print "split_last_date year %d derived from DR for variable %s in table %s"%(lastyear,cmv.label,table)
            endyear="%04s"%(lastyear+1)
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
    wr(out,'activity_id',reduce(lambda x,y : x+" "+y, activity_id))
    #
    if contact and contact is not "" : wr(out,'contact',contact) 
    wr(out,'data_specs_version',dq.version) 
    wr(out,'dr2xml_version',version) 
    #
    wr(out,'experiment_id',expid_in_filename)
    if experiment_id != expid_in_filename :
        wr(out,'description',description)
        wr(out,'title',description)
        wr(out,'experiment',experiment)
    # 
    # TBD: check external_variables
    # Let us yet hope that all tables but those with an 'O'
    # as first letter require areacella, and the others require areacello
    external_variables= "areacella" 
    if table[0]=='O' or table[0:1]=='SI' : external_variables= "areacello" 
    if 'fx' in table : external_variables= "" 
    wr(out,'external_variables',external_variables)
    #
    wr(out,'forcing_index',forcing_index,num_type="int") 
    wr(out,'frequency',cmv.frequency)
    #
    wr(out,'further_info_url',further_info_url)
    #
    wr(out,'grid',grid_description) ; wr(out,'grid_label',grid_label) ;
    wr(out,'nominal_resolution',grid_resolution)
    comment=lset.get('comment','')+" "+sset.get('comment','')
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
                raise(dr2xml_error("Fatal: Institution_id for %s not found "+\
                        "in CMIP6_CV at %s"%(institution,cvspath)))
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
    if parent_experiment_id and parent_experiment_id != 'no parent':
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
        if "branch_year_in_parent" in sset :
           date_branch=datetime.datetime(sset["branch_year_in_parent"],1,1)
           date_ref=datetime.datetime(int(parent_time_ref_year),1,1)
           nb_days=(date_branch-date_ref).days
           wr(out,'branch_time_in_parent',"%d.0D"%nb_days) 
        else:
            wr(out,'branch_time_in_parent',sset) 
        # Use branch year in child if available
        if "branch_year_in_parent" in sset :
           date_branch=datetime.datetime(sset["branch_year_in_child"],1,1)
           date_ref=datetime.datetime(sset["child_time_ref_year"],1,1)
           nb_days=(date_branch-date_ref).days
           wr(out,'branch_time_in_child',"%d.0D"%nb_days) 
        else:
            wr(out,'branch_time_in_child',sset)
    #
    wr(out,"physics_index",physics_index,num_type="int") 
    wr(out,'product','model-output')
    wr(out,"realization_index",realization_index,num_type="int") 
    wr(out,'realm',cmv.modeling_realm)
    wr(out,'references',lset,default=False) 
    #
    try:
        with open(cvspath+project+"_source_id.json","r") as json_fp :
            sources=json.loads(json_fp.read())['source_id']
            source=make_source_string(sources,source_id)
    except :
        if "source" in lset : source=lset['source']
        else:
            raise(dr2xml_error("Fatal: source for %s not found in CMIP6_CV at"+\
                               "%s, nor in lset"%(source_id,cvspath)))
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
    wr(out,"title","%s model output prepared for %s / %s %s"%(\
        source_id,project,activity_id,experiment_id))
    #
    wr(out,"variable_id",cmv.label)
    #
    variant_info=sset.get('variant_info',"none")
    if variant_info!="none": variant_info+=variant_info_warning
    wr(out,"variant_info",variant_info)
    wr(out,"variant_label",variant_label)
    for name,value in attributes : wr(out,name,value)
    #
    #--------------------------------------------------------------------
    # Build all XIOS auxilliary elements (end_file_defs, field_defs, domain_defs, grid_defs, axis_defs)
    #---
    # Write XIOS field_group node (containing field elements, stored in end_field_defs)
    # including CF field attributes 
    #--------------------------------------------------------------------
    end_field_defs=dict()
    create_xios_aux_elmts_defs(cmv,alias,table,lset,sset,end_field_defs,
                                field_defs,axis_defs,grid_defs,domain_defs,dummies,context,target_hgrid_id,pingvars)
    if len(end_field_defs.keys())==0 :
        raise dr2xml_error("No end_field_def for %s in %s"%(cmv.label,table))
        return
    #if table == "6hrLev" and alias != lset["ping_variables_prefix"]+"ps" :
    if cmv.spatial_shp[0:4]=='XY-A':
        # create a field_def entry for surface pressure 
        sv_psol=get_simplevar(dq,"ps",table)
        if sv_psol :
            create_xios_aux_elmts_defs(sv_psol,lset["ping_variables_prefix"]+"ps",table,lset,sset,end_field_defs,
                          field_defs,axis_defs,grid_defs,domain_defs,dummies,context,target_hgrid_id,pingvars)
    #
    for shape in end_field_defs :
        if shape :
            # Create a field group for each non-trivial shape, for performance issues
            # (remapping must be done after time average !)
            out.write('<field_group grid_ref="%s">\n'%shape)
        for entry in end_field_defs[shape] : out.write(entry)
        if shape : out.write('</field_group >\n')
    #if table == "6hrLev" :
    if cmv.spatial_shp[0:4]=='XY-A':
        # add entries for auxilliary variables : ap, ap_bnds, b, b_bnds
        names={"ap": "vertical coordinate formula term: ap(k)",
               "ap_bnds": "vertical coordinate formula term: ap(k+1/2)",
               "b": "vertical coordinate formula term: b(k)",
               "b_bnds" : "vertical coordinate formula term: b(k+1/2)"  }
        for tab in names :
            out.write('\t<field field_ref="%s%s" name="%s" long_name="%s" operation="once" prec="8" />\n'%\
                      (lset["ping_variables_prefix"],tab,tab,names[tab]))
    out.write('</file>\n\n')

def wrv(name, value, num_type="string"):
    global print_wrv
    if not print_wrv : return ""
    # Format a 'variable' entry
    return '     <variable name="%s" type="%s" > %s '%(name,num_type,value)+\
        '</variable>\n'

def create_xios_aux_elmts_defs(sv,alias,table,lset,sset,end_field_defs,
    field_defs,axis_defs,grid_defs,domain_defs,dummies,context,target_hgrid_id,pingvars) :
    """
    Create a field_ref for a simplified variable object sv (with
    lab prefix for the variable name) and store it in end_field_defs
    under a key=grid
    
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
    has_vertical_interpolation=False
    ssh=sv.spatial_shp
    prefix=lset["ping_variables_prefix"]
    lwps=sv.label_without_psuffix
    # TBD Should ensure that various additionnal dims are duly documented by model or pingfile (e.g. tau)
    if ssh[0:4] in ['XY-H','XY-P'] or ssh[0:3] == 'Y-P' or \
       (ssh[0:5]=='XY-na' and prefix+sv.label not in pingvars ):
        for sd in sv.sdims.values(): # Expect that only one can be a vertical dim
            if isVertDim(sd):
                vert_freq=lset["vertical_interpolation_sample_freq"]
                has_vertical_interpolation=True
                #  passage par 2 niveaux de field id auxiliaires rebond (alias et alias2)
                alias1=alias+"_"+sd.label   # e.g. 'CMIP6_hus7h_plev7h'
                alias_ping=prefix+lwps      # e.g. 'CMIP6_hus' and not 'CMIP6_hus7h'; 'CMIP6_co2' and not 'CMIP6_co2Clim'

                if sd.is_zoom_of: 
                    # mpmoine_note: cas d'une variable definie grace a 2 axis (zoom+union)
                    alias2=prefix+lwps+"_union" # e.g. 'CMIP6_hus_union'
                    axis_key=sd.zoom_label      # e.g. 'zoom_plev7h_hus'
                else: 
                    # mpmoine_note: cas d'une variable definie grace a seul axis (non zoom)
                    alias2=False 
                    axis_key=sd.label           # e.g. 'plev7h'
                    
                if not alias_ping in pingvars:       # e.g. alias_ping='CMIP6_hus'
                    print "Error: field id ",alias_ping," expected in pingfile but not found."

                if not alias1 in pingvars:
                    # mpmoine_note: maintenant on est toujours dans ce cas (e.g. 'CMPI6_hus7h_plev7h' plus jamais ecrit dans le ping)
                    # Construct an axis for interpolating to this dimension
                    # Here, only zoom or normal axis attached to svar, axis for unions of plevs are managed elsewhere
                    # SS e.g. <axis id="zoom_plev7h_hus" axis_ref="union_plevs_hus"> <zoom_axis index="(0,6)[  3 6 11 13 15 20 28 ]"/>
                    create_axis_def(sd,prefix,vert_freq,axis_defs,field_defs)
                    #
                    # Construct a grid using variable's grid and new axis
                    # <grid id="FULL_klev_zoom_plev7h_hus"> <domain domain_ref="FULL" /> <axis axis_ref="zoom_plev7h_hus" />
                    grid_id=create_grid_def(grid_defs,axis_key,alias_ping,context_index,table)
		    #
                    # alias_instant for a field which has 'instant' operation before time sampling
                    alias_instant=alias_ping+"_instant" # e.g.  CMIP6_zg_instant
	            # <field id="CMIP6_hus_instant" field_ref="CMIP6_hus" operation="instant" />
                    field_defs[alias_instant]=\
                        '<field id="%-25s field_ref="%-25s operation="instant" />'\
                        %(alias_instant+'"',alias_ping+'"')

                    # alias_sample for a field which is time-samples the insant field before vertical interpolation
                    alias_sample=alias_ping+"_sampled_"+vert_freq # e.g.  CMIP6_zg_sampled_3h
	            # <field id="CMIP6_hus_sampled_3h" field_ref="CMIP6_hus_instant" freq_op="3h" expr="@CMIP6_hus_instant"/>
                    field_defs[alias_sample]=\
                        '<field id="%-25s field_ref="%-25s freq_op="%-10s > @%s </field>'\
                        %(alias_sample+'"',alias_instant+'"',vert_freq+'"',alias_instant)

                    # Construct a field def for the re-mapped variable
                    if sd.is_zoom_of: # cas d'une variable definie grace a 2 axis_def (union+zoom)
                        
                        # SS : Must first create grid for levels union, e.g.:
                        # <grid id="FULL_klev_union_plevs_hus"> <domain domain_ref="FULL" /> <axis axis_ref="union_plevs_hus" />
                        grid_id=create_grid_def(grid_defs,sd.is_zoom_of,alias_ping,context_index)
	                # Ss e.g.: <field id="CMIP6_hus_union" field_ref="CMIP6_hus_sampled_3h" grid_ref="FULL_klev_union_plevs_hus"/>
                        field_defs[alias2]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
                        %(alias2+'"',alias_sample+'"',grid_id+'"')

                        # SS : Must first create grid for levels subset zoom, e.g.:
    	                # <grid id="FULL_klev_zoom_plev7h_hus"> <domain domain_ref="FULL" /> <axis axis_ref="zoom_plev7h_hus" /
                        grid_id=create_grid_def(grid_defs,sd.zoom_label,alias_ping,context_index)
	                # SS: e.g.: <field id="CMIP6_hus7h_plev7h" field_ref="CMIP6_hus_union" grid_ref="FULL_klev_zoom_plev7h_hus"
                        field_defs[alias1]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
                        %(alias1+'"',alias2+'"',grid_id+'"')

                    else: # cas d'une variable definie grace a seul axis_def (non union+zoom)
                        field_defs[alias1]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
                            %(alias1+'"',alias_sample+'"',grid_id+'"')
                        #
                #TBD what to do for singleton dimension ? 
    #
    # SS : ecriture plus lisible, et evitant des redondances
    last_alias=alias 
    if has_vertical_interpolation : last_alias=alias1 
    #--------------------------------------------------------------------
    # Retrieve XIOS temporal operation to perform by analyzing the time part of cell_methods
    #--------------------------------------------------------------------
     # Analyze 'outermost' time cell_methods and translate to 'operation'
    operation,detect_missing = analyze_cell_time_method(sv.cell_methods,sv.label,table, printout=False)
    if not operation: 
        #raise dr2xml_error("Fatal: bad xios 'operation' for %s in table %s: %s (%s)"%(sv.label,table,operation,sv.cell_methods))
        print("Fatal: bad xios 'operation' for %s in table %s: %s (%s)"%(sv.label,table,operation,sv.cell_methods))
        operation="once"
    if not type(detect_missing)==type(bool()): 
        #raise dr2xml_error("Fatal: bad xios 'detect_missing_value' for %s in table %s: %s (%s)"%(sv.label,table,detect_missing,sv.cell_methods))
        print("Fatal: bad xios 'detect_missing_value' for %s in table %s: %s (%s)"%(sv.label,table,detect_missing,sv.cell_methods))
    #
    #--------------------------------------------------------------------
    # Build XIOS grid elements (stored in grid_defs)
    # by analyzing the spatial shape
    # Including horizontal operations. Can include horiz re-gridding specification
    #--------------------------------------------------------------------
    # Compute domain name, define it if needed
    grid_ref=None
    if ssh[0:2] == 'Y-' : #zonal mean and atm zonal mean on pressure levels
        # TBD should remap before zonal mean # STOPICI_REVUE_TBD_09-05-2017
        grid_ref="zonal_mean"
        grid_defs[grid_ref]='<grid id="%s"/>'%grid_ref
    elif (ssh == 'S-na' and 'rsucs' not in alias)  : # COSP sites
        grid_ref=cfsites_grid_id
        grid_defs[grid_ref]='<grid id="%s" > <domain id="%s" /> </grid>\n'%(cfsites_grid_id,cfsites_domain_id)
        domain_defs[cfsites_radix]=' <domain id="%s" type="unstructured" prec="8"> '%(cfsites_domain_id)+\
            '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true" mode="read_or_compute" write_weight="true" /> </domain>'
        # 
    elif ssh == 'TR-na' or ssh == 'TRS-na' : #transects,   oce or SI
        pass
    elif ssh[0:3] == 'XY-' or ssh[0:3] == 'S-A'  or (ssh== "S-na" and 'rsucs' in alias) : 
        # this includes 'XY-AH' and 'S-AH' : model half-levels
        if (ssh[0:3] == 'S-A' or (ssh== "S-na" and 'rsucs' in alias )) :
            target_hgrid_id="cfsites_domain"
        if target_hgrid_id :
            # Must create and a use a grid similar to the last one defined 
            # for that variable, except for a change in the hgrid/domain
            if has_vertical_interpolation and not last_alias in pingvars:
                margs={"src_grid_string":grid_defs[grid_id]}
            else:
                margs={"alias":last_alias}
            grid_def=change_domain_in_grid(domain=target_hgrid_id, index=context_index,**margs)
            if grid_def is False or grid_def is None : 
                raise dr2xml_error("Fatal: cannot create grid_def for %s with hgrid=%s"%(alias,target_hgrid_id))
            grid_ref=grid_def[0] ;
            grid_defs[grid_ref]=grid_def[1]
            
    elif ssh[0:3] == 'YB-'  : #basin zonal mean or section
        pass
    elif ssh      == 'na-na'  : # global means or constants
        pass 
    elif ssh      == 'na-A'  : # only used for rlu, rsd, rsu ... in Efx ????
        pass 
    else :
        raise(dr2xml_error("Fatal: Issue with un-managed spatial shape %s for variable %s in table %s"%(ssh,sv.label,table)))
    #
    #--------------------------------------------------------------------
    # Build XIOS field elements (stored in end_field_defs)
    # including their CMOR attributes
    #--------------------------------------------------------------------
    #TBS# if any (sd.is_zoom_of for sd in sv.sdims.values()):
    alias_with_operation=last_alias+"_"+operation
    rep='  <field field_ref="%s" name="%s" '% (alias_with_operation,sv.label)
    if operation != 'once' :
        rep+=' freq_op="%s"'% cmipFreq2xiosFreq[sv.frequency]
    # No more need for specifying an operation at this level, because there is only 
    # one field out of the explicit time operation below
    #rep+=' operation="%s" detect_missing_value="%s" default_value="1.e+20" prec="4"'% \
    #    ( operation,detect_missing)
    detect_missing="True"
    rep+=' detect_missing_value="%s" \n\tdefault_value="1.e+20" prec="4"'%detect_missing
    # TBD: idealement if faudrait recuperer le type attendu de la DR ou des tables CMOR
    # TBD : implement DR recommendation for cell_method : The syntax is to append, in brackets, 'interval: *amount* *units*', for example 'area: time: mean (interval: 1 hr)'. The units must be valid UDUNITS, e.g. day or hr.
    rep+=' cell_methods="%s" cell_methods_mode="overwrite"'% sv.cell_methods
    rep+='>\n'
    if operation != 'once' : rep+='\t\t@%s\n'%alias_with_operation
    # Create field_def for alias_with_operation
    field_defs[alias_with_operation]='<field id="%-25s field_ref="%-25s operation="%-10s/>'\
                            %(alias_with_operation+'"',last_alias+'"',operation+'"')
    #
    comment=None
    # Process experiment-specific comment for the variable
    if sv.label in sset['comments'].keys() :
        comment=sset['comments'][sv.label] 
    else: # Process lab-specific comment for the variable
        if sv.label in lset['comments'].keys() : 
            comment=sset['comments'][sv.label] 
    if comment : rep+=wrv('comment',comment) #TBI 
    #
    rep+=wrv("standard_name",sv.stdname)
    #
    desc=sv.description
    if desc : desc=desc.replace(">","&gt;").replace("<","&lt;").replace("&","&amp;").replace("'","&apos;").replace('"',"&quot;")
    rep+=wrv("description",desc)
    #
    rep+=wrv("long_name",sv.long_name)
    if sv.positive != "None" and sv.positive != "" :
        rep+=wrv("positive",sv.positive) 
    rep+=wrv('history','none')
    rep+=wrv('units',sv.stdunits)
    rep+=wrv('cell_methods',sv.cell_methods)
    rep+=wrv('cell_measures',sv.cell_measures)
    if sv.label == "basin" :
        rep+=wrv('flag_meanings','global_land southern_ocean atlantic_ocean '+\
            'pacific_ocean arctic_ocean indian_ocean mediterranean_sea '+\
            'black_sea hudson_bay baltic_sea red_sea')
    # We override the Xios value for interval_operation because it sets it to
    # the freq_output value with our settings (for complicated reasons)
    if not has_vertical_interpolation :
        source,source_type=get_source_id_and_type(sset,lset)
        grid_choice=lset["grid_choice"][source]
        interval_op=`int(lset['sampling_timestep'][grid_choice][context])`+" s"
    else:
        interval_op=vert_freq
    rep+=wrv('interval_operation',interval_op)
    # mpmoine_note: 'missing_value(s)' normalement plus necessaire, a verifier
    #TBS# rep+=wrv('missing_values',sv.missing,num_type="double")
    rep+='     </field>\n'
    #
    if grid_ref not in end_field_defs : end_field_defs[grid_ref]=[]
    end_field_defs[grid_ref].append(rep)
    #print "Appending for %s : %s"%(grid_ref,rep)

def gather_AllSimpleVars(lset,sset,year=False,printout=False):
    mip_vars_list=select_CMORvars_for_lab(lset,sset,year,printout=printout)
    if sset.get('listof_home_vars',lset.get('listof_home_vars',None)):
        process_homeVars(lset,mip_vars_list,lset["mips"][grid_choice],dq,expid=sset['experiment_id'],printout=printout)

    else: print "Info: No HOMEvars list provided."
    return mip_vars_list

def generate_file_defs(lset,sset,year,enddate,context,cvs_path,pingfile=None,
                       dummies='include',printout=False,dirname="./",prefix="",attributes=[]) :
    # A wrapper for profiling top-level function : generate_file_defs_inner
    import cProfile, pstats, StringIO
    pr = cProfile.Profile()
    pr.enable()
    generate_file_defs_inner(lset,sset,year,enddate,context,cvs_path,pingfile=pingfile,
                             dummies=dummies,printout=printout,dirname=dirname,prefix=prefix,attributes=attributes) 
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    # Just un-comment next line to get the profile on stdout
    #print s.getvalue()

    
def generate_file_defs_inner(lset,sset,year,enddate,context,cvs_path,pingfile=None,
                       dummies='include',printout=False,dirname="./",prefix="",attributes=[]) :
    """
    Using global DR object dq, a dict of lab settings LSET, and a dict 
    of simulation settings SSET, generate an XIOS file_defs 'file' for a 
    given XIOS 'context', which content matches 
    the DR for the experiment quoted in simu setting dict and a YEAR.
    Makes use of CMIP6 controlled vocabulary files found in CVS_PATH
    Reads PINGFILE for analyzing dummy field_refs, 
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
    additional file-level attributes
    """
    #
    global print_wrv
    print_wrv=lset.get("print_variables",True)
    #--------------------------------------------------------------------
    # Parse XIOS settings file for the context
    #--------------------------------------------------------------------
    global context_index
    context_index=init_context(context,lset.get("path_to_parse","./"),printout=False)
    if context_index is None : sys.exit(1)
    #
    #--------------------------------------------------------------------
    # Extract CMOR variables for the experiment and year and lab settings
    #--------------------------------------------------------------------
    skipped_vars_per_table={}
    mip_vars_list=gather_AllSimpleVars(lset,sset,year,printout)
    # Group CMOR vars per realm
    svars_per_realm=dict()
    for svar in mip_vars_list :
        if svar.modeling_realm not in svars_per_realm.keys() :
            svars_per_realm[svar.modeling_realm]=[]
        if svar not in svars_per_realm[svar.modeling_realm]:
            svars_per_realm[svar.modeling_realm].append(svar)
        else:
            old=svars_per_realm[svar.modeling_realm][0]
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
    for realm in context_realms :
        excludedv=dict()
        print "Processing realm '%s' of context '%s'"%(realm,context)
        #print 50*"_"
        excludedv=dict()
        if realm in svars_per_realm.keys():
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
    # Read ping_file defined variables
    #--------------------------------------------------------------------
    pingvars=[] 
    if pingfile :
        ping_refs=read_xml_elmt_or_attrib(pingfile, tag='field', attrib='field_ref')
        if ping_refs is None :
            print "Error: issue accessing pingfile "+pingfile
            return
        if dummies=="include" :
            pingvars=ping_refs.keys()
        else :
            pingvars=[ v for v in ping_refs if 'dummy' not in ping_refs[v] ]
            if dummies=="forbid" :
                if len(pingvars) != len(ping_refs) :
                    print "They are still dummies in %s , while option is 'forbid' :"%pingfile,
                    for v in ping_refs :
                        if v not in pingvars : print v,
                    print
                    sys.exit(1)
                else :
                    pingvars=ping_refs
            elif dummies=="skip" : pass
            else:
                print "Forbidden option for dummies : "+dummies
                sys.exit(1)
    #
    #--------------------------------------------------------------------
    # Build all plev union axis and grids
    #--------------------------------------------------------------------
    field_defs=dict()
    axis_defs=dict()
    grid_defs=dict()
    if lset['use_union_zoom']:
        svars_full_list=[]
        for svl in svars_per_table.values(): svars_full_list.extend(svl)
        create_xios_axis_and_grids_for_plevs_unions(svars_full_list,
                                        multi_plev_suffixes.union(single_plev_suffixes),
                                        lset["ping_variables_prefix"],
                                        lset["vertical_interpolation_sample_freq"],
                                        axis_defs,grid_defs,field_defs, ping_refs, printout=True )
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
        for s in lset : out.write(' %s : %s\n'%(s,lset[s]))
        out.write('-->\n')
        out.write('<!-- Simulation settings : \n')        
        for s in sset : out.write(' %s : %s\n'%(s,sset[s]))
        out.write('-->\n')
        domain_defs=dict()
        #for table in ['day'] :    
        out.write('\n<file_definition type="one_file" enabled="true" > \n')
        foo,sourcetype=get_source_id_and_type(sset,lset)
        for table in svars_per_table :
            count=dict()
            for svar in svars_per_table[table] :
                if True : #realm_is_processed(svar.modeling_realm,sourcetype) : <- realms are note reliable enough in DR
                    if svar.label not in count :
                        count[svar.label]=svar
                        for grid in svar.grids :
                            write_xios_file_def(svar,year,table, lset,sset,out,cvs_path,
                                            field_defs,axis_defs,grid_defs,domain_defs,dummies,
                                            skipped_vars_per_table,prefix,context,grid,pingvars,
                                            enddate,attributes)
                    else :
                        pass
                        #print "Duplicate var in %s : %s %s %s"%(
                        #    table, svar.label, `svar.temporal_shp`, \
                        #    `count[svar.label].temporal_shp`)
                else:
                    print "Var %s of realm %s is not processed by source-type %s"%\
                        (svar.label,svar.modeling_realm,sourcetype)
        if cfsites_grid_id in grid_defs : out.write(cfsites_input_filedef())
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
            out.write('<field_group freq_op="_reset_" >\n')
        for obj in field_defs: out.write("\t"+field_defs[obj]+"\n")
        if lset.get("nemo_sources_management_policy_master_of_the_world",False) and context=='nemo':
            out.write('</field_group>\n')
        out.write('\n</field_definition> \n')
        #
        out.write('\n<axis_definition> \n')
        out.write('<axis_group prec="8">\n')
        for obj in axis_defs.keys(): out.write("\t"+axis_defs[obj]+"\n")
        if False and lset['use_union_zoom']:
            for obj in union_axis_defs.keys(): out.write("\t"+union_axis_defs[obj]+"\n")
        out.write('</axis_group>\n')
        out.write('</axis_definition> \n')
        #
        out.write('\n<domain_definition> \n')
        out.write('<domain_group prec="8">\n')
        if lset['grid_policy'] != "native" : create_standard_domains(domain_defs)
        for obj in domain_defs.keys(): out.write("\t"+domain_defs[obj]+"\n")
        out.write('</domain_group>\n')
        out.write('</domain_definition> \n')
        #
        out.write('\n<grid_definition> \n')
        for obj in grid_defs.keys(): out.write("\t"+grid_defs[obj])
        if False and lset['use_union_zoom']:
            for obj in union_grid_defs.keys(): out.write("\t"+union_grid_defs[obj]+"\n")
        out.write('</grid_definition> \n')
        out.write('</context> \n')
    if printout :
        print "\nfile_def written as %s"%filename
    
    # mpmoine_petitplus:generate_file_defs: pour sortir des stats sur ce que l'on sort reelement
    # SS - non : gros plus
    if printout: print_SomeStats(context,svars_per_table,skipped_vars_per_table)

    warn=dict()
    for warning,label,table in cell_method_warnings:
        if warning not in warn : warn[warning]=set()
        warn[warning].add(label)
    print "\nWarnings about cell methods (with var list)"
    for w in warn  : print "\t",w," for vars : ",warn[w]
        

# mpmoine_petitplus: nouvelle fonction print_SomeStats (plus d'info sur les skipped_vars, nbre de vars / (shape,freq) )
# SS - non : gros plus
def print_SomeStats(context,svars_per_table,skipped_vars_per_table):

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
    for table in svars_per_table.keys():
    	for sv in svars_per_table[table]:
    		dic_freq={}
    		dic_shp={}
    		if table not in skipped_vars_per_table.keys()  or \
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

    print "\n\nSome Statistics on variables per frequency+shape..."
    for k1,v1 in stats_out.items():
    	for k2,v2 in v1.items():
    		nb=len(v2.values())
    		print "\n\t* %d variables output at %s frequency with shape %s ---> "%(nb,k1,k2),
    		for k3,v3 in v2.items(): print k3,"(",v3,"),",
    print
    return True


def create_axis_def(sdim,prefix,vert_frequency,axis_defs,field_defs):
    """

    From a simplified Dim object SDIM representing a vertical dimension,
    creates and stores an Xios axis definition in AXIS_DEFS

    If the dimension implies vertical interpolation (on air_pressure
    or altitude levels), creates and stores (in FIELD_DEFS) an
    intermediate field for the sampling of that coordinate field at
    VERT_FREQUENCY

    If the dimension is a zoom of another one, analyzes its 'requested'
    field against the list of values declared for the other one, for
    defining the zoom in XIOS syntax

    """

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
        if n_glo>1 :
            # Case of a non-degenerated vertical dimension (not a singleton)
            rep+='n_glo="%g" '%n_glo
            rep+='value="(0,%g)[ %s ]"'%(n_glo-1,sdim.requested)
        else:
            if n_glo!=1: 
                print "Warning: axis is singleton but has",n_glo,"values"
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
        coordname_sampled=coordname+"_sampled_"+vert_frequency # e.g. CMIP6_pfull_sampled_3h
        rep+='\n\t<interpolate_axis type="polynomial" order="1"'
        rep+=' coordinate="%s"/>\n\t</axis>'%coordname_sampled
        axis_defs[sdim.label]=rep
        #
        # Create and store a definition for time-sampled field for the vertical coordinate
        coorddef='<field id="%-25s field_ref="%-25s operation="instant" freq_op="%-10s> @%s</field>'\
                        %(coordname_sampled+'"',coordname+'"', vert_frequency+'"',coordname)
        field_defs[coordname_sampled]=coorddef
    else: # zoom case
        # Axis is subset of another, write it as a zoom_axis
        rep='<axis id="%s"'%sdim.zoom_label
        rep+=' axis_ref="%s">'%sdim.is_zoom_of
        rep+='\t<zoom_axis index="(0,%g)[ '%(n_glo-1)
        values=re.sub(r'.*\[ *(.*) *\].*',r'\1',axis_defs[sdim.is_zoom_of])
        values=values.split("\n")[0]
        union_vals=values.strip(" ").split()
        union_vals_num=[float(v) for v in union_vals]
        for val in glo_list_num : rep+=' %g'%union_vals_num.index(val)
        rep+=' ]"/>'
        rep+='</axis>'
        axis_defs[sdim.zoom_label]=rep
    # Store definition for the new axis
    return rep 

def change_domain_in_grid(domain,alias=None,src_grid_string=None,index=None,printout=False):
    """ 
    Provided with either a variable name (ALIAS) or the string for a grid definition,
    (SRC_GRID_STRING) returns a grid_definition where the domain has been changed to DOMAIN
    """
    if src_grid_string is None:
        if alias is None :
            raise dr2xml_error("change_domain_in_grid: must provide alias or grid_string ")
        src_grid=id2grid(alias,index,printout=printout)
        if src_grid is not None : 
            src_grid_id=src_grid.attrib['id']
            src_grid_string=ET.tostring(src_grid)
        else:
            raise dr2xml_error("Fatal: ask for creating a grid_def for var %s which has no grid "%(alias))
    else :
        src_grid_id=re.sub(r'.*grid id= *.([\w_]*).*\n.*',r'\g<1>',src_grid_string,1)
        if src_grid_id == src_grid_string : 
            raise dr2xml_error("Issue extracting grid id for %s from %s "%(alias,src_grid_string))
        #print "src_grid_id=%s"%src_grid_id
    target_grid_id=src_grid_id+"_"+domain
    # Change domain
    (target_grid_string,count)=re.subn('domain *id= *.([\w_])*.','domain id="%s"'%domain,src_grid_string,1) 
    if count != 1 :
        (target_grid_string,count)=re.subn('domain *domain_ref= *.([\w_])*.','domain domain_ref="%s"'%domain,src_grid_string,1) 
        if count != 1 :
            raise dr2xml_error("Fatal: cannot find a domain to change in src_grid_string %s for %s"%(src_grid_string,alias))
    target_grid_string=re.sub('grid id= *.([\w_])*.','grid id="%s"'%target_grid_id,target_grid_string)
    return (target_grid_id,target_grid_string)

def create_grid_def(grid_defs,axis_key,alias=None,context_index=None,table=None):
    # mpmoine_correction:create_grid_def:  si, il faut generer une grille autour des axes de zoom aussi
    #if not sd.is_zoom_of and not sd.is_union_for: # a grid_def to build in classical case (a vertical axis without using union)
    if alias and context_index:
        src_grid=id2grid(alias,context_index)
        if src_grid is not None : 
            src_grid_id=src_grid.attrib['id']
            src_grid_string=ET.tostring(src_grid)
            target_grid_id=src_grid_id+"_"+axis_key
            # Change only first instance of axis_ref, which is assumed to match the vertical dimension
            #(target_grid_string,count)=re.subn('axis *id= *.([\w_])*.','axis id="%s"'%axis_key,src_grid_string,1)
            (target_grid_string,count)=re.subn('<axis[^\>]*>','<axis axis_ref="%s"/>'%axis_key,src_grid_string,1)
            if count != 1 :
                axis_name="axis_for_"+target_grid_id
                (target_grid_string,count)=re.subn('axis *axis_ref= *.([\w_])*.',\
                                                   'axis id="%s" axis_ref="%s"'% (axis_name,axis_key),\
                                                   src_grid_string,1)
                if count != 1 : 
                    raise dr2xml_error("Fatal: cannot find an axis_ref to change in src_grid_string %s for %s in %s"%\
                                       (src_grid_string,alias,table))
            target_grid_string=re.sub('grid id= *.([\w_])*.','grid id="%s"'%target_grid_id,target_grid_string)
            grid_defs[target_grid_id]=target_grid_string
            return target_grid_id
        else:
            raise dr2xml_error("Fatal: ask for creating a grid_def for var %s which has no grid "%(alias))
        #return False
    else:
        raise dr2xml_error("Fatal: ask for creating a grid_def from a native grid "+\
                           "but variable alias and/or context_index not provided (alias:%s, context_index:%s)"%(alias,context_index))


def create_xios_axis_and_grids_for_plevs_unions(svars,plev_sfxs,prefix,vert_freq,axis_defs,grid_defs,field_defs, ping_refs, printout=False): 
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

                    if  present_in_ping and not dummy_in_ping: 
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
                            print "Info: ", lwps, "not taken into account for building plevs union axis because one of these 2 reasons:" 
                            print "      a)", prefix+lwps,"is not an entry in the pingfile: Entry?",present_in_ping  
                            print "      b)", prefix+lwps,"has au dummy reference in the pingfile. Dummy?",dummy_in_ping 

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
        axis_def=create_axis_def(sdim_union,prefix,vert_freq,union_axis_defs,field_defs)
        create_grid_def(union_grid_defs,sdim_union.label,prefix+lwps,context_index)
    #
    #return (union_axis_defs,union_grid_defs)

def isVertDim(sdim):
    """
    Returns True if dim represents a dimension for which we want 
    an Xios interpolation. 
    For now, a very simple logics for interpolated vertical 
    dimension identification:
    """
    # SS : p840, p220 sont des couches de pression , pour lesquelles COSP forunit directement
    # les valeurs moyennes de parametres (e.g. cllcalipso). On les detecte par l'attribut bounds 
    test=(sdim.stdname=='air_pressure' or sdim.stdname=='altitude') and (sdim.bounds != "yes")
    return test

def analyze_cell_time_method(cm,label,table,printout=False):
    """
    Depending on cell method string CM, tells which time operation
    should be done, and if missing value detection should be set
    We rely on the missing value detection to match the requirements like
    "where sea-ice", "where cloud" since we suppose fields required in this way
    are physically undefined oustide of "where something".
    """
    operation=None
    detect_missing=False
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
            print "TBD: Cannot yet handle time: mean (with samples weighted by snow mass) for "+\
                "%15s in table %s -> averaging"%(label,table)
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where cloud"  in cm : 
        #[amncl-twm]: Weighted Time Mean on Cloud (2 variables ISSCP 
        # albisccp et pctisccp, en emDay et emMon)
        cell_method_warnings.append(('time: mean where cloud',label,table))
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
    elif "time: minimum" in cm :    
        #[tmin]: Temporal Minimum : utilisee seulement dans table daily
        operation="minimum"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: maximum" in cm :   
        #[tmax]: Time Maximum  : utilisee seulement dans table daily
        operation="maximum"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: maximum within days time: mean over days" in cm :
        #[dmax]: Daily Maximum : tasmax Amon seulement
        if label != 'tasmax' : 
            print "Error: issue with variable %s in table %s "%(label,table)+\
                "and cell method time: maximum within days time: mean over days"
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: minimum within days time: mean over days" in cm :
        #[dmin]: Daily Minimum : tasmin Amon seulement
        if label != 'tasmin' : 
            print "Error: issue with variable %s in table %s  "%(label,table)+\
                "and cell method time: minimum within days time: mean over days"
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean within years time: mean over years" in cm: 
        #[aclim]: Annual Climatology
        cell_method_warnings.append(('Cannot yet compute annual climatology',label,table))
        if printout: 
            print "TBD: Cannot yet compute annual climatology for "+\
                "%15s in table %s -> averaging"%(label,table)
        # Could transform in monthly fields to be post-processed
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean within days time: mean over days"  in cm: 
        #[amn-tdnl]: Mean Diurnal Cycle
        cell_method_warnings.append(('Cannot yet compute diurnam cycle',label,table))
        if printout: 
            print "TBD: Cannot yet compute diurnal cycle for "+\
                " %15s in table %s -> averaging"%(label,table)
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas 'Maximum Hourly Rate'
    elif "time: mean within hours time: maximum over hours"  in cm: 
        #[amn-tdnl]: Mean Diurnal Cycle
        cell_method_warnings.append(('Cannot yet compute maximum hourly rate',label,table))
        if printout: 
            print "TBD: Cannot yet compute maximum hourly rate for "+\
                " %15s in table %s -> averaging"%(label,table)
            # Could output a time average of 24 hourly fields at 01 UTC, 2UTC ...
        operation="average"
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
        #print "Warning: assuming operation is 'once' for cell_method "+\
        #    "%s for %15s in table %s" %(cm,label,table)
        operation="once"
    #----------------------------------------------------------------------------------------------------------------
    else :
        print "Warning: issue when analyzing cell_time_method "+\
            "%s for %15s in table %s, assuming it is once" %(cm,label,table)
        operation="once"
    return (operation, detect_missing)

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
    # (Merci Marie-Pierre pour la régression....)
    uniques=[] ; labels=[]
    for v in lvars : 
        if not v.label_non_ambiguous in labels :
            uniques.append(v); labels.append(v.label_non_ambiguous)
        elif not v.label_without_psuffix in labels :
            uniques.append(v); labels.append(v.label_without_psuffix)
            
    lvars=uniques
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
            out.write('<field_group freq_op="_reset_" >\n')
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
                         %(v.Priority,v.stdunits, v.stdname, v.description)) 
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
    - values are corresponding ET elements if 
      attrib is None, otherwise elt attribute ATTRIB
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
                if attrib is None: 
                    rep[field.attrib['id']]=field
                else :
                    rep[field.attrib['id']]=field.attrib[attrib]
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
    domain_defs['25km']='<domain id="CMIP6_25km" ni_glo="1440" nj_glo="720" type="rectilinear"  prec="8"> '+\
      '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute" write_weight="true" /> '+\
    '</domain>  '
    domain_defs['50km']='<domain id="CMIP6_50km" ni_glo="720" nj_glo="360" type="rectilinear"  prec="8"> '+\
      '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute" write_weight="true" /> '+\
    '</domain>  '
    domain_defs['100km']='<domain id="CMIP6_100km" ni_glo="360" nj_glo="180" type="rectilinear"  prec="8"> '+\
      '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute" write_weight="true"  /> '+\
    '</domain>  '
    domain_defs['1deg']='<domain id="CMIP6_1deg" ni_glo="360" nj_glo="180" type="rectilinear"  prec="8"> '+\
      '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute" write_weight="true"  /> '+\
    '</domain>  '
    domain_defs['2deg']='<domain id="CMIP6_2deg" ni_glo="180" nj_glo="90" type="rectilinear"  prec="8"> '+\
      '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute" write_weight="true"  /> '+\
    '</domain>  '

# def create_cfsites_grids(grid_defs):
#     """
#     Add to dictionnary grid_defs the Xios string representation for COSP standard grids
#     """
#     grid_defs['cfsites']='<grid id="cfsites_grid" > <domain id="cfsites_domain" /> </grid>'
#     grid_defs['cfsites_3D']='<grid id="cfsites_grid_3D" > <domain id="cfsites_domain" /> <axis id="axis_atm"/> </grid>'

def cfsites_input_filedef() :
    """
    Returns a file definition for defining a COSP site grid by reading a field named 
    'cfsites_grid_field' in a file named 'cfsites_grid.nc'
    """
    #rep='<file id="%s" name="%s" mode="read" >\n'%\
    rep='<file id="%s" name="%s" mode="read" output_freq="1y" >\n'%\
        (cfsites_grid_file_id,cfsites_grid_file_name)+\
      '\t<field id="%s" operation="instant" grid_ref="%s" />\n'%(cfsites_grid_field_id,cfsites_grid_id)+\
      ' </file>'
    return rep
    


def build_axis_definitions():
    """ 
    Build a dict of axis definitions 
    """
    for g in dq.coll['grids'].items :
        pass


def ping_alias(svar,lset,pingvars):
    # dans le pingfile, grace a la gestion des interpolations
    # verticales, on n'attend pas forcement les alias complets des
    # variables (CMIP6_<label>), on peut se contenter des alias
    # reduits (CMIP6_<lwps>)

    # par ailleurs, si on a defini un label non ambigu alors on l'utilise
    # comme ping_alias (i.e. le field_ref)
    
    pref=lset["ping_variables_prefix"]
    if svar.label_non_ambiguous:
        alias_ping=pref+svar.label_non_ambiguous # e.g. 'CMIP6_tsn_land' and not 'CMIP6_tsn'
    else:
        # Ping file may provide the variable on the relevant pressure level - e.g. CMIP6_rv850
        alias_ping=pref+svar.label 
        if alias_ping not in pingvars :
            # if not, ping_alias is supposed to be without a pressure level suffix
            alias_ping=pref+svar.label_without_psuffix # e.g. 'CMIP6_hus' and not 'CMIP6_hus7h'
    return alias_ping

    
        
def RequestItemInclude(ri,var_label,freq) :
    """ 
    test if a variable is requested by a requestItem at a given freq
    """
    varGroup=dq.inx.uid[dq.inx.uid[ri.rlid].refid]
    reqVars=dq.inx.iref_by_sect[varGroup.uid].a['requestVar']
    cmVars=[ dq.inx.uid[dq.inx.uid[reqvar].vid] for reqvar in reqVars ]
    return any( [ cmv.label==var_label and cmv.frequency==freq for cmv in cmVars ])

def endyear_for_CMORvar(dq,cv,expt,year,lset): 
    """ 
    For a CMORvar, returns the larger year in the time slice(s)  
    of those requestItems which apply for experiment EXPT and which 
    include YEAR. If no time slice applies, returns None 
    """ 
    # 1- Get the RequestItems which apply to CmorVar 
    # 2- Select those requestItems which include expt,
    #    and retain their endyear if larger than former one
 
    global global_rls

    # Some debug material
    if False and (cv.label=="tsl" and cv.frequency=="mon") : printout=True
    else : printout=False

    # 1- Get the RequestItems which apply to CmorVar
    rVarsUid=dq.inx.iref_by_sect[cv.uid].a['requestVar']
    rVars=[ dq.inx.uid[uid] for uid in rVarsUid ]
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
        applies,endyear=RequestItem_applies_for_exp_and_year(ri,expt,lset,year)
        if printout :
            print "For var and freq selected for debug, for ri %s, applies=%s, endyear=%s"%(ri.title, `applies`,`endyear`)
        if applies :
            if endyear is None:  return None # One of the timeslices cover the whole expt
            else :
                if larger is None : larger=endyear
                else : larger=max(larger,endyear)
    return larger


def get_source_id_and_type(sset,lset):
    if "configuration" in sset and "configurations" in lset :
        if sset["configuration"] in lset["configurations"]: 
            source_id,source_type,unused=lset["configurations"][sset["configuration"]]
        else:
            dr2xml_error("configuration %s is not known (allowed values are :)"%\
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


class dr2xml_error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
    def __str__(self):
        return `self.valeur`
    #""" just for test"""
