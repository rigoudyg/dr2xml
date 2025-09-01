#!/usr/bin/env python
# coding: utf-8

"""
Elements
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict
from copy import deepcopy, copy

from .beacon import Beacon
from utilities.encoding_tools import encode_if_needed, decode_if_needed


class Element(Beacon):
    """
    Class to deal with xml elements.
    """
    def __init__(self, tag, text=None, attrib=OrderedDict()):
        """

        :param tag:
        :param text:
        :param attrib:
        """
        super(Element, self).__init__()
        self.tag = tag.strip()
        self.text = text
        self.attrib = deepcopy(attrib)
        self.children = list()

    def __eq__(self, other):
        """

        :param other:
        :return:
        """
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
        """

        :return:
        """
        return len(self.children)

    def __copy__(self):
        """

        :return:
        """
        element = type(self).__call__(tag=self.tag, text=self.text, attrib=deepcopy(self.attrib))
        element.update_level(self.level)
        for child in self.children:
            element.children.append(copy(child))
        return element

    def dump(self):
        """

        :return:
        """
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
        """

        :param text:
        :return:
        """
        if len(text) > 0:
            if self.text is None:
                self.text = text
            else:
                self.text = "\n".join([self.text, text])

    def __getitem__(self, item):
        """

        :param item:
        :return:
        """
        return self.children[item]

    def __setitem__(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        if value is not None:
            if is_xml_element(value):
                value.update_level(self.level + 1)
                value.parent = self
                self.children[key] = value
            else:
                raise TypeError("Could not set an element of type %s as an XML element child." % type(value))

    def __delitem__(self, key):
        """

        :param key:
        :return:
        """
        self.remove(self[key])

    def append(self, element):
        """

        :param element:
        :return:
        """
        if element is not None:
            if not is_xml_element(element):
                raise TypeError("Could not append an element of type %s to an XML element." % type(element))
            element.update_level(self.level + 1)
            element.parent = self
            self.children.append(element)

    def extend(self, elements):
        """

        :param elements:
        :return:
        """
        if elements is not None:
            for (rank, element) in enumerate(elements):
                if not is_xml_element(element):
                    raise TypeError("Could not extend an XML element with elements of type %s." % type(element))
                else:
                    elements[rank].update_level(self.level + 1)
                    elements[rank].parent = self
            self.children.extend(elements)

    def insert(self, index, element):
        """

        :param index:
        :param element:
        :return:
        """
        if element is not None:
            if not is_xml_element(element):
                raise TypeError("Could not insert an element of type %s to an XML element." % type(element))
            element.update_level(self.level + 1)
            element.parent = self
            self.children.insert(index, element)

    def replace(self, index, element):
        """

        :param index:
        :param element:
        :return:
        """
        if element is not None:
            if not is_xml_element(element):
                raise TypeError("Could not replace and XML element by an element of type %s to an XML element." %
                                type(element))
            element.update_level(self.level + 1)
            element.parent = self
            self.children[index] = element

    def remove(self, element):
        """

        :param element:
        :return:
        """
        if element is not None:
            if not is_xml_element(element):
                raise TypeError("Could not append an remove of type %s to an XML element." % type(element))
            self.children.remove(element)

    def update_level(self, new_level):
        """

        :param new_level:
        :return:
        """
        super(Element, self).update_level(new_level)
        if len(self.children) > 0:
            for i in range(len(self.children)):
                self.children[i].update_level(new_level + 1)

    def _dump_children(self):
        """

        :return:
        """
        if len(self.children) > 0:
            return "\n".join([decode_if_needed(child.dump()) for child in self.children])
        else:
            return ""

    def _dump_attrib(self, sort=False):
        """

        :param sort:
        :return:
        """
        return self.dump_dict(deepcopy(self.attrib), sort=sort)

    def get_attrib(self, key, parent=True, use_default=False, default=None):
        if key in self.attrib:
            return self.attrib[key]
        elif parent is True and self.parent is not None:
            return self.parent.get_attrib(key, parent=parent, use_default=use_default, default=default)
        elif parent in ["single", ] and self.parent is not None:
            return self.parent.get_attrib(key, parent=False, use_default=use_default, default=default)
        elif use_default:
            return default
        else:
            raise KeyError("Could not find a value for attribute %s" % key)


def is_xml_element(element):
    """

    :param element:
    :return:
    """
    try:
        return element.is_xml_element()
    except:
        return False
