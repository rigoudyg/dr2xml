#!/usr/bin/python
# coding: utf-8

"""
Parser tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from io import open

from xml_writer.comment import _find_xml_comment
from xml_writer.element import _find_one_part_element, _find_two_parts_element, _build_element
from xml_writer.header import _find_xml_header
from xml_writer.pre_treament import _pre_xml_string_format
from xml_writer.utils import _find_text


def xml_parser(xml_string, verbose=False):
    xml_string = _pre_xml_string_format(xml_string, verbose=verbose)
    final_text = None
    comments = list()
    root_element = None
    header = None
    if len(xml_string) > 0:
        # Check init or end text (there should not have been any but let's check
        xml_string, final_text = _find_text(xml_string, fatal=True)
        # Check for header
        if len(xml_string) > 0:
            xml_string, header = _find_xml_header(xml_string, verbose=verbose)
        comment = True
        while comment and len(xml_string) > 0:
            xml_string, comment = _find_xml_comment(xml_string, verbose=verbose)
            if comment is not None:
                comments.append(comment)
            xml_string = xml_string.strip()
        # Check for root element (there should not have comment at this place)
        if len(xml_string) > 0:
            xml_string, root_element = _find_one_part_element(xml_string, verbose=verbose)
            xml_string = xml_string.strip()
            if root_element is None:
                xml_string, root_element = _find_two_parts_element(xml_string, verbose=verbose)
                xml_string = xml_string.strip()
            if root_element is None:
                raise Exception("Could not guess what the root element could be...")
        # Check for additional comments
        comment = True
        while len(xml_string) > 0 and comment:
            xml_string, comment = _build_element(xml_string, verbose=verbose)
            if comment is None:
                raise Exception("It seems that there was something that is not a comment after the root element...")
            else:
                comments.append(comment)
        # Check that len of xml_string is 0
        if len(xml_string) > 0:
            raise Exception("The XML string should follow the pattern: header comment root_xml_element comment")
    return final_text, comments, header, root_element


def xml_file_parser(xml_file, verbose=False):
    with open(xml_file, "rb") as opened_file:
        xml_content = opened_file.readlines()
    xml_string = "\n".join([line.decode("utf-8") for line in xml_content])
    return xml_parser(xml_string, verbose=verbose)