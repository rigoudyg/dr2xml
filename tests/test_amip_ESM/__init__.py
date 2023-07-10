#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for simulation amip ESM
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import copy
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.basic_configuration_for_tests import *
from tests.tools_for_tests import TestSimulation, create_config_elements


class TestAmipESM(unittest.TestCase, TestSimulation):
    """
    Test output generation for amip_ESM
    """
    def setUp(self):
        config = create_config_elements(
            simulation="amip_ESM",
            contexts=["surfex", "trip"],
            year="1979",
            enddate="19800101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'amipESM-CEDS2021-aerdiffus'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7a4dce8aef3dd4c1443dcfc57c36cbe7')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()
