#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import cProfile
import io
import os
import glob
import pstats
import shutil
import sys
import codecs
from io import open
import time
import argparse


from dr2xml import generate_file_defs
from dr2xml.config import python_version


def find_data(simulation):
    if simulation in ["a4SST", ]:
        # Tests a4SST_AGCM_1960
        from tests.test_a4SST_AGCM_1960.input.config import config
        from tests.test_a4SST_AGCM_1960.input.simulation_settings import simulation_settings
        from tests.test_a4SST_AGCM_1960.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_a4SST_AGCM_1960.input.config import simulation
        from tests.test_a4SST_AGCM_1960.input.config import contexts
    elif simulation in ["amip", ]:
        # Tests amip-hist_AGCM_1870_r10
        from tests.test_amip_hist_AGCM_1870_r10.input.config import config
        from tests.test_amip_hist_AGCM_1870_r10.input.simulation_settings import simulation_settings
        from tests.test_amip_hist_AGCM_1870_r10.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_amip_hist_AGCM_1870_r10.input.config import simulation
        from tests.test_amip_hist_AGCM_1870_r10.input.config import contexts
    elif simulation in ["land", ]:
        # Tests land-hist_LGCM
        from tests.test_land_hist_LGCM.input.config import config
        from tests.test_land_hist_LGCM.input.simulation_settings import simulation_settings
        from tests.test_land_hist_LGCM.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_land_hist_LGCM.input.config import simulation
        from tests.test_land_hist_LGCM.input.config import contexts
    elif simulation in ["aladin", ]:
        # Tests AAD50-641
        # TODO: Update data
        from tests.test_AAD50_641.input.config import config
        from tests.test_AAD50_641.input.simulation_settings import simulation_settings
        from tests.test_AAD50_641.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_AAD50_641.input.config import simulation
        from tests.test_AAD50_641.input.config import contexts
    elif simulation in ["1pctCO2", ]:
        # Tests AOESM_1pctCO2_rad_CM6_r1
        from tests.test_AOESM_1pctCO2_rad_CM6_r1.input.config import config
        from tests.test_AOESM_1pctCO2_rad_CM6_r1.input.simulation_settings import simulation_settings
        from tests.test_AOESM_1pctCO2_rad_CM6_r1.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_AOESM_1pctCO2_rad_CM6_r1.input.config import simulation
        from tests.test_AOESM_1pctCO2_rad_CM6_r1.input.config import contexts
    elif simulation in ["piNTCF", ]:
        # Tests AOESM_hist_piNTCF_r3bfx
        from tests.test_AOESM_hist_piNTCF_r3bfx.input.config import config
        from tests.test_AOESM_hist_piNTCF_r3bfx.input.simulation_settings import simulation_settings
        from tests.test_AOESM_hist_piNTCF_r3bfx.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_AOESM_hist_piNTCF_r3bfx.input.config import simulation
        from tests.test_AOESM_hist_piNTCF_r3bfx.input.config import contexts
    elif simulation in ["piControl", ]:
        # Tests AOESM_piControl_CM6_r1_v2
        from tests.test_AOESM_piControl_CM6_r1_v2.input.config import config
        from tests.test_AOESM_piControl_CM6_r1_v2.input.simulation_settings import simulation_settings
        from tests.test_AOESM_piControl_CM6_r1_v2.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_AOESM_piControl_CM6_r1_v2.input.config import simulation
        from tests.test_AOESM_piControl_CM6_r1_v2.input.config import contexts
    elif simulation in ["ssp585", ]:
        # Tests AOESM_ssp585_CM6_r3
        from tests.test_AOESM_ssp585_CM6_r3.input.config import config
        from tests.test_AOESM_ssp585_CM6_r3.input.simulation_settings import simulation_settings
        from tests.test_AOESM_ssp585_CM6_r3.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_AOESM_ssp585_CM6_r3.input.config import simulation
        from tests.test_AOESM_ssp585_CM6_r3.input.config import contexts
    elif simulation in ["hist_aer", ]:
        # Tests
        from tests.test_hist_aer_CM6_r4.input.config import config
        from tests.test_hist_aer_CM6_r4.input.simulation_settings import simulation_settings
        from tests.test_hist_aer_CM6_r4.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_hist_aer_CM6_r4.input.config import simulation
        from tests.test_hist_aer_CM6_r4.input.config import contexts
    elif simulation in ["piClim", ]:
        # Tests piClim_anthro_AGCM_r1
        from tests.test_piClim_anthro_AGCM_r1.input.config import config
        from tests.test_piClim_anthro_AGCM_r1.input.simulation_settings import simulation_settings
        from tests.test_piClim_anthro_AGCM_r1.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_piClim_anthro_AGCM_r1.input.config import simulation
        from tests.test_piClim_anthro_AGCM_r1.input.config import contexts
    elif simulation in ["aladin_nodr", ]:
        # Tests AAD50-641 no dr
        # TODO: Update data
        from tests.test_AAD50_641_nodr.input.config import config
        from tests.test_AAD50_641_nodr.input.simulation_settings import simulation_settings
        from tests.test_AAD50_641_nodr.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_AAD50_641_nodr.input.config import simulation
        from tests.test_AAD50_641_nodr.input.config import contexts
    elif simulation in ["levels", ]:
        # Tests levels
        from tests.test_levels.input.config import config
        from tests.test_levels.input.simulation_settings import simulation_settings
        from tests.test_levels.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_levels.input.config import simulation
        from tests.test_levels.input.config import contexts
    elif simulation in ["C3S-SF", ]:
        # Tests levels
        from tests.test_C3S_SF.input.config import config
        from tests.test_C3S_SF.input.simulation_settings import simulation_settings
        from tests.test_C3S_SF.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_C3S_SF.input.config import simulation
        from tests.test_C3S_SF.input.config import contexts
    elif simulation in ["RCSM6_HIS", ]:
        # Tests RCSM6_HIS
        from tests.test_RCSM6_HIS.input.config import config
        from tests.test_RCSM6_HIS.input.simulation_settings import simulation_settings
        from tests.test_RCSM6_HIS.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_RCSM6_HIS.input.config import simulation
        from tests.test_RCSM6_HIS.input.config import contexts
    elif simulation in ["RCSM6_HIS_light", ]:
        # Tests RCSM6_HIS
        from tests.test_RCSM6_HIS_light.input.config import config
        from tests.test_RCSM6_HIS_light.input.simulation_settings import simulation_settings
        from tests.test_RCSM6_HIS_light.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_RCSM6_HIS_light.input.config import simulation
        from tests.test_RCSM6_HIS_light.input.config import contexts
    elif simulation in ["amip_ESM", ]:
        # Tests amip_ESM
        from tests.test_amip_ESM.input.config import config
        from tests.test_amip_ESM.input.simulation_settings import simulation_settings
        from tests.test_amip_ESM.input.lab_and_model_settings import lab_and_model_settings
        from tests.test_amip_ESM.input.config import simulation
        from tests.test_amip_ESM.input.config import contexts
    else:
        raise ValueError("Unknown simulation %s" % simulation)
    return config, simulation_settings, lab_and_model_settings, simulation, contexts


def test_function(simulation, run_mode, python_version, config_dict, contexts, lset, sset, add_profile):
    print("Test simulation:", simulation)
    output_directory = os.sep.join([os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]), "tests",
                                    "test_{}".format(simulation), "output_{}_{}".format(run_mode, python_version)])
    if os.path.isdir(output_directory):
        files_to_remove = glob.glob(os.sep.join([output_directory, "*"]))
        for file_to_remove in files_to_remove:
            os.remove(file_to_remove)
    else:
        os.mkdir(output_directory)

    old_stdout = sys.stdout
    with codecs.open("dr2xml_log".format(run_mode), 'w', encoding="utf-8") as logfile:
        for context in contexts:
            print("Execute context %s" % context)
            start_time = time.time()
            sys.stdout = logfile
            if add_profile in ["yes", ]:
                pr = cProfile.Profile()
                pr.enable()
            generate_file_defs(context=context, lset=lset, sset=sset, **config_dict)
            if add_profile in ["yes", ]:
                pr.disable()
                if python_version in ["python2", ]:
                    s = io.BytesIO()
                else:
                    s = io.StringIO()
                sortby = 'cumulative'
                ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                ps.print_stats()
                print(s.getvalue())
            sys.stdout = old_stdout
            print("It took %d s" % (time.time() - start_time))

    files_to_move = glob.glob(os.sep.join([os.getcwd(), "dr2xml_*"]))
    for file_to_move in files_to_move:
        shutil.move(file_to_move, output_directory)


def read_and_check_files_content(file_1, file_2):
    with open(file_1, "r", encoding="utf-8") as fic_1:
        content_1 = fic_1.read()
    with open(file_2, "r", encoding="utf-8") as fic_2:
        content_2 = fic_2.read()
    if content_1 == content_2:
        return True
    else:
        return False


# Launch tests
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulation", help="Simulation type to be used")
    parser.add_argument("--run_mode", choices=["test", "ref"], default="test",
                        help="Run mode")
    parser.add_argument("--to_compare", choices=["python", "changes", "no"], default="no",
                        help="Should a comparison be done?")
    parser.add_argument("--add_profile", choices=["yes", "no"], default="no", help="Should profiling be done?")
    args = parser.parse_args()

    simulation = args.simulation
    run_mode = args.run_mode
    to_compare = args.to_compare
    add_profile = args.add_profile
    if add_profile in ["yes", ] and to_compare not in ["no", ]:
        raise ValueError("If profiling is on, comparison will fail.")

    (config_dict, sset, lset, simulation_name, contexts) = find_data(simulation)
    test_function(simulation_name, run_mode, python_version, config_dict, contexts, lset, sset, add_profile)

    if run_mode in ["test", ] and to_compare not in ["no", ]:
        output_dir = os.sep.join([os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]), "tests",
                                  "test_{}".format(simulation_name), "output_{}_{}"])
        outputs_test = output_dir.format("test", python_version)
        if to_compare in ["changes", ]:
            outputs_ref = output_dir.format("ref", python_version)
        elif to_compare in ["python", ] and python_version in ["python2", ]:
            outputs_ref = output_dir.format("test", "python3")
        elif to_compare in ["python", ] and python_version in ["python3", ]:
            outputs_ref = output_dir.format("test", "python2")
        else:
            raise ValueError("Unknown combination of to_compare %s and python_version %s" % (to_compare,
                                                                                             python_version))
        if os.path.isdir(outputs_test) and os.path.isdir(outputs_ref):
            # Test des log
            log_file_name = "dr2xml_log"
            log_ref = os.sep.join([outputs_ref, log_file_name])
            log_test = os.sep.join([outputs_test, log_file_name])
            if os.path.isfile(log_test) and os.path.isfile(log_ref):
                if not read_and_check_files_content(log_test, log_ref):
                    raise Exception("Log files differs")
            else:
                raise Exception("Could not compare test and ref outputs, log are missing...")
            # Test list of dev and perso variables
            list_file_name = "dr2xml_list_perso_and_dev_file_names"
            list_ref = os.sep.join([outputs_ref, list_file_name])
            list_test = os.sep.join([outputs_test, list_file_name])
            if os.path.isfile(list_test) and os.path.isfile(list_ref):
                if not read_and_check_files_content(list_test, list_ref):
                    raise Exception("List of dev and perso vars files differs")
            else:
                print("Could not compare test and ref outputs, list of dev and perso vars are missing...")
            # Test contexts
            for context in contexts:
                context_file_name = "dr2xml_{}.xml".format(context)
                context_ref = os.sep.join([outputs_ref, context_file_name])
                context_test = os.sep.join([outputs_test, context_file_name])
                if os.path.isfile(context_test) and os.path.isfile(context_ref):
                    if not read_and_check_files_content(context_test, context_ref):
                        raise Exception("Context files differs for %s" % context)
                else:
                    raise Exception("Could not compare test and ref outputs, context files for %s are missing..."
                                    % context)
        else:
            raise Exception("Could not compare test and ref outputs, no data directory...")
