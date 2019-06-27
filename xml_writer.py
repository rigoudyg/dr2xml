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
        self.attrib = OrderedDict()
        self.children = list()
        self.tag = None

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return self.dump()

    def __getitem__(self, index):
        return self.children[index]

    def __setitem__(self, index, element):
        self.children[index] = element

    def __delitem__(self, index):
        del self.children[index]

    def is_xml_element(self):
        return isinstance(self, (Beacon, Element, Comment, Header))

    def dump(self):
        raise NotImplementedError()

    def update_level(self, new_level):
        if self.level != new_level:
            self.level = new_level
            if len(self.children) > 0:
                i = 0
                while i < len(self.children):
                    self.children[i].update_level(new_level + 1)
                    i += 1

    def copy(self):
        element = Beacon()
        element.tag = copy.copy(self.tag)
        element.level = copy.copy(self.level)
        element.attrib = copy.deepcopy(self.attrib)
        element.children = list()
        for child in self.children:
            element.children.append(child.copy())
        return element

    @staticmethod
    def correct_attrib(attrib):
        if not isinstance(attrib, (dict, OrderedDict)):
            raise TypeError("attrib must be a dict or an OrderDict.")
        corrected_attrib = OrderedDict()
        for (key, value) in attrib.items():
            corrected_attrib[str(key)] = str(value)
        return corrected_attrib

    def _dump_attrib(self, sorted=False):
        if len(self.attrib) > 0:
            list_key_value = list()
            if sorted:
                for key in sorted(list(self.attrib)):
                    list_key_value.append((key, self.attrib[key]))
            else:
                for (key, value) in self.attrib.items():
                    list_key_value.append((key, value))
            return " ".join(['{}={}'.format(key, '"{}"'.format(value)) for (key, value) in list_key_value])
        else:
            return None

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
        if len(self.children) > 0:
            return "\n".join([child.dump().decode("utf-8") for child in self.children])
        else:
            return ""


class Comment(Beacon):
    """
    Class to deal with XML comments.
    """
    def __init__(self, comment):
        super(Comment, self).__init__()
        # Deal with comment attribute
        self.comment = comment

    def copy(self):
        element = Comment(comment=self.comment)
        element.level = copy.copy(self.level)
        element.attrib = copy.deepcopy(self.attrib)
        element.children = list()
        for child in self.children:
            element.children.append(child.copy())
        element.tag = copy.copy(self.tag)
        return element

    def dump(self):
        rep = "\t"*self.level+"<!-- %s -->" % self.comment
        return rep.encode("utf-8")


class Header(Beacon):
    """
    Class to deal with xml header.
    """
    def __init__(self, tag, attrib=OrderedDict()):
        super(Header, self).__init__()
        # Deal with attrib attribute
        self.attrib = copy.deepcopy(attrib)
        self.tag = tag

    def copy(self):
        element = Header(tag=self.tag)
        element.level = copy.copy(self.level)
        element.attrib = copy.deepcopy(self.attrib)
        element.children = list()
        for child in self.children:
            element.children.append(child.copy())
        return element

    def dump(self):
        offset = "\t" * self.level
        if len(self.attrib) > 0:
            rep = offset + '<?{} {} ?>'.format(self.tag, self._dump_attrib())
        else:
            rep = offset + '<?{} ?>'.format(self.tag)
        return rep.encode("utf-8")


class Element(Beacon):
    """
    Class to deal with xml elements.
    """
    def __init__(self, tag, text=None, attrib=OrderedDict()):
        super(Element, self).__init__()
        # Deal with tag attribute
        self.tag = tag
        # Deal with attrib attribute
        self.attrib = copy.deepcopy(attrib)
        # Deal with text attribute
        self.text = text

    def __len__(self):
        return len(self.children)

    def copy(self):
        element = Element(tag=self.tag, text=self.text)
        element.level = copy.copy(self.level)
        element.attrib = copy.deepcopy(self.attrib)
        element.children = list()
        for child in self.children:
            element.children.append(child.copy())
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
            rep = "{}<{} />".format(offset, header)
        else:
            rep = "{}<{} >{}</{} >".format(offset, header, content, self.tag)
        return rep.encode("utf-8")


# XML parser tools
_dict_regexp = re.compile(r'(?P<key>\S+)="(?P<value>[^"]+)"')
_xml_header_regexp = re.compile(r'(<\?\s*\w*\s*(([^><])*)\s*\?>)')
_xml_header_regexp_begin = re.compile(r'^<\?\s*(?P<tag>\w*)\s*(?P<attrib>([^><])*)\s*\?>')
_xml_comment_regexp = re.compile(r"^(?P<all><\!--\s*(?P<comment>((?!<!--)(?!-->).)+)\s*-->)")
_xml_single_part_element_regexp = re.compile(r'^(?P<all><\s*(?P<tag>\w+)\s*(?P<attrib>([^><])*)\s*/>)')
#_xml_init_two_parts_element_regexp = re.compile(r'^(?P<begin><\s*(?P<tag>\w+)\s*(?P<attrib>([^><])*)\s*>)')
_xml_string_first_element_replace = r'(?P<begin><\s*(?P<tag>{})\s*(?P<attrib>([^><])*)\s*>)'
_xml_string_init_element_replace = r'^'+_xml_string_first_element_replace
_xml_init_two_parts_element_regexp = re.compile(_xml_string_init_element_replace.format(r"\w+"))
_xml_string_content_element = r'(?P<content>\s*{}\s*)'
_xml_string_end_element_replace = r'(?P<end></\s*{}\s*>)'
_xml_string_two_parts_element_replace = _xml_string_init_element_replace + _xml_string_content_element + \
                                        _xml_string_end_element_replace


def _build_dict_attrib(dict_string):
    dict_string = dict_string.strip()
    string_match = _dict_regexp.findall(dict_string)
    attrib = OrderedDict()
    for (key, value) in string_match:
        attrib[key] = value.replace('"', '')
    return attrib


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


def _find_xml_comment(xml_string, verbose=False):
    if verbose:
        print("<<<find_xml_comment: XML_STRING before>>>", len(xml_string), xml_string)
    match_comment = _xml_comment_regexp.match(xml_string)
    if not match_comment:
        if verbose:
            print("<<<find_xml_comment: XML_STRING after>>>", len(xml_string), xml_string)
        return xml_string, None
    else:
        text = match_comment.groupdict()["comment"]
        text = text.strip()
        comment = Comment(comment=text)
        xml_string = xml_string.replace(match_comment.groupdict()["all"], "")
        if verbose:
            print("<<<find_xml_comment: XML_STRING after>>>", len(xml_string), xml_string)
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
        # Check if the element is a XML element
        xml_string, element = _find_element(xml_string, verbose=verbose)
        if element is not None:
            xml_string = xml_string.strip()
            if verbose:
                print("<<<build_element: XML_STRING after element>>>", len(xml_string), xml_string)
            return xml_string, element
        else:
            raise Exception("Could not find what the element could be...")


def _find_element(xml_string, verbose=False):
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
        match_first_part = _xml_init_two_parts_element_regexp.match(xml_string)
        if match_first_part:
            # Get as most information as possible
            tag = match_first_part.groupdict()["tag"]
            match_two_strings = re.compile(_xml_string_two_parts_element_replace.format(tag, r".*", tag)).match(xml_string)
            attrib = match_two_strings.groupdict()["attrib"]
            attrib = _build_dict_attrib(attrib)
            begin = match_two_strings.groupdict()["begin"]
            end = match_two_strings.groupdict()["end"]
            # Find out if the content contains a subpart with the same tag
            content = match_two_strings.groupdict()["content"]
            if verbose:
                print("<<<find_element: CONTENT before>>>", len(content), content)
            finditer_matches_first_part_in_content = \
                re.compile(_xml_string_first_element_replace.format(tag)).finditer(content)
            find_positions_first_part_in_content = list()
            last_position = 0
            for match in finditer_matches_first_part_in_content:
                last_position = content.find(match.groupdict()["begin"], last_position + 1)
                find_positions_first_part_in_content.append(last_position)
            if verbose:
                print("<<<find_element: rank match first part>>>", len(find_positions_first_part_in_content), find_positions_first_part_in_content)
            finditer_matches_last_part_in_content = \
                re.compile(_xml_string_end_element_replace.format(tag)).finditer(content)
            find_positions_last_part_in_content = list()
            last_position = 0
            for match in finditer_matches_last_part_in_content:
                last_position = content.find(match.groupdict()["end"], last_position + 1)
                find_positions_last_part_in_content.append(last_position)
            if verbose:
                print("<<<find_element: rank match last part>>>", len(find_positions_last_part_in_content), find_positions_last_part_in_content)
            # Find out where the content really stop
            if len(find_positions_first_part_in_content) != 0 and len(find_positions_last_part_in_content) != 0:
                # Case of nested beacons with same tag
                position_start = 0
                nb_positions_start = len(find_positions_first_part_in_content)
                position_end = 0
                nb_positions_end = len(find_positions_last_part_in_content)
                find_end = False
                nb_nested = 0
                while position_start < nb_positions_start and position_end < nb_positions_end and not find_end:
                    if verbose:
                        print("<<<find_element: POSITIONS START/END NESTED before>>>", position_start, "/", nb_positions_start, position_end, "/", nb_positions_end, nb_nested)
                    if find_positions_last_part_in_content[position_end] < find_positions_first_part_in_content[position_start]:
                        if nb_nested > 0:
                            position_end += 1
                            nb_nested -= 1
                        else:
                            content = content[0:find_positions_last_part_in_content[position_end]]
                            find_end = True
                    else:
                        nb_nested += 1
                        position_start += 1
                if verbose:
                    print("<<<find_element: POSITIONS START/END NESTED after>>>", position_start, "/",
                          nb_positions_start, position_end, "/", nb_positions_end, nb_nested)

                if not find_end and position_start == nb_positions_start and position_end == nb_positions_end - nb_nested:
                    # Case of nested and finished beacons with same tag
                    find_end = True
                    position_end += nb_nested
                    nb_nested = 0
                if not find_end:
                    raise Exception("There is a problem with the xml file... All opened beacon must be closed.")
            elif len(find_positions_last_part_in_content) != 0 or len(find_positions_first_part_in_content) != 0:
                raise Exception("There is a problem with the xml file... All opened beacon must be closed.")
            if verbose:
                print("<<<find_element: CONTENT after>>>", len(content), content)
            # Create string to remove
            string_to_remove = begin + content + end
            # Separate children from text
            sub_xml_string, text = _find_text(content)
            sub_xml_string = sub_xml_string.strip()
            if len(text) == 0:
                    text = None
            # Create the element and its children
            element = Element(tag=tag, text=text, attrib=attrib)
            while len(sub_xml_string) > 0:
                sub_xml_string, subelement = _build_element(sub_xml_string, verbose=verbose)
                sub_xml_string = sub_xml_string.strip()
                if subelement is not None:
                    element.append(subelement)
            xml_string = xml_string.replace(string_to_remove, "")
            return xml_string, element
        else:
            raise Exception("It seems that there is a problem in the XML file...")


def _find_text(xml_string, fatal=False, verbose=False):
    xml_string = xml_string.strip()
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


def xml_parser(xml_string, verbose=False):
    if not isinstance(xml_string, six.string_types):
        raise TypeError("Argument must be a string or equivalent, not %s." % type(xml_string))
    # Some pre-treatments on the string
    xml_string = xml_string.replace("\n", "")
    xml_string = xml_string.replace("\t", " ")
    xml_string = xml_string.strip()
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
    # Check for root element (there should not have comment at this place)
    if len(xml_string) > 0:
        xml_string, root_element = _find_element(xml_string, verbose=verbose)
    # Check for additional comments
    comment = True
    while comment and len(xml_string) > 0:
        xml_string, comment = _build_element(xml_string, verbose=verbose)
        if comment is not None:
            comments.append(comment)
    # Check that len of xml_string is 0
    if len(xml_string) > 0:
        raise Exception("The XML string should have a length of 0.")
    return text, comments, header, root_element


def xml_file_parser(xml_file, verbose=False):
    with open(xml_file, "rb") as opened_file:
        xml_content = opened_file.read().decode(encoding="utf-8")
    xml_string = "\n".join([line for line in xml_content])
    return xml_parser(xml_string, verbose=verbose)


if __name__ == "__main__":
    for my_xml_file in [
        #"/home/rigoudyg/dev/dr2xml/tests/test_a4SST_AGCM_1960/output_ref_python2/dr2xml_trip.xml",
        #"/home/rigoudyg/dev/dr2xml/tests/common/xml_files//./ping_surfex.xml",
        #"/home/rigoudyg/dev/dr2xml/tests/common/xml_files/iodef.xml",
        "/home/rigoudyg/dev/dr2xml/tests/common/xml_files//./surfex_fields.xml",
        #"/home/rigoudyg/dev/dr2xml/tests/common/xml_files/atmo_fields.xml",
    ]:
        print(my_xml_file)
        text, comments, header, root_element = xml_file_parser(my_xml_file, verbose=True)
        print(text)
        print(comments)
        print(header)
        print(root_element)
