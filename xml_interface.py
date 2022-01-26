#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between xml module and dr2xml.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict, defaultdict
from copy import copy, deepcopy
from io import open
import os
import json

from xml.dom import minidom

import xml_writer
from utils import decode_if_needed
from logger import get_logger
from settings_interface import get_variable_from_lset_with_default


projects_settings = None


def reformat_constraints(dict_constraints, list_keys):
    rep = defaultdict(dict)
    for key in list_keys:
        if key in dict_constraints:
            rep[key]["skip_values"] = dict_constraints[key].get("skip_values", list())
            if "authorized_types" in dict_constraints[key]:
                val = [globals()["__builtins__"][val] for val in dict_constraints[key]["authorized_types"]]
                if len(val) == 1:
                    val = val[0]
                rep[key]["authorized_types"] = val
            else:
                rep[key]["authorized_types"] = False
        else:
            rep[key]["skip_values"] = list()
            rep[key]["authorized_types"] = False
    return rep


def initialize_project_settings():
    global projects_settings
    logger = get_logger()
    if projects_settings is None:
        logger.debug("Initialize project_settings")
        project_settings_filename = get_variable_from_lset_with_default("project_settings", None)
        if project_settings_filename is not None:
            # If the project's settings filename is provided
            if os.path.isfile(project_settings_filename):
                with open(project_settings_filename) as fp:
                    projects_settings = json.load(fp)
            else:
                logger.error("Could not find the file containing the project's settings at %s" %
                             project_settings_filename)
                raise OSError("Could not find the file containing the project's settings at %s" %
                              project_settings_filename)
        else:
            # Get the default project's settings file content
            project = get_variable_from_lset_with_default("project", "CMIP6")
            project_settings_filename = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "projects",
                                                     "{}.json".format(project)])
            if os.path.isfile(project_settings_filename):
                with open(project_settings_filename) as fp:
                    projects_settings = json.load(fp)
            else:
                logger.error("Could not find the file containing the project's settings at %s" %
                             project_settings_filename)
                raise OSError("Could not find the file containing the project's settings at %s" %
                              project_settings_filename)
        for key in projects_settings:
            projects_settings[key]["attrs_constraints"] = \
                reformat_constraints(projects_settings[key]["attrs_constraints"], projects_settings[key]["attrs_list"])


class DR2XMLComment(xml_writer.Comment):

    def __init__(self, text):
        super(DR2XMLComment, self).__init__(comment=text)


class DR2XMLElement(xml_writer.Element):

    def __init__(self, tag, **kwargs):
        default_tag = kwargs.get("default_tag", tag)
        if "text" in kwargs:
            text = kwargs.pop("text")
        else:
            text = None
        tag_settings = projects_settings[default_tag]
        list_attrs = tag_settings["attrs_list"]
        attrs_constraints = tag_settings["attrs_constraints"]
        attrib = OrderedDict()
        for key in [key for key in list_attrs if key in kwargs]:
            value = kwargs[key]
            if (not(attrs_constraints[key]["authorized_types"]) or
                    (attrs_constraints[key]["authorized_types"] and
                     isinstance(value, attrs_constraints[key]["authorized_types"]))) and \
                    str(value) not in attrs_constraints[key].get("skip_values", list()):
                attrib[key] = kwargs[key]
        super(DR2XMLElement, self).__init__(tag=tag, text=text, attrib=attrib)

    def __copy__(self):
        """

        :return:
        """
        element = type(self).__call__(tag=self.tag, text=self.text, **deepcopy(self.attrib))
        element.update_level(self.level)
        for child in self.children:
            element.children.append(copy(child))
        return element


def is_xml_element_to_parse(element):
    """

    :param element:
    :return:
    """
    return isinstance(element, xml_writer.element.Element)


def parse_xml_file(xml_file, follow_src=False, path_parse="./", dont_read=list()):
    """

    :param xml_file:
    :return:
    """
    return xml_writer.xml_file_parser(xml_file, follow_src=follow_src, path_parse=path_parse, dont_read=dont_read)


def get_root_of_xml_file(xml_file, follow_src=False, path_parse="./", dont_read=list()):
    """

    :param xml_file:
    :return:
    """
    text, comments, header, root_element = parse_xml_file(xml_file, follow_src=follow_src, path_parse=path_parse,
                                                          dont_read=dont_read)
    return root_element


def create_pretty_string_from_xml_element(xml_element):
    """

    :param xml_element:
    :return:
    """
    xml_str = str(xml_element)
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


def find_rank_xml_subelement(xml_element, tag=list(), not_tag=list(), **keyval):
    if not isinstance(tag, (list, tuple)):
        tag = [tag, ]
    if not isinstance(not_tag, (list, tuple)):
        not_tag = [not_tag, ]
    if not is_xml_element_to_parse(xml_element):
        raise ValueError("Could not deal with type %s" % type(xml_element))
    else:
        return [i for (i, elt) in enumerate(xml_element) if (len(tag) == 0 or elt.tag in tag) and
                (len(not_tag) == 0 or elt.tag not in not_tag) and
                (all([key in elt.attrib and (keyval[key] is None or elt.attrib[key] in keyval[key])
                      for key in keyval]))]
