#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface to project settings
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import six

from dr2xml.config import get_config_variable
from dr2xml.settings_interface.py_settings_interface import format_dict_for_printing, is_key_in_lset, \
	get_variable_from_lset_without_default, is_key_in_sset, get_variable_from_sset_without_default
from dr2xml.utils import Dr2xmlError, read_json_content


class ValueSettings(object):

	def __init__(self, key_type=None, keys=list(), fmt=None, src=None, func=None):
		self.key_type = key_type
		if not isinstance(keys, list):
			keys = [keys, ]
		self.keys = keys
		self.fmt = fmt
		self.src = src
		self.func = func

	def dump(self):
		pass

	def return_value(self, value, common_dict=dict(), internal_dict=dict(), additional_dict=dict(),
	                 allow_additional_keytypes=True):
		if isinstance(value, type(self)):
			return value.determine_value(common_dict=common_dict, internal_dict=internal_dict,
			                             additional_dict=additional_dict,
			                             allow_additional_keytypes=allow_additional_keytypes)
		else:
			return True, value

	def determine_value(self, common_dict=dict(), internal_dict=dict(), additional_dict=dict(),
	                    allow_additional_keytypes=True):
		if self.key_type in ["combine", ] or (self.key_type is None and self.func is not None):
			keys = [self.return_value(key, common_dict=common_dict, internal_dict=internal_dict,
			                          additional_dict=additional_dict,
			                          allow_additional_keytypes=allow_additional_keytypes) for key in self.keys]
			key_found = all([elt[0] for elt in keys])
			if key_found:
				keys = [elt[1] for elt in keys]
				if self.fmt is None:
					raise ValueError("If key_type=combine, fmt must not be None")
				else:
					keys = [key[1] for key in keys]
					found = True
			else:
				found = False
				value = None
			if found:
				if self.key_type in ["combine", ]:
					value = self.fmt.format(keys)
				else:
					if isinstance(self.func, FunctionSettings):
						found, value = self.func.find_value(*keys, additional_dict=additional_dict,
						                                    internal_dict=internal_dict, common_dict=common_dict,
						                                    allow_additional_keytypes=allow_additional_keytypes)
					else:
						try:
							value = self.func.__call__(*keys)
							found = True
						except:
							value = None
							found = False
					if found and self.fmt is not None:
						value = self.fmt.format(value)
		else:
			i_keys = 0
			if self.key_type in ["common", ]:
				value = common_dict
				found = True
			elif self.key_type in ["internal", ]:
				value = internal_dict
				found = True
			elif self.key_type in ["dict", ]:
				value = additional_dict
				found = True
			elif self.key_type in ["config", ]:
				if len(self.keys) == 0:
					raise ValueError("At least a key must be provided if key_type=config")
				else:
					try:
						found, value = self.return_value(value=self.keys[i_keys],
						                                 common_dict=common_dict, internal_dict=internal_dict,
						                                 additional_dict=additional_dict,
						                                 allow_additional_keytypes=allow_additional_keytypes)
						if found:
							value = get_config_variable(value)
							i_keys += 1
					except (Dr2xmlError, ValueError, TypeError):
						found = False
						value = None
			elif self.key_type in ["laboratory", ]:
				if len(self.keys) == 0:
					value = format_dict_for_printing("lset")
					found = True
				else:
					found, value = self.return_value(value=self.keys[i_keys],
					                                 common_dict=common_dict, internal_dict=internal_dict,
					                                 additional_dict=additional_dict,
					                                 allow_additional_keytypes=allow_additional_keytypes)
					if found and is_key_in_lset(value):
						value = get_variable_from_lset_without_default(value)
						i_keys += 1
			elif self.key_type in ["simulation", ]:
				if len(self.keys) == 0:
					value = format_dict_for_printing("sset")
					found = True
				else:
					found, value = self.return_value(value=self.keys[i_keys],
					                                 common_dict=common_dict, internal_dict=internal_dict,
					                                 additional_dict=additional_dict,
					                                 allow_additional_keytypes=allow_additional_keytypes)
					if found and is_key_in_sset(value):
						value = get_variable_from_sset_without_default(value)
						i_keys += 1
			elif self.key_type in ["json", ]:
				found, src = self.return_value(value=self.src,
				                               common_dict=common_dict, internal_dict=internal_dict,
				                               additional_dict=additional_dict,
				                               allow_additional_keytypes=allow_additional_keytypes)
				if found:
					if not isinstance(src, six.string_types):
						raise TypeError("src must be a string or a ValueSettings")
					else:
						value = read_json_content(src)
			elif allow_additional_keytypes:
				if self.key_type in ["DR_version", ] and allow_additional_keytypes:
					from dr2xml.dr_interface import get_DR_version
					value = get_DR_version()
					found = True
				elif self.key_type in ["scope", ] and allow_additional_keytypes:
					from dr2xml.dr_interface import get_scope
					value = get_scope().__dict__
					found = True
				elif self.key_type in ["variable", ] and "variable" in additional_dict:
					value = additional_dict["variable"].__dict__
					found = True
				else:
					value = None
					found = False
			else:
				value = None
				found = False
			if found:
				while found and i_keys < len(self.keys):
					found, key = self.return_value(key, common_dict=common_dict, internal_dict=internal_dict,
					                               additional_dict=additional_dict,
					                               allow_additional_keytypes=allow_additional_keytypes)
					if found:
						if key in value:
							value = value[key]
							i_keys += 1
						else:
							found = False
			if found and self.func is not None:
				if not isinstance(value, list):
					value = [value, ]
				if isinstance(self.func, FunctionSettings):
					found, value = self.func.find_value(*value, additional_dict=additional_dict,
					                                    internal_dict=internal_dict, common_dict=common_dict,
					                                    allow_additional_keytypes=allow_additional_keytypes)
				else:
					try:
						value = self.func.__call__(*value)
						found = True
					except:
						value = None
						found = False
			if found and self.fmt is not None:
				if not isinstance(value, list):
					value = [value, ]
				value = self.fmt.format(*value)
		return found, value


class ParameterSettings(object):

	def __init__(self, key, skip_values=list(), forbidden_patterns=list(), conditions=list(), default_values=list(),
	             cases=list(), authorized_values=list(), authorized_types=list(), corrections=dict(), output_key=None,
	             num_type="string", is_default=False, fatal=False):
		self.key = key
		if output_key is None:
			self.output_key = key
		else:
			self.output_key = output_key
		self.default_values = default_values
		if not is_default and len(default_values) > 0:
			self.is_default = True
		else:
			self.is_default = is_default
		self.skip_values = skip_values
		self.authorized_values = authorized_values
		self.forbidden_patterns = forbidden_patterns
		self.authorized_types = authorized_types
		self.conditions = conditions
		self.cases = cases
		self.corrections = corrections
		self.num_type = num_type
		self.fatal = fatal

	def __str__(self):
		pass

	def check_value(self, value):
		pass

	def find_value(self):
		pass


class TagSettings(object):

	def __init__(self, attrs_list=list(), attrs_constraints=dict(), vars_list=list(), vars_constraints=dict()):
		self.attrs_list = attrs_list
		self.attrs_constraints = attrs_constraints
		self.vars_list = vars_list
		self.vars_constraints = vars_constraints
