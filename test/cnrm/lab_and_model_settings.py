# -*- coding: iso-8859-15 -*-


lab_and_model_settings = {
    'institution_id': "CNRM-CERFACS",  # institution full description will be read in CMIP6_CV
    'source_types': {"CNRM-CM6-1": "AOGCM", "CNRM-CM6-1-HR": "AOGCM",
                     "CNRM-ESM2-1": "ESM", "CNRM-ESM2-1-HR": "ESM"},

    "source_id": "CNRM-CM6-1",
    "source": "CNRM-CM6-1",  # Useful only if CMIP6_CV is not up-to-date for the source_id
    'references': "ref",
    'info_url': "http://www.umr-cnrm.fr/cmip6/",
    'contact': 'contact.cmip@cnrm.fr',
    'mips_short': {'C4MIP', 'SIMIP', 'OMIP', 'CFMIP', 'RFMIP'},
    'mips': {'AerChemMIP', 'C4MIP', 'CFMIP', 'DAMIP', 'FAFMIP', 'GeoMIP', 'GMMIP', 'ISMIP6', \
             'LS3MIP', 'LUMIP', 'OMIP', 'PMIP', 'RFMIP', 'ScenarioMIP', 'CORDEX', 'SIMIP', 'HighResMIP'},
    'max_priority': 3,
    'tierMax': 3,
    'ping_variables_prefix': "CMIP6_",
    # excluded_vars_file="./inputs/non_published_variables.txt"
    # exlcude pfull and phalf because we have a pressure based hydrid coordinate
    "excluded_vars": ['pfull', 'phalf', \
                      # "clcalipso","clcalipso2","clhcalipso","clcalipsoice","clcalipsoliq", \
                      # "cllcalipso","clmcalipso","cltcalipso",\
                      # "cfadLidarsr532","cfadDbze94","cfadLidarsr532","clisccp","cltisccp",\
                      # "climodis","clwmodis","jpdftaureicemodis","cltmodis","clmisr","parasolRefl"\
                      ],
    # --- mpmoine_next_modif: ignore some spatial shapes
    # mpmoine_note: grilles Groenland, Antarctic et les profils en Sites (pas encore codé dans dr2xml)
    # "excluded_spshapes": ["XYA-na","XYG-na","S-na","S-AH","S-A","na-A"],
    "excluded_spshapes": ["XYA-na", "XYG-na", "na-A", "Y-P19", "Y-P39", "Y-A", "Y-na"],
    "excluded_tables": ["Oclim", "E1hrClimMon"],  # Clims are not handled by Xios yet
    "excluded_request_links": ["CFsubhr"],  # request native grid, numerous 2D fields and even 3D fields

    # "listof_home_vars":rootpath+"dr2xml/config_utest/utest020_listof_home_vars.txt",
    "listof_home_vars": None,
    'realms_per_context': {'nem': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'],
                           'sfx': ['atmos', 'atmos atmosChem', 'aerosol', 'atmos land', 'land',
                                   'landIce land', 'aerosol land', 'land landIce', 'landIce', ],
                           # 'trip'   : [],
                           },
    'orphan_variables': {'nem': [''],
                         'sfx': [],
                         # 'trip'   : ['dgw', 'drivw', 'cfCLandToOcean', 'qgwr', 'rivi', 'rivo', 'waterDpth', 'wtd'],
                         },
    'vars_OK': dict(),
    # A per-variable dict of comments valid for all simulations
    'comments': {},
    # Sizes for atm and oce grids (cf DR doc)
    # actual_sizes=[292*362,75,128*256,91,30,14,128]
    # actual_sizes=[1442*1021,75,720*360,91,30,14,128]
    "sizes": [292 * 362, 75, 128 * 256, 91, 30, 14, 128],

    # What is the maximum size of generated files, in number of float values
    "max_file_size_in_floats": 500. * 1.e+6,

    # grid_policy among None, DR, native, native+DR, adhoc- see docin grids.py
    "grid_policy": "DR",

    # Resolutions
    "grids": {
        "LR": {
            "sfx": ["gr", "complete", "250 km", "data regridded to a T127 gaussian grid " + \
                    "(128x256 latlon) from a native atmosphere T127l reduced gaussian grid"],
            # "sfx" : [ "gn", "" , "250 km", "native T127 reduced gaussian grid"] ,
            "trip": ["gn", "", "50 km", "regular 1/2° lat-lon grid"],
            "nem": ["gn", "", "100 km", "native ocean tri-polar grid with 105 k ocean cells"], },

        "HR": {
            "sfx": ["gr", "complete", "50 km", "data regridded to a 359 gaussian grid " + \
                    "(180x360 latlon) from a native atmosphere T359l reduced gaussian grid"],
            "trip": ["gn", "", "50 km", "regular 1/2° lat-lon grid"],
            "nem": ["gn", "", "25 km", "native ocean tri-polar grid with 1.47 M ocean cells"], },
    },

    'grid_choice': {"CNRM-CM6-1": "LR", "CNRM-CM6-1-HR": "HR", "CNRM-ESM2-1": "LR", "CNRM-ESM2-1-HR": "HR"},
    #
    # Component Models Time steps (s)
    "model_timestep": {"sfx": 900., "nem": 900., "trip": 1800.},

    # --- Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR
    "use_union_zoom": False,

    #
    "vertical_interpolation_sample_freq": "3h",

    # The CMIP6 frequencies that are unreachable for a single model run. Datafiles will
    # be labelled with dates consistent with content (but not with CMIP6 requirements).
    # Allowed values are only 'dec' and 'yr'
    "too_long_periods": ["dec", "yr"]

}
