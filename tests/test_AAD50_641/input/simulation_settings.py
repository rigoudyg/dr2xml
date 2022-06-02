# -*- coding: utf-8 -*-

# An example of settings for a CMIP6 experiment/simulation, for use by dr2xml
# It complies with dr2xml v1.00. It complements another settings file, relevant
# for laboratory and model settings
# See refs at bottom

from tests.tests_config import path_homedr, path_table

aladin_path_table = "/".join([path_table, "../Tables_Aladin"])

simulation_settings = {

    "configuration": "ARCM",
    "listof_home_vars": '{}/home_data_request_aladin_RCM.txt {}/home_data_request_aladin_aerosols_RCM.txt '
                        '{}/home_data_request_trip_RCM.txt'.format(path_homedr, path_homedr, path_homedr),
    "path_extra_tables": aladin_path_table,
    # DR experiment name to process. See http://clipc-services.ceda.ac.uk/dreq/index/experiment.html
    "activity_id": "CORDEX",
    "experiment_id": "amip",
    "expid_in_filename": "evaluation",
    "driving_model_id": "ECMWF-ERAINT",
    "driving_experiment": "ERA-INTERIM, evaluation, r1i1p1",
    "driving_model_ensemble_member": "r1i1p1",
    "driving_experiment_name": "evaluation",
    "Lambert_conformal_longitude_of_central_meridian": "10.f",
    "Lambert_conformal_standard_parallel": "37.f",
    "Lambert_conformal_latitude_of_projection_origin": "37.f",
    "rcm_version_id": "V1",

    # additional information about the experiment (e.g. how you did interpret the expt design)
    "comment": "",

    'child_time_ref_year': 1979,  # should be the same in arpsfx.xml, nemo.xml, trip.xml
    "branch_year_in_child": 1979,  # This is the start year of this 'child simulation', in its calendar. it should
    # be the same as child_time_ref_year
    "branch_year_in_parent": 'N/A',
    # Annee de branchement s'il y a un parent. POUR UN SCENARIO: MEME VALEUR QUE L'HISTORIQUE CORRESP.

    # Describing the member - Values may be omitted if = 1
    "realization_index": 1,
    "initialization_index": 1,
    "physics_index": 1,
    "forcing_index": 2,  # Should be 2 for all CMIP6 experiments, until further notice...

    # You can specifically exclude some pairs (vars,tables), here in experiment settings
    # They wil be added to the lab-settings list of excluded pairs
    # Here below, this is specific to amip and historical.
    # MUST COMMENT THE LINE BELOW FOR OTHER EXPERIMENTS !!!!!!!!!!!!!!!!
    'excluded_pairs': [('ua', '6hrPlevPt'), ('va', '6hrPlevPt'), ('ta', '6hrPlevPt')],

    # It can be handy to exclude some Tables at the experiment level. They are added to the lab-level set
    # "excluded_tables"  : [ ] ,

    # It is recommended that some description be included to help identify major differences among variants, 
    # but care should be taken to record correct information.  
    "variant_info": "",

    # All about the branching scheme
    "branch_method": "standard",  # default value='standard' meaning ~ "select a start date"
    # (this is not necessarily the parent start date)
    'parent_time_ref_year': 1850,  # Fixe pour le CNRM-CERFACS. Not used if parent is "" or "N/A"

    "sub_experiment_id": "none",  # Optional, default is 'none'; example : s1960.
    "sub_experiment": "none",  # Optional, default is 'none'
    "history": "none",  # Used when a simulation is re-run, an output file is modified ....

    # For some experiments (e.g. concentration-driven historical in AESM config), the only way to 
    # avoid producing useless fields is to explictly exclude variables (in addition to those in lab_settings)
    'excluded_vars': [],

    # A per-variable dict of comments which are specific to this simulation. It will replace  
    # the all-simulation comment present in lab_and_model_settings
    'comments': {
        # 'tas' : 'tas diagnostic could have a special scheme in this simulation',
    },

    # 'parent_variant_label' :""  #Default to 'same as child'. Other cases should be exceptional
    # "parent_mip_era": 'CMIP5'   # set it only in special cases (e.g. PMIP warm start from CMIP5/PMIP3 experiment)
    # 'parent_source_id'     : 'CNRM-CM5.1' # set it only in special cases, where parent model is not the same model
    'bypass_CV_components': True,
    'CORDEX_data': True,
    'CORDEX_domain': {'nemo': 'MED-06', 'surfex': 'MED-44', 'trip': 'MED-50'},
}

# The reference documents are listed in top level document :https://pcmdi.llnl.gov/CMIP6/Guide/
# Of interest :
#   - paragraph 5 of https://pcmdi.llnl.gov/CMIP6/Guide/modelers.html
#   - CMIP6 Data Request , in browsable format: http://clipc-services.ceda.ac.uk/dreq/index.html
