#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface to project settings
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import re
from collections import OrderedDict

import six

from dr2xml.config import get_config_variable
from dr2xml.settings_interface.py_settings_interface import format_dict_for_printing, is_key_in_lset, \
    get_variable_from_lset_without_default, is_key_in_sset, get_variable_from_sset_without_default
from dr2xml.utils import Dr2xmlError
from utilities.json_tools import read_json_content
from utilities.logger import get_logger


def return_value(value, common_dict=dict(), internal_dict=dict(), additional_dict=dict(),
                 allow_additional_keytypes=True):
    if isinstance(value, ValueSettings):
        return determine_value(key_type=value.key_type, keys=value.keys, func=value.func, fmt=value.fmt, src=value.src,
                               common_dict=common_dict, internal_dict=internal_dict,
                               additional_dict=additional_dict,
                               allow_additional_keytypes=allow_additional_keytypes)
    else:
        return True, value


def determine_value(key_type=None, keys=list(), func=None, fmt=None, src=None, common_dict=dict(), internal_dict=dict(),
                    additional_dict=dict(), allow_additional_keytypes=True):
    logger = get_logger()
    if key_type in ["combine", "merge"] or (key_type is None and func is not None):
        keys = [return_value(key, common_dict=common_dict, internal_dict=internal_dict,
                             additional_dict=additional_dict, allow_additional_keytypes=allow_additional_keytypes)
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
                                        common_dict=common_dict, allow_additional_keytypes=allow_additional_keytypes)
                else:
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
        elif key_type in ["dict", ]:
            value = additional_dict
            found = True
        elif key_type in ["config", ]:
            if len(keys) == 0:
                raise ValueError("At least a key must be provided if key_type=config")
            else:
                try:
                    found, value = return_value(value=keys[i_keys], common_dict=common_dict,
                                                internal_dict=internal_dict, additional_dict=additional_dict,
                                                allow_additional_keytypes=allow_additional_keytypes)
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
                found, value = return_value(value=keys[i_keys], common_dict=common_dict,
                                            internal_dict=internal_dict, additional_dict=additional_dict,
                                            allow_additional_keytypes=allow_additional_keytypes)
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
                found, value = return_value(value=keys[i_keys], common_dict=common_dict,
                                            internal_dict=internal_dict, additional_dict=additional_dict,
                                            allow_additional_keytypes=allow_additional_keytypes)
                if found:
                    found = is_key_in_sset(value)
                if found:
                    value = get_variable_from_sset_without_default(value)
                    i_keys += 1
        elif key_type in ["json", ]:
            found, src = return_value(value=src, common_dict=common_dict, internal_dict=internal_dict,
                                      additional_dict=additional_dict,
                                      allow_additional_keytypes=allow_additional_keytypes)
            if found:
                if not isinstance(src, six.string_types):
                    raise TypeError("src must be a string or a ValueSettings")
                else:
                    value = read_json_content(src)
            else:
                value = None
        elif allow_additional_keytypes:
            if key_type in ["data_request", ] and allow_additional_keytypes:
                from dr2xml.dr_interface import get_dr_object
                value = get_dr_object("get_data_request")
                found = True
            elif key_type in ["variable", ] and "variable" in additional_dict:
                value = additional_dict["variable"]
                if isinstance(value, list):
                    value = value[0]
                value = value.__dict__
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
                                          additional_dict=additional_dict,
                                          allow_additional_keytypes=allow_additional_keytypes)
                if found:
                    if isinstance(value, (dict, OrderedDict)):
                        if key in value:
                            value = value[key]
                            i_keys += 1
                        else:
                            found = False
                    elif isinstance(value, (tuple, list, six.string_types)):
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
                    else:
                        found = False
        if found and func is not None:
            if not isinstance(value, list):
                value = [value, ]
            if isinstance(func, FunctionSettings):
                found, value = func(*value, additional_dict=additional_dict, internal_dict=internal_dict,
                                    common_dict=common_dict, allow_additional_keytypes=allow_additional_keytypes)
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

    def __init__(self, *args, **kwargs):
        self.dict_default = self.init_dict_default()
        self.updated = set()
        for elt in self.dict_default:
            if elt in kwargs:
                self.updated.add(elt)
                val = kwargs[elt]
            else:
                val = self.dict_default[elt]
            self.__setattr__(elt, val)

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

    def dump_doc(self, force_void=False):
        raise NotImplementedError("Dump documentation is not implemented for class %s" % type(self))

    def dump_doc_inner(self, value, force_void=False, format_struct=True, remove_new_lines=False):
        if isinstance(value, Settings):
            rep = value.dump_doc(force_void=force_void)
        elif isinstance(value, (list, set)):
            rep = list()
            if len(value) == 0 and force_void:
                rep.append(list())
            elif len(value) == 1:
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
                rep.append(type(value).__call__())
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
        return dict(key_type=None, keys=list(), fmt=None, src=None, func=None)

    def __init__(self, *args, **kwargs):
        super(ValueSettings, self).__init__(*args, **kwargs)
        if "keys" in self.updated and not isinstance(self.keys, list):
            self.keys = [self.keys, ]

    def dump_doc(self, force_void=False):
        rep = list()
        tmp_rep = ""
        key_type = self.key_type
        if key_type in ["laboratory", "simulation", "dict", "internal", "common", "json"]:
            if key_type in ["json", ]:
                tmp_rep = "read_json_file(%s)"
                tmp_rep = tmp_rep % self.dump_doc_inner(self.src, format_struct=False)[0]
            else:
                tmp_rep = "%s" % key_type
            keys_values = self.dump_doc_inner(self.keys, format_struct=False)
            for key_value in keys_values:
                tmp_rep += "[%s]" % key_value
        elif key_type in ["combine", ]:
            tmp_rep = ", ".join(self.dump_doc_inner(self.keys, format_struct=False))
        elif key_type in ["merge", ]:
            tmp_rep = str(self.dump_doc_inner(self.keys, format_struct=False))
        elif key_type in ["data_request", ]:
            tmp_rep = "%s" % key_type
            keys_values = self.dump_doc_inner(self.keys, format_struct=False)
            for key_value in keys_values:
                if key_value in ["__call__", ]:
                    tmp_rep += "()"
                else:
                    tmp_rep += ".%s" % key_value
        elif key_type in ["config", "variable"]:
            tmp_rep = "%s" % key_type
            if key_type in ["config", ]:
                tmp_rep = "dr2xml." + tmp_rep
            keys_values = self.dump_doc_inner(self.keys, format_struct=False)
            for key_value in keys_values:
                tmp_rep += ".%s" % key_value
        if self.func is not None:
            tmp_rep += self.dump_doc_inner(self.func, format_struct=False)[0]
        if self.fmt is not None:
            tmp_rep = self.dump_doc_inner(self.fmt, force_void=force_void, remove_new_lines=True)[0] + \
                      ".format(%s)" % tmp_rep
        if len(tmp_rep) == 0:
            rep.extend(super().dump_doc(force_void=force_void))
        else:
            rep.append(tmp_rep)
        return rep


class ParameterSettings(Settings):

    def init_dict_default(self):
        return dict(skip_values=list(), forbidden_patterns=list(), conditions=list(), default_values=list(),
                    cases=list(), authorized_values=list(), authorized_types=list(), corrections=dict(),
                    output_key=None, num_type="string", is_default=False, fatal=False, key=None, help="TODO",
                    target_type=None)

    def dump_doc(self, force_void=False):
        rep = list()
        rep.append("   %s" % self.key)
        fmt = "      %s"
        rep.append(fmt % "")
        rep.append(fmt % self.help)
        rep.append(fmt % "")
        output_keys = ["fatal", "default_values", "skip_values", "authorized_values", "authorized_types",
                      "forbidden_patterns", "conditions", "cases", "corrections", "num_type"]
        if self.__getattribute__("output_key") != self.key:
            output_keys.insert(0, "output_key")
        for key in output_keys:
            value = self.__getattribute__(key)
            value = self.dump_doc_inner(value, force_void=force_void or key in ["default_values", ],
                                        format_struct=key not in ["cases", "conditions"])
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
                rep.extend(fmt % elt for elt in value)
                add = True
            if add:
                rep.append(fmt % "")
        return rep

    def __init__(self, *args, **kwargs):
        super(ParameterSettings, self).__init__(*args, **kwargs)
        if self.key is None:
            raise ValueError("Attribute 'key' must not be None")
        if self.output_key is None:
            self.output_key = self.key
        if not self.is_default and len(self.default_values) > 0:
            self.is_default = True
            self.updated.add("is_default")
        elif self.is_default and len(self.default_values) == 0:
            self.is_default = False
            self.updated.add("is_default")
        if isinstance(self.authorized_types, list) and len(self.authorized_types) == 1:
            self.authorized_types = self.authorized_types[0]
        if not self.target_type in ["list", "set", "str", None]:
            raise ValueError("Target type must have a value among 'str', 'set', 'list', None.")

    def update(self, other):
        super(ParameterSettings, self).update(other)
        for elt in other.updated:
            if elt in ["corrections", ]:
                self.corrections.update(other.corrections)
            else:
                self.__setattr__(elt, other.__getattribute__(elt))
            self.updated.add(elt)

    def check_value(self, value, internal_dict=dict(), common_dict=dict(), additional_dict=dict(),
                    allow_additional_keytypes=True):
        test = True
        relevant = True
        i = 0
        while test and i < len(self.conditions):
            cond = self.conditions[i]
            if isinstance(cond, bool):
                test = test and cond
            else:
                relevant, cond = cond.check(internal_dict=internal_dict, common_dict=common_dict,
                                            additional_dict=additional_dict,
                                            allow_additional_keytypes=allow_additional_keytypes)
                test = relevant and cond
            if test:
                i += 1
        if test:
            skip_values = [return_value(val, internal_dict=internal_dict, common_dict=common_dict,
                                        additional_dict=additional_dict,
                                        allow_additional_keytypes=allow_additional_keytypes)
                           for val in self.skip_values]
            relevant = all([elt[0] for elt in skip_values])
            skip_values = [elt[1] for elt in skip_values]
            test = relevant and value not in skip_values
        if test and ((isinstance(self.authorized_types, list) and len(self.authorized_types) > 0)
                     or not isinstance(self.authorized_types, list)):
            test = isinstance(value, self.authorized_types)
        if test:
            if isinstance(self.authorized_values, ValueSettings):
                relevant, authorized_values = return_value(self.authorized_values, internal_dict=internal_dict,
                                                           common_dict=common_dict, additional_dict=additional_dict,
                                                           allow_additional_keytypes=allow_additional_keytypes)
            elif isinstance(self.authorized_values, list) and len(self.authorized_values) > 0:
                authorized_values = [return_value(val, internal_dict=internal_dict, common_dict=common_dict,
                                                  additional_dict=additional_dict,
                                                  allow_additional_keytypes=allow_additional_keytypes)
                                     for val in self.authorized_values]
                relevant = all([elt[0] for elt in authorized_values])
                authorized_values = [elt[1] for elt in authorized_values]
            else:
                authorized_values = None
            if authorized_values is not None:
                test = relevant and value in authorized_values
        if test:
            test = not (any([re.compile(pattern).match(str(value)) for pattern in self.forbidden_patterns]))
        return relevant, test

    def correct_value(self, value, internal_values=dict(), common_values=dict(), additional_dict=dict(),
                      allow_additional_keytypes=True):
        test = True
        if isinstance(value, six.string_types):
            value = value.strip()
        if isinstance(value, (int, float, six.string_types)) and value in self.corrections:
            correction = self.corrections[value]
            if isinstance(correction, list):
                conditions, correction = correction
                conditions = [condition.check(internal_dict=internal_values, common_dict=common_values,
                                              additional_dict=additional_dict,
                                              allow_additional_keytypes=allow_additional_keytypes)
                              for condition in conditions]
                test = all(elt[0] for elt in conditions)
                conditions = all(elt[1] for elt in conditions)
                test = test and conditions
            if test:
                test, value = return_value(correction, internal_dict=internal_values, common_dict=common_values,
                                           additional_dict=additional_dict,
                                           allow_additional_keytypes=allow_additional_keytypes)
        return test, value

    def find_value(self, is_value=False, value=None, internal_dict=dict(), common_dict=dict(), additional_dict=dict(),
                   allow_additional_keytypes=True, raise_on_error=True):
        test = False
        if is_value:
            test, value = self.correct_value(value, internal_values=internal_dict, common_values=common_dict,
                                             additional_dict=dict(), allow_additional_keytypes=True)
            relevant, test = self.check_value(value, internal_dict=internal_dict, common_dict=common_dict,
                                              additional_dict=additional_dict,
                                              allow_additional_keytypes=allow_additional_keytypes)
            test = test and relevant
        i = 0
        while not test and i < len(self.cases):
            test, value = self.cases[i].check(internal_dict=internal_dict, common_dict=common_dict,
                                              additional_dict=additional_dict,
                                              allow_additional_keytypes=allow_additional_keytypes)
            if test:
                test, value = self.correct_value(value, internal_values=internal_dict, common_values=common_dict,
                                                 additional_dict=dict(),
                                                 allow_additional_keytypes=allow_additional_keytypes)
            if test:
                relevant, test = self.check_value(value, internal_dict=internal_dict, common_dict=common_dict,
                                                  additional_dict=additional_dict,
                                                  allow_additional_keytypes=allow_additional_keytypes)
                test = test and relevant
            if not test:
                i += 1
        i = 0
        while not test and i < len(self.default_values):
            default = self.default_values[i]
            test, value = return_value(default, internal_dict=internal_dict, common_dict=common_dict,
                                       additional_dict=additional_dict,
                                       allow_additional_keytypes=allow_additional_keytypes)
            if test:
                test, value = self.correct_value(value, internal_values=internal_dict, common_values=common_dict,
                                                 additional_dict=dict(), allow_additional_keytypes=True)
            if test:
                relevant, test = self.check_value(value, internal_dict=internal_dict, common_dict=common_dict,
                                                  additional_dict=additional_dict,
                                                  allow_additional_keytypes=allow_additional_keytypes)
                test = test and relevant
            if not test:
                i += 1
        if test:
            value = self.correct_target_type(value)
        elif not test and self.fatal and raise_on_error:
            raise ValueError("Could not find a proper value for %s" % self.key)
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
        return value


class TagSettings(Settings):

    def init_dict_default(self):
        return dict(attrs_list=list(), attrs_constraints=dict(), vars_list=list(), vars_constraints=dict(),
                    comments_list=list(), comments_constraints=dict(), help="TODO", key="TODO")

    def dump_doc(self, force_void=False):
        rep = list()
        rep.append("   %s" % self.key)
        fmt = "      %s"
        rep.append(fmt % "")
        rep.append(fmt % self.help)
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
            if elt in ["attrs_constraints", "vars_constraints", "comments_constraints"]:
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

    def __init__(self, func, options=dict()):
        self.func = func
        self.options = options

    def dump_doc(self, force_void=False):
        rep = list()
        tmp_rep = self.func.__name__ + "(%s)"
        options = self.dump_doc_inner(self.options, force_void=force_void, format_struct=False)
        tmp_rep = tmp_rep % ", ".join(options)
        rep.append(tmp_rep)
        return rep

    def __call__(self, *args, additional_dict=dict(), internal_dict=dict(), common_dict=dict(),
                 allow_additional_keytypes=True):
        logger = get_logger()
        test = True
        for key in sorted(list(self.options)):
            key_test, val = return_value(self.options[key], common_dict=common_dict, internal_dict=internal_dict,
                                         additional_dict=additional_dict,
                                         allow_additional_keytypes=allow_additional_keytypes)
            if key_test:
                self.options[key] = val
            else:
                del self.options[key]
        try:
            value = self.func(*args, **self.options)
        except BaseException as e:
            logger.debug("Issue calling %s with arguments %s and options %s" % (str(self.func), str(args), str(self.options)))
            logger.debug(str(e))
            value = None
            test = False
        return test, value


class ConditionSettings(Settings):

    def __init__(self, check_value, check_to_do, reference_values):
        self.check_value = check_value
        self.check_to_do = check_to_do
        if not isinstance(reference_values, list):
            reference_values = [reference_values, ]
        self.reference_values = reference_values

    def dump_doc(self, force_void=False):
        rep = list()
        rep.append("   Condition:")
        rep.append("   ")
        fmt = "      %s"
        output_keys = ["check_value", "check_to_do", "reference_values"]
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

    def check(self, common_dict=dict(), internal_dict=dict(), additional_dict=dict(), allow_additional_keytypes=True):
        test = False
        relevant, check_value = return_value(self.check_value, common_dict=common_dict, internal_dict=internal_dict,
                                             additional_dict=additional_dict,
                                             allow_additional_keytypes=allow_additional_keytypes)
        if relevant:
            if isinstance(check_value, list) and len(check_value) == 1:
                check_value = check_value[0]
            reference_values = [return_value(reference_value, common_dict=common_dict, internal_dict=internal_dict,
                                             additional_dict=additional_dict,
                                             allow_additional_keytypes=allow_additional_keytypes)
                                for reference_value in self.reference_values]
            relevant = all([elt[0] for elt in reference_values])
            if relevant:
                reference_values = [elt[1] for elt in reference_values]
                if self.check_to_do in ["eq", ]:
                    test = check_value in reference_values
                elif self.check_to_do in ["neq", ]:
                    test = check_value not in reference_values
                elif self.check_to_do in ["match", ]:
                    test = all([re.compile(val).match(str(check_value)) is not None for val in reference_values])
                elif self.check_to_do in ["nmatch", ]:
                    test = not(any([re.compile(val).match(str(check_value)) is not None for val in reference_values]))
                else:
                    ValueError("Conditions can have 'eq' or 'neq' as operator, found: %s" % self.check_to_do)
        elif len(self.reference_values) == 0 and self.check_to_do in ["eq", ]:
            test = True
            relevant = True
        return relevant, test


class CaseSettings(Settings):

    def __init__(self, conditions, value):
        if not isinstance(conditions, list):
            conditions = [conditions, ]
        self.conditions = conditions
        self.value = value

    def dump_doc(self, force_void=False):
        rep = list()
        rep.append("   Case:")
        rep.append("   ")
        fmt = "      %s"
        output_keys = ["conditions", "value"]
        for key in output_keys:
            value = self.__getattribute__(key)
            value = self.dump_doc_inner(value, force_void=force_void, format_struct=key not in ["conditions", ])
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

    def check(self, common_dict=dict(), internal_dict=dict(), additional_dict=dict(), allow_additional_keytypes=True):
        test, value = return_value(self.value, common_dict=common_dict, additional_dict=additional_dict,
                                   internal_dict=internal_dict, allow_additional_keytypes=allow_additional_keytypes)
        if test:
            check_conditions = [elt.check(common_dict=common_dict, additional_dict=additional_dict,
                                          internal_dict=internal_dict,
                                          allow_additional_keytypes=allow_additional_keytypes)
                                if isinstance(elt, ConditionSettings) else (True, elt)
                                for elt in self.conditions]
            test = all([elt[0] for elt in check_conditions])
            if test:
                check_conditions = [elt[1] for elt in check_conditions]
                test = all(check_conditions)
        return test, value

