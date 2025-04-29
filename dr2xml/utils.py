#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Several tools used in dr2xml.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict
from functools import reduce

import six

from utilities.logger import get_logger


class Dr2xmlError(Exception):
    """
    dr2xml generic exceptions.
    """
    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        logger = get_logger()
        logger.error(repr(self.valeur), )
        return "\n\n" + repr(self.valeur) + "\n\n"
    # """ just for test"""


class Dr2xmlGridError(Dr2xmlError):
    """
    Dr2xml grids specific exceptions.
    """
    pass


class VarsError(Dr2xmlError):
    """
    Vars specific exceptions.
    """
    pass


def print_struct(struct, skip_sep=False, sort=False, back_line=False):
    """

    :param struct:
    :param skip_sep:
    :param sort:
    :param back_line:
    :return:
    """
    if isinstance(struct, list):
        list_elt = [print_struct(elt) for elt in struct]
        if sort:
            list_elt = sorted(list_elt)
        rep = ", ".join(list_elt)
        if not skip_sep:
            rep = "[" + rep + "]"
        return rep
    elif isinstance(struct, tuple):
        rep = ", ".join([print_struct(elt) for elt in struct])
        if not skip_sep:
            rep = "(" + rep + ")"
        return rep
    elif isinstance(struct, (dict, OrderedDict)):
        list_keys = list(struct)
        if sort:
            list_keys = sorted(list_keys)
        if back_line:
            elements_sep = ",\n"
        else:
            elements_sep = ", "
        rep = elements_sep.join(["{} = {}".format(print_struct(key), print_struct(struct[key])) for key in list_keys])
        if not skip_sep:
            rep = "{" + rep + "}"
        return rep
    elif isinstance(struct, set):
        list_items = sorted(list(struct))
        rep = ", ".join([print_struct(elt) for elt in list_items])
        if not skip_sep:
            rep = "{" + rep + "}"
        return rep
    else:
        return "'{}'".format(struct)


def reduce_and_strip(elt):
    if isinstance(elt, list):
        elt = reduce(lambda x, y: x + " " + y, elt)
    if isinstance(elt, six.string_types):
        elt = elt.strip()
    return elt


def is_elt_applicable(elt, attribute=None, included=None, excluded=None):
    if attribute is not None:
        if isinstance(elt, tuple):
            attr = tuple([e.__getattribute__(attribute) for e in elt])
        else:
            attr = elt.__getattribute__(attribute)
    else:
        attr = elt
    test = True
    if test and excluded is not None and len(excluded) > 0 and attr in excluded:
        test = False
    if test and included is not None and len(included) > 0 and attr not in included:
        test = False
    return test


def convert_string_to_year(data):
    try:
        return int(float(data))
    except:
        logger = get_logger()
        logger.debug("Input data to convert to float: %s" % data)
        return None


def check_objects_equals(obj1, obj2):
    rep = isinstance(obj1, type(obj2))
    if rep:
        if isinstance(obj1, (list, tuple, set)):
            rep = sorted(list(obj1)) == sorted(list(obj2))
        elif isinstance(obj1, (dict, OrderedDict)):
            rep = check_objects_equals(list(obj1), list(obj2)) and all(obj1[elt] == obj2[elt] for elt in list(obj1))
        else:
            rep = obj1 == obj2
    return rep
