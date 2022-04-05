#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Variable selection
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import defaultdict

from logger import get_logger
from settings_interface import get_settings_values
from utils import print_struct, Dr2xmlError
from vars_interface.generic_data_request import select_data_request_CMORvars_for_lab, get_grid_choice
from vars_interface.home_data_request import process_home_vars


def test_variables_similar(var_1, var_2):
    return var_1.label == var_2.label and var_1.spatial_shp == var_2.spatial_shp and \
           var_1.frequency == var_2.frequency and var_1.cell_methods == var_2.cell_methods


def check_exclusion(var, *exclusions):
    tests = list()
    reasons = list()
    for (attr, ref, reason) in exclusions:
        test = var.__getattribute__(attr) in ref
        tests.append(test)
        if test:
            reasons.append(reason)
    tests = any(tests)
    if tests:
        reasons = ". ".join(reasons).strip()
        if len(reasons) == 0:
            reasons = "Unknown reason."
    return tests, reasons


def select_variables_to_be_processed(year, context, select):
    """
    Return the list of variables to be processed.
    """
    internal_dict = get_settings_values("internal")
    logger = get_logger()
    #
    # --------------------------------------------------------------------
    # Extract CMOR variables for the experiment and year and lab settings
    # --------------------------------------------------------------------
    mip_vars_list = gather_AllSimpleVars(year, select)
    # Group vars per realm
    svars_per_realm = defaultdict(list)
    for svar in mip_vars_list:
        realm = svar.modeling_realm
        if svar not in svars_per_realm[realm]:
            add = not any([test_variables_similar(svar, ovar) for ovar in svars_per_realm[realm]])
            # Settings may allow for duplicate var in two tables.
            # In DR01.00.21, this actually applies to very few fields (ps-Aermon, tas-ImonAnt, areacellg)
            if internal_dict['allow_duplicates'] or add:
                svars_per_realm[realm].append(svar)
            else:
                logger.warning("Not adding duplicate %s (from %s) for realm %s" % (svar.label, svar.mipTable, realm))
        else:
            logger.warning("Duplicate svar %s %s" % (svar.label, svar.grid))
    logger.info("\nRealms for these CMORvars : %s" % " ".join(sorted(list(svars_per_realm))))
    #
    # --------------------------------------------------------------------
    # Select on context realms, grouping by table
    # Excluding 'excluded_vars' and 'excluded_spshapes' lists
    # --------------------------------------------------------------------
    context_realms = internal_dict['realms_per_context']
    processed_realms = sorted(list(set(context_realms) & set(list(svars_per_realm))))
    non_processed_realms = sorted(list(set(context_realms) - set(list(svars_per_realm))))
    for realm in non_processed_realms:
        print("Processing realm '%s' of context '%s' -- no variable asked (skip)" % (realm, context))
    svars_per_table = defaultdict(list)
    for realm in processed_realms:
        print("Processing realm '%s' of context '%s'" % (realm, context))
        excluded_vars = defaultdict(list)
        for svar in svars_per_realm[realm]:
            # exclusion de certaines spatial shapes (ex. Polar Stereograpic Antarctic/Groenland)
            test, reason = check_exclusion(svar,
                                           ("label", internal_dict["excluded_vars_lset"],
                                            "They are in exclusion list"),
                                           ("spatial_shp", [None, False], "They have no spatial shape"),
                                           ("spatial_shp", internal_dict["excluded_spshapes_lset"],
                                            "They have excluded spatial shape : %s" % svar.spatial_shp))
            if test:
                excluded_vars[reason].append((svar.label, svar.mipTable))
            else:
                svars_per_table[svar.mipTable].append(svar)
        if len(excluded_vars) > 0:
            logger.info("The following pairs (variable,table) have been excluded for these reasons :\n%s" %
                        "\n".join(["%s: %s" % (reason, print_struct(excluded_vars[reason], skip_sep=True, sort=True))
                                   for reason in sorted(list(excluded_vars))]))
    for table in sorted(list(svars_per_table)):
        logger.debug("For table %s: %s" % (table, " ".join([v.label for v in svars_per_table[table]])))
    #
    # --------------------------------------------------------------------
    # Add svars belonging to the orphan list
    # --------------------------------------------------------------------
    orphan_variables = internal_dict["orphan_variables"]
    if context in orphan_variables:
        orphans = orphan_variables[context]
        for svar in [svar for svar in mip_vars_list if svar.label in orphans]:
            test, reason = check_exclusion(svar, ("label", internal_dict["excluded_vars_lset"], ""),
                                           ("spatial_shp", [None, False], ""),
                                           ("spatial_shp", internal_dict["excluded_spshapes_lset"],
                                            ""))
            if not test:
                svars_per_table[svar.mipTable].append(svar)
    #
    # --------------------------------------------------------------------
    # Remove svars belonging to other contexts' orphan lists
    # --------------------------------------------------------------------
    other_contexts = sorted(list(set(orphan_variables) - set([context, ])))
    orphans = list()
    for other_context in other_contexts:
        orphans.extend(orphan_variables[other_context])
    orphans = sorted(list(set(orphans)))
    for table in svars_per_table:
        svars_per_table[table] = [svar for svar in svars_per_table[table] if svar.label not in orphans]
    return svars_per_table


def gather_AllSimpleVars(year=False, select="on_expt_and_year"):
    """
    List of mip variables asked
    :param year: year when the variables are created
    :param select: selection criteria
    :return: list of mip variables
    """
    logger = get_logger()
    internal_dict = get_settings_values("internal")
    if select in ["on_expt_and_year", ""]:
        mip_vars_list = select_data_request_CMORvars_for_lab(True, year)
    elif select in ["on_expt", ]:
        mip_vars_list = select_data_request_CMORvars_for_lab(True, None)
    elif select in ["no", ]:
        mip_vars_list = select_data_request_CMORvars_for_lab(False, None)
    else:
        logger.error("Choice %s is not allowed for arg 'select'" % select)
        raise Dr2xmlError("Choice %s is not allowed for arg 'select'" % select)
    #
    if internal_dict['listof_home_vars']:
        exp = internal_dict['experiment_for_requests']
        mip_vars_list = process_home_vars(mip_vars_list, internal_dict["mips"][get_grid_choice()], expid=exp)
    else:
        logger.info("Info: No HOMEvars list provided.")
    return mip_vars_list


