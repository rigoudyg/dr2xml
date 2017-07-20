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
  june 2017 - SS               introduce horizontal remapping

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

# 3- XIOS release must be 1047 or above (to be fed with the outputs)
#  see https://forge.ipsl.jussieu.fr/ioserver/wiki

####################################
# End of pre-requisites
####################################

version="0.14"
print "* dr2xml version:", version

from datetime import datetime
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
                multi_plev_suffixes, single_plev_suffixes
from grids import decide_for_grids, DRgrid2gridatts,\
    split_frequency_for_variable, timesteps_per_freq_and_duration
from Xparse import init_context, id2grid

# A auxilliary tables
from table2freq import table2freq, table2splitfreq, cmipFreq2xiosFreq

from dr2cmip6_expname import dr2cmip6_expname

print_DR_errors=True

dq = dreq.loadDreq()
print "* CMIP6 Data Request version: ", dq.version

context_index=None

# Names for COSP-CFsites related elements.
# A file named cfsites_grid_file_id must be provided at runtime, which
# includes a field named cfsites_grid_field_id, defined on a unstructured 
# grid which is composed of CF sites
cfsites_radix        ="cfsites"
cfsites_domain_id    =cfsites_radix+"_domain"
cfsites_grid_id      =cfsites_radix+"_grid"
cfsites_grid_file_id =cfsites_grid_id
cfsites_grid_field_id=cfsites_radix+"_field"

""" An example/template  of settings for a lab and a model"""
example_lab_and_model_settings={
    'institution_id': "CNRM-CERFACS", # institution should be read in CMIP6_CV, if up-to-date
    'source_id'      : "CNRM-CM6-1", 
    # The description of lab models, in CMIP6 CV wording
    'source_types' : { "CNRM-CM6-1" : "AOGCM", "CNRM-CM6-1-HR" : "AOGCM", 
                       "CNRM-ESM2-1": "ESM"  , "CNRM-ESM2-1-HR": "ESM" },
    'source'         : "CNRM-CM6-1", # Useful only if CMIP6_CV is not up to date
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
    'mips' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
                      'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
    # Max variable priority level to be output
    'max_priority' : 1,
    'tierMax'      : 1,

    # The ping file defines variable names, which are constructed using CMIP6 "MIPvarnames" 
    # and a prefix which must be set here, and can be the empty string :
    "ping_variables_prefix" : "CMIP6_",

    # We account for a list of variables which the lab does not want to produce , 
    # Names must match DR MIPvarnames (and **NOT** CF standard_names)
    # excluded_vars_file="../../cnrm/non_published_variables"
    "excluded_vars":[],

    # We account for a list of variables which the lab wants to produce in some cases
    "listof_home_vars":"../../cnrm/listof_home_vars.txt",
    
    # Each XIOS  context does adress a number of realms
    'realms_per_context' : { 
        'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'] ,
        'arpsfx' : ['atmos', 'atmos atmosChem', 'aerosol', 'atmos land', 'land',
                    'landIce land',  'aerosol land','land landIce',  'landIce', ],
        'trip'   : [],
                          }, 
    # Some variables, while belonging to a realm, may fall in another XIOS context than the 
    # context which hanldes that realm
    'orphan_variables' : { 'nemo'    : [''],
                           ' arpsfx' : [],
                           'trip'    : ['dgw', 'drivw', 'cfCLandToOcean', 'qgwr', 'rivi', 'rivo', 'waterDpth', 'wtd'],
                           },
    'vars_OK' : dict(),
    # A per-variable dict of comments valid for all simulations
    'comments'     : {
        'tas' : 'nothing special about tas'
        },
    # Sizes for atm and oce grids (cf DR doc)
    # actual_sizes=[292*362,75,128*256,91,30,14,128]
    # actual_sizes=[1442*1021,75,720*360,91,30,14,128]
    #"sizes"  : [259200,60,64800,40,20,5,100],
    "sizes"  : [292*362,75,128*256,91,30,14,128],
    #
    # What is the maximum size of generated files, in number of float values
    "max_file_size_in_floats" : 500.*1.e+6 ,
    # grid_policy among None, DR, native, native+DR, adhoc- see docin grids.py 
    "grid_policy" : "adhoc",
    # Grids : per model resolution and per context :
    #              CMIP6 name, name_of_target_domain (if remapping is needed), CMIP6-std resolution, and description
    "grids" : { 
      "LR"    : {
        "surfex" : [ "gr","complete" , "250 km", "data regridded to a T127 gaussian grid (128x256 latlon) from a native atmosphere T127l reduced gaussian grid"] ,
          "trip" : [ "gn", "" ,  "50 km" , "regular 1/2 deg lat-lon grid" ],
          "nemo" : [ "gn", ""        , "100 km" , "native ocean tri-polar grid with 105 k ocean cells" ],},
      "HR"    : {
        "surfex" : [ "gr","complete" , "50 km", "data regridded to a 359 gaussian grid (180x360 latlon) from a native atmosphere T359l reduced gaussian grid"] ,
          "trip" : [ "gn", "" ,  "50 km" , "regular 1/2 deg lat-lon grid" ],
          "nemo" : [ "gn", ""         , "25 km" , "native ocean tri-polar grid with 1.47 M ocean cells" ],},
    },
    'grid_choice' : { "CNRM-CM6-1" : "LR", "CNRM-CM6-1-HR" : "HR",
                      "CNRM-ESM2-1": "LR"  , "CNRM-ESM2-1-HR": "HR" },
    #        
    # Component Models Time steps (s)
    "model_timestep" : { "surfex":900., "nemo":900., "trip": 1800. },
    #--- Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR
    "use_union_zoom" : False,
    "vertical_interpolation_sample_freq" : "3h"
}


""" An example/template of settings for a simulation """

example_simulation_settings={    
    # Dictionnary describing the necessary attributes for a given simulation

    # Warning : some lines are commented out in this example but should be 
    # un-commented in some cases. See comments

    "experiment_id"  : "historical",
    #"contact"        : "", set it only if it is specific to the simualtion
    #"project"        : "CMIP6",  #CMIP6 is the default

    #'source_type'    : "ESM" # If source_type deduced from model name is not relevant for this 
                   #experiment (e.g. : AMIP), you may tell that here

    # MIPs specifying the experiment. For historical, it is CMIP
    # itself In a few cases it may be appropriate to include multiple
    # activities in the activity_id (separated by single spaces).  
    # An example of this is 'LUMIP AerChemMIP' for one of the land-use change experiments.
    "activity_id"      : "CMIP", # examples : "PMIP", 'LS3MIP LUMIP'; defaults to "CMIP"
    
    # It is recommended that some description be included to help
    # identify major differences among variants, but care should be
    # taken to record correct information.  Prudence dictates that
    # this attribute includes a warning along the following lines:
    # 'Information provided by this attribute may in some cases be
    # flawed.# Users can find more comprehensive and up-to-date
    # documentation via the further_info_url global attribute.'
    "variant_info"      : "Start date chosen so that variant r1i1p1f1 has "+\
                          "the better fit with Krakatoa impact on tos",
    #
    "realization_index"    : 1, # Value may be omitted if = 1
    "initialization_index" : 1, # Value may be omitted if = 1
    "physics_index"        : 1, # Value may be omitted if = 1
    "forcing_index"        : 1, # Value may be omitted if = 1
    #
    # All about the parent experiment and branching scheme
    "parent_experiment_id" : "piControl", # omit or set to 'no parent' if not applicable
                                          # (remaining parent attributes will be disregarded)
    "branch_method"        : "standard", # default value='standard' meaning ~ "select a start date" 
    "branch_time_in_child" : "0.0D0",   # a double precision value in child time units (days), used if applicable
    "branch_time_in_parent": "365.0D0", # a double precision value, in days, used if applicable 
    'parent_time_ref_year' : 1850, # default=1850. 
    #'parent_variant_label' :""  #Default to 'same as child'. Other cases should be exceptional
    #"parent_mip_era"       : 'CMIP5'   # only in special cases (as e.g. PMIP warm 
                                        #start from CMIP5/PMIP3 experiment)
    #'parent_activity_id'   : 'CMIP'    # only in special cases, defaults to CMIP
    #'parent_source_id'     : 'CNRM-CM5.1' # only in special cases, where parent model 
                                           # is not the same model
    #
    "sub_experiment_id"    : "None", # Optional, default is 'none'; example : s1960. 
    "sub_experiment"       : "None", # Optional, default in 'none'
    "history"              : "None", #Used when a simulation is re-run, an output file is modified ...
    # A per-variable dict of comments which are specific to this simulation. It will replace  
    # the all-simulation comment
    'comments'     : {
        'tas' : 'tas diagnostic uses a special scheme in this simulation : .....',
        }
    }

#def hasCMORVarName(hmvar):
#    for cmvar in dq.coll['CMORvar'].items:
#        if (cmvar.label==hmvar.label): return True

def RequestItem_applies_for_exp_and_year(ri,experiment,year,debug=False):
    """ 
    Returns True if requestItem 'ri' in data request 'dq' (global) is relevant 
    for a given 'experiment' and 'year'. Toggle 'debug' allow some printouts 
    """
    # Acces experiment or experiment group for the RequestItem
    if (debug) : print "Checking ","% 15s"%ri.label,
    item_exp=dq.inx.uid[ri.esid]
    relevant=False
    exps=dq.coll['experiment'].items
    # esid can link to an experiment or an experiment group
    if item_exp._h.label== 'experiment' :
        if (debug) : print "%20s"%"Simple Expt case", item_exp.label,
        if item_exp.label==experiment : 
            if (debug) : print " OK",
            relevant=True
    elif item_exp._h.label== 'exptgroup' :
        if (debug)  : print "%20s"%"Expt Group case ",item_exp.label,
        group_id=ri.esid
        for e in exps :
            if 'egid' in dir(e) and e.egid == group_id and \
               e.label==experiment : 
                if (debug) :  print " OK for experiment based on group"+\
                   group_id.label,
                relevant=True
    elif item_exp._h.label== 'mip' :
        mip_id=ri.esid
        if (debug)  : print "%20s"%"Mip case ",dq.inx.uid[mip_id].label,
        for e in exps :
            if 'mip' in dir(e) and e.mip == mip_id :
                if (debug) :  print e.label,",",
                if e.label==experiment : 
                    if (debug) :  print " OK for experiment based on mip"+\
                       mip_id.label,
                    relevant=True
    else :
        if (debug)  :
            print "%20s"%'Error %s for %s'%(item_exp._h.label,`ri`)
        #raise(dr2xml_error("%20s"%'Other case , label=%s|'%item_exp._h.label))
    if relevant :
        if 'tslice' in ri.__dict__ :
            if ri.tslice == '__unset__' :
                print "tslice is unset for reqlink %s "%ri.title
                relevant=True
            else:
                timeslice=dq.inx.uid[ri.tslice]
                if (debug) : print "OK for the year"
                try :
                    relevant=year >= timeslice.start and year<=timeslice.end
                except :
                    relevant=True
                    print "tslice not well set for "+timeslice.label+" "+\
                        timeslice.uid+\
                        ". Assuming it applies for RequestItem "+ri.title
        else :
            if (debug)  : print "tslice not set -> OK for the year"
            #print "No tslice for %s"%ri.title
            relevant=True
    return relevant

def select_CMORvars_for_lab(lset, experiment_id=None, year=None,printout=False):
    """
    A function to list CMOR variables relevant for a lab (and also, 
    optionnally for an experiment and a year)
    
    Args:
      lset (dict): laboratory settings; used to provide the list of MIPS,  
                   the max Tier, and a list of excluded variable names
      experiment_id (string,optional): if willing to filter on a given 
                   experiment - not used if year is None
      year (int,optional) : simulation year - used to filter the request 
                   for an experiment and a year

    Returns:
      A list of 'simplified CMOR variables'
    
    """
    #
    # From MIPS set to Request links
    global sc
    sc = dreqQuery(dq=dq, tierMax=lset['tierMax'])

    # Set sizes for lab settings, if available (or use CNRM-CM6-1 defaults)
    mcfg = collections.namedtuple( 'mcfg', \
                ['nho','nlo','nha','nla','nlas','nls','nh1'] )
    sizes=lset.get("sizes",[259200,60,64800,40,20,5,100])
    sc.mcfg = mcfg._make( sizes )._asdict()
    #
    rls_for_mips=sc.getRequestLinkByMip(lset['mips'])
    if printout :
        print "Number of Request Links which apply to MIPS",
        print lset['mips']," is: ", len(rls_for_mips)
    #
    for rl in rls_for_mips :
        if rl.label=="CFsubhr":
            rlCFsubhr=rl
            #print "One reqlink : "+`rl.label`+" grid="+rl.grid+" uid="+rl.uid
    # TBD : verifier si ce requestlink CFsubhr, qui indique grille native en subhr (!), a ete rectifie
    rls_for_mips.remove(rlCFsubhr)
    #
    if (year) :
        filtered_rls=[]
        for rl in rls_for_mips :
            # Access all requesItems ids which refer to this RequestLink
            ri_ids=dq.inx.iref_by_sect[rl.uid].a['requestItem']
            for ri_id in ri_ids :
                ri=dq.inx.uid[ri_id]
                #print "Checking requestItem ",ri.label
                if RequestItem_applies_for_exp_and_year(ri,
                                    experiment_id, year,False) :
                    #print "% 25s"%ri.label," applies "
                    filtered_rls.append(rl)
        rls=filtered_rls
        if printout :
            print "Number of Request Links which apply to experiment ", \
                experiment_id,"and MIPs", lset['mips'] ," is: ",len(rls)
    else :
        rls=rls_for_mips
       
    # From Request links to CMOR vars + grid
    #miprl_ids=[ rl.uid for rl in rls ]
    #miprl_vars=sc.varsByRql(miprl_ids, pmax=lset['max_priority'])
    miprl_vars_grids=[]
    for rl in rls :
        rl_vars=sc.varsByRql([rl.uid], pmax=lset['max_priority'])
        for v in rl_vars :
            if (v,rl.grid) not in miprl_vars_grids :
                miprl_vars_grids.append((v,rl.grid))
    if printout :
        print 'Number of (CMOR variable, grid) pairs for these requestLinks is :%s'%len(miprl_vars_grids)
    # 
    filtered_vars=[]
    for (v,g) in miprl_vars_grids : 
        cmvar=dq.inx.uid[v]
        mipvar=dq.inx.uid[cmvar.vid]
        if mipvar.label not in lset['excluded_vars'] : 
            filtered_vars.append((v,g))
    if printout :
        print 'Number once filtered by excluded vars is : %s'%len(filtered_vars)

    # Filter the list of grids requested for each variable based on lab policy
    d=dict()
    for (v,g) in filtered_vars :
        if v not in d : d[v]=set()
        d[v].add(g)
    if printout :
        print 'Number of distinct CMOR variables (whatever the grid) : %d'%len(d)
    for v in d:
        d[v]=decide_for_grids(v,d[v],lset,dq)
        if printout and len(d[v]) > 1 :
            print "\tVariable %s will be processed with multiple grids : %s"%(dq.inx.uid[v].label,`d[v]`)
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
        complement_svar_using_cmorvar(svar,cmvar,dq)
        svar.Priority=analyze_priority(cmvar,lset['mips'])
        svar.grids=d[v]
        simplified_vars.append(svar)
    print '\nNumber of simplified vars is :',len(simplified_vars)
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
        out.write('  <variable name="%s"  type="%s" > %s '%(key,num_type,val))
        out.write('  </variable>\n')


def freq2datefmt(freq,operation):
    # WIP doc v6.2.3 - Apr. 2017: <time_range> format is frequency-dependant 
    datefmt=False
    offset=None
    if freq == "dec":
        datefmt="%y"
        if operation in ["average","minimum","maximum"] : offset=False
        else : offset="10y"
    if freq == "yr":
        datefmt="%y"
        if operation in ["average","minimum","maximum"] : offset=False
        else : offset="1y"
    elif freq in ["mon","monClim"]:
        datefmt="%y%mo"
        if operation in ["average","minimum","maximum"] : offset=False
        else : offset="1mo"
    elif freq=="day":
        datefmt="%y%mo%d"
        if operation in ["average","minimum","maximum"] : offset="12h"
        else : offset="1d"
    elif freq in ["6hr","3hr","3hrClim","1hr","hr","1hrClimMon"]: 
        datefmt="%y%mo%d%h%mi"
        if freq=="6hr":
            if operation in ["average","minimum","maximum"] : offset="3h"
            else : offset="6h"
        elif freq in [ "3hr", "3hrClim"] :
            if operation in ["average","minimum","maximum"] : offset="90mi"
            else : offset="3h"
        #mpmoine_TBD: supprimer "hr" selon reponse de D. Nadeau a l'issue https://github.com/PCMDI/cmip6-cmor-tables/issues/59
        elif freq in ["1hr", "hr",  "1hrClimMon"]: 
            if operation in ["average","minimum","maximum"] : offset="30mi"
            else : offset="1h"
        # TBD : remove this use of 'table', which is here only for compensating a bug in PrePARE.py checks (3.2.5)
        if table=="6hrPlevPt" : datefmt="%y%mo%d%h%mi%s"

    elif freq=="subhr":
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

def write_xios_file_def(cmv,table,lset,sset,out,cvspath,
                        field_defs,axis_defs,grid_defs,domain_defs,
                        dummies,skipped_vars_per_table,
                        prefix,context,grid,pingvars=None,enddate=None,
                        attributes=[]) :
    """ 
    Generate an XIOS file_def entry in out for :
      - a dict for laboratory settings 
      - a dict of simulation settings 
      - a 'simplifed CMORvar' cmv
      - which all belong to given table
      - a path 'cvs' for Controlled Vocabulary
      
    Lenghty code, but not longer than the corresponding specification document
    
    After a prologue, attributes valid for all variables are 
    written as file-level metadata, in the same order than in 
    WIP document; last, field-level metadate are written
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
        else:                       alias=lset["ping_variables_prefix"]+cmv.label
        # TBD mpmoine_correction: suppression des terminaisons en "Clim" pour l'alias 
        split_alias=alias.split("Clim")
        alias=split_alias[0]
        if pingvars is not None :
            # mpmoine_zoom_modif:write_xios_file_def: dans le pingfile, on attend plus les alias complets  des variables (CMIP6_<label>) mais les alias reduits (CMIP6_<lwps>)
            # mpmoine  si on a defini un label non ambigu alors on l'untilise comme ping_alias (i.e. le field_ref) 
            if cmv.label_non_ambiguous:
                alias_ping=lset["ping_variables_prefix"]+cmv.label_non_ambiguous # e.g. 'CMIP6_tsn_land' and not 'CMIP6_tsn'
            else:
                alias_ping=lset["ping_variables_prefix"]+cmv.label_without_psuffix # e.g. 'CMIP6_hus' and not 'CMIP6_hus7h'
            if not alias_ping in pingvars:
                #print "Must skip alias_ping=%s"%alias_ping
                # mpmoine: on classe les skipped_vars par table (pour avoir plus d'info au print) 
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
    source_id=lset['source_id']
    experiment_id=sset['experiment_id']
    institution_id=lset['institution_id']
    #
    contact=sset.get('contact',lset.get('contact',None))
    conventions="CF-1.7 CMIP-6.0"
    #
    # Variant matters
    realization_index=sset.get('realization_index',1) 
    initialization_index=sset.get('initialization_index',1)
    physics_index=sset.get('physics_index',1)
    forcing_index=sset.get('forcing_index',1)
    variant_label="r%di%dp%df%d"%(realization_index,initialization_index,\
                                  physics_index,forcing_index)
    # mpmoine_WIP_update:write_xios_file_def: WIP doc v6.2.3 - Apr. 2017: cf recommendation in note 16 for 'variant_info'
    variant_info_warning=". Information provided by this attribute may in some cases be flawed. "+\
                         "Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute."
    #
    # WIP Draft 14 july 2016
    activity_id=sset.get('activity_id','CMIP')
    # mpmoine_last_modif:write_xios_file_def: mip_era n'est plus toujours 'CMIP6' (par ex. 'PRIMAVERA')
    mip_era=cmv.mip_era
    #
    # WIP doc v 6.2.0 - dec 2016 
    # <variable_id>_<table_id>_<source_id>_<experiment_id >_<member_id>_<grid_label>[_<time_range>].nc
    member_id=variant_label
    # mpmoine_cmor_update:write_xios_file_def: CMOR3.2.2 impose 'None' (et non 'none') comme default value de sub_experiment_id
    # mpmoine_cmor_update:write_xios_file_def: CMOR3.2.3 impose 'none'(et non 'None' !) comme default value de sub_experiment_id
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
        # DR requested type of grid. Assume that the ping_file includes an Xios definition for it <- TBD
        if grid == 'cfsites' :
            target_hgrid_id=cfsites_domain_id
        else:
            target_hgrid_id=lset["ping_variables_prefix"]+grid
        grid_label,grid_resolution,grid_description=DRgrid2gridatts(grid)
        # grid_label=grid2label(grid)
        # grid_description=grid2desc(grid)
        # grid_resolution=grid2resol(grid)
    if table in [ 'AERMonZ',' EmonZ', 'EdayZ' ] : grid_label+="z"
    if "Ant" in table : grid_label+="a"
    if "Gre" in table : grid_label+="g"
    # mpmoine_TBD : change grid_label depending on shape (sites, transects)
    #
    #--------------------------------------------------------------------
    # Set NetCDF output file name according to the DRS
    #--------------------------------------------------------------------
    #
    # mpmoine : les noms d'expe dans la DR ne sont pas les meme que dans le CV CMIP6
    with open(cvspath+project+"_experiment_id.json","r") as json_fp :
        CMIP6_experiments=json.loads(json_fp.read())['experiment_id']
        if CMIP6_experiments.has_key(sset['experiment_id']):
            expname=sset['experiment_id']
        else:
            # mpmoine_last_modif:write_xios_file_def: provisoire, laisser passer cette erreur tant que le
            # mpmoine_last_modif:write_xios_file_def: CV_CMIP6 et celui de la DR ne sont pas concordants
            dr2xml_error("Issue getting experiment description in CMIP6 CV for %20s"+\
                         " => Search for experiment name correspondance from DR to CMIP6 CV."\
                               %sset['experiment_id'])
            expname=dr2cmip6_expname[sset['experiment_id']]
        exp_entry=CMIP6_experiments[expname]
        experiment=exp_entry['experiment']
        description=exp_entry['description']
    # 
    date_range="%start_date%-%end_date%" # XIOS syntax
    operation,detect_missing = analyze_cell_time_method(cmv.cell_methods,cmv.label,table)
    date_format,offset_begin,offset_end=freq2datefmt(cmv.frequency,operation,table)
    #
    # mpmoine: WIP doc v6.2.3 : [_<time_range>] omitted if frequency is "fx"
    if "fx" in cmv.frequency:
        filename="%s%s_%s_%s_%s_%s_%s"%\
                   (prefix,cmv.label,table,source_id,expname,
                    member_id,grid_label)
    else:
        # mpmoine: WIP doc v6.2.3 : a suffix "-clim" should be added if climatology
        # TBD : for the time being, we should also have attribute 'climatology' for dimension 'time',
        # TBD : but we cannot -> forget temporarily about this extension
        if False and "Clim" in cmv.frequency: suffix="-clim"
        else: suffix=""
        filename="%s%s_%s_%s_%s_%s_%s_%s%s"%\
            (prefix,cmv.label,table,source_id,expname,
             member_id,grid_label,date_range,suffix)
    #
    further_info_url="http://furtherinfo.es-doc.org/%s.%s.%s.%s.%s.%s"%(
        mip_era,institution_id,source_id,expname,
        sub_experiment_id,variant_label)
    #
    #--------------------------------------------------------------------
    # Compute XIOS split frequency
    #--------------------------------------------------------------------
    # mpmoine_last_modif:write_xios_file_def: Maintenant, dans le cas type='perso', table='NONE'. On ne doit donc pas compter sur le table2freq pour recuperer la frequence en convention xios => fonction cmipFreq2xiosFreq
    split_freq=split_frequency_for_variable(cmv, lset, sc.mcfg, context)
    #
    #--------------------------------------------------------------------
    # Write XIOS file node:
    # including global CMOR file attributes
    #--------------------------------------------------------------------
    out.write(' <file name="%s" '%filename)
    out.write(' output_freq="%s" '%cmipFreq2xiosFreq[cmv.frequency])
    out.write(' append="true" ')
    if not "fx" in cmv.frequency :
        out.write(' split_freq="%s" '%split_freq)
        # mpmoine_cmor_update:write_xios_file_def: ajout de 'split_freq_format' pour se conformer a CMOR3.0.3 
        out.write(' split_freq_format="%s" '%date_format)
        #
        # Modifiers for date parts of the filename, due to silly KT conventions. 
        if offset_begin is not False :
            out.write(' split_start_offset="%s" ' %offset_begin)
        if offset_end is not False  :
            out.write(' split_end_offset="%s" '%offset_end)
        # Using Eclis convention : endday looks like 20131231, rather than 20140101
        endyear=enddate[0:4]
        endmonth=enddate[4:6]
        endday=enddate[6:8]
        out.write(' split_last_date="%s-%s-%s 00:00:00 +1d" '%(endyear,endmonth,endday))
    #
    #out.write('timeseries="exclusive" >\n')
    out.write(' time_units="days" time_counter_name="time"')
    # mpmoine_cmor_update:write_xios_file_def: ajout de time_counter="exclusive"
    out.write(' time_counter="exclusive"')
    out.write(' time_stamp_name="creation_date" ')
    out.write(' time_stamp_format="%Y-%m-%dT%H:%M:%SZ"')
    out.write(' uuid_name="tracking_id" uuid_format="hdl:21.14100/%uuid%"')
    out.write(' >\n')
    #
    wr(out,'activity_id',activity_id)
    #
    if contact and contact is not "" : wr(out,'contact',contact) 
    wr(out,'Conventions',conventions) 
    wr(out,'data_specs_version',dq.version) 
    wr(out,'dr2xml_version',version) 
    #
    wr(out,'description',description)
    wr(out,'experiment',experiment)
    wr(out,'experiment_id',expname)
    # 
    # TBD: check external_variables
    # Let us yet hope that all tables but those with an 'O'
    # as first letter require areacella, and the others require areacello
    external_variables= "areacella" 
    if table[0]=='O' or table[0:1]=='SI' : external_variables= "areacello" 
    if 'fx' in table : external_variables= "" 
    wr(out,'external_variables',external_variables)
    #
    # mpmoine_cmor_update:write_xios_file_def: ecriture de forcing_index en integer requis par la version CMOR3.2.3
    wr(out,'forcing_index',forcing_index,num_type="int") 
    # mpmoine_last_modif: Maintenant, dans le cas type='perso', table='NONE'. On ne doit donc pas compter sur table2freq pour recuperer la frequence
    wr(out,'frequency',cmv.frequency)
    #
    # URL
    wr(out,'further_info_url',further_info_url)
    #
    wr(out,'grid',grid_description) ; wr(out,'grid_label',grid_label) ;
    wr(out,'nominal_resolution',grid_resolution)    
    wr(out,'history',sset,default='none') 
    # mpmoine_cmor_update:write_xios_file_def: ecriture de  initialization_index en integer requis par la version CMOR3.2.3 
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
    # mpmoine_cmor_update:write_xios_file_def: changement des defaults values pour les parent_<XXX>: default en dur remplace par la valeur pour <XXX> 
    # mpmoine_cmor_update:write_xios_file_def: et utilisation de l'attribut optionnel 'default' de la fonction 'wr' plutot que sset.get avec une default
    parent_experiment_id=sset.get('parent_experiment_id',False)
    if parent_experiment_id and parent_experiment_id != 'no parent':
        wr(out,'parent_experiment_id',parent_experiment_id)
        wr(out,'parent_mip_era',sset,default=mip_era)
        wr(out,'parent_activity_id',sset,default=activity_id)
        wr(out,'parent_source_id',sset,default=source_id)
        # TBX : syntaxe XIOS pour designer le time units de la simu courante
        parent_time_ref_year=sset.get('parent_time_ref_year',"1850")
        parent_time_units="days since %s-01-01 00:00:00"%parent_time_ref_year
        wr(out,'parent_time_units',sset,default=parent_time_units)
        wr(out,'parent_variant_label',sset,default=variant_label)
        wr(out,'branch_method',sset,default='standard') 
        wr(out,'branch_time_in_child',sset)
        wr(out,'branch_time_in_parent',sset) 
    #
    # mpmoine_cmor_update:write_xios_file_def: ecriture de physics_index en integer requis par la version CMOR3.2.3 
    wr(out,"physics_index",physics_index,num_type="int") 
    # mpmoine_cmor_update:write_xios_file_def: changement des valeurs de 'product' requis par la version CMOR3.2.3
    wr(out,'product','model-output')
    # mpmoine_cmor_update:write_xios_file_def: ecriture de realization_index en integer requis par la version CMOR3.2.3
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
    if 'source_type' in sset :
        source_type=sset['source_type']
    else:
        if 'source_type' in lset :
            source_type=lset['source_type']
        else:
            if 'source_types' in lset :
                source_type=lset['source_types'][source_id] 
            else:
                raise dr2xml_error("Fatal: No source-type found - Check inputs")
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
    #
    for shape in end_field_defs :
        if shape :
            # Create a field group for each non-trivial shape, for performance issues
            # (remapping must follow time average !)
            out.write('<field_group expr="@this" grid_ref="%s">\n'%shape)
        for entry in end_field_defs[shape] : out.write(entry)
        if shape : out.write('</field_group >\n')
    out.write('</file>\n\n')

 # mpmoine_last_modif:wrv: ajout de l'argument num_type

def wrv(name, value, num_type="string"):
    # Format a 'variable' entry
    return '     <variable name="%s" type="%s" > %s '%(name,num_type,value)+\
        '</variable>\n'

def create_xios_aux_elmts_defs(sv,alias,table,lset,sset,end_field_defs,
    field_defs,axis_defs,grid_defs,domain_defs,dummies,context,target_hgrid_id,pingvars) :
    """
    Create a field_ref for a simplified variable object sv (with
    lab prefix for the variable name) and store it in end_field_defs
    under a key=grid
    
    Add field definitions for intermediate variables in dic field_defs
    Add axis  definitions for interpolations in dic axis_defs
    Use pingvars as the list of variables actually defined in ping file

    """
    # By convention, field references are built as prefix_<MIP_variable_name>
    # Such references must be fulfilled using a dedicated filed_def
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
    # mpmoine_zoom_modif:create_xios_aux_elmts_defs: recup de lwps
    lwps=sv.label_without_psuffix
    # TBD Should ensure that various additionnal dims are duly documented by model or pingfile (e.g. tau)
    # TBD : cas 'XY-na' pour capturer les dimensions singleton : il faut etre plus selectif : existence d'un cids (grid de lg 1)
    if ssh[0:4] in ['XY-H','XY-P'] or ssh[0:3] == 'Y-P' or ssh[0:5]=='XY-na':
        # mpmoine_last_modif:create_xios_aux_elmts_defs: on recupere maintenant 'dimids' depuis svar
        # mpmoine_future_modif:create_xios_aux_elmts_defs: on utilise maintenant sv.sdims pour analyser les dimension
        # mpmoine_question: je ne comprend pas l'usage de nextvar... A priori on ne peut pas avoir plus d'une dimension verticale ?
        for sd in sv.sdims.values(): # Expect that only one can be a vertical dim
            if isVertDim(sd):
                vert_freq=lset["vertical_interpolation_sample_freq"]
                has_vertical_interpolation=True
                # mpmoine_zoom_modif:create_xios_aux_elmts_defs: on supprime l'usage de netxvar
                # mpmoine_zoom_modif:create_xios_aux_elmts_defs: passage par 2 niveaux de field id auxiliaires rebond (alias et alias2)
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
                    # SS : peut-etre a revoir, ca.. (COSP)
                    #
                    # Construct an axis for interpolating to this dimension
                    # Here, only zoom or normal axis attached to svar, axis for unions of plevs are managed elsewhere
                    axisdef,coordname,coorddef=create_axis_def(sd,prefix,vert_freq)
                    axis_defs[axis_key]=axisdef
                    field_defs[coordname]=coorddef
                    #
                    # Construct a grid using variable's grid and new axis
                    #TBS# if not sd.is_zoom_of: # create a (target) grid for re-mapping only if vert axis is not a zoom (i.e. if normal or union)
                    #TBS# grid_def=create_grid_def(sd,alias,context_index)
                    grid_def=create_grid_def(sd,axis_key,alias_ping,context_index)
                    if grid_def is False : 
                        raise dr2xml_error("Fatal: cannot create grid_def for %s and %s"%(alias,sd))
                    grid_id=grid_def[0]
                    grid_defs[grid_id]=grid_def[1]
		            #
                    # Construct a field def for the re-mapped variable
                    # mpmoine_correction:create_xios_aux_elmts_defs: passage par grid_ref aussi pour les varaibles definies sur des zoom
                    if sd.is_zoom_of: # cas d'une variable definie grace a 2 axis_def (union+zoom)
                        field_defs[alias1]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
                        %(alias1+'"',alias2+'"',"grid_"+sd.zoom_label+'"')
                        # mpmoine_merge_dev2_v0.12:create_xios_aux_elmts_defs: remplacement axis_ref=sd.is_zoom_of -> grid_ref="grid_"+sd.is_zoom_of
                        field_defs[alias2]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
                        %(alias2+'"',alias_ping+'"',"grid_"+sd.is_zoom_of+'"') 
                    else: # cas d'une variable definie grace a seul axis_def (non union+zoom)
                        # alias_sample for a field which is time-sampled before vertical interpolation
                        alias_sample=alias_ping+"_sampled_"+vert_freq # e.g.  CMIP6_zg_sampled_3h
                        field_defs[alias1]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
                        %(alias1+'"',alias_sample+'"',grid_id+'"')
                        #
                        field_defs[alias_sample]='<field id="%-25s field_ref="%-25s operation="instant" freq_op="%-10s> @%s</field>'\
                        %(alias_sample+'"',alias_ping+'"',vert_freq+'"',alias_ping) 
                # mpmoine_note: voir en desactivant les zooms si c'est ok                    
                #TBD what to do for singleton dimension ? 
    #
    # SS : ecriture plus lisible, et evitant des redondances
    last_alias=alias 
    if has_vertical_interpolation : last_alias=alias1 
    #--------------------------------------------------------------------
    # Retrieve XIOS temporal operation to perform
    # by analyzing the time part of cell_methods
    #--------------------------------------------------------------------
     # Analyze 'outermost' time cell_methods and translate to 'operation'
    operation,detect_missing = analyze_cell_time_method(sv.cell_methods,sv.label,table)
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
    #elif ssh[0:2] == 'S-' : # COSP sites - neutralise
    #    pass
    elif ssh == 'S-na' : # COSP sites
        grid_ref=cfsites_grid_id
        grid_defs[grid_ref]='<grid id="%s" > <domain id="%s" /> </grid>'%(cfsites_grid_id,cfsites_domain_id)
        domain_defs[cfsites_radix]=' <domain id="%s" type="unstructured" prec="8"> '%cfsites_domain_id+\
            '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true" mode="read_or_compute"/> </domain>'
    elif ssh == 'TR-na' or ssh == 'TRS-na' : #transects,   oce or SI
        pass
    elif ssh[0:3] == 'XY-' or ssh[0:3] == 'S-A'  : # includes 'XY-AH' and 'S-AH' : model half-levels
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
        raise(dr2xml_error("Fatal: Issue with un-managed spatial shape %s for variable %s"%(ssh,sv.label)))
    #
    #--------------------------------------------------------------------
    # Build XIOS field elements (stored in end_field_defs)
    # including their CMOR attributes
    #--------------------------------------------------------------------
    # mpmoine_correction:create_xios_aux_elmts_defs: alias1  au lieu de alias pour l'ecriture de end_field_defs
    #TBS# if any (sd.is_zoom_of for sd in sv.sdims.values()):
    # mpmoine_cmor_update:create_xios_aux_elmts_defs: les tables CMOR demandent les champs en 'float' ou 'real' => ajout de prec="4"
    # TBI: idealement if faudrait recuperer le type attendu de la DR ou des tables CMOR
    rep='  <field field_ref="%s" name="%s" '% (last_alias,sv.label)
    rep+=' operation="%s" detect_missing_value="%s" default_value="1.e+20" prec="4"'% \
        ( operation,detect_missing)
    rep+=' cell_methods="%s" cell_methods_mode="overwrite"'% sv.cell_methods
    rep+='>\n'
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
    if desc : desc=desc.replace(">","").replace("<","")
    rep+=wrv("description",desc)
    #
    rep+=wrv("long_name",sv.long_name)
    if sv.positive != "None" and sv.positive != "" :
        rep+=wrv("positive",sv.positive) 
    rep+=wrv('history','none')
    rep+=wrv('units',sv.stdunits)
    rep+=wrv('cell_methods',sv.cell_methods)
    rep+=wrv('cell_measures',sv.cell_measures)
    # mpmoine_note: 'missing_value(s)' normalement plus necessaire, a verifier
    #TBS# rep+=wrv('missing_values',sv.missing,num_type="double")
    rep+='     </field>\n'
    #
    if grid_ref not in end_field_defs : end_field_defs[grid_ref]=[]
    end_field_defs[grid_ref].append(rep)
    #print "Appending for %s : %s"%(grid_ref,rep)

# mpmoine_last_modif:gather_AllSimpleVars: nouvelle fonction qui rassemble les operations select_CMORvars_for_lab et read_homeVars_list. 
# mpmoine_last_modif:gather_AllSimpleVars: Necessaire pour create_ping_file qui doit tenir compte des extra_Vars
def gather_AllSimpleVars(lset,expid=False,year=False,printout=False):
    mip_vars_list=select_CMORvars_for_lab(lset,expid,year,printout=printout)
    if lset['listof_home_vars']:
        process_homeVars(lset,mip_vars_list,dq,expid,printout)

    else: print "Info: No HOMEvars list provided."
    return mip_vars_list

def generate_file_defs(lset,sset,year,enddate,context,cvs_path,pingfile=None,
                       dummies='include',printout=False,dirname="./",prefix="",attributes=[]) :
    """
    Using global DR object dq, a dict of lab settings LSET, and a dict 
    of simulation settings SSET, generate an XIOS file_defs file for a 
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
    #--------------------------------------------------------------------
    # Parse XIOS settings file for the context
    #--------------------------------------------------------------------
    global context_index
    # mpmoine_amelioration:generate_file_defs: ajout de l'argument 'path_parse' a la fonction init_context
    context_index=init_context(context,lset.get("path_to_parse","./"),printout=False)
    if context_index is None : sys.exit(0)
    #
    #--------------------------------------------------------------------
    # Extract CMOR variables for the experiment and year and lab settings
    #--------------------------------------------------------------------
    # mpmoine_skipped_modif:generate_file_defs: skipped_vars (liste) change en skipped_vars_per_table (dictionnaire)
    skipped_vars_per_table={}
    mip_vars_list=gather_AllSimpleVars(lset,sset['experiment_id'],year,printout)
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
        print "Processing realm '%s' of context '%s'"%(realm,context)
        print 50*"_"
        if realm in svars_per_realm.keys():
            for svar in svars_per_realm[realm] :
                # mpmoine_last_modif:generate_file_defs: patch provisoire pour retirer les  svars qui n'ont pas de spatial_shape 
                # mpmoine_last_modif:generate_file_defs: (cas par exemple de 'hus' dans table '6hrPlev' => spid='__struct_not_found_001__')
                # mpmoine_next_modif: generate_file_defs: exclusion de certaines spatial shapes (ex. Polar Stereograpic Antarctic/Groenland)
                if svar.label not in lset['excluded_vars'] and \
                   svar.spatial_shp and \
                   svar.spatial_shp not in lset["excluded_spshapes"]:  
                    if svar.mipTable not in svars_per_table : 
                        svars_per_table[svar.mipTable]=[]
                    svars_per_table[svar.mipTable].append(svar)
                else:
                    # mpmoine_future_modif:generate_file_defs: juste un peu plus de printout...
                    if printout:
                        print "Warning: %20s in table %s"%(svar.label,svar.mipTable)+\
                            " has been excluded because :",
                        if svar.label in lset['excluded_vars']: print " it is in exclusion list /",
                        if not svar.spatial_shp: print " it has no spatial shape /",
                        if svar.spatial_shp in lset["excluded_spshapes"]:
                            print " it has an excluded spatial shape:", svar.spatial_shp,
                        print
    #      
    #--------------------------------------------------------------------
    # Add svars belonging to the orphan list
    #--------------------------------------------------------------------
    orphans=lset['orphan_variables'][context]
    for svar in mip_vars_list :
        if svar.label in orphans:
            # mpmoine_last_modif:generate_file_defs: patch provisoire pour retirer les  svars qui n'ont pas de spatial_shape 
            # mpmoine_last_modif:generate_file_defs: (cas par exemple de 'hus' dans table '6hrPlev' => spid='__struct_not_found_001__')
            # mpmoine_next_modif: generate_file_defs: exclusion de certaines spatial shapes (ex. Polar Stereograpic Antarctic/Groenland)
            if svar.label not in lset['excluded_vars'] and svar.spatial_shp and \
               svar.spatial_shp not in lset["excluded_spshapes"]:  
                if svar.mipTable not in svars_per_table : svars_per_table[svar.mipTable]=[]
                svars_per_table[svar.mipTable].append(svar)
    #    
    #
    # mpmoine_zoom_modif:generate_file_defs: build axis defs of plevs unions
    #--------------------------------------------------------------------
    # Build all plev union axis and grids
    #--------------------------------------------------------------------
    if lset['use_union_zoom']:
        svars_full_list=[]
        for svl in svars_per_table.values(): svars_full_list.extend(svl)
        # mpmoine_merge_dev2_v0.12:generate_file_defs: on recupere maintenant non seulement les union_axis_defs mais aussi les union_grid_defs
        (union_axis_defs,union_grid_defs)=create_xios_axis_and_grids_for_plevs_unions(svars_full_list,
                                        multi_plev_suffixes.union(single_plev_suffixes),
                                        lset["ping_variables_prefix"])
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
                    print "They are dummies in %s :"%pingfile,
                    for v in ping_refs :
                        if v not in pingvars : print v,
                    print
                    return 
                else :
                    pingvars=ping_ref
            elif dummies=="skip" : pass
            else:
                print "Forbidden option for dummies : "+dummies
                return 

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
        out.write('<!-- dr2xml version %s --> \n'%version)
        field_defs=dict()
        axis_defs=dict()
        grid_defs=dict()
        domain_defs=dict()
        #for table in ['day'] :    
        out.write('\n<file_definition type="one_file" enabled="true" > \n')
        for table in svars_per_table :
            count=dict()
            for svar in svars_per_table[table] :
                if svar.label not in count :
                    count[svar.label]=svar
                    for grid in svar.grids :
                        write_xios_file_def(svar,table, lset,sset,out,cvs_path,
                                            field_defs,axis_defs,grid_defs,domain_defs,dummies,
                                            skipped_vars_per_table,prefix,context,grid,pingvars,
                                            enddate,attributes)
                else :
                    pass
                    print "Duplicate var in %s : %s %s %s"%(
                        table, svar.label, `svar.temporal_shp`, \
                        `count[svar.label].temporal_shp`)
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
        for obj in field_defs: out.write("\t"+field_defs[obj]+"\n")
        out.write('\n</field_definition> \n')
        out.write('\n<axis_definition> \n')
        for obj in axis_defs.keys(): out.write("\t"+axis_defs[obj]+"\n")
        # mpmoine_zoom_modif:generate_file_defs: on ecrit maintenant les axis defs pour les unions
        # mpmoine_zoom_amelioration:generate_file_defs: usage de 'use_union_zoom'
        if lset['use_union_zoom']:
            for obj in union_axis_defs.keys(): out.write("\t"+union_axis_defs[obj]+"\n")
        out.write('</axis_definition> \n')
        #
        out.write('\n<domain_definition> \n')
        create_standard_domains(domain_defs)
        for obj in domain_defs.keys(): out.write("\t"+domain_defs[obj]+"\n")
        out.write('</domain_definition> \n')
        #
        out.write('\n<grid_definition> \n')
        for obj in grid_defs.keys(): out.write("\t"+grid_defs[obj]+"\n")
        # mpmoine_merge_dev2_v0.12:generate_file_defs: on ecrit maintenant les grid defs pour les unions
        # mpmoine_zoom_amelioration:generate_file_defs: usage de 'use_union_zoom'
        if lset['use_union_zoom']:
            for obj in union_grid_defs.keys(): out.write("\t"+union_grid_defs[obj]+"\n")
        out.write('</grid_definition> \n')
        out.write('</context> \n')
    if printout :
        print "\nfile_def written as %s"%filename
    
    # mpmoine_petitplus:generate_file_defs: pour sortir des stats sur ce que l'on sort reelement
    if printout: print_SomeStats(context,svars_per_table,skipped_vars_per_table)

# mpmoine_petitplus: nouvelle fonction print_SomeStats (plus d'info sur les skipped_vars, nbre de vars / (shape,freq) )
def print_SomeStats(context,svars_per_table,skipped_vars_per_table):

    #--------------------------------------------------------------------
    # Print Summary: list of  considered variables per table 
    # (i.e. not excuded_vars and not excluded_shapes)
    #--------------------------------------------------------------------
    print "\nTables concerned by context %s : "%context, svars_per_table.keys()
    print "\nVariables per table :"
    for table in svars_per_table.keys():
    	print "\n>>> DBG >>> TABLE",
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
            print "%15s %02d/%02d ---->"%(table,len(skipvars),len(svars_per_table[table])),
            #TBS# print "\n\t",table ," ",len(skipvars),"--->",
            for skv in skipvars: 
            	print skv #already contains priority info
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
    		if ( table not in skipped_vars_per_table.keys() ) or \
    		   ( table in skipped_vars_per_table.keys() and sv not in skipped_vars_per_table[table] ) :
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

    print "\n\nSome Statistics..."
    for k1,v1 in stats_out.items():
    	for k2,v2 in v1.items():
    		nb=len(v2.values())
    		print "\n\n* %d variables output at %s frequency with shape %s ---> "%(nb,k1,k2)
    		for k3,v3 in v2.items(): print k3,"(",v3,"),",
    return True


# mpmoine_future_modif:create_axis_def: suppression de l'argument 'field_defs' qui n'est pas utilise
# mpmoine_future_modif:create_axis_def: suppression de l'argument 'field_defs' qui n'est pas utilise
def create_axis_def(sdim,prefix,vert_frequency=None):
    """ 
    From a  simplified Dim object, returns an Xios axis definition 
    """
    # mpmoine_future_modif:create_axis_def: plusieurs modifs car on passe maintenant sdim en argument et non dim_name_or_obj
    if sdim is None:
        print "Warning: cannot create an axis_def from "+sdim
        return None

    # mpmoine_zoom_modif:create_axis_def: nbre de valeurs de l'axe determine aussi si on est en dim singleton
    if sdim.requested:
        # mpmoine_future_modif: je vire le separateur " ", pour regler le pb des " " successifs
        glo_list=sdim.requested.strip(" ").split()
    else:
        glo_list=sdim.value.strip(" ").split()
    glo_list_num=[float(v) for v in glo_list]
    n_glo=len(glo_list)

    # mpmoine_zoom_modif:create_axis_def: traitement du cas non zoom (classique, comme avant)
    if not sdim.is_zoom_of:
        # Axis is not a zoom of another, write axis_def normally (with value, interpolate_axis,etc.)
        rep='<axis id="%s" '%sdim.label
        if not sdim.positive in [ None, "" ] :
            rep+='positive="%s" '%sdim.positive
        if n_glo>1 :
            # Case of a non-degenerated vertical dimension (not a singleton)
            rep+='n_glo="%g" '%n_glo
            # mpmoine_future_modif:create_axis_def: je supprime le -1 pour n_glo car regle avec rstrip/split()
            # mpmoine_correction:create_axis_def: n_glo->(n_glo-1)
            rep+='value="(0,%g) [%s]"'%(n_glo-1,sdim.requested)
        else:
            if n_glo!=1: 
                print "Warning: axis is sigleton but has",n_glo,"values"
                return None
            # Singleton case (degenerated vertical dimension)
            rep+='n_glo="%g" '%n_glo
            rep+='value="(0,0)[%s]"'%sdim.value
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
        coorddef='<field id="%-25s field_ref="%-25s operation="instant" freq_op="%-10s> @%s</field>'\
                        %(coordname_sampled+'"',coordname+'"', vert_frequency+'"',coordname) 
        return rep,coordname_sampled,coorddef
    # mpmoine_zoom_modif:create_axis_def: traitement du cas zoom
    else:
        # Axis is subset of another, write it as a zoom_axis
        rep='<axis id="%s"'%sdim.zoom_label
        rep+=' axis_ref="%s">\n'%sdim.is_zoom_of
        # mpmoine_correction:create_axis_def:  correction syntaxe begin du zoom
        rep+='\t<zoom_axis begin="%g" n="%g"/>\n'%(0,n_glo)
        rep+='\t</axis>'
        return rep

def change_domain_in_grid(domain,alias=None,src_grid_string=None,index=None):
    """ 
    Provided with either a variable name (ALIAS) or the string for a grid definition,
    returns a grid_definition where the domain has been changed  to DOMAIN
    """
    if src_grid_string is None:
        if alias is None :
            raise dr2xml_error("change_domain_in_grid: must provide alias or grid_string ")
        src_grid=id2grid(alias,index)
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
        raise dr2xml_error("Fatal: cannot find a domain to change in src_grid_string %s for %s"%(src_grid_string,alias))
    target_grid_string=re.sub('grid id= *.([\w_])*.','grid id="%s"'%target_grid_id,target_grid_string)
    return (target_grid_id,target_grid_string)

def create_grid_def(sd,axis_key,alias=None,context_index=None):
    # mpmoine_correction:create_grid_def:  si, il faut generer une grille autour des axes de zoom aussi
    #if not sd.is_zoom_of and not sd.is_union_for: # a grid_def to build in classical case (a vertical axis without using union)
    if alias and context_index:
        src_grid=id2grid(alias,context_index,printout=True)
        if src_grid is not None : 
            src_grid_id=src_grid.attrib['id']
            src_grid_string=ET.tostring(src_grid)
            target_grid_id=src_grid_id+"_"+axis_key
            # Change only first instance of axis_ref, which is assumed to match the vertical dimension
            (target_grid_string,count)=re.subn('axis *id= *.([\w_])*.','axis id="%s"'%axis_key,src_grid_string,1)
            if count != 1 : 
                raise dr2xml_error("Fatal: cannot find an axis_ref to change in src_grid_string %s for %s"%\
                                   (src_grid_string,alias))
            target_grid_string=re.sub('grid id= *.([\w_])*.','grid id="%s"'%target_grid_id,target_grid_string)
            return (target_grid_id,target_grid_string)
        else:
            raise dr2xml_error("Fatal: ask for creating a grid_def for var %s which has no grid "%(alias))
        #return False
    else:
        raise dr2xml_error("Fatal: ask for creating a grid_def from a native grid "+\
                           "but variable alias and/or context_index not provided (alias:%s, context_index:%s)"%(alias,context_index))
        #return False
    # elif sd.is_union_for: # a grid_def to build in union case
    #     grid_id="grid_"+axis_key
    #     grid_string='<grid id="%s">'%grid_id
    #     grid_string+='\n\t<domain domain_ref="%s"/>'%"domain_atm" # mpmoine_note: attention, en dur !
    #     grid_string+='\n\t<axis axis_ref="%s"/>'%axis_key
    #     grid_string+='\n\t</grid>'
    #     return (grid_id,grid_string)
    # elif sd.is_zoom_of: # a grid_def to build in zoom case
    #     grid_id="grid_"+axis_key
    #     grid_string='<grid id="%s">'%grid_id
    #     grid_string+='\n\t<domain domain_ref="%s"/>'%"domain_atm" # mpmoine_note: attention, en dur !
    #     grid_string+='\n\t<axis axis_ref="%s"/>'%axis_key
    #     grid_string+='\n\t</grid>'
    #     return (grid_id,grid_string)
    # else:
    #     print "Warning: calling create_grid_def for a vertical axis which nothing among classical/union/zoom... Humm, don't know what this axis is..."
    #     return False

# mpmoine_zoom_modif: nouvelle fonction 'create_xios_axis_for_plevs_unions'
# mpmoine_merge_dev2_v0.12: 'create_xios_axis_for_plevs_unions' renomee en 'create_xios_axis_and_grids_for_plevs_unions'
def create_xios_axis_and_grids_for_plevs_unions(svars,plev_sfxs,prefix,printout=False): 
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
            # mpmoine_note: couvre les dimensions verticales de type 'plev7h' ou 'p850'
            if sd.label.startswith("p") and any(sd.label.endswith(s) for s in plev_sfxs): 
                lwps=sv.label_without_psuffix
                if lwps:
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
                    # svar will be expected on a zoom axis of the union. Corresponding vertical dim must
                    # have a zoom_label named plevXX_<lwps> (multiple pressure levels) or pXX_<lwps> (single pressure level)
                    sv.sdims[sd.label].zoom_label='zoom_'+sd.label+"_"+lwps 
                else:
                    print "Warning: dim is pressure but label_without_psuffix=", lwps, \
                            "for",sv.label, sv.mipTable, sv.mip_era
    #
    # Second, create xios axis for union of plevs
    union_axis_defs={}
    union_grid_defs={}
    for lwps in dict_plevs.keys():
        sdim_union=simple_Dim()
        plevs_union_xios=""
        plevs_union=set()
        for plev in dict_plevs[lwps].keys():  
            plev_values=[]
            for sv in dict_plevs[lwps][plev].values(): 
                if not plev_values:
                    # svar is the first one with this plev => get its level values
                    # mpmoine_note: on reecrase les attributs de sdim_union a chaque nouveau plev. Pas utile mais
                    # mpmoine_note: c'est la facon la plus simple de faire
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
                if printout: print "       *",svar.label,"(",svar.mipTable,")"
        list_plevs_union=list(plevs_union)
        # mpmoine_further_zoom_modif:create_xios_axis_for_plevs_unions: correction du tri des niveaux de pression sur les axes d'union
        list_plevs_union_num=[float(lev) for lev in list_plevs_union]
        list_plevs_union_num.sort(reverse=True)
        list_plevs_union=[str(lev) for lev in list_plevs_union_num]
        for lev in list_plevs_union: plevs_union_xios+=" "+lev
        if printout: print ">>> XIOS plevs union:", plevs_union_xios
        sdim_union.label="union_plevs_"+lwps
        if len(list_plevs_union)>1: sdim_union.requested=plevs_union_xios
        if len(list_plevs_union)==1: sdim_union.value=plevs_union_xios
        axis_def=create_axis_def(sdim_union,prefix)
        union_axis_defs.update({sdim_union.label:axis_def})
        # mpmoine_merge_dev2_v0.12: maintenant on doit non seulement creer les axes d'union mais aussi les grid les englobant
        # SS : ajout des deux derniers arguments, pour ne pas avoir de domains en dur dans create_grid_def
        grid_def=create_grid_def(sdim_union,sdim_union.label,prefix+lwps,context_index)
        grid_id=grid_def[0]
        union_grid_defs[grid_id]=grid_def[1]
    #
    return (union_axis_defs,union_grid_defs)

def isVertDim(sdim):
    """
    Returns True if dim represents a dimension for which we want 
    an Xios interpolation. 
    For now, a very simple logics for interpolated vertical 
    dimension identification:
    """
    # mpmoine_future_modif: isVertDim: on utilise maintenant sv.sdims pour analyser les dimensions
    # SS : p840, p220 sont des couches de pression , pour lesquelles COSP forunit directement
    # les valeurs moyennes de paramètres (e.g. cllcalipso). On les detecte par l'attribut bounds 
    test=(sdim.stdname=='air_pressure' or sdim.stdname=='altitude') and (sdim.bounds != "yes")
    return test

def analyze_cell_time_method(cm,label,table):
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
        print "TBD: Cannot yet handle time: mean (with samples weighted by snow mass) for "+\
            "%15s in table %s -> averaging"%(label,table)
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean where cloud"  in cm : 
        #[amncl-twm]: Weighted Time Mean on Cloud (2 variables ISSCP 
        # albisccp et pctisccp, en emDay et emMon)
        print "Note : assuming that 'time: mean where cloud' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #-------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where sea_ice_melt_pound"
    elif "time: mean where sea_ice_melt_pound" in cm :
        #[amnnsimp-twmm]: Weighted Time Mean in Sea-ice Melt Pounds (uniquement des 
        #variables en SImon)
        print "Note : assuming that 'time: mean where sea_ice_melt_pound' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #-------------------------------------------------------------------------------------------------
    elif "time: mean where sea_ice" in cm :
        #[amnsi-twm]: Weighted Time Mean on Sea-ice (presque que des 
        #variables en SImon, sauf sispeed et sithick en SIday)
        # mpmoine_correction:analyze_cell_time_method: ajout de operation="average" pour "time: mean where sea_ice"
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
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where floating_ice_shelf"
    elif "time: mean where floating_ice_shelf" in cm :
        #[amnfi-twmn]: Weighted Time Mean on Floating Ice Shelf (presque que des 
        #variables en Imon, Iyr, sauf sftflt en LImon !?)
        print "Note : assuming that 'time: mean where floating_ice_shelf' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where grounded_ice_sheet"
    elif "time: mean where grounded_ice_sheet" in cm :
        #[amngi-twm]: Weighted Time Mean on Grounded Ice Shelf (uniquement des 
        #variables en Imon, Iyr)
        print "Note : assuming that 'time: mean where grounded_ice_sheet' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where ice_sheet"
    elif "time: mean where ice_sheet" in cm :
        #[amnni-twmn]: Weighted Time Mean on Ice Shelf (uniquement des 
        #variables en Imon, Iyr)
        print "Note : assuming that 'time: mean where ice_sheet' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where landuse"
    elif "time: mean where landuse" in cm :
        #[amlu-twm]: Weighted Time Mean on Land Use Tiles (uniquement des 
        #variables suffixees en 'Lut')
        print "Note : assuming that 'time: mean where landuse' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where crops"
    elif "time: mean where crops" in cm :
        #[amc-twm]: Weighted Time Mean on Crops (uniquement des 
        #variables suffixees en 'Crop')
        print "Note : assuming that 'time: mean where crops' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where natural_grasses"
    elif "time: mean where natural_grasses" in cm :
        #[amng-twm]: Weighted Time Mean on Natural Grasses (uniquement des 
        #variables suffixees en 'Grass')
        print "Note : assuming that 'time: mean where natural_grasses' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where shrubs"
    elif "time: mean where shrubs" in cm :
        #[ams-twm]: Weighted Time Mean on Shrubs (uniquement des 
        #variables suffixees en 'Shrub')
        print "Note : assuming that 'time: mean where shrubs' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where trees"
    elif "time: mean where trees" in cm :
        #[amtr-twm]: Weighted Time Mean on Bare Ground (uniquement des 
        #variables suffixees en 'Tree')
        print "Note : assuming that 'time: mean where trees' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas "time: mean where vegetation"
    elif "time: mean where vegetation" in cm :
        #[amv-twm]: Weighted Time Mean on Vegetation (pas de varibles concernees)
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
        print "TBD: Cannot yet compute annual climatology for "+\
            "%15s in table %s -> averaging"%(label,table)
        # Could transform in monthly fields to be post-processed
        operation="average"
    #----------------------------------------------------------------------------------------------------------------
    elif "time: mean within days time: mean over days"  in cm: 
        #[amn-tdnl]: Mean Diurnal Cycle
        print "TBD: Cannot yet compute diurnal cycle for "+\
        " %15s in table %s -> averaging"%(label,table)
    #----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas 'Maximum Hourly Rate'
    elif "time: mean within hours time: maximum over hours"  in cm: 
        #[amn-tdnl]: Mean Diurnal Cycle
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
# mpmoine_amelioration: ajout argument 'path_special' a la fonction pingFileForRealmsList
def pingFileForRealmsList(context,lrealms,svars,path_special,dummy="field_atm",
    dummy_with_shape=False, exact=False,
    comments=False,prefix="CV_",filename=None):
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
    #if lset["use_area_suffix"] :
    #    lvars.sort(key=lambda x:x.label_with_area)
    #else:
    # mpmoine_future_modif:pingFileForRealmsList: on s'appuie sur le mipVar label (label_without_area) et non plus le cmorVar label
    # mpmoine_zoom_modif:pingFileForRealmsList: on s'appuie sur le label_without_psuffix et non plus le label_without_area
    lvars.sort(key=lambda x:x.label_without_psuffix)
    # Remove duplicates
    uniques=[] ; last_label=""
    for v in lvars : 
        # mpmoine_future_modif:pingFileForRealmsList: on s'appuie sur le mipVar label (label_without_area) et non plus le cmorVar label
        # mpmoine_zoom_modif:pingFileForRealmsList: on s'appuie sur le label_without_psuffix et non plus le label_without_area
        if v.label_without_psuffix!= last_label : 
            uniques.append(v)
            # mpmoine_future_modif:pingFileForRealmsList: on s'appuie sur le mipVar label (label_without_area) et non plus le cmorVar label
            # mpmoine_zoom_modif:pingFileForRealmsList: on s'appuie sur le label_without_psuffix et non plus le label_without_area
            last_label=v.label_without_psuffix
    lvars=uniques
    #
    if filename is None : filename="ping"+name+".xml"
    # mpmoine_future_modif:pingFileForRealmsList: typo 'filneme' -> 'filename'
    if filename[-4:] != ".xml" : filename +=".xml"
    #
    # mpmoine_amelioration:pingFileForRealmsList:: ajout argument 'path_special' a la fonction read_special_fields_defs + protection si path_special existe
    if path_special: 
        specials=read_special_fields_defs(lrealms,path_special)
    else: 
        specials=False
    with open(filename,"w") as fp:
        fp.write('<!-- Ping files generated by dr2xml %s using Data Request %s -->\n'%(version,dq.version))
        fp.write('<!-- lrealms= %s -->\n'%`lrealms`)
        fp.write('<!-- exact= %s -->\n'%`exact`)
        fp.write('<context id="%s">\n'%context)
        fp.write("<field_definition>\n")
        if exact : 
            fp.write("<!-- for variables which realm intersects any of "\
                     +name+"-->\n")
        else:
            fp.write("<!-- for variables which realm equals one of "\
                     +name+"-->\n")
        for v in lvars :
            # mpmoine_future_modif:pingFileForRealmsList: pour le field_id du pingfile on s'appuie sur le 'label_without_psuffix' et non plus le label complet
            # mpmoine_correction:pingFileForRealmsList: pour le field_id du pingfile on prend le label non ambigu s'il existe
            if v.label_non_ambiguous: 
                label=v.label_non_ambiguous
            else:
                label=v.label_without_psuffix
            # mpmoine_amelioration:pingFileForRealmsList: protection si specials existe
            if specials and label in specials :
                line=ET.tostring(specials[label]).replace("DX_",prefix)
                line=line.replace("\n","").replace("\t","")
                fp.write('   '); fp.write(line)
            else:
                fp.write('   <field id="%-20s'%(prefix+label+'"')+\
                         ' field_ref="')
                if dummy : 
                    # mpmoine_last_modif: svar en argument de highest_rank et non pas seulement son label_without_area
                    # mpmoine_zoom_modif:pingFileForRealmsList: on s'appuie sur le label_without_psuffix et non plus le label_without_area
                    shape=highest_rank(v)
                    # Bugfix for DR 1.0.1 content :
                    # mpmoine_future_modif:pingFileForRealmsList: on s'appuie sur le mipVar label (label_without_area) et non plus le cmorVar label
                    # mpmoine_zoom_modif:pingFileForRealmsList: on s'appuie sur le label_without_psuffix et non plus le label_without_area
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
        fp.write("</field_definition>\n")
        #
        print "%3d variables written for %s"%(len(lvars),filename)
        #
        # Write axis_defs, domain_defs, ... read from relevant input/DX_ files
        # mpmoine_amelioration:pingFileForRealmsList: protection si path_special existe
        if path_special:
            for obj in [ "axis", "domain", "grid" ] :
                #print "for obj "+obj
                # mpmoine_amelioration:pingFileForRealmsList: ajout argument 'path_special' a la fonction copy_obj_from_DX_file
                copy_obj_from_DX_file(fp,obj,prefix,lrealms,path_special)
        fp.write('</context>\n')

# mpmoine_amelioration: ajout argument 'path_special' a la fonction copy_obj_from_DX_file
def copy_obj_from_DX_file(fp,obj,prefix,lrealms,path_special) :
    # Insert content of DX_<obj>_defs files (changing prefix)
    #print "copying %s defs :"%obj,
    subrealms_seen=[]
    for realm in lrealms :
        for subrealm in realm.split() :
            if subrealm in subrealms_seen : continue
            subrealms_seen.append(subrealm)
            #print "\tand realm %s"%subrealm, 
            # mpmoine_amelioration:opy_obj_from_DX_file: ajout argument 'path_special' a la fonction DX_defs_filename
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

# mpmoine_amelioration: ajout argument 'path_special' a la fonction DX_defs_filename
def DX_defs_filename(obj,realm,path_special):
    #TBS# return prog_path+"/inputs/DX_%s_defs_%s.xml"%(obj,realm)
    return path_special+"/DX_%s_defs_%s.xml"%(obj,realm)

# mpmoine_future_modif: renommage de la fonction 'field_defs' en 'get_xml_childs'
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

# mpmoine_future_modif: renommage de la fonction 'read_defs' en 'read_xml_elmt_or_attrib'
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

# mpmoine_amelioration: ajout de l'argument 'path_special' a la fonction read_special_field_defs
def read_special_fields_defs(realms,path_special,printout=False) :
    special=dict()
    subrealms_seen=[]
    for realm in realms  :
        for subrealm in realm.split() :
            if subrealm in subrealms_seen : continue
            subrealms_seen.append(subrealm)
            # mpmoine_amelioration:read_special_fields_defs: ajout de l'argument 'path_special' a la fonction DX_defs_filename
            d=read_xml_elmt_or_attrib(DX_defs_filename("field",subrealm,path_special),\
                                        tag='field',printout=printout)
            if d: special.update(d)
    rep=dict()
    # Use raw label as key
    for r in special : rep[r.replace("DX_","")]=special[r]
    return rep

# mpmoine_last_modif:highest_rank: svar en argument et non pas seulement son label_without_area
def highest_rank(svar):
    """Returns the shape with the highest needed rank among the CMORvars
    referencing a MIPvar with this label
    This, assuming dr2xml would handle all needed shape reductions
    """
    mipvarlabel=svar.label_without_area
    shapes=[]
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
                        print "DR Error: issue with stid or spid for "+\
                        st.label+" "+v.label+string(cvar.mipTable)
                    # One known case in DR 1.0.2: hus in 6hPlev
                    shape="XY"
            except :
                print "DR Error: issue with stid for "+v.label+string(cvar.mipTableSection)
                shape="?st"
        else:
            # Pour recuperer le spatial_shp pour le cas de variables qui n'ont
            # pas un label CMORvar de la DR (ex. HOMEvar ou EXTRAvar)
            shape=svar.spatial_shp
        if shape: shapes.append(shape)
    #if not shapes : shape="??"
    if not shapes : shape="XY"
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
    elif any([ "Y-A"  in s for s in shapes]) : shape="lat-A" #XYZ
    elif any([ "Y-P"  in s for s in shapes]) : shape="lat-P" #XYZ
    elif any([ "Y-na" in s for s in shapes]) : shape="lat"
    elif any([ "TRS-na" in s for s in shapes]): shape="TRS"
    elif any([ "TR-na" in s for s in shapes]) : shape="TR"
    elif any([ "L-na" in s for s in shapes]) :  shape="COSPcurtain"
    elif any([ "L-H40" in s for s in shapes]) : shape="COSPcurtainH40"
    elif any([ "S-na" in s for s in shapes]) :  shape="XY" # fine once remapped
    elif any([ "na-na" in s for s in shapes]) : shape="0d" # analyser realm
    #else : shape="??"
    else : shape="XY"

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
    domain_defs['50km']='<domain id="CMIP6_50km" ni_glo="720" nj_glo="360" type="rectilinear"  prec="8"> '+\
      '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute"/> '+\
    '</domain>  '
    domain_defs['100km']='<domain id="CMIP6_100km" ni_glo="360" nj_glo="180" type="rectilinear"  prec="8"> '+\
      '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute"/> '+\
    '</domain>  '
    domain_defs['1deg']='<domain id="CMIP6_1deg" ni_glo="360" nj_glo="180" type="rectilinear"  prec="8"> '+\
      '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute"/> '+\
    '</domain>  '
    domain_defs['2deg']='<domain id="CMIP6_2deg" ni_glo="180" nj_glo="90" type="rectilinear"  prec="8"> '+\
      '<generate_rectilinear_domain/> <interpolate_domain order="1" renormalize="true"  mode="read_or_compute"/> '+\
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
    rep='<file id="%s" name="%s" mode="read" output_freq="1ts">\n'%(cfsites_grid_file_id,cfsites_grid_file_id)+\
      '\t<field id="%s" operation="instant" grid_ref="%s" />\n'%(cfsites_grid_field_id,cfsites_grid_id)+\
      ' </file>'
    return rep
    


def build_axis_definitions():
    """ 
    Build a dict of axis definitions 
    """
    for g in dq.coll['grids'].items :
        pass

class dr2xml_error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
    def __str__(self):
        return `self.valeur`
    #""" just for test"""
