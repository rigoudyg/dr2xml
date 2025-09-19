#!/usr/bin/python
# -*- coding: utf-8 -*-


lab_and_model_settings = {
    'data_request_used': 'CMIP7',
    'data_request_content_version': 'test',
    'institution_id': "IPSL",
    'laboratory_used': "ipsl",
    'project': "ping",
    # 'mips' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
    #                  'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
    # If you want to get comprehensive ping files; use :
    'mips': {},
    'max_priority': 3,
    'tierMax': 3,
    # Each XIOS  context does adress a number of realms
    'realms_per_context': {'LMDZ': ['atmos', 'land', 'landIce', 'atmosChem', 'aerosol'],
                           'orchidee': ['land', 'landIce'],
                           'nemo': ['seaIce', 'ocean', 'ocnBgchem'],
                           },
    "ping_variables_prefix": "CMIP7_",
    # We account for a file listing the variables which the lab does not want to produce
    # Format : MIP varname as first column, comment lines begin with '#'
    "excluded_vars_file": [],
    "excluded_vars": [],
    # We account for a list of variables which the lab wants to produce in some cases
    "listof_home_vars": None,
    "path_extra_tables": None,
    # mpmoine_correction: Path for special XIOS defs files
    "path_special_defs": None
}