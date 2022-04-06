#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Prototype of xml writer to keep order.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import os

from .beacon import Beacon
from .element import Element
from .header import Header
from .comment import Comment
from .parser import xml_file_parser, parse_xml_string_rewrite
from .utils import encode_if_needed, decode_if_needed

if __name__ == "__main__":
    dr2xml_tests_dir = os.sep.join([os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]), "tests"])
    for my_xml_file in [
        os.sep.join([dr2xml_tests_dir, "tests_xml_writer.xml"]),
    ]:
        print(my_xml_file)
        text, comments, header, root_element = xml_file_parser(my_xml_file, verbose=False)
        print(text)
        print(comments)
        print(header)
        print(root_element)
