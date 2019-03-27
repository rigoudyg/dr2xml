#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Several tools used in dr2xml.
"""

from __future__ import print_function, division, absolute_import, unicode_literals


class dr2xml_error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        return "\n\n" + `self.valeur` + "\n\n"
    # """ just for test"""


class dr2xml_grid_error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        return `self.valeur`


class vars_error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        return "\n\n" + `self.valeur` + "\n\n"
