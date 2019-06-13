#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Prototype of xml writer to keep order.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict
import copy
import six
import re
from io import open


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

    def is_xml_element(self):
        return isinstance(self, (Beacon, Element, Comment, Header))

    def dump(self):
        raise NotImplementedError()

    def update_level(self, new_level):
        if self.level != new_level:
            self.level = new_level

    def copy(self):
        element = Beacon()
        element.level = self.level
        return element

    def _dump_attrib(self, sorted=False):
        if len(self.attrib) > 0:
            if sorted:
                return " ".join(['{}="{}"'.format(key, self.attrib[key]) for key in sorted(list(self.attrib))])
            else:
                return " ".join(['{}="{}"'.format(key, value) for (key, value) in self.attrib.items()])
        else:
            return None


class Comment(Beacon):
    """
    Class to deal with XML comments.
    """
    def __init__(self, comment):
        super(Comment, self).__init__()
        # Deal with comment attribute
        if not isinstance(comment, str):
            comment = str(comment)
        self.comment = comment

    def copy(self):
        element = super(Element, self).copy()
        element.comment = self.comment
        return element

    def dump(self):
        return "\t"*self.level+"<!-- {} -->".format(self.comment)

    def copy(self):
        element = super(Comment, self).copy()
        element.comment = self.comment


class Header(Beacon):
    """
    Class to deal with xml header.
    """
    def __init__(self, tag, attrib=OrderedDict()):
        super(Header, self).__init__()
        # Deal with attrib attribute
        if not isinstance(attrib, (dict, OrderedDict)):
            raise TypeError("attrib must be a dict or an OrderDict.")
        self.attrib = attrib
        self.tag = tag

    def copy(self):
        element = super(Element, self).copy()
        element.tag = self.tag
        element.attrib = copy.deepcopy(self.attrib)
        return element

    def dump(self):
        offset = "\t" * self.level
        if len(self.attrib) > 0:
            return offset + '<?{} {} ?>'.format(self.tag, self._dump_attrib())
        else:
            return offset + '<?{} ?>'.format(self.tag)


class Element(Beacon):
    """
    Class to deal with xml elements.
    """
    def __init__(self, tag, text=None, attrib=OrderedDict()):
        super(Element, self).__init__()
        # Deal with tag attribute
        if not isinstance(tag, str):
            tag = str(tag)
        self.tag = tag
        # Deal with attrib attribute
        if not isinstance(attrib, (dict, OrderedDict)):
            raise TypeError("attrib must be a dict or an OrderDict.")
        self.attrib = attrib
        # Deal with text attribute
        if text is not None and not isinstance(text, str):
            text = str(text)
        self.text = text
        # Deal with children attribute
        self.children = list()

    def __len__(self):
        return len(self.children)

    def __getitem__(self, index):
        return self.children[index]

    def __setitem__(self, index, element):
        self.children[index] = element

    def __delitem__(self, index):
        del self.children[index]

    def copy(self):
        element = super(Element, self).copy()
        element.tag = self.tag
        element.attrib = copy.deepcopy(self.attrib)
        element.text = self.text
        element.children = self.children
        return element

    def update_level(self, new_level):
        if self.level != new_level:
            self.level = new_level
            if len(self) > 0:
                i = 0
                while i < len(self.children):
                    self.children[i].update_level(new_level + 1)
                    i += 1

    def append(self, element):
        if not element.is_xml_element():
            raise TypeError("Could not append an element of type %s to an XML element." % type(element))
        element.update_level(self.level + 1)
        self.children.append(element)

    def extend(self, elements):
        for (rank, element) in enumerate(elements):
            if not element.is_xml_element():
                raise TypeError("Could not extend an XML element with elements of type %s." % type(element))
            else:
                elements[rank].update_level(self.level + 1)
        self.children.extend(elements)

    def insert(self, index, element):
        if not element.is_xml_element():
            raise TypeError("Could not insert an element of type %s to an XML element." % type(element))
        element.update_level(self.level + 1)
        self.children.insert(index, element)

    def remove(self, element):
        if not element.is_xml_element():
            raise TypeError("Could not append an remove of type %s to an XML element." % type(element))
        self.children.remove(element)

    def _dump_children(self):
        return "\n".join(child.dump() for child in self.children)

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
            rep = "{}< {} />".format(offset, header)
        else:
            rep = "{}< {} >{}</ {} >".format(offset, header, content, self.tag)
        return rep


# XML parser tools
_dict_regexp = re.compile(r"(?P<key>\S+)=(?P<value>[\S]+)")
def _build_dict_attrib(dict_string):
    dict_string = dict_string.strip()
    string_match = _dict_regexp.findall(dict_string)
    attrib = OrderedDict()
    for (key, value) in string_match:
        attrib[key] = value.replace('"', '')
    return attrib


_xml_header_regexp = re.compile(r'(<\?\s*\w*\s*(\w+=[\w+|\s+|"|\.|\-]+)*\s*\?>)')
_xml_header_regexp_begin = re.compile(r'^<\?\s*(?P<tag>\w*)\s*(?P<attrib>(\w+=[\w+|\s+|"|\.|\-]+)*)\s*\?>')
def _find_xml_header(xml_string):
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


_xml_comment_regexp = re.compile(r"^(?P<all><\!--\s*(?P<comment>.*)\s*-->)")
def _find_comment(xml_string):
    match_comment = _xml_comment_regexp.match(xml_string)
    if not match_comment:
        return xml_string, None
    else:
        text = match_comment.groupdict()["comment"]
        comment = Comment(comment=text)
        xml_string = xml_string.replace(match_comment.groupdict()["all"], "")
        return xml_string, comment


_xml_single_part_element_regexp = re.compile(r'^(?P<all><\s*(?P<tag>\w+)\s*(?P<attrib>(\w+=[\w+|\s+|"]+)*)\s*/>)')
_xml_init_two_parts_element_regexp = re.compile(r'^(?P<begin><\s*(?P<tag>\w+)\s*(?P<attrib>([^><])*)\s*>)')
_xml_string_init_element_replace = r'^(?P<begin><\s*(?P<tag>{})\s*(?P<attrib>([^><])*)\s*>)'
_xml_string_content_element = r'(?P<content>.*)'
_xml_string_end_element_replace = r'(?P<end></\s*{}\s*>)'
_xml_string_two_parts_element_replace = _xml_string_init_element_replace + _xml_string_content_element + \
                                        _xml_string_end_element_replace
def _find_element(xml_string):
    xml_string = xml_string.strip()
    match_single_part = _xml_single_part_element_regexp.match(xml_string)
    print(xml_string)
    if match_single_part:
        tag = match_single_part.groupdict()["tag"]
        attrib = match_single_part.groupdict()["attrib"]
        attrib = _build_dict_attrib(attrib)
        element = Element(tag=tag, attrib=attrib)
        xml_string = xml_string.replace(match_single_part.groupdict()["all"], "")
        return xml_string, element
    else:
        match_first_part = _xml_init_two_parts_element_regexp.match(xml_string)
        if match_first_part:
            tag = match_first_part.groupdict()["tag"]
            match_two_strings = re.compile(_xml_string_two_parts_element_replace.format(tag, tag)).match(xml_string)
            attrib = match_two_strings.groupdict()["attrib"]
            attrib = _build_dict_attrib(attrib)
            begin = match_two_strings.groupdict()["begin"]
            end = match_two_strings.groupdict()["end"]
            content = match_two_strings.groupdict()["content"]
            if end in content:
                content = content.split(end)[0]
            sub_xml_string, text = _find_text(content)
            print(len(sub_xml_string), sub_xml_string)
            print(begin + content + end)
            if len(text) == 0:
                    text = None
            element = Element(tag=tag, text=text, attrib=attrib)
            while len(sub_xml_string) > 0:
                print(">>>>sub_xml_string<<<<", len(sub_xml_string), sub_xml_string)
                sub_xml_string, subelement = _find_comment(sub_xml_string)
                if subelement is not None:
                    element.append(subelement)
                    print(">>>subelement<<<<", subelement)
                    print(">>>element<<<<", element)
                else:
                    sub_xml_string, subelement = _find_element(sub_xml_string)
                    if subelement is not None:
                        element.append(subelement)
                        print(">>>subelement<<<<", subelement)
                        print(">>>element<<<<", element)
                    else:
                        raise Exception("Content do not match anything know as a XML beacon.")
            xml_string = xml_string.replace(begin+content+end, "")
            print(">>>>", xml_string)
            print(">>>>", element)
            return xml_string, element
        else:
            raise Exception("It seems that there is a problem in the XML file...")


def _find_text(xml_string, fatal=False):
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
            xml_string = xml_string[0:rank_end_last_element]
        else:
            end_text = ""
        if rank_start_init_element > 0:
            init_text = xml_string[0:(rank_start_init_element-1)]
            xml_string = xml_string[rank_start_init_element:]
        else:
            init_text = ""
        xml_text = " ".join([init_text, end_text])
    xml_text = xml_text.strip()
    xml_string = xml_string.strip()
    return xml_string, xml_text


def xml_parser(xml_string):
    if not isinstance(xml_string, six.string_types):
        raise TypeError("Argument must be a string or equivalent, not %s." % type(xml_string))
    # Some pre-treatments on the string
    xml_string = xml_string.strip()
    xml_string = xml_string.replace("\n", "")
    xml_string = xml_string.replace("\t", "")
    # Check init or end text (there should not have been any but let's check
    xml_string, text = _find_text(xml_string, fatal=True)
    print(xml_string)
    # Check for header
    xml_string, header = _find_xml_header(xml_string)
    print(header)
    print(xml_string)
    # Check for root element (there should not have comment at this place)
    xml_string, root_element = _find_element(xml_string)
    print(root_element)
    # Check that len of xml_string is 0
    if len(xml_string) > 0:
        raise Exception("The XML string should have a length of 0.")
    return text, header, root_element


def xml_file_parser(xml_file):
    with open(xml_file) as opened_file:
        xml_content = opened_file.readlines()
    xml_string = "\n".join(xml_content)
    return xml_parser(xml_string)

if __name__ == "__main__":
    my_xml_file = "/home/rigoudyg/dev/dr2xml/tests/test_a4SST_AGCM_1960/output_test_python2/dr2xml_trip.xml"
    text, header, root_element = xml_file_parser(my_xml_file)
    print(text)
    print(header.dump())
    print(root_element.dump())
