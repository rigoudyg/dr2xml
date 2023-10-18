#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ping files variables tools.
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict
from io import open

import os
import sys

# Utilities
from .settings_interface import get_settings_values
from .utils import Dr2xmlError

# Logger
from logger import get_logger

# Global variables and configuration tools
from .config import get_config_variable, add_value_in_dict_config_variable, set_config_variable, \
    add_value_in_list_config_variable

# Interface to Data Request
from .dr_interface import get_data_request
# Interface to xml tools
from .xml_interface import get_root_of_xml_file, DR2XMLElement

# Variables tools
from .vars_interface.generic_data_request import get_grid_choice


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
        logger.info("No file ")
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


def read_special_fields_defs(realms, path_special, printout=False):
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
            d = read_xml_elmt_or_attrib(DX_defs_filename("field", subrealm, path_special), tag='field')
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
    logger = get_logger()
    mipvarlabel = svar.label_without_psuffix
    shapes = []
    altdims = set()
    data_request = get_data_request()
    for cvar in data_request.get_list_by_id('CMORvar').items:
        v = data_request.get_element_uid(cvar.vid, elt_type="variable")
        if v.label == mipvarlabel:
            st = data_request.get_element_uid(cvar.stid, check_print_DR_errors=False,
                                              error_msg="DR Error: issue with stid for : %s in table section : %s" %
                                                        (v.label, str(cvar.mipTableSection)))
            if st is None:
                shape = "?st"
            else:
                sp = data_request.get_element_uid(st.spid, error_msg="DR Error: issue with spid for %s %s %s" %
                                                                     (st.label, v.label, str(cvar.mipTable)))
                if sp is None:
                    # One known case in DR 1.0.2: hus in 6hPlev
                    shape = "XY"
                else:
                    shape = sp.label
                if "odims" in st.__dict__:
                    try:
                        map(altdims.add, st.odims.split("|"))
                    except:
                        logger.error("Issue with odims for %s st=%s" % (v.label, st.label))

        else:
            # Pour recuperer le spatial_shp pour le cas de variables qui n'ont
            # pas un label CMORvar de la DR (ex. HOMEvar ou EXTRAvar)
            shape = svar.spatial_shp
        if shape:
            shapes.append(shape)
    # if not shapes : shape="??"
    if len(shapes) == 0:
        shape = "XY"
    elif any(["XY-A" in s for s in shapes]):
        shape = "XYA"
    elif any(["XY-O" in s for s in shapes]):
        shape = "XYO"
    elif any(["XY-AH" in s for s in shapes]):
        shape = "XYAh"  # Zhalf
    elif any(["XY-SN" in s for s in shapes]):
        shape = "XYSn"  # snow levels
    elif any(["XY-S" in s for s in shapes]):
        shape = "XYSo"  # soil levels
    elif any(["XY-P" in s for s in shapes]):
        shape = "XYA"
    elif any(["XY-H" in s for s in shapes]):
        shape = "XYA"
    elif any(["XY-HG" in s for s in shapes]):
        shape = "XYA"
    #
    elif any(["XY-na" in s for s in shapes]):
        shape = "XY"  # analyser realm, pb possible sur ambiguite singleton
    #
    elif any(["YB-na" in s for s in shapes]):
        shape = "basin_zonal_mean"
    elif any(["YB-O" in s for s in shapes]):
        shape = "basin_merid_section"
    elif any(["YB-R" in s for s in shapes]):
        shape = "basin_merid_section_density"
    elif any(["S-A" in s for s in shapes]):
        shape = "COSP-A"
    elif any(["S-AH" in s for s in shapes]):
        shape = "COSP-AH"
    elif any(["na-A" in s for s in shapes]):
        shape = "site-A"
    elif any(["Y-A" in s for s in shapes]):
        shape = "XYA"  # lat-A
    elif any(["Y-P" in s for s in shapes]):
        shape = "XYA"  # lat-P
    elif any(["Y-na" in s for s in shapes]):
        shape = "lat"
    elif any(["TRS-na" in s for s in shapes]):
        shape = "TRS"
    elif any(["TR-na" in s for s in shapes]):
        shape = "TR"
    elif any(["L-na" in s for s in shapes]):
        shape = "COSPcurtain"
    elif any(["L-H40" in s for s in shapes]):
        shape = "COSPcurtainH40"
    elif any(["S-na" in s for s in shapes]):
        shape = "XY"  # fine once remapped
    elif any(["na-na" in s for s in shapes]):
        shape = "0d"  # analyser realm
    # else : shape="??"
    else:
        shape = "XY"
    #
    for d in altdims:
        dims = d.split(' ')
        for dim in dims:
            shape += "_" + dim
    #
    return shape


def copy_obj_from_DX_file(fp, obj, prefix, lrealms, path_special):
    """
    Insert content of DX_<obj>_defs files (changing prefix)
    """
    # print "copying %s defs :"%obj,
    logger = get_logger()
    subrealms_seen = []
    for realm in lrealms:
        for subrealm in realm.split():
            if subrealm in subrealms_seen:
                continue
            subrealms_seen.append(subrealm)
            # print "\tand realm %s"%subrealm,
            defs = DX_defs_filename(obj, subrealm, path_special)
            if os.path.exists(defs):
                with open(defs, "r") as fields:
                    # print "from %s"%defs
                    fp.write("\n<%s_definition>\n" % obj)
                    lines = fields.readlines()
                    for line in lines:
                        if not obj + "_definition" in line:
                            fp.write(line.replace("DX_", prefix))
                    fp.write("</%s_definition>\n" % obj)
            else:
                logger.info(" no file :%s " % defs)


def DX_defs_filename(obj, realm, path_special):
    """
    Return the path of the DX file.
    """
    # TBS# return prog_path+"/inputs/DX_%s_defs_%s.xml"%(obj,realm)
    return path_special + "/DX_%s_defs_%s.xml" % (obj, realm)


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
        filename = externs[sv.label][hgrid][get_grid_choice()]
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
