#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CMIP7 python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals


from dr2xml.projects.dr2xml_func import sort_mips, format_sizes, get_logger
from dr2xml.projects.basics_func import build_external_variables, compute_nb_days
from dr2xml.projects.CMIP6_esgvoc_func import get_ids_from_list


def format_id(input_id):
    return input_id.replace("-", "_").lower()


def get_attr_and_join(list_values, attribute="drs_name", separator=" "):
    return separator.join(sorted([elt.__getattribute__(attribute) for elt in list_values]))


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
    logger = get_logger()
    components = source['model_components']
    rep = source_id + " (" + str(source['release_year']) + "):"
    for realm in ["aerosol", "atmosphere", "atmospheric_chemistry", "land_surface", "ocean", "ocean_biogeochemistry", "sea_ice"]:
        description = [component.__dict__ for component in components if component.__dict__["component"] in [realm, ]]
        if len(description) != 1:
            logger.error("Either no component or several components found for realm %s: %s" % (realm, description))
            raise ValueError("Either no component or several components found for realm %s: %s" % (realm, description))
        else:
            description = description[0]["name"]
        if description not in ["none", "None", None]:
            rep = rep + "\n" + realm + ": " + description
    return rep


def build_filename(variable_id, branding_suffix, frequency, region, grid_label, source_id, expid_in_filename,
                   variant_label, date_range, var_type, list_perso_dev_file, prefix):
    filename = "_".join(([variable_id, branding_suffix, frequency, region, grid_label, source_id, expid_in_filename,
                          variant_label]))
    if var_type in ["perso", "dev"]:
        with open(list_perso_dev_file, mode="a", encoding="utf-8") as list_perso_and_dev:
            list_perso_and_dev.write(".*{}.*\n".format(filename))
    filename = prefix + filename
    if frequency not in ["fx", ]:
        filename = "_".join([filename, date_range])
    return filename


def fill_license(value, institution_id, info_url, license_id, license_url, commercial_license):
    value = value.replace("<Your Centre Name>", institution_id)
    value = value.replace("<Your Institution; see CMIP6_institution_id.json>", institution_id)
    # TODO: Adapt next line
    value = value.replace("[NonCommercial-]", commercial_license)
    value = value.replace("<Creative Commons; select and insert a license_id; see below>", license_id)
    value = value.replace("[ and at <some URL maintained by modeling group>]", " and at " + info_url)
    value = value.replace("<insert the matching license_url; see below>", license_url)
    return value
