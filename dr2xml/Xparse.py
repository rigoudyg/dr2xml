#!/usr/bin/env python
# coding: utf-8

"""
Whats' necessary for reading XIOS xml file and process attribute's inheritance for
being able to request the grid_ref for any valid XIOS 'field' object

Main useful functions :
  <opaque>    context = init_context(context_name,printout=False)
  <ET object>    grid = id2grid(field_id,context,printout=False)
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict

# Interface to xml tools
from .xml_interface import get_root_of_xml_file, is_xml_element_to_parse, find_rank_xml_subelement

# Logger
from utilities.logger import get_logger


# Define for each object kind those attributes useful for grid inheritance
attributes = OrderedDict()
attributes['field'] = ['grid_ref', 'field_ref']
attributes['field_definition'] = attributes['field']
attributes['field_group'] = attributes['field']
attributes['grid'] = ['axis_ref', 'domain_ref', 'grid_ref']
attributes['grid_group'] = attributes['grid']
attributes['context'] = []
attributes['axis'] = ['axis_ref']


# attributes['axis_definition'] = []  # attributes['domain_definition'] = []
# attributes['grid_definition'] = []  # attributes['calendar'] = []


def remove_non_xml_element(elt):
    list_elt_to_remove = [e for e in elt if not is_xml_element_to_parse(e)]
    for e in list_elt_to_remove:
        elt.remove(e)
    for i in range(len(elt)):
        elt[i] = remove_non_xml_element(elt[i])
    return elt


def read_src(input_file, path_parse, dont_read=list()):
    """
    Recursively reads the subfiles indicated by tag 'src' in childs of ELT
    """
    elt = get_root_of_xml_file(input_file, follow_src=True, path_parse=path_parse, dont_read=dont_read)
    elt = remove_non_xml_element(elt)
    return elt


tags_to_merge = ['context', 'file_definition', 'field_definition', 'axis_definition', 'grid_definition', 'calendar',
                 'field', 'field_group', 'file_group']


def merge_sons(elt, level=0):
    """
    Merge all mergeable childs of  ELT based on tag, or
    on tag+id when tag is 'context' or 'field' or '..._group'
    """
    logger = get_logger()
    # Using a dict with first instance of an elt for each tag (or tag+id)
    bytag = OrderedDict()
    nb_child_remove = 0
    for i in range(len(elt)):
        child = elt[i - nb_child_remove]
        if child.tag in tags_to_merge:
            if child.tag not in ['context', 'field'] and '_group' not in child.tag:
                tag = child.tag
            elif 'id' in child.attrib:
                tag = child.tag + "_" + child.attrib['id']
            else:
                # do not merge attributes for anonymous fields
                logger.debug(level * "\t" + "%s %s" % (child.tag, child.attrib.get('id', 'no_id')))
                elt.replace(i - nb_child_remove, merge_sons(child, level + 1))
                continue
            if tag not in bytag:
                bytag[tag] = child
                logger.debug(level * "\t" + "%s %s" % (child.tag, child.attrib.get('id', 'no_id')))
                elt.replace(i - nb_child_remove, merge_sons(child, level + 1))
            elif child != bytag[tag]:
                if 'src' in child.attrib:
                    name = child.attrib['src']
                else:
                    if 'id' in child.attrib:
                        name = child.attrib['id']
                    else:
                        name = 'no_id'
                logger.debug(level * "\t" + "Moving %s %s content to %s" % (child.tag, name, tag))
                #
                # Move childs from secondary entry to first entry (brother)
                for sub in child:
                    bytag[tag].append(sub)
                # Update attributes, too
                for a in child.attrib:
                    bytag[tag].attrib[a] = child.attrib[a]
                logger.debug("removing one %s child : %s" % (elt.tag, child.tag))
                elt.remove(child)
                nb_child_remove += 1
        else:
            logger.debug(level * "\t" + "%s %s" % (child.tag, child.attrib.get('id', 'no_id')))
            elt.replace(i - nb_child_remove, merge_sons(child, level + 1))
    return elt


def solve_downward(attribs, elt):
    """ propagate attribute ATTRIB 's VALUE downward of ELT,
    setting recursively it for all childs to the parent value or
    to the value encountered in an intermediate node
    """
    for i in range(len(elt)):
        child = elt[i]
        for attrib in attribs:
            if attrib in attributes.get(child.tag, list()):
                value = child.get_attrib(key=attrib, parent="single", use_default=True, default=None)
                if value is not None:
                    elt[i].attrib[attrib] = value
        elt[i] = solve_downward(attribs, child)
    return elt


def make_index(elt, index=None, level=0):
    """
    Create an index of all elements having an id in ELT childs recursively
    and complement attributes and children of these indexed objects when
    crossing their id multiple times
    """
    logger = get_logger()
    if index is None:
        index = OrderedDict()
    for child in [child for child in elt if "id" in child.attrib]:
        the_id = child.attrib['id']
        logger.debug(level * "\t" + " indexing " + the_id,)
        if the_id in index:
            logger.debug(" (merging)")
            # Update indexed object with current attributes
            index[the_id].attrib.update(child.attrib)
            # Add child children to indexed objects
            index[the_id].extend(child[:])
        else:
            logger.debug(" init index")
            index[the_id] = child
    for child in elt:
        make_index(child, index, level + 1)
    return index


def attrib_by_ref(elt, attrib, index, level):
    """
        Provide ATTRIB value for ELT' id using its references
        and objects's dict INDEX
    """
    logger = get_logger()
    for a in [att for att in elt.attrib if "_ref" in att]:
        refid = elt.attrib[a]
        logger.debug("\n" + (level + 1) * "\t" + a + " -> " + refid,)
        try:
            ref = index[refid]
            if attrib in ref.attrib:
                rep = ref.attrib[attrib]
            else:
                rep = attrib_by_ref(ref, attrib, index, level + 1)
            logger.debug(" ---> !! GOT : %s !!!" % rep)
            if rep:
                return rep
        except:
            if not "dummy" in refid:
                raise XparseError("Error : reference '%s' is invalid" % refid)


def solve_by_ref(attribs, index, elt, level=0):
    got_one = 0
    for i in find_rank_xml_subelement(elt, not_tag=[None, "variable"]):
        child = elt[i]
        for attrib in attribs:
            if child.tag in attributes and attrib in attributes[child.tag] and attrib not in child.attrib:
                by_ref = attrib_by_ref(elt[i], attrib, index, level)
                if by_ref:
                    elt[i].attrib[attrib] = by_ref
                    got_one += 1
        got_one += solve_by_ref(attribs, index, elt[i], level + 1)
    return got_one


def select_context(rootel, context_id):
    """
    Find the context corresponding to context_id
    :param rootel: root of xml element
    :param context_id: id of the context to find
    :return: context corresponding to context_id in rootel
    """
    rank = find_rank_xml_subelement(rootel, tag="context", id=context_id)
    if len(rank) > 0:
        return rootel[rank[0]]
    else:
        return None


def init_context(context_id, path_parse="./"):
    """
    Create the index for xml elements
    :param context_id: id of the context of the index
    :param path_parse: directory of the xml iodef
    :param printout: boolean to active verbose log
    :return: the index of the context
    """
    logger = get_logger()
    xmldef = path_parse + "iodef.xml"
    logger.debug("Parsing %s ..." % xmldef,)
    rootel = read_src(xmldef, path_parse, dont_read=["dr2xml_", ])
    logger.debug("sourcing files  ...",)
    rootel = merge_sons(rootel)
    rootel = select_context(rootel, context_id)
    if rootel is not None:
        refs = ["grid_ref", "domain_ref", "axis_ref", "field_ref"]
        rootel = solve_downward(refs, rootel)
        index = make_index(rootel, None)
        while True:
            n = solve_by_ref(refs, index, rootel)
            logger.debug("%d refs solved" % n)
            if n == 0:
                break
        return index
    else:
        logger.warning("Xparse::init_context : context %s not found in %s" % (context_id, xmldef))


def id2gridid(field_id, index):
    """
    Call to id2grid and get "id" parameter
    :param field_id: id of the field
    :param index: index of the xml elements
    :param printout: boolean to active verbose log
    :return: the id of the grid corresponding to the entry parameters.
    """
    grid = id2grid(field_id, index)
    return grid.attrib['id']


def id2grid(field_id, index):
    """
    Returns the list of Element composing the grid of a field
    """
    logger = get_logger()
    if field_id in index:
        attrib = index[field_id].attrib
        if 'grid_ref' in attrib:
            grid_ref_field_id = attrib['grid_ref']
            if grid_ref_field_id in index:
                logger.debug("grid_ref value for %s is %s" % (grid_ref_field_id, repr(index[grid_ref_field_id])))
                return index[grid_ref_field_id]
            else:
                # if printout: print("field %s grid reference is %s
                # but that field has no grid"%(field_id,grid_ref_field_id))
                raise XparseError(
                    "field %s grid reference is %s but that field no grid" % (field_id, grid_ref_field_id))
        else:
            # if printout: print("field %s has no grid_ref"%(field_id))
            raise XparseError("field %s has no grid_ref" % field_id)
    else:
        # if printout: print("field %s is not known"%field_id)
        raise XparseError("field %s is not known" % field_id)


def id_has_expr_with_at(field_id, index):
    """
    Returns True if field has an expr attribute with includes an @
    """
    logger = get_logger()
    if field_id in index:
        attrib = index[field_id].attrib
        if 'expr' in attrib:
            logger.debug("In withAt, for %s, expr=%s" % (field_id, attrib['expr']))
            return '@' in attrib['expr']
        else:
            # if printout : print "In withAt, for %s, no expr"%(field_id)
            return False
    else:
        return False
        # raise Xparse_error("field %s is not known"%field_id)


class XparseError(Exception):
    """
    Xparse exceptions class.
    """

    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        logger = get_logger()
        logger.error(self.valeur)
        return repr(self.valeur)
