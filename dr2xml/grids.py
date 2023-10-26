#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Grids general tools.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from functools import reduce

import re

# Utilities
from .settings_interface import get_settings_values
from .utils import Dr2xmlError

# Logger
from logger import get_logger

# Global variables and configuration tools
from .config import get_config_variable, add_value_in_dict_config_variable

# Interface to Data Request
from .dr_interface import get_data_request
# Interface to xml tools
from .xml_interface import find_rank_xml_subelement, DR2XMLElement


# Next variable is used to circumvent an Xios 1270 shortcoming. Xios
# should read that value in the datafile. Actually, it did, in some
# earlier version ...
axis_count = 0


def get_grid_def(grid_id):
    """
    Get the grid definition corresponding to grid_id from the context_index or the list of grid definitions.
    """
    context_index = get_config_variable("context_index")
    grid_defs = get_config_variable("grid_defs")
    if grid_id in grid_defs:
        # Simple case : already stored
        grid_def = grid_defs[grid_id]
    elif grid_id in context_index:
        # Grid defined through xml
        grid_def = context_index[grid_id]
    else:
        raise Dr2xmlError("Cannot guess a grid def for %s" % grid_id)
    return grid_def


def guess_simple_domain_grid_def(grid_id):
    """
    dr2xml sometimes must be able to reconstruct the grid def for a grid which has
    just a domain, from the grid_id, using a regexp with a numbered group that matches
    domain_name in grid_id. Second item is group number
    """
    logger = get_logger()
    regexp = get_settings_values("internal", "simple_domain_grid_regexp")
    domain_id, n = re.subn(regexp[0], r'\%d' % regexp[1], grid_id)
    if n != 1:
        raise Dr2xmlError("Cannot identify domain name in grid_id %s using regexp %s" % (grid_id, regexp[0]))
    grid_def = DR2XMLElement(tag="grid", id=grid_id)
    grid_def.append(DR2XMLElement(tag="domain", domain_ref=domain_id))
    logger.warning("Warning: Guess that structure for grid %s is : %s" % (grid_id, grid_def))
    # raise dr2xml_error("Warning: Guess that structure for grid %s is : %s"%(grid_id,grid_def))
    return grid_def


def create_grid_def(axis_def, axis_name, src_grid_id):
    """
    Create and store a grid definition by changing in SRC_GRID_ID grid def
    its only axis member (either def or ref) with AXIS_DEF (where any id
    has been removed)

    Returned grid_id = input grid_id + suffix '_AXIS_NAME'

    raises error if there is not exactly one axis def or reg in input grid

    """
    src_grid_def = get_grid_def(src_grid_id)
    #
    # Retrieve axis key and remove id= from axis definition
    xios_version = get_settings_values("internal")["xios_version"]
    if xios_version <= 2:
        new_axis_def = axis_def.copy()
        axis_key = new_axis_def.attrib.pop("id")
    else:
        axis_key = axis_def.attrib["id"]
        new_axis_def = DR2XMLElement(tag="axis", axis_ref=axis_key)
    target_grid_id = src_grid_id + "_" + axis_key
    #
    # Change only first instance of axis_ref, which is assumed to match the vertical dimension
    # Enforce axis_name in axis_def :  TBD
    target_grid_def = src_grid_def.copy()
    axis_rank = find_rank_xml_subelement(target_grid_def, tag="axis")
    if len(axis_rank) > 0:
        target_grid_def[axis_rank[0]] = new_axis_def
    else:
        raise Dr2xmlError("Fatal: cannot find an axis ref in grid %s : %s " % (src_grid_id, target_grid_def))
    target_grid_def.attrib["id"] = target_grid_id
    add_value_in_dict_config_variable(variable="grid_defs", key=target_grid_id, value=target_grid_def)
    return target_grid_id


def create_axis_def(sdim):
    """

    From a simplified Dim object SDIM representing a vertical dimension,
    creates and stores an Xios axis definition in AXIS_DEFS

    If the dimension implies vertical interpolation (on air_pressure
    or altitude levels), creates and stores (in FIELD_DEFS) two
    intermediate fields for the sampling of that coordinate field at
    the vert_frequency and with the type of operation indicated by LSET

    If the dimension is a zoom of another one, analyzes its 'requested'
    field against the list of values declared for the other one, for
    defining the zoom in XIOS syntax

    """
    logger = get_logger()
    internal_dict = get_settings_values("internal")
    prefix = internal_dict["ping_variables_prefix"]
    # nbre de valeurs de l'axe determine aussi si on est en dim singleton
    if sdim.requested:
        glo_list = sdim.requested.strip(" ").split()
    else:
        glo_list = sdim.value.strip(" ").split()
    glo_list_num = [float(v) for v in glo_list]
    glo_list_num.sort(reverse=True)
    n_glo = len(glo_list)

    if not sdim.is_zoom_of:  # pure interpolation
        # Axis is not a zoom of another, write axis_def normally (with value, interpolate_axis,etc.)
        if n_glo > 1:
            # Case of a non-degenerated vertical dimension (not a singleton)
            value = "(0,{})[ {} ]".format(n_glo - 1, sdim.requested)
        elif n_glo != 1:
            logger.warning("Warning: axis for %s is singleton but has %d values" % (sdim.label, n_glo))
            return None
        else:
            # Singleton case (degenerated vertical dimension)
            value = '(0,0)[ {} ]'.format(sdim.value)
        axis_xml = DR2XMLElement(tag="axis", id=sdim.label, positive=sdim.positive, n_glo=str(n_glo), value=value,
                                 name=sdim.out_name, standard_name=sdim.stdname, long_name=sdim.long_name,
                                 unit=sdim.units, axis_type=sdim.axis)
        # Define some other values
        if sdim.stdname in ["air_pressure", ]:
            coordname = prefix + "pfull"
        elif sdim.stdname in ["altitude", ]:
            coordname = prefix + "zg"
        else:
            coordname = prefix + sdim.label
        if coordname not in get_config_variable("pingvars"):
            raise Dr2xmlError("Could not find coordinate variable %s in pingfile." % coordname)
        #
        # Create an intermediate field for coordinate , just adding time sampling
        operation = internal_dict["vertical_interpolation_operation"]
        coordname_with_op = coordname + "_" + operation  # e.g. CMIP6_pfull_instant
        coorddef_op = DR2XMLElement(tag="field", id=coordname_with_op, field_ref=coordname, detect_missing_value="true",
                                    operation=operation)
        add_value_in_dict_config_variable(variable="field_defs", key=coordname_with_op, value=coorddef_op)
        #
        # Create and store a definition for time-sampled field for the vertical coordinate
        vert_frequency = internal_dict["vertical_interpolation_sample_freq"]
        coordname_sampled = coordname_with_op + "_sampled_" + vert_frequency  # e.g. CMIP6_pfull_instant_sampled_3h
        axis_xml.append(DR2XMLElement(tag="interpolate_axis", type="polynomial", order="1",
                                      coordinate=coordname_sampled))
        # Store definition for the new axis
        add_value_in_dict_config_variable(variable="axis_defs", key=sdim.label, value=axis_xml)
        coorddef = DR2XMLElement(tag="field", text="@{}".format(coordname), id=coordname_sampled,
                                 field_ref=coordname_with_op, freq_op=vert_frequency, detect_missing_value="true")
        add_value_in_dict_config_variable(variable="field_defs", key=coordname_sampled, value=coorddef)
    else:  # zoom case
        # Axis is subset of another, write it as a zoom_axis
        axis_xml = DR2XMLElement(tag="axis", id=sdim.zoom_label, axis_ref=sdim.zoom_of, name="plev",
                                 axis_type=sdim.axis)
        values = get_config_variable("axis_defs", keys=sdim.is_zoom_of).attrib["value"]
        values = re.sub(r'.*\[ *(.*) *\].*', r'\1', values)
        values = values.split("\n")[0]
        union_vals = values.strip(" ").split()
        union_vals_num = [float(v) for v in union_vals]
        index_values = "(0, {})[ {} ]".format(n_glo - 1,
                                              " ".join([str(union_vals_num.index(val)) for val in glo_list_num]))
        axis_xml.append(DR2XMLElement(tag="zoom_axis", index=index_values))
        # Store definition for the new axis
        add_value_in_dict_config_variable(variable="axis_defs", key=sdim.zoom_label, value=axis_xml)
    return axis_xml


def change_domain_in_grid(domain_id, src_grid_id=None, turn_into_axis=False):
    """
    Provided with a grid id SRC_GRID_ID or alternatively a variable name (ALIAS),
    (SRC_GRID)
     - creates and stores a grid_definition where the domain_id has been changed to DOMAIN_ID
    -  returns its id, which is
    """
    if src_grid_id is None:
        raise Dr2xmlError("deprecated")
    else:
        src_grid = get_grid_def_with_lset(src_grid_id)
        # Find the domain rank in the grid definition
        rank = find_rank_xml_subelement(src_grid, tag="domain", domain_ref=None)
        if len(rank) > 0:
            rank = rank[0]
        else:
            raise Dr2xmlError("Fatal: cannot find a domain to replace by %s in src_grid_string %s" % (domain_id,
                                                                                                      src_grid))
        # Check that there is a change to be done (domain->axis or change in domain_ref)
        if not turn_into_axis and src_grid[rank].attrib["domain_ref"] in [domain_id, ]:
            return src_grid_id
        else:
            target_grid_id = src_grid_id + "_" + domain_id
            # print("<<<DEBUG>>> src_grid_id, domain_id, target_grid_id", src_grid_id, domain_id, target_grid_id)
            # sequence below was too permissive re. assumption that all grid definition use refs rather than ids
            # (target_grid_string,count)=re.subn('domain *id= *.([\w_])*.','%s id="%s" %s'% \
            # (domain_or_axis,domain_id,axis_name), src_grid_string,1)
            # if count != 1 :
            target_grid_xml = src_grid.copy()
            if turn_into_axis:
                target_grid_xml[rank].tag = "axis"
                del target_grid_xml[rank].attrib["domain_ref"]
                target_grid_xml[rank].attrib["axis_ref"] = domain_id
                target_grid_xml[rank].attrib["name"] = "lat"
            else:
                target_grid_xml[rank].attrib["domain_ref"] = domain_id
            target_grid_xml.attrib["id"] = target_grid_id
            add_value_in_dict_config_variable(variable="grid_defs", key=target_grid_id, value=target_grid_xml)
            # print "target_grid_id=%s : %s"%(target_grid_id,target_grid_string)
            return target_grid_id


def get_grid_def_with_lset(grid_id):
    """
    Get the grid definition corresponding to grid_id.
    """
    try:
        grid_def = get_grid_def(grid_id)
    except:
        grid_def = guess_simple_domain_grid_def(grid_id)
        add_value_in_dict_config_variable(variable="grid_defs", key=grid_id, value=grid_def)
    return grid_def


def change_axes_in_grid(grid_id):
    """
    Create a new grid based on GRID_ID def by changing all its axis references to newly created
    axis which implement CMIP6 axis attributes
    Works only on axes which id match the labels of DR dimensions (e.g. sdepth, landUSe ...)
    Stores the definitions in GRID_DEFS and AXIS_DEFS
    Returns the new grid_id
    """
    internal_dict = get_settings_values("internal")
    data_request = get_data_request()
    global axis_count
    logger = get_logger()
    grid_def_init = get_grid_def(grid_id)
    grid_def = grid_def_init.copy()
    output_grid_id = grid_id
    # print "in change_axis for %s "%(grid_id)

    # Get settings info about axes normalization
    aliases = internal_dict['non_standard_axes']

    # Add cases where dim name 'sector' should be used,if needed
    # sectors = dims which have type character and are not scalar
    sectors = internal_dict.get("sectors", data_request.get_sectors_list())
    for sector in sectors:
        if not any([sector in [aliases[aid], aliases[aid][0]] for aid in aliases]):
            # print "\nadding sector : %s"%sector
            aliases[sector] = sector

    changed_done = False
    rank_sub_axis = find_rank_xml_subelement(grid_def, tag="axis")
    for i in rank_sub_axis:
        # print "checking grid %s"%grid_def
        sub = grid_def[i]
        if 'axis_ref' not in sub.attrib:
            # Definitely don't want to change an unnamed axis. Such an axis is
            # generated by vertical interpolation
            if not any([ssub.tag in ['interpolate_axis', ] for ssub in sub]):
                logger.warning("Cannot normalize an axis in grid %s: no axis_ref for axis %s" % (grid_id, sub))
        else:
            axis_ref = sub.attrib['axis_ref']
            # Just quit if axis doesn't have to be processed
            if axis_ref in aliases:
                dr_axis_id = aliases[axis_ref]
                if isinstance(dr_axis_id, tuple):
                    dr_axis_id, alt_labels = dr_axis_id
                else:
                    alt_labels = None
                dr_axis_id = dr_axis_id.replace('axis_', '')  # For toy_cnrmcm, atmosphere part
                #
                dim_id = 'dim:{}'.format(dr_axis_id)
                # print "in change_axis for %s %s"%(grid_id,dim_id)
                # dim_id should be a dimension !
                dim = data_request.get_element_uid(dim_id, elt_type="dim",
                                                   error_msg="Value %s in 'non_standard_axes' is not a DR dimension id"
                                                             % dr_axis_id)
                # We don't process scalars here
                if dim.value in ['', ] or dim.label in ["scatratio", ]:
                    axis_id, axis_name = create_axis_from_dim(dim, alt_labels, axis_ref)
                    # cannot use ET library which does not guarantee the ordering of axes
                    changed_done = True
                    axis_count += 1
                    grid_def[i].attrib = dict(axis_ref=axis_id, name=axis_name,
                                              id="ref_to_{}_{}".format(axis_id, axis_count))
                    output_grid_id += "_" + dim.label
                else:
                    raise Dr2xmlError("Dimension %s is scalar and shouldn't be quoted in 'non_standard_axes'" %
                                      dr_axis_id)
    if not changed_done:
        return grid_id
    else:
        grid_def.attrib["id"] = output_grid_id
        add_value_in_dict_config_variable(variable="grid_defs", key=output_grid_id, value=grid_def)
        return output_grid_id


def create_axis_from_dim(dim, labels, axis_ref):
    """
    Create an axis definition by translating all DR dimension attributes to XIos
    constructs generating CMIP6 requested attributes
    """
    axis_id = "DR_" + dim.label + "_" + axis_ref
    axis_name = dim.name
    if axis_id in get_config_variable("axis_defs"):
        return axis_id, axis_name
    #
    value = None
    bounds = None
    dim_name = None
    label = None
    if dim.type not in ["character", ]:
        if dim.requested not in ['', ]:
            nb = len(dim.requested.split())
            value = "(0,{})[ {} ]".format(nb, dim.requested.strip())
            if isinstance(dim.boundsRequested, list):
                vals = " ".join([str(v) for v in dim.boundsRequested])
                valsr = reduce(lambda x, y: x + y, vals)
                bounds = "(0,1)x(0,{})[ {} ]".format(nb - 1, valsr)
    else:
        dim_name = dim.altLabel
        if labels is None:
            labels = dim.requested
        if dim.label in ["oline", ] and get_settings_values("internal", 'add_Gibraltar'):
            labels += " gibraltar"
        labels = labels.replace(', ', ' ').replace(',', ' ')
        length = len(labels.split())
        # print 'labels=',labels.split()
        strings = " "
        for s in labels.split():
            strings += "%s " % s
        if length > 0:
            label = "(0,{})[ {} ]".format(length - 1, strings)
    rep = DR2XMLElement(tag="axis", id=axis_id, name=axis_name, axis_ref=axis_ref, standard_name=dim.stdname,
                        long_name=dim.title, prec=dim.type, unit=dim.units, value=value, bounds=bounds,
                        dim_name=dim_name, label=label, axis_type=dim.axis)
    add_value_in_dict_config_variable(variable="axis_defs", key=axis_id, value=rep)
    # print "new DR_axis :  %s "%rep
    return axis_id, axis_name


def is_vert_dim(sdim):
    """
    Returns True if dim represents a dimension for which we want
    an Xios interpolation.
    For now, a very simple logics for interpolated vertical
    dimension identification:
    """
    # SS : p840, p220 sont des couches de pression.  On les detecte par l'attribut value
    # test=(sdim.stdname=='air_pressure' or sdim.stdname=='altitude') and (sdim.value == "")
    test = (sdim.axis in ['Z', ])
    return test


def create_standard_domains(domain_defs):
    """
    Add to dictionary domain_defs the Xios string representation for DR-standard horizontal grids, such as '1deg'

    """
    # Next definition is just for letting the workflow work when using option dummy='include'
    # Actually, ping_files for production run at CNRM do not activate variables on that grid (IceSheet vars)
    domain_defs['25km'] = create_standard_domain('25km', 1440, 720)
    domain_defs['50km'] = create_standard_domain('50km', 720, 360)
    domain_defs['100km'] = create_standard_domain('100km', 360, 180)
    domain_defs['1deg'] = create_standard_domain('1deg', 360, 180)
    domain_defs['2deg'] = create_standard_domain('2deg', 180, 90)


def create_standard_domain(resol, ni, nj):
    """
    Create a xml like string corresponding to the domain using resol, ni and nj.
    """
    rep = DR2XMLElement(tag="domain", id="CMIP6_{}".format(resol), ni_glo=str(ni), nj_glo=str(nj), type="rectilinear",
                        prec="8")
    rep.append(DR2XMLElement(tag="generate_rectilinear_domain"))
    rep.append(DR2XMLElement(tag="interpolate_domain", order="1", renormalize="true", mode="read_or_compute",
                             write_weight="true"))
    return rep


def add_scalar_in_grid(gridin_def, gridout_id, scalar_id, scalar_name, remove_axis, change_scalar=True):
    """
    Returns a grid_definition with id GRIDOUT_ID from an input grid definition
    GRIDIN_DEF, by adding a reference to scalar SCALAR_ID

    If CHANGE_SCALAR is True and GRIDIN_DEF has an axis with an extract_axis child,
    remove it (because it is assumed to be a less well-defined proxy for the DR scalar

    If such a reference is already included in that grid definition, just return
    input def

    if REMOVE_AXIS is True, if GRIDIN_DEF already includes an axis, remove it for output grid

    Note : name of input_grid is not changed in output_grid

    """
    rep = gridin_def.copy()
    rank_scalar = find_rank_xml_subelement(rep, tag="scalar", scalar_ref=[scalar_id, ])
    if len(rank_scalar) > 0:
        return rep
    else:
        # TBD : in change_scalar : discard extract_axis only if really relevant (get the right axis)
        # TBD : in change_scalar : preserve ordering of domains/axes...
        if change_scalar:
            rank_scalar = find_rank_xml_subelement(rep, tag="scalar")
            rank_scalar.reverse()
            for i in rank_scalar:
                if len(find_rank_xml_subelement(rep[i], tag="extract_axis")) > 0:
                    del rep[i]
        if "id" in rep.attrib:
            rep.attrib["id"] = gridout_id
            rep.append(DR2XMLElement(tag="scalar", scalar_ref=scalar_id, name=scalar_name))
        else:
            raise Dr2xmlError("No way to add scalar '%s' in grid '%s'" % (scalar_id, gridin_def))
        # Remove any axis if asked for
        if remove_axis:
            for i in find_rank_xml_subelement(rep, tag="axis"):
                del rep[i]
        return rep
