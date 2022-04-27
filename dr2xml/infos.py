#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools to print statistics
"""
from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict

from logger import get_logger


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
    if False:
        # --------------------------------------------------------------------
        # Print Summary: list of  considered variables per table
        # (i.e. not excuded_vars and not excluded_shapes)
        # --------------------------------------------------------------------
        logger.info("\nTables concerned by context %s : " % context, list(svars_per_table))
        logger.info("\nVariables per table :")
        for table in list(svars_per_table):
            logger.info("\n>>> TABLE:")
            logger.info("%15s %02d ---->" % (table, len(svars_per_table[table])))
            for svar in svars_per_table[table]:
                logger.info("%s (%s)" % (svar.label, str(svar.Priority)))
        logger.info("")

    if True:
        # --------------------------------------------------------------------
        # Print Summary: list of skipped variables per table
        # (i.e. not in the ping_file)
        # --------------------------------------------------------------------
        if skipped_vars_per_table:
            logger.info("\nSkipped variables (i.e. whose alias is not present in the pingfile):")
            for table, skipvars in skipped_vars_per_table.items():
                logger.info(">>> TABLE: %15s %02d/%02d ----> %s" % (table, len(skipvars), len(svars_per_table[table]),
                                                                    " ".join(skipvars)))
                # TBS# print "\n\t",table ," ",len(skipvars),"--->",
                logger.info("")
            logger.info("")

        # --------------------------------------------------------------------
        # Print Summary: list of variables really written in the file_def
        # (i.e. not excluded and not skipped)
        # --------------------------------------------------------------------
        stats_out = {}
        for table in svars_per_table:
            for sv in svars_per_table[table]:
                dic_freq = {}
                dic_shp = {}
                if table not in skipped_vars_per_table or \
                        sv.label + "(" + str(sv.Priority) + ")" not in skipped_vars_per_table[table]:
                    freq = sv.frequency
                    shp = sv.spatial_shp
                    prio = sv.Priority
                    var = sv.label
                    if freq in stats_out:
                        dic_freq = stats_out[freq]
                        if shp in dic_freq:
                            dic_shp = dic_freq[shp]
                    dic_shp.update({var: table + "-P" + str(prio)})
                    dic_freq.update({shp: dic_shp})
                    stats_out.update({freq: dic_freq})

        logger.info("\n\nSome Statistics on actually written variables per frequency+shape...")

        #    ((sv.label,sv.table,sv.frequency,sv.Priority,sv.spatial_shp))
        dic = OrderedDict()
        for label, long_name, table, frequency, Priority, spatial_shp in actually_written_vars:
            if frequency not in dic:
                dic[frequency] = OrderedDict()
            if spatial_shp not in dic[frequency]:
                dic[frequency][spatial_shp] = OrderedDict()
            if table not in dic[frequency][spatial_shp]:
                dic[frequency][spatial_shp][table] = OrderedDict()
            if Priority not in dic[frequency][spatial_shp][table]:
                dic[frequency][spatial_shp][table][Priority] = []
            dic[frequency][spatial_shp][table][Priority].append(label)
        tot_among_freqs = 0
        for frequency in dic:
            tot_for_freq_among_shapes = 0
            for spatial_shp in dic[frequency]:
                tot_for_freq_and_shape_among_tables = 0
                for table in dic[frequency][spatial_shp]:
                    for Priority in dic[frequency][spatial_shp][table]:
                        list_priority = dic[frequency][spatial_shp][table][Priority]
                        tot_for_freq_and_shape_among_tables += len(list_priority)
                        logger.info("%10s %8s %12s P%1d %3d: %s" % (" ", " ", table, Priority, len(list_priority),
                                                                    " ".join(list_priority)))
                logger.info("%10s %8s %11s --- %3d" % (frequency, spatial_shp, "--------",
                                                       tot_for_freq_and_shape_among_tables))
                tot_for_freq_among_shapes += tot_for_freq_and_shape_among_tables
                logger.info("")
            logger.info("%10s %8s %11s --- %3d" % (frequency, "--------", "--------", tot_for_freq_among_shapes))
            tot_among_freqs += tot_for_freq_among_shapes
            logger.info("")
        logger.info("")
        logger.info("%10s %8s %11s --- %3d" % ("----------", "--------", "--------", tot_among_freqs))

        if extended:
            logger.info("\n\nSome Statistics on actually written variables per variable...")
            dic = OrderedDict()
            dic_ln = OrderedDict()
            for label, long_name, table, frequency, Priority, spatial_shp in actually_written_vars:
                if label not in dic:
                    dic[label] = []
                    dic_ln.update({label: long_name})
                dic[label].append(frequency + '_' + table + '_' + spatial_shp + '_' + str(Priority))

            list_labels = list(dic)
            list_labels.sort()
            if len(list_labels) > 0:
                logger.info(">>> DBG >>> %s" % " ".join(list_labels))

            for label in list_labels:
                logger.info((14 + len(label)) * "-")
                logger.info("--- VARNAME: %s: %s" % (label, dic_ln[label]))
                logger.info((14 + len(label)) * "-")
                for val in dic[label]:
                    logger.info(14 * " " + "* %20s %s" % (val, label))

        return True