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

from tests.tools_for_tests import create_config_elements, TestPing


class TestPingFilesAllCNRM(unittest.TestCase, TestPing):
    """
    Test ping files generation for CMIP7 at CNRM
    """
    def setUp(self):
        config = create_config_elements(
            simulation="pingfiles_CMIP7_CNRM",
            contexts=["nemo", "arpsfx"],
            year=None,
            select="no",
	        is_ping=True,
            filename="ping_{content}.xml",
            by_realm=False,
            debug=True
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()