#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for simulation piNTCF
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import copy
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.tools_for_tests import TestSimulation, create_config_elements


class TestPiNTCF(unittest.TestCase, TestSimulation):
    """
    Test output generation for AOESM_piNTCF_r3bfx
    """
    def setUp(self):
        config = create_config_elements(
            simulation="AOESM_hist_piNTCF_r3bfx",
            contexts=["nemo", "surfex", "trip"],
            year="1850",
            enddate="18510101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_nemo.xml {path_xml}/ping_nemo_gelato.xml "
                      "{path_xml}/ping_nemo_ocnBgChem.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'CNRM-ESM2-1_hist-piNTCF_r3i1p1f2_AOESM_hist-piNTCF_r3bfx'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()
