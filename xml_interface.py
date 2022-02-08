#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between xml module and dr2xml.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict
from copy import copy, deepcopy
from functools import reduce
from io import open
import os
import json
import re

from xml.dom import minidom

import six

import xml_writer
from config import get_config_variable
from dr_interface import get_DR_version
from utils import decode_if_needed
from logger import get_logger
from settings_interface import get_variable_from_lset_with_default, get_variable_from_sset_with_default

projects_settings = None


def prepare_project_settings(dict_settings):
    if "parent_project_settings" in dict_settings:
        parent = dict_settings.pop("parent_project_settings")
        parent_settings = read_project_settings(parent)
        parent_settings = prepare_project_settings(parent_settings)
        for tag in dict_settings:
            if tag not in parent_settings:
                parent_settings[tag] = dict_settings[tag]
            else:
                if "attrs_list" in dict_settings[tag]:
                    parent_settings[tag]["attrs_list"] = dict_settings[tag]["attrs_list"]
                if "attrs_constraints" in dict_settings[tag]:
                    if "attrs_constraints" in parent_settings[tag]:
                        for key in dict_settings[tag]["attrs_constraints"]:
                            if key in parent_settings[tag]["attrs_constraints"]:
                                parent_settings[tag]["attrs_constraints"][key].update(
                                    dict_settings[tag]["attrs_constraints"][key]
                                )
                            else:
                                parent_settings[tag]["attrs_constraints"][key] = \
                                    dict_settings[tag]["attrs_constraints"][key]
                    else:
                        parent_settings[tag]["attrs_constraints"] = dict_settings[tag]["attrs_constraints"]
                if "vars_list" in dict_settings[tag]:
                    parent_settings[tag]["vars_list"] = dict_settings[tag]["vars_list"]
                if "vars_constraints" in dict_settings[tag]:
                    if "vars_constraints" in parent_settings[tag]:
                        for key in dict_settings[tag]["vars_constraints"]:
                            if key in parent_settings[tag]["vars_constraints"]:
                                parent_settings[tag]["vars_constraints"][key].update(
                                    dict_settings[tag]["vars_constraints"][key]
                                )
                            else:
                                parent_settings[tag]["vars_constraints"][key] = \
                                    dict_settings[tag]["vars_constraints"][key]
                    else:
                        parent_settings[tag]["vars_constraints"] = dict_settings[tag]["vars_constraints"]
    else:
        parent_settings = dict_settings
    return parent_settings


def reformat_settings(dict_settings):
    dict_settings = prepare_project_settings(dict_settings)
    for tag in dict_settings:
        if "attrs_list" not in dict_settings[tag]:
            dict_settings[tag]["attrs_list"] = list()
        dict_settings[tag]["attrs_constraints"] = \
            reformat_constraints(tag, dict_settings[tag].get("attrs_constraints", dict()),
                                 dict_settings[tag]["attrs_list"])
        if "vars_list" not in dict_settings[tag]:
            dict_settings[tag]["vars_list"] = list()
        dict_settings[tag]["vars_constraints"] = \
            reformat_constraints(tag, dict_settings[tag].get("vars_constraints", dict()),
                                 dict_settings[tag]["vars_list"])
    return dict_settings


regexp_default = re.compile(r"^(?P<default_name>.*)!:@(?P<default_src>.*)!:@(?P<format>.*)?$")
eq_regexp = re.compile(r"(?P<type_key>(key|val)):(?P<key>.*)==(?P<type_val>(key|val)):(?P<val>.*)")
neq_regexp = re.compile(r"(?P<type_key>(key|val)):(?P<key>.*)!=(?P<type_val>(key|val)):(?P<val>.*)")


def reformat_default_values(default_list):
    rep = list()
    for elt in default_list:
        match = regexp_default.match(elt)
        if match is not None:
            default_name = match.groupdict()["default_name"]
            default_src = match.groupdict()["default_src"]
            default_format = match.groupdict()["format"]
            if default_src in ["lab", "laboratory", "model"]:
                elt = get_variable_from_lset_with_default(default_name)
            elif default_src in ["sim", "simulation"]:
                elt = get_variable_from_sset_with_default(default_name)
            elif default_src in ["conf", "config", "configuration"]:
                elt = get_config_variable(default_name)
            elif default_src in ["DR_version", ]:
                elt = get_DR_version()
            elif default_src in ["dict"]:
                # TODO: Must be treated while evaluating
                pass
            else:
                raise ValueError("Unknown source for %s and %s" % (default_src, default_name))
            if default_format is not None:
                elt = default_format.format(elt)
        rep.append(elt)
    return rep


def reformat_constraints(tag, dict_constraints, list_keys):
    logger = get_logger()
    for key in list_keys:
        if key in dict_constraints:
            try:
                if "skip_values" not in dict_constraints[key]:
                    dict_constraints[key]["skip_values"] = list()
                if "authorized_types" in dict_constraints[key]:
                    if dict_constraints[key]["authorized_types"]:
                        val = [globals()["__builtins__"][val] for val in dict_constraints[key]["authorized_types"]]
                        if len(val) == 1:
                            val = val[0]
                        dict_constraints[key]["authorized_types"] = val
                else:
                    dict_constraints[key]["authorized_types"] = False
                if "default_values" in dict_constraints[key]:
                    if not isinstance(dict_constraints[key]["default_values"], list):
                        dict_constraints[key]["default_values"] = [dict_constraints[key]["default_values"], ]
                    dict_constraints[key]["default_values"] = \
                        reformat_default_values(dict_constraints[key]["default_values"])
                    if len(dict_constraints[key]["default_values"]) == 0:
                        dict_constraints[key]["is_default"] = False
                    elif "is_default" not in dict_constraints[key]:
                        dict_constraints[key]["is_default"] = True
                elif "default_values" not in dict_constraints[key]:
                    dict_constraints[key]["default_values"] = list()
                    dict_constraints[key]["is_default"] = False
                if "output_key" not in dict_constraints[key]:
                    dict_constraints[key]["output_key"] = key
                if "fatal" not in dict_constraints[key]:
                    dict_constraints[key]["fatal"] = False
                elif dict_constraints[key]["fatal"] in ["True", ]:
                    dict_constraints[key]["fatal"] = True
                else:
                    dict_constraints[key]["fatal"] = False
                if "num_type" not in dict_constraints[key]:
                    dict_constraints[key]["num_type"] = "string"
                if "conditions" not in dict_constraints[key]:
                    dict_constraints[key]["conditions"] = list()
                logger.debug("Constraints for tag %s and key %s: %s" % (tag, key, str(dict_constraints[key])))
            except:
                logger.error("Issue with tag %s and key %s" % (tag, key))
                raise
        else:
            dict_constraints[key] = dict(skip_values=list(), authorized_types=list(), default_values=None,
                                         is_default=False, output_key=key, fatal=False, num_type="string")
    return dict_constraints


def read_project_settings(filename):
    if not os.path.isfile(filename):
        filename = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "projects", "{}.json".format(filename)])
    return read_json_content(filename)


def read_json_content(filename):
    logger = get_logger()
    if os.path.isfile(filename):
        with open(filename) as fp:
            content = json.load(fp)
            return content
    else:
        logger.error("Could not find the file containing the project's settings at %s" %
                     filename)
        raise OSError("Could not find the file containing the project's settings at %s" %
                      filename)


def initialize_project_settings():
    global projects_settings
    logger = get_logger()
    if projects_settings is None:
        logger.debug("Initialize project_settings")
        project_settings_filename = get_variable_from_lset_with_default("project_settings", None)
        if project_settings_filename is not None:
            # If the project's settings filename is provided
            projects_settings = read_project_settings(project_settings_filename)
        else:
            # Get the default project's settings file content
            projects_settings = read_project_settings(get_variable_from_lset_with_default("project", "CMIP6"))
        projects_settings = reformat_settings(projects_settings)


class DR2XMLComment(xml_writer.Comment):

    def __init__(self, text):
        super(DR2XMLComment, self).__init__(comment=text)


class DR2XMLElement(xml_writer.Element):

    @staticmethod
    def check_value(value, authorized_types, skip_values):
        is_valid = True
        if authorized_types and not isinstance(value, authorized_types):
            is_valid = False
        if is_valid and str(value) in skip_values:
            is_valid = False
        return is_valid

    def find_value(self, key, value, is_value=True, authorized_types=False, skip_values=list(), is_default=False,
                   default_values=None, output_key=None, fatal=False, num_type="string", conditions=list()):
        logger = get_logger()
        if is_value:
            is_valid = self.check_value(value, authorized_types, skip_values)
            logger.debug("Check value %s for key %s... is proper? %s" % (value, key, is_valid))
        else:
            is_valid = False
            logger.debug("No specified value for key %s" % key)
        if is_default:
            i = 0
            while not is_valid and i < len(default_values):
                value = default_values[i]
                is_valid = self.check_value(value, authorized_types, skip_values)
                logger.debug("Check value %s for key %s... is proper? %s" % (value, key, is_valid))
                i += 1
        if not is_valid and fatal:
            logger.error("Could not find a proper value for attribute %s" % key)
            raise ValueError("Could not find a proper value for attribute %s" % key)
        else:
            return is_valid, output_key, value, num_type, conditions

    def __init__(self, tag, **kwargs):
        default_tag = kwargs.get("default_tag", tag)
        if "text" in kwargs:
            text = kwargs.pop("text")
        else:
            text = None
        tag_settings = projects_settings[default_tag]
        attrs_list = tag_settings["attrs_list"]
        attrs_constraints = tag_settings["attrs_constraints"]
        attrib = OrderedDict()
        for key in attrs_list:
            is_valid, output_key, value, num_type, conditions = \
                self.find_value(key=key, value=kwargs.get(key), is_value=key in kwargs, **attrs_constraints[key])
            if is_valid:
                attrib[output_key] = value
        super(DR2XMLElement, self).__init__(tag=tag, text=text, attrib=attrib)
        vars_list = tag_settings["vars_list"]
        vars_constraints = tag_settings["vars_constraints"]
        for var in vars_list:
            is_valid, output_var, value, num_type, conditions = \
                self.find_value(key=var, value=kwargs.get(var), is_value=var in kwargs, **vars_constraints[var])
            if is_valid and self.check_conditions(key, value, conditions, kwargs):
                self.append(wrv(output_var, value, num_type))

    def check_conditions(self, key, val, conditions, kwargs):
        rep = all([self.interprete_conditions(key, val, cond, kwargs) for cond in conditions])
        return rep

    @staticmethod
    def interprete_conditions(key, val, condition, kwargs):
        rep = True
        match = eq_regexp.match(condition)
        if match:
            type_key = match.groupdict()["type_key"]
            key_match = match.groupdict()["key"]
            type_val = match.groupdict()["type_val"]
            val_match = match.groupdict()["val"]
            if type_key in ["key"]:
                key_match = kwargs[key_match]
            if type_val in ["key"]:
                val_match = kwargs[val_match]
            if key_match != val_match:
                rep = False
        else:
            match = neq_regexp.match(condition)
            if match:
                type_key = match.groupdict()["type_key"]
                key_match = match.groupdict()["key"]
                type_val = match.groupdict()["type_val"]
                val_match = match.groupdict()["val"]
                if type_key in ["key"]:
                    key_match = kwargs[key_match]
                if type_val in ["key"]:
                    val_match = kwargs[val_match]
                if key_match != val_match:
                    rep = False
        return rep

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


def wr(out, key, dic_or_val=None, num_type="string", default=None):
    """
    Short cut for a repetitive pattern : add in 'out' a string variable name and value.
    The value of the XML variable created is defined using the following algorithm:

    - if ``dic_or_val`` is not ``None``:
        - if  ``dic_or_val`` is a ``dict``:
            - if ``key`` is in ``dic_or_val``:
                - ``value=dic_or_val[key]``
            - else if not ``default=False``:
                - ``value=default``
        - else if ``dic_or_val`` not ``None`` nor ``False``:
            - ``dic_or_val=value``
    - else use value of local variable ``key``

    :param out: XML element to which the variable will be added
    :param key: key to be put in variable
    :param dic_or_val: value or dictionary containing the value of the variable
    :param num_type: type of the value to be added (specfic requirements if string)
    :param default: default value to be use
    :return: Add an XML variable to ``out``.
    """
    logger = get_logger()
    print_variables = get_variable_from_lset_with_default("print_variables", True)
    if not print_variables:
        return
    elif isinstance(print_variables, list) and key not in print_variables:
        return

    val = None
    if isinstance(dic_or_val, (dict, OrderedDict)):
        if key in dic_or_val:
            val = dic_or_val[key]
        else:
            if default is not None:
                if default is not False:
                    val = default
            else:
                logger.warning('warning: %s not in dic and default is None' % key)
    else:
        if dic_or_val is not None:
            val = dic_or_val
        else:
            logger.error('error in wr,  no value provided for %s' % key)
    if val:
        if num_type in ["string", ]:
            # val=val.replace(">","&gt").replace("<","&lt").replace("&","&amp").replace("'","&apos").replace('"',"&quot").strip()
            val = val.replace(">", "&gt").replace("<", "&lt").strip()
            # CMIP6 spec : no more than 1024 char
            val = val[0:1024]
        if num_type not in ["string", ] or len(val) > 0:
            out.append(DR2XMLElement(tag="variable", text=val, name=key, type=num_type))


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
    if isinstance(value, list):
        value = reduce(lambda x, y: x + " " + y, value)
    if isinstance(value, six.string_types):
        value = value[0:1024]  # CMIP6 spec : no more than 1024 char
    # Format a 'variable' entry
    return DR2XMLElement(tag="variable", text=str(value), name=name, type=num_type)