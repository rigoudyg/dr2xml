# -*- coding: iso-8859-15 -*-

# This file is used for telling dr2xml a number of parameters that are dependant on the
# laboratory and models, and the default value for parameters that are dependant on the
# experiment (and which may be changed in a companion file 'experiment_settings.py'

# The plain user will usually not change anything here; the CMIP6 expert will, in
# agreement with the lab's CMIP6 point(s) of contact

# The reference documents are listed in top level document :https://pcmdi.llnl.gov/CMIP6/Guide/
# Of interest :
#   - paragraph 5 of https://pcmdi.llnl.gov/CMIP6/Guide/modelers.html
#   - CMIP6 Data Request , in browsable format: http://clipc-services.ceda.ac.uk/dreq/index.html

lab_and_model_settings={

    #---------------------------------------------------------------------------------------------- 
    #----- SETTINGS FOR THE MODELLING GROUP & ITS MODEL (possibly several versions):
    #---------------------------------------------------------------------------------------------- 
    
    'institution_id': "CNRM-CERFACS", # institution full description will be read in CMIP6_CV
    
    # We describe the "CMIP6 source type" (i.e. components assembly) which is the default
    # for each model. This value can be changed on a per experiment basis, in experiment_settings file
    # However, using a 'configuration' is finer (see below)
    # CMIP6 component conventions are described at
    #          https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_source_type.json
    #>>>'source_types'  : {
    #>>>                "CNRM-CM6-1"    : "AOGCM",
    #>>>                "CNRM-ESM2-1"   : "AOGCM BGC AER CHEM",
    #>>>                   },

    # 'configurations' are shortcuts for a triplet (model, source_type, unused_contexts)
    'configurations' : {
                    "AOGCM":  ("CNRM-CM6-1"   ,"AOGCM"              , []      ),
                    "AOESM":  ("CNRM-ESM2-1"  ,"AOGCM BGC AER CHEM" , []      )
                        },
    
    # A character string containing additional information about the models. Will be complemented
    # with the experiment's specific comment string
    #>>>"comment"              : "",
    
    # Which are the MIPs the lab is taking part in. This should not be changed.
    # MIPS list is at http://clipc-services.ceda.ac.uk/dreq/index/mip.html
    'mips' : {
        "LR" : {'CMIP', 'OMIP'},
        "HR" : {'CMIP'},
        },
    
    # Describe the branching scheme for experiments involved in some 'branchedYears type' tslice
    # (for details, see: http://clipc-services.ceda.ac.uk/dreq/index/Slice.html )
    # Just put the as key the common start year in child and as value the list of start years in parent for all members
    "branching" : {},
  
    # dr2xml must know which Xios 'context' handle which 'realms'
    'realms_per_context' : { 'nemo'  : ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgChem', 'seaIce ocean'] ,
                            'surfex' : ['atmos', 'atmos atmosChem', 'atmosChem', 'aerosol', 'atmos land', 'land',
                                        'landIce land',  'aerosol','land landIce',  'landIce', ],
                            'trip'   : [],
                            }, 
    
    # Some variables, while belonging to a realm, may fall in another XIOS context than the 
    # context which hanldes that realm
    'orphan_variables' : {},
    
    # The ping file defines variable names, which are constructed using CMIP6 
    # "MIPvarnames" and a prefix which must be set here
    "ping_variables_prefix" : "CMIP6_",

    # The path of the directory which, at run time, contains the root XML file (iodef.xml)
    "path_to_parse":"./xml_input/basics/",

    #---------------------------------------------------------------------------------------------- 
    #----- SELECTION OF OUTPUT VARIABLE TO PRODUCE (EXCLUDE/INCLUDE ONLY):
    #---------------------------------------------------------------------------------------------- 

    # The default priority level for variables to produce. Can be changed on a per experiment basis
    # For generating ping_files templates, you would set it to 3
    'max_priority'  : 1,

    # Next value is used when creating ping_files templates
    'tierMax'       : 1,

    # Variables we  exclude from the production
    # Note : Names must match DR MIPvarnames (and **NOT** CMOR standard_names)
    # Note : Names must match DR MIPvarnames (and **NOT** CMOR standard_names)
    "excluded_vars" : [''],

    # For test purpose, we can alternatively specify an inclusive list of 
    # variables to process. This has precedence over the excluded_vars stuff
    #>>>"included_vars" : [],

    # You can specifically exclude some pairs (vars,tables), here in lab_settings 
    # and also (in addition) in experiment_settings
    #>>>"excluded_pairs" : [] ,
    # The list of CMIP6 tables is at http://clipc-services.ceda.ac.uk/dreq/index/miptable.html
    # For test purpose, you may exclude some tables, using entry "excluded_tables", or alternatively specify 
    # an inclusive list of tables to process, using entry "included_tables"
    #>>>"excluded_tables"  : [],
    #>>>"included_tables"  : [],    # This entry has precedence over excluded_tables. Used for debug

    # When atmospheric vertical coordinate implies putting psol in model-level output files, we
    # must avoid creating such file_def entries if the model does not actually send the 3D fields
    # (because this leads to files full of undefined values)

    # We choose to describe such fields as a list of vars dependant on the model configuration
    # because the DR is not in a good enough shape about realms for this purpose    
    #>>>"excluded_vars_per_config" : {
    #>>>    "AOGCM":  [], 
    #>>>    },
 
    # Handling field shapes
    "excluded_spshapes": [
                        "XYA-na","XYG-na", # GreenLand and Antarctic grids we do not want to produce
                        #"na-A",            # RFMIP.OfflineRad : rld, rlu, rsd, rsu in table Efx ?????
                        #"Y-P19","Y-P39", "Y-A","Y-na" 
                        ],

    # Each DR RequestLink links a set of variables with a set of experiments
    # The requestLinks list is at http://clipc-services.ceda.ac.uk/dreq/index/requestLink.html 
    "excluded_request_links"  : [
        "RFMIP-AeroIrf" # 4 scattered days of historical, heavy output -> please rerun model for one day
        # for each day of this request_link 
        ],
    
    # Tell which CMIP6 frequencies are unreachable for a single model run. Datafiles will
    # be labelled with dates consistent with content (but not with CMIP6 requirements).
    # Allowed values are only 'dec' and 'yr'
    #>>>"too_long_periods" : [],
    
    # You may provide some variables already horizontally remapped 
    # to some grid (i.e. Xios domain) in external files. The varname in file 
    # must match the DR variable label. Used for fixed fields only
    # TBD - Not yet validated 
    #>>>'fx_from_file' : {},
    
    # When using select='no', Xios may enter an endless loop, which is solved if next setting is False
    #>>>'allow_tos_3hr_1deg' : False,
    
    # Should we allow for another type of duplicate vars : two vars
    # with same name in same table (usually with different
    # shapes). This applies to e.g. CMOR vars 'ua' and 'ua7h' in
    # 6hPlevPt. Default to False, because CMIP6 rules does not allow
    # to name output files differently in that case. If set to True,
    # you should also set 'use_cmorvar_label_in_filename' to True to
    # overcome the said rule
    #>>>'allow_duplicates_in_same_table' : False,

    #---------------------------------------------------------------------------------------------- 
    #----- GRID SETTINGS:
    #---------------------------------------------------------------------------------------------- 
    
    # dr2xml allows for the lab to choose among various output grid policies:
    #  - DR or None : always follow DR requirement
    #  - native     : never follow DR spec (always use native or close-to-native grid)
    #  - native+DR  : always produce on the union of grids
    #  - adhoc      : decide on each case, based on CMORvar attributes, using a 
    #                 lab-specific scheme implemented in a lab-provided Python 
    #                 function lab_adhoc_grid_policy in grids.py 
    "grid_policy" : "adhoc",
    # at the time of writing, CNRM choice is:
    #  - tos and sos are provided on those DR requested grids which are among ("native", "1deg")
    #  - other vars are provided on DR requested grids except on "1deg", "2deg", "100km", "50km" 

    # Output grids description : per model resolution and per context :
    #              - CMIP6 qualifier (i.e. 'gn' or 'gr') for the main grid chosen (because you
    #                 may choose as main production grid a regular one, when the native grid is e.g. unstructured)
    #              - Xios id for the production grid (if it is not the native grid),
    #              - Xios id for the latitude axis used for zonal means (mist match latitudes for grid above)
    #              - resolution of the production grid (using CMIP6 conventions),
    #              - grid description
    "grids" : { 
      "LR"    : {
        "surfex" : [ "gr", "complete", "glat","250 km", "data regridded to a T127 gaussian grid "+\
                    "(128x256 latlon) from a native atmosphere T127l reduced gaussian grid"] ,
        #"surfex" : [ "gn", "" , "250 km", "native T127 reduced gaussian grid"] ,
        "trip" : [ "gn", "",  "","50 km", "regular 1/2 deg lat-lon grid" ],
        "nemo" : [ "gn", "",  "","100 km", "native ocean tri-polar grid with 105 k ocean cells" ],
          },

      "HR"    : {
        "surfex" : [ "gr","complete", "glat","50 km", "data regridded to a 359 gaussian grid "+\
                    "(360x720 latlon) from a native atmosphere T359l reduced gaussian grid"] ,
        "trip" : [ "gn", "", "", "50 km", "regular 1/2 deg lat-lon grid" ],
        "nemo" : [ "gn", "", "", "25 km", "native ocean tri-polar grid with 1.47 M ocean cells" ]
          },
        },
        
    # Tell which model use which grids resolutions set                      
    'grid_choice' : { "CNRM-CM6-1" : "LR", "CNRM-CM6-1-HR" : "HR", "CNRM-ESM2-1": "LR"  , "CNRM-ESM2-1-HR": "HR" },
           
    # Sizes for atm and oce grids (cf DR doc); Used for computing file split frequency
    "sizes"  : { "LR" : [294*362  , 75, 128*256, 91, 30, 14, 128],
                 "HR" : [1442*1050, 75, 720*360, 91, 30, 14, 128] },
  
    #---------------------------------------------------------------------------------------------- 
    #----- TIMESTEPS & SPECIAL TIME OPERATIONS:
    #---------------------------------------------------------------------------------------------- 
        
    # Basic sampling timestep set in your field definition (used to feed metadata 'interval_operation')
    "sampling_timestep" : {
                "LR"    : { "surfex":900., "nemo":1800., "trip":1800. },
                "HR"    : { "surfex":900., "nemo":1800., "trip":1800. }, 
                },
    
    # Vars computed with a period which is not the basic timestep must be declared explictly,
    # grouped by their timestep, in order that 'instant' sampling works correctly
    # (the units for period should be different from the units of any instant ouput frequency
    # for those variables - 'mi' loooks fine, 'ts' may work)
    #>>>"special_timestep_vars" : {
    #>>>    "60mi" : ['']
    #>>>    },
    
    # dr2xml will drive vertical interpolation to pressure levels. This is a costly step if done
    # at every timestep
    "vertical_interpolation_sample_freq" : "",  # use Xios duration syntax
    #>>>"vertical_interpolation_operation"   : "", # LMD prefers 'average'
        
    # CFMIP has an elaborated requirement for defining subhr frequency; by default, dr2xml uses 1 time step
    #>>>"CFsubhr_frequency" : "2ts",
      
    #---------------------------------------------------------------------------------------------- 
    #----- HANDLING THE SIZE OF NETCDF OUTPUT FILES:
    #---------------------------------------------------------------------------------------------- 

    # What is the target maximum size of generated files, in number of float values
    "max_file_size_in_floats" : 4.*1.e+9 , # 5 Go
    
    # NetCDF compression level
    "compression_level"  :  4,
    
    # Estimate of number of bytes per floating value, given the chosen compression level
    "bytes_per_float" : 2.4,

    #---------------------------------------------------------------------------------------------- 
    #----- HANDLING FILE & VARIABLE ATTRIBUTES:
    #---------------------------------------------------------------------------------------------- 

    # You may add a series of NetCDF attributes in all files for this simulation
    #>>>"non_standard_attributes" : {},

    # If your model has some axis which does not have all its attributes
    # as in DR, and you want dr2xml to fix that it, give here
    # the correspondence from model axis id to DR dim/grid id.
    # For label dimensions you should provide the list of labels, ordered
    # as in your model, as second element of a pair
    # Label-type axes will be processed even if not quoted
    # Scalar dimensions are not concerned by this feature
    #>>>'non_standard_axes' : {},

    # A smart workflow will allow you to extend a simulation during it
    # course and to complement the output files accordingly, by
    # managing the 'end date' part in filenames. You can then set next
    # setting to False. 
    #>>>'dr2xml_manages_enddate' : False,
    
    # CMIP6 rule is that filenames includes the variable label, and
    # that this variable label is not the CMORvar label, but 'MIPvar'
    # label. This may lead to conflicts, e.g. for 'ua' and 'ua7h' in
    # table 6hPlevPt; next setting allows to avoid that, if set to True
    #>>>'use_cmorvar_label_in_filename' : False,

    # DR has sn attributes for MIP variables. They can be real,CF-compliant, standard_names or
    # pseudo_standard_names, i.e. not yet approved labels. Default is to use only CF ones
    #>>>'allow_pseudo_standard_names' : True,
     
    #---------------------------------------------------------------------------------------------- 
    #----- ADDITIONAL NETCDF ATTRIBUTES TO WRITE IN OUTPUT FILES:
    #---------------------------------------------------------------------------------------------- 
        
    # Contact and more info pointers
    #>>>'references'    : "",
    'info_url'      : "",
    #>>>'contact'       : '',

    # A per-variable dict of comments valid for all simulations. They will be 
    # included in datafiles as field metadata
    'comments'     : {},
        
    #---------------------------------------------------------------------------------------------- 
    #----- LOG & DEBUG PRINT LEVEL:
    #---------------------------------------------------------------------------------------------- 

    # For an extended printout of selected CMOR variables, grouped by variable label
    #>>>'print_stats_per_var_label' : False,
    
    # In order to identify which xml files generates a problem, you can use this flag
    'debug_parsing' : False, # default to False !

}

