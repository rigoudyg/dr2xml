#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CMIP6 python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals


from dr2xml.projects.dr2xml_func import sort_mips, format_sizes, format_grids
from dr2xml.projects.basics_func import build_external_variables, compute_nb_days

def build_filename(frequency, prefix, source_id, expid_in_filename, date_range, var_type, list_perso_dev_file, label,
                   mipVarLabel, domain_id, driving_source_id, driving_variant_label, institution_id,
                   version_realization, use_cmorvar=False):
    if "fx" in frequency:
        varname_for_filename = label
    else:
        if use_cmorvar:
            varname_for_filename = label
        else:
            varname_for_filename = mipVarLabel
        # DR21 has a bug with tsland : the MIP variable is named "ts"
        if label in ["tsland", ]:
            varname_for_filename = "tsland"
    filename = "_".join(([elt for elt in [varname_for_filename, domain_id, driving_source_id, expid_in_filename,
                                          driving_variant_label, institution_id, source_id,
                                          version_realization, frequency] if
                          len(str(elt)) > 0]))
    if var_type in ["perso", "dev"]:
        with open(list_perso_dev_file, mode="a", encoding="utf-8") as list_perso_and_dev:
            list_perso_and_dev.write(".*{}.*\n".format(filename))
    filename = prefix + filename
    if "fx" not in frequency:
        if frequency in ["1hrCM", "monC"]:
            suffix = "-clim"
        else:
            suffix = ""
        filename = "_".join([filename, date_range + suffix])
    return filename