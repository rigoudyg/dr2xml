#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create ping files based on lab choices

from __future__ import print_function, division, absolute_import, unicode_literals

import os.path
import shutil
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dr2xml import create_ping_files

# Select your laboratory among: 'cnrm', 'cerfacs', 'ipsl'
lab = 'cnrm'

# Lab settings

if lab in ['cnrm', 'cerfacs']:
    # This dictionnary should be the same as the one used for creating file_defs.
    # Here , we quoted only those entries useful for creating ping files
    settings = {
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

if lab in ['cerfacs', ]:
    # settings["mips"]={'HighResMIP','DCPP'}
    settings["listof_home_vars"] = "./input_labs/cerfacs/home_vars/listof_primavera_extra_vars.txt"
    settings["path_extra_tables"] = "./input_labs/cerfacs/extra_Tables"

if lab in ['ipsl', ]:
    # This dictionnary should be the same as the one used for creating file_defs.
    # Here , we quoted only those entries useful for creating ping files
    settings = {
        'institution_id': "IPSL",
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
        'realms_per_context': {
            'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'],
            'lmdz': ['atmos', 'atmos land'],
            'orchidee': ['land', 'landIce land', 'land landIce', 'landIce'],
        },
        "ping_variables_prefix": "CMIP6_",
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

# Read excluded variables list - you may skip that

l = []
if settings["excluded_vars"] is None and settings["excluded_vars_file"] is not None:
    with open(settings["excluded_vars_file"], 'r') as fv:
        varlines = fv.readlines()
    for line in varlines:
        fields = line.split()
        if len(fields) > 0:
            first = fields[0]
            if first[0] != '#':
                l.append(first)
settings["excluded_vars"] = l

# For getting a comprehensive ping file, one can (re)set the excluded_var list to an empty list

settings["excluded_vars"] = []

# When using function create_ping_files with argument exact=False, each ping file will adress all variables which
# realm includes or is included in one of the strings in a realms set  <br><br> e.g for set ['ocean','seaIce'],
# ping file 'ping_ocean_seaIce.xml' will includes variables which realm is either 'ocean' or 'seaIce' or 'ocean seaIce'

# Create various ping files for various sets of realms

# In/Out directory
my_dir = "output_labs/" + lab + "/"
if os.path.exists(my_dir):
    shutil.rmtree(my_dir)
os.makedirs(my_dir)

# Generate one ping file per context:
for my_context in settings["realms_per_context"].keys():
    print("=== CREATING PINGFILE FOR CONTEXT", my_context)
    create_ping_files(context=my_context, lset=settings, sset=dict(), path_special=settings["path_special_defs"],
                      comments=True, exact=False, dummy=True,
                      filename=my_dir + 'ping_' + my_context + '.xml', dummy_with_shape=True)

# ! head -n 5 output_sample/ping_nemo.xml

# Generate one ping file per realm:
for my_context in settings["realms_per_context"].keys():
    create_ping_files(context=my_context, lset=settings, sset=dict(), path_special=settings["path_special_defs"],
                      comments=True, exact=False, dummy=True,
                      filename=my_dir + 'ping_' + my_context + '_%s.xml', dummy_with_shape=True, by_realm=True)
