#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for simulation piControl
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import copy
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.tools_for_tests import TestSimulation, create_config_elements


class TestPiControlCMIP7(unittest.TestCase, TestSimulation):
    """
    Test output generation for AOESM_piControl_CMIP7
    """
    def setUp(self):
        config = create_config_elements(
            simulation="AOESM_piControl_CMIP7",
            contexts=["nemo", "surfex", "trip"],
            year="1850",
            enddate="18510101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml {path_xml}/ping_nemo.xml",
            attributes=[('EXPID', 'CNRM-ESM2-1_esm-piControl_r1i1p1f2_v2'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()
