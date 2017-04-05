
# coding: utf-8

# # An example for generating the XIOS file_def for a given lab, model, experiment, year and XIOS context

# # _This example shows how to use a list of Home Variables_

# In[ ]:

# Select your laboratory among: 'cnrm', 'cerfacs', 'ipsl'
lab='cnrm'


# ## Define the settings specific to the laboratory and the model

# In[ ]:

if lab=='cnrm' or lab=='cerfacs':
    lab_and_model_settings={
        'institution_id': "CNRM-CERFACS", # institution should be read in CMIP6_CV, if up-to-date

        # entry 'source_types' allows to describe, using CMIP6 CV, the various model configurations
        # for the lab; This can be superseded by an entry 'source_type' either just below or in dict  
        # for simulation settings (further below)
        'source_types' : { "CNRM-CM6-1" : "AOGCM", "CNRM-CM6-1-HR" : "AOGCM", 
                           "CNRM-ESM2-1": "ESM"  , "CNRM-ESM2-1-HR": "ESM" },

        "source_id"      : "CNRM-CM6-1",
        "source"         : "CNRM-CM6-1", # Useful only if CMIP6_CV is not up-to-date for the source_id
        # You may override here the source-type value deduced from source_id and sources_type
        #-'source_type' : "AER"  

        'references'    :  "A character string containing a list of published or web-based "+\
            "references that describe the data or the methods used to produce it."+\
            "Typically, the user should provide references describing the model"+\
            "formulation here",
        'info_url'      : "http://www.umr-cnrm.fr/cmip6/",
        'contact'       : 'contact.cmip@cnrm.fr',

        # We account for the list of MIPS in which the lab takes part.
        # Note : a MIPs set limited to {'C4MIP'} leads to a number of tables and 
        # variables which is manageable for eye inspection
        'mips_all' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
                          'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
        'mips': {'C4MIP', 'SIMIP', 'OMIP', 'CFMIP', 'RFMIP'} , 

        # Max variable priority level to be output
        'max_priority' : 1,
        'tierMax'      : 3,

        # The ping file defines variable names, which are constructed using CMIP6 "MIPvarnames" 
        # and a prefix which must be set here, and can be the empty string :
        "ping_variables_prefix" : "CMIP6_",

        # We account for a list of variables which the lab does not want to produce , 
        # oragnized by realms
        "excluded_vars_file":"./inputs/non_published_variables.txt",
        "excluded_vars":[],
        # mpmoine_next_modif: ignore some spatial shapes
        "excluded_spshapes":["XYA-na","XYG-na"],

        # We account for a list of variables which the lab wants to produce in some cases
        "listof_home_vars":None,
        # mpmoine_last_modif: Path for extra Tables
        "path_extra_tables":None,

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
            },

        # Sizes of oce and atm grids (cf DR doc)
        "sizes"  : [292*362,75,128*256,91,30,14,128],

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
        'grid_choice' : { "CNRM-CM6-1" : "LR", "CNRM-CM6-1-HR" : "HR", "CNRM-ESM2-1": "LR"  , "CNRM-ESM2-1-HR": "HR" },
        # mpmpoine_next_modif: Model component Time steps (min)
        "model_timestep" : { "arpsfx":60., "nemo":60.}
        }


# In[ ]:

if lab=='cerfacs':  
    lab_and_model_settings["mips"]={'HighResMIP'}
    lab_and_model_settings["listof_home_vars"]="./inputs/my_listof_home_vars.txt"
    lab_and_model_settings["path_extra_tables"]="./inputs/extra_Tables"


# In[ ]:

if lab=='ipsl':
    lab_and_model_settings={
        'institution_id': "IPSL", # institution should be read in CMIP6_CV, if up-to-date
        'source_id'      : "IPSL-CM6-1", 
        # The description of lab models, in CMIP6 CV wording
        'source_types' : { "IPSL-CM6-1" : "AOGCM", "IPSL-CM6-1-HR" : "AOGCM", 
                           "IPSL-ESM2-1": "ESM"  , "IPSL-ESM2-1-HR": "ESM" },
        'source'         : "IPSL-CM6-1", # Useful only if CMIP6_CV is not up to date
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
        "excluded_vars_file":None,
        "excluded_vars":[],
        # mpmoine_next_modif: ignore some spatial shapes
        "excluded_spshapes":["XYA-na","XYG-na"],

        # We account for a list of variables which the lab wants to produce in some cases
        "listof_home_vars":None,
        # mpmoine_last_modif: Path for extra Tables
        "path_extra_tables":None,

        # Each XIOS  context does adress a number of realms
        'realms_per_context' : { 
            'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'],
            'lmdz' : ['atmos', 'atmos land'] , 
            'orchidee': ['land', 'landIce land',  'land landIce', 'landIce'] ,
                              }, 
        # Some variables, while belonging to a realm, may fall in another XIOS context than the 
        # context which hanldes that realm
        'orphan_variables' : { 
            'nemo' : [],
            'lmdz' : [],
            'orchidee' : [],
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
        # Grids : CMIP6 name, name_of_target_domain, CMIP6-std resolution, and description
        "grids" : { 
          "LR"    : {
            "lmdz" : [ "gr","" , "??? km", "LMDZ grid"] ,
              "nemo" : [ "gn", ""        , "100km" , "native ocean tri-polar grid with 105 k ocean cells" ],
          "orchidee" :  [ "gr","" , "??? km", "LMDZ grid"],},
        },
        'grid_choice' : { "IPSL-CM6-1" : "LR", "IPSL-CM6-1-HR" : "HR",
                          "IPSL-ESM2-1": "LR"  , "IPSL-ESM2-1-HR": "HR" },
        # mpmpoine_next_modif: Model component Time steps (min)
        "model_timestep" : { "nemo":60., "lmdz":60.,"orchidee":60.}

    }


# ## Define the settings for the processed simulation 

# In[ ]:

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
    # mpmoine_future_modif: CMOR3.2.2 impose 'None' pour sub_experiment_id et sub_experiment
    "sub_experiment_id"    : "None", # Optional, default is 'None'; example : s1960. 
    "sub_experiment"       : "None", # Optional, default in 'None'
    "history"              : "None", #Used when a simulation is re-run, an output file is modified ....
    # A per-variable dict of comments which are specific to this simulation. It will replace  
    # the all-simulation comment present in lab_and_model_settings
    'comments'     : {
        'tas' : 'tas diagnostic uses a special scheme in this simulation',
        }
    }



# In[ ]:

if lab=='cerfacs':    
    simulation_settings["experiment_id"]="Forced-Atmos-Land"
    #simulation_settings["experiment_id"]="Coupled"
    #simulation_settings["experiment_id"]="DCPP-C13"


# In[ ]:

from dr2xml import generate_file_defs


# In[ ]:

# Path to local copy of CMIP6 CVs, which you can get from https://github.com/WCRP-CMIP/CMIP6_CVs
if lab=='cnrm':
    my_cvspath="/cnrm/est/USERS/senesi/public/CMIP6/data_request/CMIP6_CVs/"
elif lab=='cerfacs':
    my_cvspath="/Users/moine/Codes/MyDevel_Codes/CMIP6_DATA_SUITE/CMIP6_CVs/"
elif lab=='ipsl':
    my_cvspath="/ccc/cont003/home/gencmip6/p86caub/CMIP6_DR_DR2XML/CMIP6_CVs/"
my_cvspath="/Users/moine/Codes/MyDevel_Codes/CMIP6_DATA_SUITE/CMIP6_CVs/"


# In[ ]:

# In/Out directory
my_dir="output_test/"+lab+"/"


# In[ ]:

#help(generate_file_defs)


# In[ ]:

if True : 
    for my_context in lab_and_model_settings["realms_per_context"].keys():
        generate_file_defs(lab_and_model_settings, simulation_settings,year=2000,context=my_context,
                    pingfile=my_dir+"ping_"+my_context+".xml", printout=True, 
                    cvs_path=my_cvspath,dummies='include', dirname=my_dir)


# ### after some edit in ping files, which does not discard every 'dummy' entries 
# 

# In[ ]:

# In/Out directory
my_dir="../pingfiles_edited/"+lab+"/"


# In[ ]:

# after some edit in ping_arpsfx.xml, which does not discard every 'dummy' entries 
if False :
    for my_context in lab_and_model_settings["realms_per_context"].keys():
        generate_file_defs(lab_and_model_settings, simulation_settings,year=2000,context=my_context,
                    pingfile=my_dir+"ping_"+my_context+".xml", printout=True, 
                    cvs_path=my_cvspath,dummies='skip', dirname=my_dir)


# 
