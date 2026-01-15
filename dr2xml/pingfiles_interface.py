#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ping files variables tools.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import glob
from collections import OrderedDict, defaultdict
import os
import sys
import six

# Utilities
from .settings_interface import get_settings_values
from .utils import Dr2xmlError

# Logger
from utilities.logger import get_logger

# Global variables and configuration tools
from .config import get_config_variable, add_value_in_dict_config_variable, set_config_variable, \
    add_value_in_list_config_variable

# Interface to xml tools
from .xml_interface import get_root_of_xml_file, DR2XMLElement, DR2XMLComment, parse_xml_file, create_pretty_xml_doc


def read_pingfiles_variables(pingfiles, dummies):
    """
    Read variables defined in the ping files.
    """
    logger = get_logger()
    pingvars = list()
    all_ping_refs = OrderedDict()
    if pingfiles is not None:
        all_pingvars = list()
        # print "pingfiles=",pingfiles
        for pingfile in pingfiles.split():
            ping_refs = read_xml_elmt_or_attrib(pingfile, tag='field', attrib='field_ref')
            # ping_refs=read_xml_elmt_or_attrib(pingfile, tag='field')
            if ping_refs is None:
                logger.error("Error: issue accessing pingfile %s" % pingfile)
                return
            all_ping_refs.update(ping_refs)
            if dummies == "include":
                pingvars = list(ping_refs)
            else:
                pingvars = [v for v in ping_refs if 'dummy' not in ping_refs[v]]
                if dummies == "forbid":
                    if len(pingvars) != len(ping_refs):
                        for v in ping_refs:
                            if v not in pingvars:
                                logger.info(v)
                        logger.info("")
                        raise Dr2xmlError("They are still dummies in %s , while option is 'forbid' :" % pingfile)
                    else:
                        pingvars = list(ping_refs)
                elif dummies == "skip":
                    pass
                else:
                    logger.error("Forbidden option for dummies : %s" % dummies)
                    sys.exit(1)
            all_pingvars.extend(pingvars)
        pingvars = all_pingvars
    set_config_variable("pingvars", pingvars)
    set_config_variable("ping_refs", all_ping_refs)


def read_xml_elmt_or_attrib(filename, tag='field', attrib=None):
    """
    Returns a dict of objects tagged TAG in FILENAME, which
    - keys are ids
    - values depend on ATTRIB
          * if ATTRIB is None : object (elt)
          * else : values of attribute ATTRIB  (None if field does not have attribute ATTRIB)
    Returns None if filename does not exist
    """
    #
    logger = get_logger()
    rep = OrderedDict()
    logger.info("processing file %s:" % filename,)
    if os.path.exists(filename):
        logger.info("OK %s" % filename)
        root = get_root_of_xml_file(filename)
        defs = get_xml_childs(root, tag)
        if defs:
            for field in defs:
                logger.debug(".")
                key = field.attrib['id']
                if attrib is None:
                    value = field
                else:
                    value = field.attrib.get(attrib, None)
                rep[key] = value
            logger.debug("")
            return rep
    else:
        logger.info("No file")
        return None


def get_xml_childs(elt, tag='field', groups=['context', 'field_group',
                                             'field_definition', 'axis_definition', 'axis', 'domain_definition',
                                             'domain', 'grid_definition', 'grid', 'interpolate_axis']):
    """
        Returns a list of elements in tree ELT
        which have tag TAG, by digging in sub-elements
        named as in GROUPS
        """
    rep = list()
    if elt.tag in groups:
        for child in elt:
            rep.extend(get_xml_childs(child, tag))
    elif elt.tag == tag:
        rep.append(elt)
    return rep


def check_for_file_input(sv, hgrid):
    """
    Add an entry in pingvars
    """
    logger = get_logger()
    internal_dict = get_settings_values("internal")
    externs = internal_dict['fx_from_file']
    # print "/// sv.label=%s"%sv.label, sv.label in externs ,"hgrid=",hgrid
    if sv.label in externs and \
            any([d == hgrid for d in externs[sv.label]]):
        pingvar = internal_dict['ping_variables_prefix'] + sv.label
        add_value_in_list_config_variable(variable="pingvars", value=pingvar)
        # Add a grid made of domain hgrid only
        grid_id = "grid_" + hgrid
        grid_def = DR2XMLElement(tag="grid", id=grid_id)
        grid_def.append(DR2XMLElement(tag="domain", domain_ref=hgrid))

        # Add a grid and domain for reading the file (don't use grid above to avoid reampping)
        file_domain_id = "remapped_%s_file_domain" % sv.label
        domain_def = DR2XMLElement(tag="domain", id=file_domain_id, type="rectilinear")
        domain_def.append(DR2XMLElement(tag="generate_rectilinear_domain"))
        add_value_in_dict_config_variable(variable="domain_defs", key=file_domain_id, value=domain_def)
        file_grid_id = "remapped_{}_file_grid".format(sv.label)
        remap_grid_def = DR2XMLElement(tag="grid", id=file_grid_id)
        remap_grid_def.append(DR2XMLElement(tag="domain", domain_ref=file_domain_id))
        add_value_in_dict_config_variable(variable="grid_defs", key=file_grid_id, value=remap_grid_def)
        logger.debug(domain_def)
        logger.debug(remap_grid_def)

        # Create xml for reading the variable
        filename = externs[sv.label][hgrid][internal_dict["select_grid_choice"]]
        file_id = "remapped_{}_file".format(sv.label)
        field_in_file_id = "_".join([sv.label, hgrid])
        # field_in_file_id=sv.label
        file_def = DR2XMLElement(tag="file", id=file_id, name=filename, mode="read", output_freq="1ts", enabled="true")
        file_def.append(DR2XMLElement(tag="field", id=field_in_file_id, name=sv.label, operation="instant",
                                      freq_op="1ts", freq_offset="1ts", grid_ref=file_grid_id))
        add_value_in_dict_config_variable(variable="file_defs", key=file_id, value=file_def)
        logger.debug(file_def)
        #
        # field_def='<field id="%s" grid_ref="%s" operation="instant" >%s</field>'%\
        field_def = DR2XMLElement(tag="field", id=pingvar, grid_ref=grid_id, field_ref=field_in_file_id,
                                  operation="instant", freq_op="1ts", freq_offset="0ts")
        add_value_in_dict_config_variable(variable="field_defs", key=field_in_file_id, value=field_def)
        context_index = get_config_variable("context_index", to_change=True)
        context_index[pingvar] = field_def

        logger.debug(field_def)


def ping_file_for_realms_list(context, svars, lrealms, path_special, dummy="field_atm",
                              dummy_with_shape=False, exact=False,
                              comments=False, filename=None, debug=[]):
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
    internal_values = get_settings_values("internal")
    prefix = internal_values["ping_variables_prefix"]
    name = ""
    for r in lrealms:
        name += "_" + r.replace(" ", "%")
    lvars = []
    for table in svars:
        for v in svars[table]:
            added = False
            if len(set(v.modeling_realm) & set(lrealms)) > 0 or \
                    (not(exact) and len(set(lrealms) & v.set_modeling_realms) > 0):
                lvars.append(v)
                added = True
            if not added and context in internal_values['orphan_variables'] and \
                    v.label in internal_values['orphan_variables'][context]:
                lvars.append(v)
    lvars.sort(key=lambda x: x.label_without_psuffix)

    # Remove duplicates : want to get one single entry for all variables having
    # the same label without psuffix, and one for each having different non-ambiguous label
    # Keep the one with the best piority
    best_prio = defaultdict(list)
    for v in lvars:
        if v.label_non_ambiguous is not None:
            best_prio[v.label_non_ambiguous].append(v)
        if v.label_without_psuffix is not None:
            best_prio[v.label_without_psuffix].append(v)
    lvars = [sorted(best_prio[elt], key=lambda x: x.Priority)[0] for elt in best_prio]
    # lvars=uniques
    lvars.sort(key=lambda x: x.label_without_psuffix)
    #
    if filename is None:
        filename = "ping" + name + ".xml"
    if not filename.endswith(".xml"):
        filename += ".xml"
    #
    if path_special:
        specials = read_special_fields_defs(lrealms, path_special)
    else:
        specials = False

    xml_context = DR2XMLElement(tag="context")
    xml_field_def = DR2XMLElement(tag="field_definition")
    xml_fields = list()
    for v in lvars:
        if v.label_non_ambiguous:
            label = v.label_non_ambiguous
        else:
            label = v.label_without_psuffix
        if v.label in debug:
            logger.debug("pingFile ... processing %s in table %s, label=%s" % (v.label, v.mipTable, label))

        if specials and label in specials:
            xml_fields.append(specials[label])
        else:
            if dummy:
                shape = highest_rank(v)
                if dummy is True:
                    dummies = "dummy"
                    if dummy_with_shape:
                        dummies = "_".join([dummies, shape])
                else:
                    dummies = dummy
                field_ref = '?%-18s' % dummies
            else:
                field_ref = '?%-16s' % label
            xml_fields.append(DR2XMLElement(tag="field", id="%-20s" % (prefix + label), field_ref=field_ref))
        if comments:
            # Add units, stdname and long_name as a comment string
            if isinstance(comments, six.string_types):
                xml_fields.append(DR2XMLComment(text=comments))
            xml_fields.append(DR2XMLComment(text="P%d (%s) %s : %s" %
                                                 (v.Priority, v.units, v.stdname, v.description.replace(" \n", os.linesep))))
    if 'atmos' in lrealms or 'atmosChem' in lrealms or 'aerosol' in lrealms:
        for tab in ["ap", "ap_bnds", "b", "b_bnds"]:
            xml_fields.append(DR2XMLElement(tag="field", id="%s%s" % (prefix, tab), field_ref="dummy_hyb"))
            xml_fields.append(DR2XMLComment(text="One of the hybrid coordinate arrays"))
    if internal_values["nemo_sources_management_policy_master_of_the_world"] and context in ['nemo', ]:
        xml_field_group = DR2XMLElement(tag="field_group", freq_op="_reset_", freq_offset="_reset_")
        for elt in xml_fields:
            xml_field_group.append(elt)
        xml_field_def.append(xml_field_group)
    else:
        for elt in xml_fields:
            xml_field_def.append(elt)
    xml_context.append(xml_field_def)
    #
    logger.info("%3d variables written for %s" % (len(lvars), filename))
    #
    # Write axis_defs, domain_defs, ... read from relevant input/DX_ files
    if path_special:
        for xml_file in glob.glob(os.sep.join([path_special, "DX_[%s]_defs_[%s].xml" %
                                                             ("|".join(["axis", "domain", "grid", "field"]),
                                                              "|".join(lrealms))])):
            _, _, _, elt = parse_xml_file(xml_file=xml_file, path_parse=path_special)
            xml_context.append(elt)
    create_pretty_xml_doc(xml_element=xml_context, filename=filename)


def read_special_fields_defs(realms, path_special):
    """
    Read external files and return a dictionary containing the fields.
    """
    special = OrderedDict()
    subrealms_seen = []
    for realm in realms:
        for subrealm in realm.split():
            if subrealm in subrealms_seen:
                continue
            subrealms_seen.append(subrealm)
            d = read_xml_elmt_or_attrib(path_special + "/DX_%s_defs_%s.xml" % ("field", subrealm), tag='field')
            if d:
                special.update(d)
    rep = OrderedDict()
    # Use raw label as key
    for r in special:
        rep[r.replace("DX_", "")] = special[r]
    return rep


def highest_rank(svar):
    """Returns the shape with the highest needed rank among the CMORvars
    referencing a MIPvar with this label
    This, assuming dr2xml would handle all needed shape reductions
    """
    # mipvarlabel=svar.label_without_area
    # if not shapes : shape="??"
    if svar.spatial_shp is None or svar.spatial_shp in ["XY-na", "S-na"]:
        shape = "XY" # analyser realm, pb possible sur ambiguite singleton
    elif svar.spatial_shp in ["XY-A", "XY-P", "XY-H", "XY-HG", "Y-A", "Y-P"]:
        shape = "XYA"
    elif svar.spatial_shp in ["XY-O", ]:
        shape = "XYO"
    elif svar.spatial_shp in ["XY-AH", ]:
        shape = "XYAh" # Zhalf
    elif svar.spatial_shp in ["XY-SN", ]:
        shape = "XYSn" # Snow levels
    elif svar.spatial_shp in ["XY-S", ]:
        shape = "XYSo" # Soil levels
    elif svar.spatial_shp in ["YB-na", ]:
        shape = "basin_zonal_mean"
    elif svar.spatial_shp in ["YB-O", ]:
        shape = "basin_merid_section"
    elif svar.spatial_shp in ["YB-R", ]:
        shape = "basin_merid_section_density"
    elif svar.spatial_shp in ["S-A", ]:
        shape = "COSP-A"
    elif svar.spatial_shp in ["S-AH", ]:
        shape = "COSP-AH"
    elif svar.spatial_shp in ["na-A", ]:
        shape = "site-A"
    elif svar.spatial_shp in ["Y-na", ]:
        shape = "lat"
    elif svar.spatial_shp in ["TRS-na", ]:
        shape = "TRS"
    elif svar.spatial_shp in ["TR-na", ]:
        shape = "TR"
    elif svar.spatial_shp in ["L-na", ]:
        shape = "COSPcurtain"
    elif svar.spatial_shp in ["L-H40", ]:
        shape = "COSPcurtainH40"
    elif svar.spatial_shp in ["na-na", ]:
        shape = "0d"  # analyser realm
    else:
        shape = "XY"
    #
    altdims = sorted(list(set(list(svar.sdims)) - set(["latitude", "longitude", "basin", "siline", "olevel"])))
    for d in altdims:
        shape += "_" + d
    #
    return shape
