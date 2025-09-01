#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools specific to a laboratory, interface
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import os
from importlib.machinery import SourceFileLoader


laboratory_source = None


def initialize_laboratory_settings():
    global laboratory_source
    if laboratory_source is None:
        from dr2xml.settings_interface import get_settings_values
        internal_dict = get_settings_values("internal")
        institution_id = internal_dict["institution_id"]
        if institution_id in ["CNRM-CERFACS", "CNRM", "lfpw"]:
            from . import CNRM_CERFACS
            laboratory_source = CNRM_CERFACS
        elif institution_id in ["IPSL", "ipsl"]:
            from . import IPSL
            laboratory_source = IPSL
        else:
            laboratory_used = internal_dict["laboratory_used"]
            if laboratory_used is not None:
                if os.path.isfile(laboratory_used):
                    laboratory_source = SourceFileLoader(os.path.basename(laboratory_used),
                                                         laboratory_used).load_module(os.path.basename(laboratory_used))
            if laboratory_source is None:
                raise ValueError("Could not find the laboratory source module for %s" % institution_id)


def lab_adhoc_grid_policy(cmvarid, grids):
    """
    Decide , in a lab specific way, which set of grids a given
    variable should be produced on You should re-engine code below to
    your own decision scheme, if the schemes of the standard grid
    policy choices (see function decide_for_grid) do not fit

    CMVARID is uid of the CMORvar
    GRIDS is a list of strings for grid as specified in requestLink (with some normalization)
    LSET is the laboratory settings dictionary. It carries a policy re. grids

    Returns either a single grid string or a list of such strings
    """
    return laboratory_source.__getattribute__("lab_grid_policy").__call__(cmvarid, grids)
