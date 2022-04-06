#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Definitions of objects for DR interface
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import namedtuple


class Scope(object):
	def __init__(self, scope=None):
		self.scope = scope
		self.mcfg = self.build_mcfg([None, None, None, None, None, None, None])

	def build_mcfg(self, value):
		mcfg = namedtuple('mcfg', ['nho', 'nlo', 'nha', 'nla', 'nlas', 'nls', 'nh1'])
		return mcfg._make(value)._asdict()

	def get_request_link_by_mip(self, mips_list):
		return list()

	def get_vars_by_request_link(self, request_link, pmax):
		return list()


class ListWithItems(list):

	def __init__(self):
		self.items = self.build_content()

	def build_content(self):
		return self[:]

	def __setitem__(self, key, value):
		super(ListWithItems, self).__setitem__(key, value)
		self.items = self.build_content()

	def __delitem__(self, key):
		super(ListWithItems, self).__delitem__(key)
		self.items = self.build_content()
