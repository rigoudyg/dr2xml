#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import os
import glob
import shutil
import sys
import codecs
from io import open
import time
import argparse


from dr2xml import generate_file_defs
from config import python_version


def find_data(simulation):
    if simulation in ["a4SST", ]:
        # Tests a4SST_AGCM_1960
        from tests.test_a4SST_AGCM_1960.input.config import config as config_dict_a4SST
        from tests.test_a4SST_AGCM_1960.input.simulation_settings import simulation_settings as sset_a4SST
        from tests.test_a4SST_AGCM_1960.input.lab_and_model_settings import lab_and_model_settings as lset_a4SST
        from tests.test_a4SST_AGCM_1960.input.config import simulation as simulation_a4SST
        from tests.test_a4SST_AGCM_1960.input.config import contexts as contexts_a4SST
        return (config_dict_a4SST, sset_a4SST, lset_a4SST, simulation_a4SST, contexts_a4SST)
    elif simulation in ["aladin", ]:
        # Tests AAD50-641
        # TODO: Update data
        from tests.test_AAD50_641.input.config import config as config_dict_aladin
        from tests.test_AAD50_641.input.simulation_settings import simulation_settings as sset_aladin
        from tests.test_AAD50_641.input.lab_and_model_settings import lab_and_model_settings as lset_aladin
        from tests.test_AAD50_641.input.config import simulation as simulation_aladin
        from tests.test_AAD50_641.input.config import contexts as contexts_aladin
        return (config_dict_aladin, sset_aladin, lset_aladin, simulation_aladin, contexts_aladin)
    elif simulation in ["levels", ]:
        # Tests levels
        from tests.test_levels.input.config import config as config_dict_levels
        from tests.test_levels.input.simulation_settings import simulation_settings as sset_levels
        from tests.test_levels.input.lab_and_model_settings import lab_and_model_settings as lset_levels
        from tests.test_levels.input.config import simulation as simulation_levels
        from tests.test_levels.input.config import contexts as contexts_levels
        return (config_dict_levels, sset_levels, lset_levels, simulation_levels, contexts_levels)
    else:
        raise ValueError("Unknown simulation %s" % simulation)


def test_function(simulation, run_mode, python_version, config_dict, contexts, lset, sset):
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
            generate_file_defs(context=context, lset=lset, sset=sset, **config_dict)
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
    args = parser.parse_args()

    simulation = args.simulation
    run_mode = args.run_mode
    to_compare = args.to_compare

    (config_dict, sset, lset, simulation_name, contexts) = find_data(simulation)
    test_function(simulation_name, run_mode, python_version, config_dict, contexts, lset, sset)

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
