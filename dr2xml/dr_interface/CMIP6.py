#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between the CMIP6 Data Request and dr2xml.
# See documentation at: https://c6dreq.dkrz.de/DreqPy_Intro.html
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import re

from .definition import Scope as ScopeBasic


try:
    import dreq
except ImportError:
    from dreqPy import dreq

try:
    from scope import dreqQuery
except ImportError:
    from dreqPy.scope import dreqQuery


dq = dreq.loadDreq()

print_DR_errors = True
print_DR_stdname_errors = False


class Scope(ScopeBasic):

    def __init__(self, scope=None):
        super(Scope, self).__init__(scope=scope)
        self.mcfg = self.scope.mcfg

    def get_request_link_by_mip(self, mips_list):
        return sorted(list(self.scope.getRequestLinkByMip(set(mips_list))), key=lambda x: x.label)

    def get_vars_by_request_link(self, request_link, pmax):
        if not isinstance(request_link, list):
            request_link = [request_link, ]
        return self.scope.varsByRql(request_link, pmax)


scope = None


def get_DR_version():
    """
    Get the version of the DR
    """
    return dq.version


def initialize_scope(tier_max):
    global scope
    if scope is None:
        scope = Scope(dreqQuery(dq=dq, tierMax=tier_max))
    return scope


def get_scope(tier_max=None):
    if scope is None:
        return initialize_scope(tier_max)
    else:
        return scope


def set_scope(sc):
    if sc is not None:
        global scope
        scope = sc


def get_list_of_elements_by_id(collection):
    """
    Get the collection corresponding to the collection id.
    """
    return dq.coll[collection]


def get_element_uid(id=None):
    """
    Get the uid of an element if precised, else the list of all elements.
    """
    if id is None:
        return dq.inx.uid
    else:
        return dq.inx.uid[id]


def get_experiment_label(experiment):
    """
    Get the experiment from its label.
    """
    return dq.inx.experiment.label[experiment][0]


def get_request_by_id_by_sect(id, request):
    """
    Get the attribute request of the element id.
    """
    return dq.inx.iref_by_sect[id].a[request]


def get_cmor_var_id_by_label(label):
    """
    Get the id of the CMOR var corresponding to label.
    """
    return dq.inx.CMORvar.label[label]


def correct_data_request_dim(dim):
    # because value is unset in DR01.00.18
    if dim.label in ["misrBands", ]:
        dim.dimsize = 16


def correct_data_request_variable(variable):
    if variable.label is not None:
        # DR21 has a bug with tsland : the MIP variable is named "ts"
        if variable.label in ["tsland", ]:
            variable.mipVarLabel = "tsland"
        # Fix for emulating DR01.00.22 from content of DR01.00.21
        if "SoilPools" in variable.label:
            variable.frequency = "mon"
            variable.cell_methods = "area: mean where land time: mean"
        # For PrePARE missing in DR01.00.21!
        if variable.label in ["sitimefrac", ]:
            variable.stdname = "sea_ice_time_fraction"
        # TBD Next sequences are adhoc for errors DR 01.00.21
        if variable.label in ['tauuo', 'tauvo']:
            variable.cell_measures = 'area: areacello'
        elif variable.cell_measures in ['area: areacella', ] and \
                variable.label in ['tos', 't20d', 'thetaot700', 'thetaot2000', 'thetaot300', 'mlotst']:
            variable.cell_measures = 'area: areacello'
    if variable.modeling_realm is not None:
        # Because wrong in DR01.00.20
        if variable.modeling_realm.startswith("zoo"):
            variable.modeling_realm = "ocnBgChem"
        # TBD : this cell_measure choice for seaice variables is specific to Nemo
        if "seaIce" in variable.modeling_realm and variable.cell_measures is not None and \
                "areacella" in variable.cell_measures:
            if variable.label in ['siconca', ]:
                variable.cell_measures = 'area: areacella'
            else:
                variable.cell_measures = 'area: areacello'
    # A number of DR values indicate a choice or a directive for attribute cell_measures (--OPT, --MODEL ...)
    # See interpretation guidelines at https://www.earthsystemcog.org/projects/wip/drq_interp_cell_center
    if variable.cell_measures in ['--MODEL', ]:
        variable.cell_measures = ''
    elif variable.cell_measures in ['--OPT', ]:
        variable.cell_measures = ''
    if variable.long_name is None:
        variable.long_name = "empty in DR %s" % get_DR_version()
    if variable.units is None:
        variable.units = "empty in DR %s" % get_DR_version()
    if variable.modeling_realm in ["seaIce", ] and re.match(".*areacella.*", str(variable.cell_measures)) \
            and variable.label not in ["siconca", ]:
        variable.comments = ". Due an error in DR01.00.21 and to technical constraints, this variable may have " \
                            "attribute cell_measures set to area: areacella, while it actually is area: areacello"
