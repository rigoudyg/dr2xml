#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between xml module and dr2xml.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict
from io import open

from xml.dom import minidom

import xml_writer
from utils import decode_if_needed


def create_xml_element(tag, attrib=OrderedDict(), text=None):
    """

    :param tag:
    :param attrib:
    :param text:
    :return:
    """
    return xml_writer.Element(tag=tag, attrib=attrib, text=text)


def create_xml_sub_element(xml_element, tag, attrib=OrderedDict(), text=None):
    """

    :param xml_element:
    :param tag:
    :param attrib:
    :param text:
    :return:
    """
    subelement = xml_writer.Element(tag=tag, attrib=attrib, text=text)
    xml_element.append(subelement)


def create_xml_element_from_string(string):
    """

    :param string:
    :return:
    """
    return xml_writer.parse_xml_string_rewrite(string)


def create_string_from_xml_element(xml_element):
    """

    :param xml_element:
    :return:
    """
    return xml_element.dump()


def create_xml_comment(text):
    """

    :param text:
    :return:
    """
    return xml_writer.Comment(comment=text)


def add_xml_comment_to_element(element, text):
    """

    :param element:
    :param text:
    :return:
    """
    element.append(create_xml_comment(text))


def dump_xml_element(xml_element):
    """

    :param xml_element:
    :return:
    """
    return xml_element.dump()


def is_xml_element_to_parse(element):
    """

    :param element:
    :return:
    """
    return isinstance(element, xml_writer.element.Element)


def parse_xml_file(xml_file):
    """

    :param xml_file:
    :return:
    """
    return xml_writer.xml_file_parser(xml_file)


def get_root_of_xml_file(xml_file):
    """

    :param xml_file:
    :return:
    """
    text, comments, header, root_element = parse_xml_file(xml_file)
    return root_element


def create_xml_string(tag, attrib=OrderedDict(), text=None):
    """

    :param tag:
    :param attrib:
    :param text:
    :return:
    """
    return create_string_from_xml_element(create_xml_element(tag=tag, attrib=attrib, text=text))


def create_pretty_string_from_xml_element(xml_element):
    """

    :param xml_element:
    :return:
    """
    xml_str = create_string_from_xml_element(xml_element)
    reparsed = minidom.parseString(xml_str)
    return reparsed.toprettyxml(indent="\t", newl="\n", encoding="utf-8")


def create_header():
    """

    :return:
    """
    att_dict = OrderedDict()
    att_dict["version"] = "1.0"
    att_dict["encoding"] = "utf-8"
    return xml_writer.Header(tag="xml", attrib=att_dict)


def create_pretty_xml_doc(xml_element, filename):
    """

    :param xml_element:
    :param filename:
    :return:
    """
    with open(filename, "w", encoding="utf-8") as out:
        xml_header = create_header()
        out.write(decode_if_needed(xml_header.dump()))
        out.write("\n")
        out.write(decode_if_needed(xml_element.dump()))


def remove_subelement_in_xml_element(xml_element, tag=None, attrib=OrderedDict()):
    """

    :param xml_element:
    :param tag:
    :param attrib:
    :return:
    """
    children_to_remove = list()
    nb_conditions = len(attrib)
    if tag is not None:
        nb_conditions += 1
    for (rank, child) in enumerate(xml_element):
        to_remove = 0
        if tag is not None:
            if child.tag == tag:
                to_remove += 1
        for (key, value) in attrib.items():
            if key in child.attrib and child.attrib[key] == value:
                to_remove += 1
        if to_remove == nb_conditions:
            children_to_remove.append(child)
        else:
            xml_element[rank] = remove_subelement_in_xml_element(child, tag=tag, attrib=attrib)
    for child_to_remove in children_to_remove:
        xml_element.remove(child_to_remove)
    return xml_element
