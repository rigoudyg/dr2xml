#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Settings functions.

    In particular:

    Provide frequencies for a table name - Both in XIOS syntax and in CMIP6_CV
    and also split_frequencies for the files holding the whole of a table's variables

    Rationale: Because CMIP6_CV does not (yet) provide the correspondence between a table name
    and the corresponding frequency (albeit this is instrumental in DRS), and because
    we need to translate anyway to XIOS syntax
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import sys

# Utilities
from .settings_interface import get_settings_values
from .utils import Dr2xmlError

# Logger
from logger import get_logger

# Global variables and configuration tools
from .config import add_value_in_list_config_variable

# Interface to Data Request
from .dr_interface import print_DR_errors


def freq2datefmt(in_freq, operation, table):
    """

    :param in_freq:
    :param operation:
    :param table:
    :return:
    """
    internal_dict = get_settings_values("internal")
    # WIP doc v6.2.3 - Apr. 2017: <time_range> format is frequency-dependant
    too_long_periods = internal_dict["too_long_periods"]
    datefmt = False
    offset = None
    freq = in_freq
    if freq in ["dec", "10y"]:
        if not any("dec" in f for f in too_long_periods):
            datefmt = "%y"
            if operation in ["average", "minimum", "maximum"]:
                offset = "5y"
            else:
                offset = "10y"
        else:
            freq = "yr"  # Ensure dates in filenames are consistent with content, even if not as required
    if freq in ["yr", "yrPt", "1y"]:
        if not any("yr" in f for f in too_long_periods):
            datefmt = "%y"
            if operation in ["average", "minimum", "maximum"]:
                offset = False
            else:
                offset = "1y"
        else:
            freq = "mon"  # Ensure dates in filenames are consistent with content, even if not as required
    if freq in ["mon", "monC", "monPt", "1mo"]:
        datefmt = "%y%mo"
        if operation in ["average", "minimum", "maximum"]:
            offset = False
        else:
            offset = "1mo"
    elif freq in ["day", "1d"]:
        datefmt = "%y%mo%d"
        if operation in ["average", "minimum", "maximum"]:
            offset = "12h"
        else:
            offset = "1d"
    elif freq in ["10day", "10d"]:
        datefmt = "%y%mo%d"
        if operation in ["average", "minimum", "maximum"]:
            offset = "30h"
        else:
            offset = "2.5d"
    elif freq in ["5day", "5d"]:
        datefmt = "%y%mo%d"
        if operation in ["average", "minimum", "maximum"]:
            offset = "60h"
        else:
            offset = "5d"
    elif freq in ["6hr", "6hrPt", "3hr", "3hrPt", "3hrClim", "1hr", "1hrPt", "hr", "6h", "3h", "1h"]:
        datefmt = "%y%mo%d%h%mi"
        if freq in ["6hr", "6hrPt", "6h"]:
            if operation in ["average", "minimum", "maximum"]:
                offset = "3h"
            else:
                offset = "6h"
        elif freq in ["3hr", "3hrPt", "3hrClim", "3h"]:
            if operation in ["average", "minimum", "maximum"]:
                offset = "90mi"
            else:
                offset = "3h"
        elif freq in ["1hr", "1h", "hr", "1hrPt"]:
            if operation in ["average", "minimum", "maximum"]:
                offset = "30mi"
            else:
                offset = "1h"
    elif freq in ["1hrClimMon", "1hrCM"]:
        datefmt = "%y%mo%d%h%mi"
        offset = "0s"
    elif freq in ["subhr", "subhrPt", "1ts"]:
        datefmt = "%y%mo%d%h%mi%s"
        if operation in ["average", "minimum", "maximum"]:
            # Does it make sense ??
            # assume that 'subhr' means every timestep
            offset = "0.5ts"
        else:
            offset = "1ts"
            if "subhr" in freq and "CFsubhr" in table:
                offset = internal_dict["CFsubhr_frequency"]
    elif "fx" in freq:
        pass  # WIP doc v6.2.3 - Apr. 2017: if frequency="fx", [_<time_range>] is ommitted
    if freq in ["1hrClimMon", "1hrCM"]:
        offset_end = "0s"
    elif offset is not None:
        if operation in ["average", "minimum", "maximum"]:
            if offset is not False:
                offset_end = "-" + offset
            else:
                offset_end = False
        else:
            offset_end = "0s"
    elif "fx" not in freq:
        raise Dr2xmlError("Cannot compute offsets for freq=%s and operation=%s" % (freq, operation))
    else:
        offset = "0s"
        offset_end = "0s"
    return datefmt, offset, offset_end


def analyze_cell_time_method(cm, label, table):
    """
    Depending on cell method string CM, tells / returns
    - which time operation should be done
    - if missing value detection should be set
    - if some climatology has to be done (and its name - e.g. )

    We rely on the missing value detection to match the requirements like
    "where sea-ice", "where cloud" since we suppose fields required in this way
    are physically undefined except on "where something".
    """
    logger = get_logger()
    operation = None
    detect_missing = False
    clim = False
    #
    if cm is None:
        if "fx" in table:
            # Case of fixed fields required by home data request
            operation = "once"
        else:
            if print_DR_errors:
                logger.error("DR Error: cell_time_method is None for %15s in table %s, averaging" % (label, table))
            operation = "average"
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean (with samples weighted by snow mass)" in cm:
        # [amnla-tmnsn]: Snow Mass Weighted (LImon : agesnow, tsnLi)
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('Cannot yet handle time: mean (with samples weighted by snow mass)',
                                           label, table))
        logger.info("Will not explicitly handle time: mean (with samples weighted by snow mass) for "
                    "%15s in table %s -> averaging" % (label, table))
        operation = "average"
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean where cloud" in cm:
        # [amncl-twm]: Weighted Time Mean on Cloud (2 variables ISSCP
        # albisccp et pctisccp, en emDay et emMon)
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('Will not explicitly handle time: mean where cloud', label, table))
        logger.info("Note : assuming that for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # -------------------------------------------------------------------------------------
    elif "time: mean where sea_ice_melt_pound" in cm:
        # [amnnsimp-twmm]: Weighted Time Mean in Sea-ice Melt Pounds (uniquement des
        # variables en SImon)
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where sea_ice_melt_pound', label, table))
        logger.info("Note : assuming that 'time: mean where sea_ice_melt_pound' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # -------------------------------------------------------------------------------------------------
    elif "time: mean where sea_ice" in cm:
        # [amnsi-twm]: Weighted Time Mean on Sea-ice (presque que des
        # variables en SImon, sauf sispeed et sithick en SIday)
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where sea_ice', label, table))
        logger.info("Note : assuming that 'time: mean where sea_ice' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    elif "time: mean where sea" in cm:  # [amnesi-tmn]:
        # Area Mean of Ext. Prop. on Sea Ice : pas utilisee
        logger.warning("time: mean where sea is not supposed to be used (%s,%s)" % (label, table))
    # -------------------------------------------------------------------------------------
    elif "time: mean where sea" in cm:  # [amnesi-tmn]:
        # Area Mean of Ext. Prop. on Sea Ice : pas utilisee
        logger.warning("time: mean where sea is not supposed to be used (%s,%s)" % (label, table))
    # -------------------------------------------------------------------------------------
    elif "time: mean where floating_ice_shelf" in cm:
        # [amnfi-twmn]: Weighted Time Mean on Floating Ice Shelf (presque que des
        # variables en Imon, Iyr, sauf sftflt en LImon !?)
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where floating_ice_shelf', label, table))
        logger.info("Note : assuming that 'time: mean where floating_ice_shelf' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean where grounded_ice_sheet" in cm:
        # [amngi-twm]: Weighted Time Mean on Grounded Ice Shelf (uniquement des
        # variables en Imon, Iyr)
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where grounded_ice_sheet', label, table))
        logger.info("Note : assuming that 'time: mean where grounded_ice_sheet' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean where ice_sheet" in cm:
        # [amnni-twmn]: Weighted Time Mean on Ice Shelf (uniquement des
        # variables en Imon, Iyr)
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where ice_sheet', label, table))
        logger.info("Note : assuming that 'time: mean where ice_sheet' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean where landuse" in cm:
        # [amlu-twm]: Weighted Time Mean on Land Use Tiles (uniquement des
        # variables suffixees en 'Lut')
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where land_use', label, table))
        logger.info("Note : assuming that 'time: mean where landuse' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean where crops" in cm:
        # [amc-twm]: Weighted Time Mean on Crops (uniquement des
        # variables suffixees en 'Crop')
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where crops', label, table))
        logger.info("Note : assuming that 'time: mean where crops' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean where natural_grasses" in cm:
        # [amng-twm]: Weighted Time Mean on Natural Grasses (uniquement des
        # variables suffixees en 'Grass')
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where natural_grasses', label, table))
        logger.info("Note : assuming that 'time: mean where natural_grasses' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean where shrubs" in cm:
        # [ams-twm]: Weighted Time Mean on Shrubs (uniquement des
        # variables suffixees en 'Shrub')
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where shrubs', label, table))
        logger.info("Note : assuming that 'time: mean where shrubs' " 
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean where trees" in cm:
        # [amtr-twm]: Weighted Time Mean on Bare Ground (uniquement des
        # variables suffixees en 'Tree')
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where trees', label, table))
        logger.info("Note : assuming that 'time: mean where trees' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean where vegetation" in cm:
        # [amv-twm]: Weighted Time Mean on Vegetation (pas de variables concernees)
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('time: mean where vegetation', label, table))
        logger.info("Note : assuming that 'time: mean where vegetation' "
                    " for %15s in table %s is well handled by 'detect_missing'" % (label, table))
        operation = "average"
        detect_missing = True
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: maximum within days time: mean over days" in cm:
        # [dmax]: Daily Maximum : tasmax Amon seulement
        if label != 'tasmax' and label != 'sfcWindmax':
            logger.error("Error: issue with variable %s in table %s "
                         "and cell method time: maximum within days time: mean over days" % (label, table))
        # we assume that pingfile provides a reference field which already implements "max within days"
        operation = "average"
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: minimum within days time: mean over days" in cm:
        # [dmin]: Daily Minimum : tasmin Amon seulement
        if label != 'tasmin':
            logger.error("Error: issue with variable %s in table %s  "
                         "and cell method time: minimum within days time: mean over days" % (label, table))
        # we assume that pingfile provides a reference field which already implements "min within days"
        operation = "average"
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean within years time: mean over years" in cm:
        # [aclim]: Annual Climatology
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('Cannot yet compute annual climatology - must do it as a postpro',
                                           label, table))
        logger.info("Cannot yet compute annual climatology for %15s in table %s -> averaging" % (label, table))
        # Could transform in monthly fields to be post-processed
        operation = "average"
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: mean within days time: mean over days" in cm:
        # [amn-tdnl]: Mean Diurnal Cycle
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('File structure for diurnal cycle is not yet CF-compliant', label, table))
        operation = "average"
        clim = True
    # ----------------------------------------------------------------------------------------------------------------
    # mpmoine_correction:analyze_cell_time_method: ajout du cas 'Maximum Hourly Rate'
    elif "time: mean within hours time: maximum over hours" in cm:
        add_value_in_list_config_variable("cell_method_warnings",
                                          ('Cannot yet compute maximum hourly rate', label, table))
        logger.info("TBD: Cannot yet compute maximum hourly rate for %15s in table %s -> averaging" % (label, table))
        # Could output a time average of 24 hourly fields at 01 UTC, 2UTC ...
        operation = "average"
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: minimum" in cm:
        # [tmin]: Temporal Minimum : utilisee seulement dans table daily
        operation = "minimum"
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: maximum" in cm:
        # [tmax]: Time Maximum  : utilisee seulement dans table daily
        operation = "maximum"
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: sum" in cm:
        # [tsum]: Temporal Sum  : pas utilisee !
        # print "Error: time: sum is not supposed to be used - Transformed to 'average' for %s in table %s"
        #       %(label,table)
        operation = "accumulate"
    elif "time: mean" in cm:  # [tmean]: Time Mean
        operation = "average"
    # ----------------------------------------------------------------------------------------------------------------
    elif "time: point" in cm:
        operation = "instant"
    elif table == 'fx' or table == 'Efx' or table == 'Ofx':
        operation = "once"
    # ----------------------------------------------------------------------------------------------------------------
    else:
        logger.warning("Warning: issue when analyzing cell_time_method "
                       "%s for %15s in table %s, assuming it is once" % (cm, label, table))
        operation = "once"

    if not operation:
        # raise dr2xml_error("Fatal: bad xios 'operation' for %s in table %s: %s (%s)"
        #                    %(sv.label,table,operation,sv.cell_methods))
        logger.critical("Fatal: bad xios 'operation' for %s in table %s: %s (%s)" % (label, table, operation, cm))
        operation = "once"
    if not isinstance(detect_missing, bool):
        # raise dr2xml_error("Fatal: bad xios 'detect_missing_value' for %s in table %s: %s (%s)"
        #                    %(sv.label,table,detect_missing,sv.cell_methods))
        logger.critical("Fatal: bad xios 'detect_missing_value' for %s in table %s: %s (%s)" %
                        (label, table, detect_missing, cm))

    return operation, detect_missing, clim


def cmip6_freq_to_xios_freq(freq, table):
    """

    :param freq:
    :param table:
    :return:
    """
    logger = get_logger()
    if freq in ["subhr", "subhrPt"]:
        if table == "CFsubhr":
            rep = get_settings_values("internal", "CFsubhr_frequency")
        elif table is None:
            logger.error("Issue in dr2xml with table None and freq=%s" % freq)
            sys.exit(0)
        else:
            rep = "1ts"
    else:
        corresp = {
            "1hr": "1h",
            "1hrPt": "1h",
            "hr": "1h",
            "3hr": "3h",
            "3hrPt": "3h",
            "6hr": "6h",
            "6hrPt": "6h",
            #
            "day": "1d",
            "5day": "5d",
            "10day": "10d",
            #
            "mon": "1mo",
            "monPt": "1mo",
            #
            "yr": "1y",
            "yrPt": "1y",
            #
            "dec": "10y",
            #
            "fx": "1d",
            #
            "monC": "1mo",
            "1hrCM": "1mo",
        }
        rep = corresp[freq]
    return rep


def guess_freq_from_table_name(table):
    """
    Based on non-written CMIP6 conventions, deduce the frequency from the
    table name; returned frequencies are in CMIP6 syntax

    Used for cases where the table is not a CMIP6 one
    """
    logger = get_logger()
    if "subhr" in table:
        return "subhr"
    elif "1hr" in table:
        return "1hr"
    elif "3hr" in table:
        return "3hr"
    elif "6hr" in table:
        return "6hr"
    elif "hr" in table:
        return "1hr"
    elif "5day" in table:
        return "5d"
    elif "day" in table:
        return "day"
    elif "mon" in table:
        return "mon"
    elif "yr" in table:
        return "yr"
    elif "dec" in table:
        return "dec"
    elif "fx" in table:
        return "fx"
    else:
        logger.error("ERROR in guess_freq_from_table : cannot deduce frequency from table named %s" % table)
        sys.exit(1)


def longest_possible_period(freq, too_long_periods):
    """
    Returns the longest period/frequency accessible given the value of too_long_periods
    Input and output freqs follow Xios syntax
    Too_long_periods follow CMIP6 syntax (i.e.  : dec, "yr" )
    """
    if freq in ["10y", ] and any(['dec' in f for f in too_long_periods]):
        return longest_possible_period("1y", too_long_periods)
    elif freq in ["1y", ] and any(['yr' in f for f in too_long_periods]):
        return longest_possible_period("1mo", too_long_periods)
    else:
        return freq


cellmethod2area_dict = {
    "where ice_free_sea over sea ": "ifs",
    "where land": "land",
    "where floating_ice_shelf": "fisf",
    "where land over all_area_types": "loaat",
    "where landuse over all_area_types": "luoaat",
    "where sea": "sea",
    "where sea_ice": "si",
    "where sea_ice_over_sea": "sios",
    "where snow over sea_ice": "sosi",
    "where grounded_ice_shelf": "gisf",
    "where snow": "snow",
    "where cloud": "cloud",
    "where crops": "crops",
    "where grounded_ice_sheet": "gist",
    "ice_sheet": "ist",
    "where landuse": "lu",
    "where natural_grasses": "ngrass",
    "where sea_ice_melt_ponds": "simp",
    "where shrubs": "shrubs",
    "where trees": "trees",
    "where vegetation": "veg",
    "where ice_shelf": "isf"
}


def cellmethod2area(method):
    """
    Analyze METHOD to identify if its part related to area includes
    some key words which describe given area types
    """
    if method is None:
        return None
    else:
        rep = [cellmethod2area_dict[key] for key in cellmethod2area_dict if key in method]
        if len(rep) > 0:
            return rep[0]
        else:
            return None


DR_grid_to_grid_atts_dict = {
    "cfsites": ("gn", "100 km", "data sampled in model native grid by nearest neighbour method "),
    "1deg": ("gr1", "1x1 degree", "data regridded to a CMIP6 standard 1x1 degree latxlon grid from the native grid"),
    "2deg": ("gr2", "2x2 degree", "data regridded to a CMIP6 standard 2x2 degree latxlon grid from the native grid"),
    "100km": ("gr3", "100 km", "data regridded to a CMIP6 standard 100 km resol grid from the native grid"),
    "50km": ("gr4", "50 km", "data regridded to a CMIP6 standard 50 km resol grid from the native grid"),
    "25km": ("gr5", "25 km", "data regridded to a CMIP6 standard 25 km resol grid from the native grid"),
    "default": ["grx", "?x? degree", "grid has no description - please fix DR_grid_to_grid_atts for grid %s"]
}


def DR_grid_to_grid_atts(grid):
    """ Returns label, resolution, description for a DR grid name"""
    default = DR_grid_to_grid_atts_dict["default"]
    default[-1] = default[-1] % grid
    return DR_grid_to_grid_atts_dict.get(grid, default)