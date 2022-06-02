#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import os

from tests.tests_config import path_cv, path_xml
path_xml_aladin = "/".join([path_xml, "../xml_files_RCSM6_HIS"])

path_simulation = os.getcwd()
simulation = "RCSM6_HIS"
contexts = ["nemo", "surfex", "trip"]

config = dict(
    year="1949",
    enddate="19490901",
    pingfiles="{}/ping_nemo.xml {}/ping_surfex.xml {}/ping_trip.xml".format(path_xml_aladin, path_xml_aladin,
                                                                            path_xml_aladin),
    printout=True,
    cvs_path=path_cv,
    dummies="skip",
    dirname="./",
    prefix="IOXDIR",
    attributes=[("EXPID", "RCSM6.1_HIS_SP0"),
                ],
    select="on_expt"
)
