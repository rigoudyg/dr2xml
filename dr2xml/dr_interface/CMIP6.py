#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface between the CMIP6 Data Request and dr2xml.
# See documentation at: https://c6dreq.dkrz.de/DreqPy_Intro.html
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import re
import sys
from collections import OrderedDict, defaultdict

import six

from utilities.logger import get_logger
from .definition import DataRequest as DataRequestBasic
from .definition import SimpleObject
from .definition import SimpleDim as SimpleDimBasic
from .definition import SimpleCMORVar as SimpleCMORVarBasic
from ..projects.dr2xml import format_sizes
from ..utils import Dr2xmlError, print_struct, is_elt_applicable, convert_string_to_year
from dr2xml.settings_interface import get_settings_values, get_values_from_internal_settings

data_request_path = get_settings_values("internal", "data_request_path")
if data_request_path is not None:
    sys.path.insert(0, data_request_path)

try:
    import dreq
except ImportError:
    from dreqPy import dreq

try:
    from scope import dreqQuery
except ImportError:
    from dreqPy.scope import dreqQuery


class DataRequest(DataRequestBasic):
    def set_mcfg(self):
        self.scope = dreqQuery(dq=self.data_request, tierMax=get_settings_values("internal", "select_tierMax"))
        self.mcfg = format_sizes(self.scope.mcfg)

    def update_mcfg(self):
        mcfg = get_settings_values('internal', 'select_sizes')
        if mcfg is not None:
            self.mcfg = mcfg

    def get_version(self):
        return self.data_request.version

    def get_list_by_id(self, collection, elt_type=None, **kwargs):
        rep = self.data_request.coll[collection]
        if elt_type in ["variable", ]:
            rep = [SimpleCMORVar.get_from_dr(elt, id=elt.uid) for elt in rep.items]
        return rep

    def get_sectors_list(self):
        """
        Get the sectors list.
        :return:
        """
        rep = super().get_sectors_list()
        rep = [dim.label for dim in rep.items if dim.type in ['character', ] and dim.value in ['', ]]
        # Error in DR 01.00.21
        return sorted(list(set(rep) - {"typewetla"}))

    def get_experiment_label(self, experiment):
        return self.data_request.inx.experiment.label[experiment][0]

    def get_experiment_label_start_end_years(self, experiment):
        exp = self.get_element_uid(self.get_experiment_label(experiment))
        if exp is not None:
            return exp.label, exp.starty, exp.endy
        else:
            return super().get_experiment_label_start_end_years(experiment)

    def _filter_request_link_by_experiment_and_year(self, request_links, experiment_id, year,
                                                    filter_on_realization=False, realization_index=1, branching=dict(),
                                                    branch_year_in_child=None, endyear=False):
        logger = get_logger()
        _, starty, endy = self.get_experiment_label_start_end_years(experiment_id)
        logger.info("Filtering for experiment %s, covering years [ %s , %s ] in DR" %
                    (experiment_id, starty, endy))
        # print "Request links before filter :"+`[ rl.label for rl in rls_for_mips ]`
        rep = list()
        for rl in request_links:
            # Access all requesItems ids which refer to this RequestLink
            rl_req_items = self.get_request_by_id_by_sect(rl.uid, 'requestItem')
            if any([self._check_requestitem_for_exp_and_year(self.get_element_uid(ri_id), experiment_id, year,
                                                             filter_on_realization, endyear, realization_index,
                                                             branching, branch_year_in_child)[0]
                    for ri_id in rl_req_items]):
                rep.append(rl)
        return rep

    def _check_requestitem_for_exp_and_year(self, ri, experiment, year, filter_on_realization=False, endyear=False,
                                            realization_index=1, branching=dict(), branch_year_in_child=None):
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
        logger = get_logger()
        logger.debug("In RIapplies.. Checking % 15s" % ri.title)
        item_exp = self.get_element_uid(ri.esid)
        ri_applies_to_experiment = False
        # esid can link to an experiment or an experiment group
        if item_exp._h.label in ['experiment', ]:
            logger.debug("%20s %s" % ("Simple Expt case", item_exp.label))
            if item_exp.label in [experiment, ]:
                logger.debug(" OK", )
                ri_applies_to_experiment = True
        elif item_exp._h.label in ['exptgroup', ]:
            logger.debug("%20s %s" % ("Expt Group case ", item_exp.label))
            exps_id = self.get_request_by_id_by_sect(ri.esid, 'experiment')
            for e in [self.get_element_uid(eid) for eid in exps_id]:
                if e.label in [experiment, ]:
                    logger.debug(" OK for experiment based on group %s" % item_exp.label)
                    ri_applies_to_experiment = True
        elif item_exp._h.label in ['mip', ]:
            logger.debug("%20s %s" % ("Mip case ", self.get_element_uid(item_exp.label).label))
            exps_id = self.get_request_by_id_by_sect(ri.esid, 'experiment')
            for e in [self.get_element_uid(eid) for eid in exps_id]:
                logger.debug(e.label + ",", )
                if e.label == experiment:
                    logger.debug(" OK for experiment based on mip %s" % item_exp.label)
                    ri_applies_to_experiment = True
        else:
            logger.debug("Error on esid link for ri: %s uid=%s %s" % (ri.title, ri.uid, item_exp._h.label))
        # print "ri=%s"%ri.title,
        # if year is not None :
        #    print "Filtering for year %d"%year
        if filter_on_realization:
            if ri.nenmax != -1 and (realization_index > ri.nenmax):
                ri_applies_to_experiment = False

        if ri_applies_to_experiment:
            logger.debug("Year considered: %s %s" % (year, type(year)))
            if year is None:
                rep = True
                endyear = None
                logger.debug(" ..applies because arg year is None")
            else:
                year = int(year)
                rep, endyear = self._is_year_in_requestitem(ri, experiment, year, branching, branch_year_in_child,
                                                            endyear)
                logger.debug(" ..year in ri returns: %s %s" % (rep, endyear))
                # if (ri.label=="AerchemmipAermonthly3d") :
                #    print "reqItem=%s,experiment=%s,year=%d,rep=%s,"%(ri.label,experiment,year,rep)
            # print " rep=",rep
            return rep, endyear
        else:
            # print
            return False, None

    def _is_year_in_requestitem(self, ri, exp, year, branching=dict(), branch_year_in_child=None, endyear=False):
        """
        :param ri: request item
        :param exp: experiment
        :param year: year to treat
        :return: a tuple which contains a boolean indicated whether the year has to be treated and the last year to treat
        """
        logger = get_logger()
        exp_label, exp_startyear, exp_endyear = self.get_experiment_label_start_end_years(exp)
        if ri.label in ["CfmipCf3hrSimNew", ]:
            return (year == 2008), 2008
        if "HighResMIP, HighResMIP-6hrPlevExtr, amip" in ri.title:
            return True, 2018
        if 'tslice' in ri.__dict__:
            logger.debug("calling year_in_ri_tslice")
            rep, endyear = self._is_year_in_requestitem_tslice(ri, exp_label, exp_startyear, year, branching,
                                                               branch_year_in_child)
            return rep, endyear
        try:
            ny = int(ri.nymax)
        except:
            logger.warning("Cannot tell if reqItem %s applies to year %d  (ny=%s) -> assumes yes" % (ri.title, year,
                                                                                                     repr(ny)))
            return True, None
        #
        # From now, this the case of a RequestItem which starts from experiment's start
        actual_first_year = self.find_exp_start_year(exp_label, exp_startyear, branch_year_in_child)  # The start year, possibly fixed by the user
        actual_end_year = self.find_exp_end_year(exp_endyear, endyear)  # = the end year requested by the user if any
        DR_first_year = convert_string_to_year(exp_startyear)
        DR_end_year = convert_string_to_year(exp_endyear)
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

    def _is_year_in_requestitem_tslice(self, ri, exp_label, exp_startyear, year, branching=dict(),
                                       branch_year_in_child=None):
        """
        Returns a couple : relevant, endyear.
        RELEVANT is True if requestItem RI applies to
          YEAR, either implicitly or explicitly (e.g. timeslice)
        ENDYEAR, which is meaningful if RELEVANT is True, and is the
          last year in the timeslice (or None if timeslice ==
          the whole experiment duration)
        """
        logger = get_logger()
        if 'tslice' not in ri.__dict__:
            logger.debug("No tslice for reqItem %s -> OK for any year" % ri.title)
            return True, None
        if ri.tslice in ['__unset__', ]:
            logger.debug("tslice is unset for reqItem %s " % ri.title)
            return True, None
        #
        relevant = False
        endyear = None
        tslice = self.get_element_uid(ri.tslice)
        logger.debug("tslice label/type is %s/%s for reqItem %s " % (tslice.label, tslice.type, ri.title))
        if tslice.type in ["relativeRange", ]:  # e.g. _slice_abrupt30
            first_year = self.find_exp_start_year(exp_label, exp_startyear, branch_year_in_child=branch_year_in_child)
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
            start_year = self.find_exp_start_year(exp_label, exp_startyear, branch_year_in_child=branch_year_in_child)
            relevant = (year >= start_year and year < start_year + nyear)
            endyear = start_year + nyear - 1
        elif tslice.type in ["monthlyClimatology", ]:  # e.g. _slice_clim20
            relevant = (year >= tslice.start and year <= tslice.end)
            endyear = tslice.end
        elif tslice.type in ["branchedYears", ]:  # e.g. _slice_piControl020
            if len(branching) == 0:
                pass
            elif tslice.child in branching:
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
                        logger.debug(
                            "slice OK: year=%d, start=%d tslice.start=%d refyear=%d tslice.nyears=%d lastyear=%d" %
                            (year, start, tslice.start, refyear, tslice.nyears, lastyear))
            else:
                raise Dr2xmlError("For tslice %s, child %s start year is not documented" % (tslice.title, tslice.child))
        else:
            raise Dr2xmlError("type %s for time slice %s is not handled" % (tslice.type, tslice.title))
        logger.debug("for year %d and experiment %s, relevant is %s for tslice %s of type %s, endyear=%s" %
                     (year, exp_label, repr(relevant), ri.title, tslice.type, repr(endyear)))
        return relevant, endyear

    def _get_requestitems_for_cmorvar(self, cmorvar_id, pmax, global_rls):
        logger = get_logger()

        rVarsUid = self.get_request_by_id_by_sect(cmorvar_id, 'requestVar')
        rVars = [self.get_element_uid(uid) for uid in rVarsUid
                 if self.get_element_uid(uid).priority <= pmax]
        logger.debug("les requestVars: %s" % " ".join([rVar.title for rVar in rVars]))
        VarGroups = [self.get_element_uid(rv.vgid) for rv in rVars]
        logger.debug("les requestVars groups: %s" % " ".join([rVg.label for rVg in VarGroups]))
        RequestLinksId = list()
        for vg in VarGroups:
            RequestLinksId.extend(self.get_request_by_id_by_sect(vg.uid, 'requestLink'))
        FilteredRequestLinks = list()
        for rlid in RequestLinksId:
            rl = self.get_element_uid(rlid)
            if rl in global_rls:
                FilteredRequestLinks.append(rl)
        logger.debug("les requestlinks: %s" % " ".join([self.get_element_uid(rlid).label
                                                        for rlid in RequestLinksId]))
        logger.debug("les FilteredRequestlinks: %s" % " ".join([rl.label for rl in FilteredRequestLinks]))
        RequestItems = list()
        for rl in FilteredRequestLinks:
            RequestItems.extend(self.get_request_by_id_by_sect(rl.uid, 'requestItem'))
        logger.debug(
            "les requestItems: %s" % " ".join([self.get_element_uid(riid).label for riid in RequestItems]))
        return RequestItems

    def get_endyear_for_cmorvar(self, cmorvar, experiment, year, internal_dict, global_rls):
        logger = get_logger()
        logger.debug("In end_year for %s %s" % (cmorvar.label, cmorvar.mipTable))
        # 1- Get the RequestItems which apply to CmorVar
        max_priority = get_values_from_internal_settings("max_priority", "max_priority_lset", merge=False)
        request_items = self._get_requestitems_for_cmorvar(cmorvar.id, max_priority, global_rls)

        # 2- Select those request links which include expt and year
        larger = None
        for riid in request_items:
            ri = self.get_element_uid(riid)
            applies, endyear = self._check_requestitem_for_exp_and_year(ri, experiment, year,
                                                                        internal_dict["filter_on_realization"],
                                                                        internal_dict["end_year"],
                                                                        internal_dict["realization_index"],
                                                                        internal_dict["branching"],
                                                                        internal_dict["branch_year_in_child"])
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

    def get_element_uid(self, id=None, error_msg=None, raise_on_error=False, check_print_DR_errors=True,
                        check_print_stdnames_error=False, elt_type=None, **kwargs):
        logger = get_logger()
        if id is None:
            rep = self.data_request.inx.uid
        elif id in self.data_request.inx.uid:
            rep = self.data_request.inx.uid[id]
        else:
            if error_msg is None:
                error_msg = "DR Error: issue with %s" % id
            if raise_on_error:
                raise Dr2xmlError(error_msg)
            elif check_print_DR_errors and self.print_DR_errors:
                logger.error(error_msg)
            elif check_print_stdnames_error and self.print_DR_stdname_errors:
                logger.error(error_msg)
            rep = None
        if rep is not None:
            if elt_type in ["variable", ]:
                rep = SimpleCMORVar.get_from_dr(rep, id=id, **kwargs)
            elif elt_type in ["dim", ]:
                rep = SimpleDim.get_from_dr(rep, id=id)
        return rep

    def get_request_by_id_by_sect(self, id, request):
        return self.data_request.inx.iref_by_sect[id].a[request]

    def get_cmor_var_id_by_label(self, label):
        return self.data_request.inx.CMORvar.label[label]

    def get_dimensions_dict(self):
        rep = OrderedDict()
        for sshp in self.get_list_by_id('spatialShape').items:
            rep[sshp.dimensions] = sshp.label
        return rep

    def get_grids_dict(self):
        rep = OrderedDict()
        for g in self.get_list_by_id("grids").items:
            rep[g.label] = g.uid
        return rep

    def get_single_levels_list(self):
        rep = list()
        for struct in self.get_list_by_id('structure').items:
            spshp = self.get_element_uid(struct.spid)
            if spshp.label in ["XY-na", ] and 'cids' in struct.__dict__:
                if isinstance(struct.cids[0], six.string_types) and len(struct.cids[0]) > 0:
                    # this line is needed prior to version 01.00.08.
                    c = self.get_element_uid(struct.cids[0])
                    # if c.axis == 'Z': # mpmoine_note: non car je veux dans dr_single_levels toutes les dimensions
                    # singletons (ex. 'typenatgr'), par seulement les niveaux
                    rep.append(c.label)
        return rep

    def get_cmorvars_list(self, select_tierMax, select_mips, select_included_request_links,
                          select_excluded_request_links, select_max_priority, select_included_vars,
                          select_excluded_vars, select_included_tables, select_excluded_tables, select_excluded_pairs,
                          experiment_filter=False, **kwargs):
        logger = get_logger()
        self.update_mcfg()
        # Get the request links for all experiments filtered by MIPs
        rls_for_mips = self._get_filtered_request_links_by_mip_included_excluded(
            mips_list=select_mips, included_request_links=select_included_request_links,
            excluded_request_links=select_excluded_request_links
        )
        rls_for_mips = sorted(rls_for_mips, key=lambda x: x.label)
        # Filter by experiment if needed
        if experiment_filter:
            rls = self._filter_request_link_by_experiment_and_year(rls_for_mips, **experiment_filter)
            logger.info("Number of Request Links which apply to experiment %s member %s and MIPs %s is: %d" %
                        (experiment_filter["experiment_id"], experiment_filter['realization_index'],
                         print_struct(select_mips), len(rls)))
        else:
            rls = rls_for_mips
        # Get variables and grids by mips
        miprl_vars_grids = set()
        for rl in rls:
            logger.debug("processing RequestLink %s" % rl.title)
            for v in self._get_vars_by_request_link(request_link=rl.uid, pmax=select_max_priority):
                # The requested grid is given by the RequestLink except if spatial shape matches S-*
                gr = rl.grid
                cmvar = self.get_element_uid(v, elt_type="variable")
                sp = cmvar.spatial_shp
                if sp.startswith("S-"):
                    gr = 'cfsites'
                miprl_vars_grids.add((v, gr))
        miprl_vars_grids = sorted(list(miprl_vars_grids))
        logger.info('Number of (CMOR variable, grid) pairs for these requestLinks is: %s' % len(miprl_vars_grids))
        # Filter variables
        filtered_vars = list()
        for (v, g) in miprl_vars_grids:
            cmvar = self.get_element_uid(v, elt_type="variable")
            if is_elt_applicable(cmvar.mipVarLabel, excluded=select_excluded_vars, included=select_included_vars) and \
                    is_elt_applicable(cmvar.mipTable, excluded=select_excluded_tables, included=select_included_tables) and \
                    is_elt_applicable((cmvar.mipVarLabel, cmvar.mipTable), excluded=select_excluded_pairs):
                filtered_vars.append((v, g))
                logger.debug("adding var %s, grid=%s, ttable=%s=" % (cmvar.label, g, cmvar.mipTable))

        logger.info('Number once filtered by excluded/included vars and tables and spatial shapes is: %s'
                    % len(filtered_vars))

        filtered_vars_with_grids = defaultdict(set)
        for (v, g) in filtered_vars:
            filtered_vars_with_grids[v].add(g)
        return filtered_vars_with_grids, rls

    def _get_request_link_by_mip(self, mips_list):
        return sorted(list(self.scope.getRequestLinkByMip(set(mips_list))), key=lambda x: x.label)

    def _get_filtered_request_links_by_mip_included_excluded(self, mips_list, included_request_links=None,
                                                            excluded_request_links=None):
        logger = get_logger()
        rep = self._get_request_link_by_mip(mips_list)
        logger.info("Number of Request Links which apply to MIPS %s  is: %d" %
                    (print_struct(mips_list), len(rep)))
        rep = [rl for rl in rep if is_elt_applicable(rl, attribute="label", excluded=excluded_request_links)]
        logger.info("Number of Request Links after filtering by excluded_request_links is: %d" % len(rep))
        if included_request_links is not None and len(included_request_links) > 0:
            excluded_rls = [rl for rl in rep if not is_elt_applicable(rl, attribute="label",
                                                                      included=included_request_links)]
            for rl in excluded_rls:
                logger.critical("RequestLink %s is not included" % rl.label)
                rep.remove(rl)
        logger.info("Number of Request Links after filtering by included_request_links is: %d" % len(rep))

        return rep

    def _get_vars_by_request_link(self, request_link, pmax):
        if not isinstance(request_link, list):
            request_link = [request_link, ]
        return self.scope.varsByRql(request_link, pmax)


data_request = None


def initialize_data_request():
    global data_request
    if data_request is None:
        data_request = DataRequest(data_request=dreq.loadDreq(), print_DR_errors=True, print_DR_stdname_errors=False)
    return data_request


def get_data_request():
    if data_request is None:
        return initialize_data_request()
    else:
        return data_request


def normalize_grid(grid):
    """ in DR 1.0.2, values are :
    ['', 'model grid', '100km', '50km or smaller', 'cfsites', '1deg', '2deg', '25km or smaller', 'native']
    """
    if grid in ["native", "model grid", "", None]:
        return ""
    else:
        return grid.replace(" or smaller", "")


class SimpleDim(SimpleDimBasic):
    def correct_data_request(self):
        super().correct_data_request()
        # because value is unset in DR01.00.18
        if self.label in ["misrBands", ]:
            self.dimsize = 16
        if self.type in ["character", ]:
            self.name = "sector"
        else:
            self.name = self.altLabel
        # The latter is a bug in DR01.00.21 : typewetla has no value there
        if self.label in ["typewetla", ]:
            self.value = "wetland"
        if self.name in ["sector", ]:
            if self.label in ["oline", "siline"]:
                self.altLabel = "line"
            elif self.label in ["vegtype", ]:
                self.altLabel = "type"
        if self.name in ["alevel", ]:
            self.name = "lev"
        if self.name in ["sza5", ]:
            self.name = "sza"

    @classmethod
    def get_from_dr(cls, input_dim, id=None, **kwargs):
        input_dim_dict = copy.deepcopy(input_dim.__dict__)
        input_dim_dict["stdname"] = input_dim.standardName
        input_dim_dict["long_name"] = input_dim.title
        input_dim_dict["out_name"] = input_dim.altLabel
        stdname = data_request.get_element_uid(input_dim.standardName, check_print_stdnames_error=True,
                                               check_print_DR_errors=False,
                                               error_msg="Issue with standardname for dimid %s" % id)
        if stdname is not None:
            stdname = stdname.uid
        else:
            stdname = ""
        input_dim_dict["stdname"] = stdname
        return cls(from_dr=True, **input_dim_dict)


class SimpleCMORVar(SimpleCMORVarBasic):
    def correct_data_request(self):
        logger = get_logger()
        if self.label is not None:
            # DR21 has a bug with tsland : the MIP variable is named "ts"
            if self.label in ["tsland", ]:
                self.mipVarLabel = "tsland"
            # Fix for emulating DR01.00.22 from content of DR01.00.21
            if "SoilPools" in self.label:
                self.frequency = "mon"
                self.cell_methods = "area: mean where land time: mean"
            # For PrePARE missing in DR01.00.21!
            if self.label in ["sitimefrac", ]:
                self.stdname = "sea_ice_time_fraction"
            # TBD Next sequences are adhoc for errors DR 01.00.21
            if self.label in ['tauuo', 'tauvo']:
                self.cell_measures = 'area: areacello'
            elif self.cell_measures in ['area: areacella', ] and \
                    self.label in ['tos', 't20d', 'thetaot700', 'thetaot2000', 'thetaot300', 'mlotst']:
                self.cell_measures = 'area: areacello'
            if self.label in ["jpdftaure", ]:
                self.spatial_shape = "XY-na"
        if self.modeling_realm is not None:
            # Because wrong in DR01.00.20
            if self.modeling_realm.startswith("zoo"):
                self.modeling_realm = "ocnBgChem"
            # TBD : this cell_measure choice for seaice variables is specific to Nemo
            if "seaIce" in self.modeling_realm and self.cell_measures is not None and \
                    "areacella" in self.cell_measures:
                if self.label in ['siconca', ]:
                    self.cell_measures = 'area: areacella'
                else:
                    self.cell_measures = 'area: areacello'
        # A number of DR values indicate a choice or a directive for attribute cell_measures (--OPT, --MODEL ...)
        # See interpretation guidelines at https://www.earthsystemcog.org/projects/wip/drq_interp_cell_center
        if self.cell_measures in ['--MODEL', ]:
            self.cell_measures = ''
        elif self.cell_measures in ['--OPT', ]:
            self.cell_measures = ''
        if self.long_name is None:
            self.long_name = "empty in DR %s" % data_request.get_version()
        if self.units is None:
            self.units = "empty in DR %s" % data_request.get_version()
        if self.modeling_realm in ["seaIce", ] and re.match(".*areacella.*", str(self.cell_measures)) \
                and self.label not in ["siconca", ]:
            self.comments = ". Due an error in DR01.00.21 and to technical constraints, this variable may have " \
                                "attribute cell_measures set to area: areacella, while it actually is area: areacello"
        super().correct_data_request()

    @classmethod
    def get_from_dr(cls, input_var, sn_issues=None, allow_pseudo=False, mip_list=list(), id=None, **kwargs):
        logger = get_logger()
        input_var_dict = copy.deepcopy(input_var.__dict__)
        data_request = get_data_request()
        if input_var.stid in ["__struct_not_found_001__", ]:
            struct = None
            if data_request.print_DR_errors:
                logger.warning("Warning: stid for %s in table %s is a broken link to structure in DR: %s" %
                               (input_var.label, input_var.mipTable, input_var.stid))
            spatial_shp = False
            temporal_shp = False
        else:
            struct = data_request.get_element_uid(input_var.stid)
            spatial_shp = data_request.get_element_uid(struct.spid, error_msg="Warning: spatial shape for %s in table "
                                                                              "%s not found in DR." %
                                                                              (input_var.label, input_var.mipTable))
            if spatial_shp is not None:
                spatial_shp = spatial_shp.label
            temporal_shp = data_request.get_element_uid(struct.tmid, error_msg="Warning: temporal shape for %s in table"
                                                                               " %s not found in DR." %
                                                                               (input_var.label, input_var.mipTable))
            if temporal_shp is not None:
                temporal_shp = temporal_shp.label
        table = data_request.get_element_uid(input_var.mtid)
        mipvar = data_request.get_element_uid(input_var.vid)
        if struct is not None:
            cm = data_request.get_element_uid(struct.cmid, check_print_DR_errors=False,
                                              error_msg="No cell method for %-15s %s(%s)"
                                                        % (struct.label, input_var.label, input_var.mipTable))
            measures = struct.cell_measures
        else:
            cm = None
            measures = None
        cm_corrected = cm
        if cm is not None:
            cm = cm.cell_methods
            cm_corrected = cm.replace("mask=siconc or siconca", "mask=siconc")
        sn = data_request.get_element_uid(mipvar.sn)
        # see https://github.com/cmip6dr/CMIP6_DataRequest_VariableDefinitions/issues/279
        if sn._h.label in ["standardname", ]:
            stdname = sn.uid
        else:
            if allow_pseudo:
                stdname = sn.uid
            else:
                stdname = ""
            if sn_issues is not None:
                if stdname not in sn_issues:
                    sn_issues[input_var.label] = set()
                    sn_issues[input_var.label].add(table.label)
        product_of_other_dims = 1
        all_dimids = list()
        if spatial_shp not in ["na-na", ]:
            spid = data_request.get_element_uid(struct.spid)
            all_dimids.extend(spid.dimids)
        if 'cids' in struct.__dict__:
            cids = struct.cids
            # when cids not empty, cids=('dim:p850',) or ('dim:typec4pft', 'dim:typenatgr') for e.g.;
            # when empty , cids=('',).
            if cids[0] not in ['', ]:  # this line is needed prior to version 01.00.08.
                all_dimids.extend(cids)
            # if (svar.label=="rv850") : print "rv850 has cids %s"%cids
        if 'dids' in struct.__dict__:
            dids = struct.dids
            if dids[0] not in ['', ]:
                all_dimids.extend(dids)
        sdims_dict = dict()
        for dimid in all_dimids:
            sdim = data_request.get_element_uid(dimid, elt_type="dim")
            product_of_other_dims *= sdim.dimsize
            sdims_dict[sdim.label] = sdim
        input_var_dict["sdims"] = copy.deepcopy(sdims_dict)
        if product_of_other_dims >1:
            input_var_dict["other_dims_size"] = product_of_other_dims
        priority = input_var.defaultPriority
        if len(mip_list) > 0:
            rv_ids = data_request.get_request_by_id_by_sect(input_var.uid, 'requestVar')
            for rv_id in rv_ids:
                rv = data_request.get_element_uid(rv_id)
                vg = data_request.get_element_uid(rv.vgid)
                if vg.mip in mip_list:
                    if rv.priority < priority:
                        priority = rv.priority
        input_var_dict["units"] = mipvar.units
        input_var_dict["stdname"] = stdname
        input_var_dict["spatial_shp"] = spatial_shp
        input_var_dict["temporal_shp"] = temporal_shp
        input_var_dict["mipTable"] = table.label
        input_var_dict["mipVarLabel"] = mipvar.label
        input_var_dict["cm"] = cm
        input_var_dict["cell_methods"] = cm_corrected
        input_var_dict["Priority"] = priority
        input_var_dict["long_name"] = input_var.title
        input_var_dict["struct"] = struct
        input_var_dict["cell_measures"] = measures
        input_var_dict["id"] = id
        if input_var.description:
            input_var_dict["description"] = input_var.description.rstrip(' ')
        else:
            input_var_dict["description"] = input_var.title
        input_var_dict["type"] = "cmor"
        input_var_dict["mip_era"] = "CMIP6"
        input_var_dict["prec"] = input_var.type
        if struct is not None:
            input_var_dict["flag_meanings"] = struct.flag_meanings
            input_var_dict["flag_values"] = struct.flag_values
        return cls(from_dr=True, **input_var_dict)
