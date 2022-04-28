#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import os

from tests.tests_config import path_cv, path_xml

path_simulation = os.getcwd()
simulation = "hist_aer_CM6_r4"
contexts = ["nemo", "surfex", "trip"]

config = dict(
    year="1850",
    enddate= "18510101",
    pingfiles="{}/ping_surfex.xml {}/ping_nemo.xml {}/ping_nemo_gelato.xml {}/ping_nemo_ocnBgChem.xml "
              "{}/ping_trip.xml".format(path_xml, path_xml, path_xml, path_xml, path_xml),
    printout="1",
    cvs_path=path_cv,
    dummies="skip",
    dirname="./",
    prefix="IOXDIR",
    attributes=[('EXPID', 'CNRM-CM6-1_hist-aer_r4i1p1f2'),
                ('CMIP6_CV_version', 'cv=6.2.3.0-7-g2019642'),
                ('dr2xml_md5sum', '7040f60f6bf3118dc6c58b9fb8727d87')],
    select="on_expt"
)
