#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Miscellaneous functions
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from .dr_interface import get_element_uid, get_request_by_id_by_sect


def request_item_include(ri, var_label, freq):
    """
    test if a variable is requested by a requestItem at a given freq
    """
    var_group = get_element_uid(get_element_uid(ri.rlid).refid)
    req_vars = get_request_by_id_by_sect(var_group.uid, 'requestVar')
    cm_vars = [get_element_uid(get_element_uid(reqvar).vid) for reqvar in req_vars]
    return any([cmv.label == var_label and cmv.frequency == freq for cmv in cm_vars])


def realm_is_processed(realm, source_type):
    """
    Tells if a realm is definitely not processed by a source type

    list of source-types : AGCM BGC AER CHEM LAND OGCM AOGCM
    list of known realms : 'seaIce', '', 'land', 'atmos atmosChem', 'landIce', 'ocean seaIce',
                           'landIce land', 'ocean', 'atmosChem', 'seaIce ocean', 'atmos',
                           'aerosol', 'atmos land', 'land landIce', 'ocnBgChem'
    """
    components = source_type.split(" ")
    rep = True
    #
    if realm == "atmosChem" and 'CHEM' not in components:
        return False
    if realm == "aerosol" and 'AER' not in components:
        return False
    if realm == "ocnBgChem" and 'BGC' not in components:
        return False
    #
    with_ocean = ('OGCM' in components or 'AOGCM' in components)
    if 'seaIce' in realm and not with_ocean:
        return False
    if 'ocean' in realm and not with_ocean:
        return False
    #
    with_atmos = ('AGCM' in components or 'AOGCM' in components)
    if 'atmos' in realm and not with_atmos:
        return False
    if 'atmosChem' in realm and not with_atmos:
        return False
    if realm == '' and not with_atmos:  # In DR 01.00.15 : some atmos variables have realm=''
        return False
    #
    with_land = with_atmos or ('LAND' in components)
    if 'land' in realm and not with_land:
        return False
    #
    return rep
