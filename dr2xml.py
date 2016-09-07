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

# Next package retrieved using
#    svn co http://proj.badc.rl.ac.uk/svn/exarch/CMIP6dreq/tags/01.beta.34
# (and must include 01.beta.34/dreqPy in PYTHONPATH)
from scope import dreqQuery

# Where is the local copy of CMIP6 Controled vocabulary (available from 
# https://github.com/WCRP-CMIP/CMIP6_CVs
my_cvs_path="/cnrm/aster/data3/aster/senesi/public/CMIP6/data_request/CMIP6_CVs/"

# A local auxilliary table
from table2freq import table2freq


""" An example/template  of settings for a lab and a model"""
cnrm_lab_and_model_settings={
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

historical_simulation_settings={    
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

def RequestItem_applies_for_exp_and_year(dq,ri,experiment,year,debug=False):
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
            if 'gid' in dir(e) and e.gid == group_id and e.label==experiment : 
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
    return False


def select_CMORvars_for_lab(dq,lset, experiment_id=None, year=None, printout=False):
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
                if RequestItem_applies_for_exp_and_year(dq,ri,experiment_id, year,False) :
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
    
    return filtered_vars



def write_xios_file_def(dq,cmvs,table, lset,sset, out,cvspath) :
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
    out.write('<file name="%s"\n'%filename)
    
    # WIP Draft 14 july 2016
    activity=sset['activity'] 
    freq=table2freq[table] 
    split_freq="10y" #TBD : compute file-level split_freq
    out.write(' freq_output="%s" append="true" split_freq="%s" timeseries="exclusive" >\n'%\
              (freq[0],split_freq))
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
    with open(cvspath+"CMIP6_experiment_id.json","r") as json_fp :
        CMIP6_experiments=json.loads(json_fp.read())['experiment_id']
    exp_entry=CMIP6_experiments[sset['experiment_id']]
    experiment=exp_entry['experiment']
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
        write_xios_field_ref_in_file_def(dq,cmv,out,lset,sset)
    out.write('<file/>\n\n')


def write_xios_field_ref_in_file_def(dq,cmv,out,lset,sset) :
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
    mipvar=dq.inx.uid[cmv.vid]
    alias="CMIP_"+mipvar.label
    split_freq="10y" #TBD - Should be computed
    operation="average" #TBD - Not systematically - to improve
    out.write('  <field field_ref="%s" name="%s" operation="%s" ts_enabled="true" ts_split_freq="%s">\n'%(
                        alias,mipvar.label,operation,split_freq))

    #
    def wrv(name, value):
        # Write a 'variable' entry
        out.write('     <variable name="%s" type="string" > %s </variable>\n'%(name,value))
    #
    comment=None
    if mipvar.label in sset['comments'] :
        comment=sset['comments'][mipvarlabel]
    else: 
        if mipvar.label in sset['comments'] :
            comment=sset['comments'][mipvarlabel]
    if comment : wrv('comment',comment) #TBI 
    #
    wrv('realm',cmv.modeling_realm) 
    wrv('variable_id',mipvar.label)
    #
    slabel="Issue"
    desc="Issue"
    try :
       stdname=dq.inx.uid[mipvar.sn]
       #units=mipvar.units
       if stdname._h.label == 'standardname':
            slabel=stdname.label
            #sunits=stdname.units
            desc=stdname.description
       else :
            print "Issue : stdname is remark in DR for %s!"%mipvar.label
    except:
        print "Issue accessing sn for %s !"%cmv.label
    wrv("standard_name",slabel)
    wrv("description",desc)
    wrv("long_name",mipvar.title)
    if cmv.positive != "None" and cmv.positive != "" : wrv("positive",cmv.positive)
    #
    # TBD : translate cell_method in XIOS operations
    #
    #structure=dq.inx.uid[cmv.stid]
    #wrv("cell_methods",structure.cell_methods)
    #wrv("cell_measures",structure.cell_measures)
    #
    out.write('     </field>\n')

    


def generate_file_defs(dq,lset,sset,year,context,printout=False,
                       cvs_path=my_cvs_path) :
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
    miprl_vars_list=select_CMORvars_for_lab(dq,lset, sset['experiment_id'], \
                                            year,printout=printout)
    #
    # Group CMOR vars per realm
    cmvs_per_realm=dict()
    for cmv_uid in miprl_vars_list :
        cmv=dq.inx.uid[cmv_uid]
        if cmv.modeling_realm not in cmvs_per_realm :
            cmvs_per_realm[cmv.modeling_realm]=[]
        cmvs_per_realm[cmv.modeling_realm].append(cmv_uid)
    if printout :
        print "\nRealms for these CMORvars :",cmvs_per_realm.keys()
    #
    # Select on context realms, grouping by table
    cmvs_pertable=dict()
    context_realms=lset['realms_per_context'][context]
    for realm in context_realms :
        if realm in cmvs_per_realm:
            for cmv_uid in cmvs_per_realm[realm] :
                cmv=dq.inx.uid[cmv_uid]
                #print cmv.label,
                if cmv.mipTable not in cmvs_pertable : 
                    cmvs_pertable[cmv.mipTable]=[]
                if cmv.label not in lset['excluded_vars'] : 
                    cmvs_pertable[cmv.mipTable].append(cmv)
    #
    # Add cmvars belonging to the orphan list
    orphans=lset['orphan_variables'][context]
    for cmv_uid in miprl_vars_list :
        cmv=dq.inx.uid[cmv_uid]
        if cmv.label in orphans:
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
    # Write XIOS file_def
    filename="%s.xml"%context
    with open(filename,"w") as out :
        #for table in ['day'] :    
        for table in cmvs_pertable :    
            write_xios_file_def(dq,cmvs_pertable[table],table, lset,sset,out,cvs_path)
    if printout :
        print "\nfile_def written as %s"%filename
