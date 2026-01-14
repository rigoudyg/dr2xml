#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals

import six
import argparse

def check_bool(value):
    if isinstance(value, bool):
        return value
    elif isinstance(value, (six.string_types, int)):
        if value in ["", "0", "no", "none", "None", "False", "false", 0]:
            return False
        elif value in ["1", "yes", "True", "true", 1]:
            return True
        else:
            try:
                return bool(value)
            except ValueError:
                raise argparse.ArgumentTypeError("%s is not a boolean" % value)
    else:
        raise TypeError("Unexpected case")


def check_int(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, six.string_types) and value in ["none", "None", ""]:
        return None
    else:
        try:
            value = int(value)
            return value
        except ValueError:
            raise argparse.ArgumentTypeError("%s is not an integer" % value)

def check_none_or_other(value):
    if value is None or value in ["", "none", "None"]:
        return None
    elif isinstance(value, six.string_types):
        return value.strip()
    else:
        return str(value).strip()