#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools to compute split frequencies.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import re
from collections import OrderedDict, defaultdict
from io import open

# Utilities
import six

from .dr_interface import get_dr_object
from .settings_interface import get_settings_values
from .utils import Dr2xmlGridError, Dr2xmlError

# Logger
from utilities.logger import get_logger

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
            with open(splitfile, "r") as freq:
                print("Reading split_freqs from file %s" % splitfile)
                lines = freq.readlines()
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
            with open("compression_factors.dat", "r") as fact:
                lines = fact.readlines()
            compression_factor = defaultdict(lambda: OrderedDict)
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


def split_frequency_for_variable(svar, grid, context):
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
        size = field_size(svar) * internal_settings["bytes_per_float"]
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


freq_regexp = re.compile(r"(?P<len>\d*)(?P<type>(subhr|hr|h|day|d|mon|mo|yr|y|dec))(?P<suffix>(Pt|C|CM)?)")
freq_type_dict = dict(hr=1 / 24., h=1 / 24., day=1., d=1., mon=31., mo=31., yr=365., y=365., dec=10 * 365.)


def timesteps_per_freq_and_duration(freq, nbdays, sampling_tstep):
    """
    This function returns the number of records within nbdays
    :param freq:
    :param nbdays:
    :param sampling_tstep:
    :return:
    """
    if freq in ["fx", ]:
        return 1.
    else:
        # If freq actually translate to a duration, return number of timesteps for number of days
        freq_type_dict['subhr'] = 1 / (86400. / sampling_tstep)
        duration = 0.
        ndays = float(nbdays)
        # Translate freq strings to duration in days
        if isinstance(freq, six.string_types):
            freq_match = freq_regexp.match(freq)
            if freq_match:
                freq_type = freq_match.groupdict()["type"]
                freq_len = freq_match.groupdict()["len"]
                freq_suffix = freq_match.groupdict()["suffix"]
                if freq_suffix in ["CM", ]:
                    ndays = (int(float(nbdays) / 31) + 1)
                if freq_len in ["", None]:
                    freq_len = 1.
                else:
                    freq_len = float(freq_len)
                duration = freq_len * freq_type_dict.get(freq_type, 0.)
        if duration != 0.:
            return ndays / duration
        else:
            raise Dr2xmlGridError("Frequency %s is not handled" % freq)


spatial_shape_regexp = re.compile(r"(?P<hdim>\w+)-(?P<vdim>\w+)(?P<other>(\|\w+)?)")


def field_size(svar):
    """

    :param svar:
    :return:
    """
    # COmputing field size is basee on the fact that sptial dimensions
    # are deduced from spatial shape and values in mcfg, while
    # attribute other_dims_size of the variable indicates he prodcut
    # of the non-spatial dimensions sizes

    # ['nho','nlo','nha','nla','nlas','nls','nh1'] / nz = sc.mcfg['nlo']
    dr = get_dr_object("get_data_request")
    nb_lat = dr.mcfg['nh1']
    nb_lat_ocean = dr.mcfg['nh1']
    atm_grid_size = dr.mcfg['nha']
    atm_nblev = dr.mcfg['nla']
    soil_nblev = dr.mcfg['nls']
    oce_nblev = dr.mcfg['nlo']
    oce_grid_size = dr.mcfg['nho']
    # TBD : dimension sizes below should be derived from DR query
    nb_cosp_sites = dr.mcfg["nb_cosp_sites"]
    nb_lidar_temp = dr.mcfg["nb_lidar_temp"]
    nb_parasol_refl = dr.mcfg["nb_parasol_refl"]
    nb_isccp_tau = dr.mcfg["nb_isccp_tau"]
    nb_isccp_pc = dr.mcfg["nb_isccp_pc"]
    nb_curtain_sites = dr.mcfg["nb_curtain_sites"]
    #
    siz = 0
    s = svar.spatial_shp
    s_match = spatial_shape_regexp.match(s)
    if s_match:
        s_hdim = s_match.groupdict()["hdim"]
        s_vdim = s_match.groupdict()["vdim"]
        s_other = s_match.groupdict()["other"]

        if s_hdim in ["XY", ]:
            if s_vdim in ["O", ] or len(set(svar.list_modeling_realms) &
                                        {'ocean', 'seaIce', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean'}) > 0:
                siz = oce_grid_size
            else:
                siz = atm_grid_size
        elif s_hdim in ["na", "TR", "TRS"]:
            siz = 1
        elif s_hdim in ["S", ]:
            siz = nb_cosp_sites
        elif s_hdim in ["L", ]:
            siz = nb_curtain_sites
        elif s_hdim in ["Y", ]:
            siz = nb_lat
        elif s_hdim in ["YB", "GYB"]:
            siz = nb_lat_ocean

        if s_vdim in ["A", ]:
            siz *= atm_nblev
        elif s_vdim in ["AH", ]:
            siz *= (atm_nblev + 1)
        elif s_vdim.startswith("H") or s_vdim.startswith("P") or (s_vdim in ["na", ] and s_hdim in ["XY", "TR", "TRS"]):
            siz *= svar.other_dims_size
        elif s_vdim in ["S", ]:
            siz *= soil_nblev
        elif s_vdim in ["O", "R"]:
            siz *= oce_nblev
        elif s_vdim in ["temp", ]:
            siz *= nb_lidar_temp
        elif s_vdim in ["sza5", ]:
            siz *= nb_parasol_refl
        elif s_vdim in ["tau", ]:
            siz *= nb_isccp_tau

        if s_other in ["plev7c", ]:
            siz *= nb_isccp_pc

    if siz == 0:
        raise Dr2xmlGridError("Cannot compute field_size for var %s and shape %s" % (svar.label, s))

    return siz


split_freq_units_list = ["d", "mo", "m", "y", "dec"]
units_dict = dict(m="mo")
regexp_split_freq = re.compile(r"(?P<length>\d+)(?P<units>({}))".format("|".join(split_freq_units_list)))


def evaluate_split_freq_value(split_freq):
    split_freq_match = regexp_split_freq.match(split_freq)
    if split_freq_match is None:
        raise ValueError("Unknown format for split_freq value %s" % split_freq)
    else:
        split_freq_units = split_freq_match.groupdict()["units"]
        split_freq_units = units_dict.get(split_freq_units, split_freq_units)
        split_freq_length = int(split_freq_match.groupdict()["length"])
        return split_freq_units, split_freq_length


def determine_split_freq(svar, grid_choice, context):
    split_freq = split_frequency_for_variable(svar, grid_choice, context)
    max_split_freq = get_settings_values("internal", "max_split_freq")
    if max_split_freq is not None:
        split_freq_units, split_freq_length = evaluate_split_freq_value(split_freq)
        max_split_freq_units, max_split_freq_length = evaluate_split_freq_value(max_split_freq)
        if max_split_freq_units == split_freq_units:
            length = min(split_freq_length, max_split_freq_length)
            units = max_split_freq_units
        else:
            units = split_freq_units_list[min(split_freq_units_list.index(split_freq_units),
                                              split_freq_units_list.index(max_split_freq_units))]
            if units == split_freq_units:
                length = split_freq_length
            else:
                length = max_split_freq_length
        split_freq = "{}{}".format(length, units)
    return split_freq
