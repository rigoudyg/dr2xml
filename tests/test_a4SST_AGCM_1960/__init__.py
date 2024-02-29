#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for simulation a4SST
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import copy
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.tools_for_tests import TestSimulation, create_config_elements


class TestA4SST(unittest.TestCase, TestSimulation):
    """
    Test output generation for a4SST_AGCM_1960
    """
    def setUp(self):
        config = create_config_elements(
            simulation="a4SST_AGCM_1960",
            contexts=["surfex", "trip"],
            year="1960",
            enddate="19610101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[("EXPID", "CNRM-CM6-1_a4SST_r1i1p1f2"),
                        ("CMIP6_CV_version", "cv=6.2.3.0-7-g2019642"),
                        ("dr2xml_md5sum", "7040f60f6bf3118dc6c58b9fb8727d87")
                        ]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()
