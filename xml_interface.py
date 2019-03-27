#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Interface between xml module and dr2xml.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import xml.etree.ElementTree as ET


def create_xml_element(tag, attrib=dict()):
    return ET.Element(tag=tag, attrib=attrib)


def create_xml_sub_element(xml_element, tag, attrib=dict()):
    return ET.SubElement(parent=xml_element, tag=tag, attrib=attrib)


def create_xml_element_from_string(string):
    return ET.fromstring(string)


def create_string_from_xml_element(xml_element):
    return ET.tostring(xml_element)


def dump_xml_element(xml_element):
    ET.dump(xml_element)


def parse_xml_file(xml_file):
    return ET.parse(xml_file)


def get_root_of_xml_file(xml_file):
    return parse_xml_file(xml_file).getroot()


def create_xml_string(tag, attrib):
    return create_string_from_xml_element(create_xml_element(tag, attrib))
