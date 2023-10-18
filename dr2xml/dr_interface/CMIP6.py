#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between the CMIP6 Data Request and dr2xml.
# See documentation at: https://c6dreq.dkrz.de/DreqPy_Intro.html
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import re
from collections import OrderedDict

import six

from logger import get_logger
from .definition import Scope as ScopeBasic
from .definition import DataRequest as DataRequestBasic
from .definition import SimpleObject
from .definition import SimpleDim as SimpleDimBasic
from .definition import SimpleCMORVar as SimpleCMORVarBasic
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

    def get_list_by_id(self, collection, **kwargs):
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
                        check_print_stdnames_error=False, elt_type=None, **kwargs):
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
                rep = SimpleCMORVar.get_from_dr(rep, id=id, **kwargs)
            elif elt_type in ["dim", ]:
                rep = SimpleDim.get_from_dr(rep, id=id)
        return rep

    def get_request_by_id_by_sect(self, id, request):
        return self.data_request.inx.iref_by_sect[id].a[request]

    def get_cmor_var_id_by_label(self, label):
        return self.data_request.inx.CMORvar.label[label]

    def get_dimensions_dict(self):
        rep = OrderedDict()
        for sshp in self.get_list_by_id('spatialShape').items:
            rep[sshp.dimensions] = sshp.label
        return rep

    def get_grids_dict(self):
        rep = OrderedDict()
        for g in self.get_list_by_id("grids").items:
            rep[g.label] = g.uid
        return rep

    def get_single_levels_list(self):
        rep = list()
        for struct in self.get_list_by_id('structure').items:
            spshp = self.get_element_uid(struct.spid)
            if spshp.label in ["XY-na", ] and 'cids' in struct.__dict__:
                if isinstance(struct.cids[0], six.string_types) and len(struct.cids[0]) > 0:
                    # this line is needed prior to version 01.00.08.
                    c = data_request.get_element_uid(struct.cids[0])
                    # if c.axis == 'Z': # mpmoine_note: non car je veux dans dr_single_levels toutes les dimensions
                    # singletons (ex. 'typenatgr'), par seulement les niveaux
                    rep.append(c.label)
        return rep


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


class SimpleDim(SimpleDimBasic):
    def correct_data_request(self):
        super().correct_data_request()
        # because value is unset in DR01.00.18
        if self.label in ["misrBands", ]:
            self.dimsize = 16
        if self.type in ["character", ]:
            self.name = "sector"
        else:
            self.name = self.altLabel
        # The latter is a bug in DR01.00.21 : typewetla has no value there
        if self.label in ["typewetla", ]:
            self.value = "wetland"
        if self.name in ["sector", ]:
            if self.label in ["oline", "siline"]:
                self.altLabel = "line"
            elif self.label in ["vegtype", ]:
                self.altLabel = "type"
        if self.name in ["alevel", ]:
            self.name = "lev"
        if self.name in ["sza5", ]:
            self.name = "sza"

    @classmethod
    def get_from_dr(cls, input_dim, id=None, **kwargs):
        input_dim_dict = copy.deepcopy(input_dim.__dict__)
        input_dim_dict["stdname"] = input_dim.standardName
        input_dim_dict["long_name"] = input_dim.title
        input_dim_dict["out_name"] = input_dim.altLabel
        stdname = data_request.get_element_uid(input_dim.standardName, check_print_stdnames_error=True,
                                               check_print_DR_errors=False,
                                               error_msg="Issue with standardname for dimid %s" % id)
        if stdname is not None:
            stdname = stdname.uid
        else:
            stdname = ""
        input_dim_dict["stdname"] = stdname
        return cls(**input_dim_dict)


class SimpleCMORVar(SimpleCMORVarBasic):
    def correct_data_request(self):
        logger = get_logger()
        if self.label is not None:
            # DR21 has a bug with tsland : the MIP variable is named "ts"
            if self.label in ["tsland", ]:
                self.mipVarLabel = "tsland"
            # Fix for emulating DR01.00.22 from content of DR01.00.21
            if "SoilPools" in self.label:
                self.frequency = "mon"
                self.cell_methods = "area: mean where land time: mean"
            # For PrePARE missing in DR01.00.21!
            if self.label in ["sitimefrac", ]:
                self.stdname = "sea_ice_time_fraction"
            # TBD Next sequences are adhoc for errors DR 01.00.21
            if self.label in ['tauuo', 'tauvo']:
                self.cell_measures = 'area: areacello'
            elif self.cell_measures in ['area: areacella', ] and \
                    self.label in ['tos', 't20d', 'thetaot700', 'thetaot2000', 'thetaot300', 'mlotst']:
                self.cell_measures = 'area: areacello'
            if self.label in ["jpdftaure", ]:
                self.spatial_shape = "XY-na"
        if self.modeling_realm is not None:
            # Because wrong in DR01.00.20
            if self.modeling_realm.startswith("zoo"):
                self.modeling_realm = "ocnBgChem"
            # TBD : this cell_measure choice for seaice variables is specific to Nemo
            if "seaIce" in self.modeling_realm and self.cell_measures is not None and \
                    "areacella" in self.cell_measures:
                if self.label in ['siconca', ]:
                    self.cell_measures = 'area: areacella'
                else:
                    self.cell_measures = 'area: areacello'
        # A number of DR values indicate a choice or a directive for attribute cell_measures (--OPT, --MODEL ...)
        # See interpretation guidelines at https://www.earthsystemcog.org/projects/wip/drq_interp_cell_center
        if self.cell_measures in ['--MODEL', ]:
            self.cell_measures = ''
        elif self.cell_measures in ['--OPT', ]:
            self.cell_measures = ''
        if self.long_name is None:
            self.long_name = "empty in DR %s" % data_request.get_version()
        if self.units is None:
            self.units = "empty in DR %s" % data_request.get_version()
        if self.modeling_realm in ["seaIce", ] and re.match(".*areacella.*", str(self.cell_measures)) \
                and self.label not in ["siconca", ]:
            self.comments = ". Due an error in DR01.00.21 and to technical constraints, this variable may have " \
                                "attribute cell_measures set to area: areacella, while it actually is area: areacello"
        super().correct_data_request()

    @classmethod
    def get_from_dr(cls, input_var, sn_issues=None, allow_pseudo=False, mip_list=list(), id=None, **kwargs):
        logger = get_logger()
        input_var_dict = copy.deepcopy(input_var.__dict__)
        data_request = get_data_request()
        if input_var.stid in ["__struct_not_found_001__", ]:
            struct = None
            if data_request.print_DR_errors:
                logger.warning("Warning: stid for %s in table %s is a broken link to structure in DR: %s" %
                               (input_var.label, input_var.mipTable, input_var.stid))
            spatial_shp = False
            temporal_shp = False
        else:
            struct = data_request.get_element_uid(input_var.stid)
            spatial_shp = data_request.get_element_uid(struct.spid, error_msg="Warning: spatial shape for %s in table "
                                                                              "%s not found in DR." %
                                                                              (input_var.label, input_var.mipTable))
            if spatial_shp is not None:
                spatial_shp = spatial_shp.label
            temporal_shp = data_request.get_element_uid(struct.tmid, error_msg="Warning: temporal shape for %s in table"
                                                                               " %s not found in DR." %
                                                                               (input_var.label, input_var.mipTable))
            if temporal_shp is not None:
                temporal_shp = temporal_shp.label
        table = data_request.get_element_uid(input_var.mtid)
        mipvar = data_request.get_element_uid(input_var.vid)
        if struct is not None:
            cm = data_request.get_element_uid(struct.cmid, check_print_DR_errors=False,
                                              error_msg="No cell method for %-15s %s(%s)"
                                                        % (struct.label, input_var.label, input_var.mipTable))
            measures = struct.cell_measures
        else:
            cm = None
            measures = None
        cm_corrected = cm
        if cm is not None:
            cm = cm.cell_methods
            cm_corrected = cm.replace("mask=siconc or siconca", "mask=siconc")
        sn = data_request.get_element_uid(mipvar.sn)
        # see https://github.com/cmip6dr/CMIP6_DataRequest_VariableDefinitions/issues/279
        if sn._h.label in ["standardname", ]:
            stdname = sn.uid
        else:
            if allow_pseudo:
                stdname = sn.uid
            else:
                stdname = ""
            if sn_issues is not None:
                if stdname not in sn_issues:
                    sn_issues[input_var.label] = set()
                    sn_issues[input_var.label].add(table.label)
        product_of_other_dims = 1
        all_dimids = list()
        if spatial_shp not in ["na-na", ]:
            spid = data_request.get_element_uid(struct.spid)
            all_dimids.extend(spid.dimids)
        if 'cids' in struct.__dict__:
            cids = struct.cids
            # when cids not empty, cids=('dim:p850',) or ('dim:typec4pft', 'dim:typenatgr') for e.g.;
            # when empty , cids=('',).
            if cids[0] not in ['', ]:  # this line is needed prior to version 01.00.08.
                all_dimids.extend(cids)
            # if (svar.label=="rv850") : print "rv850 has cids %s"%cids
        if 'dids' in struct.__dict__:
            dids = struct.dids
            if dids[0] not in ['', ]:
                all_dimids.extend(dids)
        sdims_dict = dict()
        for dimid in all_dimids:
            sdim = data_request.get_element_uid(dimid, elt_type="dim")
            if sdim.dimsize > 1:
                # print "for var % 15s and dim % 15s, size=%3d"%(svar.label,dimid,dimsize)
                pass
            product_of_other_dims *= sdim.dimsize
            sdims_dict[sdim.label] = sdim
        input_var_dict["sdims"] = copy.deepcopy(sdims_dict)
        if product_of_other_dims >1:
            input_var_dict["other_dims_size"] = product_of_other_dims
        priority = input_var.defaultPriority
        if len(mip_list) > 0:
            rv_ids = data_request.get_request_by_id_by_sect(input_var.uid, 'requestVar')
            for rv_id in rv_ids:
                rv = data_request.get_element_uid(rv_id)
                vg = data_request.get_element_uid(rv.vgid)
                if vg.mip in mip_list:
                    if rv.priority < priority:
                        priority = rv.priority
        input_var_dict["units"] = mipvar.units
        input_var_dict["stdname"] = stdname
        input_var_dict["spatial_shp"] = spatial_shp
        input_var_dict["temporal_shp"] = temporal_shp
        input_var_dict["mipTable"] = table.label
        input_var_dict["mipVarLabel"] = mipvar.label
        input_var_dict["cm"] = cm
        input_var_dict["cell_methods"] = cm_corrected
        input_var_dict["Priority"] = priority
        input_var_dict["long_name"] = input_var.title
        input_var_dict["struct"] = struct
        input_var_dict["cell_measures"] = measures
        input_var_dict["id"] = id
        if input_var.description:
            input_var_dict["description"] = input_var.description.rstrip(' ')
        else:
            input_var_dict["description"] = input_var.title
        input_var_dict["type"] = "cmor"
        input_var_dict["mip_era"] = "CMIP6"
        input_var_dict["prec"] = input_var.type
        return cls(**input_var_dict)
