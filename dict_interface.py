#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Interface to get and set laboratory and simulations dictionaries.
"""

import copy

from utils import dr2xml_error


# Initial simulation (sset) and laboratory (lset) dictionaries
sset = None
lset = None


def initialize_dict(new_lset=None, new_sset=None):
    global sset, lset
    if new_lset is not None:
        lset = copy.deepcopy(new_lset)
    if new_sset is not None:
        sset = copy.deepcopy(new_sset)


def get_variable_from_sset_else_lset_with_default(key_sset, key_lset=None, default=None):
    """
    Find the best value by looking at the different dictionaries
    :param key_sset: a key to be looked for in the simulation dictionary
    :param key_lset: a key to be looked for in the laboratory dictionary
    :param default: the default value to put
    :return: the value associated with the specified key in the sset dictionary if exists,
    else in the lset dictionary, else default
    """
    if key_lset is None:
        key_lset = key_sset
    return sset.get(key_sset, lset.get(key_lset, default))


def get_variable_from_sset_and_lset_without_default(key_sset, key_lset=None):
    if key_lset is None:
        key_lset = key_sset
    if sset and key_sset in sset:
        return sset[key_sset]
    else:
        return lset[key_lset]


def get_variable_from_lset_with_default(key, default):
    return lset.get(key, default)


def get_variable_from_lset_without_default(*args):
    result = None
    nb_levels = len(args)
    for level in range(nb_levels):
        if level == 0:
            result = lset[args[level]]
        else:
            result = result[args[level]]
    return result


def get_variable_from_sset_with_default(key, default):
    return sset.get(key, default)


def get_variable_from_sset_with_default_in_sset(key, key_default):
    return sset.get(key, sset[key_default])


def get_variable_from_sset_without_default(*args):
    result = None
    nb_levels = len(args)
    for level in range(nb_levels):
        if level == 0:
            result = sset[args[level]]
        else:
            result = result[args[level]]
    return result


def is_key_in_lset(key):
    return lset and (key in lset)


def is_key_in_sset(key):
    return sset and (key in sset)


def is_sset_not_None():
    return sset


def get_lset_iteritems():
    return lset.iteritems()


def get_sset_iteritems():
    return sset.iteritems()


def get_source_id_and_type():
    if "configuration" in sset and "configurations" in lset:
        if sset["configuration"] in lset["configurations"]:
            source_id, source_type, unused = lset["configurations"][sset["configuration"]]
        else:
            raise dr2xml_error("configuration %s is not known (allowed values are :)" % \
                               sset["configuration"] + `lset["configurations"]`)
    else:
        source_id = sset['source_id']
        if 'source_type' in sset:
            source_type = sset['source_type']
        else:
            if 'source_types' in lset:
                source_type = lset['source_types'][source_id]
            else:
                raise dr2xml_error("Fatal: No source-type found - Check inputs")
    return source_id, source_type
