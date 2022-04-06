#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface if no data request should be used.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from .definition import Scope, ListWithItems


print_DR_errors = False
print_DR_stdname_errors = False
scope = Scope()


def get_DR_version():
    """
    Get the version of the DR
    """
    return "No data request"


def get_scope(tierMax=None):
    return scope


def set_scope(sc):
    if sc is not None:
        global scope
        scope = sc


def get_list_of_elements_by_id(id):
    """
    Get the list of elements corresponding to the id.
    """
    return ListWithItems()


def get_element_uid(id=None):
    """
    Get the uid of an element if precised, else the list of all elements.
    """
    if id is None:
        return list()
    else:
        return None


def get_experiment_label(experiment):
    return ""


def get_request_by_id_by_sect(id, request):
    return list()


def get_cmor_var_id_by_label(label):
    return None


def correct_data_request_dim(dim):
    pass


def correct_data_request_variable(variable):
    pass
