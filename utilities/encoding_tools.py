from __future__ import division, absolute_import, print_function, unicode_literals

import sys

from .logger import get_logger

python_version = sys.version


def encode_if_needed(a_string, encoding="utf-8"):
    """
    If needed, encode the python string ``a_string`` into the encoding specify by ``encoding``.

    :param six.string_types a_string: the string to encode
    :param six.string_types encoding: the encoding to be used
    :return: a string encoded if needed
    """
    logger = get_logger()
    if python_version.startswith("2."):
        return a_string.encode(encoding)
    elif python_version.startswith("3."):
        return a_string
    else:
        logger.error("Unknown Python version %s" % python_version.split()[0])
        raise OSError("Unknown Python version %s", python_version.split()[0])


def decode_if_needed(a_string, encoding="utf-8"):
    """
    If needed, decode the python string ``a_string`` into the encoding specify by ``encoding``.

    :param six.string_types a_string: the string to decode
    :param six.string_types encoding: the encoding to be used
    :return: a string decoded if needed
    """
    logger = get_logger()
    if sys.version.startswith("2."):
        return a_string.decode(encoding)
    elif python_version.startswith("3."):
        return a_string
    else:
        logger.error("Unknown Python version %s" % python_version.split()[0])
        raise OSError("Unknown Python version %s", python_version.split()[0])
