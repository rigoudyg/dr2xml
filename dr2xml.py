"""
In the context of Climate Model Intercomparison Projects (CMIP) :

A few functions for processing 
  - a CMIP Data request and 
  - a set of settings related to a laboratory, and a model 
  - a set of settings related to an experiment, 
to a set of xml-syntax files used by XIOS for outputing fields 

Version 0.8 : S.Senesi - 2016/09/07

"""


from datetime import datetime
import json
from uuid import uuid4
import sys

# Next package retrieved using
#    svn co http://proj.badc.rl.ac.uk/svn/exarch/CMIP6dreq/tags/01.beta.34
# (and must include 01.beta.34/dreqPy in PYTHONPATH)
from scope import dreqQuery
#mpmoine_modif# en definissant dq ici et non dans le Notebook on evite le passage de dq par argument
from dreqPy import dreq
dq = dreq.loadDreq()
print dq.version

# Where is the local copy of CMIP6 Controled vocabulary (available from 
# https://github.com/WCRP-CMIP/CMIP6_CVs
#mpmoine# Depend de l utilisateur -> Pas de valeur par defaut
#cvspath="/cnrm/aster/data3/aster/senesi/public/CMIP6/data_request/CMIP6_CVs/"

# A local auxilliary table
from table2freq import table2freq


""" An example/template  of settings for a lab and a model"""
lab_and_model_settings={
    'institution_id': "CNRM",
    # TBD : institution should be read in CMIP6_CV, once updated
    'institution'   : "Centre National de Recherches Meteorologiques", 
    'model_id'      : "CNRM-CM6", 
    'model'         : "CNRM CM6",#Should be read in CMIP6_CV, form model_id (once updated)
    'source_type'   : 'AOGCM', # This should be udpated at the simulation dict level 
    'references'    :  "A character string containing a list of published or web-based "+\
        "references that describe the data or the methods used to produce it."+\
        "Typically, the user should provide references describing the model"+\
        "formulation here",
    'info_url'      : "http://www.cnrm-game-meteo.fr/cmip6/",
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

    # We account for a list of variables which the lab does not want to produce , 
    # oragnized by realms
    # excluded_vars_file="../../cnrm/non_published_variables"
    "excluded_vars":[],

    # We account for a list of variables which the lab want absolutely to produce
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
        }
    }


""" An example/template of settings for a simulation """

simulation_settings={    
    # Dictionnary describing the necessary attributes for a given simulation

    # Warning : some lines are commented out in this example but should be 
    # un-commented in some cases. See comments

    "experiment_id"  : "historical",
    #"contact"        : "", set it only if it is specific to the simualtion
    #"project"        : "CMIP6",  #CMIP6 is the default

    #'source_type'    : "ESM" # If source_type is special only for this experiment (e.g. : AMIP)
                      #(i.e. not the same as in lan_and_model settings), you may tell that here

    # MIP specifying the experiment. For historical, it is CMIP6
    # itself In a few cases it may be appropriate to include multiple
    # activities in the activity_id (with multiple activities allowed,
    # separated by single spaces).  An example of this is 'LUMIP
    # AerChemMIP' for one of the land-use change experiments.
    "activity"             : "CMIP6", # examples : "PMIP", 'LS3MIP LUMIP'; defaults to "CMIP6"
    
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
    "branch_method"        : "standard", # default value='standard' meaning 
                                         #~ "select a start date" 
    "branch_time_in_parent": "365.0D0", # a double precision value, in parent time units, 
    "branch_time_in_child" : "0.0D0", # a double precision value, in child time units, 
    #'parent_time_units'    : "" #in case it is not the same as child time units
    #'parent_variant_label' :""  #Default to 'same as child'. Other cases should be expceptional
    #'parent_sub_experiment_id' : "" # In case it is not the same as child
    #"parent_mip_era"       : 'CMIP5'   # only in special cases (as e.g. PMIP warm 
                                        #start from CMIP5/PMIP3 experiment)
    #'parent_activity   '   : 'CMIP'    # only in special cases, defaults to CMIP
    #'parent_source_id'     : 'CNRM-CM5.1' # only in special cases, where parent model 
                                           # is not the same model
    #
    "sub_experiment_id"    : "none", # Optional, default is 'none'; example : s1960. 
    "sub_experiment"       : "none", # Optional, default in 'none'
    #'parent_subexperiment_id': '' # unusual
    "history"              : "", #Used when a simulation is re-run, an output file is modified ...
    # A per-variable dict of comments which are specific to this simulation. It will replace  
    # the all-simulation comment
    'comments'     : {
        'tas' : 'tas diagnostic uses a special scheme in this simulation',
        }
    }

#mpmoine_new: classe necessaire a la fonctionnalite "liste maison"
class simple_CMORvar(object):
    def __init__(self):
        self.type           = None # Only useful for HOMEvar.
        self.modeling_realm = None # Useful for both HOMEvar and CMORvar.
        self.mipTable       = None # Useful for both HOMEvar and CMORvar.
        self.label          = None # Useful for both HOMEvar and CMORvar.
        self.frequency      = None # Useful for both HOMEvar and CMORvar.
        self.mipTable       = None # Useful for both HOMEvar and CMORvar.
        self.positive       = None # Useful for CMORvar and updated HOMEvar.
        self.description    = None # Useful for CMORvar and updated HOMEvar.
        self.stdname        = None # Useful for CMORvar and updated HOMEvar.
        self.long_name      = None # Useful for CMORvar and updated HOMEvar.
        #self.cell_methods   = None
        #self.cell_measures  = None
        self.spatial_shp    = None # Only useful for HOMEvar.
        self.temporal_shp   = None # Only useful for HOMEvar.
        self.experiment     = None # Only useful for HOMEvar.
        self.mip            = None # Only useful for HOMEvar.

#mpmoine_new: dictionnaire necessaire a la fonctionnalite "liste maison"

spid2label={}
nobjs=len(dq.coll['spatialShape'].items)
for i in range(nobjs-1):
    obj=dq.coll['spatialShape'].items[i]
    spid2label.update({obj.uid:obj.label}) 

#mpmoine_new: dictionnaire necessaire a la fonctionnalite "liste maison"
tmid2label={}
nobjs=len(dq.coll['temporalShape'].items)
for i in range(nobjs-1):
    obj=dq.coll['temporalShape'].items[i]
    tmid2label.update({obj.uid:obj.label}) 

#mpmoine_new: fonction necessaire a la fonctionnalite "liste maison"
def read_homeVars_list(hmv_file,expid,mips):
    # File structure: name of attributes to read, number of header line 
    home_attrs=['type','label','modeling_realm','frequency','mipTable','temporal_shp','spatial_shp','experiment','mip']
    skip=3
    # Read file
    with open(hmv_file,"r") as fp:
        data=fp.readlines()
    # Build list of home variables
    homevars=[]
    nhv=0
    for line in data[skip:]:  
        line_split=line.split(';')
        nhv+=1
        home_var=simple_CMORvar()
        cc=-1
        for col in line_split:
            ccol=col.lstrip(' ').rstrip('\n\t ')
            if ccol!='': 
                cc+=1
                setattr(home_var,home_attrs[cc],ccol)
        if home_var.mip!="ANY":
            if home_var.mip in mips:
                if home_var.experiment!="ANY":
                     if home_var.experiment==expid: homevars.append(home_var)
                else: 
                    homevars.append(home_var)
        else:
            if home_var.experiment!="ANY":
                if home_var.experiment==expid: homevars.append(home_var)
            else: 
                homevars.append(home_var)
    return homevars

#mpmoine_new: fonction necessaire a la fonctionnalite "liste maison"
def get_SpatialAndTemporal_Shapes(cmvar):
    try:
        for struct in dq.coll['structure'].items:
            if struct.uid==cmvar.stid: 
                spatial_shape=spid2label[struct.spid]
                temporal_shape=tmid2label[struct.tmid]
                return [spatial_shape,temporal_shape]
    except:
        print "Error:",[cmvar.label, cmvar.mipTable],"CMORvar: Structure of CMORvar NOT found!"
        return [False,False]

#mpmoine_new: fonction necessaire a la fonctionnalite "liste maison"
def get_corresp_CMORvar(hmvar):
    collect=dq.coll['CMORvar']
    found=False
    count=0
    cmvar_found=[]
    for cmvar in collect.items:
        # Consider case where no modeling_realm associated to the current CMORvar as matching anymay. 
        #mpmoine# A mieux gerer avec les orphan_variables ?
        match_label=(cmvar.label==hmvar.label)
        match_freq=(cmvar.frequency==hmvar.frequency)
        match_table=(cmvar.mipTable==hmvar.mipTable)
        match_realm=(hmvar.modeling_realm in cmvar.modeling_realm.split(' '))
        empty_realm=(cmvar.modeling_realm=='') 
        matching=( match_label and match_freq and match_table and (match_realm or empty_realm) )
        if matching: 
            same_shapes=(get_SpatialAndTemporal_Shapes(cmvar)==[hmvar.spatial_shp,hmvar.temporal_shp])
            if same_shapes:
                found=True
                count+=1
                cmvar_found.append(cmvar)
            else: 
                print "Error: ",[hmvar.label,hmvar.mipTable]," HOMEVar: Spatial and Temporal Shapes specified DO NOT match CMORvar ones." \
                      " -> Provided:",[hmvar.spatial_shp,hmvar.temporal_shp],'Expected:',get_SpatialAndTemporal_Shapes(cmvar)

    if found:
        if count==1: 
            # Collect complementary attributes from CMORvar and glue them to HOMEvar
            hmvar.positive=cmvar_found[0].positive
            hmvar.long_name=cmvar_found[0].title
            mipvar = dq.inx.uid[cmvar_found[0].vid]
            #hmvar.long_name=mipvar.title
            stdname = dq.inx.uid[mipvar.sn]
            if stdname:
                if stdname._h.label == 'standardname':
                    hmvar.stdname = stdname.label
                    hmvar.description = stdname.description
                else:
                    print "Issue: stdname is remark in DR for",mipvar.label
            else:
                print "Issue: accessing sn for",cmvar_found[0].label
            return hmvar
        else:
            return False
    else:
        return False

#mpmoine_new: fonction necessaire a la fonctionnalite "liste maison"
def hasCMORVarName(hmvar):
    collect=dq.coll['CMORvar']
    match_label=False
    for cmvar in collect.items:
        if (cmvar.label==hmvar.label): match_label=True
    return match_label
                
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
            #mpmoine_modif# 'e.egid' au lieu de 'e.gid'
            if 'egid' in dir(e) and e.egid == group_id and e.label==experiment : 
                if (debug) :  print " OK for experiment based on group"+group_id.label,
                relevant=True
    elif item_exp._h.label== 'mip' :
        mip_id=ri.esid
        if (debug)  : print "%20s"%"Mip case ",dq.inx.uid[mip_id].label,
        for e in exps :
            if 'mip' in dir(e) and e.mip == mip_id :
                if (debug) :  print e.label,",",
                if e.label==experiment : 
                    if (debug) :  print " OK for experiment based on mip"+mip_id.label,
                    relevant=True
    else :
        # TBD !! : understand what is happening in that case 
        if (debug)  : print "%20s"%'Other case , label=%s|'%item_exp._h.label,
    if relevant :
        if 'tslice' in ri.__dict__ and ri.tslice != '__unset__' :
            timeslice=dq.inx.uid[ri.tslice]
            if (debug) : print "OK for the year"
            return year >= timeslice.start and year<=timeslice.end
        else :
            # TBD : !! test once timeSlices will be set in DR
            if (debug)  : print "tslice not set -> OK for the year"
            return True
    if (debug)  : print "NOK"
    #mpmoine_modif# return 'relevant' au lieu 'False'
    return relevant

def select_CMORvars_for_lab(lset, experiment_id=None, year=None, printout=False):
    """
    A function to list CMOR variables relevant for a lab (and also, optionnally for 
    an experiment and a year)
    
    Args:
      dq : dreqQuery object
      lset (dict): laboratory settings; used to provide the list of MIPS, the max 
                   Tier, and a list of excluded variable names
      experiment_id (string,optional): if willing to filter on a given experiment - not 
                   used if year is None
      year (int,optional) : simulation year - used to filter the request for an 
                   experiment and a year
    
    Returns:
      A list of CMOR variables DR uids
      
    
    """
    #
    # From MIPS set to Request links
    sc = dreqQuery(dq=dq, tierMax=lset['tierMax'])
    rls_for_mips=sc.getRequestLinkByMip(lset['mips'])
    if printout :
        print "\nNumber of Request Links which apply to MIPS", lset['mips']," is: ",\
            len(rls_for_mips)
        
    if (year) :
        filtered_rls=[]
        for rl in rls_for_mips :
            # Access all requesItems ids which refer to this RequestLink
            ri_ids=dq.inx.iref_by_sect[rl.uid].a['requestItem']
            for ri_id in ri_ids :
                ri=dq.inx.uid[ri_id]
                #print "Checking requestItem ",ri.label
                if RequestItem_applies_for_exp_and_year(ri,experiment_id, year,False) :
                    #print "% 25s"%ri.label," applies "
                    filtered_rls.append(rl)
        rls=filtered_rls
        if printout :
            print "\nNumber of Request Links which apply to experiment ", \
                experiment_id,"and experiment",\
        lset['mips'] ," is: ",len(rls)
    else :
        rls=rls_for_mips
       
    # From Request links to CMOR vars
    miprl_ids=[ rl.uid for rl in rls ]
    miprl_vars=sc.varsByRql(miprl_ids, pmax=lset['max_priority'])
    if printout :
        print '\nNumber of CMOR variables for these requestLinks is :',len(miprl_vars)
    filtered_vars=[ v for v in miprl_vars if dq.inx.uid[v].label not in lset['excluded_vars'] ]
    if printout :
        print '\nNumber of CMOR variables once filtered by excluded vars is :',len(miprl_vars)
    
    # Just for printout : Count distinct var labels
    varlabels=set()
    for v in filtered_vars : varlabels.add(dq.inx.uid[v].label)
    if printout :
        print '\nNumber of variables with distinct labels is :',len(varlabels)

    #mpmoine_new# on alimente un objet de type cimple_CMORvar. Necessaire a la "liste maison"
    # Build a list of simplified CMORvar objects
    simplified_vars = []
    for v in filtered_vars :
        svar = simple_CMORvar()
        cmvar = dq.inx.uid[v]
        svar.label = cmvar.label
        svar.frequency = cmvar.frequency
        svar.mipTable = cmvar.mipTable
        svar.modeling_realm = cmvar.modeling_realm
        svar.mipTable = cmvar.mipTable
        svar.positive = cmvar.positive
        mipvar = dq.inx.uid[cmvar.vid]
        svar.long_name = mipvar.title
        [svar.spatial_shp,svar.temporal_shp]=get_SpatialAndTemporal_Shapes(cmvar)

        #mpmoine_modif# deplacement dans 'select_CMORvars_for_lab' de tout ce qui concerne les MAJ d'attributs (stdname, units, cell_methods,...)
        #mpmoine_modif# anciennement dans 'write_xios_field_ref_in_file_def' pour centraliser le renseignement es attributs 'svar'
        try :
            stdname = dq.inx.uid[mipvar.sn]
            #units=mipvar.units
            if stdname._h.label == 'standardname':
                svar.stdname = stdname.label
                #svar.units = stdname.units
                svar.description = stdname.description
            else :
                print "Issue : stdname is remark in DR for %s!"%mipvar.label
        except:
            print "Issue accessing sn for %s !"%cmvar.label
        # TBD : translate cell_method in XIOS operations
        #struct=dq.inx.uid[cmvar.stid]
        #svar.cell_methods = struct.cell_methods
        #svar.cell_measures = struct.cell_methods
        simplified_vars.append(svar)
    
     #mpmoine_modif# return 'simplified_vars' au lieu de 'filtered_vars'
    return simplified_vars

def write_xios_file_def(cmvs,table, lset,sset, out,cvspath) :
    """ 
    Generate an XIOS file_def entry in out for :
      - a dict for laboratory settings 
      - a dict of simulation settings 
      - a list 'cmvs' of CMOR variables DR ids, 
      - which all belong to given table
      - a path 'cvs' for Controlled Vocabulary
      
    Lenghty code, but not longer than the corresponding specification document
    
    After a prologue, attributes valid for all variables are written as file-level metadata, 
    in the same order than in WIP document; last, field-level meatdate are written
    """
    #
    experiment_id=sset['experiment_id']
    # Variant matters
    realization_index=sset.get('realization_index',1) 
    initialization_index=sset.get('initialization_index',1)
    physics_index=sset.get('physics_index',1)
    forcing_index=sset.get('forcing_index',1)
    variant_label="r%di%dp%df%d"%(realization_index,initialization_index,\
                                  physics_index,forcing_index)
    #
    # WIP Draft on filenames - july 2016 
    # <variable_id>_<table_id>_<experiment_id >_<source_id>_<member_id>_<grid_label>[_<time_range>].nc
    member_id=variant_label
    sub_experiment_id=sset.get('sub_experiment_id','none')
    if sub_experiment_id != 'none':
        member_id = sub_experiment_id+"-"+member_id
    grid_label="TBD" #TBD
    time_range="%start_date%_%end_date%" # XIOS syntax
    filename="%s_%s_%s_%s_%s_%s"%\
               (table, experiment_id,lset['model_id'], member_id,grid_label,time_range)
    #mpmoine_modif# out.write('<file name="%s"\n'%filename)

    # WIP Draft 14 july 2016
    activity=sset['activity'] 
    freq=table2freq[table] 
    split_freq="10y" #TBD : compute file-level split_freq
    #mpmoine_modif# deplacement de l'ecriture du debut de banniere '<file name=' ici pour s approcher
    #mpmoine_modif# d'un xml valide
    out.write('<file name="%s" freq_output="%s" append="true" split_freq="%s" timeseries="exclusive" >\n'%\
              (filename,freq[0],split_freq))
    out.write('  <variable name="project_id" type="string" > %s/%s </variable>\n'%(
                   sset.get('project',"CMIP6"),activity))
    #
    def wr(key,dic_or_val=None,default=None) :
        """
        Short cut for a repetitive pattern : writing in 'out' a string variable name and value
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
            if dic_or_val  : val=dic_or_val
            else :
                print 'error in wr,  no value provided for '%key
        if val :
            out.write('  <variable name="%s"  type="string" > %s </variable>\n'%(key,val))

    wr('activity',activity)
    #wr('comment') # par variable
    contact=sset.get('contact',lset.get('contact',None))
    if contact and contact is not "" : wr('contact',contact) 
    conventions="CF-1.7 CMIP-6.0" ;     wr('conventions',conventions) 
    # YYYY-MM-DDTHH:MM:SSZ
    creation_date=datetime.utcnow().isoformat()[0:-7]+"Z" ; wr('creation_date',creation_date) 
    data_specs_version="TBD" # TBD, but not yet available in CMIP6_CVs ...
    wr('data_specs_version',data_specs_version)
    #
    #mpmoine_modif# ajout d une gestion d exception dans la correspondance entre experiment_id (DRQ) et experiment (CMIP6-CVs)
    #mpmoine_modif# car le CV de la DataRequest n est pas encore totalement coherent avec le CMIP6-CVs
    with open(cvspath+"CMIP6_experiment_id.json") as json_fp :
        json_data=json.loads(json_fp.read())
    try:
        CMIP6_experiments=json_data[experiment_id]
        experiment=CMIP6_experiments['experiment']
    except:
        experiment="Issue"
    wr('experiment',experiment)
    wr('experiment_id',experiment_id)
    # 
    external_variables= "TBD" 
    wr('forcing_index',forcing_index) 
    wr('frequency',freq[1])
    # URL
    mip_era="CMIP6"
    institution_id=lset['institution_id']
    source_id=lset['model_id']
    sub_experiment_id=sset.get('sub_experiment_id','none')
    further_info_url="http://furtherinfo.es-doc.org/%s.%s.%s.%s.%s.%s"%(
        mip_era,institution_id,source_id,experiment_id,sub_experiment_id,variant_label)
    wr('further_info_url',further_info_url)
    #
    wr('grid','TBD') #TBD - depend du model et du realm, donc de la variabble
    wr('grid_label','TBD') #TBD - -d - gn pour Nemo, gr pour Arpege
    wr('grid_resolution','TBD') #TBD - id
    wr('history',sset) 
    wr("initialization_index",initialization_index)
    wr("institution_id",institution_id)
    wr("institution",lset)
    license="CMIP6 model data produced by %s is licensed under a Creative Commons Attribution"\
        %lset['institution']+\
     "'Share Alike' 4.0 International License (http://creativecommons.org/licenses/by/4.0/). "+\
      "Use of the data should be acknowledged following guidelines found at "+\
      "https://pcmdi.llnl.gov/home/CMIP6/citation.html."+\
      "Further information about this data, including some limitations, can be found "+\
      "via the further_info_url"+\
      "(recorded as a global attribute in data files)[ and at %s].  "%lset["info_url"]+\
      "The data producers and data providers make no warranty, either express or implied,, "+\
      " including but not limited to, warranties of merchantability and fitness for a "+\
      "particular purpose. All liabilities arising"+\
     " from the supply of the information (including any liability arising in negligence) "+\
     "are excluded to the fullest extent permitted by law."
    wr("license",license)
    wr('mip_era',mip_era)
    parent_experiment_id=sset.get('parent_experiment_id',None)
    if parent_experiment_id and parent_experiment_id != 'no_parent' :
        parent_activity_id=sset.get('parent_activity','CMIP')
        wr('parent_activity_id',parent_activity_id)
        wr("parent_experiment_id",sset); 
        parent_mip_era=sset.get('parent_mip_era',"CMIP6") ; 
        if parent_mip_era=="" : parent_mip_era="CMIP6"
        wr('parent_mip_era',parent_mip_era) 
        parent_source_id=sset.get('parent_source_id',source_id) ; 
        wr('parent_source_id',parent_source_id)
        wr("parent_sub_experiment_id",sset, False); 
        # TBX : syntaxe XIOS pour designer le time units de la simu courante
        parent_time_units=sset.get('parent_time_units',"TBX") 
        wr("parent_time_units",parent_time_units)
        parent_variant_label=sset.get('parent_variant_label',variant_label) 
        wr('parent_variant_label',parent_variant_label)
        wr('branch_method',sset,'standard')
        wr('branch_time_in_child',sset)
        wr('branch_time_in_parent',sset) 
    wr("physics_index",physics_index) 
    wr('product','output')
    wr("realization_index",realization_index) 
    #wr('realm',"TBD") # decline par variable
    wr('references',lset) 
    # TBD - should be taken from CMIP6_CV once it is updated for CNRM and IPSL models
    wr('source',lset['model']) 
    wr('source_id',source_id)
    source_type=sset.get('source_type',lset.get('source_type')) 
    if type(source_type)==type([]) :
        source_type=reduce(lambda x,y : x+" "+y, source_type)
    wr('source_type',source_type)
    wr('sub_experiment_id',sub_experiment_id) 
    wr("table_id",table)
    wr("title","%s model output prepared for %s / %s %s"%(\
        source_id,sset.get('project',"CMIP6"),activity,experiment_id))
    wr("tracking_id","hdl:21.14100/"+uuid4().get_urn().split(":")[2]) 
    #variable_id # decline par variable
    wr("variant_info",sset,"")
    wr("variant_label",variant_label)
    #
    # Iterate on variables
    #

    for cmv in cmvs : 
        write_xios_field_ref_in_file_def(cmv,out,lset,sset)
    #mpmoine# correction de la banniere de cloture
    out.write('</file>\n\n')

def write_xios_field_ref_in_file_def(cmv,out,lset,sset) :
    """
    Writes a CMOR variable entry (provided as a DR uid) as a field reference in out, 
    with prefix 'CMIP_' for the variable name
    """
    # TBD : identify the cell_method wrt to time and translate it to XIOS time_operation. 
    # + same for space
    # TBD : logic for computing ts_split_frequency from rank and time-space ops
    
    #
    # By convention, field references are built as CMIP_<MIP_varable_name>
    # Such references muts be fulfilled using a dedicated filed_def section implementing 
    # the match between legacy model field names and such names
    #

    def wrv(name, value):
        # Write a 'variable' entry
        out.write('     <variable name="%s" type="string" > %s </variable>\n'%(name,value))
    #
    alias="CMIP_"+cmv.label
    split_freq="10y" #TBD - Should be computed
    operation="average" #TBD - Not systematically - to improve

    out.write('  <field field_ref="%s" name="%s" operation="%s" ts_enabled="true" ts_split_freq="%s">\n'%(
                        alias,cmv.label,operation,split_freq))
    comment=None
    if cmv.stdname in sset['comments'] :
        comment=sset['comments'][mipvarlabel] #A_VERIFIER: mipvarlabel
    else: 
        if cmv.stdname in sset['comments'] : #A_VERIFIER: meme condition repetee
            comment=sset['comments'][mipvarlabel] #A_VERIFIER: mipvarlabel
    if comment : wrv('comment',comment) #TBI 
    #
    wrv('realm',cmv.modeling_realm) 
    wrv('variable_id',cmv.label)
    wrv("standard_name",cmv.stdname)
    wrv("description",cmv.description)
    wrv("long_name",cmv.long_name)
    if cmv.positive != "None" and cmv.positive != "" : wrv("positive",cmv.positive) 

    #mpmoine_modif# deplacement dans 'select_CMORvars_for_lab' de tout ce qui concerne les MAJ d'attributs (stdname, units, cell_methods,...)
    #mpmoine_modif# anciennement dans 'write_xios_field_ref_in_file_def' pour centraliser le renseignement es attributs 'svar'

    #
    out.write('     </field>\n')

def generate_file_defs(lset,sset,year,context,cvs_path,printout=False) :
    """
    Using DR objetc dq, a dict of lab settings and a dict of simulation settings, 
    generate an XIOS file_def file for a given XIOS 'context', which content matches 
    the DR for the experiment quoted in simu setting dict and a year
    Makes use of CMIP6 controlled vocuabulary files found in cvs_path
    Output file is named <context>.xml
    Structure of the two dicts is documented elsewhere. It includes the 
    correspodance between a context and a few realms
    """
    #
    # Extract CMOR variables for the experiment and year and lab settings
    mip_vars_list=select_CMORvars_for_lab(lset, sset['experiment_id'], \
                                            year,printout=printout)
    if lset['listof_home_vars']:
        # Read HOME variables
        home_vars_list=read_homeVars_list(lset['listof_home_vars'],sset['experiment_id'],lset['mips'])
        for hv in home_vars_list: 
            hv_info={"varname":hv.label,"realm":hv.modeling_realm,"freq":hv.frequency,"table":hv.mipTable}
            print hv_info
            if hv.type=='cmor':
                # Update each HOME variable with complementary attributes get from the corresponding CMOR variable (if exist)
                updated_hv=get_corresp_CMORvar(hv)
                if(updated_hv):
                    already_in_dr=False
                    for cmv in mip_vars_list:
                        matching=(  cmv.label==updated_hv.label and \
                                    cmv.modeling_realm==updated_hv.modeling_realm and \
                                    cmv.frequency==updated_hv.frequency and \
                                    cmv.mipTable==updated_hv.mipTable and \
                                    cmv.temporal_shp==updated_hv.temporal_shp and \
                                    cmv.spatial_shp==updated_hv.spatial_shp  )
                        if matching: already_in_dr=True

                    # Corresponding CMOR Variable fond for the current HOME variable 
                    if not already_in_dr:
                        # Append HOME variable only if not already selected with the DataRequest
                        if printout: print "Info:",hv_info,"HOMEVar is not in the DataRequest." \
                                         " => Taken into account."
                        mip_vars_list.append(updated_hv)
                    else:
                        if printout: print "Info:",hv_info,"HOMEVar is already in the DataRequest." \
                                           " => Not taken into account."
                else:
                    if printout: print "Error:",hv_info,"HOMEVar is anounced as cmor but no corresponding CMORVar was found." \
                                       " => Not taken into account."
                    sys.exit("Abort: HOMEVar is cmor but no corresponding CMORVar found.")
            elif hv.type=='perso':
                # Check if HOME variable anounced as 'perso' is in fact 'cmor'
                is_cmor=get_corresp_CMORvar(hv)
                if not is_cmor:
                    # Check if  HOME variable differs from CMOR one only by shapes
                    has_cmor_varname=hasCMORVarName(hv)
                    if has_cmor_varname:
                        if printout: print "Warning:",hv_info,"HOMEVar is anounced as perso, is not a CMORVar, but has a cmor name." \
                                            " => Not taken into account."
                        sys.exit("Abort: HOMEVar is anounced as perso, is not a CMORVar, but has a cmor name.")
                    else:
                        # This HOME variable is purely personnal (does not exist in the CMOR language)
                        if printout: print "Info:",hv_info,"HOMEVar is purely personnal." \
                                           " => Taken into account."
                        mip_vars_list.append(hv)
                else:
                    if printout: print "Error:",hv_info,"HOMEVar is anounced as perso, but in reality is cmor." \
                                       " => Not taken into account."
                    sys.exit("Abort: HOMEVar is anounced as perso but should be cmor.")
            else:
                if printout: print "Error:",hv_info,"HOMEVar type",hv.type,"does not correspond to any known keyword."\
                                   " => Not taken into account."
                sys.exit("Abort: unknown type keyword is provided for HOMEVar.")
    else:
        print "Info: No HOMEvars list provided."
    # Group CMOR vars per realm
    cmvs_per_realm=dict()
    #mpmoine_modif# changement de noms des variables ('cmv_uuid'->'cmv'; 'miprl_vars_list'->'mip_vars_list') car avec
    #mpmoine_modif# les  elements des listes de variables CMOR ne sont plus des RequestLinks mais des Simple_CMORVars maintenant
    for cmv in mip_vars_list :
        if cmv.modeling_realm not in cmvs_per_realm.keys() :
            cmvs_per_realm[cmv.modeling_realm]=[]
        cmvs_per_realm[cmv.modeling_realm].append(cmv)
    if printout :
        print "\nRealms for these CMORvars :",cmvs_per_realm.keys()
    #
    # Select on context realms, grouping by table
    cmvs_pertable=dict()
    context_realms=lset['realms_per_context'][context]
    for realm in context_realms : 
        if realm in cmvs_per_realm.keys():
            for cmv in cmvs_per_realm[realm] :
                if cmv.mipTable not in cmvs_pertable : 
                    cmvs_pertable[cmv.mipTable]=[]
                if cmv.label not in lset['excluded_vars'] : 
                    cmvs_pertable[cmv.mipTable].append(cmv)
    #
    # Add cmvars belonging to the orphan list
    orphans=lset['orphan_variables'][context]
    for cmv in mip_vars_list :
        if cmv.label in orphans:
            #mpmoine_rmq# ligne suivante: realm_cmvs_pertable n est pas defini
            if cmv.mipTable not in realm_cmvs_pertable :
                cmvs_pertable[cmv.mipTable]=[]
            if cmv.label not in excluded_vars : 
                cmvs_pertable[cmv.mipTable].append(cmv)
    #    
    if printout :
        print "\nTables concerned by context %s : "%context, cmvs_pertable.keys()
    if printout :
        print "\nVariables per table :"
    for table in cmvs_pertable :    
        if printout :
            print "%15s %02d ---->"%(table,len(cmvs_pertable[table])),
        for cmv in cmvs_pertable[table] : 
            if printout :
                print cmv.label,
        if printout :
            print
    #
    # Write XIOS file_def
    filename="%s.xml"%context
    with open(filename,"w") as out :
        #for table in ['day'] :    
        for table in cmvs_pertable :  
            write_xios_file_def(cmvs_pertable[table],table, lset,sset,out,cvs_path)
    if printout :
        print "\nfile_def written as %s"%filename
