#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generic data request tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict

from dr2xml.dr_interface import get_dr_object
from utilities.logger import get_logger
from dr2xml.settings_interface import get_settings_values, set_internal_value, get_values_from_internal_settings
from dr2xml.utils import print_struct, Dr2xmlError, check_objects_equals
from .generic import complement_svar_using_cmorvar
from dr2xml.laboratories import lab_adhoc_grid_policy


def select_data_request_CMORvars_for_lab(sset=False, year=None):
    """
    A function to list CMOR variables relevant for a lab (and also,
    optionally for an experiment and a year)
    The variables relative to the laboratory settings are get using the dict_interface module:
    list of MIPS, max Tier, list of excluded variables names

    Args:
      sset (boolean): should simulation settings be used
                      the parameter taken here are: source_type,
                      max priority (and all for filtering on the simulation)
                      If sset is False, use union of mips among all grid choices
      year (int,optional) : simulation year - used when sset is not None,
                   to additionally filter on year

    Returns:
      A list of 'simplified CMOR variables'

    """
    logger = get_logger()
    internal_settings = get_settings_values("internal")
    data_request = get_dr_object("get_data_request")
    # Set sizes for lab settings, if available (or use CNRM-CM6-1 defaults)
    mip_list_by_grid = get_values_from_internal_settings("mips")
    grid_choice = get_values_from_internal_settings((sset, "grid_choice"), default="LR", merge=False)
    sizes = get_values_from_internal_settings((sset, "sizes"), default=None, merge=False)
    tierMax = get_values_from_internal_settings((sset, "tierMax"), "tierMax_lset", merge=False)
    excvars = get_values_from_internal_settings("excluded_vars_lset", (sset, "excluded_vars_sset"),
                                                (sset, "excluded_vars_per_config"), merge=True)
    exctab = get_values_from_internal_settings("excluded_tables_lset", (sset, "excluded_tables_sset"), merge=True)
    excpairs = get_values_from_internal_settings("excluded_pairs_lset", (sset, "excluded_pairs_sset"), merge=True)
    incvars = get_values_from_internal_settings((sset, "included_vars"), "excluded_vars_lset", merge=False)
    inctab = get_values_from_internal_settings((sset, "included_tables"), "excluded_tables_lset", merge=False)
    inclinks = get_values_from_internal_settings((sset, "included_request_links"), default=None, merge=False)
    excluded_links = get_values_from_internal_settings((sset, "excluded_request_links"), default=None, merge=False)
    pmax = get_values_from_internal_settings((sset, "max_priority"), "max_priority_lset", merge=False)
    if sset:
        mips_list = set(mip_list_by_grid[grid_choice])
        experiment_id = internal_settings["experiment_for_requests"]
        experiment_filter = dict(experiment_id=experiment_id,
                                 year=year,
                                 filter_on_realization=internal_settings["filter_on_realization"],
                                 realization_index=internal_settings["realization_index"],
                                 branching=internal_settings["branching"],
                                 branch_year_in_child=internal_settings["branch_year_in_child"],
                                 endyear=internal_settings["end_year"])
    else:
        if isinstance(mip_list_by_grid, (dict, OrderedDict)):
            mips_list = set().union(*[set(mip_list_by_grid[grid]) for grid in mip_list_by_grid])
        else:
            mips_list = mip_list_by_grid
        experiment_filter = False
    mips_list = sorted(list(mips_list))

    set_internal_value("grid_choice", grid_choice)

    last_filter_options = get_settings_values("internal_values", "initial_selection_configuration")
    filter_options = dict(tierMax=tierMax, mips_list=mips_list, included_request_links=inclinks,
                          excluded_request_links=excluded_links, max_priority=pmax, included_vars=incvars,
                          excluded_vars=excvars, included_tables=inctab, excluded_tables=exctab,
                          excluded_pairs=excpairs, experiment_filter=experiment_filter, sizes=sizes)
    if check_objects_equals(filter_options, last_filter_options):
        d = get_settings_values("internal_values", "cmor_vars")
    else:
        d, rls = data_request.get_cmorvars_list(tierMax=tierMax, mips_list=mips_list, included_request_links=inclinks,
                                                excluded_request_links=excluded_links, max_priority=pmax,
                                                included_vars=incvars, excluded_vars=excvars, included_tables=inctab,
                                                excluded_tables=exctab, excluded_pairs=excpairs,
                                                experiment_filter=experiment_filter, sizes=sizes)
        set_internal_value("global_rls", rls)
        set_internal_value("cmor_vars", d)
        set_internal_value("initial_selection_configuration", filter_options, action="update")
    logger.info('Number of distinct CMOR variables (whatever the grid): %d' % len(d))
    multiple_grids = list()
    print_multiple_grids = get_settings_values("internal_values", "print_multiple_grids")
    for v in d:
        d[v] = decide_for_grids(v, d[v])
        if len(d[v]) > 1:
            multiple_grids.append(data_request.get_element_uid(v, elt_type="variable").label)
            if print_multiple_grids:
                logger.info("\tVariable %s will be processed with multiple grids: %s"
                            % (multiple_grids[-1], repr(d[v])))
    if not print_multiple_grids and multiple_grids is not None and len(multiple_grids) > 0:
        logger.info("\tThese variables will be processed with multiple grids "
                    "(rerun with print_multiple_grids set to True for details): %s" % repr(sorted(multiple_grids)))
    #
    # Print a count of distinct var labels
    logger.info('Number of distinct var labels is: %d' % len(set([data_request.get_element_uid(v, elt_type="variable").label for v in d])))

    # Translate CMORvars to a list of simplified CMORvar objects
    simplified_vars = []
    allow_pseudo = internal_settings['allow_pseudo_standard_names']
    sn_issues = get_settings_values("internal_values", "sn_issues")
    for v in d:
        svar = get_dr_object("SimpleCMORVar")
        cmvar = data_request.get_element_uid(v, elt_type="variable", sn_issues=sn_issues, allow_pseudo=allow_pseudo,
                                             mip_list=mips_list)
        complement_svar_using_cmorvar(svar, cmvar, [])
        svar.Priority = cmvar.Priority
        svar.grids = d[v]
        simplified_vars.append(svar)
    set_internal_value("sn_issues", sn_issues)
    logger.info('Number of simplified vars is: %d' % len(simplified_vars))
    logger.info("Issues with standard names are: %s" % print_struct(sorted(list(sn_issues))))

    return simplified_vars


def endyear_for_CMORvar(cv, expt, year):
    """
    For a CMORvar, returns the largest year in the time slice(s)
    of those requestItems which apply for experiment EXPT and which
    include YEAR. If no time slice applies, returns None
    """
    # 1- Get the RequestItems which apply to CmorVar
    # 2- Select those requestItems which include expt,
    #    and retain their endyear if larger than former one
    internal_dict = get_settings_values("internal")
    data_request = get_dr_object("get_data_request")

    # Some debug material
    larger = data_request.get_endyear_for_cmorvar(cmorvar=cv, experiment=expt, year=year, internal_dict=internal_dict,
                                                  global_rls=get_settings_values("internal_values", "global_rls"))
    return larger


def decide_for_grids(cmvarid, grids):
    """
    Decide which set of grids a given variable should be produced on

    CMVARID is uid of the CMORvar
    GRIDS is a list of strings for grid as specified in requestLink
    LSET is the laboratory settings dictionary. It carries a policy re. grids

    Returns a list of grid strings (with some normalization) (see below)

    TBD : use Martin's acronyms for grid policy
    """
    # Normalize and remove duplicates in grids list
    ngrids = map(get_dr_object("normalize_grid"), grids)
    ngrids = sorted(list(set(ngrids)))
    #
    policy = get_settings_values("internal", "grid_policy")
    if policy in [None, "DR"]:  # Follow DR spec
        return ngrids
    elif policy in ["native", ]:  # Follow lab grids choice (gr or gn depending on context - see lset['grids"])
        if ngrids == ['cfsites']:
            return ngrids
        else:
            return ["", ]
    elif policy in ["native+DR", ]:  # Produce both in 'native' and DR grid
        if ngrids == ['cfsites', ]:
            return ngrids
        else:
            return sorted(list(set(ngrids) | {''}))
    elif policy in ["adhoc", ]:
        return lab_adhoc_grid_policy(cmvarid, ngrids)
    else:
        raise Dr2xmlError("Invalid grid policy %s" % policy)
