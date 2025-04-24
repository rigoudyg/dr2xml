#!/usr/bin/python
# -*- coding: utf-8 -*-


lab_and_model_settings = {
    'data_request_used': 'CMIP7',
    'data_request_path': '/home/rigoudyg/dev/data_request/CMIP7_DReq_Software/data_request_api',
    'data_request_content_version': 'v1.2',
    'institution_id': "CNRM-CERFACS",
    'project': "ping",
    # 'mips' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
    #                  'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
    # If you want to get comprehensive ping files; use :
    'mips': {"CERESMIP", "PAMIP", "SIMIP", "OMIP", "SOFIAMIP", "LMIP", "RFMIP", "AerChemMIP2", "GeoMIP", "TIPMIP",
             "DAMIP", "PMIP", "FAFMIP", "DCPP", "CDRMIP", "NAHosMIP", "ISMIP7", "CMIP", "ScenarioMIP", "HighResMIP",
             "LUMIP", "Other", "VolMIP", "HT-MIP/VolMIP", "CORDEX", "CFMIP", "C4MIP", "WhatIfMIP", "VIACSAB", "RAMIP",
             "FireMIP", "IRRMIP", "LongRunMIP", "MISOMIP2", "FishMIP", "ISIMIP"},
    'max_priority': 3,
    'tierMax': 3,
    # Each XIOS  context does adress a number of realms
    'realms_per_context': {'nemo': ['ocean', 'ocnBgchem', 'seaIce'],
                           'arpsfx': ['aerosol', 'atmos', 'atmosChem', 'land', 'landIce'],
                           },
    "ping_variables_prefix": "CMIP7_",
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