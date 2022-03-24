#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CMIP6 python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals


def build_filename(expid_in_filename, realm, frequency, label, date_range, var_type, list_perso_dev_file):
    filename = "_".join(([expid_in_filename, realm, frequency, label]))
    if var_type in ["perso", "dev"]:
        with open(list_perso_dev_file, mode="a", encoding="utf-8") as list_perso_and_dev:
            list_perso_and_dev.write("{}.*\n".format(filename))
    filename = "_".join([filename, date_range + ".nc"])
    return filename


def convert_frequency(freq):
    if freq.endswith("hr"):
        freq.rstrip("hr")
        freq += "hourly"
    elif freq.endswith("h"):
        freq.rstrip("h")
        freq += "hourly"
    elif freq in ["day", ]:
        freq = "daily"
    elif freq in ["mon", ]:
        freq = "monthly"
    return freq


def build_string_from_list(args):
    return ", ".join(args)
