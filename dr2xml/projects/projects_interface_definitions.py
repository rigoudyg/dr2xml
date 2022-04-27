#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface to project settings
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import re
from collections import OrderedDict

import six

from dr2xml.config import get_config_variable
from dr2xml.settings_interface.py_settings_interface import format_dict_for_printing, is_key_in_lset, \
    get_variable_from_lset_without_default, is_key_in_sset, get_variable_from_sset_without_default
from dr2xml.utils import Dr2xmlError, read_json_content


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
    if key_type in ["combine", ] or (key_type is None and func is not None):
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
            else:
                if isinstance(func, FunctionSettings):
                    found, value = func(*keys, additional_dict=additional_dict, internal_dict=internal_dict,
                                        common_dict=common_dict, allow_additional_keytypes=allow_additional_keytypes)
                else:
                    try:
                        value = func(*keys)
                        found = True
                    except:
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
            if key_type in ["DR_version", ] and allow_additional_keytypes:
                from dr2xml.dr_interface import get_DR_version
                value = get_DR_version()
                found = True
            elif key_type in ["scope", ] and allow_additional_keytypes:
                from dr2xml.dr_interface import get_scope
                value = get_scope().__dict__
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
                    elif value is not None and key in value.__dict__:
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
                except:
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


class ValueSettings(Settings):

    def init_dict_default(self):
        return dict(key_type=None, keys=list(), fmt=None, src=None, func=None)

    def __init__(self, *args, **kwargs):
        super(ValueSettings, self).__init__(*args, **kwargs)
        if "keys" in self.updated and not isinstance(self.keys, list):
            self.keys = [self.keys, ]


class ParameterSettings(Settings):

    def init_dict_default(self):
        return dict(skip_values=list(), forbidden_patterns=list(), conditions=list(), default_values=list(),
                    cases=list(), authorized_values=list(), authorized_types=list(), corrections=dict(),
                    output_key=None, num_type="string", is_default=False, fatal=False, key=None)

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
            test = not (any([re.compile(pattern).match(value) for pattern in self.forbidden_patterns]))
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
                                                 additional_dict=dict(), allow_additional_keytypes=True)
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
        if not test and self.fatal and raise_on_error:
            raise ValueError("Could not find a proper value for %s" % self.key)
        return test, value


class TagSettings(Settings):

    def init_dict_default(self):
        return dict(attrs_list=list(), attrs_constraints=dict(), vars_list=list(), vars_constraints=dict(),
                    comments_list=list(), comments_constraints=dict())

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

    def __call__(self, *args, additional_dict=dict(), internal_dict=dict(), common_dict=dict(),
                 allow_additional_keytypes=True):
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
            # print(e)
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

    def check(self, common_dict=dict(), internal_dict=dict(), additional_dict=dict(), allow_additional_keytypes=True):
        test = False
        relevant, check_value = return_value(self.check_value, common_dict=common_dict, internal_dict=internal_dict,
                                             additional_dict=additional_dict,
                                             allow_additional_keytypes=allow_additional_keytypes)
        if relevant:
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

