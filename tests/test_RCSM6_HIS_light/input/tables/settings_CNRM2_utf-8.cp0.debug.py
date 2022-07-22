# -*- coding: utf-8 -*-

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
    
    'institution_id': "CNRM", # institution full description will be read in CMIP6_CV
    'institution': "CNRM (Centre National de Recherches Meteorologiques, Toulouse 31057, France)", 
    
    # We describe the "CMIP6 source type" (i.e. components assembly) which is the default
    # for each model. This value can be changed on a per experiment basis, in experiment_settings file
    # However, using a 'configuration' is finer (see below)
    # CMIP6 component conventions are described at
    #          https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_source_type.json
    'source_types'  : {
                           "CNRM-ALADIN64"  : "ARCM AER",
                           "CNRM-RCSM6A"    : "AORCM AER",
                           "CNRM-CM6-1"    : "AOGCM",
                           "CNRM-CM6-1-HR" : "AOGCM", 
                           "CNRM-ESM2-1"   : "AOGCM BGC AER CHEM"  ,
                           "CNRM-ESM2-1-HR": "AOGCM BGC AER" },

    # 'configurations' are shortcuts for a triplet (model, source_type, unused_contexts)
    'configurations' : {
        "ARCM":   ("CNRM-ALADIN64"  ,"ARCM AER"           , ['nemo']),
        "AGCM":   ("CNRM-CM6-1"    ,"AGCM"               , ['nemo']),
        "AGCMAER":("CNRM-CM6-1"    ,"AGCM AER"           , ['nemo']),
        "AESM":   ("CNRM-ESM2-1"   ,"AGCM BGC AER CHEM"  , ['nemo']),
        "AORCM":  ("CNRM-RCSM6A"    ,"AORCM AER"          , []),
        "AOGCM":  ("CNRM-CM6-1"    ,"AOGCM"              , []      ),
        "AOESM":  ("CNRM-ESM2-1"   ,"AOGCM BGC AER CHEM" , []      ),
        "AGCMHR": ("CNRM-CM6-1-HR" ,"AGCM"               , ['nemo']),
        "AGCMHRAER":("CNRM-CM6-1-HR","AGCM AER"           , ['nemo']),
        "AESMHR": ("CNRM-ESM2-1-HR","AGCM BGC AER"       , []      ),
        "AOGCMHR":("CNRM-CM6-1-HR" ,"AOGCM"              , []      ),
        "AOESMHR":("CNRM-ESM2-1-HR","AOGCM BGC AER"      , []      ),
        "LGCM":   ("CNRM-CM6-1"    ,"LAND"               , ['nemo']),
        "LESM":   ("CNRM-ESM2-1"   ,"LAND BGC"           , ['nemo']),
        "OGCM":   ("CNRM-CM6-1"    ,"OGCM"               , ['surfex','trip']),
        "OESM":   ("CNRM-ESM2-1"   ,"OGCM BGC"           , ['surfex','trip']),
        "OGCMHR": ("CNRM-CM6-1-HR" ,"OGCM"               , ['surfex','trip']),
        "OESMHR": ("CNRM-ESM2-1-HR","OGCM BGC"           , ['surfex','trip'])},

    # Which are the MIPs the lab is taking part in. This should not be changed.
    # MIPS list is at http://clipc-services.ceda.ac.uk/dreq/index/mip.html
    'mips' : {
        "LR" : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP', 'GeoMIP','GMMIP','ISMIP6',\
                'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP',\
                'HighResMIP', 'DCPP', 'CMIP6', 'CMIP'},
        "HR" : {'OMIP','ScenarioMIP','CMIP6', 'CMIP'},
        "REG" : {'CORDEX'},
        },

    # A character string containing additional information about the models. Will be complemented
    # with the experiment's specific comment string
    "comment"              : "",

    # The default priority level for variables to produce. Can be changed on a per experiment basis
    # For generating ping_files templates, you would set it to 3
    'max_priority'  : 1,

    # Next value is used when creating ping_files templates
    'tierMax'       : 1,
    
    # Handling variables to produce : We exclude
    # - pfull and phalf because we have a pressure based hydrid coordinate, and 
    # - <GHG>xxxClim because we always have inter-annual variation (except for piControl
    #   but we want a reguler scheme)
    # Note : Names must match DR MIPvarnames (and **NOT** CMOR standard_names)
    "excluded_vars" : ['pfull', 'phalf',\
                       'n2oClim', 'ch4globalClim', 'co2massClim', \
                       'n2oglobalClim', 'ch4Clim', 'o3Clim', 'co2Clim'],

    # Vars computed with a period which is not the basic timestep must be declared explictly,
    # grouped by their timestep, in order that 'instant' sampling works correctly
    # (the units for period should be different from the units of any instant ouput frequency
    # for those variables - 'mi' loooks fine, 'ts' may work)
    "special_timestep_vars" : {
        "60mi" : ['cllcalipso', 'clmcalipso', 'clhcalipso', 'cltcalipso', \
                     'cllcalipsoice', 'clmcalipsoice', 'clhcalipsoice', 'cltcalipsoice', \
                     'cllcalipsoliq', 'clmcalipsoliq', 'clhcalipsoliq', 'cltcalipsoliq', \
                     'cllcalipsoun', 'clmcalipsoun', 'clhcalipsoun', 'cltcalipsoun', \
                     'clcalipso', 'clcalipsoice', 'clcalipsoliq', 'clcalipsoun', \
                     'clcalipsotmp', 'clcalipsotmpice', 'clcalipsotmpliq', 'clcalipsotmpun', \
                     'cfadLidarsr532', \
                     'parasolRefl', 'parasolCRefl', \
                     'cltlidarradar', 'clcalipso2', 'cfadDbze94', \
                     'cltisccp', 'pctisccp', 'tauisccp', 'albisccp', 'meantbisccp', 'meantbclrisccp', 'clisccp', \
                     'cltmodis', 'clwmodis', 'climodis', 'clhmodis', 'clmmodis', 'cllmodis', \
                     'tautmodis', 'tauwmodis', 'tauimodis', 'reffclwmodis', 'reffclimodis', \
                     'pctmodis', 'lwpmodis', 'iwpmodis', 'clmodis', \
                     'jpdftaureliqmodis', 'jpdftaureicemodis', \
                     'clmisr'],
        },

    # For test purpose, we can alternatively specify an inclusive list of 
    # variables to process. This has precedence over the excluded_vars stuff
    #"included_vars" : ['ccb' ],

    # You can specifically exclude some pairs (vars,tables), here in lab_settings 
    # and also (in addition) in experiment_settings
    #"excluded_pairs" : [ ('sfdsi','SImon') ] ,

    # The list of CMIP6 tables is at http://clipc-services.ceda.ac.uk/dreq/index/miptable.html
    # For test purpose, you may exclude some tables, using entry "excluded_tables", or alternatively specify 
    # an inclusive list of tables to process, using entry "included_tables"
    #"excluded_tables"  : [ "Eyr", "Oyr", "Odec", "IfxAnt", "ImonAnt" ],    
    "included_tables"  : [ "Amon" ],    # This entry has precedence over excluded_tables. Used for debug
    
    # When atmospheric vertical coordinate implies putting psol in model-level output files, we
    # must avoid creating such file_def entries if the model does not actually send the 3D fields
    # (because this leads to files full of undefined values)
    # We choose to describe such fields as a list of vars dependant on the model configuration
    # because the DR is not in a good enough shape about realms for this purpose
    "excluded_vars_per_config" : {
        "ARCM":  [ "ch4", "co2", "co", "h2o", "hcho", "hcl", 
                   "hno3", "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", 
                   "fco2antt", "fco2fos", "fco2nat", 
                   'oxloss', 'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage', 'noy','cLand',
                   'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp',
                   'netAtmosLandCO2Flux', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                   'fVegLitter', 'nbp', 'shrubFrac' ],
        "AORCM":  [ "ch4", "co2", "co", "h2o", "hcho", "hcl", 
                   "hno3", "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", 
                   "fco2antt", "fco2fos", "fco2nat", 
                   'oxloss', 'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage', 'noy','cLand',
                   'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp',
                   'netAtmosLandCO2Flux', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                   'fVegLitter', 'nbp', 'shrubFrac' ],
        "AGCM":  [ "ch4", "co2", "co", "concdust", "ec550aer", "h2o", "hcho", "hcl", 
                   "hno3", "mmrbc", "mmrdust", "mmroa", "mmrso4", "mmrss", 
                   "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", "so2", "mmrpm1", 
                   "fco2antt", "fco2fos", "fco2nat", "loadbc", "loaddust", "loadoa", "loadso4", "loadss",
                   'oxloss', 'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage', 'noy', 'drybc', 'drydust',
                   'dryoa', 'dryso2', 'dryso4', 'dryss', 'emibc', 'emidust', 'emioa', 'emiso2', 'emiso4',
                   'emiss', 'od440aer', 'od870aer', 'od550lt1aer', 'wetbc', 'wetdust', 'wetoa', 'wetso4', 'wetss', 'cLand',
                   'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp',
                   'netAtmosLandCO2Flux', 'od443dust', 'od865dust', 'sconcdust', 'sconcso4', 'sconcss',
                   'sedustCI', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                   'fVegLitter', 'nbp', 'shrubFrac' ],
        "AGCMAER":[ "ch4", "co2", "co", "h2o", "hcho", "hcl", 
                   "hno3",  
                   "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh",  
                   "fco2antt", "fco2fos", "fco2nat", 
                   'oxloss', 'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage', 'noy', 
                   'cLand',
                   'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp',
                   'netAtmosLandCO2Flux', 
                   'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                   'fVegLitter', 'nbp', 'shrubFrac' ],
        "AGCMHRAER":[ "ch4", "co2", "co", "h2o", "hcho", "hcl", 
                   "hno3",  
                   "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh",  
                   "fco2antt", "fco2fos", "fco2nat", 
                   'oxloss', 'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage', 'noy', 
                   'cLand',
                   'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp',
                   'netAtmosLandCO2Flux', 
                   'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                   'fVegLitter', 'nbp', 'shrubFrac' ],
        "AOGCM": [ "ch4", "co2", "co", "concdust", "ec550aer", "h2o", "hcho", "hcl", 
                    "hno3", "mmrbc", "mmrdust", "mmroa", "mmrso4", "mmrss", 
                    "n2o", "no2", "no", "o3Clim", "o3loss", "o3prod", "oh", "so2", "mmrpm1", 
                    "fco2antt", "fco2fos", "fco2nat", "loadbc", "loaddust", "loadoa", "loadso4", "loadss",
                   'oxloss', 'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage', 'noy', 'drybc', 'drydust',
                   'dryoa', 'dryso2', 'dryso4', 'dryss', 'emibc', 'emidust', 'emioa', 'emiso2', 'emiso4',
                   'emiss', 'od440aer', 'od870aer', 'od550lt1aer', 'wetbc', 'wetdust', 'wetoa', 'wetso4', 'wetss', 'cLand',
                   'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp',
                   'netAtmosLandCO2Flux', 'od443dust', 'od865dust', 'sconcdust', 'sconcso4', 'sconcss',
                   'sedustCI', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                   'fVegLitter', 'nbp', 'shrubFrac' ],
        "AESM":  [ 'co2mass', 'ch4global', 'n2oglobal' ],
        "AOESM": [ 'co2mass', 'ch4global', 'n2oglobal' ],
        "LGCM":  ['ch4', 'co2', 'hur', 'hus', 'n2o', 'o3', 'ta', 'ua', 'va', 'wap', 'zg', 'clt',
                  'ccb', 'cct', 'ci', 'clivi', 'clt', 'clwvi', 'evspsbl', 'fco2antt', 'fco2fos',
                  'pr', 'prc', 'prsn', 'prw', 'ps', 'psl', 'rldscs','rlut', 'rlutcs', 'rsdscs', 
                  'rsdt', 'rsuscs', 'rsut', 'rsutcs','ch4global', 'co2mass', 'n2oglobal','mc',
                   'cl', 'cli', 'clw'],
        "LESM":  ['ch4', 'co2', 'hur', 'hus', 'n2o', 'o3', 'ta', 'ua', 'va', 'wap', 'zg', 'clt',
                  'ccb', 'cct', 'ci', 'clivi', 'clt', 'clwvi', 'evspsbl', 'fco2antt', 'fco2fos',
                  'pr', 'prc', 'prsn', 'prw', 'ps', 'psl', 'rldscs','rlut', 'rlutcs', 'rsdscs', 
                  'rsdt', 'rsuscs', 'rsut', 'rsutcs','ch4global', 'co2mass', 'n2oglobal','mc',
                   'cl', 'cli', 'clw'],
        },
    #
    # Handling field shapes
    "excluded_spshapes": ["XYA-na","XYG-na", # GreenLand and Antarctic grids we do not want to produce
                          "na-A",            # RFMIP.OfflineRad : rld, rlu, rsd, rsu in table Efx ?????
                          #"Y-P19","Y-P39", "Y-A","Y-na" 
                          ],

    # Each DR RequestLink links a set of variables with a set of experiments
    # The requestLinks list is at http://clipc-services.ceda.ac.uk/dreq/index/requestLink.html 
    "excluded_request_links"  : [
        "RFMIP-AeroIrf" # 4 scattered days of historical, heavy output -> please rerun model for one day
        # for each day of this request_link 
    ],
    
    # Describe the branching scheme for experiments involved in some 'branchedYears type' tslice
    # (for details, see: http://clipc-services.ceda.ac.uk/dreq/index/Slice.html )
    # Just put the as key the common start year in child and as value the list of start years in parent for all members
    "branching" : {
        "CNRM-CM6-1"    : {"historical" : (1850, [ 1850, 1883, 1941, 1960, 1990, 2045, 2079, 2108, 2214, 2269 ]) },
        "CNRM-ESM2-1"   : {"historical" : (1850, [ 1850, 1883, 1941 ]) },
        "CNRM-CM6-1-HR" : {"historical" : (1850, [ 1850, 1883, 1941 ]) },
        },

    # dr2xml will drive vertical interpolation to pressure levels. This is a costly step if done
    # at every timestep
    "vertical_interpolation_sample_freq" : "1h",      # use Xios duration syntax
    "vertical_interpolation_operation"   : "instant", # LMD prefers 'average'

    # dr2xml allows for the lab to choose among various output grid policies  :
    #  - DR or None : always follow DR requirement
    #  - native     : never follow DR spec (always use native or close-to-native grid)
    #  - native+DR  : always produce on the union of grids
    #  - adhoc      : decide on each case, based on CMORvar attributes, using a 
    #                 lab-specific scheme implemented in a lab-provided Python 
    #                 function lab_adhoc_grid_policy in grids.py 
    "grid_policy" : "adhoc",
    # at the time of writing, CNRM choice is :
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
      "REG"    : {
          "surfex" : [ "gn", "C", "glat","50 km", "regional zone C "] ,
          #"surfex" : [ "gn", "" , "250 km", "native T127 reduced gaussian grid"] ,
          "trip"   : [ "gn", "",  "","50 km", "regular 1/2 deg lat-lon grid" ],
          "nemo"   : [ "gn", "",  "","8 km", "native ocean tri-polar grid" ],},
      "LR"    : {
          "surfex" : [ "gr", "complete", "glat","250 km", "data regridded to a T127 gaussian grid "+\
                     "(128x256 latlon) from a native atmosphere T127l reduced gaussian grid"] ,
          #"surfex" : [ "gn", "" , "250 km", "native T127 reduced gaussian grid"] ,
          "trip"   : [ "gn", "",  "","50 km", "regular 1/2 deg lat-lon grid" ],
          "nemo"   : [ "gn", "",  "","100 km", "native ocean tri-polar grid with 105 k ocean cells" ],},


      "HR"    : {
          "surfex" : [ "gr","complete", "glat","50 km", "data regridded to a 359 gaussian grid "+\
                     "(360x720 latlon) from a native atmosphere T359l reduced gaussian grid"] ,
          "trip"   : [ "gn", "", "", "50 km", "regular 1/2 deg lat-lon grid" ],
          "nemo"   : [ "gn", "", "", "25 km", "native ocean tri-polar grid with 1.47 M ocean cells" ],},
    },

    # Basic sampling timestep set in your field definition (used to feed metadata 'interval_operation')
    "sampling_timestep" : {
              "REG"   : { "surfex":900., "nemo":1800., "trip":1800. },
              "LR"    : { "surfex":900., "nemo":1800., "trip":1800. },
              "HR"    : { "surfex":900., "nemo":1800., "trip":1800. }, 
    },

    # CFMIP has an elaborated requirement for defining subhr frequency; by default, dr2xml uses 1 time step
    "CFsubhr_frequency" : "2ts",

    # dr2xml must know which Xios 'context' handle which 'realms'
    'realms_per_context' : { 'nemo'   : ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgChem', 'seaIce ocean'] ,
                             'surfex' : ['atmos', 'atmos atmosChem', 'atmosChem', 'aerosol', 'atmos land', 'land',
                                         'landIce land',  'aerosol','land landIce',  'landIce', ],
                             'trip'   : [],
                          }, 
    # Some variables, while belonging to a realm, may fall in another XIOS context than the 
    # context which hanldes that realm
    'orphan_variables' : { 'nemo'   : [''],
                           'surfex' : ['siconca'],
                           'trip'   : ['areacellr', 'dgw', 'drivw', 'qgwr', 'rivi', 'rivo', 'waterDpth', 'wtd', 'fwtd', 'fldf',
                                       'carbw','carbdis','carbin'],
                           },
    # Contact and more info pointers
    'references'    : "http://www.umr-cnrm.fr/",
    'info_url'      : "http://www.umr-cnrm.fr/",
    'contact'       : 'contact.aladin-cordex@meteo.fr',

    # What is the target maximum size of generated files, in number of float values
    "max_file_size_in_floats" : 4.*1.e+9 , # 5 Go
    "compression_level"  :  0,
    # Estimate of number of bytes per floating value, given the chosen compression level
    "bytes_per_float" : 2.4,

    # Tell which model use which grids resolutions set                      
    'grid_choice' : { "CNRM-ALADIN64" : "REG", "CNRM-RCSM6A" : "REG", "CNRM-CM6-1" : "LR", "CNRM-CM6-1-HR" : "HR", "CNRM-ESM2-1": "LR"  , "CNRM-ESM2-1-HR": "HR" },
           
    # Sizes for atm and oce grids (cf DR doc); Used for computing file split frequency
    "sizes"  : { "LR" : [294*362  , 75, 128*256, 91, 30, 14, 128],
                 "REG" : [294*362, 75, 128*180, 91, 30, 14, 128] ,
                 "HR" : [1442*1050, 75, 720*360, 91, 30, 14, 128] },

    # Tell which CMIP6 frequencies are unreachable for a single model run. Datafiles will
    # be labelled with dates consistent with content (but not with CMIP6 requirements).
    # Allowed values are only 'dec' and 'yr'
    "too_long_periods" : ["dec", "yr" ],

    # You may add a series of NetCDF attributes in all files for this simulation
    "non_standard_attributes" : { "arpege_minor_version" : "6.4.1" ,
                                  "nemo_gelato_commit" : "49095b3accd5d4c_6524fe19b00467a",
                                  "xios_commit" : "1442-shuffle",},

    # If your model has some axis which does not have all its attributes
    # as in DR, and you want dr2xml to fix that it, give here
    # the correspondence from model axis id to DR dim/grid id.
    # For label dimensions you should provide the list of labels, ordered
    # as in your model, as second element of a pair
    # Label-type axes will be processed even if not quoted
    # Scalar dimensions are not concerned by this feature
    'non_standard_axes' : {
        # Space dimensions - Arpege :
        'klev' : 'alevel' , 'klev_half' : 'alevel' ,
    
        # COSP
        'effectRadIc'  :'effectRadIc' , 'effectRadL'   :'effectRadL',
        'sza5'         :'sza5' ,
        'dbze'         :'dbze' ,
        
        # Land dimensions
        'soil_carbon_pools' :('soilpools', 'fast medium slow'),
        #'landUse'      :'landUse' ,
        'vegtype'      : ('vegtype','Bare_soil Rock Permanent_snow Temperate_broad-leaved_decidus Boreal_needleaf_evergreen Tropical_broad-leaved_evergreen C3_crop C4_crop Irrigated_crop C3_grass C4_grass Wetland Tropical_broad-leaved_decidus Temperate_broad-leaved_evergreen Temperate_needleaf_evergreen Boreal_broad-leaved_decidus Boreal_needleaf_decidus Tundra_grass Shrub') ,
        
        # Space dimensions - Nemo
        #'jmean' : 'latitude',
    
        # Ocean transects and basins
        'oline'        :'oline' ,
        'siline'       :'siline',
        'basin'        :('basin','global_ocean atlantic_arctic_ocean indian_pacific_ocean dummy dummy'),
    
    },

    # A smart workflow will allow you to extend a simulation during it
    # course and to complement the output files accordingly, by
    # managing the 'end date' part in filenames. You can then set next
    # setting to False. 
    'dr2xml_manages_enddate' : True ,

    # You may provide some variables already horizontally remapped 
    # to some grid (i.e. Xios domain) in external files. The varname in file 
    # must match the DR variable label. Used for fixed fields only
    # TBD - Not yet validated 
    'fx_from_file' : {
        "areacella" : { "complete" :
                        { "LR" : "areacella_complete_CMIP6_tl127",
                          "HR" : "areacella_complete_CMIP6_tl359",}},
                          "C" : { "REG" : "areacella_zoneC",}},

    # Should we allow for another type of duplicate vars : two vars
    # with same name in same table (usually with different
    # shapes). This applies to e.g. CMOR vars 'ua' and 'ua7h' in
    # 6hPlevPt. Default to False, because CMIP6 rules does not allow
    # to name output files differently in that case. If set to True,
    # you should also set 'use_cmorvar_label_in_filename' to True to
    # overcome the said rule
    'allow_duplicates_in_same_table' : False,

    # CMIP6 rule is that filenames includes the variable label, and
    # that this variable label is not the CMORvar label, but 'MIPvar'
    # label. This may lead to conflicts, e.g. for 'ua' and 'ua7h' in
    # table 6hPlevPt; next setting allows to avoid that, if set to True
    'use_cmorvar_label_in_filename' : False,

    # DR has sn attributes for MIP variables. They can be real,CF-compliant, standard_names or
    # pseudo_standard_names, i.e. not yet approved labels. Default is to use only CF ones
    'allow_pseudo_standard_names' : True,

    # For an extended printout of selected CMOR variables, grouped by variable label
    'print_stats_per_var_label' : False,

    # The ping file defines variable names, which are constructed using CMIP6 
    # "MIPvarnames" and a prefix which must be set here
    "ping_variables_prefix" : "CMIP6_",

    # In order to identify which xml files generates a problem, you can use this flag
    'debug_parsing' : True, # default to False !
    
    # A per-variable dict of comments valid for all simulations. They will be 
    # included in datafiles as field metadata
    'comments'     : {
        'zomsf_3bsn' :  "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.",
        'hfbasin' :     "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.",
        'hfbasinpmad' : "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.",
        'htovgyre  ' :  "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.",
        'htovovrt' :    "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.",
        'sltbasin' :    "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.",
        'sltnortha' :   "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.",
        'sltovgyre' :   "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.",
        'sltovovrt' :   "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.",

        'sivols' :      'The sector attribute is erroneous, this variable is indeed integrated over the southern hemisphere.',
        'siextents' :   'The sector attribute is erroneous, this variable is indeed integrated over the southern hemisphere.',
        'siareas' :     'The sector attribute is erroneous, this variable is indeed integrated over the southern hemisphere.',
        'snovols' :     'The sector attribute is erroneous, this variable is indeed integrated over the southern hemisphere.',

        'sivoln' :      'The sector attribute is erroneous, this variable is indeed integrated over the northern hemisphere.',
        'siextentn' :   'The sector attribute is erroneous, this variable is indeed integrated over the northern hemisphere.',
        'siarean' :     'The sector attribute is erroneous, this variable is indeed integrated over the northern hemisphere.',
        'snovoln' :     'The sector attribute is erroneous, this variable is indeed integrated over the northern hemisphere.',

        'drivw':	'CTRIP river water budget = (drivw+dgw)/dt - (rivi-rivo)*1000/areacellr - qgwr',
        'dgw':		'CTRIP river water budget = (drivw+dgw)/dt - (rivi-rivo)*1000/areacellr - qgwr',
        'rivi':		'CTRIP river grid-cell inflow considering upstream grdi-cell water fluxes and total runoff input (mrro) from ISBA',
        'dtes':		'ISBA land energy budget = (dtes+dtesn)/dt + hfmlt - hfdsl ; dt is given by netcdf attribute : interval_operation',
        'dtesn':	'ISBA land energy budget = (dtes+dtesn)/dt + hfmlt - hfdsl ; dt is given by netcdf attribute : interval_operation',
        
        'dslw':		'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'dcw':		'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'dsn':		'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        
        'sw':		'Surface floodplains water storage (e.g. Decharme et al. 2018)',
        'dsw':		'Change in floodplains water ; ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'eow':		'Liquid water evaporation from floodplains (e.g. Decharme et al. 2018)',
        
        'fldcapacity':	'100 * ISBA Field Capacity in m3/m3',
        'wilt':		'100 * ISBA Wilting Point in m3/m3',
        
        'snc':		'ISBA snow cover over bare ground comparable with stallite data (Psng in equation C1 in Decharme et al. 2016)',
        'prsnsn':	'In ISBA, prsnsn is always 1 because all snowfall falls onto snowpack',
        'dmlt':		'Region where always 12m correspond to none-permafrost areas',
        'tpf':		'Region where always 0m correspond to none-permafrost areas',
        'mrtws':	'ISBA-CTRIP total water storage (soil+canopy+snow+rivers+groundwater+floodplains; e.g. Decharme et al. 2018)',
        
        #'rld' : 'nothing special about this variable'
        },

    # For an extended printout of selected CMOR variables, grouped by variable label
    'print_stats_per_var_label' : True,

    # When using select='no', Xios may enter an endless loop, which is solved if next setting is False
    'allow_tos_3hr_1deg' : True,
    # When not using CMIP6_CV
    'source' : 'CORDEX',
    # Select the attributes to write
    'print_variables' : ['activity_id','description','comment','contact','Conventions','creation_date','data_specs_version','dr2xml_version','experiment_id','EXPID','external_variables','frequency','grid','grid_label','history','institution','institute_id','nominal_resolution','product','project_id','model_id','rcm_version_id','realization_index','realm','references','table_id','title','tracking_id','variable_id','xios_commit','standard_name','long_name','units','cell_methods','cell_measures','driving_experiment','driving_experiment_name','driving_model_id','driving_model_ensemble_member','CORDEX_domain','grid_mapping','Lambert_conformal_longitude_of_central_meridian','Lambert_conformal_standard_parallel','Lambert_conformal_latitude_of_projection_origin'],

}

