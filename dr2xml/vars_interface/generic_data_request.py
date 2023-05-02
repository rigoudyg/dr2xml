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
from dr2xml.settings_interface.py_settings_interface import is_sset_not_None
from dr2xml.utils import print_struct, Dr2xmlError
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
        # Because scope do not accept list types
        rls_for_mips = sc.get_request_link_by_mip(mips_list)
        logger.info("Number of Request Links which apply to MIPS %s  is: %d" %
                    (print_struct(mips_list), len(rls_for_mips)))
        #
        excluded_links = internal_settings["excluded_request_links"]
        rls_for_mips = [rl for rl in rls_for_mips if is_elt_applicable(rl, attribute="label", excluded=excluded_links)]
        logger.info("Number of Request Links after filtering by excluded_request_links is: %d" % len(rls_for_mips))
        #
        inclinks = internal_settings["included_request_links"]
        if len(inclinks) > 0:
            excluded_rls = [rl for rl in rls_for_mips
                            if not is_elt_applicable(rl, attribute="label", included=inclinks)]
            for rl in excluded_rls:
                logger.critical("RequestLink %s is not included" % rl.label)
                rls_for_mips.remove(rl)
        logger.info("Number of Request Links after filtering by included_request_links is: %d" % len(rls_for_mips))
        rls_for_all_experiments = [rl for rl in rls_for_mips]
    else:
        rls_for_mips = sorted(rls_for_all_experiments, key=lambda x: x.label)
    #
    if sset:
        experiment_id = internal_settings["experiment_for_requests"]
        exp = data_request.get_element_uid(data_request.get_experiment_label(experiment_id))
        if exp is not None:
            starty = exp.starty
            endy = exp.endy
        else:
            starty = "??"
            endy = "??"
        logger.info("Filtering for experiment %s, covering years [ %s , %s ] in DR" %
                    (experiment_id, starty, endy))
        # print "Request links before filter :"+`[ rl.label for rl in rls_for_mips ]`
        filtered_rls = []
        for rl in rls_for_mips:
            # Access all requesItems ids which refer to this RequestLink
            rl_req_items = data_request.get_request_by_id_by_sect(rl.uid, 'requestItem')
            if any([RequestItem_applies_for_exp_and_year(data_request.get_element_uid(ri_id), experiment_id, year)[0]
                    for ri_id in rl_req_items]):
                filtered_rls.append(rl)

        rls = filtered_rls
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
            cmvar = data_request.get_element_uid(v)
            st = data_request.get_element_uid(cmvar.stid)
            sp = data_request.get_element_uid(st.spid)
            if sp.label.startswith("S-"):
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
        cmvar = data_request.get_element_uid(v)
        ttable = data_request.get_element_uid(cmvar.mtid)
        mipvar = data_request.get_element_uid(cmvar.vid)
        if is_elt_applicable(mipvar, attribute="label", excluded=excvars, included=incvars) and \
            is_elt_applicable(ttable, attribute="label", excluded=exctab, included=inctab) and \
                is_elt_applicable((mipvar, ttable), attribute="label", excluded=excpairs):
            filtered_vars.append((v, g))
            logger.debug("adding var %s, grid=%s, ttable=%s=" % (cmvar.label, g, ttable.label))  # ,exctab,excvars

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
        cmvar = data_request.get_element_uid(v)
        sn_issues = complement_svar_using_cmorvar(svar, cmvar, sn_issues, [], allow_pseudo)
        svar.Priority = analyze_priority(cmvar, mips_list)
        svar.grids = d[v]
        if data_request.get_element_uid(v).label in ["tas", ]:
            logger.debug("When complementing, tas is included , grids are %s" % svar.grids)
        simplified_vars.append(svar)
    logger.info('Number of simplified vars is: %d' % len(simplified_vars))
    logger.info("Issues with standard names are: %s" % print_struct(sorted(list(sn_issues))))

    return simplified_vars


def is_elt_applicable(elt, attribute=None, included=None, excluded=None):
    if attribute is not None:
        if isinstance(elt, tuple):
            attr = tuple([e.__getattribute__(attribute) for e in elt])
        else:
            attr = elt.__getattribute__(attribute)
    else:
        attr = elt
    test = True
    if test and excluded is not None and len(excluded) > 0 and attr in excluded:
        test = False
    if test and included is not None and len(included) > 0 and attr not in included:
        test = False
    return test


def RequestItem_applies_for_exp_and_year(ri, experiment, year=None):
    """
    Returns True if requestItem 'ri' in data request is relevant
    for a given 'experiment' and 'year'. Toggle 'debug' allow some printouts
    """
    # Returns a couple : relevant, endyear.
    # RELEVANT is True if requestItem RI applies to EXPERIMENT and
    #   has a timeslice wich includes YEAR, either implicitly or explicitly
    # ENDYEAR is meaningful if RELEVANT is True, and is the
    #   last year in the timeslice (or None if timeslice ==
    #   the whole experiment duration)

    # Acces experiment or experiment group for the RequestItem
    # if (ri.label=='C4mipC4mipLandt2') : debug=True
    # if ri.title=='AerChemMIP, AERmon-3d, piControl' : debug=True
    # if ri.title=='CFMIP, CFMIP.CFsubhr, amip' : debug=True
    internal_dict = get_settings_values("internal")
    data_request = get_data_request()
    logger = get_logger()
    logger.debug("In RIapplies.. Checking % 15s" % ri.title)
    item_exp = data_request.get_element_uid(ri.esid)
    ri_applies_to_experiment = False
    endyear = None
    # esid can link to an experiment or an experiment group
    if item_exp._h.label in ['experiment', ]:
        logger.debug("%20s %s" % ("Simple Expt case", item_exp.label))
        if item_exp.label in [experiment, ]:
            logger.debug(" OK",)
            ri_applies_to_experiment = True
    elif item_exp._h.label in ['exptgroup', ]:
        logger.debug("%20s %s" % ("Expt Group case ", item_exp.label))
        exps_id = data_request.get_request_by_id_by_sect(ri.esid, 'experiment')
        for e in [data_request.get_element_uid(eid) for eid in exps_id]:
            if e.label in [experiment, ]:
                logger.debug(" OK for experiment based on group %s" % item_exp.label)
                ri_applies_to_experiment = True
    elif item_exp._h.label in ['mip', ]:
        logger.debug("%20s %s" % ("Mip case ", data_request.get_element_uid(item_exp.label).label))
        exps_id = data_request.get_request_by_id_by_sect(ri.esid, 'experiment')
        for e in [data_request.get_element_uid(eid) for eid in exps_id]:
            logger.debug(e.label + ",",)
            if e.label == experiment:
                logger.debug(" OK for experiment based on mip %s" % item_exp.label)
                ri_applies_to_experiment = True
    else:
        logger.debug("Error on esid link for ri: %s uid=%s %s" % (ri.title, ri.uid, item_exp._h.label))
    # print "ri=%s"%ri.title,
    # if year is not None :
    #    print "Filtering for year %d"%year
    filter_on_realization = internal_dict["filter_on_realization"]
    if filter_on_realization:
        if ri.nenmax != -1 and (internal_dict["realization_index"] > ri.nenmax):
            ri_applies_to_experiment = False

    if ri_applies_to_experiment:
        logger.debug("Year considered: %s %s" % (year, type(year)))
        if year is None:
            rep = True
            endyear = None
            logger.debug(" ..applies because arg year is None")
        else:
            year = int(year)
            exp = data_request.get_element_uid(data_request.get_experiment_label(experiment))
            rep, endyear = year_in_ri(ri, exp, year)
            logger.debug(" ..year in ri returns: %s %s" % (rep, endyear))
            # if (ri.label=="AerchemmipAermonthly3d") :
            #    print "reqItem=%s,experiment=%s,year=%d,rep=%s,"%(ri.label,experiment,year,rep)
        # print " rep=",rep
        return rep, endyear
    else:
        # print
        return False, None


def analyze_priority(cmvar, lmips):
    """
    Returns the max priority of the CMOR variable, for a set of mips
    """
    data_request = get_data_request()
    prio = cmvar.defaultPriority
    rv_ids = data_request.get_request_by_id_by_sect(cmvar.uid, 'requestVar')
    for rv_id in rv_ids:
        rv = data_request.get_element_uid(rv_id)
        vg = data_request.get_element_uid(rv.vgid)
        if vg.mip in lmips:
            if rv.priority < prio:
                prio = rv.priority
    return prio


def year_in_ri(ri, exp, year):
    """
    :param ri: request item
    :param exp: experiment
    :param year: year to treat
    :return: a tuple which contains a boolean indicated whether the year has to be treated and the last year to treat
    """
    logger = get_logger()
    if ri.label in ["CfmipCf3hrSimNew", ]:
        return (year == 2008), 2008
    if "HighResMIP, HighResMIP-6hrPlevExtr, amip" in ri.title:
        return True, 2018
    if 'tslice' in ri.__dict__:
        logger.debug("calling year_in_ri_tslice")
        rep, endyear = year_in_ri_tslice(ri, exp, year)
        return rep, endyear
    try:
        ny = int(ri.nymax)
    except:
        logger.warning("Cannot tell if reqItem %s applies to year %d  (ny=%s) -> assumes yes" % (ri.title, year,
                                                                                                 repr(ny)))
        return True, None
    #
    # From now, this the case of a RequestItem which starts from experiment's start
    actual_first_year = experiment_start_year(exp)  # The start year, possibly fixed by the user
    actual_end_year = experiment_end_year_from_sset(exp)  # = the end year requested by the user if any
    DR_first_year = experiment_start_year_without_sset(exp)
    DR_end_year = experiment_end_year(exp)
    logger.debug("year_in_ri: start DR: %s actual: %s | end DR: %s actual: %s | ny=%d" %
                 (DR_first_year, actual_first_year, DR_end_year, actual_end_year, ny))
    #
    ri_is_for_all_experiment = False
    if ny <= 0:
        ri_is_for_all_experiment = True
        logger.debug("year_in_ri: RI applies systematically")
    else:
        if DR_first_year and DR_end_year and ny == (DR_end_year - DR_first_year + 1):
            ri_is_for_all_experiment = True
            logger.debug("year_in_ri: RI applies because ny=end-start")
    if ri_is_for_all_experiment:
        return True, None
    #
    # From now, we know that requestItem duration is less than experiment duration, or that
    # experiment duration is not known
    # We may have errors in requestItem duration ny, because of an error in DR for start year
    # So, we add to ny the difference between DR and actual start_years, if the DR value is meaningful
    if DR_first_year:
        ny += DR_first_year - actual_first_year  # Will be 0 if end is defined in DR and not by the user
        logger.debug("year_in_ri: compensating ny for diff in first year")
    RI_end_year = actual_first_year + ny - 1
    # For these kind of requestItem of limited duration, no need to extend it, whatever the actual end date
    applies = (year <= RI_end_year)
    logger.debug("year_in_ri: returning %s %s" % (applies, RI_end_year))
    return applies, RI_end_year


def year_in_ri_tslice(ri, exp, year):
    """
    Returns a couple : relevant, endyear.
    RELEVANT is True if requestItem RI applies to
      YEAR, either implicitly or explicitly (e.g. timeslice)
    ENDYEAR, which is meaningful if RELEVANT is True, and is the
      last year in the timeslice (or None if timeslice ==
      the whole experiment duration)
    """
    logger = get_logger()
    internal_dict = get_settings_values("internal")
    data_request = get_data_request()
    if 'tslice' not in ri.__dict__:
        logger.debug("No tslice for reqItem %s -> OK for any year" % ri.title)
        return True, None
    if ri.tslice in ['__unset__', ]:
        logger.debug("tslice is unset for reqItem %s " % ri.title)
        return True, None
    #
    relevant = False
    endyear = None
    tslice = data_request.get_element_uid(ri.tslice)
    logger.debug("tslice label/type is %s/%s for reqItem %s " % (tslice.label, tslice.type, ri.title))
    if tslice.type in ["relativeRange", ]:  # e.g. _slice_abrupt30
        first_year = experiment_start_year(exp)
        # first_year = sset["branch_year_in_child"]
        relevant = (year >= tslice.start + first_year - 1 and year <= tslice.end + first_year - 1)
        endyear = first_year + tslice.end - 1
    elif tslice.type in ["simpleRange", ]:  # e.g. _slice_DAMIP20
        relevant = (year >= tslice.start and year <= tslice.end)
        endyear = tslice.end
    elif tslice.type in ["sliceList", ]:  # e.g. _slice_DAMIP40
        for start in range(tslice.start, int(tslice.end - tslice.sliceLen + 2), int(tslice.step)):
            if year >= start and year < start + tslice.sliceLen:
                relevant = True
                endyear = start + tslice.sliceLen - 1
    elif tslice.type in ["dayList", ]:  # e.g. _slice_RFMIP2
        # e.g. startList[i]: [1980, 1, 1, 1980, 4, 1, 1980, 7, 1, 1980, 10, 1, 1992, 1, 1, 1992, 4, 1]
        years = [tslice.startList[3 * i] for i in range(len(tslice.startList) / 3)]
        if year in years:
            relevant = True
            endyear = year
    elif tslice.type in ["startRange", ]:  # e.g. _slice_VolMIP3
        # used only for VolMIP : _slice_VolMIP3
        start_year = experiment_start_year(exp)
        relevant = (year >= start_year and year < start_year + nyear)
        endyear = start_year + nyear - 1
    elif tslice.type in ["monthlyClimatology", ]:  # e.g. _slice_clim20
        relevant = (year >= tslice.start and year <= tslice.end)
        endyear = tslice.end
    elif tslice.type in ["branchedYears", ]:  # e.g. _slice_piControl020
        branching = internal_dict["branching"]
        if tslice.child in branching:
            endyear = False
            (refyear, starts) = branching[tslice.child]
            for start in starts:
                if ((year - start >= tslice.start - refyear) and
                        (year - start < tslice.start - refyear + tslice.nyears)):
                    relevant = True
                    lastyear = start + tslice.start - refyear + tslice.nyears - 1
                    if endyear is False:
                        endyear = lastyear
                    else:
                        endyear = max(endyear, lastyear)
                    logger.debug("slice OK: year=%d, start=%d tslice.start=%d refyear=%d tslice.nyears=%d lastyear=%d" %
                                 (year, start, tslice.start, refyear, tslice.nyears, lastyear))
        else:
            raise Dr2xmlError("For tslice %s, child %s start year is not documented" % (tslice.title, tslice.child))
    else:
        raise Dr2xmlError("type %s for time slice %s is not handled" % (tslice.type, tslice.title))
    logger.debug("for year %d and experiment %s, relevant is %s for tslice %s of type %s, endyear=%s" %
                 (year, exp.label, repr(relevant), ri.title, tslice.type, repr(endyear)))
    return relevant, endyear


def experiment_start_year_without_sset(exp):
    """
    Find start year of an experiment
    :param exp: experiment
    :param debug: boolean to activate debug log
    :return: start year of the experiment
    """
    logger = get_logger()
    try:
        return int(float(exp.starty))
    except:
        logger.debug("start_year: starty=%s" % exp.starty)
        return None


def experiment_start_year(exp):
    """
    Find star year of an experiment
    :param exp: experiment
    :param debug: boolean for debug verbose level activation
    :return: start year of an experiment
    """
    internal_dict = get_settings_values("internal")
    if "branch_year_in_child" in internal_dict:
        return internal_dict["branch_year_in_child"]
    else:
        starty = experiment_start_year_without_sset(exp)
        if starty is None:
            form = "Cannot guess first year for experiment %s: DR says:'%s' "
            if is_sset_not_None():
                form += "and 'branch_year_in_child' is not provided in experiment's settings"
            raise Dr2xmlError(form % (exp.label, exp.starty))


def experiment_end_year(exp):
    """
    Find the year of an experiment
    :param exp: experiment
    :return: end year of the experiment
    """
    try:
        return int(float(exp.endy))
    except:
        return None


def experiment_end_year_from_sset(exp):
    """
    Find the end year of an experiment
    :param exp: experiment
    :return: end year of the experiment
    """
    internal_dict = get_settings_values("internal")
    if "end_year" in internal_dict:
        return internal_dict["end_year"]
    else:
        return experiment_end_year(exp)


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
    logger = get_logger()
    logger.debug("In end_year for %s %s" % (cv.label, cv.mipTable))
    pmax = internal_dict['max_priority']

    # 1- Get the RequestItems which apply to CmorVar
    rVarsUid = data_request.get_request_by_id_by_sect(cv.uid, 'requestVar')
    rVars = [data_request.get_element_uid(uid) for uid in rVarsUid
             if data_request.get_element_uid(uid).priority <= pmax]
    logger.debug("les requestVars: %s" % " ".join([rVar.title for rVar in rVars]))
    VarGroups = [data_request.get_element_uid(rv.vgid) for rv in rVars]
    logger.debug("les requestVars groups: %s" % " ".join([rVg.label for rVg in VarGroups]))
    RequestLinksId = list()
    for vg in VarGroups:
        RequestLinksId.extend(data_request.get_request_by_id_by_sect(vg.uid, 'requestLink'))
    FilteredRequestLinks = list()
    for rlid in RequestLinksId:
        rl = data_request.get_element_uid(rlid)
        if rl in global_rls:
            FilteredRequestLinks.append(rl)
    logger.debug("les requestlinks: %s" % " ".join([data_request.get_element_uid(rlid).label
                                                    for rlid in RequestLinksId]))
    logger.debug("les FilteredRequestlinks: %s" % " ".join([rl.label for rl in FilteredRequestLinks]))
    RequestItems = list()
    for rl in FilteredRequestLinks:
        RequestItems.extend(data_request.get_request_by_id_by_sect(rl.uid, 'requestItem'))
    logger.debug("les requestItems: %s" % " ".join([data_request.get_element_uid(riid).label for riid in RequestItems]))

    # 2- Select those request links which include expt and year
    larger = None
    for riid in RequestItems:
        ri = data_request.get_element_uid(riid)
        applies, endyear = RequestItem_applies_for_exp_and_year(ri, expt, year)
        logger.debug("For var and freq selected for debug and year %s, for ri %s, applies=%s, endyear=%s" %
                     (str(year), ri.title, str(applies), str(endyear)))
        if applies:
            if endyear is None:
                return None  # One of the timeslices cover the whole expt
            if larger is None:
                larger = endyear
            else:
                larger = max(larger, endyear)
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
