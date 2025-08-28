#!/usr/bin/python
# -*- coding: utf-8 -*-


lab_and_model_settings = {
    'institution_id': "CNRM-CERFACS",
    'project': "ping",
    # 'mips' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
    #                  'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
    # If you want to get comprehensive ping files; use :
    'mips': {"CMIP6", "AerChemMIP", "C4MIP", "CFMIP", "DAMIP", "DCPP", "FAFMIP", "GeoMIP", "GMMIP",
             "HighResMIP", "ISMIP6", "LS3MIP", "LUMIP", "OMIP", "PDRMIP", "PMIP", "RFMIP", "ScenarioMIP",
             "SolarMIP", "VolMIP", "CORDEX", "DynVar", "SIMIP", "VIACSAB", "SPECS", "CCMI", "CMIP5",
             "CMIP", "DECK"},
    'max_priority': 3,
    'tierMax': 3,
    # Each XIOS  context does adress a number of realms
    'realms_per_context': {'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'],
                           'arpsfx': ['atmos', 'atmos atmosChem', 'aerosol', 'atmos land', 'land',
                                      'landIce land', 'aerosol land', 'land landIce', 'landIce', ],
                           },
    "ping_variables_prefix": "CMIP6_",
    # We account for a file listing the variables which the lab does not want to produce
    # Format : MIP varname as first column, comment lines begin with '#'
    # "excluded_vars_file":"/cnrm/est/USERS/senesi/public/CMIP6/data_request/cnrm/excluded_vars.txt",
    "excluded_vars_file": [],
    "excluded_vars": [],
    # We account for a list of variables which the lab wants to produce in some cases
    "listof_home_vars": None,
    # "listof_home_vars": None,
    "path_extra_tables": None,
    # mpmoine_correction: Path for special XIOS defs files
    "path_special_defs": "./input/special_defs"
}