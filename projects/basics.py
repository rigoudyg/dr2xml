#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basics python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import datetime
import re

from utils import Dr2xmlError


def build_external_variables(cell_measures):
	#
	# CF rule : if the file variable has a cell_measures attribute, and
	# the corresponding 'measure' variable is not included in the file,
	# it must be quoted as external_variable
	external_variables = list()
	if "area:" in cell_measures:
		external_variables.append(re.sub(".*area: ([^ ]*).*", r'\1', cell_measures))
	if "volume:" in cell_measures:
		external_variables.append(re.sub(".*volume: ([^ ]*).*", r'\1', cell_measures))
	return " ".join(external_variables)


def compute_nb_days(year_ref, year_branch, month_ref=1, month_branch=1, day_ref=1, day_branch=1):
	date_ref = datetime.datetime(year_ref, month_ref, day_ref)
	date_branch = datetime.datetime(year_branch, month_branch, day_branch)
	nb_days = (date_branch - date_ref).days
	return "{}.0D".format(nb_days)
