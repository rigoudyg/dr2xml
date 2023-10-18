#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools specific to a CNRM-CERFACS
"""
from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.dr_interface import get_data_request
from dr2xml.settings_interface import get_settings_values


def lab_grid_policy(cmvarid, grids):  # TBD
    """
    See doc of lab_adhoc_grid_policy
    """
    internal_dict = get_settings_values("internal")
    cmvar_uid = get_data_request().get_element_uid(cmvarid, elt_type="variable")
    if cmvar_uid is not None and cmvar_uid.label in ["sos"]:
        return [g for g in grids if g in ["", "1deg"]]
    elif cmvar_uid is not None and cmvar_uid.label in ["tos"] and (cmvar_uid.mipTable not in ["3hr"] or
                                                                   internal_dict["allow_tos_3hr_1deg"]):
        if internal_dict["adhoc_policy_do_add_1deg_grid_for_tos"]:
            list_grids = list()
            if "" in grids:
                list_grids.append("")
            list_grids.append("1deg")
            return list_grids
        else:
            return [g for g in grids if g in ["", "1deg"]]
    else:
        ngrids = [g for g in grids if g not in ["1deg", "2deg", "100km", "50km"]]
        # if "cfsites" in grids : return ["","cfsites"]
        if len(ngrids) == 0:
            ngrids = [""]  # We should at least provide native grid
        return ngrids