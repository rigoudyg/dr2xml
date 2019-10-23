#!/usr/bin/python
# coding: utf-8

"""
Comments
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import re

from xml_writer.beacon import Beacon
from xml_writer.utils import encode_if_needed


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


# XML comment regexp
_xml_comment_regexp = re.compile(r"^(?P<all>\s?<\!--\s?(?P<comment>((?!<\!--)(?!-->).)+)\s?-->)\s?")


def _find_xml_comment(xml_string, verbose=False):
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