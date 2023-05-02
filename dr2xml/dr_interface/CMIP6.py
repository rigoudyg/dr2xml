#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between the CMIP6 Data Request and dr2xml.
# See documentation at: https://c6dreq.dkrz.de/DreqPy_Intro.html
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import re

from logger import get_logger
from .definition import Scope as ScopeBasic
from .definition import DataRequest as DataRequestBasic
from ..utils import Dr2xmlError

try:
    import dreq
except ImportError:
    from dreqPy import dreq

try:
    from scope import dreqQuery
except ImportError:
    from dreqPy.scope import dreqQuery


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


class DataRequest(DataRequestBasic):

    def get_version(self):
        return self.data_request.version

    def get_list_by_id(self, collection):
        return self.data_request.coll[collection]

    def get_sectors_list(self):
        """
        Get the sectors list.
        :return:
        """
        rep = super().get_sectors_list()
        rep = [dim.label for dim in rep.items if dim.type in ['character', ] and dim.value in ['', ]]
        # Error in DR 01.00.21
        return sorted(list(set(rep) - {"typewetla"}))

    def get_experiment_label(self, experiment):
        return self.data_request.inx.experiment.label[experiment][0]

    def get_element_uid(self, id=None, error_msg=None, raise_on_error=False, check_print_DR_errors=True,
                        check_print_stdnames_error=False, elt_type=None):
        logger = get_logger()
        if id is None:
            rep = self.data_request.inx.uid
        elif id in self.data_request.inx.uid:
            rep = self.data_request.inx.uid[id]
        else:
            if error_msg is None:
                error_msg = "DR Error: issue with %s" % id
            if raise_on_error:
                raise Dr2xmlError(error_msg)
            elif check_print_DR_errors and self.print_DR_errors:
                logger.error(error_msg)
            elif check_print_stdnames_error and self.print_DR_stdname_errors:
                logger.error(error_msg)
            rep = None
        if rep is not None:
            if elt_type in ["variable", ]:
                pass
            elif elt_type in ["dim", ]:
                correct_data_request_dim(rep)
        return rep

    def get_request_by_id_by_sect(self, id, request):
        return self.data_request.inx.iref_by_sect[id].a[request]

    def get_cmor_var_id_by_label(self, label):
        return self.data_request.inx.CMORvar.label[label]


scope = None
data_request = None


def initialize_data_request():
    global data_request
    if data_request is None:
        data_request = DataRequest(data_request=dreq.loadDreq(), print_DR_errors=True, print_DR_stdname_errors=False)
    return data_request


def get_data_request():
    if data_request is None:
        return initialize_data_request()
    else:
        return data_request


def initialize_scope(tier_max):
    global scope
    dq = get_data_request()
    if scope is None:
        scope = Scope(dreqQuery(dq=dq.data_request, tierMax=tier_max))
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


def normalize_grid(grid):
    """ in DR 1.0.2, values are :
    ['', 'model grid', '100km', '50km or smaller', 'cfsites', '1deg', '2deg', '25km or smaller', 'native']
    """
    if grid in ["native", "model grid", ""]:
        return ""
    return grid.replace(" or smaller", "")


def correct_data_request_dim(dim):
    # because value is unset in DR01.00.18
    if dim.label in ["misrBands", ]:
        dim.dimsize = 16
    if dim.type in ["character", ]:
        dim.name = "sector"
    else:
        dim.name = dim.altLabel
    # The latter is a bug in DR01.00.21 : typewetla has no value there
    if dim.label in ["typewetla", ]:
        dim.value = "wetland"


def correct_data_request_variable(variable):
    logger = get_logger()
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
        if variable.label in ["jpdftaure", ]:
            variable.spatial_shape = "XY-na"
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
        variable.long_name = "empty in DR %s" % data_request.get_version()
    if variable.units is None:
        variable.units = "empty in DR %s" % data_request.get_version()
    if variable.modeling_realm in ["seaIce", ] and re.match(".*areacella.*", str(variable.cell_measures)) \
            and variable.label not in ["siconca", ]:
        variable.comments = ". Due an error in DR01.00.21 and to technical constraints, this variable may have " \
                            "attribute cell_measures set to area: areacella, while it actually is area: areacello"
