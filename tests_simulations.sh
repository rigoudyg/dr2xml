#!/usr/bin/bash

run_mode=${1:-"test"} # "ref" or "test"
to_compare=${2:-"no"} # "changes" or "python" or "no"
add_coverage=${3:-"no"} # "yes" or "no"
add_profile=${4:-"no"} # "yes" or "no"
simulations_to_test=${5:-"a4SST amip land 1pctCO2 piNTCF piControl ssp585 hist_aer piClim aladin levels aladin_nodr C3S-SF RCSM6_HIS amip_ESM RCSM6_HIS_light"}

if [ "${add_coverage}" = "yes" ]; then
  # Remove old results
  coverage erase
  rm -rf $PWD/tests/htmlcov
  scripts_to_cover="xml_writer,xml_interface,Xwrite,Xparse,vars_selection,vars_home,utils,settings_interface,postprocessing,plevs_unions,pingfiles_interface,infos,grids_selection,grids,file_splitting,dr_interface,config,cfsites,analyzer"
  # Run coverage with different tests
  for simulation in $simulations_to_test; do
    coverage run --parallel-mode --source=$scripts_to_cover tests_simulations.py $simulation $run_mode $to_compare $add_profile
      if [ ! $? -eq 0 ] ; then
          exit 1
      fi
  done
  # Assemble results
  coverage combine
  # Make html results
  coverage html --title "dr2xml unitests coverage" -d $PWD/tests/htmlcov
  # Open html coverage
  firefox file://$PWD/tests/htmlcov/index.html
else
  for simulation in $simulations_to_test; do
    python tests_simulations.py --simulation=$simulation --run_mode=$run_mode --to_compare=$to_compare --add_profile=$add_profile
      if [ ! $? -eq 0 ] ; then
          exit 1
      fi
  done
fi