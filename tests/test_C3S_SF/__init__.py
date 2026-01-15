#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for simulation C3S-SF
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import copy
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.tools_for_tests import TestSimulation, create_config_elements


class TestC3SSF(unittest.TestCase, TestSimulation):
    """
    Test output generation for C3S_SF
    """
    def setUp(self):
        config = create_config_elements(
            simulation="C3S_SF",
            contexts=["surfex", "nemo", "trip"],
            year="2010",
            enddate="2011",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_nemo.xml {path_xml}/ping_trip.xml",
            attributes=[("EXPID", "H2010E001")]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()
