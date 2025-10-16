#!/usr/bin/env bash
# -*- coding: utf-8 -*-

set -e

coverage erase

# coverage run
for f in $(ls tests/test_*.py); do
    coverage run --parallel-mode -m unittest $f
done
for f in $(ls tests/test_*/__init__.py); do
    coverage run --parallel-mode -m unittest $f
done
coverage run --parallel-mode scripts/create_docs_projects.py --target_directory=test
coverage run --parallel-mode scripts/check_outputs_produced.py --out=test tests/xml_outputs/dr2xml_trip.xml --ioxdir=tests/xml_outputs/outputs --fatal=0
coverage run --parallel-mode scripts/check_outputs_produced.py --out=test tests/xml_outputs/dr2xml_trip.xml --ioxdir=tests/xml_outputs/outputs2
coverage run --parallel-mode scripts/find_netcdf_names_from_xml_files.py --out=test tests/xml_outputs/dr2xml_trip.xml
coverage run --parallel-mode scripts/create_ping_files.py --lab=cnrm --out=test
coverage combine

coverage html
