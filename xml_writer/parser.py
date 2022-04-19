#!/usr/bin/env python
# coding: utf-8

"""
Parser tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import os
import re
from io import open

from .element import Element
from .comment import _find_xml_comment
from .header import _find_xml_header
from .pre_treatment import _pre_xml_string_format
from .utils import _find_text, print_if_needed, iterate_on_string, _generic_dict_regexp, _build_dict_attrib


def xml_file_parser(xml_file, verbose=False, follow_src=False, path_parse="./", dont_read=list()):
    """

    :param xml_file:
    :param verbose:
    :return:
    """
    with open(xml_file, "rb") as opened_file:
        xml_content = opened_file.readlines()
    xml_string = "\n".join([line.decode("utf-8") for line in xml_content])
    xml_string = _pre_xml_string_format(xml_string, verbose=verbose)
    return parse_xml_string_rewrite(xml_string, verbose=verbose, follow_src=follow_src, path_parse=path_parse,
                                    dont_read=dont_read)


def parse_xml_string_rewrite(xml_string, verbose=False, follow_src=False, path_parse="./", dont_read=list()):
    """

    :param xml_string:
    :param verbose:
    :return:
    """
    # Build the list of xml elements from the xml_string
    list_of_elements = generate_list_from_xml_string(xml_string, verbose=verbose, follow_src=follow_src,
                                                     path_parse=path_parse, dont_read=dont_read)
    # Build the xml tree from the built list
    list_of_elements, root_element, texts, comments, headers = generate_xml_tree_from_list(list_of_elements,
                                                                                           verbose=verbose)
    texts = "\n".join(texts)
    if len(headers) > 1:
        raise Exception("Multiple headers are not possible.")
    elif len(headers) == 1:
        headers = headers[0]
    else:
        headers = None
    if len(root_element) > 1:
        raise Exception("There must be only one root element.")
    elif len(root_element) == 1:
        root_element = root_element[0]
    else:
        root_element = None
    return texts, comments, headers, root_element


def generate_list_from_xml_string(xml_string, verbose=False, follow_src=False, path_parse="./", dont_read=list()):
    """

    :param xml_string:
    :param verbose:
    :return:
    """
    list_of_elements = list()
    remained_xml_string = ""
    level = 0
    tags = list()
    separator = ">"
    # Loop on substrings of xml_string
    for (sub_xml_string, pos_init) in iterate_on_string(xml_string, separator=separator, verbose=verbose):
        # Take into account what remains from the previous loop if any
        sub_xml_string = remained_xml_string + sub_xml_string
        # Check if some elements could be found there
        elt_found = True
        while len(sub_xml_string) > 0 and elt_found is not None:
            if len(tags) > 0:
                tag = tags[-1]
            else:
                tag = None
            (sub_xml_string, tuple_info) = find_next_element(sub_xml_string, level=level, tag=tag, verbose=verbose,
                                                             follow_src=follow_src, path_parse=path_parse,
                                                             dont_read=dont_read)
            (level, elt_type, elt_found) = tuple_info
            if elt_type is not None:
                list_of_elements.append((level, elt_type, elt_found))
                if elt_type == "start_two_parts_element":
                    tags.append(elt_found.tag)
                    level += 1
                elif elt_type == "end_two_parts_element":
                    tags.pop()
        # Update the remaining string
        remained_xml_string = sub_xml_string
    # At this stage, the input string should be empty
    if len(remained_xml_string) > 0:
        raise Exception("All the xml string should have been treated...%s..." % remained_xml_string)
    else:
        return list_of_elements


def generate_xml_tree_from_list(list_of_elements, verbose=False):
    """

    :param list_of_elements:
    :param verbose:
    :return:
    """
    current_elts = list()
    list_of_texts = list()
    list_of_comments = list()
    list_of_headers = list()
    is_complete = False
    while len(list_of_elements) > 0 and not is_complete:
        (level, elt_type, elt) = list_of_elements.pop(0)
        print_if_needed("<<<generate_xml_tree>>>", level, elt_type, elt, verbose=verbose)
        if elt_type == "text":
            list_of_texts.append(elt)
        elif elt_type == "comment":
            if level == 0:
                list_of_comments.append(elt)
            else:
                current_elts.append(elt)
        elif elt_type == "header":
            if level == 0:
                list_of_headers.append(elt)
            else:
                raise Exception("Header must be on top level.")
        elif elt_type == "single_part_element":
            current_elts.append(elt)
        elif elt_type == "start_two_parts_element":
            list_of_elements, child_elts, child_texts, child_comments, child_headers = \
                generate_xml_tree_from_list(list_of_elements, verbose=verbose)
            elt.extend(child_elts)
            for text in child_texts:
                elt.set_text(text)
            current_elts.append(elt)
        elif elt_type == "end_two_parts_element":
            is_complete = True
        else:
            raise Exception("Unknown element type %s" % elt_type)
    if level != 0 and not is_complete:
        raise Exception("There is a problem with the xml tree.")
    return list_of_elements, current_elts, list_of_texts, list_of_comments, list_of_headers


def find_next_element(xml_string, level=0, tag=None, verbose=False, follow_src=False, path_parse="./",
                      dont_read=list()):
    """

    :param xml_string:
    :param level:
    :param tag:
    :param verbose:
    :return:
    """
    xml_string = xml_string.strip()
    print_if_needed(xml_string, verbose=verbose)
    # Check if the element is some text
    xml_string, find_element = _find_text(xml_string, fatal=False)
    if len(find_element) == 0:
        find_element = None
    if find_element is not None:
        print_if_needed("<<<Text found>>>", find_element, verbose=verbose)
        return xml_string, (level, "text", find_element)
    else:
        # Check if the element is a header
        xml_string, find_element = _find_xml_header(xml_string, verbose=verbose)
        if find_element is not None:
            print_if_needed("<<<Header found>>>", find_element, verbose=verbose)
            return xml_string, (level, "header", find_element)
        else:
            # Check if the element is a comment
            xml_string, find_element = _find_xml_comment(xml_string, verbose=verbose)
            if find_element is not None:
                print_if_needed("<<<Comment found>>>", find_element, verbose=verbose)
                return xml_string, (level, "comment", find_element)
            else:
                # Check if the element is a single part element
                xml_string, find_element = _find_one_part_element(xml_string, verbose=verbose, follow_src=follow_src,
                                                                  path_parse=path_parse, dont_read=dont_read)
                if find_element is not None:
                    print_if_needed("<<<Single part element found>>>", find_element, verbose=verbose)
                    return xml_string, (level, "single_part_element", find_element)
                else:
                    # Check if a new double parts element is opening
                    xml_string, find_element = _find_two_parts_element_init(xml_string, verbose=verbose,
                                                                            follow_src=follow_src,
                                                                            path_parse=path_parse, dont_read=dont_read)
                    if find_element is not None:
                        print_if_needed("<<<Double part element found (%d nested)>>>" % (level + 1),
                                        find_element, verbose=verbose)
                        return xml_string, (level, "start_two_parts_element", find_element)
                    elif tag is not None and level > 0:
                        # Check if the current double parts element is closing
                        xml_string, find_element = _find_two_parts_element_end(xml_string, tag, verbose=verbose)
                        if find_element is not None:
                            print_if_needed("<<<Closing double part element found (%d nested)>>>" % level, tag,
                                            find_element, verbose=verbose)
                            return xml_string, (level - 1, "end_two_parts_element", None)
                        else:
                            return xml_string, (level, None, None)
                    else:
                        return xml_string, (level, None, None)


def read_src(src, follow_src=False, path_parse="./", dont_read=list(), verbose=False):
    if not src.startswith(os.path.sep) and path_parse not in ["./", ]:
        filen = os.path.sep.join([path_parse, src])
    else:
        filen = src
    if not any([os.path.basename(filen).startswith(prefix) for prefix in dont_read]):
        print_if_needed("Reading %s" % filen, verbose=verbose)
        texts, comments, headers, root_element = xml_file_parser(filen, follow_src=follow_src, path_parse=path_parse,
                                                                 dont_read=dont_read, verbose=verbose)
        return root_element
    else:
        return None


#: XML single part regexp
_xml_single_part_element_regexp = re.compile(r'^\s?(?P<all><\s?(?P<tag>\w+)\s?{}\s?/>)\s?'.format(
    _generic_dict_regexp))


def _find_one_part_element(xml_string, verbose=False, follow_src=False, path_parse="./", dont_read=list()):
    """

    :param xml_string:
    :param verbose:
    :return:
    """
    print_if_needed("<<<find_one_part_element BEFORE>>>", len(xml_string), xml_string, verbose=verbose)
    xml_string = xml_string.strip()
    match_single_part = _xml_single_part_element_regexp.match(xml_string)
    if match_single_part:
        match_single_part = match_single_part.groupdict()
        tag = match_single_part["tag"].strip()
        attrib = _build_dict_attrib(match_single_part["attrib"])
        if follow_src and "src" in attrib:
            src = attrib.pop("src")
            child = read_src(src, path_parse=path_parse, dont_read=dont_read, verbose=verbose, follow_src=follow_src)
            if child is not None and child.tag == tag:
                attrib.update(child.attrib)
                element = Element(tag=tag, attrib=attrib)
                element.extend(child[:])
            elif child is not None:
                element = Element(tag=tag, attrib=attrib)
                element.append(child)
            else:
                element = Element(tag=tag, attrib=attrib)
        else:
            element = Element(tag=tag, attrib=attrib)
        xml_string = xml_string.replace(match_single_part["all"], "", 1)
        print_if_needed("<<<find_one_part_element AFTER>>>", len(xml_string), xml_string, verbose=verbose)
        return xml_string, element
    else:
        return xml_string, None


#: XML two parts regexp
_xml_string_first_element_replace = \
    r'(?P<all_begin>\s?(?P<begin><\s?(?P<tag>{}){}\s?>)\s?)'.format('{}', _generic_dict_regexp)
_xml_string_init_element_replace = r'^'+_xml_string_first_element_replace
_xml_init_two_parts_element_regexp = re.compile(_xml_string_init_element_replace.format(r"\w+\s?"))
_xml_string_end_element_replace = r'(?P<all_end>\s?(?P<end></\s?{}\s?>)\s?)'


def _find_two_parts_element_init(xml_string, verbose=False, follow_src=False, path_parse="./", dont_read=list()):
    """

    :param xml_string:
    :param verbose:
    :return:
    """
    xml_string = xml_string.strip()
    match = _xml_init_two_parts_element_regexp.match(xml_string)
    if not match:
        return xml_string, None
    else:
        match_group_dict = match.groupdict()
        begin = match_group_dict["begin"]
        tag = match_group_dict["tag"]
        attrib = match_group_dict["attrib"]
        attrib = _build_dict_attrib(attrib)
        if follow_src and "src" in attrib:
            src = attrib.pop("src")
            child = read_src(src, path_parse=path_parse, dont_read=dont_read, verbose=verbose, follow_src=follow_src)
            element = Element(tag=tag, attrib=attrib)
            if child is not None and child.tag == tag and (len(child.attrib) == 0 or child.attrib == attrib):
                element.extend(child[:])
            elif child is not None:
                element.append(child)
        else:
            element = Element(tag=tag, attrib=attrib)
        xml_string = xml_string.replace(begin, "", 1).strip()
        return xml_string, element


def _find_two_parts_element_end(xml_string, tag, verbose=False):
    """

    :param xml_string:
    :param tag:
    :param verbose:
    :return:
    """
    xml_string = xml_string.strip()
    match = re.compile(r"^" + _xml_string_end_element_replace.format(tag)).match(xml_string)
    if not match:
        return xml_string, None
    else:
        match_group_dict = match.groupdict()
        end = match_group_dict["end"]
        xml_string = xml_string.replace(end, "", 1).strip()
        return xml_string, True
