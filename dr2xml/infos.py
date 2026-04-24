#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools to print statistics
"""
from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict, defaultdict

from utilities.logger import get_logger


# mpmoine_petitplus: nouvelle fonction print_some_stats (plus d'info sur les skipped_vars, nbre de vars / (shape,freq) )
# SS - non : gros plus
def print_some_stats(context, svars_per_table, skipped_vars_per_table, actually_written_vars, extended=False):
    """

    :param context:
    :param svars_per_table:
    :param skipped_vars_per_table:
    :param actually_written_vars:
    :param extended:
    :return:
    """
    logger = get_logger()

    if True:
        # --------------------------------------------------------------------
        # Print Summary: list of skipped variables per table
        # (i.e. not in the ping_file)
        # --------------------------------------------------------------------
        if skipped_vars_per_table:
            logger.info("\nSkipped variables (i.e. whose alias is not present in the pingfile):")
            for realm in sorted(list(skipped_vars_per_table)):
                for table in sorted(list(skipped_vars_per_table[realm])):
                    for region in sorted(list(skipped_vars_per_table[realm][table])):
                        skipvars = sorted(skipped_vars_per_table[realm][table][region])
                        logger.info(">>> REALM: %15s TABLE: %15s REGION: %15s %02d/%02d ----> %s" %
                                    (realm, table, region, len(skipvars), len(svars_per_table[table][region]),
                                     " ".join(skipvars)))
                        # TBS# print "\n\t",table ," ",len(skipvars),"--->",
                        logger.info("")
                    logger.info("")
                logger.info("")
            logger.info("")

        logger.info("\n\nSome Statistics on actually written variables per frequency+shape...")

        #    ((sv.label,sv.table,sv.frequency,sv.Priority,sv.spatial_shp))
        dic = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))))
        for (label, long_name, stdname, realm, table, region, frequency, Priority, spatial_shp) in actually_written_vars:
            realm = " ".join(sorted(realm.split(" ")))
            dic[realm][frequency][spatial_shp][table][region][Priority].append(label)
        tot_among_realms = 0
        for realm in sorted(list(dic)):
            tot_among_freqs = 0
            for frequency in sorted(list(dic[realm])):
                tot_for_freq_among_shapes = 0
                for spatial_shp in sorted(list(dic[realm][frequency])):
                    tot_for_freq_and_shape_among_tables = 0
                    for table in sorted(list(dic[realm][frequency][spatial_shp])):
                        tot_for_regions_among_table = 0
                        for region in sorted(list(dic[realm][frequency][spatial_shp][table])):
                            for Priority in sorted(list(dic[realm][frequency][spatial_shp][table][region])):
                                list_priority = sorted(dic[realm][frequency][spatial_shp][table][region][Priority])
                                tot_for_freq_and_shape_among_tables += len(list_priority)
                                logger.info("%15s %10s %8s %12s %10s P%1d %3d: %s" %
                                            (" ", " ", " ", table, region, Priority, len(list_priority),
                                             " ".join(list_priority)))
                            tot_for_regions_among_table += tot_for_freq_and_shape_among_tables
                            logger.info("%15s %10s %8s %12s %10s -- %3d" %
                                        (realm, frequency, spatial_shp, table, region, tot_for_freq_and_shape_among_tables))
                        logger.info("%15s %10s %8s %12s %10s -- %3d" %
                                    (realm, frequency, spatial_shp, table, "--------", tot_for_regions_among_table))
                    logger.info("%15s %10s %8s %12s %10s -- %3d" % (realm, frequency, spatial_shp, "--------", "--------",
                                                           tot_for_freq_and_shape_among_tables))
                    tot_for_freq_among_shapes += tot_for_freq_and_shape_among_tables
                    logger.info("")
                logger.info("%15s %10s %8s %12s %10s -- %3d" % (realm, frequency, "--------", "--------", "--------", tot_for_freq_among_shapes))
                tot_among_freqs += tot_for_freq_among_shapes
                logger.info("")
            logger.info("")
            logger.info("%15s %10s %8s %11s %10s -- %3d" % (realm, "----------", "--------", "--------", "--------", tot_among_freqs))
            tot_among_realms += tot_among_freqs
        logger.info("")
        logger.info("%15s %10s %8s %11s %10s -- %3d" % ("----------", "----------", "--------", "--------", "--------", tot_among_realms))

        if extended:
            logger.info("\n\nSome Statistics on actually written variables per variable...")
            dic = OrderedDict()
            dic_ln = defaultdict(set)
            dic_sn = defaultdict(set)
            for label, long_name, stdname, realm, table, region, frequency, Priority, spatial_shp in actually_written_vars:
                dic_ln[label].add(long_name)
                dic_sn[label].add(stdname)
                if label not in dic:
                    dic[label] = list()
                dic[label].append(frequency + '_' + table + '_' + region + "_" + spatial_shp + '_' + str(Priority))

            list_labels = sorted(list(dic))

            for label in list_labels:
                ln = sorted(list(dic_ln[label]), key=lambda x: str(x))
                sn = sorted(list(dic_sn[label]), key=lambda x: str(x))
                logger.info((14 + len(label)) * "-")
                logger.info("--- VARNAME: {}: {}".format(label, ln[0]).strip())
                logger.info((14 + len(label)) * "-")
                for val in dic[label]:
                    logger.info(14 * " " + "* %20s %s" % (val, label))
                if len(ln) > 1:
                    logger.warning(14 * " " + "Warning: several long names are available:")
                    for long_name in ln:
                        logger.warning(18 * " " + "- %s" % long_name)
                if len(sn) > 1:
                    logger.warning(14 * " " + "Warning: several standard names are available:")
                    for stdname in sn:
                        logger.warning(18 * " " + "- %s" % stdname)

        return True
