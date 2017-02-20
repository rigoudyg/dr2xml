rootpath="/cnrm/est/USERS/senesi/public/CMIP6/"
my_cvspath=rootpath+"data_request/CMIP6_CVs/"

lab_and_model_settings={
    'institution_id': "CNRM-CERFACS", # institution should be read in CMIP6_CV, if up-to-date
    'source_types' : { "CNRM-CM6-1" : "AOGCM", "CNRM-CM6-1-HR" : "AOGCM", 
                       "CNRM-ESM2-1": "ESM"  , "CNRM-ESM2-1-HR": "ESM" },

    "source_id"      : "CNRM-CM6-1",
    "source"         : "CNRM-CM6-1", # Useful only if CMIP6_CV is not up-to-date for the source_id
    'references'    :  "ref",
    'info_url'      : "http://www.umr-cnrm.fr/cmip6/",
    'contact'       : 'contact.cmip@cnrm.fr',
    'mips': {'C4MIP', 'SIMIP', 'OMIP', 'CFMIP', 'RFMIP'} , 
    'mips_all' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
                      'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
    'max_priority' : 3,
    'tierMax'      : 3,
    "ping_variables_prefix" : "CMIP6_",
    # excluded_vars_file="./inputs/non_published_variables.txt"
    "excluded_vars":[],
    "listof_home_vars":rootpath+"dr2xml/config_utest/utest020_listof_home_vars.txt",
    'realms_per_context' : { 'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'] ,
                          'arpsfx' : ['atmos', 'atmos atmosChem', 'aerosol', 'atmos land', 'land',
                                     'landIce land',  'aerosol land','land landIce',  'landIce', ],
                          }, 
    'orphan_variables' : { 'nemo' : ['dummy_variable_for_illustration_purpose'],
                           'arpsfx' : [],
                           },
    'vars_OK' : dict(),
    # A per-variable dict of comments valid for all simulations
    'comments'     : {},
        # Sizes for atm and oce grids (cf DR doc)
    "sizes"  : [259200,60,64800,40,20,5,100],
    # What is the maximum size of generated files, in number of float values
    "max_file_size_in_floats" : 500.*1.e+6 ,
    # grid_policy among None, DR, native, native+DR, adhoc- see docin grids.py 
    "grid_policy" : "native",
    # Resolutions
    "grids" : { 
      "LR"    : {
#        "arpsfx" : [ "gr","complete" , "250 km", "data regridded to a T127 gaussian grid (128x256 latlon) from a native atmosphere T127l reduced gaussian grid"] ,
        "arpsfx" : [ "gn","" , "250 km", "native T127 reduced gaussian grid"] ,
          "nemo" : [ "gn", ""        , "100km" , "native ocean tri-polar grid with 105 k ocean cells" ],},
      "HR"    : {
        "arpsfx" : [ "gr","completeHR", "50 km", "data regridded to a 359 gaussian grid (180x360 latlon) from a native atmosphere T359l reduced gaussian grid"] ,
          "nemo" : [ "gn", ""         , "25km" , "native ocean tri-polar grid with 1.47 M ocean cells" ],},
    },
    'grid_choice' : { "CNRM-CM6-1" : "LR", "CNRM-CM6-1-HR" : "HR", "CNRM-ESM2-1": "LR"  , "CNRM-ESM2-1-HR": "HR" },

    }

simulation_settings={    
    "experiment_id"  : "historical",
    "activity_id"       : "CMIP", 
    "parent_experiment_id" : "piControl", # omit this setting (or set to 'no parent') if not applicable # (remaining parent attributes will be disregarded)
    "branch_method"        : "standard", # default value='standard', meaning ~ "select a start date" 
    "branch_time_in_parent": "365.0D0", # a double precision value, in parent time units, 
    "branch_time_in_child" : "0.0D0", # a double precision value, in child time units,
    "comments"             : {}
    }

