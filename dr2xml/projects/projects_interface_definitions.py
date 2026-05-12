#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface to project settings
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import os
import re
from collections import OrderedDict
from importlib.util import spec_from_file_location, module_from_spec

import six

from dr2xml.config import get_config_variable
from dr2xml.settings_interface.py_settings_interface import format_dict_for_printing, is_key_in_lset, \
    get_variable_from_lset_without_default, is_key_in_sset, get_variable_from_sset_without_default
from dr2xml.utils import Dr2xmlError
from utilities.json_tools import read_json_content
from utilities.logger import get_logger


def val_or_func(key, element, project_funcs=None):
    if isinstance(element, dict):
        element_type = element.get("type")
        if element_type is None:
            return element
        elif element_type in ["condition", ]:
            return ConditionSettings.from_dict(key, element, project_funcs=project_funcs)
        elif element_type in ["func", ]:
            return FunctionSettings.from_dict(key, element, project_funcs=project_funcs)
        else:
            return ValueSettings.from_dict(key, element, project_funcs=project_funcs)
    else:
        return element


def return_value(value, init_dict=dict(), common_dict=dict(), internal_dict=dict(), additional_dict=dict(),
                 allow_additional_keytypes=True, project_funcs=None, common_tag=dict(), **attrs):
    if isinstance(value, (ValueSettings, FunctionSettings, ConditionSettings)):
        return value.__call__(common_dict=common_dict, internal_dict=internal_dict, additional_dict=additional_dict,
                              allow_additional_keytypes=allow_additional_keytypes, init_dict=init_dict,
                              project_funcs=project_funcs, common_tag=common_tag, **attrs)
    else:
        return True, value


def determine_value(key_type=None, keys=list(), func=None, fmt=None, src=None, common_dict=dict(), internal_dict=dict(),
                    additional_dict=dict(), allow_additional_keytypes=True, init_dict=dict(), project_funcs=None,
                    common_tag=dict()):
    logger = get_logger()
    if key_type in ["combine", "merge"] or (key_type is None and func is not None):
        keys = [return_value(key, common_dict=common_dict, internal_dict=internal_dict, init_dict=init_dict,
                             additional_dict=additional_dict, allow_additional_keytypes=allow_additional_keytypes,
                             project_funcs=project_funcs, common_tag=common_tag)
                for key in keys]
        key_found = all([elt[0] for elt in keys])
        if key_found:
            keys = [elt[1] for elt in keys]
            if fmt is None and key_type in ["combine", ]:
                raise ValueError("If key_type=combine, fmt must not be None")
            else:
                found = True
        else:
            found = False
            value = None
        if found:
            if key_type in ["combine", ]:
                keys = [",".join(key) if isinstance(key, (list, tuple)) else key for key in keys]
                value = fmt.format(*keys)
            elif key_type in ["merge", ]:
                value = list()
                for key in keys:
                    value.extend(key)
            else:
                if isinstance(func, FunctionSettings):
                    found, value = func(*keys, additional_dict=additional_dict, internal_dict=internal_dict,
                                        init_dict=init_dict, common_dict=common_dict,
                                        allow_additional_keytypes=allow_additional_keytypes,
                                        project_funcs=project_funcs, common_tag=common_tag)
                else:
                    if isinstance(func, ValueSettings):
                        func_test, func_value = return_value(func, common_dict=common_dict, internal_dict=internal_dict,
                                                             additional_dict=additional_dict, init_dict=init_dict,
                                                             allow_additional_keytypes=allow_additional_keytypes,
                                                             prohect_funcs=project_funcs, common_tag=common_tag)
                        if not func_test:
                            logger.warning("Unable to determine function %s" % func)
                        else:
                            func = func_value
                    try:
                        value = func(*keys)
                        found = True
                    except BaseException as e:
                        logger.debug("Issue calling func %s with arguments %s" % (str(func), str(keys)))
                        logger.debug(str(e))
                        value = None
                        found = False
                if found and fmt is not None:
                    value = fmt.format(value)
    else:
        i_keys = 0
        if key_type in ["common", ]:
            value = common_dict
            found = True
        elif key_type in ["internal", ]:
            value = internal_dict
            found = True
        elif key_type in ["init", ]:
            value = init_dict
            found = True
        elif key_type in ["dict", ]:
            value = additional_dict
            found = True
        elif key_type in ["config", ]:
            if len(keys) == 0:
                raise ValueError("At least a key must be provided if key_type=config")
            else:
                try:
                    found, value = return_value(value=keys[i_keys], common_dict=common_dict, init_dict=init_dict,
                                                internal_dict=internal_dict, additional_dict=additional_dict,
                                                allow_additional_keytypes=allow_additional_keytypes,
                                                project_funcs=project_funcs)
                    if found:
                        value = get_config_variable(value)
                        i_keys += 1
                except (Dr2xmlError, ValueError, TypeError):
                    found = False
                    value = None
        elif key_type in ["laboratory", ]:
            if len(keys) == 0:
                value = format_dict_for_printing("lset")
                found = True
            else:
                found, value = return_value(value=keys[i_keys], common_dict=common_dict, init_dict=init_dict,
                                            internal_dict=internal_dict, additional_dict=additional_dict,
                                            allow_additional_keytypes=allow_additional_keytypes,
                                            project_funcs=project_funcs)
                if found:
                    found = is_key_in_lset(value)
                if found:
                    value = get_variable_from_lset_without_default(value)
                    i_keys += 1
        elif key_type in ["simulation", ]:
            if len(keys) == 0:
                value = format_dict_for_printing("sset")
                found = True
            else:
                found, value = return_value(value=keys[i_keys], common_dict=common_dict, init_dict=init_dict,
                                            internal_dict=internal_dict, additional_dict=additional_dict,
                                            allow_additional_keytypes=allow_additional_keytypes,
                                            project_funcs=project_funcs)
                if found:
                    found = is_key_in_sset(value)
                if found:
                    value = get_variable_from_sset_without_default(value)
                    i_keys += 1
        elif key_type in ["json", ]:
            found, src = return_value(value=src, common_dict=common_dict, internal_dict=internal_dict,
                                      additional_dict=additional_dict, init_dict=init_dict,
                                      allow_additional_keytypes=allow_additional_keytypes,
                                      project_funcs=project_funcs)
            if found:
                if not isinstance(src, six.string_types):
                    raise TypeError("src must be a string or a ValueSettings")
                else:
                    value = read_json_content(src)
            else:
                value = None
        elif allow_additional_keytypes:
            if key_type in ["data_request", ]:
                from dr2xml.dr_interface import get_dr_object
                value = get_dr_object("get_data_request")
                found = True
            elif key_type in ["vocabulary", ]:
                from dr2xml.vocabulary import get_vocabulary
                value = get_vocabulary()
                found = True
            elif key_type in ["variable", ] and "variable" in additional_dict:
                value = additional_dict["variable"]
                if isinstance(value, list):
                    value = value[0]
                value = value.__dict__
                found = True
            elif key_type in ["common_tag", ]:
                value = common_tag
                found = True
            else:
                value = None
                found = False
        else:
            value = None
            found = False
        if found:
            while found and i_keys < len(keys):
                found, key = return_value(keys[i_keys], common_dict=common_dict, internal_dict=internal_dict,
                                          additional_dict=additional_dict, init_dict=init_dict,
                                          allow_additional_keytypes=allow_additional_keytypes,
                                          project_funcs=project_funcs, common_tag=common_tag)
                if found:
                    if isinstance(value, (dict, OrderedDict)):
                        if key in value:
                            value = value[key]
                            i_keys += 1
                        else:
                            found = False
                    elif isinstance(value, (tuple, list, six.string_types)) and isinstance(key, int):
                        if isinstance(key, int) and key < len(value):
                            value = value[key]
                            i_keys += 1
                        else:
                            found = False
                    elif value is not None and key in ["__call__", ]:
                        value = value.__call__()
                        i_keys += 1
                    elif value is not None and key in value.__dir__():
                        value = value.__getattribute__(key)
                        i_keys += 1
                    elif value is not None and "__dict__" in value.__dir__():
                        value = value.__getattr__(key)
                        i_keys += 1
                    else:
                        found = False
        if found and func is not None:
            if not isinstance(value, list):
                value = [value, ]
            if isinstance(func, FunctionSettings):
                found, value = func(*value, additional_dict=additional_dict, internal_dict=internal_dict,
                                    init_dict=init_dict, common_dict=common_dict,
                                    allow_additional_keytypes=allow_additional_keytypes,
                                    project_funcs=project_funcs, common_tag=common_tag)
            else:
                try:
                    value = func(*value)
                    found = True
                except Exception as e:
                    logger.debug(str(e))
                    value = None
                    found = False
        if found and fmt is not None:
            if not isinstance(value, list):
                value = [value, ]
            value = fmt.format(*value)
    return found, value


class Settings(object):

    def __init__(self, *args, project_funcs=None, **kwargs):
        self.dict_default = self.init_dict_default()
        self.updated = set()
        for elt in self.dict_default:
            if elt in kwargs:
                self.updated.add(elt)
                val = kwargs[elt]
            else:
                val = self.dict_default[elt]
            self.__setattr__(elt, val)

    @classmethod
    def from_dict(cls, key, kwargs, additional_keys=False, project_funcs=None):
        raise NotImplementedError()

    def init_dict_default(self):
        return dict()

    def update(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Could not merge the following types: %s and %s" % (type(self), type(other)))

    def __str__(self):
        return "%s(%s)" % (type(self).__name__, {key: value for (key, value) in self.__dict__.items()
                                                 if key not in ["updated", ]}.__repr__())

    def __repr__(self):
        return self.__str__()

    def __call__(self, init_dict=dict(), internal_dict=dict(), common_dict=dict(), additional_dict=dict(),
                 allow_additional_keytypes=False, project_funcs=None, **attrs):
        raise NotImplementedError()

    def dump_doc(self, force_void=False):
        raise NotImplementedError("Dump documentation is not implemented for class %s" % type(self))

    def dump_doc_inner(self, value, force_void=False, format_struct=True, remove_new_lines=False,
                       force_format_struct=False):
        if isinstance(value, Settings):
            rep = value.dump_doc(force_void=force_void)
        elif isinstance(value, (list, set)):
            rep = list()
            if len(value) == 0 and force_void:
                rep.append(list())
            elif len(value) == 1 and not force_format_struct:
                rep.extend(self.dump_doc_inner(value[0], force_void=force_void, format_struct=format_struct))
            elif format_struct:
                rep.append("   ")
                for elt in value:
                    rep.extend(["   - %s" % subelt for subelt in self.dump_doc_inner(elt, force_void=force_void,
                                                                                     format_struct=format_struct)])
            else:
                for elt in value:
                    rep.extend(self.dump_doc_inner(elt, force_void=force_void, format_struct=format_struct))
        elif isinstance(value, (dict, OrderedDict)):
            rep = list()
            if len(value) == 0 and force_void:
                rep.append("%s" % type(value).__call__())
            else:
                if format_struct:
                    rep.append("   ")
                for elt in value:
                    if format_struct:
                        tmp_rep = "   - %s: %s"
                    else:
                        tmp_rep = "%s= %s"
                    val = self.dump_doc_inner(value[elt], force_void=force_void)
                    elt = self.dump_doc_inner(elt, force_void=force_void)
                    if len(val) == 1:
                        tmp_rep = tmp_rep % (elt[0], val[0])
                        rep.append(tmp_rep)
                    else:
                        tmp_rep = tmp_rep % (elt[0], "")
                        rep.append(tmp_rep)
                        rep.append("   ")
                        rep.extend(["      %s" % v for v in val])
        elif isinstance(value, six.string_types):
            if format_struct:
                rep = ["'%s'" % value, ]
            else:
                rep = ["%s" % value, ]
        elif isinstance(value, type(return_value)):
            rep = ["%s()" % value.__name__, ]
        else:
            rep = [value, ]
        if remove_new_lines:
            new_rep = list()
            for elt in rep:
                if isinstance(elt, six.string_types):
                    new_rep.append(elt.replace(os.linesep, "***newline***"))
                else:
                    new_rep.append(elt)
            rep = new_rep
        return rep


class ValueSettings(Settings):

    def init_dict_default(self):
        return dict(key=None, type=None, origin=None, keys=[], format=False, src=False, values=[])

    def __init__(self, *args, project_funcs=None, **kwargs):
        logger = get_logger()
        super(ValueSettings, self).__init__(*args, project_funcs=project_funcs, **kwargs)
        if "keys" in self.updated and not isinstance(self.keys, list):
            self.keys = [self.keys, ]
        self.keys = [val_or_func(self.key, elt, project_funcs=project_funcs) for elt in self.keys]
        if self.type in ["file", ]:
            if self.origin not in ["json", ]:
                logger.error("'Origin' must be specified among 'json' for %s, not %s" % (self.key, self.type))
                raise ValueError( "'Origin' must be specified among 'json' for %s, not %s" % (self.key, self.type))
            if isinstance(self.src, six.string_types) and not os.path.exists(self.src):
                logger.error("Source file provided for %s does not exists: %s")
        elif self.type in ["merge", ]:
            if not isinstance(self.values, list) or len(self.values) == 0:
                logger.error("Values must be specified for %s" % self.key)
                raise ValueError("Values must be specified for %s" % self.key)
        elif self.type in ["value", ]:
            if self.origin not in ["attrs", "common", "config", "dict", "init", "internal", "laboratory", "simulation",
                                   "variable", "common_tag", "vocabulary_server"]:
                logger.error("'Origin' must be specified among 'attrs', 'common', 'config', 'dict', 'init', 'internal',"
                             " 'common_tag', 'laboratory', 'simulation', 'vocabulary_server' and 'variable' for %s, not %s" %
                             (self.key, self.origin))
                raise ValueError("'Origin' must be specified among 'attrs', 'common', 'config', 'dict', 'init',"
                                 " 'internal', 'common_tag', 'laboratory', 'simulation', 'vocabulary_server' and 'variable' for %s, not %s" %
                                 (self.key, self.origin))
        else:
            logger.error("'Type' must be specified among 'file', 'merge' and 'value' for %s, not %s" % (self.key, self.type))
            raise ValueError("'Type' must be specified among 'file', 'merge' and 'value' for %s, not %s" % (self.key, self.type))

    @classmethod
    def from_dict(cls, key, kwargs, additional_keys=False, project_funcs=None):
        logger = get_logger()
        attrs = copy.deepcopy(kwargs)
        for (keyword, val) in attrs.items():
            if keyword in ["type", "origin"] and not isinstance(val, six.string_types):
                logger.error("Attribute '%s' of ValueSettings %s must be a string" % (keyword, key))
                raise ValueError("Attribute '%s' of ValueSettings %s must be a string" % (keyword, key))
            elif keyword in ["src", "values", "keys", "format"]:
                if isinstance(val, list):
                    for (i, subval) in enumerate(val):
                        attrs[keyword][i] = val_or_func(keyword, subval, project_funcs=project_funcs)
                else:
                    attrs[keyword] = val_or_func(keyword, val, project_funcs=project_funcs)
        attrs["key"] = key
        return cls(project_funcs=project_funcs, **attrs)

    def __call__(self, init_dict=dict(), internal_dict=dict(), common_dict=dict(), additional_dict=dict(),
                 allow_additional_keytypes=False, project_funcs=None, common_tag=dict(), **attrs):
        logger = get_logger()
        found = False
        keys = copy.deepcopy(self.keys)
        if self.type in ["file", ]:
            if self.origin in ["json", ]:
                found, src = return_value(self.src, init_dict=init_dict, internal_dict=internal_dict,
                                          common_dict=common_dict, additional_dict=additional_dict,
                                          allow_additional_keytypes=allow_additional_keytypes,
                                          project_funcs=project_funcs, common_tag=common_tag, **attrs)
                if found:
                    if not isinstance(src, six.string_types):
                        logger.error("src found should be a string for %s, not %s" % (self.key, src))
                        raise TypeError("src found should be a string for %s, not %s" % (self.key, src))
                    else:
                        value = read_json_content(src)
                        found = True
            else:
                logger.error("Unknown origin %s for type %s" % (self.origin, self.type))
                raise ValueError("Unknown origin %s for type %s" % (self.origin, self.type))
        elif self.type in ["merge", ]:
            values = [return_value(val, init_dict=init_dict, internal_dict=internal_dict,
                                   common_dict=common_dict, additional_dict=additional_dict,
                                   allow_additional_keytypes=allow_additional_keytypes,
                                   project_funcs=project_funcs, common_tag=common_tag, **attrs)
                      for val in self.values]
            if all(val[0] for val in values):
                value = list()
                for val in values:
                    value.extend(val[1])
                found = True
            else:
                logger.error("Unable to determine the %s index to be merged in %s" %
                             (str([i for (i, val) in enumerate(values) if not val[0]]), self.key))
                raise ValueError("Unable to determine the %s index to be merged in %s" %
                                 (str([i for (i, val) in enumerate(values) if not val[0]]), self.key))
        elif self.type in ["value", ]:
            if self.origin in ["attrs", ]:
                value = additional_dict
                found = True
            elif self.origin in ["dict", ]:
                value = additional_dict
                found = True
            elif self.origin in ["init", ]:
                value = init_dict
                found = True
            elif self.origin in ["internal", ]:
                value = internal_dict
                found = True
            elif self.origin in ["common", ]:
                value = common_dict
                found = True
            elif self.origin in ["common_tag", ]:
                value = common_tag
                found = True
            elif self.origin in ["variable", ] and allow_additional_keytypes:
                value = additional_dict["variable"]
                if isinstance(value, list):
                    value = value[0]
                value = value.__dict__
                found = True
            elif self.origin in ["vocabulary_server", ] and allow_additional_keytypes:
                from dr2xml.vocabulary import get_version
                value = get_version()
                found = True
            elif self.origin in ["config", "simulation", "laboratory"]:
                if len(keys) == 0:
                    if self.origin in ["config", ]:
                        logger.error("Must define at least one keys for type values and origin config")
                        raise ValueError("Must define at least one keys for type values and origin config")
                    elif self.origin in ["simulation", ]:
                        value = format_dict_for_printing("sset")
                        found = True
                    elif self.origin in ["laboratory", ]:
                        value = format_dict_for_printing("lset")
                        found = True
                    else:
                        logger.error("Unexpected origin %s" % self.origin)
                        raise ValueError("Unexpected origin %s" % self.origin)
                else:
                    key = keys[0]
                    keys = keys[1:]
                    key = val_or_func(self.key, key, project_funcs=project_funcs)
                    found, value = return_value(key, init_dict=init_dict, internal_dict=internal_dict,
                                                common_dict=common_dict, additional_dict=additional_dict,
                                                allow_additional_keytypes=allow_additional_keytypes,
                                                project_funcs=project_funcs, common_tag=common_tag, **attrs)
                    if found:
                        if self.origin in ["config", ]:
                            value = get_config_variable(key)
                            found = True
                        elif self.origin in ["simulation", ]:
                            found = is_key_in_sset(key)
                            if found:
                                value = get_variable_from_sset_without_default(key)
                        elif self.origin in ["laboratory", ]:
                            found = is_key_in_lset(key)
                            if found:
                                value = get_variable_from_lset_without_default(key)
                        else:
                            logger.error("Unexpected origin %s" % self.origin)
                            raise ValueError("Unexpected origin %s" % self.origin)
                    else:
                        logger.error("Could not find the first value to be looked for for %s" % self.key)
                        raise ValueError("Could not find the first value to be looked for for %s" % self.key)

            else:
                logger.error("Unknown origin %s for type %s and allow additional %s" %
                             (self.origin, self.type, allow_additional_keytypes))
                raise ValueError("Unknown origin %s for type %s and allow additional %s" %
                                 (self.origin, self.type, allow_additional_keytypes))
        else:
            logger.error("Unknown type %s" % self.type)
            raise ValueError("Unknown type %s" % self.type)
        while found and len(keys) > 0:
            key = keys[0]
            keys = keys[1:]
            key = val_or_func(self.key, key, project_funcs=project_funcs)
            found, key = return_value(key, init_dict=init_dict, internal_dict=internal_dict,
                                      common_dict=common_dict, additional_dict=additional_dict,
                                      allow_additional_keytypes=allow_additional_keytypes,
                                      project_funcs=project_funcs, common_tag=common_tag, **attrs)
            if found:
                if isinstance(value, (dict, OrderedDict)):
                    if key in value:
                        value = value[key]
                    else:
                        found = False
                elif isinstance(value, (tuple, list, six.string_types)) and isinstance(key, int):
                    if isinstance(key, int) and key < len(value):
                        value = value[key]
                    else:
                        found = False
                elif value is not None and key in value.__dir__():
                    value = value.__getattribute__(key)
                elif value is not None and "__dict__" in value.__dir__():
                    value = value.__dict__.get(key)
                else:
                    found = False
        if found and self.format is not False:
            if isinstance(self.format, FunctionSettings):
                found, value = self.format(value)
            elif isinstance(self.format, six.string_types):
                if not isinstance(value, list):
                    value = [value, ]
                value = self.format.format(*value)
            else:
                logger.error("Unknown format type %s" % self.format)
                raise TypeError("Unknown format type %s" % self.format)
        return found, value

    def dump_doc(self, force_void=False):
        rep = list()
        tmp_rep = ""
        value_origin = self.origin
        value_type = self.type
        if value_type in ["value", ]:
            if value_origin in ["laboratory", "simulation", "dict", "init", "internal", "common", "attrs", "common_tag"]:
                tmp_rep = "%s" % value_origin
                keys_values = self.dump_doc_inner(self.keys, format_struct=False)
                for key_value in keys_values:
                    tmp_rep += "[%s]" % key_value
            elif value_origin in ["data_request", "vocabulary", "config", "variable"]:
                tmp_rep = "%s" % value_origin
                keys_values = self.dump_doc_inner(self.keys, format_struct=False)
                for key_value in keys_values:
                    tmp_rep += ".%s" % key_value
        elif value_type in ["file", ]:
            tmp_rep = "read_%s_file(%s)" % (value_origin, self.dump_doc_inner(self.src, format_struct=False)[0])
            keys_values = self.dump_doc_inner(self.keys, format_struct=False)
            for key_value in keys_values:
                tmp_rep += "[%s]" % key_value
        elif value_type in ["merge", ]:
            tmp_rep = "merge_lists(%s)" % ", ".join(self.dump_doc_inner(self.keys, format_struct=False))
        if self.format is not False:
            if isinstance(self.format, FunctionSettings):
                tmp_rep += " formatted with %s" % self.dump_doc_inner(self.format, force_void=force_void, remove_new_lines=True)[0]
            else:
                tmp_rep = self.dump_doc_inner(self.format, force_void=force_void, remove_new_lines=True)[0] + \
                          ".format(%s)" % tmp_rep
        if len(tmp_rep) == 0:
            print(self)
            rep.extend(super().dump_doc(force_void=force_void))
        else:
            rep.append(tmp_rep)
        return rep


class ParameterSettings(Settings):

    def init_dict_default(self):
        return dict(key=None, help="TODO", fatal=False, corrections=False, values=list(), target_type=False,
                    authorized_values=True, authorized_types=True, authorized_patterns=True,
                    forbidden_types=True, forbidden_patterns=True, forbidden_values=True,
                    output_key=False, num_type="string", conditions=True)

    @classmethod
    def from_dict(cls, key, kwargs, additional_keys=False, project_funcs=None):
        logger = get_logger()
        attrs = copy.deepcopy(kwargs)
        if not additional_keys:
            for elt in ["output_key", "num_type", "conditions"]:
                if elt in attrs:
                    del attrs[elt]
        for (keyword, val) in attrs.items():
            if keyword in ["help", ] and not isinstance(val, six.string_types):
                logger.error("Attribute '%s' of ParameterSettings %s must be a string" % (keyword, key))
                raise ValueError("Attribute '%s' of ParameterSettings %s must be a string" % (keyword, key))
            elif keyword in ["fatal", ] and not isinstance(val, bool):
                logger.error("Attribute '%s' of ParameterSettings %s must be a boolean" % (keyword, key))
                raise ValueError("Attribute '%s' of ParameterSettings %s must be a boolean" % (keyword, key))
            elif keyword in ["num_type", ] and val is not False and not isinstance(val, six.string_types):
                logger.error("Attribute '%s' of ParameterSettings %s must be a string or None or False" % (keyword, key))
                raise ValueError("Attribute '%s' of ParameterSettings %s must be a string or None or False" % (keyword, key))
            elif keyword in ["target_type", ] and val is not False and val is not None and not isinstance(val, six.string_types):
                logger.error("Attribute '%s' of ParameterSettings %s must be a string or None or False" % (keyword, key))
                raise ValueError("Attribute '%s' of ParameterSettings %s must be a string or None or False" % (keyword, key))
            elif keyword in ["corrections", ] and val is not False and not isinstance(val, dict):
                logger.error("Attribute '%s' of ParameterSettings %s must be a dict or False" % (keyword, key))
                raise ValueError("Attribute '%s' of ParameterSettings %s must be a dict or False" % (keyword, key))
            elif keyword in ["authorized_types", "forbidden_types", "authorized_patterns", "forbidden_patterns"] \
                    and val is not True and not isinstance(val, list) \
                    and not all([isinstance(elt, six.string_types) for elt in val]):
                logger.error("Attribute '%s' of ParameterSettings %s must be a list of str or False" % (keyword, key))
                raise ValueError("Attribute '%s' of ParameterSettings %s must be a list of str or False" % (keyword, key))
            elif keyword in ["conditions", ] and val is not True:
                if isinstance(val, list):
                    attrs[keyword] = copy.deepcopy([ConditionSettings.from_dict(keyword, elt, project_funcs=project_funcs) for elt in val])
                else:
                    logger.error("Attribute '%s' of ParameterSettings %s must be a list or True" % (keyword, key))
                    raise ValueError("Attribute '%s' of ParameterSettings %s must be a list or True" % (keyword, key))
            elif keyword in ["authorized_values", "forbidden_values"] and val is not True:
                if isinstance(val, list):
                    attrs[keyword] = copy.deepcopy([val_or_func(keyword, elt, project_funcs=project_funcs) for elt in val])
                else:
                    logger.error("Attribute '%s' of ParameterSettings %s must be a list or True" % (keyword, key))
                    raise ValueError("Attribute '%s' of ParameterSettings %s must be a list or True" % (keyword, key))
            elif keyword in ["values", ]:
                if isinstance(val, list):
                    attrs[keyword] = copy.deepcopy([val_or_func(keyword, elt, project_funcs=project_funcs) for elt in val])
                else:
                    logger.error("Attribute '%s' of ParameterSettings %s must be a list" % (keyword, key))
                    raise ValueError("Attribute '%s' of ParameterSettings %s must be a list" % (keyword, key))
        attrs["key"] = key
        return cls(project_funcs=project_funcs, **attrs)

    def dump_doc(self, force_void=False):
        rep = list()
        rep.append("   %s" % self.key)
        fmt = "      %s"
        rep.append(fmt % "")
        rep.append(fmt % self.help)
        rep.append(fmt % "")
        output_keys = ["fatal", "values", "corrections", "target_type", "authorized_values", "authorized_patterns",
                       "authorized_types", "forbidden_values", "forbidden_patterns", "forbidden_types", "conditions",
                       "num_type"]
        default_dict = self.init_dict_default()
        if self.output_key != self.key:
            output_keys.insert(0, "output_key")
        for key in output_keys:
            value = self.__getattribute__(key)
            if value not in [default_dict[key], ] or key in ["num_type", ]:
                value = self.dump_doc_inner(value, force_void=force_void or key in ["values", ],
                                            format_struct=key not in ["conditions", ],
                                            force_format_struct=key in ["values", ])
                add = False
                key = key.replace("_", " ")
                if len(value) > 1 or key in ["values", ]:
                    rep.append(fmt % ("%s:" % key))
                    rep.extend(fmt % elt for elt in value)
                    add = True
                elif len(value) == 1:
                    value = "%s" % value[0]
                    value = value.strip()
                    if len(value) > 0:
                        rep.append(fmt % ("%s: %s" % (key, value)))
                        add = True
                if add:
                    rep.append(fmt % "")
        return rep

    def __init__(self, *args, project_funcs=None, **kwargs):
        super(ParameterSettings, self).__init__(*args, **kwargs)
        if self.key is None:
            raise ValueError("Attribute 'key' must not be None")
        if self.output_key is None:
            self.output_key = self.key
        if isinstance(self.authorized_types, list) and len(self.authorized_types) == 1:
            self.authorized_types = self.authorized_types[0]
        if isinstance(self.forbidden_types, list) and len(self.forbidden_types) == 1:
            self.forbidden_types = self.forbidden_types[0]
        if self.target_type and not self.target_type in ["list", "set", "str", "dict", None]:
            raise ValueError("Target type must have a value among 'str', 'set', 'list', 'dict', None.")

    def update(self, other):
        super(ParameterSettings, self).update(other)
        for elt in other.updated:
            if elt in ["corrections", ]:
                self.corrections.update(other.corrections)
            else:
                self.__setattr__(elt, other.__getattribute__(elt))
            self.updated.add(elt)

    def check_value(self, value, init_dict=dict(), internal_dict=dict(), common_dict=dict(), additional_dict=dict(),
                    allow_additional_keytypes=True, project_funcs=None, common_tag=dict()):
        test = True
        relevant = True
        if isinstance(self.conditions, bool):
            test = self.conditions
        else:
            i = 0
            while test and i < len(self.conditions):
                cond = self.conditions[i]
                if isinstance(cond, bool):
                    test = test and cond
                else:
                    relevant, cond = cond.check(init_dict=init_dict, internal_dict=internal_dict, common_dict=common_dict,
                                                additional_dict=additional_dict, project_funcs=project_funcs,
                                                allow_additional_keytypes=allow_additional_keytypes,
                                                common_tag=common_tag)
                    test = relevant and cond
                if test:
                    i += 1
        if test:
            if isinstance(self.forbidden_values, bool):
                test = self.forbidden_values
            else:
                forbidden_values = [return_value(val, init_dict=init_dict, internal_dict=internal_dict,
                                                 common_dict=common_dict, additional_dict=additional_dict,
                                                 allow_additional_keytypes=allow_additional_keytypes,
                                                 project_funcs=project_funcs, common_tag=common_tag)
                               for val in self.forbidden_values]
                relevant = all([elt[0] for elt in forbidden_values])
                forbidden_values = [elt[1] for elt in forbidden_values]
                test = relevant and value not in forbidden_values
        if test:
            if isinstance(self.authorized_types, bool):
                test = self.authorized_types
            elif ((isinstance(self.authorized_types, list) and len(self.authorized_types) > 0)
                  or not isinstance(self.authorized_types, list)):
                test = isinstance(value, self.authorized_types)
        if test:
            if isinstance(self.forbidden_types, bool):
                test = self.forbidden_types
            elif ((isinstance(self.forbidden_types, list) and len(self.forbidden_types) > 0)
                  or not isinstance(self.forbidden_types, list)):
                test = not isinstance(value, self.forbidden_types)
        if test:
            if isinstance(self.authorized_values, ValueSettings):
                relevant, authorized_values = return_value(self.authorized_values, init_dict=init_dict,
                                                           internal_dict=internal_dict, common_dict=common_dict,
                                                           additional_dict=additional_dict,
                                                           allow_additional_keytypes=allow_additional_keytypes,
                                                           project_funcs=project_funcs, common_tag=common_tag)
            elif isinstance(self.authorized_values, list) and len(self.authorized_values) > 0:
                authorized_values = [return_value(val, init_dict=init_dict, internal_dict=internal_dict,
                                                  common_dict=common_dict, additional_dict=additional_dict,
                                                  allow_additional_keytypes=allow_additional_keytypes,
                                                  project_funcs=project_funcs, common_tag=common_tag)
                                     for val in self.authorized_values]
                relevant = all([elt[0] for elt in authorized_values])
                authorized_values = [elt[1] for elt in authorized_values]
            else:
                authorized_values = None
            if authorized_values is not None:
                test = relevant and value in authorized_values
        if test:
            if isinstance(self.forbidden_patterns, bool):
                test = self.forbidden_patterns
            else:
                test = not (any([re.compile(pattern).match(str(value)) for pattern in self.forbidden_patterns]))
        if test:
            if isinstance(self.authorized_patterns, bool):
                test = self.authorized_patterns
            else:
                test = any([re.compile(pattern).match(str(value)) for pattern in self.authorized_patterns])
        return relevant, test

    def correct_value(self, value, init_dict=dict(), internal_values=dict(), common_values=dict(),
                      additional_dict=dict(), allow_additional_keytypes=True, project_funcs=None, common_tag=dict()):
        test = True
        if isinstance(value, six.string_types):
            value = value.strip()
        if isinstance(value, (int, float, six.string_types)) and self.corrections is not False and value in self.corrections:
            correction = self.corrections[value]
            if isinstance(correction, list):
                conditions, correction = correction
                conditions = [condition.check(init_dict=init_dict, internal_dict=internal_values,
                                              common_dict=common_values, additional_dict=additional_dict,
                                              allow_additional_keytypes=allow_additional_keytypes,
                                              project_funcs=project_funcs, common_tag=common_tag)
                              for condition in conditions]
                test = all(elt[0] for elt in conditions)
                conditions = all(elt[1] for elt in conditions)
                test = test and conditions
            if test:
                test, value = return_value(correction, init_dict=init_dict, internal_dict=internal_values,
                                           common_dict=common_values, additional_dict=additional_dict,
                                           allow_additional_keytypes=allow_additional_keytypes,
                                           project_funcs=project_funcs, common_tag=common_tag)
        return test, value

    def find_value(self, is_value=False, value=None, init_dict=dict(), internal_dict=dict(), common_dict=dict(),
                   additional_dict=dict(), allow_additional_keytypes=True, raise_on_error=True, project_funcs=None,
                   common_tag=dict()):
        logger = get_logger()
        test = False
        if is_value:
            test, value = self.correct_value(value, init_dict=init_dict, internal_values=internal_dict,
                                             common_values=common_dict, additional_dict=additional_dict,
                                             allow_additional_keytypes=allow_additional_keytypes,
                                             project_funcs=project_funcs, common_tag=common_tag)
            relevant, test = self.check_value(value, init_dict=init_dict, internal_dict=internal_dict,
                                              common_dict=common_dict, additional_dict=additional_dict,
                                              allow_additional_keytypes=allow_additional_keytypes,
                                              project_funcs=project_funcs, common_tag=common_tag)
            test = test and relevant
        i = 0
        while not test and i < len(self.values):
            default = self.values[i]
            test, value = return_value(default, init_dict=init_dict, internal_dict=internal_dict,
                                       common_dict=common_dict, additional_dict=additional_dict,
                                       allow_additional_keytypes=allow_additional_keytypes,
                                       project_funcs=project_funcs, common_tag=common_tag)
            if test:
                test, value = self.correct_value(value, init_dict=init_dict, internal_values=internal_dict,
                                                 common_values=common_dict, additional_dict=dict(),
                                                 allow_additional_keytypes=allow_additional_keytypes,
                                                 project_funcs=project_funcs, common_tag=common_tag)
            if test:
                relevant, test = self.check_value(value, init_dict=init_dict, internal_dict=internal_dict,
                                                  common_dict=common_dict, additional_dict=additional_dict,
                                                  allow_additional_keytypes=allow_additional_keytypes,
                                                  project_funcs=project_funcs, common_tag=common_tag)
                test = test and relevant
            if not test:
                i += 1
        if test:
            value = self.correct_target_type(value)
            logger.debug("For parameter %s, found value %s" % (self.key, "''" if isinstance(value, str) and len(value) == 0 else value))
        elif not test and self.fatal and raise_on_error:
            logger.debug("Could not find a proper value for %s" % self.key)
            raise ValueError("Could not find a proper value for %s" % self.key)
        else:
            logger.debug("Could not find a proper value for %s" % self.key)
        return test, value

    def correct_target_type(self, value):
        target_type = self.target_type
        if target_type in ["list", ]:
            if isinstance(value, set):
                value = list(value)
            elif isinstance(value, six.string_types):
                value = [value, ]
            elif not isinstance(value, list):
                raise ValueError(f"Unable to transform {type(value)} into {target_type}.")
        elif target_type in ["set", ]:
            if isinstance(value, list):
                value = set(value)
            elif isinstance(value, six.string_types):
                value = set([value, ])
            elif not isinstance(value, set):
                raise ValueError(f"Unable to transform {type(value)} into {target_type}.")
        elif target_type in ["str", ]:
            if isinstance(value, (list, set)) and len(value) == 1:
                value = self.correct_target_type(value[0])
            elif not isinstance(value, six.string_types):
                value = str(value)
        elif target_type in ["dict", ]:
            if isinstance(value, dict):
                pass
            elif len(value) == 0:
                value = dict()
            else:
                raise ValueError(f"Unable to transform {type(value)} into {target_type}.")
        return value


class TagSettings(Settings):

    def init_dict_default(self):
        return dict(attrs_list=list(), attrs_constraints=dict(), vars_list=list(), vars_constraints=dict(),
                    comments_list=list(), comments_constraints=dict(), help="TODO", key=None,
                    common_list=list(), common_constraints=dict())

    @classmethod
    def from_dict(cls, key, kwargs, additional_keys=False, project_funcs=None):
        logger = get_logger()
        attrs = copy.deepcopy(kwargs)
        for (keyword, val) in attrs.items():
            if keyword in ["help", ] and not isinstance(val, six.string_types):
                logger.error("Attribute '%s' of TagSettings %s must be a string" % (keyword, key))
                raise ValueError("Attribute '%s' of TagSettings %s must be a string" % (keyword, key))
            elif keyword.endswith("_list") and not isinstance(val, list) \
                    and not all([isinstance(elt, six.string_types) for elt in val]):
                logger.error("Attribute '%s' of TagSettings %s must be a list of str" % (keyword, key))
                raise ValueError("Attribute '%s' of TagSettings %s must be a list of str" % (keyword, key))
            elif keyword.endswith("constraints"):
                if isinstance(val, dict):
                    for (subkey, subval) in val.items():
                        attrs[keyword][subkey] = copy.deepcopy(ParameterSettings.from_dict(subkey, subval,
                                                                                           additional_keys=True,
                                                                                           project_funcs=project_funcs))
                else:
                    logger.error("Attribute '%s' of TagSettings %s must be a dict" % (keyword, key))
                    raise ValueError("Attribute '%s' of TagSettings %s must be a dict" % (keyword, key))
        attrs["key"] = key
        return cls(**attrs)

    def dump_doc(self, force_void=False):
        rep = list()
        rep.append("   %s" % self.key)
        fmt = "      %s"
        rep.append(fmt % "")
        rep.append(fmt % self.help)
        if len(self.common_list) > 0:
            rep.append(fmt % "")
            rep.append(fmt % "Common:")
            for common in self.common_list:
                rep.extend([fmt % elt for elt in self.common_constraints[common].dump_doc(force_void=force_void)])
        if len(self.comments_list) > 0:
            rep.append(fmt % "")
            rep.append(fmt % "Comments:")
            for comment in self.comments_list:
                rep.extend([fmt % elt for elt in self.comments_constraints[comment].dump_doc(force_void=force_void)])
        if len(self.attrs_list) > 0:
            rep.append(fmt % "")
            rep.append(fmt % "Attributes:")
            for attr in self.attrs_list:
                rep.extend([fmt % elt for elt in self.attrs_constraints[attr].dump_doc(force_void=force_void)])
        if len(self.vars_list) > 0:
            rep.append(fmt % "")
            rep.append(fmt % "Variables")
            for var in self.vars_list:
                rep.extend([fmt % elt for elt in self.vars_constraints[var].dump_doc(force_void=force_void)])
        return rep

    def update(self, other):
        super(TagSettings, self).update(other)
        for elt in other.updated:
            if elt in ["attrs_constraints", "vars_constraints", "comments_constraints", "common_constraints"]:
                current_val = self.__getattribute__(elt)
                new_val = other.__getattribute__(elt)
                for key in new_val:
                    if key in current_val:
                        current_val[key].update(new_val[key])
                    else:
                        current_val[key] = new_val[key]
                self.__setattr__(elt, current_val)
            else:
                self.__setattr__(elt, other.__getattribute__(elt))
            self.updated.add(elt)

    def complete_and_clean(self):
        for common in [common for common in self.common_list if common not in self.common_constraints]:
            self.common_constraints[common] = ParameterSettings(key=common)
        for common in [common for common in self.common_constraints if common not in self.common_list]:
            del self.common_constraints[common]
        for attr in [attr for attr in self.attrs_list if attr not in self.attrs_constraints]:
            self.attrs_constraints[attr] = ParameterSettings(key=attr)
        for attr in [attr for attr in self.attrs_constraints if attr not in self.attrs_list]:
            del self.attrs_constraints[attr]
        for comment in [comment for comment in self.comments_list if comment not in self.comments_constraints]:
            self.comments_constraints[comment] = ParameterSettings(key=comment)
        for comment in [comment for comment in self.comments_constraints if comment not in self.comments_list]:
            del self.comments_constraints[comment]
        for var in [var for var in self.vars_list if var not in self.vars_constraints]:
            self.vars_constraints[var] = ParameterSettings(key=var)
        for var in [var for var in self.vars_constraints if var not in self.vars_list]:
            del self.vars_constraints[var]


class FunctionSettings(Settings):

    def init_dict_default(self):
        return dict(type=False, origin=False, keys=[], options=dict(), template=False, format=False,
                    functions_file=None, func=None, key=None)

    def __init__(self, *args, project_funcs=None, **kwargs):
        logger = get_logger()
        super(FunctionSettings, self).__init__(*args, **kwargs)
        if "keys" in self.updated and not isinstance(self.keys, list):
            self.keys = [self.keys, ]
        if not isinstance(self.keys, list) or len(self.keys) == 0:
            logger.error("Keys must be specified for %s" % self.key)
            raise ValueError("Keys must be specified for %s" % self.key)
        elif self.origin in ["self"]:
            if self.keys == ["format", ] and self.template is False:
                logger.error("To use 'format' function in %s, 'template' must be a specified." % self.key)
                raise ValueError("To use 'format' function in %s, 'template' must be a specified." % self.key)
            elif self.keys in [["format", ], ["lower", ], ["upper", ]]:
                self.func = self.keys[0]
            elif self.keys == ["join", ]:
                if not isinstance(self.template, six.string_types):
                    logger.error("To use 'join' function in %s, 'template' must be a specified to the joining string." % self.key)
                    raise ValueError("To use 'join' function in %s, 'template' must be a specified to the joining string." % self.key)
                else:
                    self.func = "join"
            elif self.keys == ["replace", ]:
                if not isinstance(self.template, list) and not len(self.template) == 2:
                    logger.error("To use 'replace' function in %s, 'template' must be a specified to list of two strings." % self.key)
                    raise ValueError("To use 'replace' function in %s, 'template' must be a specified to list of two strings" % self.key)
                else:
                    self.func = "replace"
            else:
                logger.error("Unknown self functions %s" % self.key)
                raise ValueError("Unknown self functions %s" % self.key)
        elif self.format is not False and not isinstance(self.format, FunctionSettings):
            logger.error("Format must be either False or a function for %s" % self.key)
            raise ValueError("Format must be either False or a function for %s" % self.key)
        elif self.origin in ["functions_file", ]:
            if self.functions_file is None and project_funcs is not None:
                spec = spec_from_file_location("functions_file", project_funcs)
                self.functions_file = module_from_spec(spec)
                spec.loader.exec_module(self.functions_file)
            elif isinstance(self.functions_file, six.string_types):
                spec = spec_from_file_location("functions_file", self.functions_file)
                self.functions_file = module_from_spec(spec)
                spec.loader.exec_module(self.functions_file)
            if self.functions_file is None or self.keys[0] not in self.functions_file.__dir__():
                logger.error("Could not find function %s from file %s" % (self.keys[0], self.functions_file))
                raise ValueError("Could not find function %s from file %s" % (self.keys[0], self.functions_file))
            else:
                self.func = self.functions_file.__getattribute__(self.keys[0])
        elif self.origin in ["data_request", "vocabulary_server"]:
            pass
        else:
            raise ValueError(self.origin)
            # TODO

    def __deepcopy__(self, memo):
        dict_call = dict(
            type=self.type,
            origin=self.origin,
            keys=copy.deepcopy(self.keys),
            options=copy.deepcopy(self.options),
            template=self.template,
            format=self.format,
            key=self.key
        )
        if self.functions_file is None:
            dict_call["project_funcs"] = None
        elif isinstance(self.functions_file, six.string_types):
            dict_call["project_funcs"] = self.functions_file
        elif "__file__" in self.functions_file.__dir__():
            dict_call["project_funcs"] = self.functions_file.__file__
        else:
            dict_call["project_funcs"] = copy.deepcopy(self.functions_file)
        return FunctionSettings(**dict_call)

    @classmethod
    def from_dict(cls, key, kwargs, additional_keys=False, project_funcs=None):
        logger = get_logger()
        attrs = copy.deepcopy(kwargs)
        for (keyword, val) in attrs.items():
            if keyword in ["type",] and val not in ["func", ]:
                logger.error("Attribute '%s' of FunctionSettings %s must be 'func' not %s" % (keyword, key, val))
                raise ValueError("Attribute '%s' of FunctionSettings %s must be 'func' not %s" % (keyword, key, val))
            elif keyword in ["origin",] and val not in ["functions_file", "self", "vocabulary_server", "data_request"]:
                logger.error("Attribute '%s' of FunctionSettings %s must be 'functions_file', 'self', 'vocabulary_server' and"
                             " 'data_request' not %s" % (keyword, key, val))
                raise ValueError("Attribute '%s' of FunctionSettings %s must be 'functions_file', 'self', 'vocabulary_server'"
                                 " and 'data_request' not %s" % (keyword, key, val))
            elif keyword in ["keys", "options", "format", "template"]:
                if isinstance(val, list):
                    for (i, subval) in enumerate(val):
                        attrs[keyword][i] = val_or_func(keyword, subval, project_funcs=project_funcs)
                elif isinstance(val, dict):
                    for (subkey, subval) in val.items():
                        attrs[keyword][subkey] = val_or_func(subkey, subval, project_funcs=project_funcs)
                else:
                    attrs[keyword] = val_or_func(keyword, val, project_funcs=project_funcs)
        attrs["key"] = key
        return cls(project_funcs=project_funcs, **attrs)

    def dump_doc(self, force_void=False):
        rep = list()
        tmp_rep = "function from %s named %s" % (self.origin, self.keys[0]) + "(%s)"
        options = self.dump_doc_inner(self.options, force_void=force_void, format_struct=False)
        tmp_rep = tmp_rep % ", ".join(options)
        rep.append(tmp_rep)
        return rep

    def __call__(self, *args, init_dict=dict(), internal_dict=dict(), common_dict=dict(), additional_dict=dict(),
                 allow_additional_keytypes=False, project_funcs=None, common_tag=dict(), **attrs):
        logger = get_logger()
        test = True
        options = copy.deepcopy(self.options)
        for key in sorted(list(self.options)):
            val = val_or_func(key, options[key], project_funcs=project_funcs)
            key_test, val = return_value(val, common_dict=common_dict, internal_dict=internal_dict,
                                         additional_dict=additional_dict, init_dict=init_dict,
                                         allow_additional_keytypes=allow_additional_keytypes,
                                         project_funcs=project_funcs, common_tag=common_tag, **attrs)
            if key_test:
                options[key] = val
            else:
                del options[key]
        if isinstance(self.func, ValueSettings):
            func_test, func_val = return_value(self.func, common_dict=common_dict, internal_dict=internal_dict,
                                               additional_dict=additional_dict, init_dict=init_dict,
                                               allow_additional_keytypes=allow_additional_keytypes,
                                               project_funcs=project_funcs, common_tag=common_tag, **attrs)
            if func_test:
                self.func = func_val
            else:
                logger.error("Unable to determine function to be used %s" % self.func)
                raise ValueError("Unable to determine function to be used %s" % self.func)
        elif self.func is None and allow_additional_keytypes:
            if self.origin in ["data_request", ]:
                from dr2xml.dr_interface import get_dr_object
                value = get_dr_object("get_data_request")
            elif self.origin in ["vocabulary_server", ]:
                from dr2xml.vocabulary import get_vocabulary
                value = get_vocabulary()
            else:
                value = None
            if value is not None:
                if self.keys[0] not in value.__dir__():
                    logger.error("Could not find function %s from %s" % (self.keys[0], self.origin.replace("_", " ")))
                    raise ValueError("Could not find function %s from %s" % (self.keys[0], self.origin.replace("_", " ")))
                else:
                    self.func = value.__getattribute__(self.keys[0])
        if self.origin in ["self", ] and isinstance(self.func, six.string_types):
            if self.func in ["lower", ]:
                try:
                    value = args[0].lower()
                except BaseException as e:
                    logger.debug("Issue formating string %s with method %s" % (args[0], self.func))
                    logger.debug(str(e))
                    value = None
                    test = False
            elif self.func in ["upper", ]:
                try:
                    value = args[0].upper()
                except BaseException as e:
                    logger.debug("Issue formating string %s with method %s" % (args[0], self.func))
                    logger.debug(str(e))
                    value = None
                    test = False
            elif self.func in ["format", ]:
                try:
                    value = self.template.format(*args, **options)
                except BaseException as e:
                    logger.debug("Issue formating string %s with %s and %s" % (self.template, args, options))
                    logger.debug(str(e))
                    value = None
                    test = False
            elif self.func in ["join", ]:
                try:
                    if not isinstance(args, tuple):
                        args = tuple([args, ])
                    if not isinstance(args[0], list):
                        args = tuple([[args[0], ], ])
                    value = self.template.join(*args)
                except BaseException as e:
                    logger.debug("Issue joining string %s with %s" % (self.template, args))
                    logger.debug(str(e))
                    value = None
                    test = False
            elif self.func in ["replace", ]:
                try:
                    value = args[0].replace(*self.template)
                except BaseException as e:
                    logger.debug("Issue joining string %s with %s" % (self.template, args))
                    logger.debug(str(e))
                    value = None
                    test = False
            else:
                logger.error("Unknown func %s" % self.func)
                raise ValueError("Unknown func %s" % self.func)
        else:
            try:
                value = self.func(*args, **options)
            except BaseException as e:
                logger.debug("Issue calling %s with args %s and options %s" % (str(self.func), str(args), str(options)))
                logger.debug(str(e))
                value = None
                test = False
        return test, value


class ConditionSettings(Settings):

    def init_dict_default(self):
        return dict(value_to_check=False, check_to_perform=False, reference_values=False, values=list(), key=None,
                    not_values=list())

    def __init__(self, *args, project_funcs=None, **kwargs):
        logger = get_logger()
        super(ConditionSettings, self).__init__(*args, **kwargs)
        if not isinstance(self.reference_values, list):
            self.reference_values = [self.reference_values, ]
        self.reference_values = [val_or_func(self.key, elt, project_funcs=project_funcs) for elt in self.reference_values]
        if not isinstance(self.values, list):
            self.values = [self.values, ]
        self.values = [val_or_func(self.key, elt, project_funcs=project_funcs) for elt in self.values]
        if not isinstance(self.not_values, list):
            self.not_values = [self.not_values, ]
        self.not_values = [val_or_func(self.key, elt, project_funcs=project_funcs) for elt in self.not_values]
        if self.value_to_check is False or self.check_to_perform is False or len(self.reference_values) == 0:
            logger.error("For condition %s, 'value_to_check', 'check_to_perform' and 'reference_values' must be "
                         "specified" % self.key)
            raise ValueError("For condition %s, 'value_to_check', 'check_to_perform' and 'reference_values' must be "
                             "specified" % self.key)
        elif self.check_to_perform not in ["eq", "neq", "match", "nmatch"]:
            logger.error("For condition %s, 'check_to_perform' values must be among 'eq', 'neq', 'match', 'nmatch'" % self.key)
            raise ValueError("For condition %s, 'check_to_perform' values must be among 'eq', 'neq', 'match', 'nmatch'" % self.key)

    @classmethod
    def from_dict(cls, key, kwargs, additional_keys=False, project_funcs=None):
        logger = get_logger()
        attrs = copy.deepcopy(kwargs)
        for (keyword, val) in attrs.items():
            if keyword in ["type", ] and val not in ["condition", ]:
                logger.error("Attribute '%s' of ConditionSettings %s must be 'func' not %s" % (keyword, key, val))
                raise ValueError("Attribute '%s' of ConditionSettings %s must be 'func' not %s" % (keyword, key, val))
            elif keyword in ["values", "value_to_check", "reference_values"]:
                if isinstance(val, list):
                    for (i, subval) in enumerate(val):
                        attrs[keyword][i] = val_or_func(keyword, subval, project_funcs=project_funcs)
                else:
                    attrs[keyword] = val_or_func(keyword, val, project_funcs=project_funcs)
        attrs["key"] = key
        return cls(project_funcs=project_funcs, **attrs)

    def dump_doc(self, force_void=False):
        rep = list()
        rep.append("   Condition:")
        rep.append("   ")
        fmt = "      %s"
        output_keys = ["value_to_check", "check_to_perform", "reference_values"]
        if len(self.values) > 0:
            output_keys.append("values")
        for key in output_keys:
            value = self.__getattribute__(key)
            value = self.dump_doc_inner(value, force_void=force_void)
            add = False
            key = key.replace("_", " ")
            if len(value) == 1:
                value = "%s" % value[0]
                value = value.strip()
                if len(value) > 0:
                    rep.append(fmt % ("%s: %s" % (key, value)))
                    add = True
            elif len(value) > 1:
                rep.append(fmt % ("%s:" % key))
                rep.extend("   " + fmt % elt for elt in value)
                add = True
            if add:
                rep.append(fmt % "")
        return rep

    def __call__(self, init_dict=dict(), internal_dict=dict(), common_dict=dict(), additional_dict=dict(),
                 allow_additional_keytypes=False, project_funcs=None, common_tag=dict(), **attrs):
        relevant, test = self.check(common_dict=common_dict, internal_dict=internal_dict, init_dict=init_dict,
                                    additional_dict=additional_dict, allow_additional_keytypes=True,
                                    project_funcs=project_funcs, common_tag=common_tag, **attrs)
        if not relevant:
            return relevant, None
        elif test:
            if len(self.values) == 0:
                return relevant and test, None
            else:
                test = False
                i = 0
                while i < len(self.values) and not test:
                    test, val = return_value(self.values[i], common_dict=common_dict, internal_dict=internal_dict,
                                             additional_dict=additional_dict, init_dict=init_dict,
                                             allow_additional_keytypes=allow_additional_keytypes,
                                             project_funcs=project_funcs, common_tag=common_tag, **attrs)
                    i += 1
                return relevant and test, val
        else:
            if len(self.not_values) == 0:
                return relevant and test, None
            else:
                test = False
                i = 0
                while i < len(self.not_values) and not test:
                    test, val = return_value(self.not_values[i], common_dict=common_dict, internal_dict=internal_dict,
                                             additional_dict=additional_dict, init_dict=init_dict,
                                             allow_additional_keytypes=allow_additional_keytypes,
                                             project_funcs=project_funcs, common_tag=common_tag, **attrs)
                    i += 1
                return relevant and test, val

    def check(self, common_dict=dict(), internal_dict=dict(), additional_dict=dict(), allow_additional_keytypes=True,
              init_dict=dict(), project_funcs=None, common_tag=dict(), **attrs):
        test = False
        relevant, check_value = return_value(self.value_to_check, common_dict=common_dict, internal_dict=internal_dict,
                                             additional_dict=additional_dict, init_dict=init_dict,
                                             allow_additional_keytypes=allow_additional_keytypes,
                                             project_funcs=project_funcs, common_tag=common_tag, **attrs)
        if relevant:
            if isinstance(check_value, list) and len(check_value) == 1:
                check_value = check_value[0]
            reference_values = [return_value(reference_value, common_dict=common_dict, internal_dict=internal_dict,
                                             additional_dict=additional_dict, init_dict=init_dict,
                                             allow_additional_keytypes=allow_additional_keytypes,
                                             project_funcs=project_funcs, common_tag=common_tag, **attrs)
                                for reference_value in self.reference_values]
            relevant = all([elt[0] for elt in reference_values])
            if relevant:
                reference_values = [elt[1] for elt in reference_values]
                if self.check_to_perform in ["eq", ]:
                    test = check_value in reference_values
                elif self.check_to_perform in ["neq", ]:
                    test = check_value not in reference_values
                elif self.check_to_perform in ["match", ]:
                    test = all([re.compile(val).match(str(check_value)) is not None for val in reference_values])
                elif self.check_to_perform in ["nmatch", ]:
                    test = not(any([re.compile(val).match(str(check_value)) is not None for val in reference_values]))
                else:
                    ValueError("Conditions can have 'eq', 'neq', 'match' or 'nmatch' as operator, found: %s" % self.check_to_perform)
        elif len(self.reference_values) == 0 and self.check_to_perform in ["eq", ]:
            test = True
            relevant = True
        return relevant, test
