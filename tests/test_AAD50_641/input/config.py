#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import os

from tests.tests_config import path_cv, path_xml
path_xml_aladin = "/".join([path_xml, "../xml_files_Aladin"])

path_simulation = os.getcwd()
simulation = "AAD50_641"
contexts = ["surfex", "trip"]

config = dict(
    year="2003",
    enddate="20030201",
    pingfiles="{}/ping_surfex.xml {}/ping_trip.xml".format(path_xml_aladin, path_xml_aladin),
    printout="1",
    cvs_path=path_cv,
    dummies="skip",
    dirname="./",
    prefix="IOXDIR",
    attributes=[("EXPID", "AAD50_641"),
                ],
    select="on_expt"
)
