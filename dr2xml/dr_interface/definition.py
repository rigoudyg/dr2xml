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


class DataRequest(object):

    def __init__(self, data_request=None, print_DR_errors=False, print_DR_stdname_errors=False):
        self.data_request = data_request
        self.print_DR_errors = print_DR_errors
        self.print_DR_stdname_errors = print_DR_stdname_errors

    def get_version(self):
        """
        Get the version of the DR
        """
        raise NotImplementedError()

    def get_list_by_id(self, collection):
        """
        Get the collection corresponding to the collection id.
        """
        raise NotImplementedError()

    def get_sectors_list(self):
        return self.get_list_by_id("grids")

    def get_experiment_label(self, experiment):
        """
        Get the experiment from its label.
        """
        raise NotImplementedError()

    def get_cmor_var_id_by_label(self, label):
        """
        Get the id of the CMOR var corresponding to label.
        """
        raise NotImplementedError()

    def get_element_uid(self, id=None, error_msg=None, raise_on_error=False, check_print_DR_errors=True,
                    check_print_stdnames_error=False, elt_type=None):
        """
        Get the uid of an element if precised, else the list of all elements.
        """
        raise NotImplementedError()

    def get_request_by_id_by_sect(self, id, request):
        """
        Get the attribute request of the element id.
        """
        raise NotImplementedError()


class ListWithItems(list):

    def __init__(self):
        super().__init__()
        self.items = self.build_content()

    def build_content(self):
        return self[:]

    def __setitem__(self, key, value):
        super(ListWithItems, self).__setitem__(key, value)
        self.items = self.build_content()

    def __delitem__(self, key):
        super(ListWithItems, self).__delitem__(key)
        self.items = self.build_content()
