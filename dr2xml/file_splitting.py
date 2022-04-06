#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools to compute split frequencies.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict, defaultdict
from io import open

# Utilities
from .settings_interface import get_settings_values
from .utils import Dr2xmlGridError

# Logger
from logger import get_logger

# Interface to configuration
from .config import get_config_variable, set_config_variable


def read_splitfreqs():
    """
    Read split_frequencies: first column is variable label, second
    column is mipTable; third column is the split_freq
    """
    splitfreqs = get_config_variable("splitfreqs", to_change=True)
    # No need to reread or try for ever
    if splitfreqs is None:
        splitfile = get_settings_values("internal", "split_frequencies")
        try:
            freq = open(splitfile, "r")
            print("Reading split_freqs from file %s" % splitfile)
            lines = freq.readlines()
            freq.close()
            splitfreqs = defaultdict(lambda: OrderedDict)
            for line in [l for l in lines if not l.startswith("#")]:
                (varlabel, table, freq) = line.split()[0:3]
                # Keep smallest factor for each variable label
                if table not in splitfreqs[varlabel]:
                    splitfreqs[varlabel][table] = freq
            set_config_variable("splitfreqs", splitfreqs)
        except:
            splitfreqs = False
            set_config_variable("splitfreqs", splitfreqs)


def read_compression_factors():
    """
    read compression factors: first column is variable label, second
    column is mipTabe; third column is a correction factor due to
    compression efficiency for that variable (good compression <-> high value);
    They should be evaluated on test runs, and applied on runs with
    the same compression_level setting
    This factor is applied above the bytes_per_float setting
    """
    compression_factor = get_config_variable("compression_factor", to_change=True)
    # No need to reread or try for ever
    if compression_factor is not None:
        return
    else:
        try:
            fact = open("compression_factors.dat", "r")
            lines = fact.readlines()
            compression_factor = defaultdict(lambda : OrderedDict)
            for line in [l for l in lines if not l.startswith("#")]:
                varlabel, table, factor = line.split()[0:3]
                # Keep smallest factor for each variablelabel
                if table not in compression_factor[varlabel] or \
                        compression_factor[varlabel][table] > factor:
                    compression_factor[varlabel][table] = factor
            set_config_variable("compression_factor", compression_factor)
        except:
            compression_factor = False
            set_config_variable("compression_factor", compression_factor)
            return


def split_frequency_for_variable(svar, grid, mcfg, context):
    """
    Compute variable level split_freq and returns it as a string

    Method : if shape is basic, compute period using field size and a
    parameter from lset indicating max filesize, with some smart
    rounding.  Otherwise, use a fixed value which depends on shape,
    with a default value

    """
    logger = get_logger()
    internal_settings = get_settings_values("internal")
    splitfreqs = get_config_variable("splitfreqs")
    if splitfreqs is None:
        read_splitfreqs()
        splitfreqs = get_config_variable("splitfreqs")
    if splitfreqs and svar.label in splitfreqs and svar.mipTable in splitfreqs[svar.label]:
        return splitfreqs[svar.label][svar.mipTable]
    else:
        #
        max_size = internal_settings["max_file_size_in_floats"]
        #
        compression_factor = get_config_variable("compression_factor")
        size = field_size(svar, mcfg) * internal_settings["bytes_per_float"]
        if compression_factor is None:
            read_compression_factors()
            compression_factor = get_config_variable("compression_factor")
        if compression_factor and svar.label in compression_factor and \
                svar.mipTable in compression_factor[svar.label]:
            logger.info("Dividing size of %s by %g : %g -> %g"
                        % (svar.label, compression_factor[svar.label][svar.mipTable], size,
                           (size + 0.) // compression_factor[svar.label][svar.mipTable]))
            size = (size + 0.) // compression_factor[svar.label][svar.mipTable]
        # else:
        #    # Some COSP outputs are highly compressed
        #    if 'cfad' in svar.label : size/=10.
        #    if 'clmisr' in svar.label : size/=10.

        if size != 0:
            freq = svar.frequency
            sts = internal_settings["sampling_timestep"][grid][context]
            # Try by years first
            size_per_year = size * timesteps_per_freq_and_duration(freq, 365, sts)
            nbyears = max_size / float(size_per_year)
            logger.debug("size per year=%s, size=%s, nbyears=%g" % (repr(size_per_year), repr(size), nbyears))
            if nbyears > 1.:
                if nbyears > 500:
                    return "500y"
                elif nbyears > 250:
                    return "250y"
                elif nbyears > 100:
                    return "100y"
                elif nbyears > 50:
                    return "50y"
                elif nbyears > 25:
                    return "25y"
                elif nbyears > 10:
                    return "10y"
                elif nbyears > 5:
                    return "5y"
                elif nbyears > 2:
                    return "2y"
                else:
                    return "1y"
            else:
                # Try by month
                size_per_month = size * timesteps_per_freq_and_duration(freq, 31, sts)
                nbmonths = max_size / float(size_per_month)
                if nbmonths > 6.:
                    return "6mo"
                elif nbmonths > 4.:
                    return "4mo"
                elif nbmonths > 3.:
                    return "3mo"
                elif nbmonths > 0.7:
                    return "1mo"
                else:
                    # Try by day
                    size_per_day = size * timesteps_per_freq_and_duration(freq, 1, sts)
                    nbdays = max_size / float(size_per_day)
                    if nbdays > 1.:
                        return "1d"
                    else:
                        raise Dr2xmlGridError("No way to put even a single day of data in %g for frequency %s, var %s,"
                                              " table %s" % (max_size, freq, svar.label, svar.mipTable))
        else:
            raise Dr2xmlGridError(
                "Warning: field_size returns 0 for var %s, cannot compute split frequency." % svar.label)


def timesteps_per_freq_and_duration(freq, nbdays, sampling_tstep):
    """

    :param freq:
    :param nbdays:
    :param sampling_tstep:
    :return:
    """
    # This function returns the number of records within nbdays
    duration = 0.
    # Translate freq strings to duration in days
    if freq in ["3hr", "3hrPt", "3h"]:
        duration = 1. / 8
    elif freq in ["6hr", "6hrPt", "6h"]:
        duration = 1. / 4
    elif freq in ["day", "1d"]:
        duration = 1.
    elif freq in ["5day", "5d"]:
        duration = 5.
    elif freq in ["10day", "10d"]:
        duration = 10.
    elif freq in ["1hr", "hr", "1hrPt", "1h"]:
        duration = 1. / 24
    elif freq in ["mon", "monPt", "monC", "1mo"]:
        duration = 31.
    elif freq in ["yr", "yrPt", "1y"]:
        duration = 365.
    # TBD ; use setting's value for CFsubhr_frequency
    elif freq in ["subhr", "subhrPt", "1ts"]:
        duration = 1. / (86400. / sampling_tstep)
    elif freq in ["dec", "10y"]:
        duration = 10. * 365
    #
    # If freq actually translate to a duration, return
    # number of timesteps for number of days
    #
    if duration != 0.:
        return float(nbdays) / duration
    # Otherwise , return a sensible value
    elif freq in ["fx", ]:
        return 1.
    # elif freq=="monClim" : return (int(float(nbdays)/365) + 1)* 12.
    # elif freq=="dayClim" : return (int(float(nbdays)/365) + 1)* 365.
    # elif freq=="1hrClimMon" : return (int(float(nbdays)/31) + 1) * 24.
    elif freq in ["1hrCM", ]:
        return (int(float(nbdays) / 31) + 1) * 24.
    else:
        raise Dr2xmlGridError("Frequency %s is not handled" % freq)


def field_size(svar, mcfg):
    """

    :param svar:
    :param mcfg:
    :return:
    """
    # COmputing field size is basee on the fact that sptial dimensions
    # are deduced from spatial shape and values in mcfg, while
    # attribute other_dims_size of the variable indicates he prodcut
    # of the non-spatial dimensions sizes

    # ['nho','nlo','nha','nla','nlas','nls','nh1'] / nz = sc.mcfg['nlo']

    nb_lat = mcfg['nh1']
    nb_lat_ocean = mcfg['nh1']
    atm_grid_size = mcfg['nha']
    atm_nblev = mcfg['nla']
    soil_nblev = mcfg['nls']
    oce_nblev = mcfg['nlo']
    oce_grid_size = mcfg['nho']
    # TBD : dimension sizes below should be derived from DR query
    nb_cosp_sites = 129
    nb_lidar_temp = 40
    nb_parasol_refl = 5
    nb_isccp_tau = 7
    nb_isccp_pc = 7
    nb_curtain_sites = 1000
    #
    siz = 0
    s = svar.spatial_shp
    if s in ["XY-A", ]:  # Global field on model atmosphere levels
        siz = atm_nblev * atm_grid_size
    elif s in ["XY-AH", ]:  # Global field on model atmosphere half-levels
        siz = (atm_nblev + 1) * atm_grid_size
    elif s in ["na-AH", ]:  # profile on model atmosphere half-levels
        siz = atm_nblev + 1
    elif s.startswith("XY-P"):  # Global field (pressure levels)
        if "jpdftaure" in svar.label:
            siz = atm_grid_size
        else:
            siz = atm_grid_size * svar.other_dims_size
    elif s.startswith("XY-H") or s.startswith("XY-HG"):  # Global field (altitudes)
        siz = atm_grid_size * svar.other_dims_size
    elif s in ["S-AH", ]:  # Atmospheric profiles (half levels) at specified sites
        siz = (atm_nblev + 1) * nb_cosp_sites
    elif s in ["S-A", ]:  # Atmospheric profiles at specified sites
        siz = atm_nblev * nb_cosp_sites
    elif s in ["S-na", ]:  # Site (129 specified sites)
        siz = nb_cosp_sites
    elif s in ["L-na", ]:  # COSP curtain
        siz = nb_curtain_sites
    elif s in ["L-H40", ]:  # Site profile (at 40 altitudes)
        siz = nb_curtain_sites * svar.other_dims_size
    elif s in ["Y-P19", "Y-P39"]:  # Atmospheric Zonal Mean (on ... pressure levels)
        siz = nb_lat * svar.other_dims_size
    elif s in ["Y-A", ]:  # Zonal mean (on model levels)
        siz = nb_lat * atm_nblev
    elif s in ["Y-na", ]:  # Zonal mean (on surface)
        siz = nb_lat
    elif s in ["na-A", ]:  # Atmospheric profile (model levels)
        # mpmoine_correction:field_size: 'na-A' s'applique a des dims (alevel)+spectband mais aussi a (alevel,site)
        # => *nb_cosp_sites
        siz = atm_nblev * nb_cosp_sites
    elif s in ["XY-S", ]:  # Global field on soil levels
        siz = soil_nblev * atm_grid_size
    elif s in ["XY-SN", ]:  # TBD : restore correct size for fields on snow levels (was supposed to be size 1, for tsnl)
        siz = atm_grid_size
    elif s in ["XY-O", ]:  # Global ocean field on model levels
        siz = oce_nblev * oce_grid_size
    elif s in ["XY-na", ]:  # Global field (single level)
        siz = atm_grid_size
        if svar.modeling_realm in ['ocean', 'seaIce', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean']:
            siz = oce_grid_size
        siz *= svar.other_dims_size
    elif s in ["XY-temp", ]:  # Global field (lidar_temp)
        siz = atm_grid_size * nb_lidar_temp
    elif s in ["XY-sza5", ]:  # Global field (parasol_refl)
        siz = atm_grid_size * nb_parasol_refl
    elif s in ["XY-tau|plev7c", ]:  # Global field (isccp_tau x isccp_pc)
        siz = atm_grid_size * nb_isccp_tau * nb_isccp_pc
    elif s in ["YB-R", "YB-O", "GYB-O"]:  # Ocean Basin Meridional Section (on density surfaces for first one)
        siz = oce_nblev * nb_lat_ocean
    elif s in ["YB-na", ]:  # Ocean Basin Zonal Mean
        siz = nb_lat_ocean
    elif s in ["TR-na", "TRS-na"]:  # Ocean Transect or Sea-ice ocean transect
        siz = svar.other_dims_size
    elif s in ["na-na", ]:  # Global mean/constant
        siz = 1

    if siz == 0:
        raise Dr2xmlGridError("Cannot compute field_size for var %s and shape %s" % (svar.label, s))

    return siz
