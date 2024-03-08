#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for simulation AAD50 nodr
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import copy
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.tools_for_tests import TestSimulation, create_config_elements


class TestAAD50NoDR(unittest.TestCase, TestSimulation):
    """
    Test output generation for AAD50_641_nodr
    """
    def setUp(self):
        config = create_config_elements(
            simulation="AAD50_641_nodr",
            contexts=["surfex", "trip"],
            year="2003",
            enddate="20030201",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[("EXPID", "AAD50_641"),
                        ]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()
