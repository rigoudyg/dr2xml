#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C3S python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals


from dr2xml.projects.dr2xml_func import sort_mips, format_sizes
from dr2xml.projects.basics_func import build_external_variables, compute_nb_days


def build_filename(expid_in_filename, realm, frequency, label, date_range, var_type, list_perso_dev_file):
    if isinstance(realm, (list, tuple)):
        realm = realm[0]
    filename = "_".join(([expid_in_filename, realm, frequency, label]))
    if var_type in ["perso", "dev"]:
        with open(list_perso_dev_file, mode="a", encoding="utf-8") as list_perso_and_dev:
            list_perso_and_dev.write("{}.*\n".format(filename))
    filename = "_".join([filename, date_range + ".nc"])
    return filename


def convert_frequency(freq):
    if freq.endswith("hr"):
        freq = freq.replace("hr", "hourly")
    elif freq.endswith("h"):
        freq = freq.replace("h", "hourly")
    elif freq in ["day", ]:
        freq = "daily"
    elif freq in ["mon", ]:
        freq = "monthly"
    return freq


def convert_realm(realm):
    if not isinstance(realm, (list, set, tuple)):
        realm = [realm, ]
    if "ocean" in realm or "seaIce" in realm:
        realm = "nemo",
    elif "land" in realm:
        realm = "atmo"
    elif len(realm) == 1:
        realm = list(realm)[0]
    else:
        raise ValueError("Unable to figure out the realm to be used.")
    return realm
