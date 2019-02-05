#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Grids general tools.
"""

import re
import xml.etree.ElementTree as ET

from dict_interface import get_variable_from_lset_without_default, get_variable_from_lset_with_default, is_key_in_lset
from config import get_config_variable
from dr_interface import get_collection, get_uid
from utils import dr2xml_error


# Next variable is used to circumvent an Xios 1270 shortcoming. Xios
# should read that value in the datafile. Actually, it did, in some
# earlier version ...
axis_count = 0


def get_grid_def(grid_id, grid_defs):
    context_index = get_config_variable("context_index")
    if grid_id in grid_defs:
        # Simple case : already stored
        grid_def = grid_defs[grid_id]
    else:
        if grid_id in context_index:
            # Grid defined through xml
            grid_def = ET.tostring(context_index[grid_id])
        else:
            raise dr2xml_error("Cannot guess a grid def for %s" % grid_id)
            grid_def = None
    return grid_def


def guess_simple_domain_grid_def(grid_id):
    # dr2xml sometimes must be able to restconstruct the grid def for a grid which has
    # just a domain, from the grid_id, using a regexp with a numbered group that matches
    # domain_name in grid_id. Second item is group number
    regexp = get_variable_from_lset_without_default("simple_domain_grid_regexp")
    domain_id, n = re.subn(regexp[0], r'\%d' % regexp[1], grid_id)
    if n != 1:
        raise dr2xml_error("Cannot identify domain name in grid_id %s using regexp %s" % (grid_id, regexp[0]))
    grid_def = '<grid id="%s" ><domain domain_ref="%s"/></grid>' % (grid_id, domain_id)
    print("Warning: Guess that structure for grid %s is : %s" % (grid_id, grid_def))
    # raise dr2xml_error("Warning: Guess that structure for grid %s is : %s"%(grid_id,grid_def))
    return grid_def


def create_grid_def(grid_defs, axis_def, axis_name, src_grid_id):
    """
    Create and store a grid definition by changing in SRC_GRID_ID grid def
    its only axis member (either def or ref) with AXIS_DEF (where any id
    has been removed)

    Returned grid_id = input grid_id + suffix '_AXIS_NAME'

    raises error if there is not exactly one axis def or reg in input grid

    """
    src_grid_def = get_grid_def(src_grid_id, grid_defs)
    #
    # Retrieve axis key from axis definition string
    axis_key = re.sub(r'.*id= *.([\w_]*).*', r'\1', axis_def.replace('\n', ' '))
    target_grid_id = src_grid_id + "_" + axis_key
    #
    # Remove id= from axis definition string
    axis_def = re.sub(r'id= *.([\w_]*).', '', axis_def)
    #
    # Change only first instance of axis_ref, which is assumed to match the vertical dimension
    # Enforce axis_name in axis_def :  TBD
    (target_grid_def, count) = re.subn('<axis[^\>]*>', axis_def, src_grid_def, 1)
    if count != 1:
        raise dr2xml_error("Fatal: cannot find an axis ref in grid %s : %s " % (src_grid_id, src_grid_def))
    target_grid_def = re.sub('grid id= *.([\w_])*.', 'grid id="%s"' % target_grid_id, target_grid_def)
    grid_defs[target_grid_id] = target_grid_def
    return target_grid_id


def create_axis_def(sdim, axis_defs, field_defs):
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
    prefix = get_variable_from_lset_without_default("ping_variables_prefix")
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
        rep = '<axis id="%s" ' % sdim.label
        if sdim.positive not in [None, ""]:
            rep += 'positive="%s" ' % sdim.positive
        if n_glo > 1:
            # Case of a non-degenerated vertical dimension (not a singleton)
            rep += 'n_glo="%g" ' % n_glo
            rep += 'value="(0,%g)[ %s ]"' % (n_glo - 1, sdim.requested)
        else:
            if n_glo != 1:
                print "Warning: axis for %s is singleton but has %d values" % (sdim.label, n_glo)
                return None
            # Singleton case (degenerated vertical dimension)
            rep += 'n_glo="%g" ' % n_glo
            rep += 'value="(0,0)[ %s ]"' % sdim.value
        rep += ' name="%s"' % sdim.out_name
        rep += ' standard_name="%s"' % sdim.stdname
        rep += ' long_name="%s"' % sdim.long_name
        rep += ' unit="%s"' % sdim.units
        rep += '>'
        if sdim.stdname == "air_pressure":
            coordname = prefix + "pfull"
        if sdim.stdname == "altitude":
            coordname = prefix + "zg"
        #
        # Create an intemediate field for coordinate , just adding time sampling
        operation = get_variable_from_lset_with_default("vertical_interpolation_operation", "instant")
        coordname_with_op = coordname + "_" + operation  # e.g. CMIP6_pfull_instant
        coorddef_op = '<field id="%-25s field_ref="%-25s operation="%s" detect_missing_value="true"/>' \
                      % (coordname_with_op + '"', coordname + '"', operation)
        field_defs[coordname_with_op] = coorddef_op
        #
        # Create and store a definition for time-sampled field for the vertical coordinate
        vert_frequency = get_variable_from_lset_without_default("vertical_interpolation_sample_freq")
        coordname_sampled = coordname_with_op + "_sampled_" + vert_frequency  # e.g. CMIP6_pfull_instant_sampled_3h
        rep += '<interpolate_axis type="polynomial" order="1"'
        rep += ' coordinate="%s"/>\n\t</axis>' % coordname_sampled
        # Store definition for the new axis
        axis_defs[sdim.label] = rep
        coorddef = '<field id="%-25s field_ref="%-25s freq_op="%-10s detect_missing_value="true"> @%s</field>' \
                   % (coordname_sampled + '"', coordname_with_op + '"', vert_frequency + '"', coordname)
        field_defs[coordname_sampled] = coorddef
    else:  # zoom case
        # Axis is subset of another, write it as a zoom_axis
        rep = '<axis id="%s"' % sdim.zoom_label
        rep += ' axis_ref="%s" name="plev"' % sdim.is_zoom_of
        rep += ' axis_type="%s">' % sdim.axis
        rep += '\t<zoom_axis index="(0,%g)[ ' % (n_glo - 1)
        values = re.sub(r'.*\[ *(.*) *\].*', r'\1', axis_defs[sdim.is_zoom_of])
        values = values.split("\n")[0]
        union_vals = values.strip(" ").split()
        union_vals_num = [float(v) for v in union_vals]
        for val in glo_list_num:
            rep += ' %g' % union_vals_num.index(val)
        rep += ' ]"/>'
        rep += '</axis>'
        # Store definition for the new axis
        axis_defs[sdim.zoom_label] = rep
    return rep


def change_domain_in_grid(domain_id, grid_defs, ping_alias=None, src_grid_id=None, turn_into_axis=False,
                          printout=False):
    """
    Provided with a grid id SRC_GRID_ID or alertnatively a variable name (ALIAS),
    (SRC_GRID_STRING)
     - creates ans stores a grid_definition where the domain_id has been changed to DOMAIN_ID
    -  returns its id, which is
    """
    if src_grid_id is None:
        raise dr2xml_error("deprecated")
    else:
        src_grid_string = get_grid_def_with_lset(src_grid_id, grid_defs)
    target_grid_id = src_grid_id + "_" + domain_id
    # Change domain
    domain_or_axis = "domain"
    axis_name = ""
    if turn_into_axis:
        domain_or_axis = "axis"
        axis_name = ' name="lat"'
    # sequence below was too permissive re. assumption that all grid definition use refs rather than ids
    # (target_grid_string,count)=re.subn('domain *id= *.([\w_])*.','%s id="%s" %s'% \
    # (domain_or_axis,domain_id,axis_name), src_grid_string,1)
    # if count != 1 :
    (target_grid_string, count) = re.subn('domain *domain_ref= *.([\w_])*.',
                                          '%s %s_ref="%s" %s' % (domain_or_axis, domain_or_axis, domain_id, axis_name),
                                          src_grid_string, 1)
    if count != 1:
        raise dr2xml_error("Fatal: cannot find a domain to replace by %s"
                           "in src_grid_string %s, count=%d " % (domain_id, src_grid_string, count))
    target_grid_string = re.sub('grid *id= *.([\w_])*.', 'grid id="%s"' % target_grid_id, target_grid_string)
    grid_defs[target_grid_id] = target_grid_string
    # print "target_grid_id=%s : %s"%(target_grid_id,target_grid_string)
    return target_grid_id


def get_grid_def_with_lset(grid_id, grid_defs):
    try:
        grid_def = get_grid_def(grid_id, grid_defs)
    except:
        grid_def = guess_simple_domain_grid_def(grid_id)
        grid_defs[grid_id] = grid_def
    return grid_def


def change_axes_in_grid(grid_id, grid_defs, axis_defs):
    """
    Create a new grid based on GRID_ID def by changing all its axis references to newly created
    axis which implement CMIP6 axis attributes
    Works only on axes which id match the labels of DR dimensions (e.g. sdepth, landUSe ...)
    Stores the definitions in GRID_DEFS and AXIS_DEFS
    Returns the new grid_id
    """
    global axis_count
    grid_def = get_grid_def(grid_id, grid_defs)
    grid_el = ET.fromstring(grid_def)
    output_grid_id = grid_id
    axes_to_change = []
    # print "in change_axis for %s "%(grid_id)

    # Get settings info about axes normalization
    aliases = get_variable_from_lset_with_default('non_standard_axes', dict())

    # Add cases where dim name 'sector' should be used,if needed
    # sectors = dims which have type charcter and are not scalar
    if is_key_in_lset('sectors'):
        sectors = get_variable_from_lset_without_default('sectors')
    else:
        sectors = [dim.label for dim in get_collection('grids').items if dim.type == 'character' and dim.value == '']
    if 'typewetla' in sectors:
        sectors.remove('typewetla')  # Error in DR 01.00.21
    # print "sectors=",sectors
    for sector in sectors:
        found = False
        for aid in aliases:
            if aliases[aid] == sector:
                found = True
                continue
            if type(aliases[aid]) == type(()) and aliases[aid][0] == sector:
                found = True
                continue
        if not found:
            # print "\nadding sector : %s"%sector
            aliases[sector] = sector

    for sub in grid_el:
        if sub.tag == 'axis':
            # print "checking grid %s"%grid_def
            if 'axis_ref' not in sub.attrib:
                # Definitely don't want to change an unnamed axis. Such an axis is
                # generated by vertical interpolation
                if any([ssub.tag == 'interpolate_axis' for ssub in sub]):
                    continue
                else:
                    print "Cannot normalize an axis in grid %s : no axis_ref for axis %s" % (grid_id, ET.tostring(sub))
                    continue
                    # raise dr2xml_error("Grid %s has an axis without axis_ref : %s"%(grid_id,grid_def))
            axis_ref = sub.attrib['axis_ref']
            #

            # Just quit if axis doesn't have to be processed
            if axis_ref not in aliases.keys():
                # print "for grid ",grid_id,"axis ",axis_ref, " is not in aliases"
                continue
            #
            dr_axis_id = aliases[axis_ref]
            alt_labels = None
            if type(dr_axis_id) == type(()):
                dr_axis_id, alt_labels = dr_axis_id
            dr_axis_id = dr_axis_id.replace('axis_', '')  # For toy_cnrmcm, atmosphere part
            # print ">>> axis_ref=%s, dr_axis_id=%s,alt_labels=%s"%(axis_ref,dr_axis_id,alt_labels),aliases[axis_ref]
            #
            dim_id = 'dim:%s' % dr_axis_id
            # print "in change_axis for %s %s"%(grid_id,dim_id)
            if dim_id not in get_uid():  # This should be a dimension !
                raise dr2xml_error("Value %s in 'non_standard_axes' is not a DR dimension id" % dr_axis_id)
            dim = get_uid(dim_id)
            # We don't process scalars here
            if dim.value == '' or dim.label == "scatratio":
                axis_id, axis_name = create_axis_from_dim(dim, alt_labels, axis_ref, axis_defs)
                # cannot use ET library which does not guarantee the ordering of axes
                axes_to_change.append((axis_ref, axis_id, axis_name))
                output_grid_id += "_" + dim.label
            else:
                raise dr2xml_error("Dimension %s is scalar and shouldn't be quoted in 'non_standard_axes'" % dr_axis_id)
    if len(axes_to_change) == 0:
        return grid_id
    for old, new, name in axes_to_change:
        axis_count += 1
        grid_def = re.sub("< *axis[^>]*axis_ref= *.%s. *[^>]*>" % old,
                          '<axis axis_ref="%s" name="%s" id="ref_to_%s_%d"/>' % (new, name, new, axis_count), grid_def)
    grid_def = re.sub("< *grid([^>]*)id= *.%s.( *[^>]*)>" % grid_id,
                      r'<grid\1id="%s"\2>' % output_grid_id, grid_def)
    grid_defs[output_grid_id] = grid_def
    return output_grid_id


def create_axis_from_dim(dim, labels, axis_ref, axis_defs):
    """
    Create an axis definition by translating all DR dimension attributes to XIos
    constructs generating CMIP6 requested attributes
    """
    axis_id = "DR_" + dim.label + "_" + axis_ref
    if dim.type == "character":
        axis_name = "sector"
    else:
        axis_name = dim.altLabel
    if axis_id in axis_defs:
        return axis_id, axis_name

    rep = '<axis id="%s" name="%s" axis_ref="%s"' % (axis_id, axis_name, axis_ref)
    if type(dim.standardName) == type(""):
        rep += ' standard_name="%s"' % dim.standardName
    rep += ' long_name="%s"' % dim.title
    #
    if dim.type == "double":
        rep += ' prec="8"'
    elif dim.type in ["integer", "int"]:
        rep += ' prec="2"'
    elif dim.type == "float":
        rep += ' prec="4"'
    #
    if dim.units != '':
        rep += ' unit="%s"' % dim.units
    if dim.type != "character":
        if dim.requested != "":
            nb = len(dim.requested.split())
            rep += ' value="(0,%d)[ ' % nb + dim.requested + ' ]"'
        if type(dim.boundsRequested) == type([]):
            vals = [" %s" % v for v in dim.boundsRequested]
            valsr = reduce(lambda x, y: x + y, vals)
            rep += ' bounds="(0,1)x(0,%d)[ ' % (nb - 1) + valsr + ' ]"'
    else:
        rep += ' dim_name="%s" ' % dim.altLabel
        if labels is None:
            labels = dim.requested
        if dim.label == "oline" and get_variable_from_lset_with_default('add_Gibraltar', False):
            labels += " gibraltar"
        labels = labels.replace(', ', ' ').replace(',', ' ')
        length = len(labels.split())
        # print 'labels=',labels.split()
        strings = " "
        for s in labels.split():
            strings += "%s " % s
        if length > 0:
            rep += ' label="(0,%d)[ %s ]"' % (length - 1, strings)
    rep += "/>"
    axis_defs[axis_id] = rep
    # print "new DR_axis :  %s "%rep
    return axis_id, axis_name


def isVertDim(sdim):
    """
    Returns True if dim represents a dimension for which we want
    an Xios interpolation.
    For now, a very simple logics for interpolated vertical
    dimension identification:
    """
    # SS : p840, p220 sont des couches de pression.  On les detecte par l'attribut value
    # test=(sdim.stdname=='air_pressure' or sdim.stdname=='altitude') and (sdim.value == "")
    test = (sdim.axis == 'Z')
    return test


def scalar_vertical_dimension(sv):
    if 'cids' in sv.struct.__dict__:
        cid = get_uid(sv.struct.cids[0])
        if cid.axis == 'Z':
            return cid.altLabel
    return None
