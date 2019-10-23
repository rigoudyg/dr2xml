#!/usr/bin/python
# coding: utf-8

"""
Pre-treatment tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import re

import six


def _pre_xml_string_format(xml_string, verbose=False):
    if not isinstance(xml_string, six.string_types):
        raise TypeError("Argument must be a string or equivalent, not %s." % type(xml_string))
    # Some other pre-treatments on the string
    xml_string = xml_string.replace("\n", " ")
    xml_string = xml_string.replace("\t", " ")
    xml_string = xml_string.strip()
    xml_string = xml_string.split(" ")
    xml_string = " ".join([m for m in xml_string if len(m) > 0])
    # Initialize the dictionary of strings to be replaced
    to_replace = dict()
    # Initialize the comments' positions list
    begin_comment_positions = [m.start() for m in re.compile(r"<!--").finditer(xml_string)]
    end_comment_positions = [m.end() - 1 for m in re.compile(r"-->").finditer(xml_string)]
    if len(begin_comment_positions) != len(end_comment_positions):
        raise Exception("All comments must be closed")
    comments_positions = [(comment_begin, comment_end) for (comment_begin, comment_end) in zip(begin_comment_positions, end_comment_positions)]
    if verbose:
        print("<<<pre_xml_string_format: comment_positions>>>", len(comments_positions))
    # Initialize the double quotes' positions list
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
    # Initialize the single quotes' positions list
    single_quotes_positions_tmp = [m.start() for m in re.compile(r"'").finditer(xml_string)]
    single_quotes_positions = list()
    for pos in single_quotes_positions_tmp:
        if _find_in_out(pos, comments_positions, verbose=False) or \
                _find_in_out(pos, double_quotes_positions, verbose=False):
            single_quotes_positions.append(pos)
    single_quotes_positions_tmp = sorted(list(set(single_quotes_positions_tmp) - set(single_quotes_positions)))
    i = 0
    to_add = list()
    while i < len(single_quotes_positions_tmp):
        pos = single_quotes_positions_tmp[i]
        if ((pos > 0 and xml_string[pos - 1] == "=") or
            (pos > 1 and xml_string[pos - 2] == "=" and xml_string[pos - 1] == " ")) and \
                i < len(single_quotes_positions_tmp) - 1:
            next_pos = single_quotes_positions_tmp[i + 1]
            xml_string = replace_char_at_pos_by_string(xml_string, "'", '"', pos, pos, verbose=verbose)
            xml_string = replace_char_at_pos_by_string(xml_string, "'", '"', next_pos, next_pos, verbose=verbose)
            to_add.extend([pos, next_pos])
            i += 2
        else:
            single_quotes_positions.append(pos)
            i += 1
    single_quotes_positions_tmp = sorted(list(set(single_quotes_positions_tmp) - set(single_quotes_positions)))
    single_quotes_positions_tmp = sorted(list(set(single_quotes_positions_tmp) - set(to_add)))
    if len(single_quotes_positions_tmp) > 0:
        raise Exception("Find additional single quotes and do not know what to do with them...",
                        len(single_quotes_positions_tmp), single_quotes_positions_tmp)
    to_add = [(to_add[2 * pos], to_add[2 * pos + 1]) for pos in range(len(to_add) // 2)]
    double_quotes_positions.extend(to_add)
    double_quotes_positions = sorted(double_quotes_positions, key=lambda t: t[0])
    if verbose:
        print("<<<pre_xml_string_format: single_quotes_positions>>>", len(single_quotes_positions))
        print("<<<pre_xml_string_format: double_quotes_positions>>>", len(double_quotes_positions))

    # Look for reserved symbols (< and >) and replace them
    possible_greater_positions = [m.start() for m in re.compile(r">").finditer(xml_string)]
    if verbose:
        print("<<<pre_xml_string_format: possible_greater_positions>>>", len(possible_greater_positions))

    possible_lower_positions = [m.start() for m in re.compile(r'<').finditer(xml_string)]
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
                to_replace[l_pos] = ("<", "&lt")
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
                to_replace[g_pos] = (">", "&gt")
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
                to_replace[possible_greater_positions[g]] = (">", "&gt")
            else:
                beacon_open = False
            g += 1
        else:
            raise Exception("There are two many '>' in XML string.")
    if beacon_open or l != len(possible_lower_positions) or g != len(possible_greater_positions):
        raise Exception("There is issues in '>' and '<' usage in XML string")
    greater_positions = [i for i in to_replace if to_replace[i] == (">", "&gt")]
    lower_positions = [i for i in to_replace if to_replace[i] == ("<", "&lt")]
    # Replace all that needs to be replaced
    if verbose:
        print("<<<pre_xml_string_format: greater than found:>>>", len(greater_positions), greater_positions, [xml_string[a-20:a+20] for a in greater_positions])
        print("<<<pre_xml_string_format: lower than found:>>>", len(lower_positions), lower_positions, [xml_string[a-20:a+20] for a in lower_positions])
    new_xml_string = xml_string
    for i in sorted(list(to_replace), reverse=True):
        if verbose:
            print("<<<pre_xml_string_format: before replacement:>>>", new_xml_string[i - 2:i + 20])
        new_xml_string = replace_char_at_pos_by_string(new_xml_string, to_replace[i][0],
                                                       to_replace[i][1], i, i + len(to_replace[i][0]) - 1,
                                                       verbose=verbose)
        if verbose:
            print("<<<pre_xml_string_format: after replacement:>>>", new_xml_string[i - 2:i + 20])
    if verbose:
        print("<<<pre_xml_string_format: greater than found:>>>", len(greater_positions), greater_positions, [new_xml_string[a-20:a+20] for a in greater_positions])
        print("<<<pre_xml_string_format: lower than found:>>>", len(lower_positions), lower_positions, [new_xml_string[a-20:a+20] for a in lower_positions])
    return " ".join(new_xml_string.split(" "))


def replace_char_at_pos_by_string(complete_string, string_in, replace_out, pos_init, pos_end, verbose=False):
    if verbose:
        print("<<<replace_char_at_pos_by_string>>> len of input string", len(complete_string))
    single_char = pos_init == pos_end
    if pos_init < 0 or (not single_char and pos_end > len(complete_string)) or \
            (single_char and pos_end >= len(complete_string)):
        raise Exception("The string to be replaced is not in the complete string")
    if (single_char and complete_string[pos_init] != string_in) or \
            (not single_char and complete_string[pos_init:pos_end] != string_in):
        raise Exception("The string to be replaced is not the one present: %s / %s" %
                        (string_in, complete_string[pos_init:pos_end]))
    if single_char:
        if pos_init == 0:
            return replace_out + complete_string[pos_end + 1:]
        elif pos_end == len(complete_string) - 1:
            return complete_string[:pos_init] + replace_out
        else:
            return complete_string[:pos_init] + replace_out + complete_string[pos_end + 1:]
    else:
        if pos_init == 0:
            return replace_out + complete_string[pos_end:]
        elif pos_end == len(complete_string):
            return complete_string[:pos_init] + replace_out
        else:
            return complete_string[:pos_init] + replace_out + complete_string[pos_end:]


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