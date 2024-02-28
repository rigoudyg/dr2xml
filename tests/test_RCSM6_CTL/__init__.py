#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for simulation levels
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import copy
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.basic_configuration_for_tests import *
from tests.tools_for_tests import TestSimulation, create_config_elements


class TestCTL(unittest.TestCase, TestSimulation):
    """
    Test output generation for RCSM6_CTL
    """
    def setUp(self):
        path_xml_aladin = "/".join([path_xml, "../xml_files_Aladin"])
        config = create_config_elements(
            simulation="RCSM6_CTL",
            contexts=["nemo", "surfex", "trip"],
            year="2009",
            enddate="20210101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'RCSM6-CTL.3'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()
