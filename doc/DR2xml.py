# coding: utf-8

# # An example for generating the XIOS file_def for a given lab, model, experiment, year and XIOS context

# In[ ]:

# --- Select your laboratory: 'cnrm', 'cerfacs' or'ipsl'
lab = 'cerfacs'
# --- Select your model type: 'GCM' or 'ESM'
mod = 'GCM'
# --- Select your molde resolution: 'LR' or 'HR'
resol = 'LR'

# ## 1. Define the settings specific to the laboratory and the model

# In[ ]:

if lab == 'cnrm' or lab == 'cerfacs':
    #
    # --- Sizes of oce and atm grids ['nho','nlo','nha','nla','nlas','nls','nh1'] (cf DR doc)
    if resol == "LR":
        actual_sizes = [292 * 362, 75, 128 * 256, 91, 30, 14, 128]
    if resol == "HR":
        actual_sizes = [1442 * 1021, 75, 720 * 360, 91, 30, 14, 128]
    # --- Model name like declared to the CMIP6 WIP panel
    if mod == 'GCM' and resol == 'LR':
        actual_source_id = "CNRM-CM6-1"
    if mod == 'GCM' and resol == 'HR':
        actual_source_id = "CNRM-CM6-1-HR"
    if mod == 'ESM' and resol == 'LR':
        actual_source_id = "CNRM-ESM2-1"
    if mod == 'ESM' and resol == 'HR':
        actual_source_id = "CNRM-ESM2-1-HR"
    #
    lab_and_model_settings = {
        #
        "institution_id": "CNRM-CERFACS",
        # "institution": "CNRM, blabla...; CERFACS, blabla...", # institution should be read in CMIP6_CV, if up-to-date
        #
        # --- entry 'source_types' allows to describe, using CMIP6 CV, the various model configurations
        # --- for the lab; This can be superseded by an entry 'source_type' either just below or in dict
        # --- for simulation settings (further below)
        "source_types": {"CNRM-CM6-1": "AOGCM", "CNRM-CM6-1-HR": "AOGCM",
                         "CNRM-ESM2-1": "ESM", "CNRM-ESM2-1-HR": "ESM"},
        #
        "source_id": actual_source_id,
        # "source"         : "CNRM-CM6-1 blabla...", # Useful only if CMIP6_CV is not up-to-date for the source_id
        # --- You may override here the source_type value deduced from source_id and sources_type
        # "source_type" : "AER"
        #
        # --- references & contact
        # "references"    :  "Blabla...", # A character string containing a list of published or web-based
        # references that describe the data or the methods used to produce it.
        # Typically, the user should provide references describing the model
        # formulation here
        "info_url": "http://www.umr-cnrm.fr/cmip6/",
        "contact": 'contact.cmip@cnrm.fr',
        #
        # --- We account for the list of MIPS in which the lab takes part.
        # --- Note : a MIPs set limited to {'C4MIP'} leads to a number of tables and
        # --- variables which is manageable for eye inspection
        "mips_all": {'AerChemMIP', 'C4MIP', 'CFMIP', 'DAMIP', 'FAFMIP', 'GeoMIP', 'GMMIP', 'ISMIP6',
                     'LS3MIP', 'LUMIP', 'OMIP', 'PMIP', 'RFMIP', 'ScenarioMIP', 'CORDEX', 'SIMIP'},
        "mips": {'C4MIP', 'SIMIP', 'OMIP', 'CFMIP', 'RFMIP'},
        #
        # --- Max variable priority level to be output
        "max_priority": 1,
        "tierMax": 3,
        #
        # --- The ping file defines variable names, which are constructed using CMIP6 "MIPvarnames"
        # --- and a prefix which must be set here, and can be the empty string :
        "ping_variables_prefix": "CMIP6_",
        #
        # --- mpmoine_amelioration: pour ecrire un ts_prefix
        # 'output_path' : "@IOXDIR@/%file_name%",
        'output_path': "@IOXDIR@/",
        #
        # --- We account for a list of variables which the lab does not want to produce ,
        # --- oragnized by realms
        # "excluded_vars_file":"./input/excluded_vars/non_published_variables.txt",
        # mpmoine_note: exclusion des variables Cloud Simulator tant que pas activé
        "excluded_vars": ["clcalipso", "clcalipso2", "clhcalipso", "clcalipsoice", "clcalipsoliq", "cllcalipso",
                          "clmcalipso", "cltcalipso", "cfadLidarsr532", "cfadDbze94", "cfadLidarsr532", "clisccp",
                          "cltisccp", "climodis", "clwmodis", "jpdftaureicemodis", "cltmodis", "clmisr", "parasolRefl"],
        #
        # --- mpmoine_next_modif: ignore some spatial shapes
        # mpmoine_note: grilles Groenland, Antarctic et les profils en Sites (pas encore codé dans dr2xml)
        "excluded_spshapes": ["XYA-na", "XYG-na", "S-na", "S-AH", "S-A", "na-A"],
        #
        # --- We account for a list of variables which the lab wants to produce in some cases
        "listof_home_vars": None,
        #
        # --- mpmoine_last_modif: Path for extra Tables
        "path_extra_tables": None,
        #
        # --- mpmoine_correction: Path for natives XIOS xml files to parse
        "path_to_parse": "./input_labs/cnrm/to_parse/for_arpege_grid",
        #
        # Each XIOS  context does adress a number of realms
        "realms_per_context": {'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'],
                               'arpsfx': ['atmos', 'atmos atmosChem', 'aerosol', 'atmos land', 'land',
                                          'landIce land', 'aerosol land', 'land landIce', 'landIce', ],
                               },
        #
        # --- Some variables, while belonging to a realm, may fall in another XIOS context than the
        # --- context which handles that realm
        "orphan_variables": {'nemo': ['dummy_variable_for_illustration_purpose'],
                             'arpsfx': [],
                             },
        "vars_OK": dict(),
        #
        # --- A per-variable dict of comments valid for all simulations
        "comments": {
            'tas': 'nothing special about tas'
        },
        #
        # --- Sizes of oce and atm grids ['nho','nlo','nha','nla','nlas','nls','nh1'] (cf DR doc)
        "sizes": actual_sizes,
        #
        # --- What is the maximum size of generated files, in number of float values
        "max_file_size_in_floats": 500. * 1.e+6,
        #
        # --- grid_policy among None, DR, native, native+DR, adhoc- see docin grids.py
        "grid_policy": "adhoc",
        #
        # --- Grids : CMIP6 name, name_of_target_domain, CMIP6-std resolution, and description
        "grids": {
            "LR": {
                "arpsfx": ["gr", "complete", "250 km",
                           "data regridded to a T127 gaussian grid (128x256 latlon) "
                           "from a native atmosphere T127l reduced gaussian grid"],
                "nemo": ["gn", "", "100 km", "native ocean tri-polar grid with 105 k ocean cells"], },
            "HR": {
                "arpsfx": ["gr", "completeHR", "50 km",
                           "data regridded to a 359 gaussian grid (180x360 latlon) "
                           "from a native atmosphere T359l reduced gaussian grid"],
                "nemo": ["gn", "", "25 km", "native ocean tri-polar grid with 1.47 M ocean cells"], },
        },
        "grid_choice": {"CNRM-CM6-1": "LR", "CNRM-CM6-1-HR": "HR", "CNRM-ESM2-1": "LR", "CNRM-ESM2-1-HR": "HR"},
        #
        # --- mpmpoine_next_modif: Model component Time steps (min)
        "model_timestep": {"arpsfx": 900., "nemo": 900.},
        #
        # --- mpmoine_amelioration: booleen pour activer ou non l'usage des union/zoom
        # --- Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR
        "use_union_zoom": False
        #
    }

# In[ ]:

if lab == 'cerfacs':
    changes = {
        "mips": 'HighResMIP',
        "max_priority": 2,
        "listof_home_vars": "./input_labs/cerfacs/home_vars/listof_primavera_extra_vars.txt",
        # "listof_home_vars"    : "./input_labs/cerfacs/home_vars/listof_test_extra_vars.txt",
        "path_extra_tables": "./input_labs/cerfacs/extra_Tables",
        # "path_to_parse"       : "./input_labs/cerfacs/to_parse/for_arpege_grid_dr2xml_"+resol+"_STMARTIN_EXCLUPLEV",
        "path_to_parse": "./input_labs/cerfacs/to_parse/for_arpege_grid_dr2xml_" + resol + "_STMARTIN",
        # "path_to_parse"       : "./input_labs/cerfacs/to_parse/for_arpege_grid_dr2xml_"+resol+"_TEST",
        # "path_to_parse"       : "./input_labs/cerfacs/to_parse/for_toy_grid_"+resol,
        # "grids" : {
        #  "LR"    : {
        #    "arpsfx" : ["gn","reduced-gaussian_LR" ,"250 km", "native atmosphere T127l reduced gaussian grid"] ,
        #      "nemo" : ["gn", ""        , "100 km" , "native ocean tri-polar grid ORCA1 with 105 k ocean cells"],},
        #  "HR"    : {
        #    "arpsfx" : ["gn","reduced-gaussian_HR", "50 km", "native atmosphere T359l reduced gaussian grid"] ,
        #      "nemo" : ["gn", ""         , "25 km" , "native ocean tri-polar grid ORCA025 with 1.47 M ocean cells"],},
        # },
        'comments': {},
        'contact': 'contact.cmip6@cerfacs.fr',
        "excluded_spshapes": ["XYA-na", "XYG-na", "S-na", "S-AH", "S-A", "na-A", "Y-P39"]
        # "Y-P19","Y-P39","XY-P19","XY-P27","XY-P3","XY-P4","XY-P7","XY-P7T","XY-P8"]
    }
    lab_and_model_settings.update(changes)

# In[ ]:

if lab == 'ipsl':
    lab_and_model_settings = {
        #
        "institution_id": "IPSL",
        # "institution": "IPSL, blabla...", # institution should be read in CMIP6_CV, if up-to-date
        "source_id": "IPSL-CM6-1",
        # "source"         : "IPSL-CM6-1 blabla...", # Useful only if CMIP6_CV is not up-to-date for the source_id
        # --- You may override here the source_type value deduced from source_id and sources_type
        # "source_type" : "AER"
        #
        # --- The description of lab models, in CMIP6 CV wording
        "source_types": {"IPSL-CM6-1": "AOGCM", "IPSL-CM6-1-HR": "AOGCM",
                         "IPSL-ESM2-1": "ESM", "IPSL-ESM2-1-HR": "ESM"},
        "source": "IPSL-CM6-1",  # Useful only if CMIP6_CV is not up to date
        #
        # --- references & contact
        # "references"    :  "Blabla...", # A character string containing a list of published or web-based
        # references that describe the data or the methods used to produce it.
        # Typically, the user should provide references describing the model
        # formulation here
        "info_url": "http://www.blabla",
        "contact": 'blabla@blabla.fr',
        #
        # --- We account for the list of MIPS in which the lab takes part.
        # --- Note : a MIPs set limited to {'C4MIP'} leads to a number of tables and
        # --- variables which is manageable for eye inspection
        "mips_for_test": {'C4MIP', 'SIMIP', 'OMIP', 'CFMIP', 'RFMIP'},
        "mips": {'AerChemMIP', 'C4MIP', 'CFMIP', 'DAMIP', 'FAFMIP', 'GeoMIP', 'GMMIP', 'ISMIP6', 'LS3MIP', 'LUMIP',
                 'OMIP', 'PMIP', 'RFMIP', 'ScenarioMIP', 'CORDEX', 'SIMIP'},
        #
        # --- Max variable priority level to be output
        'max_priority': 1,
        'tierMax': 1,
        #
        # --- The ping file defines variable names, which are constructed using CMIP6 "MIPvarnames"
        # --- and a prefix which must be set here, and can be the empty string :
        "ping_variables_prefix": "CMIP6_",
        #
        # --- mpmoine_amelioration: pour ecrire un ts_prefix
        'output_path': None,
        #
        # --- We account for a list of variables which the lab does not want to produce ,
        # --- Names must match DR MIPvarnames (and **NOT** CF standard_names)
        "excluded_vars_file": None,
        # mpmoine_note: exclusion des variables Cloud Simulator tant que pas activé
        "excluded_vars": ["clcalipso", "clcalipso2", "clhcalipso", "clcalipsoice", "clcalipsoliq", "cllcalipso",
                          "clmcalipso", "cltcalipso", "cfadLidarsr532", "cfadDbze94", "cfadLidarsr532", "clisccp",
                          "cltisccp", "climodis", "clwmodis", "jpdftaureicemodis", "cltmodis", "clmisr", "parasolRefl"],
        # --- mpmoine_next_modif: ignore some spatial shapes
        # mpmoine_note: grilles Groenland, Antarctic et les profils en Sites (pas encore codé dans dr2xml)
        "excluded_spshapes": ["XYA-na", "XYG-na", "S-na", "S-AH", "S-A", "na-A"],
        #
        # --- We account for a list of variables which the lab wants to produce in some cases
        "listof_home_vars": None,
        #
        # --- mpmoine_last_modif: Path for extra Tables
        "path_extra_tables": None,
        #
        # --- mpmoine_correction: Path for natives XIOS xml files to parse
        "path_to_parse": "./input_labs/ipsl/to_parse",
        #
        # --- Each XIOS  context does adress a number of realms
        "realms_per_context": {
            'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'],
            'lmdz': ['atmos', 'atmos land'],
            'orchidee': ['land', 'landIce land', 'land landIce', 'landIce'],
        },
        #
        # --- Some variables, while belonging to a realm, may fall in another XIOS context than the
        # --- context which hanldes that realm
        "orphan_variables": {
            'nemo': [],
            'lmdz': [],
            'orchidee': [],
        },
        "vars_OK": dict(),
        #
        # --- A per-variable dict of comments valid for all simulations
        "comments": {
            'tas': 'nothing special about tas'
        },
        #
        # --- Sizes for atm and oce grids ['nho','nlo','nha','nla','nlas','nls','nh1'] (cf DR doc)
        "sizes": [259200, 60, 64800, 40, 20, 5, 100],
        #
        # --- What is the maximum size of generated files, in number of float values
        "max_file_size_in_floats": 500. * 1.e+6,
        #
        # --- Grids : CMIP6 name, name_of_target_domain, CMIP6-std resolution, and description
        "grids": {
            "LR": {
                "lmdz": ["gr", "", "??? km", "LMDZ grid"],
                "nemo": ["gn", "", "100 km", "native ocean tri-polar grid with 105 k ocean cells"],
                "orchidee": ["gr", "", "??? km", "LMDZ grid"], },
        },
        "grid_choice": {"IPSL-CM6-1": "LR", "IPSL-CM6-1-HR": "HR",
                        "IPSL-ESM2-1": "LR", "IPSL-ESM2-1-HR": "HR"},
        #
        # --- mpmpoine_next_modif: Model component Time steps (min)
        "model_timestep": {"nemo": 60., "lmdz": 60., "orchidee": 60.},
        #
        # --- mpmoine_amelioration: booleen pour activer ou non l'usage des union/zoom
        # --- Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR
        "use_union_zoom": False
        #
    }

# ## 2. Define the settings for the processed simulation

# In[ ]:

simulation_settings = {
    # --- Dictionnary describing the necessary attributes for a given simulation
    # --- Warning : some lines are commented out in this example but should be
    # --- un-commented in some cases. See comments
    #
    "experiment_id": "historical",
    #
    # "contact"        : "", set it only if it is specific to the simualtion
    "project": "CMIP6",  # CMIP6 is the default
    #
    # "source_type"    : "ESM" # If source_type is special only for this experiment (e.g. : AMIP)
    # (i.e. not the same as in lab_and_model settings), you may tell that here
    #
    # --- MIP specifying the experiment. For historical, it is CMIP6 itself
    # --- In a few cases it may be appropriate to include multiple activities in the activity_id
    # --- (with multiple activities allowed, separated by single spaces).
    # --- An example of this is “LUMIP AerChemMIP” for one of the land-use change experiments.
    "activity_id": "CMIP",  # examples : “PMIP”, “LS3MIP LUMIP”; default is "CMIP"

    # --- It is recommended that some description be included to help identify major differences among variants,
    # --- but care should be taken to record correct information.  Prudence dictates that this attribute includes
    # --- a warning along the following lines:  “Information provided by this attribute may in some cases be flawed.#
    # --- Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute.”
    "variant_info": "Start date chosen so that variant r1i1p1f1 has the better fit with Krakatoa impact on tos",
    #
    # --- 'variant_label' attribute is built gluing <r><i><p><f> values
    "realization_index": 1,  # Value may be omitted if = 1
    "initialization_index": 1,  # Value may be omitted if = 1
    "physics_index": 1,  # Value may be omitted if = 1
    "forcing_index": 1,  # Value may be omitted if = 1
    #
    # --- All about the parent experiment and branching scheme
    "parent_experiment_id": "piControl",
    # Optional, default is False. Omit it (or set it to 'no parent') if not applicable
    # Others parent and branch attributes will be disregarded if omitted or set to 'no parent'
    # but will be required id parent_experiment_id is defined.
    #
    "parent_mip_era": 'CMIP5',
    # Optional, default is 'mip_era'. Only in special cases (e.g. PMIP warm start from CMIP5/PMIP3 experiment)
    "parent_activity_id": 'CMIP',  # Optional, default is 'activity_id'. Only in special cases, defaults to CMIP
    "parent_source_id": 'CNRM-CM5.1',
    # Optional, default is 'source_id'. Only in special cases, where parent model is not the same model
    # "parent_time_ref_year" : '1950'       # Optional, default is '1850'. Is used to build 'parent_time_units'
    # "parent_time_units"    : "days sice 1950-31-12 00:00:00"
    #                                                   # Default is 'days since <parent_time_ref_year>-01-01 00:00:00'.
    #                                                   # Default is ???. In case it is not the same as child time units
    # "parent_variant_label" : "r3i1p1f2"   # Optional, default is 'variant label'. Other cases should be expceptional
    "branch_method": "standard",  # Optional, default is 'standard'. Meaning ~ "select a start date"
    "branch_time_in_parent": "365.0D0",  # Optional, default is False. A double precision value, in parent time units
    "branch_time_in_child": "0.0D0",  # Optional, default is False. a double precision value, in child time units
    #
    # --- mpmoine_cmor_update: CMOR3.2.3 impose 'none' comme default values pour sub_experiment_id et sub_experiment
    "sub_experiment_id": "none",  # Optional, default is 'none'; example : s1960.
    "sub_experiment": "none",  # Optional, default in 'none'
    "history": "none",  # Used when a simulation is re-run, an output file is modified ....
    #
    # --- A per-variable dict of comments which are specific to this simulation. It will replace
    # --- the all-simulation comment present in lab_and_model_settings
    'comments': {
        'tas': 'tas diagnostic uses a special scheme in this simulation',
    }
}

# In[ ]:

if lab == 'cerfacs':
    changes = {
        "experiment_id": "Forced-Atmos-Land",
        "source_type": "AGCM",  # If source_type is special only for this experiment (e.g. : AMIP)
        # (i.e. not the same as in lab_and_model settings), you may tell that here
        "activity_id": "HighResMIP",  # examples : “PMIP”, “LS3MIP LUMIP”; defaults is "CMIP"
        "realization_index": 1,  # Value may be omitted if = 1
        "initialization_index": 1,  # Value may be omitted if = 1
        "physics_index": 1,  # Value may be omitted if = 1
        "forcing_index": 1,  # Value may be omitted if = 1
        "parent_experiment_id": "no parent",
        # Optional, default is False. Omit this setting (or set it to 'no parent') if not applicable
        # Others parent and branch attributes will be disregarded if omitted or set to 'no parent'
        # but will be required id parent_experiment_id is defined.
        # "variant_info"         : "Petite variation en Re mineur",
        "variant_info": "none",
        'comments': {}
    }
    simulation_settings.update(changes)

# In[ ]:

# --- Path to local copy of CMIP6 CVs, which you can get from https://github.com/WCRP-CMIP/CMIP6_CVs
if lab == 'cnrm':
    my_cvspath = "/cnrm/est/USERS/senesi/public/CMIP6/data_request/CMIP6_CVs/"
elif lab == 'cerfacs':
    my_cvspath = "/Users/moine/Codes/MyDevel_Codes/CMIP6_DATA_SUITE/CMIP6_CVs/"
elif lab == 'ipsl':
    my_cvspath = "/ccc/cont003/home/gencmip6/p86caub/CMIP6_DR_DR2XML/CMIP6_CVs/"
my_cvspath = "/Users/moine/Codes/MyDevel_Codes/CMIP6_DATA_SUITE/CMIP6_CVs/"

# ## 3. Generate a first file-def with a dummy ping-file, including dummies

# In[ ]:

note = "VERSIONS:"
print note
print "-" * len(note)

from dr2xml import generate_file_defs

# In[ ]:

note = "\nLAB AND MODEL SETTINGS:"
print note
print "-" * len(note)

for k, v in lab_and_model_settings.items():
    print "* ", k, "=", v

note = "\nSIMULATION SETTINGS:"
print note
print "-" * len(note)

# Path to local copy of CMIP6 CVs, which you can get from https://github.com/WCRP-CMIP/CMIP6_CVs
# my_cvspath="/Users/moine/Codes/MyDevel_Codes/CMIP6_DATA_SUITE/CMIP6_CVs/"
my_cvspath = "~/dev/CMIP6_CVs"

for k, v in simulation_settings.items():
    print "* ", k, "=", v

# In[ ]:

# In/Out directory
my_dir = "output_labs/" + lab + "/"

# In[ ]:

# help(generate_file_defs)


# In[ ]:

if False:
    # for my_context in lab_and_model_settings["realms_per_context"].keys():
    for my_context in ["arpsfx"]:
        generate_file_defs(lab_and_model_settings, simulation_settings, year=2000, context=my_context,
                           pingfile=my_dir + "ping_" + my_context + ".xml", printout=True,
                           cvs_path=my_cvspath, dummies='include', dirname=my_dir)

# ## 4. After some edit in ping files, which does not discard every 'dummy' entries
#

# In[ ]:

note = "VERSIONS:"
print note
print "-" * len(note)

from dr2xml import generate_file_defs

# In[ ]:

note = "\nLAB AND MODEL SETTINGS:"
print note
print "-" * len(note)

for k, v in lab_and_model_settings.items():
    print "* ", k, "=", v

note = "\nSIMULATION SETTINGS:"
print note
print "-" * len(note)

for k, v in simulation_settings.items():
    print "* ", k, "=", v

# In[ ]:

# In/Out directory
# my_dir="../pingfiles_edited/"+lab+"/"
# my_dir="../pingfiles_reduced/"+lab+"/"
my_dir = lab_and_model_settings["path_to_parse"] + "/"

# In[ ]:

# after some edit in the ping files, which does not discard every 'dummy' entries
if True:
    # for my_context in lab_and_model_settings["realms_per_context"].keys():
    for my_context in ["arpsfx"]:
        generate_file_defs(lab_and_model_settings, simulation_settings, year=2000, context=my_context,
                           pingfile=my_dir + "ping_" + my_context + ".xml", printout=True,
                           cvs_path=my_cvspath, dummies='skip', dirname=my_dir)
