#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Miscellaneous functions
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict
from io import open

from six import string_types

from logger import get_logger
from . import get_config_variable

from .cfsites import cfsites_grid_id, add_cfsites_in_defs, cfsites_domain_id
from .dr_interface import get_data_request
from .grids import change_domain_in_grid
from .pingfiles_interface import read_special_fields_defs, highest_rank, copy_obj_from_DX_file
from .utils import Dr2xmlError


def request_item_include(ri, var_label, freq):
    """
    test if a variable is requested by a requestItem at a given freq
    """
    data_request = get_data_request()
    var_group = data_request.get_element_uid(data_request.get_element_uid(ri.rlid).refid)
    req_vars = data_request.get_request_by_id_by_sect(var_group.uid, 'requestVar')
    cm_vars = [data_request.get_element_uid(data_request.get_element_uid(reqvar).vid, elt_type="variable")
               for reqvar in req_vars]
    return any([cmv.label == var_label and cmv.frequency == freq for cmv in cm_vars])


def realm_is_processed(realm, source_type):
    """
    Tells if a realm is definitely not processed by a source type

    list of source-types : AGCM BGC AER CHEM LAND OGCM AOGCM
    list of known realms : 'seaIce', '', 'land', 'atmos atmosChem', 'landIce', 'ocean seaIce',
                           'landIce land', 'ocean', 'atmosChem', 'seaIce ocean', 'atmos',
                           'aerosol', 'atmos land', 'land landIce', 'ocnBgChem'
    """
    components = source_type.split(" ")
    rep = True
    #
    if realm == "atmosChem" and 'CHEM' not in components:
        return False
    if realm == "aerosol" and 'AER' not in components:
        return False
    if realm == "ocnBgChem" and 'BGC' not in components:
        return False
    #
    with_ocean = ('OGCM' in components or 'AOGCM' in components)
    if 'seaIce' in realm and not with_ocean:
        return False
    if 'ocean' in realm and not with_ocean:
        return False
    #
    with_atmos = ('AGCM' in components or 'AOGCM' in components)
    if 'atmos' in realm and not with_atmos:
        return False
    if 'atmosChem' in realm and not with_atmos:
        return False
    if realm == '' and not with_atmos:  # In DR 01.00.15 : some atmos variables have realm=''
        return False
    #
    with_land = with_atmos or ('LAND' in components)
    if 'land' in realm and not with_land:
        return False
    #
    return rep


def create_output_grid(ssh, target_hgrid_id, margs):
    """
    Build output grid (stored in grid_defs) by analyzing the spatial shape
    Including horizontal operations. Can include horiz re-gridding specification
    """
    grid_ref = None

    # Compute domain name, define it if needed
    if ssh[0:2] in ['Y-', ]:  # zonal mean and atm zonal mean on pressure levels
        # Grid normally has already been created upstream
        grid_ref = margs['src_grid_id']
    elif ssh in ['S-na', ]:
        # COSP sites. Input field may have a singleton dimension (XIOS scalar component)
        grid_ref = cfsites_grid_id
        add_cfsites_in_defs()
        #
    elif ssh[0:3] in ['XY-', 'S-A']:
        # this includes 'XY-AH' and 'S-AH' : model half-levels
        if ssh[0:3] in ['S-A', ]:
            add_cfsites_in_defs()
            target_hgrid_id = cfsites_domain_id
        if target_hgrid_id:
            # Must create and a use a grid similar to the last one defined
            # for that variable, except for a change in the hgrid/domain
            grid_ref = change_domain_in_grid(target_hgrid_id)
            if grid_ref is False or grid_ref is None:
                raise Dr2xmlError("Fatal: cannot create grid_def for %s with hgrid=%s" % (alias, target_hgrid_id))
    elif ssh in ['TR-na', 'TRS-na']:  # transects,   oce or SI
        pass
    elif ssh[0:3] in ['YB-', ]:  # basin zonal mean or section
        pass
    elif ssh in ['na-na', ]:  # TBD ? global means or constants - spatial integration is not handled
        pass
    elif ssh in ['na-A', ]:  # only used for rlu, rsd, rsu ... in Efx ????
        pass
    else:
        raise Dr2xmlError(
            "Fatal: Issue with un-managed spatial shape %s for variable %s in table %s" % (ssh, sv.label, table))
    return grid_ref


def ping_file_for_realms_list(settings, context, lrealms, svars, path_special, dummy="field_atm",
                              dummy_with_shape=False, exact=False,
                              comments=False, prefix="CV_", filename=None, debug=[]):
    """Based on a list of realms LREALMS and a list of simplified vars
    SVARS, create the ping file which name is ~
    ping_<realms_list>.xml, which defines fields for all vars in
    SVARS, with a field_ref which is either 'dummy' or '?<varname>'
    (depending on logical DUMMY)

    If EXACT is True, the match between variable realm string and one
    of the realm string in the list must be exact. Otherwise, the
    variable realm must be included in (or include) one of the realm list
    strings

    COMMENTS, if not False nor "", will drive the writing of variable
    description and units as an xml comment. If it is a string, it
    will be printed before this comment string (and this allows for a
    line break)

    DUMMY, if not false, should be either 'True', for a standard dummy
    label or a string used as the name of all field_refs. If False,
    the field_refs look like ?<variable name>.

    If DUMMY is True and DUMMY_WITH_SHAPE is True, dummy labels wiill
    include the highest rank shape requested by the DR, for
    information

    Field ids do include the provided PREFIX

    The ping file includes a <field_definition> construct

    For those MIP varnames which have a corresponding field_definition
    in a file named like ./inputs/DX_field_defs_<realm>.xml (path being
    relative to source code location), this latter field_def is
    inserted in the ping file (rather than a default one). This brings
    a set of 'standard' definitions fo variables which can be derived
    from DR-standard ones

    """
    logger = get_logger()
    name = ""
    for r in lrealms:
        name += "_" + r.replace(" ", "%")
    lvars = []
    for v in svars:
        if exact:
            if any([v.modeling_realm == r for r in lrealms]):
                lvars.append(v)
        else:
            var_realms = v.modeling_realm.split(" ")
            if any([v.modeling_realm == r or r in var_realms
                    for r in lrealms]):
                lvars.append(v)
        if context in settings['orphan_variables'] and \
                v.label in settings['orphan_variables'][context]:
            lvars.append(v)
    lvars.sort(key=lambda x: x.label_without_psuffix)

    # Remove duplicates : want to get one single entry for all variables having
    # the same label without psuffix, and one for each having different non-ambiguous label
    # Keep the one with the best piority
    uniques = []
    best_prio = OrderedDict()
    for v in lvars:
        lna = v.label_non_ambiguous
        lwps = v.label_without_psuffix
        if (lna not in best_prio) or (lna in best_prio and v.Priority < best_prio[lna].Priority):
            best_prio[lna] = v
        elif (lwps not in best_prio) or (lwps in best_prio and v.Priority < best_prio[lwps].Priority):
            best_prio[lwps] = v
        # elif not v.label_without_psuffix in labels :
        #    uniques.append(v); labels.append(v.label_without_psuffix)

    # lvars=uniques
    lvars = best_prio.values()
    lvars.sort(key=lambda x: x.label_without_psuffix)
    #
    if filename is None:
        filename = "ping" + name + ".xml"
    if filename[-4:] != ".xml":
        filename += ".xml"
    #
    if path_special:
        specials = read_special_fields_defs(lrealms, path_special)
    else:
        specials = False
    with open(filename, "w") as fp:
        fp.write('<!-- Ping files generated by dr2xml %s using Data Request %s -->\n' % (get_config_variable("version"),
                                                                                         get_data_request().get_version))
        fp.write('<!-- lrealms= %s -->\n' % repr(lrealms))
        fp.write('<!-- exact= %s -->\n' % repr(exact))
        fp.write('<!-- ')
        for s in settings:
            fp.write(' %s : %s\n' % (s, settings[s]))
        fp.write('--> \n\n')
        fp.write('<context id="%s">\n' % context)
        fp.write("<field_definition>\n")
        if settings.get("nemo_sources_management_policy_master_of_the_world", False) and context == 'nemo':
            out.write('<field_group freq_op="_reset_ freq_offset="_reset_" >\n')
        if exact:
            fp.write("<!-- for variables which realm intersects any of " + name + "-->\n")
        else:
            fp.write("<!-- for variables which realm equals one of " + name + "-->\n")
        for v in lvars:
            if v.label_non_ambiguous:
                label = v.label_non_ambiguous
            else:
                label = v.label_without_psuffix
            if v.label in debug:
                logger.debug("pingFile ... processing %s in table %s, label=%s" % (v.label, v.mipTable, label))

            if specials and label in specials:
                line = str(specials[label]).replace("DX_", prefix)
                # if 'ta' in label : print "ta is special : "+line
                line = line.replace("\n", "").replace("\t", "")
                fp.write('   ')
                fp.write(line)
            else:
                fp.write('   <field id="%-20s' % (prefix + label + '"') + ' field_ref="')
                if dummy:
                    shape = highest_rank(v)
                    if v.label_without_psuffix == 'clcalipso':
                        shape = 'XYA'
                    if dummy is True:
                        dummys = "dummy"
                        if dummy_with_shape:
                            dummys += "_" + shape
                    else:
                        dummys = dummy
                    fp.write('%-18s/>' % (dummys + '"'))
                else:
                    fp.write('?%-16s' % (label + '"') + ' />')
            if comments:
                # Add units, stdname and long_name as a comment string
                if isinstance(comments, string_types):
                    fp.write(comments)
                fp.write("<!-- P%d (%s) %s : %s -->" % (v.Priority, v.units, v.stdname, v.description))
            fp.write("\n")
        if 'atmos' in lrealms or 'atmosChem' in lrealms or 'aerosol' in lrealms:
            for tab in ["ap", "ap_bnds", "b", "b_bnds"]:
                fp.write('\t<field id="%s%s" field_ref="dummy_hyb" /><!-- One of the hybrid coordinate arrays -->\n'
                         % (prefix, tab))
        if settings.get("nemo_sources_management_policy_master_of_the_world", False) and context == 'nemo':
            out.write('</field_group>\n')
        fp.write("</field_definition>\n")
        #
        logger.info("%3d variables written for %s" % (len(lvars), filename))
        #
        # Write axis_defs, domain_defs, ... read from relevant input/DX_ files
        if path_special:
            for obj in ["axis", "domain", "grid", "field"]:
                copy_obj_from_DX_file(fp, obj, prefix, lrealms, path_special)
        fp.write('</context>\n')
