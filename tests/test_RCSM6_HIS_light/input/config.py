#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import os

from tests.tests_config import path_cv

path_simulation = os.getcwd()
simulation = "RCSM6_HIS_light"
contexts = ["nemo", "surfex", "trip"]
path_table = os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), "tables"])
path_homedr = os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), "home_data_request"])
path_xml = path_homedr

config = dict(
    year="1949",
    enddate="19491001",
    pingfiles="{}/ping_nemo.xml {}/ping_surfex.xml {}/ping_trip.xml".format(path_xml, path_xml, path_xml),
    printout="1",
    cvs_path=path_cv,
    dummies="skip",
    dirname="./",
    prefix="IOXDIR",
    attributes=[("EXPID", "RCSM6_HIS_light"),
                ("CMIP6_CV_version", "cv=6.2.3.0-7-g2019642"),
                ("dr2xml_md5sum", "7040f60f6bf3118dc6c58b9fb8727d87")
                ],
    select="on_expt"
)
