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

First version (0.8) : S.Sénési (CNRM) - sept 2016

Changes :
  oct 2016 - Marie-Pierre Moine (CERFACS) - handle 'home' Data Request 
                               in addition
  dec 2016 - S.Sénési (CNRM) - improve robustness
  jan 2017 - S.Sénési (CNRM) - handle split_freq; go single-var files; 
                               adapt to new DRS ...
  feb 2017 - S.Sénési (CNRM) - handle grids and remapping; 
                               put some func in separate module

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
version="mpmoine-dev3 = mpmoine-dev2 merged with senesi-dev-v0.12"

from datetime import datetime
import re
import json
import collections
import sys,os
import xml.etree.ElementTree as ET

# mpmoine_merge_dev2_v0.12: posixpath.dirname ne marche pas chez moi
#from os import path as os_path
#prog_path=os_path.abspath(os_path.split(__file__)[0])

# Local packages
# mpmoine_zoom_modif: import simple_Dim
from vars import simple_CMORvar, simple_Dim, process_homeVars, complement_svar_using_cmorvar, \
                multi_plev_suffixes, single_plev_suffixes
from grids import decide_for_grids, grid2resol, grid2desc, field_size,\
    split_frequency_for_variable, timesteps_per_freq_and_duration
from Xparse import init_context, id2grid

# A local auxilliary table
# mpmoine_last_modif: dr2xml.py: ajout import de cmipFreq2xiosFreq
from table2freq import table2freq, table2splitfreq, cmipFreq2xiosFreq

from dr2cmip6_expname import dr2cmip6_expname

print_DR_errors=False

dq = dreq.loadDreq()
print dq.version

context_index=None

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
                          }, 
    # Some variables, while belonging to a realm, may fall in another XIOS context than the 
    # context which hanldes that realm
    'orphan_variables' : { 'nemo' : ['dummy_variable_for_illustration_purpose'],
                        ' arpsfx' : [],
                           },
    'vars_OK' : dict(),
    # A per-variable dict of comments valid for all simulations
    'comments'     : {
        'tas' : 'nothing special about tas'
        },
    # Sizes for atm and oce grids (cf DR doc)
    "sizes"  : [259200,60,64800,40,20,5,100],
    # What is the maximum size of generated files, in number of float values
    "max_file_size_in_floats" : 500.*1.e+6 ,
    # grid_policy among None, DR, native, native+DR, adhoc- see docin grids.py 
    "grid_policy" : "adhoc",
    # Grids : CMIP6 name, name_of_target_domain, CMIP6-std resolution, and description
    "grids" : { 
      "LR"    : {
        "arpsfx" : [ "gr","complete" , "250 km", "data regridded to a T127 gaussian grid (128x256 latlon) from a native atmosphere T127l reduced gaussian grid"] ,
          "nemo" : [ "gn", ""        , "100km" , "native ocean tri-polar grid with 105 k ocean cells" ],},
      "HR"    : {
        "arpsfx" : [ "gr","completeHR", "50 km", "data regridded to a 359 gaussian grid (180x360 latlon) from a native atmosphere T359l reduced gaussian grid"] ,
          "nemo" : [ "gn", ""         , "25km" , "native ocean tri-polar grid with 1.47 M ocean cells" ],},
    },
    'grid_choice' : { "CNRM-CM6-1" : "LR", "CNRM-CM6-1-HR" : "HR",
                      "CNRM-ESM2-1": "LR"  , "CNRM-ESM2-1-HR": "HR" },

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
        if False and printout and len(d[v]) > 1 :
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
                     
# mpmoine_last_modif:wr: ajout de l'argument num_type
# mpmoine_zoom_modif:wr: ajout de l'argument out (car fonction remontee d un niveau)
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
        out.write('  <variable name="%s"  type="string" > %s '%(key,val))
        out.write('  </variable>\n')

def write_xios_file_def(cmv,table,lset,sset,out,cvspath,
    field_defs,axis_defs,grid_defs,domain_defs,
    dummies,skipped_vars_per_table,
    prefix,context,grid,pingvars=None) :
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
    # We use a simple convention for variable names in ping files : 
    if cmv.type=='perso' : alias=cmv.label
    else:
        alias=lset["ping_variables_prefix"]+cmv.label
        if pingvars is not None :
            # mpmoine_zoom_modif:write_xios_file_def: dans le pingfile, on attend plus les alias complets  des variables (CMIP6_<label>) mais les alias reduits (CMIP6_<lwps>)
            # mpmoine_zoom_modif:write_xios_file_def: => creation de alias_ping
            alias_ping=lset["ping_variables_prefix"]+cmv.label_without_psuffix # e.g. 'CMIP6_hus' and not 'CMIP6_hus7h'
            if not alias_ping in pingvars:
                # mpmoine_skipped_modif: write_xios_file_def: on classe les skipped_vars par table => skipped_vars_per_table (pour avoir plus d'info au print) 
                if skipped_vars_per_table.has_key(cmv.mipTable) and skipped_vars_per_table[cmv.mipTable]:
                    list_of_skipped=skipped_vars_per_table[cmv.mipTable]
                    list_of_skipped.append(cmv.label)
                else:
                    list_of_skipped=[cmv.label]
                skipped_vars_per_table.update({cmv.mipTable:list_of_skipped})
                return
    #
    #--------------------------------------------------------------------
    # Set global CMOR file attributes
    #--------------------------------------------------------------------
    source_id=lset['source_id']
    experiment_id=sset['experiment_id']
    # Variant matters
    realization_index=sset.get('realization_index',1) 
    initialization_index=sset.get('initialization_index',1)
    physics_index=sset.get('physics_index',1)
    forcing_index=sset.get('forcing_index',1)
    variant_label="r%di%dp%df%d"%(realization_index,initialization_index,\
                                  physics_index,forcing_index)
    # WIP Draft 14 july 2016
    activity_id=sset.get('activity_id','CMIP')
    #
    # WIP doc v 6.2.0 - dec 2016 
    # <variable_id>_<table_id>_<source_id>_<experiment_id >_<member_id>_<grid_label>[_<time_range>].nc
    member_id=variant_label
    # mpmoine_future_modif:write_xios_file_def: CMOR3.2.2 impose 'None' pour sub_experiment_id
    sub_experiment_id=sset.get('sub_experiment_id','None')
    if sub_experiment_id != 'none': member_id = sub_experiment_id+"-"+member_id
    #
    #--------------------------------------------------------------------
    # Set grid info
    #--------------------------------------------------------------------
    if grid == "" :
        # either native or close-to-native
        grid_choice=lset['grid_choice'][source_id]
        grid_label,remap_domain,grid_resolution,grid_description=\
        lset['grids'][grid_choice][context]
    else:
        # DR requested type of grid
        grid_label=grid
        remap_domain=lset["ping_variables_prefix"]+grid
        grid_description=grid2desc(grid)
        grid_resolution=grid2resol(grid)
    if table in [ 'AERMonZ',' EmonZ', 'EdayZ' ] : grid_label+="z"
    if "Ant" in table : grid_label+="a"
    if "Gre" in table : grid_label+="g"
    # TBD : change grid_label depending on shape (sites, transects)
    #
    time_range="%start_date%_%end_date%" # XIOS syntax
    #
    #--------------------------------------------------------------------
    # Set NetCDF output file name according to the DRS
    #--------------------------------------------------------------------
    #
    # mpmoine_expname:write_xios_file_def: es noms d'expe dans la DR ne sont pas les meme que dans le CV CMIP6
    with open(cvspath+"CMIP6_experiment_id.json","r") as json_fp :
        CMIP6_experiments=json.loads(json_fp.read())['experiment_id']
        if CMIP6_experiments.has_key(sset['experiment_id']):
            expname=sset['experiment_id']
        else:
            # mpmoine_last_modif:write_xios_file_def: provisoire, laisser passer cette erreur tant que le
            # mpmoine_last_modif:write_xios_file_def: CV_CMIP6 et celui de la DR ne sont pas concordants
            dr2xml_error("Issue getting experiment description in CMIP6 CV for %20s => Search for experiment name correspondance from DR to CMIP6 CV."\
                               %sset['experiment_id'])
            expname=dr2cmip6_expname[sset['experiment_id']]
        exp_entry=CMIP6_experiments[expname]
        experiment=exp_entry['experiment']
        description=exp_entry['description']
    print ">>> DEBUG >>>",expname
    #
    filename="%s%s_%s_%s_%s_%s_%s_%s"%\
               (prefix,cmv.label,table,source_id,expname,
                member_id,grid_label,time_range)
    #
    #--------------------------------------------------------------------
    # Compute XIOS split frequency
    #--------------------------------------------------------------------
    # mpmoine_last_modif:write_xios_file_def: Maintenant, dans le cas type='perso', table='NONE'. On ne doit donc pas compter sur le table2freq pour recuperer
    # mpmoine_last_modif:write_xios_file_def: la frequence en convention xios => fonction cmipFreq2xiosFreq
    # mpmoine_next_modif: write_xios_file_def: passage de 'context' en argument de split_frequency_for_variable pour recuperer le model_timestep
    split_freq=split_frequency_for_variable(cmv, lset, sc.mcfg, context)
    #
    #--------------------------------------------------------------------
    # Write XIOS file node:
    # including global CMOR file attributes
    #--------------------------------------------------------------------
    out.write(' <file name="%s" output_freq="%s" '% (filename,cmipFreq2xiosFreq[cmv.frequency]))
    out.write('  append="true" split_freq="%s" '%split_freq)
    #out.write('timeseries="exclusive" >\n')
    out.write(' time_units="days" time_counter_name="time"')
    out.write(' time_stamp_name="creation_date" ')
    out.write(' time_stamp_format="%Y-%m-%dT%H:%M:%SZ"')
    out.write(' uuid_name="tracking_id" uuid_format="hdl:21.14100/%uuid%"')
    out.write(' >\n')
    #
    wr(out,'project_id', sset.get('project',"CMIP6")+"/"+activity_id)
    wr(out,'activity_id',activity_id)
    contact=sset.get('contact',lset.get('contact',None))
    if contact and contact is not "" : wr(out,'contact',contact) 
    conventions="CF-1.7 CMIP-6.0" ;     wr(out,'Conventions',conventions) 
    # TBC : assume data_specs_version == dq.version
    wr(out,'data_specs_version',dq.version) 
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
    wr(out,'forcing_index',forcing_index) 
    # mpmoine_last_modif: Maintenant, dans le cas type='perso', table='NONE'. On ne doit donc pas compter sur table2freq pour recuperer la frequence
    wr(out,'frequency',cmv.frequency)
    #
    # URL
    # mpmoine_last_modif:write_xios_file_def: mip_era n'est plus toujours 'CMIP6'
    mip_era=cmv.mip_era
    institution_id=lset['institution_id']
    source_id=lset['source_id']
    # mpmoine_future_modif:write_xios_file_def: CMOR3.2.2 impose 'None' pour sub_experiment
    sub_experiment_id=sset.get('sub_experiment_id','None')
    further_info_url="http://furtherinfo.es-doc.org/%s.%s.%s.%s.%s.%s"%(
        mip_era,institution_id,source_id,experiment_id,
        sub_experiment_id,variant_label)
    wr(out,'further_info_url',further_info_url)
    #
    wr(out,'grid',grid_description) ; wr(out,'grid_label',grid_label) ;
    wr(out,'nominal_resolution',grid_resolution)    
    wr(out,'history',sset,'none') 
    wr(out,"initialization_index",initialization_index)
    wr(out,"institution_id",institution_id)
    if "institution" in lset :
        inst=lset['institution']
    else:
        with open(cvspath+"CMIP6_institution_id.json","r") as json_fp :
            try:
                inst=json.loads(json_fp.read())['institution_id'][institution_id]
            except :
                raise(dr2xml_error("Institution_id for %s not found "+\
                        "in CMIP6_CV at %s"%(institution,cvspath)))
    wr(out,"institution",inst)
    #
    with open(cvspath+"CMIP6_license.json","r") as json_fp :
        license=json.loads(json_fp.read())['license'][0]
    license=license.replace("<Your Centre Name>",inst)
    license=license.replace("<some URL maintained by modeling group>",
                            lset["info_url"])
    wr(out,"license",license)
    wr(out,'mip_era',mip_era)
    parent_experiment_id=sset.get('parent_experiment_id',None)
    if parent_experiment_id and parent_experiment_id != 'no_parent'\
        and parent_experiment_id != 'no parent' :
        parent_activity_id=sset.get('parent_activity_id','CMIP')
        wr(out,'parent_activity_id',parent_activity_id)
        wr(out,"parent_experiment_id",sset); 
        parent_mip_era=sset.get('parent_mip_era',"CMIP6") ; 
        if parent_mip_era=="" : parent_mip_era="CMIP6"
        wr(out,'parent_mip_era',parent_mip_era) 
        parent_source_id=sset.get('parent_source_id',source_id) ; 
        wr(out,'parent_source_id',parent_source_id)
        # TBX : syntaxe XIOS pour designer le time units de la simu courante
        parent_time_ref_year=sset.get('parent_time_ref_year',"1850") 
        parent_time_units="days since %s-01-01 00:00:00"%parent_time_ref_year
        wr(out,"parent_time_units",parent_time_units)
        parent_variant_label=sset.get('parent_variant_label',variant_label) 
        wr(out,'parent_variant_label',parent_variant_label)
        wr(out,'branch_method',sset,'standard')
        wr(out,'branch_time_in_child',sset)
        wr(out,'branch_time_in_parent',sset) 
    wr(out,"physics_index",physics_index) 
    wr(out,'product','output')
    wr(out,"realization_index",realization_index) 
    wr(out,'realm',cmv.modeling_realm)
    wr(out,'references',lset) 
    #
    try:
        with open(cvspath+"CMIP6_source_id.json","r") as json_fp :
            sources=json.loads(json_fp.read())['source_id']
            source=make_source_string(sources,source_id)
    except :
        if "source" in lset : source=lset['source']
        else:
            raise(dr2xml_error("source for %s not found in CMIP6_CV at"+\
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
                raise dr2xml_error("No source-type found - Check inputs")
    if type(source_type)==type([]) :
        source_type=reduce(lambda x,y : x+" "+y, source_type)
    wr(out,'source_type',source_type)
    #
    wr(out,'sub_experiment_id',sub_experiment_id) 
    # mpmoine_future_modif:write_xios_file_def: CMOR3.2.2 impose 'None' pour sub_experiment_id
    wr(out,'sub_experiment',sset,'None') 
    wr(out,"table_id",table)
    wr(out,"title","%s model output prepared for %s / %s %s"%(\
        source_id,sset.get('project',"CMIP6"),activity_id,experiment_id))
    wr(out,"variable_id",cmv.label)
    wr(out,"variant_info",sset,"")
    wr(out,"variant_label",variant_label)
    #
    #--------------------------------------------------------------------
    # Build all XIOS auxilliary elements (end_file_defs, field_defs, domain_defs, grid_defs, axis_defs)
    #---
    # Write XIOS field_group node (containing field elements, stored in end_field_defs)
    # including CF field attributes 
    #--------------------------------------------------------------------
    #mpmoine_zoom_modif:write_xios_file_def: appel a create_xios_aux_elmts_defs (anc. create_xios_field_ref) descendu ici
    end_field_defs=dict()
    create_xios_aux_elmts_defs(cmv,alias,table,lset,sset,end_field_defs,
                                field_defs,axis_defs,grid_defs,domain_defs,dummies,context,remap_domain,pingvars)
    if len(end_field_defs.keys())==0 :
        # TBD : restore error_message
        #raise dr2xml_error("No end field ref for %s in %s"%(cmv.label,table))
        return
    #
    # Create a field group for each shape
    for shape in end_field_defs :
        dom="" ;
        if shape : dom='grid_ref="%s"'%shape
        out.write('<field_group %s expr="@this" >\n'%dom)
        for entry in end_field_defs[shape] : out.write(entry)
        out.write('</field_group >\n')
    out.write('</file>\n\n')

 # mpmoine_last_modif:wrv: ajout de l'argument num_type

def wrv(name, value, num_type="string"):
    # Format a 'variable' entry
    return '     <variable name="%s" type="string" > %s '%(name,value)+\
        '</variable>\n'

# mpmoine_zoom_modif: renommage de la fonction 'create_xios_field_ref' en 'create_xios_aux_elmts_defs'
# mpmoine_zoom_modif: renommage de la fonction 'create_xios_field_ref' en 'create_xios_aux_elmts_defs'
def create_xios_aux_elmts_defs(sv,alias,table,lset,sset,end_field_defs,
    field_defs,axis_defs,grid_defs,domain_defs,dummies,context,remap_domain,pingvars) :
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

    # nextvar is the field name provided as output of the last
    # operation currently defined
    # mpmoine_union_modif:create_xios_aux_elmts_defs: on supprime l'usage de netxvar
    #
    #--------------------------------------------------------------------
    # Build XIOS axis elements (stored in axis_defs)
    # Proceed with vertical interpolation if needed
    #---
    # Build XIOS auxilliary field elements (stored in field_defs)
    #--------------------------------------------------------------------
    ssh=sv.spatial_shp
    prefix=lset["ping_variables_prefix"]
    # mpmoine_zoom_modif:create_xios_aux_elmts_defs: recup de lwps
    lwps=sv.label_without_psuffix
    # TBD Should handle singletons here => mpmoine_note: la mecanique des zoom/union couvre aussi les dim verticale singleton
    # TBD Should ensure that various additionnal dims are duly documented by model or pingfile (e.g. tau)
    # mpmoine_zoom_modif:create_xios_aux_elmts_defs: ajout du cas 'XY-na' pour capturer les dimensions singleton
    if ssh[0:4] in ['XY-H','XY-P'] or ssh[0:3] == 'Y-P' or ssh[0:5]=='XY-na':
        # TBD : for now, do not interpolate vertically
        # mpmoine_temporaire:je reactive l'ecriture des axis_def: return
        # mpmoine_last_modif:create_xios_aux_elmts_defs: on recupere maintenant 'dimids' depuis svar
        # mpmoine_future_modif:create_xios_aux_elmts_defs: on utilise maintenant sv.sdims pour analyser les dimension
        # mpmoine_question: je ne comprend pas l'usage de nextvar... A priori on ne peut pas avoir plus d'une dimension verticale ?
        for sd in sv.sdims.values():
            if isVertDim(sd):
                # mpmoine_zoom_modif:create_xios_aux_elmts_defs: on supprime l'usage de netxvar
                # mpmoine_zoom_modif:create_xios_aux_elmts_defs: passage par 2 niveaux de field id auxiliaires rebond (alias et alias2)
                if sd.is_zoom_of: # mpmoine_note: cas variable definie grace a 2 axis_def (zoom+union)
                    alias1=alias+"_"+sd.label   # e.g. 'CMIP6_hus7h_plev7h'
                    alias2=prefix+lwps+"_union" # e.g. 'CMIP6_hus_union'
                    cible=prefix+lwps           # e.g. 'CMIP6_hus'
                    axis_key=sd.zoom_label      # e.g. 'zoom_plev7h_hus'
                else: # mpmoine_note: cas variable definie grace a seul axis_def (non zoom)
                    alias1=alias+"_"+sd.label   # e.g. 'CMIP6_hus7h_plev7h'
                    alias2=False 
                    cible=prefix+lwps           # e.g. 'CMIP6_hus'
                    axis_key=sd.label           # e.g. 'plev7h'
                if not cible in pingvars:       # e.g. alias_ping='CMIP6_hus'
                    print "Warning: field id",cible,"expected in pingfile but not found."
                if not alias1 in pingvars: # mpmoine_note: maintenant on est toujours dans ce cas (e.g. 'CMPI6_hus7h_ple7h' plus jamais ecrit dans le ping)
                    #
                    # Construct an axis for interpolating to this dimension
                    # mpmoine_future_modif:create_xios_aux_elmts_defs: suppression de l'argument 'field_defs' de create_axis_def qui n'est pas utilise
                    # Here, only zoom or normal axis attached to svar, axis for unions of plevs are managed elsewhere
                    axis_defs[axis_key]=create_axis_def(sd,lset["ping_variables_prefix"])
                    #
                    # Construct a grid using variable's grid and new axis
                    # mpmoine_merge_dev2_v0.12: j'ai change nextvar en alias
                    # mpmoine_merge_dev2_v0.12: nouvelle une fonction 'create_grid_def' car utilisee aussi par 'create_xios_grids_for_plev_unions'
                    if not sd.is_zoom_of: # create a (target) grid for re-mapping only if vert axis is not a zoom (i.e. if normal or union)
                        grid_def=create_grid_def(sd,alias,context_index)
                        grid_id=grid_def[0]
                        grid_defs[grid_id]=grid_def[1]
		            #
                    # Construct a field def for the re-mapped variable
                    if sd.is_zoom_of: # mpmoine_note: cas variable definie grace a 2 axis_def (zoom+union)
                        field_defs[alias1]='<field id="%-25s field_ref="%-25s axis_ref="%-10s/>'\
                        %(alias1+'"',alias2+'"',sd.zoom_label+'"')
                        # mpmoine_merge_dev2_v0.12: remplacement axis_ref=sd.is_zoom_of -> grid_ref="grid_"+sd.is_zoom_of
                        field_defs[alias2]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
                        %(alias2+'"',cible+'"',"grid_"+sd.is_zoom_of+'"') 
                    else: # mpmoine_note: cas variable definie grace a seul axis_def (non zoom)
                        # mpmoine_merge_dev2_v0.12: remplacement axis_ref=sd.label -> grid_ref=grid_id
                        field_defs[alias]='<field id="%-25s field_ref="%-25s grid_ref="%-10s/>'\
                        %(alias+'"',cible+'"',grid_id+'"')                    
                #TBD what to do for singleton dimension ?
    #
    #--------------------------------------------------------------------
    # Build XIOS domain elements (stored in domain_defs)
    #--------------------------------------------------------------------
     # Analyze 'outermost' time cell_method and translate to 'operation'
    operation,detect_missing = analyze_cell_time_method(sv.cell_methods,sv.label,table)
    # Horizontal operations. Can include horiz re-gridding specification
    # Compute domain name, define it if needed
    grid_ref=None
    if ssh[0:2] == 'Y-' : #zonal mean and atm zonal mean on pressure levels
        # TBD should remap before zona mean
        grid_ref="zonal_mean"
        grid_defs[grid_ref]='<grid id="%s"/>'%grid_ref
    elif ssh[0:2] == 'S-' : #COSP sites; cas S-na, S-A, S-AH
        grid_ref="COSP_sites_grid"
        # Assume that grid COSP_sites is defined in ping_file
        #grid_defs[grid_ref]='<grid id="%s"/>'%grid_ref
    elif ssh[0:2] == 'L-' :
        grid_ref="COSP_curtain_grid"
        grid_defs[grid_ref]='<grid id="%s"/>'%grid_ref
    elif ssh == 'TR-na' or ssh == 'TRS-na' : #transects,   oce or SI
        pass
    elif ssh[0:3] == 'XY-'  : # includes 'XY-AH' : model half-levels
        if remap_domain : grid_ref=remap_domain
    elif ssh[0:3] == 'YB-'  : #basin zonal mean or section
        pass
    elif ssh      == 'na-na'  : # global means or constants
        pass 
    else :
        raise(dr2xml_error("Issue with un-managed spatial shape %s"%ssh))
    #
    #--------------------------------------------------------------------
    # Build XIOS field elements (stored in end_field_defs)
    # including their CMOR attributes
    #--------------------------------------------------------------------
    if any (sd.is_zoom_of for sd in sv.sdims.values()):
        rep='  <field field_ref="%s" name="%s" ts_enabled="true" '% \
            (alias1,sv.label)
    else:
        rep='  <field field_ref="%s" name="%s" ts_enabled="true" '% \
            (alias,sv.label)
    rep+=' operation="%s" detect_missing_value="%s" default_value="1.e+20"'% \
        ( operation,detect_missing)
    rep+=' cell_methods="%s" cell_methods_mode="overwrite"'% sv.cell_methods
    rep+='>\n'
    #
    comment=None
    # Process experiment-specific comment for the variable
    if sv.label in sset['comments'] :
        comment=sset['comments'][sv.label] 
    else: # Process lab-specific comment for the variable
        if sv.label in lset['comments'] : 
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
    # mpmoine_last_modif:create_xios_aux_elmts_defs: ajout de missing_value pour satisfaire le standard attendu par CMOR
    # mpmoine_last_modif:create_xios_aux_elmts_defs:  missing_valueS pour l'instant pour que ça passe le CMORchecker (issue)
    rep+=wrv('cell_methods',sv.cell_methods)
    rep+=wrv('cell_measures',sv.cell_measures)
    # mpmoine_note: 'missing_value(s)' normalement plus necessaire, a verifier
    #-rep+=wrv('missing_values',sv.missing,num_type="double")
    rep+='     </field>\n'
    #
    if grid_ref not in end_field_defs : end_field_defs[grid_ref]=[]
    end_field_defs[grid_ref].append(rep)

# mpmoine_last_modif:gather_AllSimpleVars: nouvelle fonction qui rassemble les operations select_CMORvars_for_lab et read_homeVars_list. 
# mpmoine_last_modif:gather_AllSimpleVars: Necessaire pour create_ping_file qui doit tenir compte des extra_Vars
def gather_AllSimpleVars(lset,expid=False,year=False,printout=False):
    mip_vars_list=select_CMORvars_for_lab(lset,expid,year,printout=printout)
    if lset['listof_home_vars']:
        process_homeVars(lset,mip_vars_list,dq,expid,printout)

    else: print "Info: No HOMEvars list provided."
    return mip_vars_list

def generate_file_defs(lset,sset,year,context,cvs_path,pingfile=None,
    dummies='include',printout=False,dirname="./",prefix="") :
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
    """
    #
    #--------------------------------------------------------------------
    # Parse XIOS setting files for the context
    #--------------------------------------------------------------------
    global context_index
    context_index=init_context(context)
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
    #--------------------------------------------------------------------
    svars_per_table=dict()
    context_realms=lset['realms_per_context'][context]
    for realm in context_realms : 
        if realm in svars_per_realm.keys():
            for svar in svars_per_realm[realm] :
                # mpmoine_last_modif:generate_file_defs: patch provisoire pour retirer les  svars qui n'ont pas de spatial_shape 
                # mpmoine_last_modif:generate_file_defs: (cas par exemple de 'hus' dans table '6hrPlev' => spid='__struct_not_found_001__')
                # mpmoine_next_modif: generate_file_defs: exclusion de certaines spatial shapes (ex. Polar Stereograpic Antarctic/Groenland)
                if svar.label not in lset['excluded_vars'] and svar.spatial_shp and svar.spatial_shp not in lset["excluded_spshapes"]:  
                    if svar.mipTable not in svars_per_table : 
                        svars_per_table[svar.mipTable]=[]
                    svars_per_table[svar.mipTable].append(svar)
                else:
                    # mpmoine_future_modif:generate_file_defs: juste un peu plus de printout...
                    if printout:
                        print "Warning: ",svar.label," in table ",svar.mipTable," has been excluded for one or several of the following reason(s):"
                        if svar.label in lset['excluded_vars']: print "   * is in excluded list"
                        if not svar.spatial_shp: print "   * has no spatial shape"
                        if svar.spatial_shp in lset["excluded_spshapes"]: print "   * has an exluded spatial shape"
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
            if svar.label not in lset['excluded_vars'] and svar.spatial_shp and svar.spatial_shp not in lset["excluded_spshapes"]:  
                if svar.mipTable not in svars_per_table :
                    svars_per_table[svar.mipTable]=[]
                svars_per_table[svar.mipTable].append(svar)
    #    
    #--------------------------------------------------------------------
    # Print Summary: list of variables per table
    #--------------------------------------------------------------------
    if printout :
        print "\nTables concerned by context %s : "%context,\
            svars_per_table.keys()
    if printout :
        print "\nVariables per table :"
    for table in svars_per_table :    
        if printout :
            print "%15s %02d ---->"%(table,len(svars_per_table[table])),
        for svar in svars_per_table[table] : 
            if printout : print svar.label,
        if printout : print
    #
    # mpmoine_zoom_modif:generate_file_defs: build axis defs of plevs unions
    #--------------------------------------------------------------------
    # Build all plev union axis and grids
    #--------------------------------------------------------------------
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
            print "Issue accessing pingfile "+pingfile
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
        field_defs=dict()
        axis_defs=dict()
        # mpmoine_merge_dev2_v0.12:generate_file_defs: initialisation de grid_defs
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
                        write_xios_file_def(svar,table,lset,sset,out,cvs_path,
                                field_defs,axis_defs,grid_defs,domain_defs,dummies,
                                skipped_vars_per_table,prefix,context,grid,pingvars)
                else :
                    pass
                    print "Duplicate var in %s : %s %s %s"%(
                        table, svar.label, `svar.temporal_shp`, \
                        `count[svar.label].temporal_shp`) 
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
        for obj in union_axis_defs.keys(): out.write("\t"+union_axis_defs[obj]+"\n")
        out.write('</axis_definition> \n')
        out.write('\n<domain_definition> \n')
        for obj in domain_defs.keys(): out.write("\t"+domain_defs[obj]+"\n")
        out.write('</domain_definition> \n')
        # mpmoine_merge_dev2_v0.12:generate_file_defs: ecriture des grid_defs
        out.write('\n<grid_definition> \n')
        for obj in grid_defs.keys(): out.write("\t"+grid_defs[obj]+"\n")
        # mpmoine_merge_dev2_v0.12:generate_file_defs: on ecrit maintenant les grid defs pour les unions
        for obj in union_grid_defs.keys(): out.write("\t"+union_grid_defs[obj]+"\n")
        out.write('</grid_definition> \n')
        out.write('</context> \n')
    if printout :
        print "\nfile_def written as %s"%filename
    # mpmoine_skipped_modif:generate_file_defs: plus d'info sur les skipped_vars
    if skipped_vars_per_table: 
        print "\nSkipped variables (i.e. whose alias is not present in the pingfile):"
        for table,skipvars in skipped_vars_per_table.items():
            print "\n%15s %02d/%02d ---->"%(table,len(skipvars),len(svars_per_table[table])),
            #-print "\n\t",table ," ",len(skipvars),"--->",
            for skv in skipvars: print skv,

# mpmoine_future_modif:create_axis_def: suppression de l'argument 'field_defs' qui n'est pas utilise
# mpmoine_future_modif:create_axis_def: suppression de l'argument 'field_defs' qui n'est pas utilise
def create_axis_def(sdim,prefix):
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
            # mpmoine_future_modif: je supprime le -1 pour n_glo car regle avec rstrip/split()
            rep+='value="(0,%g) [%s]"'%(n_glo,sdim.requested)
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
        rep+='\n\t<interpolate_axis type="polynomial" order="1"'
        rep+=' coordinate="%s"/>\n\t</axis>'%coordname
        return rep
    # mpmoine_zoom_modif:create_axis_def: traitement du cas zoom
    else:
        # Axis is subset of another, write it as a zoom_axis
        rep='<axis id="%s"'%sdim.zoom_label
        rep+=' axis_ref="%s">\n'%sdim.is_zoom_of
        rep+='\t<zoom_axis begin="%g" n="%g"/>\n'%(glo_list_num[-1],n_glo)
        rep+='\t</axis>'
        return rep

# mpmoine_merge_dev2_v0.12: nouvelle fonction create_grid_def
def create_grid_def(sd,alias=None,context_index=None):
    if not sd.is_zoom_of: # no grid_def to build in zoom case
        if not sd.is_union_for: # a grid_def to build in classical case (a vertical axis without using union)
            if alias and context_index:
                src_grid=id2grid(alias,context_index)
                src_grid_id=src_grid.attrib ['id']
                src_grid_string=ET.tostring(src_grid)
                target_grid_id=src_grid_id+"_"+sd.label
                target_grid_string=re.sub('axis_ref= *.([\w_])*.','axis_ref="%s"'%sd.label,src_grid_string)
                target_grid_string=re.sub('grid id= *.([\w_])*.','grid id="%s"'%target_grid_id,target_grid_string)
                return (target_grid_id,target_grid_string)
            else:
                print "Error: ask for creating a grid_def from a native grid \
                but variable alias and/or context_index not provided."
                return False
        else: # a grid_def to build in union case
            grid_id="grid_"+sd.label
            grid_string='<grid id="%s">'%grid_id
            grid_string+='\n\t<domain domain_ref="%s"/>'%"domain_atm" # mpmoine_note: attention, en dur !
            grid_string+='\n\t<axis axis_ref="%s"/>'%sd.label
            grid_string+='\n\t</grid>'
            return (grid_id,grid_string)
    else:
        print "Warning: calling create_grid_def for a zoom axis, this is unexpected => no grid_def created"
        return False

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
                                #-print sv.label,"in table",sv.mipTable,"already listed for",sd.label
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
                    # mpmoine_note: on reecrase les attributs de sdim_union à chaque nouveau plev. Pas utile mais
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
        grid_def=create_grid_def(sdim_union)
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
    test=(sdim.stdname=='air_pressure' or sdim.stdname=='altitude')
    return test

def analyze_cell_time_method(cm,label,table):
    """
    Depending on cell method string CM, tells which time operation
    should be done, and if missing value detection should be set
    """
    operation=None
    detect_missing=False
    if cm is None : 
        if print_DR_errors :
            print "DR Error: cell_time_method is None for %15s in table %s, averaging" %(label,table)
        operation="average"
    elif "time: mean (with samples weighted by snow mass)" in cm : 
        #[amnla-tmnsn]: Snow Mass Weighted (LImon : agesnow, tsnLi)
        print "TBD Cannot yet handle time: mean (with samples weighted by snow mass)"
    elif "time: mean where cloud"  in cm : 
        #[amncl-twm]: Weighted Time Mean on Cloud (2 variables ISSCP 
        # albisccp et pctisccp, en emDay et emMon)
        print "Note : assuming that 'time: mean where cloud' "+\
            " for %15s in table %s is well handled by 'detect_missing'"\
            %(label,table)
        operation="average"
        detect_missing=True
    elif "time: mean where sea"  in cm :#[amnesi-tmn]: 
        #Area Mean of Ext. Prop. on Sea Ice : pas utilisee
        print "time: mean where sea is not supposed to be used (%s,%s)"%(label,table)
    elif "time: mean where sea_ice" in cm :
        #[amnsi-twm]: Weighted Time Mean on Sea-ice (presque que des 
        #variables en SImon, sauf sispeed et sithick en SIday)
        detect_missing=True
    elif "time: minimum" in cm :    
        #[tmin]: Temporal Minimum : utilisee seulement dans table daily
        operation="minimum"
    elif "time: maximum" in cm :   
        #[tmax]: Time Maximum  : utilisee seulement dans table daily
        operation="maximum"
    elif "time: maximum within days time: mean over days" in cm :
        #[dmax]: Daily Maximum : tasmax Amon seulement
        if label != 'tasmax' : 
            print "Error: issue with variable %s in table %s "%(label,table)+\
                "and cell method time: maximum within days time: mean over days"
        operation="average"
    elif "time: minimum within days time: mean over days" in cm :
        #[dmin]: Daily Minimum : tasmin Amon seulement
        if label != 'tasmin' : 
            print "Error: issue with variable %s in table %s  "%(label,table)+\
                "and cell method time: minimum within days time: mean over days"
        operation="average"
    elif "time: mean within years time: mean over years" in cm: 
        #[aclim]: Annual Climatology
        print "TBD Cannot yet compute annual climatology for "+\
            "%15s in table %s -> averaging"%(label,table)
        # Could transform in monthly fields to be post-processed
        operation="average"
    elif "time: mean within days time: mean over days"  in cm: 
        #[amn-tdnl]: Mean Diurnal Cycle
        print "TBD Cannot yet compute diurnal cycle for "+\
        " %15s in table %s -> averaging"%(label,table)
        # Could output a time average of 24 hourly fields at 01 UTC, 2UTC ...
        operation="average"
    elif "time: sum"  in cm :
        # [tsum]: Temporal Sum  : pas utilisee !
        print "Error: time: sum is not supposed to be used" 
    elif "time: mean" in cm :  #    [tmean]: Time Mean  
        operation="average"
    elif "time: point" in cm:
        operation="instant"
    else :
        print "Error: issue when analyzing cell_time_method "+\
            "%s for %15s in table %s, averaging" %(cm,label,table)
    return (operation, detect_missing)

    #

def pingFileForRealmsList(context,lrealms,svars,dummy="field_atm",
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
            if any([ v.modeling_realm in r or r in v.modeling_realm
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
    specials=read_special_fields_defs(lrealms)
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
            # mpmoine_future_modif:pingFileForRealmsList: on s'appuie sur le 'label_without_psuffix' et non plus le label complet
            label=v.label_without_psuffix
            if label in specials :
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
        for obj in [ "axis", "domain", "grid" ] :
            #print "for obj "+obj
            copy_obj_from_DX_file(fp,obj,prefix,lrealms)
        fp.write('</context>\n')

def copy_obj_from_DX_file(fp,obj,prefix,lrealms) :
    # Insert content of DX_<obj>_defs files (changing prefix)
    #print "copying %s defs :"%obj,
    subrealms_seen=[]
    for realm in lrealms :
        for subrealm in realm.split() :
            if subrealm in subrealms_seen : continue
            subrealms_seen.append(subrealm)
            #print "\tand realm %s"%subrealm, 
            defs=DX_defs_filename(obj,subrealm)
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

def DX_defs_filename(obj,realm):
    #-return prog_path+"/inputs/DX_%s_defs_%s.xml"%(obj,realm)
    return "./inputs/DX_%s_defs_%s.xml"%(obj,realm)

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

def read_special_fields_defs(realms,printout=False) :
    special=dict()
    subrealms_seen=[]
    for realm in realms  :
        for subrealm in realm.split() :
            if subrealm in subrealms_seen : continue
            subrealms_seen.append(subrealm)
            d=read_xml_elmt_or_attrib(DX_defs_filename("field",subrealm),\
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
    # mpmoine_last_modif:highest_rank: pour recuperer le label_without_area
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
                    if print_DR_errors :
                        # mpmoine_last_modif:highest_rank:  pour corriger l'erreur "TypeError: cannot concatenate 'str' and 'dreqItem_CoreAttributes' objects"
                        print "DR Error: issue with stid or spid for "+\
                        st.label+" "+v.label+string(cvar.mipTable)
                    # One known case in DR 1.0.2: hus in 6hPlev
                    shape="XY"
            except :
                # mpmoine_last_modif:highest_rank:  pour corriger l'erreur "TypeError: cannot concatenate 'str' and 'dreqItem_CoreAttributes' objects"
                print "DR Error: issue with stid for "+v.label+string(cvar.mipTableSection)
                shape="?st"
        else:
            # mpmoine_last_modif:highest_rank: Pour recuperer le spatial_shp pour le cas de variables qui n'ont pas un label CMORvar de la DR (ex. HOMEvar ou EXTRAvar)
            shape=svar.spatial_shp
        # mpmoine_future_modif:highest_rank: test shape =/ None, sinon on se retrouve avec shapes=liste de None et 1 liste de None n'est pas Faux
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
    source=sources[source_id] 
    rep=source_id+"("+source['year']+")"+\
         ": atmosphere: "+source["atmosphere"]+\
         "; ocean: " + source["ocean"]+\
         "; sea_ice: "+source["sea_ice"]+\
         "; land: "+source["land"]+\
         "; aerosol: "+source["aerosol"]+\
         "; atmospheric_chemistry: "+source["atmospheric_chemistry"]+\
         "; ocean_biogeochemistry: "+source["ocean_biogeochemistry"]+";"
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
    

