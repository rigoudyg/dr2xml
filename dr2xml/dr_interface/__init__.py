#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between data request and dr2xml
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.settings_interface import get_settings_values

data_request_version = get_settings_values("internal", "data_request_used")


if data_request_version in ["CMIP6", ]:
    from .CMIP6 import *
elif data_request_version in ["no", "none", "None", None]:
    from .no import *
else:
    raise ValueError("The data request specified (%s) is not known." % data_request_version)
