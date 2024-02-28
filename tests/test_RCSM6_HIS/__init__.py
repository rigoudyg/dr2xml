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


class TestHIS(unittest.TestCase, TestSimulation):
    """
    Test output generation for RCSM6_HIS
    """
    def setUp(self):
        path_xml_aladin = "/".join([path_xml, "../xml_files_Aladin"])
        config = create_config_elements(
            simulation="RCSM6_HIS",
            contexts=["nemo", "surfex", "trip"],
            year="1949",
            enddate="19490901",
            pingfiles="{path_xml}/ping_nemo.xml {path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[("EXPID", "RCSM6.1_HIS_SP0")]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()
