#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Take in entry xml files designed for xios and return the list of netcdf file names that should be produced.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import os
from argparse import ArgumentParser

from xml_writer.utils import decode_if_needed
from check_outputs_produced import find_netcdf_filenames_from_xmls, parse_args


dict_opts = parse_args()
output = dict_opts.pop("out")

with open(output, "w", encoding="utf-8") as out:
	out.write(decode_if_needed(os.linesep.join(find_netcdf_filenames_from_xmls(**dict_opts))))