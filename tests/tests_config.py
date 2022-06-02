#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import os

path_tests = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
path_common = os.sep.join([path_tests, "common"])
path_cv = os.sep.join(([path_common, "CMIP6_CVs", ""]))
path_table = os.sep.join(([path_common, "Tables"]))
path_xml = os.sep.join([path_common, "xml_files"])
path_homedr = os.sep.join([path_common, "home_data_request"])
