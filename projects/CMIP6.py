#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CMIP6 python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals


def make_source_string(source, source_id):
    """
    From the dic of sources in CMIP6-CV, Creates the string representation of a
    given model (source_id) according to doc on global_file_attributes, so :

    <modified source_id> (<year>): atmosphere: <model_name> (<technical_name>, <resolution_and_levels>);
    ocean: <model_name> (<technical_name>, <resolution_and_levels>); sea_ice: <model_name> (<technical_name>);
    land: <model_name> (<technical_name>); aerosol: <model_name> (<technical_name>);
    atmospheric_chemistry <model_name> (<technical_name>); ocean_biogeochemistry <model_name> (<technical_name>);
    land_ice <model_name> (<technical_name>);

    """
    # mpmoine_correction:make_source_string: pour lire correctement le fichier 'CMIP6_source_id.json'
    components = source['model_component']
    rep = source_id + " (" + source['release_year'] + "): "
    for realm in ["aerosol", "atmos", "atmosChem", "land", "ocean", "ocnBgchem", "seaIce"]:
        component = components[realm]
        description = component['description']
        if description != "none":
            rep = rep + "\n" + realm + ": " + description
    return rep


def build_filename(frequency, prefix, table, source_id, expid_in_filename, member_id, grid_label, date_range,
                   var_type, list_perso_dev_file, label, mipVarLabel, use_cmorvar=False):
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
    filename = "_".join(([varname_for_filename, table, source_id, expid_in_filename, member_id, grid_label]))
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


def fill_license(value, institution_id, info_url):
    value = value.replace("<Your Centre Name>", institution_id)
    # TODO: Adapt next line
    value = value.replace("[NonCommercial-]", "NonCommercial-")
    value = value.replace("[ and at <some URL maintained by modeling group>]", " and at " + info_url)
    return value
