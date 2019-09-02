#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Prototype of xml writer to keep order.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict
import six
import re
from io import open
import os
from copy import copy, deepcopy
import sys


def is_xml_element(element):
    return isinstance(element, (Beacon, Element, Comment, Header))


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


# Create some classes to deal with xml writing
class Beacon(object):
    """
    Generic class to deal with XML beacons.
    """
    def __init__(self):
        self.level = 0

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return self.dump()

    def __len__(self):
        return len(self.dump())

    def __eq__(self, other):
        test = isinstance(other, type(self))
        if test:
            test = self._test_attribute_equality("level", other)
        return test

    def __copy__(self):
        element = Beacon()
        element.update_level(self.level)
        return element

    def dump(self):
        raise NotImplementedError()

    @staticmethod
    def _test_dict_equality(a_dict, an_other_dict):
        test = isinstance(a_dict, (dict, OrderedDict)) and isinstance(an_other_dict, (dict, OrderedDict))
        if test:
            test = len(a_dict) == len(an_other_dict)
        if test:
            for key in list(a_dict):
                test = test and key in an_other_dict and a_dict[key] == an_other_dict[key]
        return test

    def _test_attribute_equality(self, attrib, other):
        if attrib == "text":
            default = ""
        else:
            default = None
        self_attrib = getattr(self, attrib, default)
        other_attrib = getattr(other, attrib, default)
        test = isinstance(other_attrib, type(self_attrib))
        if test and self_attrib != default and other_attrib != default and self_attrib == other_attrib:
            return True
        else:
            return False

    @staticmethod
    def correct_attrib(attrib):
        if not isinstance(attrib, (dict, OrderedDict)):
            raise TypeError("attrib must be a dict or an OrderDict.")
        corrected_attrib = OrderedDict()
        for (key, value) in attrib.items():
            corrected_attrib[str(key)] = str(value)
        return corrected_attrib

    @staticmethod
    def dump_dict(a_dict, sort=False):
        if len(a_dict) > 0:
            list_key_value = list()
            if sort:
                for key in sorted(list(a_dict)):
                    list_key_value.append((key, a_dict[key]))
            else:
                for (key, value) in a_dict.items():
                    list_key_value.append((key, value))
            return " ".join(['{}={}'.format(key, '"{}"'.format(value)) for (key, value) in list_key_value])
        else:
            return None

    def _dump_attrib(self, sort=False):
        raise NotImplementedError()

    def update_level(self, new_level):
        if self.level != new_level:
            self.level = new_level


class Comment(Beacon):

    def __init__(self, comment):
        super(Comment, self).__init__()
        self.comment = comment

    def __eq__(self, other):
        test = super(Comment, self).__eq__(other)
        if test:
            test = self._test_attribute_equality("comment", other)
        return test

    def __copy__(self):
        element = Comment(comment=self.comment)
        element.update_level(self.level)
        return element

    def dump(self):
        rep = "\t" * self.level + "<!--%s-->" % self.comment
        return encode_if_needed(rep)


class Header(Beacon):
    """
    Class to deal with xml header.
    """
    def __init__(self, tag, attrib=OrderedDict()):
        super(Header, self).__init__()
        self.tag = tag
        self.attrib = deepcopy(attrib)

    def __eq__(self, other):
        test = super(Header, self).__eq__(other)
        if test:
            test = self._test_attribute_equality("tag", other)
        if test:
            test = self._test_dict_equality(self.attrib, other.attrib)
        return test

    def __copy__(self):
        element = Header(tag=self.tag, attrib=deepcopy(self.attrib))
        element.update_level(self.level)
        return element

    def dump(self):
        offset = "\t" * self.level
        if len(self.attrib) > 0:
            rep = offset + '<?{} {}?>'.format(self.tag, self._dump_attrib())
        else:
            rep = offset + '<?{}?>'.format(self.tag)
        return encode_if_needed(rep)

    def _dump_attrib(self, sort=False):
        return self.dump_dict(deepcopy(self.attrib), sort=sort)


class Element(Beacon):
    """
    Class to deal with xml elements.
    """
    def __init__(self, tag, text=None, attrib=OrderedDict()):
        super(Element, self).__init__()
        self.tag = tag
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


# XML dict regexp
_dict_regexp = re.compile(r'(?P<key>\S+)\s?=\s?"(?P<value>[^"]+)"')


def _build_dict_attrib(dict_string):
    dict_string = dict_string.strip()
    string_match = _dict_regexp.findall(dict_string)
    attrib = OrderedDict()
    for (key, value) in string_match:
        attrib[key] = value.replace('"', '')
    return attrib


# XML header regexp
_xml_header_regexp = re.compile(r'(\s?<\?\s?\w*\s?(([^><])*)\s?\?>\s?)')
_xml_header_regexp_begin = re.compile(r'^<\s?\?\s?(?P<tag>\w*)\s?(?P<attrib>([^><])*)\s?\?>')


def _find_xml_header(xml_string, verbose=False):
    pattern_findall = _xml_header_regexp.findall(xml_string)
    if len(pattern_findall) > 1:
        raise Exception("There should be only one header in an XML document.")
    elif len(pattern_findall) == 0:
        return xml_string, None
    else:
        pattern_match = _xml_header_regexp_begin.match(xml_string)
        if not pattern_match:
            raise Exception("Header should be at the beginning of the xml document.")
        else:
            tag = pattern_match.groupdict()["tag"]
            attrib = pattern_match.groupdict()["attrib"]
            attrib = _build_dict_attrib(attrib)
            header = Header(tag=tag, attrib=attrib)
            xml_string = xml_string.replace(pattern_findall[0][0], "")
            return xml_string, header


# XML comment regexp
_xml_comment_regexp = re.compile(r"^(?P<all>\s?<\!--\s?(?P<comment>((?!<\!--)(?!-->).)+)\s?-->)\s?")


def _find_xml_comment(xml_string, verbose=True):
    # if verbose:
    #     print("<<<find_xml_comment: XML_STRING before>>>", len(xml_string), xml_string)
    xml_string = xml_string.strip()
    if verbose:
        if len(xml_string) > 10:
            little_xml_string = xml_string[:10]
        else:
            little_xml_string = xml_string
        print("<<<find_xml_comment: beginning of the XML string >>>", little_xml_string)
    match_comment = _xml_comment_regexp.match(xml_string)
    if verbose:
        print("<<<find_xml_comment: is there a comment? >>>", match_comment)
    if not match_comment:
        # if verbose:
        #     print("<<<find_xml_comment: XML_STRING after>>>", len(xml_string), xml_string)
        return xml_string, None
    else:
        text = match_comment.groupdict()["comment"]
        text = text.strip()
        comment = Comment(comment=text)
        xml_string = xml_string.replace(match_comment.groupdict()["all"], "")
        xml_string = xml_string.strip()
        if verbose:
            # print("<<<find_xml_comment: XML_STRING after>>>", len(xml_string), xml_string)
            print("<<<find_xml_comment: comment >>>", len(str(comment)), str(comment))
        return xml_string, comment


def _build_element(xml_string, verbose=False):
    # Delete unused spaces
    xml_string = xml_string.strip()
    if verbose:
        print("<<<build_element: XML_STRING before>>>", len(xml_string), xml_string)
    if len(xml_string) == 0:
        raise Exception("The XML string should not be void.")
    # Check if the element is a XML comment
    xml_string, comment = _find_xml_comment(xml_string, verbose=verbose)
    if comment is not None:
        xml_string = xml_string.strip()
        if verbose:
            print("<<<build_element: XML_STRING after comment>>>", len(xml_string), xml_string)
        return xml_string, comment
    else:
        # Check if the element is a XML element made of one single part
        xml_string, element = _find_one_part_element(xml_string, verbose=verbose)
        if element is not None:
            xml_string = xml_string.strip()
            if verbose:
                print("<<<build_element: XML_STRING after element>>>", len(xml_string), xml_string)
            return xml_string, element
        else:
            # Check if the element is a XML element made of two parts
            xml_string, element = _find_two_parts_element(xml_string, verbose=verbose)
            if element is not None:
                xml_string = xml_string.strip()
                if verbose:
                    print("<<<build_element: XML_STRING after element>>>", len(xml_string), xml_string)
                return xml_string, element
            else:
                raise Exception("Could not find what the element could be...")


# XML single part regexp
_xml_single_part_element_regexp = re.compile(r'^\s?(?P<all><\s?(?P<tag>\w+)\s?(?P<attrib>([^><])*)\s?/>)\s?')


def _find_one_part_element(xml_string, verbose=False):
    xml_string = xml_string.strip()
    match_single_part = _xml_single_part_element_regexp.match(xml_string)
    if match_single_part:
        tag = match_single_part.groupdict()["tag"]
        attrib = match_single_part.groupdict()["attrib"]
        attrib = _build_dict_attrib(attrib)
        element = Element(tag=tag, attrib=attrib)
        xml_string = xml_string.replace(match_single_part.groupdict()["all"], "")
        return xml_string, element
    else:
        return xml_string, None


# XML two parts regexp
_xml_string_first_element_replace = r'(?P<all_begin>\s?(?P<begin><\s?(?P<tag>{})\s?(?P<attrib>([^><])*)\s?>)\s?)'
_xml_string_init_element_replace = r'^'+_xml_string_first_element_replace
_xml_init_two_parts_element_regexp = re.compile(_xml_string_init_element_replace.format(r"\w+"))
_xml_string_content_element = r'(?P<content>{})'
_xml_string_end_element_replace = r'(?P<all_end>\s?(?P<end></\s?{}\s?>)\s?)'
_xml_string_two_parts_element_replace = _xml_string_init_element_replace + _xml_string_content_element + \
                                        _xml_string_end_element_replace


def _find_matching_first_part_in_content(content, tag, verbose=False):
    finditer_matches_first_part_in_content = \
        re.compile(_xml_string_first_element_replace.format(tag)).finditer(content)
    find_positions_first_part_in_content = list()
    last_position = 0
    for match in finditer_matches_first_part_in_content:
        last_position = content.find(match.groupdict()["begin"], last_position + 1)
        find_positions_first_part_in_content.append(last_position)
    if verbose:
        print("<<<find_matching_first_part_in_content: rank match first part>>>",
              len(find_positions_first_part_in_content), find_positions_first_part_in_content)
    return find_positions_first_part_in_content


def _find_matching_last_part_in_content(content, tag, verbose=False):
    finditer_matches_last_part_in_content = \
        re.compile(_xml_string_end_element_replace.format(tag)).finditer(content)
    find_positions_last_part_in_content = list()
    find_groups_last_part_in_content = list()
    last_position = 0
    for match in finditer_matches_last_part_in_content:
        last_position = content.find(match.groupdict()["end"], last_position + 1)
        find_positions_last_part_in_content.append(last_position)
        find_groups_last_part_in_content.append(match.groupdict()["end"])
    if verbose:
        print("<<<find_matching_last_part_in_content: rank match last part>>>",
              len(find_positions_last_part_in_content), find_positions_last_part_in_content)
    return find_positions_last_part_in_content, find_groups_last_part_in_content


def _find_real_content(content, match_first_part, match_last_part, groups_last_part, verbose=False):
    find_end = False
    if len(match_first_part) != 0 and len(match_last_part) != 0:
        # Case of nested beacons with same tag
        position_start = 0
        nb_positions_start = len(match_first_part)
        position_end = 0
        nb_positions_end = len(match_last_part)
        nb_nested = 0
        while position_start < nb_positions_start and position_end < nb_positions_end and not find_end:
            if verbose:
                print("<<<find_element: POSITIONS START/END NESTED before>>>", position_start, "/",
                      nb_positions_start, position_end, "/", nb_positions_end, nb_nested)
            if match_last_part[position_end] < match_first_part[position_start]:
                if nb_nested > 0:
                    position_end += 1
                    nb_nested -= 1
                else:
                    content = content[0:match_last_part[position_end]]
                    find_end = True
            else:
                nb_nested += 1
                position_start += 1
        if verbose:
            print("<<<find_real_content: POSITIONS START/END NESTED after>>>", position_start, "/",
                  nb_positions_start, position_end, "/", nb_positions_end, nb_nested)

        if not find_end and position_start == nb_positions_start and position_end == (nb_positions_end - nb_nested):
            # Case of nested and finished beacons with same tag
            find_end = True
            position_end += nb_nested
            nb_nested = 0
        if not find_end:
            raise Exception("There is a problem with the xml file... All opened beacon must be closed.")
    elif len(match_last_part) != 0 or len(match_first_part) != 0:
        raise Exception("There is a problem with the xml file... All opened beacon must be closed.")
    if find_end:
        if position_end > (nb_positions_end - 1):
            return content, None
        else:
            return content, groups_last_part[position_end]
    else:
        return content, None


def _find_two_parts_element(xml_string, verbose=False):
    xml_string = xml_string.strip()
    # Match the first part of the two parts xml element
    match_first_part = _xml_init_two_parts_element_regexp.match(xml_string)
    if match_first_part:
        # Get as many information as possible
        tag = match_first_part.groupdict()["tag"]
        match_two_strings = re.compile(_xml_string_two_parts_element_replace.format(tag, r".*", tag)).match(xml_string)
        if not match_two_strings:
            raise Exception("Error - element should be a two parts element but seems not...")
        attrib = match_two_strings.groupdict()["attrib"]
        attrib = _build_dict_attrib(attrib)
        begin = match_two_strings.groupdict()["begin"]
        all_begin = match_two_strings.groupdict()["all_begin"]
        end = match_two_strings.groupdict()["end"]
        all_end = match_two_strings.groupdict()["all_end"]
        content = match_two_strings.groupdict()["content"]
        # Find out if the content contains a subpart with the same tag
        if verbose:
            print("<<<find_element: CONTENT before>>>", len(content), content)
        find_positions_first_part_in_content = _find_matching_first_part_in_content(content, tag, verbose)
        find_positions_last_part_in_content, find_groups_last_part_in_content = \
            _find_matching_last_part_in_content(content, tag, verbose)
        # Find out where the content really stop
        content, new_end = _find_real_content(content, find_positions_first_part_in_content,
                                              find_positions_last_part_in_content, find_groups_last_part_in_content,
                                              verbose=verbose)
        if new_end is not None:
            end = new_end
        else:
            end = all_end
        if verbose:
            print("<<<find_element: CONTENT after>>>", len(content), content)
        # Create string to remove
        string_to_remove = all_begin + content + end
        # Separate children from text
        sub_xml_string, text = _find_text(content)
        if verbose:
            print("<<<SUB_XML_STRING>>>", len(sub_xml_string), sub_xml_string)
        if len(text) == 0:
            text = None
        # Create the element and its children
        element = Element(tag=tag, text=text, attrib=attrib)
        while len(sub_xml_string) > 0:
            if verbose:
                print("<<<SUB_XML_STRING>>> Enter the loop...", len(sub_xml_string), sub_xml_string)
            new_sub_xml_string, subelement = _build_element(sub_xml_string, verbose=verbose)
            if sub_xml_string == new_sub_xml_string:
                raise Exception("Stop: Infinite loop!!!!!!")
            else:
                sub_xml_string = new_sub_xml_string
            sub_xml_string = sub_xml_string.strip()
            if subelement is not None:
                element.append(subelement)
        xml_string = xml_string.replace(string_to_remove, "")
        if verbose:
            print("<<<XML_STRING end of treatment>>>", len(xml_string), xml_string)
            print("<<<XML_STRING string replaced>>>", len(string_to_remove), string_to_remove)
        return xml_string, element
    else:
        return xml_string, None


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
            init_text = xml_string[0:(rank_start_init_element - 1)]
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


def _pre_xml_string_format(xml_string, verbose=False):
    if not isinstance(xml_string, six.string_types):
        raise TypeError("Argument must be a string or equivalent, not %s." % type(xml_string))
    # Some pre-treatments on the string
    xml_string = xml_string.replace("\n", " ")
    xml_string = xml_string.replace("\t", " ")
    xml_string = xml_string.strip()
    xml_string = " ".join(xml_string.split(" "))
    # Look for reserved symbols (< and >) and replace them
    begin_comment_positions = [m.start() for m in re.compile(r"<!--").finditer(xml_string)]
    end_comment_positions = [m.end() - 1 for m in re.compile(r"-->").finditer(xml_string)]
    if len(begin_comment_positions) != len(end_comment_positions):
        raise Exception("All comments must be closed")
    comments_positions = [(comment_begin, comment_end) for (comment_begin, comment_end) in zip(begin_comment_positions, end_comment_positions)]
    if verbose:
        print("<<<pre_xml_string_format: comment_positions>>>", len(comments_positions))

    double_quotes_positions_tmp = [m.start() for m in re.compile(r'"').finditer(xml_string)]
    double_quotes_positions = list()
    for pos in double_quotes_positions_tmp:
        if not _find_in_out(pos, comments_positions, verbose=False):
            double_quotes_positions.append(pos)
    double_quotes_positions_tmp = double_quotes_positions
    if len(double_quotes_positions_tmp) % 2 != 0:
        raise Exception("There should have an even number of '\"' in the xml file... have",
                        len(double_quotes_positions_tmp))
    double_quotes_positions = [(double_quotes_positions_tmp[2 * pos], double_quotes_positions_tmp[2 * pos + 1])
                               for pos in range(len(double_quotes_positions_tmp) // 2)]
    if verbose:
        print("<<<pre_xml_string_format: double_quotes_positions>>>", len(double_quotes_positions))

    possible_greater_positions = [m.start() for m in re.compile(r">").finditer(xml_string)]
    greater_positions = list()
    if verbose:
        print("<<<pre_xml_string_format: possible_greater_positions>>>", len(possible_greater_positions))

    possible_lower_positions = [m.start() for m in re.compile(r'<').finditer(xml_string)]
    lower_positions = list()
    if verbose:
        print("<<<pre_xml_string_format: possible_lower_positions>>>", len(possible_lower_positions))

    g = 0
    l = 0
    beacon_open = False
    nb_beacons = 1
    while (g < len(possible_greater_positions) and l < len(possible_lower_positions)):
        g_pos = possible_greater_positions[g]
        l_pos = possible_lower_positions[l]
        if l_pos < g_pos:
            if _find_in_out(l_pos, comments_positions, verbose=verbose):
                if verbose:
                    print("<<<pre_xml_string_format: discarded because in comment>>>", l_pos)
                l += 1
            elif _find_in_out(l_pos, double_quotes_positions, verbose=verbose):
                if verbose:
                    print("<<<pre_xml_string_format: lower than found>>>", l_pos)
                lower_positions.append(l_pos)
                l += 1
            elif not beacon_open:
                if verbose:
                    print("<<<pre_xml_string_format: open beacon>>>", l_pos)
                beacon_open = True
                l += 1
            else:
                if verbose:
                    print("<<<pre_xml_string_format: last beacons>>>", possible_lower_positions[l-1],
                          l_pos, xml_string[possible_lower_positions[l-1]:l_pos + 1])
                    raise Exception("Unexpected '<' symbol", l_pos)
        else:
            if _find_in_out(g_pos, comments_positions, verbose=verbose):
                if verbose:
                    print("<<<pre_xml_string_format: discarded because in comment>>>", g_pos)
                g += 1
            elif _find_in_out(g_pos, double_quotes_positions, verbose=verbose):
                if verbose:
                    print("<<<pre_xml_string_format: greater than found>>>", g_pos)
                greater_positions.append(g_pos)
                g += 1
            elif beacon_open:
                if verbose:
                    print("<<<pre_xml_string_format: close beacon>>>", g_pos, "/", nb_beacons)
                nb_beacons += 1
                beacon_open = False
                g += 1
            else:
                if verbose:
                    print("<<<pre_xml_string_format: last beacon>>>", possible_greater_positions[g - 1], g_pos,
                          xml_string[possible_greater_positions[g - 1]:g_pos + 1])
                raise Exception("Unexpected '>' symbol", g_pos)

    while g < len(possible_greater_positions):
        if beacon_open:
            if _find_in_out(possible_greater_positions[g], double_quotes_positions, verbose=verbose):
                greater_positions.append(possible_greater_positions[g])
            else:
                beacon_open = False
            g += 1
        else:
            raise Exception("There are two many '>' in XML string.")
    if beacon_open or l != len(possible_lower_positions) or g != len(possible_greater_positions):
        raise Exception("There is issues in '>' and '<' usage in XML string")
    # Replace the greater than and lower than symbols by &gt and &lw respectively
    if verbose:
        print("<<<pre_xml_string_format: greater than found:>>>", len(greater_positions), greater_positions, [xml_string[a-20:a+20] for a in greater_positions])
        print("<<<pre_xml_string_format: lower than found:>>>", len(lower_positions), lower_positions, [xml_string[a-20:a+20] for a in lower_positions])
    g = len(greater_positions) - 1
    l = len(lower_positions) - 1
    new_xml_string = xml_string
    while g >= 0 and l >= 0:
        g_pos = greater_positions[g]
        l_pos = lower_positions[l]
        if g_pos > l_pos:
            if verbose:
                print("<<<pre_xml_string_format: before replacement:>>>", new_xml_string[g_pos -2:g_pos + 20])
            new_xml_string = replace_char_at_pos_by_string(new_xml_string, ">", "&gt", g_pos, g_pos, verbose=verbose)
            if verbose:
                print("<<<pre_xml_string_format: after replacement:>>>", new_xml_string[g_pos -2:g_pos + 20])
            g -= 1
        else:
            if verbose:
                print("<<<pre_xml_string_format: before replacement:>>>", new_xml_string[l_pos -2:l_pos + 20])
            new_xml_string = replace_char_at_pos_by_string(new_xml_string, "<", "&lt", l_pos, l_pos, verbose=verbose)
            if verbose:
                print("<<<pre_xml_string_format: after replacement:>>>", new_xml_string[l_pos -2:l_pos + 20])
            l -= 1
    while g >= 0:
        g_pos = greater_positions[g]
        if verbose:
            print("<<<pre_xml_string_format: before replacement:>>>", new_xml_string[g_pos - 2:g_pos + 20])
        new_xml_string = replace_char_at_pos_by_string(new_xml_string, ">", "&gt", g_pos, g_pos, verbose=verbose)
        if verbose:
            print("<<<pre_xml_string_format: after replacement:>>>", new_xml_string[g_pos - 2:g_pos + 20])
        g -= 1
    while l >= 0:
        l_pos = lower_positions[l]
        if verbose:
            print("<<<pre_xml_string_format: before replacement:>>>", new_xml_string[l_pos - 2:l_pos + 20])
        new_xml_string = replace_char_at_pos_by_string(new_xml_string, "<", "&lt", l_pos, l_pos, verbose=verbose)
        if verbose:
            print("<<<pre_xml_string_format: after replacement:>>>", new_xml_string[l_pos - 2:l_pos + 20])
        l -= 1
    if verbose:
        print("<<<pre_xml_string_format: greater than found:>>>", len(greater_positions), greater_positions, [new_xml_string[a-20:a+20] for a in greater_positions])
        print("<<<pre_xml_string_format: lower than found:>>>", len(lower_positions), lower_positions, [new_xml_string[a-20:a+20] for a in lower_positions])
    return " ".join(new_xml_string.split(" "))


def replace_char_at_pos_by_string(complete_string, string_in, replace_out, pos_init, pos_end, verbose=False):
    if (pos_init == pos_end and complete_string[pos_init] != string_in) or \
            (pos_init != pos_end and complete_string[pos_init:pos_end] != string_in):
        raise Exception("The string to be replaced is not the one present: %s / %s" %
                        (string_in, complete_string[pos_init:pos_end]))
    if pos_end >= len(complete_string) or pos_init < 0:
        raise Exception("The string to be replaced is not in the complete string")
    if pos_init == 0:
        return replace_out + complete_string[(pos_end + 1):]
    elif pos_end == len(complete_string) - 1:
        return complete_string[:pos_end] + replace_out
    else:
        return complete_string[:pos_init] + replace_out + complete_string[(pos_end + 1):]


def _find_in_out(pos, list_in_out_pos, verbose=False):
    if verbose:
        print("<<<find_in_out: check pos>>>", pos)
    test = False
    for (pos_in, pos_out) in list_in_out_pos:
        if pos_in <= pos and pos_out >= pos:
            if verbose:
                print("<<<find_in_out: in out found>>>", pos, pos_in, pos_out)
            test = True
            break
    return test


def xml_parser(xml_string, verbose=False):
    xml_string = _pre_xml_string_format(xml_string, verbose=verbose)
    # Check init or end text (there should not have been any but let's check
    if len(xml_string) > 0:
        xml_string, text = _find_text(xml_string, fatal=True)
    # Check for header
    if len(xml_string) > 0:
        xml_string, header = _find_xml_header(xml_string, verbose=verbose)
    # Check for comments
    comments = list()
    comment = True
    while len(xml_string) > 0 and comment:
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
    while comment and len(xml_string) > 0:
        new_xml_string, comment = _build_element(xml_string, verbose=verbose)
        if new_xml_string == xml_string:
            raise Exception("It seems that there was something that is not a comment after the root element...")
        else:
            xml_string = new_xml_string
        if comment is not None:
            comments.append(comment)
    # Check that len of xml_string is 0
    if len(xml_string) > 0:
        raise Exception("The XML string should follow the pattern: header comment root_xml_element comment")
    return text, comments, header, root_element


def xml_file_parser(xml_file, verbose=False):
    with open(xml_file, "rb") as opened_file:
        xml_content = opened_file.readlines()
    xml_string = "\n".join([line.decode("utf-8") for line in xml_content])
    return xml_parser(xml_string, verbose=verbose)


if __name__ == "__main__":
    dr2xml_tests_dir = os.sep.join([os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]), "tests"])
    for my_xml_file in [
        os.sep.join([dr2xml_tests_dir, "test_files_aladin/arpsfx.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_files_aladin/atmo_fields.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_files_aladin/iodef.AORCM.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_files_aladin/nemo.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_files_aladin/nemo_domains.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_files_aladin/nemo_fields.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_files_aladin/ping_nemo.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_files_aladin/ping_surfex.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_files_aladin/surfex_fields.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_a4SST_AGCM_1960/output_ref_python2/dr2xml_surfex.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_a4SST_AGCM_1960/output_ref_python2/dr2xml_trip.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_amip_hist_AGCM_1870_r10/output_ref_python2/dr2xml_surfex.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_amip_hist_AGCM_1870_r10/output_ref_python2/dr2xml_trip.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_land_hist_LGCM/output_ref_python2/dr2xml_surfex.xml"]),
        os.sep.join([dr2xml_tests_dir, "test_land_hist_LGCM/output_ref_python2/dr2xml_trip.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/aero_fields.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/arpsfx.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/atmo_fields.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/chem_fields.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/iodef.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/nemo.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/nemo_domains.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/nemo_fields.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/ping_nemo.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/ping_nemo_gelato.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/ping_nemo_ocnBgChem.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/ping_surfex.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/ping_trip.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/surfex_fields.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/trip.xml"]),
        os.sep.join([dr2xml_tests_dir, "common/xml_files/trip_fields.xml"]),
    ]:
        print(my_xml_file)
        text, comments, header, root_element = xml_file_parser(my_xml_file, verbose=False)
        print(text)
        print(comments)
        print(header)
        print(root_element)
