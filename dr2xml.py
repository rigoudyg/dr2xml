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

from datetime import datetime
import json
import collections
import sys,os
import xml.etree.ElementTree as ET
import posixpath
prog_path = posixpath.dirname(__file__)

# Local packages
from vars import simple_CMORvar, process_homeVars, complement_svar_using_cmorvar
from grids import decide_for_grids, grid2resol, grid2desc, field_size,\
    split_frequency_for_variable, timesteps_per_freq_and_duration, dr2xml_error
from Xparse import init_context, id2grid

# A local auxilliary table
# mpmoine_last_modif: dr2xml.py: ajout import de cmipFreq2xiosFreq
from table2freq import table2freq, table2splitfreq, cmipFreq2xiosFreq

print_DR_errors=False

dq = dreq.loadDreq()
print dq.version

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
    "sub_experiment_id"    : "none", # Optional, default is 'none'; example : s1960. 
    "sub_experiment"       : "none", # Optional, default in 'none'
    "history"              : "no_history", #Used when a simulation is re-run, an output file is modified ...
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
    Returns True if requestItem 'ri' in data request 'dq' is relevant for a 
    given 'experiment' and 'year'. Toggle 'debug' allow some printouts 
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

def select_CMORvars_for_lab(lset, experiment_id=None, year=None,
                            printout=False):
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
        print 'Number of CMOR variables for these requestLinks is :%s'%len(miprl_vars_grids)
    # 
    filtered_vars=[]
    for (v,g) in miprl_vars_grids : 
        cmvar=dq.inx.uid[v]
        mipvar=dq.inx.uid[cmvar.vid]
        if mipvar.label not in lset['excluded_vars'] : 
            filtered_vars.append((v,g))
    if printout :
        print 'Number of CMOR variables once filtered by excluded vars is : %s'%len(filtered_vars)
    #
    # Print a count of distinct var labels
    if printout :
        varlabels=set()
        for (v,g) in filtered_vars : varlabels.add(dq.inx.uid[v].label)
        print '\nNumber of variables with distinct labels is :',len(varlabels)

    # Translate CMORvars to a list of simplified CMORvar objects
    simplified_vars = []
    for (v,grid) in filtered_vars :
        svar = simple_CMORvar()
        cmvar = dq.inx.uid[v]
        complement_svar_using_cmorvar(svar,cmvar,dq)
        svar.Priority=analyze_priority(cmvar,lset['mips'])
        svar.grids=decide_for_grids(svar,grid,lset)
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
                     


def write_xios_file_def(cmv,table, lset,sset, out,cvspath,field_defs,axis_defs,
                        domain_defs,dummies,skipped_vars,
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
            if not alias in pingvars :
                skipped_vars.append(cmv.label)
                return
    #
    source_id=lset['source_id']
    experiment_id=sset['experiment_id']
    # Variant matters
    realization_index=sset.get('realization_index',1) 
    initialization_index=sset.get('initialization_index',1)
    physics_index=sset.get('physics_index',1)
    forcing_index=sset.get('forcing_index',1)
    variant_label="r%di%dp%df%d"%(realization_index,initialization_index,\
                                  physics_index,forcing_index)
    #
    # WIP doc v 6.2.0 - dec 2016 
    # <variable_id>_<table_id>_<source_id>_<experiment_id >_<member_id>_<grid_label>[_<time_range>].nc
    member_id=variant_label
    sub_experiment_id=sset.get('sub_experiment_id','none')
    if sub_experiment_id != 'none': member_id = sub_experiment_id+"-"+member_id
    #
    # Grid - 
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
    filename="%s%s_%s_%s_%s_%s_%s_%s"%\
               (prefix,cmv.label,table,source_id,experiment_id,
                member_id,grid_label,time_range)
    # WIP Draft 14 july 2016
    activity_id=sset.get('activity_id','CMIP')
    # mpmoine_last_modif:write_xios_file_def: Maintenant, dans le cas type='perso', table='NONE'. On ne doit donc pas compter sur le table2freq pour recuperer
    # mpmoine_last_modif:write_xios_file_def: la frequence en convention xios => fonction cmipFreq2xiosFreq
    split_freq=split_frequency_for_variable(cmv, lset, sc.mcfg)
    #        
    end_field_defs=dict()
    create_xios_field_ref(cmv,alias,table,lset,sset,end_field_defs,
        field_defs,axis_defs, domain_defs,dummies,context,remap_domain,pingvars)
    if len(end_field_defs.keys())==0 :
        # TBD : restore error_message
        #raise dr2xml_error("No field ref for %s in %s"%(cmv.label,table))
        return
    #

    out.write(' <file name="%s" output_freq="%s" '% (filename,cmipFreq2xiosFreq[cmv.frequency]))
    out.write('  append="true" split_freq="%s" '%split_freq)
    #out.write('timeseries="exclusive" >\n')
    out.write(' time_units="days" time_counter_name="time"')
    out.write(' time_stamp_name="creation_date" ')
    out.write(' time_stamp_format="%Y-%m-%dT%H:%M:%SZ"')
    out.write(' uuid_name="tracking_id" uuid_format="hdl:21.14100/%uuid%"')
    out.write(' >\n')
    #
    #
    # mpmoine_last_modif:write_xios_file_def: ajout de l'argument num_type à la fonction wr
    def wr(key,dic_or_val=None,num_type="string",default=None) :
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

    wr('project_id', sset.get('project',"CMIP6")+"/"+activity_id)
    wr('activity_id',activity_id)
    contact=sset.get('contact',lset.get('contact',None))
    if contact and contact is not "" : wr('contact',contact) 
    conventions="CF-1.7 CMIP-6.0" ;     wr('Conventions',conventions) 
    # TBC : assume data_specs_version == dq.version
    wr('data_specs_version',dq.version) 
    #
    with open(cvspath+"CMIP6_experiment_id.json","r") as json_fp :
        CMIP6_experiments=json.loads(json_fp.read())['experiment_id']
        try:
            exp_entry=CMIP6_experiments[sset['experiment_id']]
            experiment=exp_entry['experiment']
        except :
            # mpmoine_last_modif:write_xios_file_def: provisoire, laisser passer cette erreur tant que le
            # mpmoine_last_modif:write_xios_file_def: CV_CMIP6 et celui de la DR ne sont pas concordants
            dr2xml_error("Issue getting experiment description for %20s"\
                               %sset['experiment_id'])
            experiment="NOT-SET"
    wr('experiment',experiment)
    wr('experiment_id',experiment_id)
    # 
    # TBD: check external_variables
    # Let us yet hope that all tables but those with an 'O'
    # as first letter require areacella, and the others require areacello
    external_variables= "areacella" 
    if table[0]=='O' or table[0:1]=='SI' : external_variables= "areacello" 
    if 'fx' in table : external_variables= "" 
    wr('external_variables',external_variables)
    #
    wr('forcing_index',forcing_index) 
    # mpmoine_last_modif: Maintenant, dans le cas type='perso', table='NONE'. On ne doit donc pas compter sur table2freq pour recuperer la frequence
    wr('frequency',cmv.frequency)
    #
    # URL
    # mpmoine_last_modif:write_xios_file_def: mip_era n'est plus toujours 'CMIP6'
    mip_era=cmv.mip_era
    institution_id=lset['institution_id']
    source_id=lset['source_id']
    sub_experiment_id=sset.get('sub_experiment_id','none')
    further_info_url="http://furtherinfo.es-doc.org/%s.%s.%s.%s.%s.%s"%(
        mip_era,institution_id,source_id,experiment_id,
        sub_experiment_id,variant_label)
    wr('further_info_url',further_info_url)
    #
    wr('grid',grid_description) ; wr('grid_label',grid_label) ;
    wr('nominal_resolution',grid_resolution)    
    wr('history',sset,'none') 
    wr("initialization_index",initialization_index)
    wr("institution_id",institution_id)
    if "institution" in lset :
        inst=lset['institution']
    else:
        with open(cvspath+"CMIP6_institution_id.json","r") as json_fp :
            try:
                inst=json.loads(json_fp.read())['institution_id'][institution_id]
            except :
                raise(dr2xml_error("Institution_id for %s not found "+\
                        "in CMIP6_CV at %s"%(institution,cvspath)))
    wr("institution",inst)
    #
    with open(cvspath+"CMIP6_license.json","r") as json_fp :
        license=json.loads(json_fp.read())['license'][0]
    license=license.replace("<Your Centre Name>",inst)
    license=license.replace("<some URL maintained by modeling group>",
                            lset["info_url"])
    wr("license",license)
    wr('mip_era',mip_era)
    parent_experiment_id=sset.get('parent_experiment_id',None)
    if parent_experiment_id and parent_experiment_id != 'no_parent'\
        and parent_experiment_id != 'no parent' :
        parent_activity_id=sset.get('parent_activity_id','CMIP')
        wr('parent_activity_id',parent_activity_id)
        wr("parent_experiment_id",sset); 
        parent_mip_era=sset.get('parent_mip_era',"CMIP6") ; 
        if parent_mip_era=="" : parent_mip_era="CMIP6"
        wr('parent_mip_era',parent_mip_era) 
        parent_source_id=sset.get('parent_source_id',source_id) ; 
        wr('parent_source_id',parent_source_id)
        # TBX : syntaxe XIOS pour designer le time units de la simu courante
        parent_time_ref_year=sset.get('parent_time_ref_year',"1850") 
        parent_time_units="days since %s-01-01 00:00:00"%parent_time_ref_year
        wr("parent_time_units",parent_time_units)
        parent_variant_label=sset.get('parent_variant_label',variant_label) 
        wr('parent_variant_label',parent_variant_label)
        wr('branch_method',sset,'standard')
        wr('branch_time_in_child',sset)
        wr('branch_time_in_parent',sset) 
    wr("physics_index",physics_index) 
    wr('product','output')
    wr("realization_index",realization_index) 
    wr('realm',cmv.modeling_realm)
    wr('references',lset) 
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
    wr('source',source) 
    wr('source_id',source_id)
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
    wr('source_type',source_type)
    #
    wr('sub_experiment_id',sub_experiment_id) 
    wr('sub_experiment',sset,'none') 
    wr("table_id",table)
    wr("title","%s model output prepared for %s / %s %s"%(\
        source_id,sset.get('project',"CMIP6"),activity_id,experiment_id))
    wr("variable_id",cmv.label)
    wr("variant_info",sset,"")
    wr("variant_label",variant_label)
    #
    # Create a field group for each shape
    for shape in end_field_defs :
        dom="" ;
        if shape : dom='domain_ref="%s"'%shape
        out.write('<field_group %s expr="@this" >\n'%dom)
        for entry in end_field_defs[shape] : out.write(entry)
        out.write('</field_group >\n')
    out.write('</file>\n\n')

def create_xios_field_ref(sv,alias,table,lset,sset,end_field_defs,
     field_defs,axis_defs,domain_defs,dummies,context,remap_domain,pingvars) :
    """
    Create a field_ref for a simplified variable object sv (with
    lab prefix for the variable name) and store it in end_field_defs
    under a key=shape
    
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
    nextvar=alias 
    #
    # Proceed with vertical interpolation if needed
    ssh=sv.spatial_shp
    prefix=lset["ping_variables_prefix"]
    # TBD Should handle singletons here
    # TBD Should ensure that various additionnal dims are duly documented by model or pingfile (e.g. tau)
    if ssh[0:4] in ['XY-H','XY-P'] or ssh[0:3] == 'Y-P' :
        # TBD : for now, do not interpolate vertically
        return
        dimids=dq.inx.uid[sv.struct.spid].dimids
        for dimid in dimids :
            d=dq.inx.uid[dimid]
            if isVertDim(d) :
                furthervar=nextvar+"_"+d.label
                if not furthervar in pingvars :
                    # Construct an axis for interpolating to this dimension
                    axis_defs[d.label]=create_axis_def(d,lset["ping_variables_prefix"],field_defs)
                    # Construct a field def for the interpolated variable
                    field_defs[furthervar]='<field id="%-25s field_ref="%-25s axis_ref="%-10s/>'\
                        %(furthervar+'"',nextvar+'"',d.label+'"')
                    #%(furthervar+'"',nextvar+'"',prefix+d.label+'"')
                nextvar=furthervar
                #TBD what to do for singleton dimension ?
     # Analyze 'outermost' time cell_method and translate to 'operation'
    operation,detect_missing = analyze_cell_time_method(
        sv.cell_methods,sv.label,table)
    # Horizontal operations. Can include horiz re-gridding specification
    # Compute domain name, define it if needed
    domain_ref=None
    if ssh[0:2] == 'Y-' : #zonal mean and atm zonal mean on pressure levels
        # TBD should remap before zona mean
        domain_ref="zonal_mean"
        domain_defs[domain_ref]='<domain id="%s"/>'%domain_ref
    elif ssh[0:2] == 'S-' : #COSP sites; cas S-na, S-A, S-AH
        domain_ref="COSP_sites"
        domain_defs[domain_ref]='<domain id="%s"/>'%domain_ref
    elif ssh[0:2] == 'L-' :
        domain_ref="COSP_curtain"
        domain_defs[domain_ref]='<domain id="%s"/>'%domain_ref
    elif ssh == 'TR-na' or ssh == 'TRS-na' : #transects,   oce or SI
        pass
    elif ssh[0:3] == 'XY-'  : # includes 'XY-AH' : model half-levels
        if remap_domain : domain_ref=remap_domain
    elif ssh[0:3] == 'YB-'  : #basin zonal mean or section
        pass
    elif ssh      == 'na-na'  : # global means or constants
        pass 
    else :
        raise(dr2xml_error("Issue with un-managed spatial shape %s"%ssh))
    #
    rep='  <field field_ref="%s" name="%s" ts_enabled="true" '% \
        ( nextvar,sv.label)
    rep+=' operation="%s" detect_missing_value="%s" default_value="1.e+20"'% \
        ( operation,detect_missing)
    rep+=' cell_methods="%s" cell_methods_mode="overwrite"'% sv.cell_methods
    rep+='>\n'
    #
    #
    # mpmoine_last_modif:wrv: ajout de l'argument num_type
    def wrv(name, value, num_type="string"):
        # Format a 'variable' entry
        return '     <variable name="%s" type="string" > %s '%(name,value)+\
            '</variable>\n'
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
    # mpmoine_last_modif: ajout de missing_value pour satisfaire le standard attendu par CMOR
    # mpmoine_last_modif: missing_valueS pour l'instant pour que ça passe le CMORchecker (issue)
    rep+=wrv('missing_values',sv.missing,num_type="double")
    rep+=wrv('cell_measures',sv.cell_measures)
    rep+='     </field>\n'
    #
    shape=domain_ref
    #shape=sv.spatial_shp
    if shape not in end_field_defs : end_field_defs[shape]=[]
    end_field_defs[shape].append(rep)

# mpmoine_last_modif:gather_AllSimpleVars: nouvelle fonction qui rassemble les operations select_CMORvars_for_lab et read_homeVars_list. 
# mpmoine_last_modif:gather_AllSimpleVars: Necessaire pour create_ping_file qui doit tenir compte des extra_Vars
def gather_AllSimpleVars(lset,expid=False,year=False,printout=False):
    mip_vars_list=select_CMORvars_for_lab(lset,expid,year,printout=printout)
    if lset['listof_home_vars']:
        home_vars_list=process_homeVars(lset,mip_vars_list,dq,expid,printout)
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
    # Parse XIOS setting files for the context
    #global xcontext
    #xcontext=init_context(context)
    # Extract CMOR variables for the experiment and year and lab settings
    skipped_vars=[]
    mip_vars_list=gather_AllSimpleVars(lset,sset['experiment_id'],year,printout)
    # Group CMOR vars per realm
    svars_per_realm=dict()
    for svar in mip_vars_list :
        if svar.modeling_realm not in svars_per_realm.keys() :
            svars_per_realm[svar.modeling_realm]=[]
        svars_per_realm[svar.modeling_realm].append(svar)
    if printout :
        print "\nRealms for these CMORvars :",svars_per_realm.keys()
    #
    # Select on context realms, grouping by table
    svars_pertable=dict()
    context_realms=lset['realms_per_context'][context]
    for realm in context_realms : 
        if realm in svars_per_realm.keys():
            for svar in svars_per_realm[realm] :
                # mpmoine_last_modif:generate_file_defs: patch provisoire pour retirer les  svars qui n'ont pas de spatial_shape 
                # mpmoine_last_modif:generate_file_defs: (cas par exemple de 'hus' dans table '6hrPlev' => spid='__struct_not_found_001__')
                if svar.label not in lset['excluded_vars'] and svar.spatial_shp: 
                #-if svar.label not in lset['excluded_vars'] :
                    if svar.mipTable not in svars_pertable : 
                        svars_pertable[svar.mipTable]=[]
                    svars_pertable[svar.mipTable].append(svar)
    #
    # Add svarars belonging to the orphan list
    orphans=lset['orphan_variables'][context]
    for svar in mip_vars_list :
        if svar.label in orphans:
            # mpmoine_last_modif:generate_file_defs: patch provisoire pour retirer les  svars qui n'ont pas de spatial_shape 
            # mpmoine_last_modif:generate_file_defs: (cas par exemple de 'hus' dans table '6hrPlev' => spid='__struct_not_found_001__')
            if svar.label not in lset['excluded_vars'] and svar.spatial_shp: 
            #-if svar.label not in lset['excluded_vars'] : 
                if svar.mipTable not in svars_pertable :
                    svars_pertable[svar.mipTable]=[]
                svars_pertable[svar.mipTable].append(svar)
    #    
    if printout :
        print "\nTables concerned by context %s : "%context,\
            svars_pertable.keys()
    if printout :
        print "\nVariables per table :"
    for table in svars_pertable :    
        if printout :
            print "%15s %02d ---->"%(table,len(svars_pertable[table])),
        for svar in svars_pertable[table] : 
            if printout : print svar.label,
        if printout : print
    #
    # read ping_file defined variables
    pingvars=[] 
    if pingfile :
        ping_refs=read_defs(pingfile, tag='field', attrib='field_ref')
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
    # Write XIOS file_def
    #filename=dirname+"filedefs_%s.xml"%context
    filename=dirname+"dr2xml_%s.xml"%context
    with open(filename,"w") as out :
        out.write('<context id="%s"> \n'%context)
        field_defs=dict()
        axis_defs=dict()
        domain_defs=dict()
        #for table in ['day'] :    
        out.write('\n<file_definition type="one_file" enabled="true" > \n')
        for table in svars_pertable :
            count=dict()
            for svar in svars_pertable[table] :
                if svar.label not in count :
                    count[svar.label]=svar
                    for grid in svar.grids :
                        write_xios_file_def(svar,table, lset,sset,out,cvs_path,
                                field_defs,axis_defs,domain_defs,dummies,
                                skipped_vars,prefix,context,grid,pingvars)
                else :
                    pass
                    print "Duplicate var in %s : %s %s %s"%(
                        table, svar.label, `svar.temporal_shp`, \
                        `count[svar.label].temporal_shp`) 
        out.write('\n</file_definition> \n')
        # Write all domain, axis, field defs needed for these file_defs
        out.write('<field_definition> \n')
        for obj in field_defs: out.write("\t"+field_defs[obj]+"\n")
        out.write('\n</field_definition> \n')
        out.write('\n<axis_definition> \n')
        for obj in axis_defs: out.write("\t"+axis_defs[obj]+"\n")
        out.write('</axis_definition> \n')
        out.write('\n<domain_definition> \n')
        for obj in domain_defs: out.write("\t"+domain_defs[obj]+"\n")
        out.write('</domain_definition> \n')
        out.write('</context> \n')
    if printout :
        print "\nfile_def written as %s"%filename
    if skipped_vars : print "Skipped variables are "+`skipped_vars`



def create_axis_def(dim_name_or_obj,prefix,field_defs):
    """ 
    From a dim DR object or a dim name, returns an Xios axis definition 
    """
    dim=None
    if type(dim_name_or_obj)==type(""):
        for g in dq.coll['grids'].items : 
            if g.label==dim_name_or_obj : dim=g
    else: dim=dim_name_or_obj
    if dim is None :
        print "cannot cretae an axis_def from "+dim_name_or_obj
        return None
    rep='<axis id="%s" '%dim.label
    if not dim.positive in [ None, "" ] :
        rep+='positive="%s" '%dim.positive
    if dim.requested != "" :
        # Case of a non-degenerated dimension (not a singleton)
        n_glo=len(dim.requested.split(" "))
        rep+='n_glo="%g" '%n_glo
        rep+='value="(0,%g) [%s]"'%(n_glo - 1,dim.requested)
    elif dim.value != "":
        # Singleton case
        rep+='n_glo=%g '%1
        rep+='value=(0,0)[%s]"'%dim.value
    else :
        pass
    stdname=dq.inx.uid[dim.standardName].uid
    rep+=' name="%s"'%dim.altLabel
    rep+=' standard_name="%s"'%stdname
    rep+=' long_name="%s"'%dim.title
    rep+=' unit="%s"'%dim.units
    rep+='>'
    if stdname=="air_pressure" : coordname=prefix+"pfull"
    if stdname=="altitude"     : coordname=prefix+"zg"
    rep+='\n\t\t<interpolate_axis type="polynomial" order="1"'
    rep+=' coordinate="%s"/>\n\t</axis>'%coordname
    return rep

def isVertDim(dim):
    """
    Returns True if dim represents a dimension for which we want 
    an Xios interpolation. 
    For now, a very simple logics for interpolated vertical 
    dimension identification:
    """
    name=dq.inx.uid[dim.standardName]
    return  (name.uid=='air_pressure' or name.uid=='altitude')
    
def analyze_cell_time_method(cm,label,table):
    """
    Depending on cell method string CM, tells which time operation
    should be done, and if missing value detection should be set
    """
    operation=None
    detect_missing=False
    if cm is None : 
        if print_DR_errors :
            print "DR Error : cell_time_method is None for %15s in table %s, averaging" %(label,table)
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
        print "time: mean where sea is not supposed to be used" 
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
        print "Errror: time: sum is not supposed to be used" 
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
    variable realm must be included in (or include) of the realm list
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
    lvars.sort(key=lambda x:x.label)
    # Remove duplicates
    uniques=[] ; last_label=""
    for v in lvars : 
        if v.label != last_label : 
            uniques.append(v)
            last_label=v.label
    lvars=uniques
    #
    if filename is None : filename="ping"+name+".xml"
    if filename[-4:] != ".xml" : filneme +=".xml"
    #
    specials=read_special_fields_defs(lrealms)
    with open(filename,"w") as fp:
        fp.write('<context id="%s">\n'%context)
        fp.write("<field_definition>\n")
        if exact : 
            fp.write("<!-- for variables which realm intersects any of "\
                     +name+"-->\n")
        else:
            fp.write("<!-- for variables which realm equals one of "\
                     +name+"-->\n")
        for v in lvars :
            label=v.label
            if label in specials :
                line=ET.tostring(specials[label]).replace("DX_",prefix)
                line=line.replace("\n","").replace("\t","")
                fp.write('   '); fp.write(line)
            else:
                fp.write('   <field id="%-20s'%(prefix+label+'"')+\
                         ' field_ref="')
                if dummy : 
                     # mpmoine_last_modif: svar en argument de highest_rank et non pas seulement son label_without_area
                    shape=highest_rank(v)
                    # Bugfix for DR 1.0.1 content :
                    if v.label=='clcalipso' : shape='XYA'
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
                #print " no file  "

def DX_defs_filename(obj,realm):
    return prog_path+"inputs/DX_%s_defs_%s.xml"%(obj,realm)

def read_defs(filename, tag='field', attrib=None, printout=False) :
    """ 
    Returns a dict of obejcts tagged TAG in FILENAME, which 
    - keys are ids
    - values are corresponding ET elements if 
      attrib is None, otherwise elt attribute ATTRIB
    Returns None if filename does not exist
    """
    #
    def field_defs(elt, tag='field', groups=['context', 'field_group',
        'field_definition', 'axis_definition','axis', 'domain_definition',
        'domain', 'grid_definition', 'grid' , 'interpolate_axis'  ]) :
        """ 
        Returns a list of elements in tree ELT 
        which have tag TAG, by digging in sub-elements 
        named as in GROUPS 
        """
        if elt.tag in groups :
            rep=[]
            for child in elt : rep.extend(field_defs(child,tag))
            return rep
        elif elt.tag==tag : return [elt]
        else :
            #print 'Syntax error : tag %s not allowed'%elt.tag
            # Case of an unkown tag : don't dig in
            return []
    #    
    rep=dict()
    if printout : print "processing file %s :"%filename,
    if os.path.exists(filename) :
        if printout : print "OK"%filename
        root = ET.parse(filename).getroot()
        defs=field_defs(root,tag) 
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
            d=read_defs(DX_defs_filename("field",subrealm),\
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
            shapes=[]
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
        shapes.append(shape)
    if not shapes : shape="??"
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
    elif any([ "S-na" in s for s in shapes]) :  shape="COSPprofile"
    elif any([ "na-na" in s for s in shapes]) : shape="0d" # analyser realm
    else : shape="??"

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


    

