#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import os

from tests.tests_config import path_cv, path_xml

path_simulation = os.getcwd()
simulation = "C3S_SF"
contexts = ["surfex", "trip"]

config = dict(
    year="2010",
    enddate= "2011",
    pingfiles="{}/ping_surfex.xml {}/ping_trip.xml".format(path_xml, path_xml),
    printout="1",
    cvs_path=path_cv,
    dummies="skip",
    dirname="./",
    attributes=[("EXPID", "H2010E001")
                ],
    select="on_expt"
)
