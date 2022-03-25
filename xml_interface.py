#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between xml module and dr2xml.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import pprint
from collections import OrderedDict
import six

import xml_writer
from logger import get_logger
from json_interface import setup_project_settings, find_value
from settings_interface import get_variable_from_lset_with_default
from utils import reduce_and_strip, decode_if_needed

projects_settings = None


def initialize_project_settings(**kwargs):
    global projects_settings
    logger = get_logger()
    logger.debug("Initialize project_settings")
    # If no filename is specified, get the one associated with the project
    projects_settings = setup_project_settings(**kwargs)
    pprint.pprint(projects_settings)


def get_project_settings(*args, is_default=False, default=None):
    if len(args) == 0:
        return projects_settings
    else:
        val = projects_settings
        test = True
        i = 0
        while test and i < len(args):
            if args[i] in val:
                val = val[args[i]]
                i += 1
            else:
                test = False
        if test:
            return val
        elif not is_default:
            raise ValueError("Could not find a proper value: %s not in %s" % (args[i], val))
        else:
            return default


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
        tag_settings = copy.deepcopy(projects_settings[default_tag])
        attrs_list = tag_settings["attrs_list"]
        attrs_constraints = tag_settings["attrs_constraints"]
        attrib = OrderedDict()
        common_dict = projects_settings["__common_values__"]
        for key in attrs_list:
            test, value, output_dict = find_value(tag=tag, key=key, value=kwargs.get(key),
                                                  is_default_value=key not in kwargs, common_dict=common_dict,
                                                  additional_dict=kwargs, **attrs_constraints[key])
            if test:
                attrib[output_dict["output_key"]] = value
        super(DR2XMLElement, self).__init__(tag=tag, text=text, attrib=attrib)
        vars_list = tag_settings["vars_list"]
        vars_constraints = tag_settings["vars_constraints"]
        for var in vars_list:
            test, value, output_dict = find_value(tag=tag, key=var, value=kwargs.get(var),
                                                  is_default_value=var not in kwargs, common_dict=common_dict,
                                                  additional_dict=kwargs, **vars_constraints[var])
            if test:
                self.append(wrv(output_dict["output_key"], value, output_dict["num_type"]))

    def __copy__(self):
        """

        :return:
        """
        element = type(self).__call__(tag=self.tag, text=self.text, **copy.deepcopy(self.attrib))
        element.update_level(self.level)
        for child in self.children:
            element.children.append(copy.copy(child))
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


def wrv(name, value, num_type="string"):
    """
    Create a string corresponding of a variable for Xios files.
    :param name: name of the variable
    :param value: value of the variable
    :param num_type: type of the variable
    :return: string corresponding to the xml variable
    """
    print_variables = get_variable_from_lset_with_default("print_variables", True)
    if not print_variables:
        return None
    elif isinstance(print_variables, list) and name not in print_variables:
        return None
    else:
        value = reduce_and_strip(value)
        if isinstance(value, six.string_types):
            value = value.replace(">", "&gt").replace("<", "&lt")
            value = value[0:1024]  # CMIP6 spec : no more than 1024 char
            value = value.strip()
        # Format a 'variable' entry
        return DR2XMLElement(tag="variable", text=str(value), name=name, type=num_type)
