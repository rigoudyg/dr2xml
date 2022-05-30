#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extra variables
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import os
from collections import OrderedDict, defaultdict

import six

from dr2xml.analyzer import guess_freq_from_table_name
from dr2xml.dr_interface import get_list_of_elements_by_id, get_element_uid
from logger import get_logger
from dr2xml.settings_interface import get_settings_values
from dr2xml.utils import VarsError, read_json_content
from .definitions import SimpleCMORVar, SimpleDim
from .generic import read_home_var, multi_plev_suffixes, single_plev_suffixes, remove_p_suffix, \
    get_simple_dim_from_dim_id

home_attrs = ['type', 'label', 'modeling_realm', 'frequency', 'mipTable', 'temporal_shp', 'spatial_shp',
              'experiment', 'mip']

dims2shape = None
dim2dimid = None
dr_single_levels = None


def read_home_var_extra(line_split, expid, mips, path_extra_tables=None, extra_vars_per_table=defaultdict(list)):
    logger = get_logger()
    rep = list()
    home_var = read_home_var(line_split, home_attrs)
    table = home_var.mipTable
    if table not in "NONE" and "_" not in table:
        logger.error("A prefix is expected in extra Table name %s" % table)
        raise VarsError("A prefix is expected in extra Table name %s" % table)
    if table not in extra_vars_per_table:
        extra_vars_per_table[table] = read_extra_table(path_extra_tables, table)
    if home_var.label in ["ANY", ]:
        var_found = extra_vars_per_table[table]
    else:
        # find home_var in extra_vars
        var_found = [var for var in extra_vars_per_table[table] if var.label == home_var.label]
        if len(var_found) == 0:
            print("Warning: 'extra' variable %s not found in table %s" % (home_var.label, table))
            var_found = list()
        else:
            var_found = var_found[0]
            if home_var.ref_var is not None:
                var_found.ref_var = home_var.ref_var
            var_found = [var_found, ]
    if home_var.mip in ["ANY", ] or home_var.mip in mips:
        if home_var.experiment not in ["ANY", ]:
            if expid in home_var.experiment:
                rep.extend(var_found)
        else:
            rep.extend(var_found)
    return rep


def initialize_dim_variables():
    global dims2shape, dim2dimid, dr_single_levels
    if dims2shape is None:
        dims2shape = OrderedDict()
        dims2shape["longitude|latitude"] = "XY-na"
        for sshp in get_list_of_elements_by_id('spatialShape').items:
            dims2shape[sshp.dimensions] = sshp.label
        # mpmoine_future_modif:dims2shape: ajout a la main des correpondances dims->shapes Primavera qui ne sont pas
        # couvertes par la DR
        # mpmoine_note: attention, il faut mettre a jour dim2shape a chaque fois qu'une nouvelle correpondance
        # est introduite
        # mpmoine_note: attention, dans les extra-Tables
        dims2shape['longitude|latitude|height100m'] = 'XY-na'
        # mpmoine_note: provisoire, XY-P12 juste pour exemple
        dims2shape['longitude|latitude|plev12'] = 'XY-P12'
        # mpmoine_zoom_modif:dims2shape:: ajout de XY-P23 qui a disparu de la DR-00.00.04 mais est demande dans les
        # tables Primavera
        dims2shape['longitude|latitude|plev23'] = 'XY-P23'
        # mpmoine_zoom_modif:dims2shape:: ajout de XY-P10 qui n'est pas dans la DR mais demande dans les tables
        # Primavera
        dims2shape['longitude|latitude|plev10'] = 'XY-P10'
        # David : test
        dims2shape['longitude|latitude|plev7hm'] = 'XY-P7HM'
        # Romain
        dims2shape['longitude|latitude|plev19hm'] = 'XY-P19HM'
        # By level for CORDEX
        dims2shape['longitude|latitude|plev925'] = 'XY-P925HM'
        dims2shape['longitude|latitude|plev850'] = 'XY-P850HM'
        dims2shape['longitude|latitude|plev700'] = 'XY-P700HM'
        dims2shape['longitude|latitude|plev500'] = 'XY-P500HM'
        dims2shape['longitude|latitude|plev200'] = 'XY-P200HM'
    #
    if dim2dimid is None:
        dim2dimid = OrderedDict()
        for g in get_list_of_elements_by_id('grids').items:
            dim2dimid[g.label] = g.uid
    #
    if dr_single_levels is None:
        dr_single_levels = list()
        for struct in get_list_of_elements_by_id('structure').items:
            spshp = get_element_uid(struct.spid)
            if spshp.label in ["XY-na", ] and 'cids' in struct.__dict__:
                if isinstance(struct.cids[0], six.string_types) and len(struct.cids[0]) > 0:
                    # this line is needed prior to version 01.00.08.
                    c = get_element_uid(struct.cids[0])
                    # if c.axis == 'Z': # mpmoine_note: non car je veux dans dr_single_levels toutes les dimensions
                    # singletons (ex. 'typenatgr'), par seulement les niveaux
                    dr_single_levels.append(c.label)
        # other single levels in extra Tables, not in DR
        # mpmoine: les ajouts ici correspondent  aux single levels Primavera.
        other_single_levels = ['height50m', 'p100']
        dr_single_levels.extend(other_single_levels)
    return dims2shape, dim2dimid, dr_single_levels


def read_extra_table(path, table):
    logger = get_logger()
    #
    dims2shape, dim2dimid, dr_single_levels = initialize_dim_variables()
    #
    extravars = list()
    dim_from_extra = defaultdict(OrderedDict)
    dynamic_shapes = defaultdict(OrderedDict)
    #
    mip_era, tbl = table.split('_')
    json_table = path + "/" + table + ".json"
    json_coordinate = path + "/" + mip_era + "_coordinate.json"
    if not os.path.exists(json_table):
        logger.error("Abort: file for extra Table does not exist: " + json_table)
        raise VarsError("Abort: file for extra Table does not exist: " + json_table)
    else:
        tdata = read_json_content(json_table)
        for k, v in tdata["variable_entry"].items():
            if "frequency" in v:
                freq = v["frequency"]
            else:
                freq = guess_freq_from_table_name(tbl)
            extra_var = SimpleCMORVar(type="extra", mip_era=mip_era, label=v["out_name"],
                                      mipVarLabel=v["out_name"], stdname=v.get("standard_name", ""),
                                      long_name=v["long_name"], units=v["units"], modeling_realm=v["modeling_realm"],
                                      frequency=freq, mipTable=tbl, cell_methods=v["cell_methods"],
                                      cell_measures=v["cell_measures"], positive=v["positive"],
                                      Priority=float(v[mip_era.lower() + "_priority"]),
                                      label_without_psuffix=v["out_name"], coordinates=v.get("dimensions", None))
            dims = v["dimensions"].split(" ")
            # get the index of time dimension to supress, if any
            dr_dims = list()
            all_dr_dims = list()
            for (i, d) in enumerate(dims):
                if "time" in d:
                    pass
                elif d not in dr_single_levels:
                    dr_dims.append(d)
                    all_dr_dims.append(d)
                else:
                    all_dr_dims.append(d)
            drdims = "|".join(dr_dims)
            if drdims in dims2shape:
                extra_var.set_attributes(spatial_shp=dims2shape[drdims])
            elif drdims.startswith("longitude|latitude|"):
                # Allow the user to put any additional vertical dimension name
                # which syntax fits further tests, such as P8MINE
                edim = drdims.replace("longitude|latitude|", "", 1)
                if any([d.startswith("height") and d.endswith("m") for d in edim.split("|")]):
                    extra_var.set_attributes(spatial_shp="XY-HG")
                else:
                    extra_var.set_attributes(spatial_shp='XY-' + edim)
                if v["out_name"] not in dynamic_shapes[edim]:
                    dynamic_shapes[edim][v["out_name"]] = extra_var.spatial_shp
            elif "spatial_shp" in v:
                extra_var.set_attributes(spatial_shp=v["spatial_shp"])
            else:
                logger.warning("spatial shape corresponding to %s for variable %s in Table %s not found in DR."
                               % (drdims, v["out_name"], table))
            dr_dimids = list()
            for d in all_dr_dims:
                if d in dim2dimid:
                    dr_dimids.append(dim2dimid[d])
                    extra_dim = get_simple_dim_from_dim_id(dim2dimid[d])
                    extra_var.update_attributes(sdims={extra_dim.label: extra_dim})
                else:
                    extra_dim_info = read_json_content(json_coordinate)["axis_entry"]
                    if d in extra_dim_info:
                        extra_dim_info = extra_dim_info[d]
                    else:
                        raise KeyError("Could not find the dimension definition for %s in %s" % (d, json_coordinate))
                    extra_dim = SimpleDim(label=d, axis=extra_dim_info["axis"], stdname=extra_dim_info["standard_name"],
                                          units=extra_dim_info["units"], long_name=extra_dim_info["long_name"],
                                          out_name=extra_dim_info["out_name"], positive=extra_dim_info["positive"],
                                          title=extra_dim_info.get("title", extra_dim_info["long_name"]),
                                          # values of multi vertical levels
                                          requested=" ".join([ilev for ilev in extra_dim_info["requested"]]).rstrip(),
                                          value=extra_dim_info["value"],  # value of single vertical level
                                          type=extra_dim_info["type"])  # axis type
                    extra_var.update_attributes(sdims={extra_dim.label: extra_dim})
                    if v["out_name"] not in dim_from_extra:
                        dim_from_extra[d][v["out_name"]] = (extra_dim.stdname, extra_dim.requested)
            extra_var.set_attributes(label_without_psuffix=remove_p_suffix(extra_var, multi_plev_suffixes,
                                                                           single_plev_suffixes,
                                                                           realms=["atmos", "aerosol", "atmosChem"]))
            extra_var.set_attributes(ref_var=extra_var.label_without_psuffix)
            extravars.append(extra_var)
    logger.info("For extra table %s (which has %d variables): " % (table, len(extravars)))
    logger.info("\tVariables which dim was found in extra coordinates table:\n%s" %
                "\n".join(["\t\t%20s: %s\n" % (d, " ".join(sorted(dim_from_extra[d])))
                           for d in sorted(list(dim_from_extra))]))
    logger.info("\tDynamical XY-xxx spatial shapes (shapes not found in DR):\n%s" %
                "\n".join(["\t\t%20s: %s\n" % (("XY-" + d), " ".join(sorted(dynamic_shapes[d])))
                           for d in sorted(list(dynamic_shapes))]))
    return extravars


def check_extra_variable(home_var, hv_info):
    logger = get_logger()
    if home_var.Priority <= get_settings_values("internal", "max_priority"):
        logger.debug("Info: %s HOMEVar is read in an extra Table with priority %s => Taken into account." %
                     (hv_info, home_var.Priority))
        return home_var
    else:
        return None
