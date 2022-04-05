#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface to get and set laboratory and simulations dictionaries.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import copy
from collections import OrderedDict
from six import string_types

from utils import Dr2xmlError, decode_if_needed, print_struct

from logger import get_logger


# Initial simulation (sset) and laboratory (lset) dictionaries
sset = None
lset = None


def initialize_dict(new_lset=None, new_sset=None):
    """

    :param new_lset:
    :param new_sset:
    :return:
    """
    global sset, lset
    if new_lset is not None:
        lset = decode_strings_in_dict(new_lset)
    if new_sset is not None:
        sset = decode_strings_in_dict(new_sset)


def decode_strings(struct):
    """

    :param struct:
    :return:
    """
    logger = get_logger()
    if isinstance(struct, (int, float)):
        return struct
    elif isinstance(struct, (string_types, type(None))):
        struct = str(struct)
        struct = decode_if_needed(struct)
        return struct
    elif isinstance(struct, (dict, OrderedDict)):
        return decode_strings_in_dict(struct)
    elif isinstance(struct, list):
        return decode_strings_in_list(struct)
    elif isinstance(struct, tuple):
        return decode_strings_in_tuple(struct)
    elif isinstance(struct, set):
        return decode_strings_in_set(struct)
    else:
        logger.error("Type of value %s is not handled by dr2xml, please report it the development team." % type(struct))
        raise TypeError("Type of value %s is not handled by dr2xml, please report it the development team."
                        % type(struct))


def decode_strings_in_dict(init_dict):
    """

    :param init_dict:
    :return:
    """
    new_dictionary = OrderedDict()
    for key in sorted(list(init_dict)):
        value = init_dict[key]
        value = decode_strings(value)
        new_dictionary[key] = value
    return new_dictionary


def decode_strings_in_set(init_set):
    """

    :param init_set:
    :return:
    """
    new_set = set(decode_strings_in_list(list(init_set)))
    return new_set


def decode_strings_in_list(init_list):
    """

    :param init_list:
    :return:
    """
    new_list = list()
    for value in init_list:
        new_list.append(decode_strings(value))
    return new_list


def decode_strings_in_tuple(init_tuple):
    """

    :param init_tuple:
    :return:
    """
    new_tuple = list()
    for value in init_tuple:
        new_tuple.append(value)
    new_tuple = decode_strings_in_list(new_tuple)
    new_tuple = tuple(new_tuple)
    return new_tuple


def format_dict_for_printing(dictionary):
    """

    :param dictionary:
    :return:
    """
    if dictionary in ["lset", ]:
        dictionary = lset
    elif dictionary in ["sset", ]:
        dictionary = sset
    return print_struct(dictionary, back_line=True, sort=True)


def get_variable_from_lset_with_default(key, default=None):
    """

    :param key:
    :param default:
    :return:
    """
    return lset.get(key, default)


def get_variable_from_lset_with_default_in_lset(key, key_default, default=None):
    """

    :param key:
    :param key_default:
    :param default:
    :return:
    """
    return lset.get(key, lset.get(key_default, default))


def get_variable_from_lset_without_default(*args):
    """

    :param args:
    :return:
    """
    return get_variable_from_dict_without_default(dictionary=lset, args=args)


def get_variable_from_dict_without_default(dictionary, args):
    """

    :param dictionary:
    :param args:
    :return:
    """
    if len(args) > 1:
        newdict = copy.deepcopy(dictionary[args[0]])
        return get_variable_from_dict_without_default(dictionary=newdict, args=args[1:])
    elif len(args) == 1:
        return dictionary[args[0]]
    else:  # Should not happen
        raise Dr2xmlError("Could not guess which key to look for.")


def get_variable_from_sset_without_default(*args):
    """

    :param args:
    :return:
    """
    return get_variable_from_dict_without_default(dictionary=sset, args=args)


def is_key_in_lset(key):
    """

    :param key:
    :return:
    """
    return lset and (key in lset)


def is_key_in_sset(key):
    """

    :param key:
    :return:
    """
    return sset and (key in sset)


def is_sset_not_None():
    """

    :return:
    """
    return sset is not None
