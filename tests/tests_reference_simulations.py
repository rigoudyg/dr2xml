#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for xml_writer module
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import copy
import pprint
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.tools_for_tests import TestSimulation, create_config_elements


# @unittest.skipUnless(False, "OK")
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


# @unittest.skipUnless(False, "Ok")
class TestAAD50(unittest.TestCase, TestSimulation):
    """
    Test output generation for AAD50_641
    """
    def setUp(self):
        config = create_config_elements(
            simulation="AAD50_641",
            contexts=["surfex", "trip"],
            year="2003",
            enddate="20030201",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[("EXPID", "AAD50_641"),
                        ]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "Ok")
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


# @unittest.skipUnless(False, "Ok")
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


# @unittest.skipUnless(False, "Ok")
class TestAmipHist(unittest.TestCase, TestSimulation):
    """
    Test output generation for amip_hist_AGCM_1870_r10
    """
    def setUp(self):
        config = create_config_elements(
            simulation="amip_hist_AGCM_1870_r10",
            contexts=["surfex", "trip"],
            year="1870",
            enddate="18710101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'CNRM-CM6-1_amip-hist_r10i1p1f2'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "Ok")
class Test1pctCO2(unittest.TestCase, TestSimulation):
    """
    Test output generation for AOESM_1pctCO2_rad_CM6_r1
    """
    def setUp(self):
        config = create_config_elements(
            simulation="AOESM_1pctCO2_rad_CM6_r1",
            contexts=["nemo", "surfex", "trip"],
            year="1850",
            enddate="19891231",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_nemo.xml {path_xml}/ping_nemo_gelato.xml "
                      "{path_xml}/ping_nemo_ocnBgChem.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'CNRM-ESM2-1_1pctCO2-rad_r1i1p1f2'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "Ok")
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


# @unittest.skipUnless(False, "To be corrected")
class TestPiControl(unittest.TestCase, TestSimulation):
    """
    Test output generation for AOESM_piControl_CM6_r1_v2
    """
    def setUp(self):
        config = create_config_elements(
            simulation="AOESM_piControl_CM6_r1_v2",
            contexts=["nemo", "surfex", "trip"],
            year="1850",
            enddate="18510101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_nemo.xml {path_xml}/ping_nemo_gelato.xml "
                      "{path_xml}/ping_nemo_ocnBgChem.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'CNRM-ESM2-1_esm-piControl_r1i1p1f2_v2'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "To be corrected")
class TestSsp585(unittest.TestCase, TestSimulation):
    """
    Test output generation for AOESM_ssp585_CM6_r3
    """
    def setUp(self):
        config = create_config_elements(
            simulation="AOESM_ssp585_CM6_r3",
            contexts=["nemo", "surfex", "trip"],
            year="2015",
            enddate="20160101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_nemo.xml {path_xml}/ping_nemo_gelato.xml "
                      "{path_xml}/ping_nemo_ocnBgChem.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'CNRM-ESM2-1_ssp585_r3i1p1f2'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "To be corrected")
class TestC3SSF(unittest.TestCase, TestSimulation):
    """
    Test output generation for C3S_SF
    """
    def setUp(self):
        config = create_config_elements(
            simulation="C3S_SF",
            contexts=["nemo", "surfex", "trip"],
            year="2010",
            enddate="2011",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_nemo.xml {path_xml}/ping_trip.xml",
            attributes=[("EXPID", "H2010E001")]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "To be corrected")
class TestHistAer(unittest.TestCase, TestSimulation):
    """
    Test output generation for hist_aer_CM6_r4
    """
    def setUp(self):
        config = create_config_elements(
            simulation="hist_aer_CM6_r4",
            contexts=["nemo", "surfex", "trip"],
            year="1850",
            enddate="18510101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_nemo.xml {path_xml}/ping_nemo_gelato.xml "
                      "{path_xml}/ping_nemo_ocnBgChem.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'CNRM-CM6-1_hist-aer_r4i1p1f2'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "Ok")
class TestLGCM(unittest.TestCase, TestSimulation):
    """
    Test output generation for land_hist_LGCM
    """
    def setUp(self):
        config = create_config_elements(
            simulation="land_hist_LGCM",
            contexts=["surfex", "trip"],
            year="1850",
            enddate="18510101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'CNRM-CM6-1_land-hist_r1i1p1f2'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "Ok")
class TestLevels(unittest.TestCase, TestSimulation):
    """
    Test output generation for levels
    """
    def setUp(self):
        config = create_config_elements(
            simulation="levels",
            contexts=["surfex", "trip"],
            year="1960",
            enddate="19610101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'CNRM-CM6-1_a4SST_r1i1p1f2'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "To be corrected")
class TestPiClim(unittest.TestCase, TestSimulation):
    """
    Test output generation for piClim_anthro_AGCM_r1
    """
    def setUp(self):
        config = create_config_elements(
            simulation="piClim_anthro_AGCM_r1",
            contexts=["surfex", "trip"],
            year="1850",
            enddate="18510101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'CNRM-CM6-1_piClim-anthro_r1i1p1f2'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "To be corrected")
class TestCTL(unittest.TestCase, TestSimulation):
    """
    Test output generation for RCSM6_CTL
    """
    def setUp(self):
        config = create_config_elements(
            simulation="RCSM6_CTL",
            contexts=["surfex", "trip"],
            year="2009",
            enddate="20210101",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[('EXPID', 'RCSM6-CTL.3'),
                        ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                        ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "To be corrected")
class TestHIS(unittest.TestCase, TestSimulation):
    """
    Test output generation for RCSM6_HIS
    """
    def setUp(self):
        config = create_config_elements(
            simulation="RCSM6_HIS",
            contexts=["surfex", "trip"],
            year="1949",
            enddate="19490901",
            pingfiles="{path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[("EXPID", "RCSM6.1_HIS_SP0")]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


# @unittest.skipUnless(False, "To be corrected")
class TestHISLight(unittest.TestCase, TestSimulation):
    """
    Test output generation for RCSM6_HIS_light
    """
    def setUp(self):
        config = create_config_elements(
            simulation="RCSM6_HIS_light",
            contexts=["nemo", "surfex", "trip"],
            year="1949",
            enddate="19490901",
            pingfiles="{path_xml}/ping_nemo.xml {path_xml}/ping_surfex.xml {path_xml}/ping_trip.xml",
            attributes=[("EXPID", "RCSM6_HIS_light")]
        )
        for elt in config:
            setattr(self, elt, copy.deepcopy(config[elt]))


if __name__ == '__main__':
    unittest.main()
