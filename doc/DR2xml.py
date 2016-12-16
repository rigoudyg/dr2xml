
# coding: utf-8

## An example for generating the XIOS file_def for a given lab, model, experiment, year and XIOS context

## _This example shows how to use a list of Home Variables_

### Define the settings specific to the laboratory and the model

# In[1]:

lab_and_model_settings={
    'institution_id': "CNRM-CERFACS", # institution should be read in CMIP6_CV, if up-to-date
    #'institution'   : "Centre National de Recherches Meteorologiques", 
    'source_types' : { "CNRM-CM6-1" : "AOGCM", "CNRM-CM6-1-HR" : "AOGCM", 
                       "CNRM-ESM2-1": "ESM"  , "CNRM-ESM2-1-HR": "ESM" },
    'source_id'      : "CNRM-CM6-1", 
    'source'         : "CNRM-CM6-1", # Useful only if CMIP6_CV is not uptodate
    #'source_type' : "AER"  # You may override here the source-type value deduced from source_id and sources_type
    'references'    :  "A character string containing a list of published or web-based "+\
        "references that describe the data or the methods used to produce it."+\
        "Typically, the user should provide references describing the model"+\
        "formulation here",
    'info_url'      : "http://www.umr-cnrm.fr/cmip6/",
    'contact'       : 'contact.cmip@cnrm.fr',
    
    # We account for the list of MIPS in which the lab takes part.
    # Note : a MIPs set limited to {'C4MIP'} leads to a number of tables and 
    # variables which is manageable for eye inspection
    'mips': {'C4MIP', 'SIMIP', 'OMIP', 'CFMIP', 'RFMIP'} , 
    'mips_all' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
                      'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
    #'mips' : {'HighResMIP'},

    # Max variable priority level to be output
    'max_priority' : 1,
    'tierMax'      : 3,

    # The ping file defines variable names, which are constructed using CMIP6 "MIPvarnames" 
    # and a prefix which must be set here, and can be the empty string :
    "ping_variables_prefix" : "CMIP6_",

    # We account for a list of variables which the lab does not want to produce , 
    # oragnized by realms
    # excluded_vars_file="./inputs/non_published_variables.txt"
    "excluded_vars":[],
    
    # We account for a list of variables which the lab wants to produce in some cases
    #"listof_home_vars":"./inputs/my_listof_home_vars.txt",
    "listof_home_vars":"./config_utest/utest020_listof_home_vars.txt",
        
    # Each XIOS  context does adress a number of realms
    'realms_per_context' : { 'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'] ,
                          'arpsfx' : ['atmos', 'atmos atmosChem', 'aerosol', 'atmos land', 'land',
                                     'landIce land',  'aerosol land','land landIce',  'landIce', ],
                          }, 
    # Some variables, while belonging to a realm, may fall in another XIOS context than the 
    # context which handles that realm
    'orphan_variables' : { 'nemo' : ['dummy_variable_for_illustration_purpose'],
                           'arpsfx' : [],
                           },
    'vars_OK' : dict(),
    # A per-variable dict of comments valid for all simulations
    'comments'     : {
        'tas' : 'nothing special about tas'
        }
    }


### Define the settings for the processed simulation 

# In[2]:

simulation_settings={    
    # Dictionnary describing the necessary attributes for a given simulation

    # Warning : some lines are commented out in this example but should be 
    # un-commented in some cases. See comments

    "experiment_id"  : "historical",
    #"experiment_id"  : "Forced-Atmos-Land",
    #"experiment_id"  : "Coupled",
    #"experiment_id"  : "DCPP-C13",
    
    #"contact"        : "", set it only if it is specific to the simualtion
    #"project"        : "CMIP6",  #CMIP6 is the default

    #'source_type'    : "ESM" # If source_type is special only for this experiment (e.g. : AMIP)
                      #(i.e. not the same as in lab_and_model settings), you may tell that here

    # MIP specifying the experiment. For historical, it is CMIP6 itself
    # In a few cases it may be appropriate to include multiple activities in the activity_id 
    # (with multiple activities allowed, separated by single spaces).  
    # An example of this is “LUMIP AerChemMIP” for one of the land-use change experiments.
    "activity_id"       : "CMIP", # examples : “PMIP”, “LS3MIP LUMIP”; defaults to "CMIP6"
    
    # It is recommended that some description be included to help identify major differences among variants, 
    # but care should be taken to record correct information.  Prudence dictates that this attribute includes 
    # a warning along the following lines:  “Information provided by this attribute may in some cases be flawed.#
    # Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute.”
    "variant_info"      : "Start date chosen so that variant r1i1p1f1 has the better fit with Krakatoa impact on tos",
    #
    "realization_index"    : 1, # Value may be omitted if = 1
    "initialization_index" : 1, # Value may be omitted if = 1
    "physics_index"        : 1, # Value may be omitted if = 1
    "forcing_index"        : 1, # Value may be omitted if = 1
    #
    # All about the parent experiment and branching scheme
    "parent_experiment_id" : "piControl", # omit this setting (or set to 'no parent') if not applicable
                                          # (remaining parent attributes will be disregarded)
    "branch_method"        : "standard", # default value='standard', meaning ~ "select a start date" 
    "branch_time_in_parent": "365.0D0", # a double precision value, in parent time units, 
    "branch_time_in_child" : "0.0D0", # a double precision value, in child time units, 
    #'parent_time_units'    : "" #in case it is not the same as child time units
    #'parent_variant_label' :""  #Default to 'same as child'. Other cases should be expceptional
    #"parent_mip_era"       : 'CMIP5'   # only in special cases (e.g. PMIP warm start from CMIP5/PMIP3 experiment)
    #'parent_activity   '   : 'CMIP'    # only in special cases, defaults to CMIP
    #'parent_source_id'     : 'CNRM-CM5.1' #only in special cases, where parent model is not the same model
    #
    "sub_experiment_id"    : "none", # Optional, default is 'none'; example : s1960. 
    "sub_experiment"       : "none", # Optional, default in 'none'
    "history"              : "none", #Used when a simulation is re-run, an output file is modified ....
    # A per-variable dict of comments which are specific to this simulation. It will replace  
    # the all-simulation comment present in lab_and_model_settings
    'comments'     : {
        'tas' : 'tas diagnostic uses a special scheme in this simulation',
        }
    }



# In[3]:

from dr2xml import generate_file_defs


# In[4]:

# Path to local copy of CMIP6 CVs, which you can get from https://github.com/WCRP-CMIP/CMIP6_CVs
#my_cvspath="/Users/moine/Codes/MyDevel_Codes/CMIP6_DATA_SUITE/CMIP6_CVs/"
my_cvspath="/cnrm/est/USERS/senesi/public/CMIP6/data_request/CMIP6_CVs/"


# In[5]:

generate_file_defs(lab_and_model_settings, simulation_settings,year=2000,context='nemo',printout=True, cvs_path=my_cvspath)


# In[6]:

generate_file_defs(lab_and_model_settings, simulation_settings,year=2000,context='arpsfx',printout=True, cvs_path=my_cvspath)


# In[ ]:




# In[ ]:



