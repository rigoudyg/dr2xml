#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generic data request tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import defaultdict, OrderedDict

from dr2xml.dr_interface import get_scope, get_data_request, normalize_grid
from logger import get_logger
from dr2xml.settings_interface import get_settings_values
from dr2xml.utils import print_struct, Dr2xmlError, is_elt_applicable
from .definitions import SimpleCMORVar
from .generic import complement_svar_using_cmorvar
from dr2xml.laboratories import lab_adhoc_grid_policy

rls_for_all_experiments = None
global_rls = None
sn_issues = OrderedDict()
print_multiple_grids = False
grid_choice = None


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
    data_request = get_data_request()
    # From MIPS set to Request links
    global global_rls, grid_choice, rls_for_all_experiments, sn_issues
    if sset:
        tierMax = internal_settings['tierMax']
    else:
        tierMax = internal_settings['tierMax_lset']
    sc = get_scope(tierMax)
    # Set sizes for lab settings, if available (or use CNRM-CM6-1 defaults)
    if sset:
        grid_choice = internal_settings["grid_choice"]
        mips_list = set(internal_settings['mips'][grid_choice])
        sizes = internal_settings["sizes"]
        sc.mcfg = sc.build_mcfg(sizes)
    else:
        mip_list_by_grid = internal_settings["mips"]
        mips_list = set().union(*[set(mip_list_by_grid[grid]) for grid in mip_list_by_grid])
        grid_choice = "LR"
    # Sort mip_list for reproducibility
    mips_list = sorted(list(mips_list))
    #
    if rls_for_all_experiments is None:
        inclinks = internal_settings["included_request_links"]
        excluded_links = internal_settings["excluded_request_links"]
        rls_for_mips = sc.get_filtered_request_links_by_mip_included_excluded(mips_list=mips_list,
                                                                              included_request_links=inclinks,
                                                                              excluded_request_links=excluded_links)
        rls_for_all_experiments = [rl for rl in rls_for_mips]
    else:
        rls_for_mips = sorted(rls_for_all_experiments, key=lambda x: x.label)
    #
    if sset:
        experiment_id = internal_settings["experiment_for_requests"]

        rls = data_request.filter_request_link_by_experiment_and_year(rls_for_mips, experiment_id, year,
                                                                      internal_settings["filter_on_realization"],
                                                                      internal_settings["realization_index"],
                                                                      internal_settings["branching"],
                                                                      internal_settings["branch_year_in_child"],
                                                                      internal_settings["end_year"])
        logger.info("Number of Request Links which apply to experiment %s member %s and MIPs %s is: %d" %
                    (experiment_id, internal_settings['realization_index'],
                     print_struct(mips_list), len(rls)))
    # print "Request links that apply :"+`[ rl.label for rl in filtered_rls ]`
    else:
        rls = rls_for_mips

    global_rls = rls

    # From Request links to CMOR vars + grid
    # miprl_ids=[ rl.uid for rl in rls ]
    # miprl_vars=sc.varsByRql(miprl_ids, pmax=lset['max_priority'])

    if sset:
        pmax = internal_settings['max_priority']
    else:
        pmax = internal_settings['max_priority_lset']

    miprl_vars_grids = set()

    for rl in rls:
        logger.debug("processing RequestLink %s" % rl.title)
        for v in sc.get_vars_by_request_link(request_link=rl.uid, pmax=pmax):
            # The requested grid is given by the RequestLink except if spatial shape matches S-*
            gr = rl.grid
            cmvar = data_request.get_element_uid(v, elt_type="variable")
            sp = cmvar.spatial_shp
            if sp.startswith("S-"):
                gr = 'cfsites'
            miprl_vars_grids.add((v, gr))
            # if 'ua' in cmvar.label : print "adding %s %s"%(cmvar.label,get_element_uid(cmvar.vid).label)
        # else:
        #    print "Duplicate pair var/grid : ",cmvar.label,cmvar.mipTable,gr
    miprl_vars_grids = sorted(list(miprl_vars_grids))
    logger.info('Number of (CMOR variable, grid) pairs for these requestLinks is: %s' % len(miprl_vars_grids))

    exctab = internal_settings["excluded_tables_lset"]
    if not isinstance(exctab, list):
        exctab = [exctab, ]
    excvars = internal_settings['excluded_vars_lset']
    if not isinstance(excvars, list):
        excvars = [excvars, ]
    excpairs = internal_settings['excluded_pairs_lset']
    if not isinstance(excpairs, list):
        excpairs = [excpairs, ]
    if sset:
        inctab = internal_settings["included_tables"]
        if not isinstance(inctab, list):
            inctab = [inctab, ]
        exctab.extend(internal_settings["excluded_tables_sset"])
        incvars = internal_settings["included_vars"]
        if not isinstance(incvars, list):
            incvars = [incvars, ]
        excvars_sset = internal_settings['excluded_vars_sset']
        if not isinstance(excvars_sset, list):
            excvars_sset = [excvars_sset, ]
        excvars.extend(excvars_sset)
        excvars_config = internal_settings['excluded_vars_per_config']
        if not isinstance(excvars_config, list):
            excvars_config = [excvars_config, ]
        excvars.extend(excvars_config)
        excpairs_sset = internal_settings['excluded_pairs_sset']
        if not isinstance(excpairs_sset, list):
            excpairs_sset = [excpairs_sset, ]
        excpairs.extend(excpairs_sset)
    else:
        inctab = internal_settings["included_tables_lset"]
        if not isinstance(inctab, list):
            inctab = [inctab, ]
        incvars = internal_settings['included_vars_lset']
        if not isinstance(incvars, list):
            incvars = [incvars, ]

    filtered_vars = list()
    for (v, g) in miprl_vars_grids:
        cmvar = data_request.get_element_uid(v, elt_type="variable")
        if is_elt_applicable(cmvar.mipVarLabel, excluded=excvars, included=incvars) and \
            is_elt_applicable(cmvar.mipTable, excluded=exctab, included=inctab) and \
                is_elt_applicable((cmvar.mipVarLabel, cmvar.mipTable), excluded=excpairs):
            filtered_vars.append((v, g))
            logger.debug("adding var %s, grid=%s, ttable=%s=" % (cmvar.label, g, cmvar.mipTable))  # ,exctab,excvars

    logger.info('Number once filtered by excluded/included vars and tables and spatial shapes is: %s'
                % len(filtered_vars))

    # Filter the list of grids requested for each variable based on lab policy
    d = defaultdict(set)
    for (v, g) in filtered_vars:
        d[v].add(g)
    logger.info('Number of distinct CMOR variables (whatever the grid): %d' % len(d))
    multiple_grids = list()
    for v in d:
        d[v] = decide_for_grids(v, d[v])
        if len(d[v]) > 1:
            multiple_grids.append(data_request.get_element_uid(v).label)
            if print_multiple_grids:
                logger.info("\tVariable %s will be processed with multiple grids: %s"
                            % (multiple_grids[-1], repr(d[v])))
    if not print_multiple_grids and multiple_grids is not None and len(multiple_grids) > 0:
        logger.info("\tThese variables will be processed with multiple grids "
                    "(rerun with print_multiple_grids set to True for details): %s" % repr(sorted(multiple_grids)))
    #
    # Print a count of distinct var labels
    logger.info('Number of distinct var labels is: %d' % len(set([data_request.get_element_uid(v).label for v in d])))

    # Translate CMORvars to a list of simplified CMORvar objects
    simplified_vars = []
    allow_pseudo = internal_settings['allow_pseudo_standard_names']
    for v in d:
        svar = SimpleCMORVar()
        cmvar = data_request.get_element_uid(v, elt_type="variable", sn_issues=sn_issues, allow_pseudo=allow_pseudo,
                                             mip_list=mips_list)
        complement_svar_using_cmorvar(svar, cmvar, [])
        svar.Priority = cmvar.Priority
        svar.grids = d[v]
        if data_request.get_element_uid(v, elt_type="variable").label in ["tas", ]:
            logger.debug("When complementing, tas is included , grids are %s" % svar.grids)
        simplified_vars.append(svar)
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
    data_request = get_data_request()

    global global_rls

    # Some debug material
    larger = data_request.get_endyear_for_cmorvar(cv, expt, year, internal_dict, global_rls)
    return larger


def initialize_sn_issues(init):
    """
    Initialize global variable sn_issues
    """
    global sn_issues
    sn_issues = init


def get_grid_choice():
    """
    Get the value of global variable grid_choice
    """
    return grid_choice


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
    ngrids = map(normalize_grid, grids)
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
        if ngrids == ['cfsites']:
            return ngrids
        else:
            return sorted(list(set(ngrids) | {''}))
    elif policy in ["adhoc", ]:
        return lab_adhoc_grid_policy(cmvarid, ngrids)
    else:
        Dr2xmlError("Invalid grid policy %s" % policy)
