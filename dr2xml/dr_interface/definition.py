#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Definitions of objects for DR interface
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import namedtuple, OrderedDict

import six


class Scope(object):
    def __init__(self, scope=None):
        self.scope = scope
        self.mcfg = self.build_mcfg([None, None, None, None, None, None, None])

    def build_mcfg(self, value):
        mcfg = namedtuple('mcfg', ['nho', 'nlo', 'nha', 'nla', 'nlas', 'nls', 'nh1'])
        return mcfg._make(value)._asdict()

    def get_request_link_by_mip(self, mips_list):
        return list()

    def get_vars_by_request_link(self, request_link, pmax):
        return list()


class DataRequest(object):

    def __init__(self, data_request=None, print_DR_errors=False, print_DR_stdname_errors=False):
        self.data_request = data_request
        self.print_DR_errors = print_DR_errors
        self.print_DR_stdname_errors = print_DR_stdname_errors

    def get_version(self):
        """
        Get the version of the DR
        """
        raise NotImplementedError()

    def get_list_by_id(self, collection, **kwargs):
        """
        Get the collection corresponding to the collection id.
        """
        raise NotImplementedError()

    def get_sectors_list(self):
        return self.get_list_by_id("grids")

    def get_experiment_label(self, experiment):
        """
        Get the experiment from its label.
        """
        raise NotImplementedError()

    def get_cmor_var_id_by_label(self, label):
        """
        Get the id of the CMOR var corresponding to label.
        """
        raise NotImplementedError()

    def get_element_uid(self, id=None, **kwargs):
        """
        Get the uid of an element if precised, else the list of all elements.
        """
        raise NotImplementedError()

    def get_request_by_id_by_sect(self, id, request):
        """
        Get the attribute request of the element id.
        """
        raise NotImplementedError()

    def get_dimensions_dict(self):
        """
        Get dimensions defined in Data Request
        """
        raise NotImplementedError()

    def get_grids_dict(self):
        """
        Get grids defined in Data Request
        """
        raise NotImplementedError()

    def get_single_levels_list(self):
        """
        Get single levels defined in Data Request
        """
        raise NotImplementedError()

    def convert_DR_variable_to_dr2xml_variable(self, input_variable):
        """
        Convert a variable from the DR used to the dr2xml template variable.
        """
        raise NotImplementedError()

    def convert_DR_dimension_to_dr2xml_dimension(self, input_dimension):
        """
        Convert a dimension from the DR used to the dr2xml template dimension.
        """
        raise NotImplementedError()


class ListWithItems(list):

    def __init__(self):
        super().__init__()
        self.items = self.build_content()

    def build_content(self):
        return self[:]

    def __setitem__(self, key, value):
        super(ListWithItems, self).__setitem__(key, value)
        self.items = self.build_content()

    def __delitem__(self, key):
        super(ListWithItems, self).__delitem__(key)
        self.items = self.build_content()


class SimpleObject(object):

    def __init__(self, **kwargs):
        self.correct_data_request()
        self._format_dict_()

    def _format_dict_(self):
        for attr in self.__dict__:
            val = self.__getattribute__(attr)
            if isinstance(val, six.string_types):
                self.__setattr__(attr, val.strip())

    def set_attributes(self, **kwargs):
        for kwarg in [kw for kw in kwargs if kw in self.__dict__]:
            val = kwargs[kwarg]
            if isinstance(val, six.string_types):
                val = val.strip()
            self.__setattr__(kwarg, val)
        self.correct_data_request()
        self._format_dict_()

    def update_attributes(self, **kwargs):
        for kwarg in [kw for kw in kwargs
                      if kw in self.__dict__ and isinstance(self.__dict__[kw], (dict, OrderedDict))]:
            self.__dict__[kwarg].update(kwargs[kwarg])
        self.correct_data_request()
        self._format_dict_()

    def correct_data_request(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()


class SimpleCMORVar(SimpleObject):
    """
    A class for unifying CMOR vars and home variables
    """
    def __init__(self, type=False, modeling_realm=None, grids=[""], label=None, mipVarLabel=None,
                 label_without_psuffix=None, label_non_ambiguous=None, frequency=None, mipTable=None, positive=None,
                 description=None, stdname=None, units=None, long_name=None, struct=None, other_dims_size=1,
                 cell_methods=None, cell_measures=None, spatial_shp=None, temporal_shp=None, experiment=None,
                 Priority=1, mip_era=False, prec="float", missing=1.e+20, cmvar=None, ref_var=None, mip=None,
                 sdims=dict(), comments=None, coordinates=None, cm=False, id=None, **kwargs):
        self.type = type
        self.modeling_realm = modeling_realm
        self.grids = grids
        self.label = label  # taken equal to the CMORvar label
        self.mipVarLabel = mipVarLabel  # taken equal to MIPvar label
        self.label_without_psuffix = label_without_psuffix
        self.label_non_ambiguous = label_non_ambiguous
        self.frequency = frequency
        self.mipTable = mipTable
        self.positive = positive
        self.description = description
        self.stdname = stdname
        self.units = units
        self.long_name = long_name
        self.struct = struct
        self.sdims = OrderedDict()
        self.sdims.update(sdims)
        self.other_dims_size = other_dims_size
        self.cell_methods = cell_methods
        self.cm = cm
        self.cell_measures = cell_measures
        self.spatial_shp = spatial_shp
        self.temporal_shp = temporal_shp
        self.experiment = experiment
        self.mip = mip
        self.Priority = Priority  # Will be changed using DR or extra-Tables
        self.mip_era = mip_era  # Later changed in projectname (uppercase) when appropriate
        self.prec = prec
        self.missing = missing
        self.cmvar = cmvar  # corresponding CMORvar, if any
        self.ref_var = ref_var
        self.comments = comments
        self.coordinates = coordinates
        self.id = id
        super(SimpleCMORVar, self).__init__(**kwargs)

    def __eq__(self, other):
        return self.label == other.label and self.modeling_realm == other.modeling_realm and \
               self.frequency == other.frequency and self.mipTable == other.mipTable and \
               self.temporal_shp == other.temporal_shp and self.spatial_shp == other.spatial_shp

    def correct_data_request(self):
        pass

    @classmethod
    def get_from_dr(cls, input_var, **kwargs):
        raise NotImplementedError()


class SimpleDim(SimpleObject):
    """
    A class for unifying grid info coming from DR and extra_Tables
    """
    def __init__(self, label=False, zoom_label=False, stdname=False, long_name=False, positive=False, requested="",
                 value=False, out_name=False, units=False, is_zoom_of=False, bounds=False, boundsValues=False,
                 axis=False, type=False, coords=False, title=False, name=None, is_union_for=list(), altLabel=False,
                 boundsRequested=False,
                 **kwargs):
        self.label = label
        if altLabel is False:
            self.altLabel = self.label
        else:
            self.altLabel = altLabel
        self.zoom_label = zoom_label
        self.stdname = stdname
        self.long_name = long_name
        self.positive = positive
        self.requested = requested
        self.value = value
        self.out_name = out_name
        self.units = units
        self.is_zoom_of = is_zoom_of
        self.bounds = bounds
        self.boundsValues = boundsValues
        self.boundsRequested = boundsRequested
        self.axis = axis
        self.type = type
        self.coords = coords
        self.title = title
        self.is_union_for = is_union_for
        self.name = name
        super(SimpleDim, self).__init__(**kwargs)

    def correct_data_request(self):
        if self.requested and len(self.requested) > 0:
            self.dimsize = max(len(self.requested.split(" ")), 1)
        else:
            self.dimsize = 1
        if self.altLabel != self.label:
            self.altLabel = self.label

    @classmethod
    def get_from_dr(cls, input_dim, **kwargs):
        raise NotImplementedError()
