#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import os

from tests.tests_config import path_cv, path_xml

path_simulation = os.getcwd()
simulation = "amip_ESM"
contexts = ["surfex", "trip"]

config = dict(
    year="1979",
    enddate="19800101",
    pingfiles="{}/ping_surfex.xml {}/ping_trip.xml".format(path_xml, path_xml),
    printout=False,
    cvs_path=path_cv,
    dummies="skip",
    dirname="./",
    prefix="IOXDIR",
    attributes=[('EXPID', 'amipESM-CEDS2021-aerdiffus'),
                ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                ('dr2xml_md5sum', '7a4dce8aef3dd4c1443dcfc57c36cbe7')],
    select="on_expt"
)