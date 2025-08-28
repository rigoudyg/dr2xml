#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generic variables
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import re
from collections import OrderedDict

import six

from dr2xml.analyzer import cellmethod2area
from dr2xml.dr_interface import get_dr_object
from utilities.logger import get_logger
from dr2xml.settings_interface import get_settings_values
from dr2xml.utils import VarsError, Dr2xmlError

tcmName2tcmValue = {"time-mean": "time: mean", "time-point": "time: point", "None": None}

# List of multi and single pressure level suffixes for which we want the union/zoom axis mecanism turned on
# For not using union/zoom, set 'use_union_zoom' to False in lab settings

# SS : le jeu plev7c est un jeu de couches du simulateur ISCCP - pas d'interpolation
# multi_plev_suffixes=set(["10","19","23","27","39","3","3h","4","7c","7h","8","12"])
multi_plev_suffixes = set(["10", "19", "23", "27", "39", "3", "3h", "4", "7h", "8", "12"])

# SS : les niveaux 220, 560 et 840 sont des couches du simulateur ISCCP - pas d'interpolation
# single_plev_suffixes=set(["1000","200","220","500","560","700","840","850","100"])
single_plev_suffixes = set(["1000", "200", "500", "700", "850", "100"])

ambiguous_mipvarnames = None

# A dict for storing home_variables issues re. standard_names
sn_issues_home = OrderedDict()


def read_home_var(line_split, list_attrs):
    logger = get_logger()
    # Initialize the home variable
    home_var = get_dr_object("SimpleCMORVar")
    # Set values to the different attributes
    home_var.set_attributes(**{key: value for (key, value) in zip(list_attrs, line_split)})
    # Update table
    table = home_var.mipTable
    if table not in ["NONE", ]:
        if "_" not in table:
            logger.critical("Abort: a prefix is expected in extra Table name: " + table)
            raise Dr2xmlError("Abort: a prefix is expected in extra Table name: " + table)
        elif home_var.type not in ["extra", ]:
            table = table.split("_")[1]
            home_var.set_attributes(mipTable=table)
    # Deal with the definition of a reference variable different from the current variable
    # Initially done only for XH-HG field (height levels) but should be applicable everywhere
    if "!" in home_var.label:
        (label, label_ref) = home_var.label.split("!")
        home_var.set_attributes(label=label, ref_var=label_ref)
    else:
        home_var.set_attributes(ref_var=home_var.label)
    return home_var


def fill_homevar(home_var):
    logger = get_logger()
    if home_var.spatial_shp in ["XY-perso", "XY-HG"]:
        home_var_sdims_info = get_settings_values("internal", 'perso_sdims_description')
        if home_var.label in home_var_sdims_info:
            home_var_sdims = OrderedDict()
            for home_var_dim in home_var_sdims_info[home_var.label]:
                home_var_sdim = get_dr_object("SimpleDim")
                home_var_sdim.label = home_var_dim
                for sdim_key in ["zoom_label", "stdname", "long_name", "positive", "requested", "value",
                                 "out_name", "units", "is_zoom_of", "bounds", "boundsValue", "axis", "type",
                                 "coords", "title", "is_union_for"]:
                    if sdim_key in home_var_sdims_info[home_var.label][home_var_dim]:
                        setattr(home_var_sdim, sdim_key,
                                home_var_sdims_info[home_var.label][home_var_dim][sdim_key])
                home_var_sdims[home_var_dim] = home_var_sdim
            home_var.sdims = home_var_sdims
        else:
            logger.error("Could not find custom sdims for {} in simulation settings.".format(home_var.label))
            raise VarsError("Could not find custom sdims for %s in simulation settings." % home_var.label)
    actual_mip = home_var.mip
    if actual_mip.startswith(r"[") and actual_mip.endswith(r"]"):
        home_var.mip = actual_mip.lstrip("[").rstrip("]").split(",")
    return home_var


def check_homevar(home_var, mips, expid):
    add = False
    if (isinstance(home_var.mip, six.string_types) and (home_var.mip == "ANY" or home_var.mip in mips)) or \
            (isinstance(home_var.mip, list) and mips.issuperset(home_var.mip)):
        if home_var.experiment not in ["ANY", ]:
            if expid in home_var.experiment:
                add = True
        else:
            add = True
    return add


def remove_p_suffix(svar, mlev_sfxs, slev_sfxs, realms):
    """
    Remove suffixes only if both suffix of svar.label *and* suffix of one of the svar.dims.label
    match the search suffix to avoid truncation of variable names like 'ch4' requested on 'plev19',
    where '4' does not stand for a plev set
    """
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    #
    # mpmoine_correction:write_xios_file_def_for_svar:remove_p_suffix:
    # suppression des terminaisons en "Clim" le cas echant
    label_out = svar.label.split("Clim")[0]
    #
    svar_realms = svar.set_modeling_realms
    valid_realms = set(realms)
    if svar_realms.intersection(valid_realms):
        mvl = r.match(label_out)
        if mvl and any(label_out.endswith(s) for s in mlev_sfxs.union(slev_sfxs)):
            for sdim in svar.sdims.values():
                mdl = r.match(sdim.label)
                if mdl and mdl.group(2) == mvl.group(2):
                    label_out = mvl.group(1)
    return label_out


def get_correspond_cmor_var(homevar):
    """
        For a home variable, find the CMOR var which corresponds.
        """
    logger = get_logger()
    data_request = get_dr_object("get_data_request")
    count = 0
    empty_table = (homevar.mipTable in ['NONE', ]) or (homevar.mipTable.startswith("None"))
    allow_pseudo = get_settings_values("internal", 'allow_pseudo_standard_names')
    global sn_issues_home
    for cmvarid in data_request.get_cmor_var_id_by_label(homevar.ref_var):
        cmvar = data_request.get_element_uid(cmvarid, elt_type="variable", sn_issues=sn_issues_home,
                                             allow_pseudo=allow_pseudo)
        logger.debug("get_corresp, checking %s vs %s in %s" % (homevar.label, cmvar.label, cmvar.mipTable))
        #
        # Consider case where no modeling_realm associated to the
        # current CMORvar as matching anyway.
        # mpmoine_TBD: A mieux gerer avec les orphan_variables ?
        match_label = (cmvar.label == homevar.ref_var)
        match_freq = (cmvar.frequency == homevar.frequency) or \
                     ("SoilPools" in homevar.label and homevar.frequency in ["mon", ] and
                      cmvar.frequency in ["monPt", ])
        match_table = (cmvar.mipTable == homevar.mipTable)
        empty_realm = len(cmvar.modeling_realm) == 0
        match_realm = (not(empty_realm) and set(homevar.modeling_realm).issubset(cmvar.set_modeling_realms)) or \
                      homevar.modeling_realm == cmvar.modeling_realm

        matching = (match_label and (match_freq or empty_table) and (match_table or empty_table) and
                    (match_realm or empty_realm))
        if matching:
            logger.debug("matches")
            same_shapes = ([cmvar.spatial_shp, cmvar.temporal_shp] == [homevar.spatial_shp, homevar.temporal_shp])
            if same_shapes:
                count += 1
                cmvar_found = cmvar
                logger.debug("and same shapes !")
            else:
                if not empty_table:
                    logger.error("(%s %s) HOMEVar: Spatial and Temporal Shapes specified DO NOT match CMORvar ones. "
                                 "-> Provided: (%s, %s) Expected: (%s, %s)"
                                 % (homevar.label, homevar.mipTable, homevar.spatial_shp, homevar.temporal_shp,
                                    cmvar.spatial_shp, cmvar.temporal_shp))
        else:
            logger.debug("doesn't match %s %s %s %s %s %s %s %s" % (match_label, match_freq, cmvar.frequency,
                                                                    homevar.frequency, match_table, match_realm,
                                                                    empty_realm, homevar.mipTable))

    if count >= 1:
        # empty table means that the frequency is changed (but the variable exists in another frequency cmor table
        if empty_table:
            var_freq_asked = homevar.frequency
        complement_svar_using_cmorvar(homevar, cmvar_found, [])
        if empty_table:
            homevar.frequency = var_freq_asked
            homevar.mipTable = "None" + homevar.frequency
        return homevar
    else:
        return False


def complement_svar_using_cmorvar(svar, cmvar, debug=[]):
    """
    SVAR will have an attribute label_non_ambiguous suffixed by an
    area name if the MIPvarname is ambiguous for that

    Used by get_corresp_cmor_var and by select_cmor_vars_for_lab

    """
    logger = get_logger()
    global ambiguous_mipvarnames
    if ambiguous_mipvarnames is None:
        ambiguous_mipvarnames = analyze_ambiguous_mip_varnames()

    # Get information form CMORvar
    svar.set_attributes(prec=cmvar.prec, frequency=cmvar.frequency, mipTable=cmvar.mipTable,
                        Priority=cmvar.Priority, positive=cmvar.positive,
                        label=cmvar.label, spatial_shp=cmvar.spatial_shp, temporal_shp=cmvar.temporal_shp, cmvar=cmvar,
                        long_name=cmvar.long_name, description=cmvar.description, ref_var=cmvar.label,
                        mipVarLabel=cmvar.mipVarLabel, units=cmvar.units, stdname=cmvar.stdname,
                        cm=cmvar.cm, cell_methods=cmvar.cell_methods, cell_measures=cmvar.cell_measures,
                        sdims=cmvar.sdims, other_dims_size=cmvar.other_dims_size, mip_era=cmvar.mip_era,
                        flag_meanings=cmvar.flag_meanings, flag_values=cmvar.flag_values,
                        modeling_realm=cmvar.modeling_realm, set_modeling_realms=cmvar.set_modeling_realms)
    area = cellmethod2area(svar.cell_methods)
    if svar.label in debug:
        logger.debug("complement_svar ... processing %s, area=%s" % (svar.label, str(area)))
    if area:
        ambiguous = any([svar.label == alabel and arealm in svar.modeling_realm
                         for (alabel, (arealm, lmethod)) in ambiguous_mipvarnames])
        if svar.label in debug:
            logger.debug("complement_svar ... processing %s, ambiguous=%s" % (svar.label, repr(ambiguous)))
        if ambiguous:
            # Special case for a set of land variables
            if not ('land' in svar.modeling_realm and svar.label[0] == 'c'):
                svar.label_non_ambiguous = svar.label + "_" + area
    if svar.label in debug:
        logger.debug("complement_svar ... processing %s, label_non_ambiguous=%s" %
                     (svar.label, svar.label_non_ambiguous))
    # removing pressure suffix must occur after resolving ambiguities (add of area suffix)
    # because this 2 processes cannot be cumulate at this stage.
    # this is acceptable since none of the variables requested on pressure levels have ambiguous names.
    svar.set_attributes(ref_var=svar.label, label_without_psuffix=remove_p_suffix(svar, multi_plev_suffixes,
                                                                                  single_plev_suffixes,
                                                                                  realms=["atmos", "aerosol",
                                                                                          "atmosChem"]))
    #


def analyze_ambiguous_mip_varnames(debug=[]):
    """
    Return the list of MIP varnames whose list of CMORvars for a single realm
    show distinct values for the area part of the cell_methods
    """
    # Compute a dict which keys are MIP varnames and values = list
    # of CMORvars items for the varname
    logger = get_logger()
    data_request = get_dr_object("get_data_request")
    d = data_request.get_variables_per_label(debug=debug)

    # Replace dic values by dic of area portion of cell_methods
    for vlabel in d:
        if len(d[vlabel]) > 1:
            cvl = d[vlabel]
            d[vlabel] = OrderedDict()
            for cv in cvl:
                cm = cv.cell_methods
                if cm is not None:
                    area = cellmethod2area(cm)
                    if area == 'sea' and 'ocean' in cv.modeling_realm:
                        area = None
                    for realm in cv.modeling_realm:
                        if vlabel in debug:
                            logger.debug("for %s 's CMORvar %s(%s), area=%s" % (vlabel, cv.label, cv.mipTable, area))
                        if realm not in d[vlabel]:
                            d[vlabel][realm] = OrderedDict()
                        if area not in d[vlabel][realm]:
                            d[vlabel][realm][area] = []
                        d[vlabel][realm][area].append(cv.mipTable)
            if vlabel in debug:
                print(vlabel, d[vlabel])
        else:
            d[vlabel] = None

    # Analyze ambiguous cases regarding area part of the cell_method
    ambiguous = []
    for vlabel in d:
        if d[vlabel]:
            # print vlabel,d[vlabel]
            for realm in d[vlabel]:
                if len(d[vlabel][realm]) > 1:
                    ambiguous.append((vlabel, (realm, d[vlabel][realm])))
    if "all" in debug:
        for v, p in ambiguous:
            logger.debug(v)
            b, d = p
            for r in d:
                logger.debug("\t %s %s" % (r, d[r]))
    return ambiguous
