#!/usr/bin/env bash
# -*- coding: utf-8 -*-

export TIME="real    %E\nuser    %U\nsys     %S"

log_file="launch_tests.log"
echo "Launch test $(date)" > ${log_file}
echo "********************" >> ${log_file}
echo "********************" >> ${log_file}
out_code_sum=0

function test_function(){
  local test_to_perform=$1
  local log_out="tests/${test_to_perform}.out"
  local log_err="tests/${test_to_perform}.err"
  echo "Test tests/${test_to_perform}" >> ${log_file}
  # /usr/bin/time -a -o ${log_file} python3 -m unittest tests/${test_to_perform} >${log_out} 2>${log_err}
  python3 -m unittest tests/${test_to_perform} >${log_out} 2>${log_err}
  local out_code=$?
  echo "Output ${out_code}" >> ${log_file}
  if [ ${out_code} -ne 0 ]; then
    cat ${log_err} >>${log_file}
  fi
  rm -f ${log_out} ${log_err}
  echo "********************" >> ${log_file}
  out_code_sum=$((${out_code_sum}+${out_code}))
}

function test_script(){
  local script_to_launch=$1
  local options_of_script=$2
  local log_out="scripts/${script_to_launch}.out"
  local log_err="scripts/${script_to_launch}.err"
  echo "Test scripts/${script_to_launch} ${options_of_script}" >> ${log_file}
  # /usr/bin/time -a -o ${log_file} python3 scripts/${script_to_launch} ${options_of_script} >${log_out} 2>${log_err}
  python3 scripts/${script_to_launch} ${options_of_script} >${log_out} 2>${log_err}
  local out_code=$?
  echo "Output ${out_code}" >> ${log_file}
  if [ ${out_code} -ne 0 ]; then
    cat ${log_err} >>${log_file}
  fi
  rm -f ${log_out} ${log_err}
  echo "********************" >> ${log_file}
  out_code_sum=$((${out_code_sum}+${out_code}))
}

for f in $(cd tests; ls test*.py); do
  test_function $f
done

for f in $(cd tests; ls test*/__init__.py); do
  test_function $f
done

test_script "create_docs_projects.py" "--target_directory=test"

test_script "check_outputs_produced.py" "--out=test tests/xml_outputs/dr2xml_trip.xml --ioxdir=tests/xml_outputs/outputs --fatal=0"

test_script "check_outputs_produced.py" "--out=test tests/xml_outputs/dr2xml_trip.xml --ioxdir=tests/xml_outputs/outputs2"

test_script "find_netcdf_names_from_xml_files.py" "--out=test tests/xml_outputs/dr2xml_trip.xml"

test_script "create_ping_files.py" "--lab=cnrm --out=test"

echo "Out code sum: ${out_code_sum}" >> ${log_file}

cat ${log_file}
rm -f ${log_file}

exit ${out_code_sum}