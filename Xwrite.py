#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
XIOS writing files tools.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

# To have ordered dictionaries
from collections import OrderedDict

import six

# Utilities
from utils import Dr2xmlError

# Logger
from logger import get_logger

# Global variables and configuration tools
from config import get_config_variable

# Interface to settings dictionaries
from settings_interface import get_variable_from_lset_with_default, get_variable_from_lset_without_default, \
    get_variable_from_sset_with_default, get_source_id_and_type, format_dict_for_printing
# Interface to Data Request
from dr_interface import get_DR_version

from xml_interface import DR2XMLElement, DR2XMLComment, create_pretty_xml_doc, find_rank_xml_subelement, wrv, \
    get_project_settings

# Settings tools
from analyzer import DR_grid_to_grid_atts, analyze_cell_time_method, freq2datefmt, longest_possible_period, \
    cmip6_freq_to_xios_freq

# CFsites tools
from cfsites import cfsites_domain_id, add_cfsites_in_defs, cfsites_grid_id, cfsites_input_filedef

# Tools to deal with ping files
from pingfiles_interface import check_for_file_input

# Grids tools
from grids import change_domain_in_grid, change_axes_in_grid, get_grid_def_with_lset, create_standard_domains, \
    add_scalar_in_grid

# Variables tools
from vars_cmor import ping_alias
from vars_home import get_simplevar
from vars_selection import get_sc, endyear_for_CMORvar, get_grid_choice

# Post-processing tools
from postprocessing import process_vertical_interpolation, process_zonal_mean, process_diurnal_cycle, \
    process_levels_over_orog

# XIOS tools
from Xparse import id2gridid, id_has_expr_with_at

# File splitting tools
from file_splitting import split_frequency_for_variable


warnings_for_optimisation = []


def write_xios_file_def_for_svar(sv, year, table, out, field_defs, axis_defs, grid_defs, domain_defs, scalar_defs,
                                 dummies, skipped_vars_per_table, actually_written_vars, context, grid, pingvars=None,
                                 enddate=None, attributes=[], debug=[]):
    """
    Generate an XIOS file_def entry in out for :
      - a dict for laboratory settings
      - a dict of simulation settings
      - a 'simplifed CMORvar' sv
      - which all belong to given table
      - a path 'cvs' for Controlled Vocabulary

    Lenghty code, but not longer than the corresponding specification document

    1- After a prologue, attributes valid for all variables are
    written as file-level metadata, in the same order than in
    WIP document;
    2- Next, field-level metadata are written
    3- For 3D variables in model levels or half-levels, also write the auxilliary
    variables requested by CF convention (e.g. for hybrid coordinate, surface_pressure field
    plus AP and B arrays and their bounds, and lev + lev_bnds with formula attribute)
    """
    logger = get_logger()
    #
    # If list of included vars has size 1, activate debug on the corresponding variable
    inc = get_variable_from_lset_with_default('included_vars', [])
    if len(inc) == 1:
        debug = inc

    # --------------------------------------------------------------------
    # Define alias for field_ref in file-def file
    # - may be replaced by alias1 later
    # - this is not necessarily the alias used in ping file because of
    #   intermediate field id(s) due to union/zoom
    # --------------------------------------------------------------------
    # We use a simple convention for variable names in ping files :
    if sv.type in ['perso', 'dev']:
        alias = sv.label
        alias_ping = sv.ref_var
    else:
        # MPM : si on a defini un label non ambigu alors on l'utilise comme alias (i.e. le field_ref)
        # et pour l'alias seulement (le nom de variable dans le nom de fichier restant svar.label)
        if sv.label_non_ambiguous:
            alias = get_variable_from_lset_without_default("ping_variables_prefix") + sv.label_non_ambiguous
        else:
            alias = get_variable_from_lset_without_default("ping_variables_prefix") + sv.ref_var
        if sv.label in debug:
            logger.debug("write_xios_file_def_for_svar ... processing %s, alias=%s" % (sv.label, alias))

        # suppression des terminaisons en "Clim" pour l'alias : elles concernent uniquement les cas
        # d'absence de variation inter-annuelle sur les GHG. Peut-etre genant pour IPSL ?
        # Du coup, les simus avec constance des GHG (picontrol) sont traitees comme celles avec variation
        split_alias = alias.split("Clim")
        alias = split_alias[0]
        if pingvars is not None:
            # Get alias without pressure_suffix but possibly with area_suffix
            alias_ping = ping_alias(sv, pingvars)
        else:
            alias_ping = sv.ref_var
    #
    # process only variables in pingvars except for dev variables
    # print(pingvars)
    # print("+++ =>>>>>>>>>>>", alias_ping, " ", sv.label)
    # print(alias_ping, "in pingvars?", alias_ping in pingvars)
    if alias_ping not in pingvars and sv.type not in ["dev", "perso"]:
        table = sv.mipTable
        if table not in skipped_vars_per_table:
            skipped_vars_per_table[table] = []
        skipped_vars_per_table[table].append(sv.label + "(" + str(sv.Priority) + ")")
        return
    #
    # --------------------------------------------------------------------
    # Set global CMOR file attributes
    # --------------------------------------------------------------------
    #
    source_id = get_project_settings("__common_values__", "source_id")
    source_type = get_project_settings("__common_values__", "source_type")
    experiment_id = get_project_settings("__common_values__", "experiment_id")
    #
    # --------------------------------------------------------------------
    # Set grid info
    # --------------------------------------------------------------------
    if grid in ["", ]:
        # either native or close-to-native
        grid_choice = get_variable_from_lset_without_default('grid_choice', source_id)
        if sv.type in ["dev", ]:
            target_grid = sv.description.split('|')[1]
            if target_grid in ["native", ]:
                grid_label, target_hgrid_id, zgrid_id, grid_resolution, grid_description = \
                    get_variable_from_lset_without_default('grids_dev', sv.label, grid_choice, context)
            else:
                grid_label, target_hgrid_id, zgrid_id, grid_resolution, grid_description = \
                    get_variable_from_lset_without_default('grids', grid_choice, context)
        else:
            grid_label, target_hgrid_id, zgrid_id, grid_resolution, grid_description = \
                get_variable_from_lset_without_default('grids', grid_choice, context)
    else:
        if grid in ['cfsites', ]:
            target_hgrid_id = cfsites_domain_id
            zgrid_id = None
        else:
            target_hgrid_id = get_variable_from_lset_without_default("ping_variables_prefix") + grid
            zgrid_id = "TBD : Should create zonal grid for CMIP6 standard grid %s" % grid
        grid_label, grid_resolution, grid_description = DR_grid_to_grid_atts(grid, is_dev=(grid == "native" and
                                                                                           sv.type == "dev"))

    if table.endswith("Z"):  # e.g. 'AERmonZ','EmonZ', 'EdayZ'
        grid_label += "z"

    if "Ant" in table:
        grid_label += "a"
    if "Gre" in table:
        grid_label += "g"
    #
    # Check model components re. CV components
    required_components = get_project_settings("__common_values__", "required_model_components", is_default=True,
                                               default=list())
    if not isinstance(required_components, list):
        required_components = [required_components, ]
    allowed_components = get_project_settings("__common_values__", "additional_allowed_model_components",
                                              is_default=True, default=list())
    if not isinstance(allowed_components, list):
        allowed_components = [allowed_components, ]
    actual_components = source_type.split(" ")
    ok = True
    for c in required_components:
        if c not in actual_components:
            ok = False
            logger.warning("Model component %s is required by CMIP6 CV for experiment %s and not present "
                           "(present=%s)" % (c, experiment_id, repr(actual_components)))
    if len(allowed_components) > 0:
        for c in actual_components:
            if c not in allowed_components and c not in required_components:
                ok = False or get_variable_from_sset_with_default('bypass_CV_components', False)
                logger.warning("Warning: Model component %s is present but not required nor allowed (%s)" %
                               (c, repr(allowed_components)))
    if not ok:
        raise Dr2xmlError("Issue with model components")
    #
    # --------------------------------------------------------------------
    # Set NetCDF output file name according to the DRS
    # --------------------------------------------------------------------
    #
    operation, detect_missing, _ = analyze_cell_time_method(sv.cell_methods, sv.label, table)
    # print "--> ",sv.label, sv.frequency, table
    date_format, offset_begin, offset_end = freq2datefmt(sv.frequency, operation, table)
    #
    # --------------------------------------------------------------------
    # Compute XIOS split frequency
    # --------------------------------------------------------------------
    sc = get_sc()
    resolution = get_variable_from_lset_without_default('grid_choice', source_id)
    split_freq = split_frequency_for_variable(sv, resolution, sc.mcfg, context)
    # Cap split_freq by setting max_split_freq (if expressed in years)
    if split_freq[-1] == 'y':
        max_split_freq = get_variable_from_sset_with_default('max_split_freq', None)
        if max_split_freq is None:
            max_split_freq = get_variable_from_lset_with_default('max_split_freq', None)
        if max_split_freq is not None:
            if max_split_freq[0:-1] != "y":
                Dr2xmlError("max_split_freq must end with an 'y' (%s)" % max_split_freq)
            split_freq = "{}y".format(min(int(max_split_freq[0:-1]), int(split_freq[0:-1])))
    # print "split_freq: %-25s %-10s %-8s"%(sv.label,sv.mipTable,split_freq)
    #
    # --------------------------------------------------------------------
    # Write XIOS file node:
    # including global CMOR file attributes
    # --------------------------------------------------------------------
    freq = longest_possible_period(cmip6_freq_to_xios_freq(sv.frequency, table),
                                   get_variable_from_lset_with_default("too_long_periods", []))

    split_freq_format = None
    split_start_offset = None
    split_end_offset = None
    split_last_date = None
    if "fx" not in sv.frequency:
        split_freq_format = date_format
        #
        # Modifiers for date parts of the filename, due to silly KT conventions.
        if offset_begin is not False:
            split_start_offset = offset_begin
        if offset_end is not False:
            split_end_offset = offset_end
        lastyear = None
        # Try to get enddate for the CMOR variable from the DR
        if sv.cmvar is not None:
            # print "calling endyear_for... for %s, with year="%(sv.label), year
            lastyear = endyear_for_CMORvar(sv.cmvar, experiment_id, year)
            # print "lastyear=",lastyear," enddate=",enddate
        if lastyear is None or (enddate is not None and lastyear >= int(enddate[0:4])):
            # DR doesn't specify an end date for that var, or a very late one
            if get_variable_from_lset_with_default('dr2xml_manages_enddate', True):
                # Use run end date as the latest possible date
                # enddate must be 20140101 , rather than 20131231
                if enddate is not None:
                    endyear = enddate[0:4]
                    endmonth = enddate[4:6]
                    endday = enddate[6:8]
                    split_last_date = "{}-{}-{} 00:00:00".format(endyear, endmonth, endday)
                else:
                    split_last_date = "10000-01-01 00:00:00"
        else:
            # Use requestItems-based end date as the latest possible date when it is earlier than run end date
            if sv.label in debug:
                logger.debug("split_last_date year %d derived from DR for variable %s in table %s for year %d" %
                             (lastyear, sv.label, table, year))
            endyear = "{:04d}".format(lastyear + 1)
            if lastyear < 1000:
                Dr2xmlError(
                    "split_last_date year %d derived from DR for variable %s in table %s for year %d does not make "
                    "sense except maybe for paleo runs; please set the right value for 'end_year' in experiment's "
                    "settings file" % (lastyear, sv.label, table, year))
            endmonth = "01"
            endday = "01"
            split_last_date = "{}-{}-{} 00:00:00".format(endyear, endmonth, endday)
    else:
        split_freq = None
    #
    xml_file = DR2XMLElement(tag="file", default_tag="file_output",
                             id="_".join([sv.label, table, grid_label]), output_freq=freq,
                             split_freq=split_freq, split_freq_format=split_freq_format,
                             split_start_offset=split_start_offset, split_end_offset=split_end_offset,
                             split_last_date=split_last_date,
                             grid=grid_description, grid_label=grid_label,
                             nominal_resolution=grid_resolution,
                             variable=sv, context=context, experiment_id=experiment_id,
                             table_id=table)
    #
    for name, value in sorted(list(attributes)):
        xml_file.append(wrv(name, value))
    non_stand_att = get_variable_from_lset_with_default("non_standard_attributes", OrderedDict())
    for name in sorted(list(non_stand_att)):
        xml_file.append(wrv(name, non_stand_att[name]))
    #
    # --------------------------------------------------------------------
    # Build all XIOS auxiliary elements (end_file_defs, field_defs, domain_defs, grid_defs, axis_defs)
    # ---
    # Write XIOS field entry
    # including CF field attributes
    # --------------------------------------------------------------------
    (end_field, target_hgrid_id) = create_xios_aux_elmts_defs(sv, alias, table, field_defs, axis_defs, grid_defs,
                                                              domain_defs, scalar_defs, dummies, context,
                                                              target_hgrid_id, zgrid_id, pingvars)
    xml_file.append(end_field)
    if sv.spatial_shp[0:4] == 'XY-A' or sv.spatial_shp[0:3] == 'S-A':  # includes half-level cases
        # create a field_def entry for surface pressure
        # print "Searching for ps for var %s, freq %s="%(alias,freq)
        sv_psol = get_simplevar("ps", table, sv.frequency)

        if sv_psol:
            # if not sv_psol.cell_measures : sv_psol.cell_measures = "cell measure is not specified in DR "+
            # get_DR_version()
            psol_field, _ = create_xios_aux_elmts_defs(sv_psol,
                                                       get_variable_from_lset_without_default("ping_variables_prefix")
                                                       + "ps", table, field_defs, axis_defs, grid_defs, domain_defs,
                                                       scalar_defs, dummies, context, target_hgrid_id, zgrid_id,
                                                       pingvars)
            xml_file.append(psol_field)
        else:
            logger.warning("Warning: Cannot complement model levels with psol for variable %s and table %s" %
                           (sv.label, sv.frequency))

    #
    names = OrderedDict()
    if sv.spatial_shp in ['XY-A', 'S-A']:
        # add entries for auxiliary variables : ap, ap_bnds, b, b_bnds
        names["ap"] = "vertical coordinate formula term: ap(k)"
        names["ap_bnds"] = "vertical coordinate formula term: ap(k+1/2)"
        names["b"] = "vertical coordinate formula term: b(k)"
        names["b_bnds"] = "vertical coordinate formula term: b(k+1/2)"
    elif sv.spatial_shp in ['XY-AH', 'S-AH']:
        # add entries for auxiliary variables : ap, ap_bnds, b, b_bnds
        names["ahp"] = "vertical coordinate formula term: ap(k)"
        names["ahp_bnds"] = "vertical coordinate formula term: ap(k+1/2)"
        names["bh"] = "vertical coordinate formula term: b(k)"
        names["bh_bnds"] = "vertical coordinate formula term: b(k+1/2)"

    for tab in list(names):
        ping_variable_prefix = get_variable_from_lset_without_default("ping_variables_prefix")
        xml_file.append(DR2XMLElement(tag="field", field_ref="".join([ping_variable_prefix, tab]),
                                      name=tab.replace('h', ''), long_name=names[tab], operation="once", prec="8"))
    actually_written_vars.append((sv.label, sv.long_name, sv.mipTable, sv.frequency, sv.Priority, sv.spatial_shp))
    # Add content to xml_file to out
    out.append(xml_file)


def create_xios_aux_elmts_defs(sv, alias, table, field_defs, axis_defs, grid_defs, domain_defs, scalar_defs, dummies,
                               context, target_hgrid_id, zgrid_id, pingvars):
    """
    Create a field_ref string for a simplified variable object sv (with
    lab prefix for the variable name) and returns it

    Add field definitions for intermediate variables in dict field_defs
    Add axis  definitions for interpolations in dict axis_defs
    Use pingvars as the list of variables actually defined in ping file

    """
    # By convention, field references are built as prefix_<MIP_variable_name>
    # Such references must be fulfilled using a dedicated field_def
    # section implementing the match between legacy model field names
    # and such names, called 'ping section'
    #
    # Identify which 'ping' variable ultimatley matches the requested
    # CMOR variable, based on shapes. This may involve building
    # intermediate variables, in order to  apply corresponding operations

    # The preferred order of operation is : vertical interp (which
    # is time-dependant), time-averaging, horizontal operations (using
    # expr=@this)
    #
    # --------------------------------------------------------------------
    # Build XIOS axis elements (stored in axis_defs)
    # Proceed with vertical interpolation if needed
    # ---
    # Build XIOS auxiliary field elements (stored in field_defs)
    # --------------------------------------------------------------------
    logger = get_logger()
    ssh = sv.spatial_shp
    prefix = get_variable_from_lset_without_default("ping_variables_prefix")

    # The id of the currently most downstream field is last_field_id
    last_field_id = alias

    context_index = get_config_variable("context_index")

    if sv.type in ["dev", ]:
        (source_grid, target_grid) = sv.description.split("|")
        sv.description = None
        if target_grid.lower() in ["none", "native"]:
            target_hgrid_id = ""
        else:
            if target_grid in grid_defs:
                target_grid_def = grid_defs[target_grid]
            elif target_grid in context_index:
                target_grid_def = context_index[target_grid]
            else:
                raise Dr2xmlError("Target horizontal is not defined in grid %s" % target_grid)
            target_hgrid_id = find_rank_xml_subelement(target_grid_def, tag="domain")[0]
            target_hgrid_id = target_grid_def[target_hgrid_id]
            if "id" in target_hgrid_id.attrib:
                target_hgrid_id = target_hgrid_id.attrib["id"]
            else:
                target_hgrid_id = target_hgrid_id.get_attrib("domain_ref")

    if sv.type in ["dev", "perso"]:
        alias_ping = sv.ref_var
    else:
        alias_ping = ping_alias(sv, pingvars)
    if sv.type in ["dev", ] and alias_ping not in context_index:
        field_def = DR2XMLElement(tag="field", id=alias_ping, long_name=sv.long_name, standard_name=sv.stdname,
                                  unit=sv.units, grid_ref=source_grid)
        field_defs[alias_ping] = field_def
        grid_id_in_ping = context_index[source_grid].attrib["id"]
    else:
        grid_id_in_ping = id2gridid(alias_ping, context_index)
    last_grid_id = grid_id_in_ping
    # last_grid_id=None
    #
    grid_with_vertical_interpolation = None

    # translate 'outermost' time cell_methods to Xios 'operation')
    operation, detect_missing, clim = analyze_cell_time_method(sv.cell_methods, sv.label, table)
    #
    # --------------------------------------------------------------------
    # Handle vertical interpolation, both XY-any and Y-P outputs
    # --------------------------------------------------------------------
    #
    # if ssh[0:4] in ['XY-H','XY-P'] or ssh[0:3] == 'Y-P' or \
    # must exclude COSP outputs which are already interpolated to height or P7 levels
    logger.debug("Deal with %s, %s, %s" % (sv.label, prefix + sv.label, sv.label_without_psuffix))
    if (ssh[0:4] == 'XY-P' and ssh != 'XY-P7') or \
            ssh[0:3] == 'Y-P' or (ssh == "XY-perso" and prefix + sv.label not in pingvars) or \
            ((ssh[0:5] == 'XY-na' or ssh[0:4] == 'Y-na') and
             prefix + sv.label not in pingvars and sv.label_without_psuffix != sv.label):
        # TBD check - last case is for singleton
        last_grid_id, last_field_id = process_vertical_interpolation(sv, alias, pingvars, last_grid_id, field_defs,
                                                                     axis_defs, grid_defs, domain_defs, table)
        # If vertical interpolation is done, change the value of those boolean to modify the behaviour of dr2xml
        grid_with_vertical_interpolation = True
    elif ssh in ["XY-HG", ]:
        # Handle interpolation on a height level over the ground
        logger.info("Deal with XY-HG spatial shape for %s,%s" % (sv.label, sv.ref_var))
        last_field_id, last_grid_id = process_levels_over_orog(sv, alias, pingvars, last_grid_id, field_defs, axis_defs,
                                                               grid_defs, domain_defs, scalar_defs, table)

    #
    # --------------------------------------------------------------------
    # Handle the case of singleton dimensions
    # --------------------------------------------------------------------
    #
    if has_singleton(sv) and ssh not in ["XY-HG", ]:
        last_field_id, last_grid_id = process_singleton(sv, last_field_id, pingvars, field_defs, grid_defs, scalar_defs,
                                                        table, grid_id_in_ping)
    #
    # TBD : handle explicitly the case of scalars (global means, shape na-na) :
    # enforce <scalar name="sector" standard_name="region" label="global" >, or , better,
    # remove the XIOS-generated scalar introduced by reduce_domain
    #
    # --------------------------------------------------------------------
    # Handle zonal means
    # --------------------------------------------------------------------
    #
    if ssh[0:2] == 'Y-':  # zonal mean and atm zonal mean on pressure levels
        last_field_id, last_grid_id = \
            process_zonal_mean(last_field_id, last_grid_id, target_hgrid_id, zgrid_id, field_defs, axis_defs, grid_defs,
                               domain_defs, operation, sv.frequency)

    #
    # --------------------------------------------------------------------
    # Build a construct for computing a climatology (if applicable)
    # --------------------------------------------------------------------
    if clim:
        if sv.frequency in ["1hrCM", ]:
            last_field_id, last_grid_id = process_diurnal_cycle(last_field_id, field_defs, grid_defs, axis_defs)
        else:
            raise Dr2xmlError("Cannot handle climatology cell_method for frequency %s and variable %s"
                              % (sv.frequency, sv.label))
    #
    # --------------------------------------------------------------------
    # Create intermediate field_def for enforcing operation upstream
    # --------------------------------------------------------------------
    #
    but_last_field_id = last_field_id
    last_field_id = last_field_id + "_" + operation
    field_defs[last_field_id] = DR2XMLElement(tag="field", id=last_field_id, field_ref=but_last_field_id,
                                              operation=operation)
    #
    # --------------------------------------------------------------------
    # Change horizontal grid if requested
    # --------------------------------------------------------------------
    #
    # This does not apply for a series of shapes
    if target_hgrid_id and ssh not in ["na-na", "TR-na", "TRS-na", "na-A"] and not ssh.startswith("Y-") \
            and not ssh.startswith("YB-"):
        if target_hgrid_id == cfsites_domain_id:
            add_cfsites_in_defs(grid_defs, domain_defs)
        # Apply DR required remapping, either toward cfsites grid or a regular grid
        last_grid_id = change_domain_in_grid(target_hgrid_id, grid_defs, src_grid_id=last_grid_id)
    #
    # --------------------------------------------------------------------
    # Change axes in grid to CMIP6-compliant ones
    # --------------------------------------------------------------------
    #
    last_grid_id = change_axes_in_grid(last_grid_id, grid_defs, axis_defs)
    #
    # --------------------------------------------------------------------
    # Create <field> construct to be inserted in a file_def, which includes re-griding
    # --------------------------------------------------------------------
    if last_grid_id != grid_id_in_ping:
        grid_ref = last_grid_id
    else:
        grid_ref = None
    #
    #
    # --------------------------------------------------------------------
    # Add offset if operation=instant for some specific variables defined in lab_settings
    # --------------------------------------------------------------------
    #
    freq_offset = None
    if operation in ['instant', ]:
        for ts in get_variable_from_lset_with_default('special_timestep_vars', []):
            if sv.label in get_variable_from_lset_without_default('special_timestep_vars', ts):
                xios_freq = cmip6_freq_to_xios_freq(sv.frequency, table)
                # works only if units are different :
                freq_offset = "-".join([xios_freq, ts])
    #
    # TBD : implement DR recommendation for cell_method : The syntax is to append, in brackets,
    # TBD    'interval: *amount* *units*', for example 'area: time: mean (interval: 1 hr)'.
    # TBD    The units must be valid UDUNITS, e.g. day or hr.
    # --------------------------------------------------------------------
    # enforce time average before remapping (when there is one) except if there
    # is an expr, set in ping for the ping variable of that field, and which
    # involves time operation (using @)
    # --------------------------------------------------------------------
    #
    freq_op = None
    expr = None
    if not id_has_expr_with_at(alias, context_index):
        # either no expr, or expr without an @  ->
        # may use @ for optimizing operations order (average before re-gridding)
        if last_grid_id != grid_id_in_ping:
            if operation in ['average', 'instant']:
                # do use @ for optimizing :
                freq_op = longest_possible_period(cmip6_freq_to_xios_freq(sv.frequency, table),
                                                  get_variable_from_lset_with_default("too_long_periods", []))
                # must set freq_op (this souldn't be necessary, but is needed with Xios 1442)
    else:  # field has an expr, with an @
        # Cannot optimize
        if operation in ['instant', ]:
            # must reset expr (if any) if instant, for using arithm. operation defined in ping.
            # this allows that the type of operation applied is really 'instant', and not the one
            # that operands did inherit from ping_file
            expr = "_reset_"
        if operation in ['average', ]:
            warnings_for_optimisation.append(alias)
        freq_op = longest_possible_period(cmip6_freq_to_xios_freq(sv.frequency, table),
                                          get_variable_from_lset_with_default("too_long_periods", []))

    text = None
    if not id_has_expr_with_at(alias, context_index) and last_grid_id != grid_id_in_ping:
        # either no expr, or expr without an @  ->
        # may use @ for optimizing operations order (average before re-gridding)
        if operation in ['average', ]:
            # do use @ for optimizing :
            text = "@{}".format(last_field_id)
        elif operation in ['instant', ] and get_variable_from_lset_with_default("useAtForInstant", False):
            text = "@{}".format(last_field_id)

    #
    # --------------------------------------------------------------------
    # Add Xios variables for creating NetCDF attributes matching CMIP6 specs
    # --------------------------------------------------------------------
    #
    # We override the Xios value for interval_operation because it sets it to
    # the freq_output value with our settings (for complicated reasons)
    if grid_with_vertical_interpolation:
        interval_op = get_variable_from_lset_without_default("vertical_interpolation_sample_freq")
    else:
        source, source_type = get_source_id_and_type()
        grid_choice = get_variable_from_lset_without_default("grid_choice", source)
        interval_op = repr(int(get_variable_from_lset_without_default('sampling_timestep', grid_choice, context))) + \
                      " s"

    rep = DR2XMLElement(tag="field", default_tag="field_output", field_ref=last_field_id, grid_ref=grid_ref,
                        freq_offset=freq_offset, operation=operation,
                        freq_op=freq_op, expr=expr, text=text, variable=sv,
                        interval_operation=interval_op)
    # mpmoine_note: 'missing_value(s)' normalement plus necessaire, a verifier
    # TBS rep.append(wrv("missing_values", sv.missing, num_type="double"))
    #
    return rep, target_hgrid_id


def process_singleton(sv, alias, pingvars, field_defs, grid_defs, scalar_defs, table, last_grid_id):
    """
    Based on singleton dimensions of variable SV, and assuming that this/these dimension(s)
    is/are not yet represented by a scalar Xios construct in corresponding field's grid,
    creates a further field with such a grid, including creating the scalar and
    re-using the domain of original grid

    """
    logger = get_logger()
    # get grid for the variable , before vertical interpo. if any
    # (could rather use last_grid_id and analyze if it has pressure dim)
    context_index = get_config_variable("context_index")
    if sv.type in ["dev", ]:
        alias_ping = sv.label
        if alias_ping in context_index:
            input_grid_id = id2gridid(alias_ping, context_index)
        else:
            input_grid_id = last_grid_id
    elif sv.type in ["perso", ]:
        alias_ping = sv.label
        input_grid_id = id2gridid(alias_ping, context_index)
    else:
        alias_ping = ping_alias(sv, pingvars)
        input_grid_id = id2gridid(alias_ping, context_index)
    input_grid_def = get_grid_def_with_lset(input_grid_id, grid_defs)
    logger.debug("process_singleton : processing %s with grid %s " % (alias, input_grid_id))
    #
    further_field_id = alias
    further_grid_id = input_grid_id
    further_grid_def = input_grid_def
    #
    # for each sv's singleton dimension, create the scalar, add a scalar
    # construct in a further grid, and convert field to a further field
    for sdim in [sv.sdims[dimk] for dimk in sorted(list(sv.sdims)) if is_singleton(sv.sdims[dimk])]:
        #
        # Create a scalar for singleton dimension
        # sdim.label is non-ambiguous id, thanks to the DR, but its value may be
        # ambiguous w.r.t. a dr2xml suffix for interpolating to a single pressure level
        scalar_dict = OrderedDict()
        scalar_id = "Scal" + sdim.label
        # These dimensions are shared by some variables with another sdim with same out_name ('type'):
        if sdim.label in ["typec3pft", "typec4pft"]:
            name = "pfttype"
        else:
            name = sdim.out_name
        #
        if sdim.stdname.strip() != '' and sdim.label != "typewetla":
            standard_name = sdim.stdname
        else:
            standard_name = None
        #
        long_name = sdim.title
        #
        label = None
        prec = None
        value = None
        if sdim.type in ['character', ]:
            label = sdim.label
        else:
            types = {'double': '8', 'float': '4', 'integer': '2'}
            prec = types[sdim.type]
            value = sdim.value
        #
        bounds_value = None
        bounds_name = None
        if sdim.bounds in ["yes", ]:
            try:
                bounds = sdim.boundsValues.split()
                bounds_value = "(0,1)[ {} {} ]".format(bounds[0], bounds[1])
                bounds_name = "{}_bounds".format(sdim.out_name)
            except:
                if sdim.label != "lambda550nm":
                    raise Dr2xmlError("Issue for var %s with dim %s bounds=%s" % (sv.label, sdim.label, bounds))
        #
        axis_type = None
        positive = None
        if isinstance(sdim.axis, six.string_types) and len(sdim.axis) > 0:
            # Space axis, probably Z
            axis_type = sdim.axis
            if sdim.positive:
                positive = sdim.positive
        #
        scalar_def = DR2XMLElement(tag="scalar", id=scalar_id, name=name, standard_name=standard_name,
                                   long_name=long_name, label=label, prec=prec, value=value, bounds=bounds_value,
                                   bounds_name=bounds_name, axis_type=axis_type, positive=positive, unit=sdim.units)
        scalar_defs[scalar_id] = scalar_def
        logger.debug("process_singleton : adding scalar %s" % scalar_def)
        #
        # Create a grid with added (or changed) scalar
        glabel = further_grid_id + "_" + scalar_id
        further_grid_def = add_scalar_in_grid(further_grid_def, glabel, scalar_id, name,
                                              sdim.axis in ["Z", ] and further_grid_def not in ["NATURE_landuse", ])
        logger.debug("process_singleton : adding grid %s" % further_grid_def)
        grid_defs[glabel] = further_grid_def
        further_grid_id = glabel

    # Compare grid definition (in case the input_grid already had correct ref to scalars)
    if further_grid_def != input_grid_def:
        #  create derived_field through an Xios operation (apply all scalars at once)
        further_field_id = alias + "_" + further_grid_id.replace(input_grid_id + '_', '')
        # Must init operation and detect_missing when there is no field ref
        field_def = DR2XMLElement(tag="field", text=alias, id=further_field_id, grid_ref=further_grid_id,
                                  operation="instant", detect_missing_value="true")
        field_defs[further_field_id] = field_def
        logger.debug("process_singleton : adding field %s" % field_def)
    return further_field_id, further_grid_id


def has_singleton(sv):
    """
    Determine if a variable has a singleton dimension.
    :param sv: variable
    :return: boolean indicating whether the variable has a singleton dimension
    """
    rep = any([is_singleton(sv.sdims[k]) for k in sv.sdims])
    return rep


def is_singleton(sdim):
    """
    Based on sdim (dimensions) characteristics, determine if it corresponds to a singleton
    :param sdim: dimensions characteristics
    :return: boolean indicating whether sdim corresponds to a singleton or not
    """
    if sdim.axis == '':
        # Case of non-spatial dims. Singleton only have a 'value' (except Scatratio has a lot (in DR01.00.21))
        return sdim.value != '' and len(sdim.value.strip().split(" ")) == 1
    else:
        # Case of space dimension singletons. Should a 'value' and no 'requested'
        return ((sdim.value != '') and (sdim.requested.strip() == '')) \
               or (sdim.label == "typewetla")  # The latter is a bug in DR01.00.21 : typewetla has no value there


def write_xios_file_def(filename, svars_per_table, year, field_defs, axis_defs, grid_defs, scalar_defs, file_defs,
                        dummies, skipped_vars_per_table, actually_written_vars, context, pingvars=None, enddate=None,
                        attributes=[]):
    """
    Write XIOS file_def.
    """
    logger = get_logger()
    # --------------------------------------------------------------------
    # Start writing XIOS file_def file:
    # file_definition node, including field child-nodes
    # --------------------------------------------------------------------
    # Create xml element for context
    xml_context = DR2XMLElement(tag="context", id=context)
    # Add all comments
    xml_context.append(DR2XMLComment(text="CMIP6 Data Request version {}".format(get_DR_version())))
    xml_context.append(DR2XMLComment(text="CMIP6-CV version {}".format("??")))
    xml_context.append(DR2XMLComment(text="CMIP6_conventions_version {}".format(
        get_config_variable("CMIP6_conventions_version"))))
    xml_context.append(DR2XMLComment(text="dr2xml version {}".format(get_config_variable("version"))))
    xml_context.append(DR2XMLComment(text="\n".join(["Lab_and_model settings", format_dict_for_printing("lset")])))
    xml_context.append(DR2XMLComment(text="\n".join(["Simulation settings", format_dict_for_printing("sset")])))
    xml_context.append(DR2XMLComment(text="Year processed {}".format(year)))
    # Initialize some variables
    domain_defs = OrderedDict()
    foo, sourcetype = get_source_id_and_type()
    # Add xml_file_definition
    xml_file_definition = DR2XMLElement(tag="file_definition", type="one_file", enabled="true")
    # Loop on values to fill the xml element
    for table in sorted(list(svars_per_table)):
        count = OrderedDict()
        for svar in sorted(svars_per_table[table], key=lambda x: (x.label + "_" + table)):
            if get_variable_from_lset_with_default("allow_duplicates_in_same_table", False) \
                    or svar.mipVarLabel not in count:
                if not get_variable_from_lset_with_default("use_cmorvar_label_in_filename", False) \
                        and svar.mipVarLabel in count:
                    form = "If you really want to actually produce both %s and %s in table %s, " + \
                           "you must set 'use_cmorvar_label_in_filename' to True in lab settings"
                    raise Dr2xmlError(form % (svar.label, count[svar.mipVarLabel].label, table))
                count[svar.mipVarLabel] = svar
                for grid in svar.grids:
                    a, hgrid, b, c, d = get_variable_from_lset_without_default('grids', get_grid_choice(), context)
                    check_for_file_input(svar, hgrid, pingvars, field_defs, grid_defs, domain_defs, file_defs)
                    write_xios_file_def_for_svar(svar, year, table, xml_file_definition, field_defs, axis_defs,
                                                 grid_defs, domain_defs, scalar_defs, dummies, skipped_vars_per_table,
                                                 actually_written_vars, context, grid, pingvars, enddate, attributes)
            else:
                logger.warning("Duplicate variable %s,%s in table %s is skipped, preferred is %s" %
                               (svar.label, svar.mipVarLabel, table, count[svar.mipVarLabel].label))
    # Add cfsites if needed
    if cfsites_grid_id in grid_defs:
        xml_file_definition.append(cfsites_input_filedef())
    # Add other file definitions
    for file_def in file_defs:
        xml_file_definition.append(file_defs[file_def])
    xml_context.append(xml_file_definition)
    #
    # --------------------------------------------------------------------
    # End writing XIOS file_def file:
    # field_definition, axis_definition, grid_definition
    # and domain_definition auxilliary nodes
    # --------------------------------------------------------------------
    # Write all domain, axis, field defs needed for these file_defs
    xml_field_definition = DR2XMLElement(tag="field_definition")
    is_reset_field_group = get_variable_from_lset_with_default("nemo_sources_management_policy_master_of_the_world",
                                                               False) and context == 'nemo'
    if is_reset_field_group:
        xml_field_group = DR2XMLElement(tag="field_group", freq_op="_reset_", freq_offset="_reset_")
        for xml_field in list(field_defs):
            xml_field_group.append(field_defs[xml_field])
        xml_field_definition.append(xml_field_group)
    else:
        for xml_field in list(field_defs):
            xml_field_definition.append(field_defs[xml_field])
    xml_context.append(xml_field_definition)
    #
    xml_axis_definition = DR2XMLElement(tag="axis_definition")
    xml_axis_group = DR2XMLElement(tag="axis_group", prec="8")
    for xml_axis in list(axis_defs):
        xml_axis_group.append(axis_defs[xml_axis])
    if False and get_variable_from_lset_with_default('use_union_zoom', False):
        for xml_axis in list(union_axis_defs):
            xml_axis_group.append(union_axis_defs[xml_axis])
    xml_axis_definition.append(xml_axis_group)
    xml_context.append(xml_axis_definition)
    #
    xml_domain_definition = DR2XMLElement(tag="domain_definition")
    xml_domain_group = DR2XMLElement(tag="domain_group", prec="8")
    if get_variable_from_lset_without_default('grid_policy') != "native":
        create_standard_domains(domain_defs)
    for xml_domain in list(domain_defs):
        xml_domain_group.append(domain_defs[xml_domain])
    xml_domain_definition.append(xml_domain_group)
    xml_context.append(xml_domain_definition)
    #
    xml_grid_definition = DR2XMLElement(tag="grid_definition")
    for xml_grid in list(grid_defs):
        xml_grid_definition.append(grid_defs[xml_grid])
    if False and get_variable_from_lset_with_default('use_union_zoom', False):
        for xml_grid in list(union_grid_defs):
            xml_grid_definition.append(union_grid_defs[xml_grid])
    xml_context.append(xml_grid_definition)
    #
    xml_scalar_definition = DR2XMLElement(tag="scalar_definition")
    for xml_scalar in list(scalar_defs):
        xml_scalar_definition.append(scalar_defs[xml_scalar])
    xml_context.append(xml_scalar_definition)
    # Write the xml element to the dedicated file
    create_pretty_xml_doc(xml_element=xml_context, filename=filename)
