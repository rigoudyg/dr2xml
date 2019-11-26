#!/usr/bin/python
# coding: utf-8

"""
Elements
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import re
from collections import OrderedDict
from copy import deepcopy, copy

from xml_writer.beacon import Beacon
from xml_writer.header import Header
from xml_writer.comment import _find_xml_comment, Comment
from xml_writer.utils import encode_if_needed, decode_if_needed, _generic_dict_regexp, \
    _build_dict_attrib, _find_text, print_if_needed


class Element(Beacon):
    """
    Class to deal with xml elements.
    """
    def __init__(self, tag, text=None, attrib=OrderedDict()):
        super(Element, self).__init__()
        self.tag = tag.strip()
        self.text = text
        self.attrib = deepcopy(attrib)
        self.children = list()

    def __eq__(self, other):
        test = super(Element, self).__eq__(other)
        if test:
            test = self._test_attribute_equality("tag", other)
        if test:
            test = self._test_attribute_equality("text", other)
        if test:
            test = self._test_dict_equality(self.attrib, other.attrib)
        if test:
            test = self._test_attribute_equality("children", other)
        return test

    def __len__(self):
        return len(self.children)

    def __copy__(self):
        element = Element(tag=self.tag, text=self.text, attrib=deepcopy(self.attrib))
        element.update_level(self.level)
        for child in self.children:
            element.children.append(copy(child))
        return element

    def dump(self):
        offset = "\t" * self.level
        # Deal with header
        if len(self.attrib) > 0:
            header = " ".join([self.tag, self._dump_attrib()])
        else:
            header = self.tag
        # Deal with content
        if len(self) == 0:
            if self.text is None:
                content = None
            else:
                content = " {} ".format(self.text)
        else:
            if self.text is None:
                content = "\n{}\n{}".format(self._dump_children(), offset)
            else:
                content = "{}\t{}\n{}\n{}".format(offset, self.text, self._dump_children(), offset)
        # Build the string
        if content is None:
            rep = "{}<{}/>".format(offset, header)
        else:
            rep = "{}<{}>{}</{}>".format(offset, header, content, self.tag)
        return encode_if_needed(rep)

    def set_text(self, text):
        if len(text) > 0:
            if self.text is None:
                self.text = text
            else:
                self.text = "\n".join([self.text, text])

    def __getitem__(self, item):
        return self.children[item]

    def __setitem__(self, key, value):
        self.children[key] = value

    def __delitem__(self, key):
        self.remove(self[key])

    def append(self, element):
        if element is not None:
            if not is_xml_element(element):
                raise TypeError("Could not append an element of type %s to an XML element." % type(element))
            element.update_level(self.level + 1)
            self.children.append(element)

    def extend(self, elements):
        if elements is not None:
            for (rank, element) in enumerate(elements):
                if not is_xml_element(element):
                    raise TypeError("Could not extend an XML element with elements of type %s." % type(element))
                else:
                    elements[rank].update_level(self.level + 1)
            self.children.extend(elements)

    def insert(self, index, element):
        if element is not None:
            if not is_xml_element(element):
                raise TypeError("Could not insert an element of type %s to an XML element." % type(element))
            element.update_level(self.level + 1)
            self.children.insert(index, element)

    def remove(self, element):
        if element is not None:
            if not is_xml_element(element):
                raise TypeError("Could not append an remove of type %s to an XML element." % type(element))
            self.children.remove(element)

    def update_level(self, new_level):
        super(Element, self).update_level(new_level)
        if len(self.children) > 0:
            for i in range(len(self.children)):
                self.children[i].update_level(new_level + 1)

    def _dump_children(self):
        if len(self.children) > 0:
            return "\n".join([decode_if_needed(child.dump()) for child in self.children])
        else:
            return ""

    def _dump_attrib(self, sort=False):
        return self.dump_dict(deepcopy(self.attrib), sort=sort)


def _build_element(xml_string, verbose=False):
    # Delete unused spaces
    xml_string = xml_string.strip()
    print_if_needed("<<<build_element: XML_STRING before>>>", len(xml_string), xml_string, verbose=verbose)
    if len(xml_string) == 0:
        raise Exception("The XML string should not be void.")
    # Check if the element is a XML comment
    xml_string, comment = _find_xml_comment(xml_string, verbose=verbose)
    if comment is not None:
        xml_string = xml_string.strip()
        print_if_needed("<<<build_element: XML_STRING after comment>>>", len(xml_string), xml_string, verbose=verbose)
        return xml_string, comment
    else:
        # Check if the element is a XML element made of one single part
        xml_string, element = _find_one_part_element(xml_string, verbose=verbose)
        if element is not None:
            xml_string = xml_string.strip()
            print_if_needed("<<<build_element: XML_STRING after element>>>", len(xml_string), xml_string,
                            verbose=verbose)
            return xml_string, element
        else:
            # Check if the element is a XML element made of two parts
            xml_string, element = _find_two_parts_element(xml_string, verbose=verbose)
            if element is not None:
                xml_string = xml_string.strip()
                print_if_needed("<<<build_element: XML_STRING after element>>>", len(xml_string), xml_string,
                                verbose=verbose)
                return xml_string, element
            else:
                raise Exception("Could not find what the element could be...")


# XML single part regexp
_xml_single_part_element_regexp = re.compile(r'^\s?(?P<all><\s?(?P<tag>\w+)\s?{}\s?/>)\s?'.format(
    _generic_dict_regexp))


def _find_one_part_element(xml_string, verbose=False):
    print_if_needed("<<<find_one_part_element BEFORE>>>", len(xml_string), xml_string, verbose=verbose)
    xml_string = xml_string.strip()
    match_single_part = _xml_single_part_element_regexp.match(xml_string)
    if match_single_part:
        match_single_part = match_single_part.groupdict()
        tag = match_single_part["tag"].strip()
        attrib = _build_dict_attrib(match_single_part["attrib"])
        element = Element(tag=tag, attrib=attrib)
        xml_string = xml_string.replace(match_single_part["all"], "", 1)
        print_if_needed("<<<find_one_part_element AFTER>>>", len(xml_string), xml_string, verbose=verbose)
        return xml_string, element
    else:
        return xml_string, None


# XML two parts regexp
_xml_string_first_element_replace = r'(?P<all_begin>\s?(?P<begin><\s?(?P<tag>{}){}\s?>)\s?)'.format('{}',
                                                                                                    _generic_dict_regexp)
_xml_string_init_element_replace = r'^'+_xml_string_first_element_replace
_xml_init_two_parts_element_regexp = re.compile(_xml_string_init_element_replace.format(r"\w+\s?"))
_xml_string_content_element = r'(?P<content>{})'
_xml_string_end_element_replace = r'(?P<all_end>\s?(?P<end></\s?{}\s?>)\s?)'
_xml_string_two_parts_element_replace = _xml_string_init_element_replace + _xml_string_content_element + \
                                        _xml_string_end_element_replace
_xml_string_pseudo_two_parts_element_replace = r"(?P<all>" + _xml_string_init_element_replace + r"\s?" + \
                                               _xml_string_end_element_replace + r")"


def _find_two_parts_element_init(xml_string, verbose=False):
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
        xml_string = xml_string.replace(begin, "", 1).strip()
        elt = Element(tag=tag, attrib=attrib)
        return xml_string, elt


def _find_two_parts_element_end(xml_string, tag, verbose=False):
    xml_string = xml_string.strip()
    match = re.compile(r"^" + _xml_string_end_element_replace.format(tag)).match(xml_string)
    if not match:
        return xml_string, None
    else:
        match_group_dict = match.groupdict()
        end = match_group_dict["end"]
        xml_string = xml_string.replace(end, "", 1).strip()
        return xml_string, True


# def _find_matching_first_part_in_content(content, tag, verbose=False):
#     finditer_matches_first_part_in_content = \
#         re.compile(_xml_string_first_element_replace.format(tag)).finditer(content)
#     find_positions_first_part_in_content = list()
#     last_position = 0
#     for match in finditer_matches_first_part_in_content:
#         last_position = match.start()
#         if content[last_position] == " ":
#             last_position += 1
#         find_positions_first_part_in_content.append(last_position)
#     if verbose:
#         print("<<<find_matching_first_part_in_content: rank match first part>>>",
#               len(find_positions_first_part_in_content), find_positions_first_part_in_content)
#     return find_positions_first_part_in_content
#
#
# def _find_matching_last_part_in_content(content, tag, verbose=False):
#     finditer_matches_last_part_in_content = \
#         re.compile(_xml_string_end_element_replace.format(tag)).finditer(content)
#     find_positions_last_part_in_content = list()
#     find_groups_last_part_in_content = list()
#     last_position = 0
#     for match in finditer_matches_last_part_in_content:
#         # last_position = content.find(match.groupdict()["end"], last_position + 1)
#         last_position = match.start()
#         if content[last_position] == " ":
#             last_position += 1
#         find_positions_last_part_in_content.append(last_position)
#         find_groups_last_part_in_content.append(match.groupdict()["end"])
#     if verbose:
#         print("<<<find_matching_last_part_in_content: rank match last part>>>",
#               len(find_positions_last_part_in_content), find_positions_last_part_in_content)
#     return find_positions_last_part_in_content, find_groups_last_part_in_content


def _find_matching_first_and_last_part_in_content(content, tag, verbose=False):
    match_found = list()
    for match in re.compile(_xml_string_first_element_replace.format(tag)).finditer(content):
        last_position = match.start()
        if match.group().startswith(" "):
            last_position += 1
        match_found.append((last_position, match.groupdict()["begin"], "match_first"))
    for match in re.compile(_xml_string_end_element_replace.format(tag)).finditer(content):
        last_position = match.start()
        if match.group().startswith(" "):
            last_position += 1
        match_found.append((last_position, match.groupdict()["end"], "match_end"))
    match_found = sorted(match_found, key=lambda match: match[0])
    for match in match_found:
        yield match


# def _find_real_content(content, match_first_part, match_last_part, groups_last_part, verbose=False):
#     find_end = False
#     if len(match_first_part) != 0 and len(match_last_part) != 0:
#         # Case of nested beacons with same tag
#         position_start = 0
#         nb_positions_start = len(match_first_part)
#         position_end = 0
#         nb_positions_end = len(match_last_part)
#         nb_nested = 0
#         while position_start < nb_positions_start and position_end < nb_positions_end and not find_end:
#             if verbose:
#                 print("<<<find_element: POSITIONS START/END NESTED before>>>", position_start, "/",
#                       nb_positions_start, position_end, "/", nb_positions_end, nb_nested)
#             if match_last_part[position_end] < match_first_part[position_start]:
#                 if nb_nested > 0:
#                     position_end += 1
#                     nb_nested -= 1
#                 else:
#                     content = content[0:match_last_part[position_end]]
#                     find_end = True
#             else:
#                 nb_nested += 1
#                 position_start += 1
#         if verbose:
#             print("<<<find_real_content: POSITIONS START/END NESTED after>>>", position_start, "/",
#                   nb_positions_start, position_end, "/", nb_positions_end, nb_nested)
#
#         if not find_end and position_start == nb_positions_start and position_end == (nb_positions_end - nb_nested):
#             # Case of nested and finished beacons with same tag
#             find_end = True
#             position_end += nb_nested
#             nb_nested = 0
#         if not find_end:
#             raise Exception("There is a problem with the xml file... All opened beacon must be closed.")
#     elif len(match_last_part) != 0 or len(match_first_part) != 0:
#         raise Exception("There is a problem with the xml file... All opened beacon must be closed.")
#     if find_end:
#         if position_end > (nb_positions_end - 1):
#             return content, None
#         else:
#             return content, groups_last_part[position_end]
#     else:
#         return content, None


def _find_real_content(content, tag, verbose=False):
    nb_nested = 0
    find_end = False
    real_content = ""
    for (match_pos, match_key, match_type) in _find_matching_first_and_last_part_in_content(content, tag,
                                                                                            verbose=verbose):
        if match_type == "match_end":
            if nb_nested > 0:
                nb_nested -= 1
            else:
                find_end = True
                real_content = content[0:match_pos]
                break
        elif match_type == "match_first":
            nb_nested += 1
        else:
            raise ValueError("Unknown match type %s" % match_type)
    if nb_nested > 0:
        raise Exception("There is a problem with the xml file... All opened beacon must be closed.")
    if find_end:
        if len(real_content) + len(match_key) >= len(content):
            return content, None
        else:
            return real_content, match_key
    else:
        return content, None


def _find_two_parts_element(xml_string, verbose=False):
    xml_string = xml_string.strip()
    # Match the first part of the two parts xml element
    match_first_part = _xml_init_two_parts_element_regexp.match(xml_string)
    if match_first_part:
        # Get as many information as possible
        tag = match_first_part.groupdict()["tag"].strip()
        # Check if it is a pseudo two parts element
        match_pseudo_two_strings = re.compile(_xml_string_pseudo_two_parts_element_replace.format(tag, tag)).match(xml_string)
        if match_pseudo_two_strings:
            match_group_dict = match_pseudo_two_strings.groupdict()
            attrib = _build_dict_attrib(match_group_dict["attrib"])
            element = Element(tag=tag, attrib=attrib)
            string_to_remove = match_group_dict["all"]
            xml_string = xml_string.replace(string_to_remove, "", 1)
            return xml_string, element
        # It is a real two parts element
        else:
            two_strings_regexp = _xml_string_two_parts_element_replace.format(tag, r".*", tag)
            match_two_strings = re.compile(two_strings_regexp).match(xml_string)
            if not match_two_strings:
                raise Exception("Error - element should be a two parts element but seems not...")
            else:
                match_group_dict = match_two_strings.groupdict()
                attrib = match_group_dict["attrib"]
                attrib = _build_dict_attrib(attrib)
                all_begin = match_group_dict["all_begin"]
                all_end = match_group_dict["all_end"]
                content = match_group_dict["content"]
                # Find out if the content contains a subpart with the same tag
                print_if_needed("<<<find_element: CONTENT before>>>", len(content), content, verbose=verbose)
                # Find out where the content really stop
                content, new_end = _find_real_content(content, tag, verbose=verbose)
                if new_end is not None:
                    end = new_end
                else:
                    end = all_end
                print_if_needed("<<<find_element: CONTENT after>>>", len(content), content, verbose=verbose)
                # Create string to remove
                string_to_remove = all_begin + content + end
                # Separate children from text
                sub_xml_string, text = _find_text(content, verbose=verbose)
                print_if_needed("<<<SUB_XML_STRING>>> Text found", text, verbose=verbose)
                print_if_needed("<<<SUB_XML_STRING>>>", len(sub_xml_string), sub_xml_string, verbose=verbose)
                if len(text) == 0:
                    text = None
                # Create the element and its children
                element = Element(tag=tag, text=text, attrib=attrib)
                while len(sub_xml_string) > 0:
                    print_if_needed("<<<SUB_XML_STRING>>> Enter the loop...", len(sub_xml_string), sub_xml_string,
                                    verbose=verbose)
                    new_sub_xml_string, text = _find_text(sub_xml_string, verbose=verbose)
                    if len(text) > 0:
                        print_if_needed("<<<SUB_XML_STRING>>> Text found:", text, verbose=verbose)
                        element.set_text(text)
                        new_sub_xml_string = new_sub_xml_string.strip()
                    new_sub_xml_string, subelement = _build_element(new_sub_xml_string, verbose=verbose)
                    if len(sub_xml_string) == len(new_sub_xml_string):
                        raise Exception("Stop: Infinite loop!!!!!!")
                    else:
                        sub_xml_string = new_sub_xml_string
                    sub_xml_string = sub_xml_string.strip()
                    if subelement is not None:
                        print_if_needed("<<<find sub_element>>>", subelement, verbose=verbose)
                        element.append(subelement)
                xml_string = xml_string.replace(string_to_remove, "", 1)
                print_if_needed("<<<XML_STRING end of treatment>>>", len(xml_string), xml_string, verbose=verbose)
                print_if_needed("<<<XML_STRING string replaced>>>", len(string_to_remove), string_to_remove,
                                verbose=verbose)
                return xml_string, element
    else:
        return xml_string, None


def is_xml_element(element):
    return isinstance(element, (Beacon, Element, Comment, Header))
