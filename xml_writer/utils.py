#!/usr/bin/python
# coding: utf-8

"""
Utilities used by xml_writer.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import re
import sys
from collections import OrderedDict


def encode_if_needed(a_string, encoding="utf-8"):
    if sys.version.startswith("2."):
        return a_string.encode(encoding)
    elif sys.version.startswith("3."):
        return a_string
    else:
        raise OSError("Unknown Python version %s", sys.version.split()[0])


def decode_if_needed(a_string, encoding="utf-8"):
    if sys.version.startswith("2."):
        return a_string.decode(encoding)
    elif sys.version.startswith("3."):
        return a_string
    else:
        raise OSError("Unknown Python version %s", sys.version.split()[0])


# XML dict regexp
_generic_dict_regexp = r'(?P<attrib>(\s(\w+\s?=\s?"([^"])*"\s?))*)'
_dict_regexp = re.compile(r'(?P<key>\w+)\s?=\s?"(?P<value>[^"]*)"')


def _build_dict_attrib(dict_string):
    attrib = OrderedDict()
    if dict_string and len(dict_string) > 0:
        dict_string = dict_string.strip()
        string_match = _dict_regexp.findall(dict_string)
        for (key, value) in string_match:
            value = value.strip().replace('"', '')
            attrib[key] = value
    return attrib


def _find_text(xml_string, fatal=False, verbose=False):
    xml_string = xml_string.strip()
    if verbose:
        print("<<<find_text: XML_STRING before>>>", len(xml_string), xml_string)
    rank_start_init_element = xml_string.find("<")
    rank_end_last_element = xml_string.rfind(">")
    if rank_start_init_element < 0 and rank_end_last_element < 0:
        if fatal:
            raise Exception("Could not find initial and final beacons.")
        else:
            xml_text = xml_string
            xml_string = ""
    elif rank_start_init_element < 0 or rank_end_last_element < 0:
        raise Exception("It seems that there is a problem in the XML file...")
    else:
        if rank_end_last_element < len(xml_string) - 1:
            end_text = xml_string[(rank_end_last_element + 1):]
            xml_string = xml_string[0:(rank_end_last_element + 1)]
        else:
            end_text = ""
        if rank_start_init_element > 0:
            init_text = xml_string[0:rank_start_init_element]
            xml_string = xml_string[rank_start_init_element:]
        else:
            init_text = ""
        xml_text = " ".join([init_text, end_text])
    xml_text = xml_text.strip()
    if verbose:
        print("<<<find_text: TEXT after>>>", len(xml_text), xml_text)
    xml_string = xml_string.strip()
    if verbose:
        print("<<<find_text: XML_STRING after>>>", len(xml_string), xml_string)
    return xml_string, xml_text
