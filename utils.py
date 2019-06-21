#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Several tools used in dr2xml.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict


class dr2xml_error(Exception):
    """
    dr2xml generic exceptions.
    """
    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        return "\n\n" + repr(self.valeur) + "\n\n"
    # """ just for test"""


class dr2xml_grid_error(Exception):
    """
    Dr2xml grids specific exceptions.
    """
    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        return repr(self.valeur)


class vars_error(Exception):
    """
    Vars specific exceptions.
    """
    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        return "\n\n" + repr(self.valeur) + "\n\n"


def build_ordered_dict(**kwargs):
    """
    In Python 3.6 and above, this function can be used to build OrderedDict by specifying all args in the desired order.
    """
    rep = OrderedDict()
    for (key, value) in kwargs.items():
        rep[key] = value
    return rep