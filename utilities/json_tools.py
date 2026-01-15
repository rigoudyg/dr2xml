from __future__ import division, absolute_import, print_function, unicode_literals

import copy
import json
import os
from collections import OrderedDict

from utilities.logger import get_logger


def read_json_content(filename):
    logger = get_logger()
    if os.path.isfile(filename):
        with open(filename) as fp:
            content = json.load(fp)
            return content
    else:
        logger.error("Could not find the json file at %s" % filename)
        raise OSError("Could not find the json file at %s" % filename)


def format_json_before_writing(settings):
    if isinstance(settings, (dict, OrderedDict)):
        for key in list(settings):
            settings[key] = format_json_before_writing(settings[key])
    elif isinstance(settings, (list, tuple)):
        for i in range(len(settings)):
            settings[i] = format_json_before_writing(settings[i])
    elif isinstance(settings, type):
        settings = str(settings)
    return settings


def write_json_content(filename, settings):
    with open(filename, "w") as fp:
        json.dump(format_json_before_writing(copy.deepcopy(settings)), fp)
