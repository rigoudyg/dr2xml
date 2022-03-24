#!/usr/bin/bash

run_mode=${1:-"test"} # "ref" or "test"
to_compare=${2:-"no"} # "changes" or "python" or "no"
simulations_to_test="a4SST aladin levels"
#simulations_to_test="a4SST"

# Run coverage with different tests
for simulation in $simulations_to_test; do
    python3 tests_simulations.py --simulation=$simulation --run_mode=$run_mode --to_compare=$to_compare
      if [ ! $? -eq 0 ] ; then
          exit 1
      fi
done
