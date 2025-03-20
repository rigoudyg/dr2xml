#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Definitions of objects for DR interface
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from collections import OrderedDict

import six

from dr2xml.settings_interface import get_settings_values
from dr2xml.settings_interface.py_settings_interface import is_sset_not_None
from dr2xml.utils import convert_string_to_year, Dr2xmlError


class DataRequest(object):

    def __init__(self, data_request=None, print_DR_errors=False, print_DR_stdname_errors=False):
        self.data_request = data_request
        self.print_DR_errors = print_DR_errors
        self.print_DR_stdname_errors = print_DR_stdname_errors
        self.mcfg = None
        self.set_mcfg()

    def set_mcfg(self):
        self.mcfg = get_settings_values('internal', 'select_sizes')

    def update_mcfg(self):
        raise NotImplementedError()

    def get_version(self):
        """
        Get the version of the DR
        """
        raise NotImplementedError()

    def get_variables_per_label(self, debug=list()):
        return OrderedDict()

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

    def get_experiment_label_start_end_years(self, experiment):
        """
        Get the experiment start and end years
        """
        return None, "??", "??"

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

    def get_endyear_for_cmorvar(self, **kwargs):
        return None

    @staticmethod
    def find_exp_start_year(exp_label, exp_startyear, branch_year_in_child=None):
        """
        Find star year of an experiment
        :param exp_label: experiment label
        :param exp_startyear: experiment start year for data request
        :return: start year of an experiment
        """
        if branch_year_in_child is not None:
            return branch_year_in_child
        else:
            starty = convert_string_to_year(exp_startyear)
            if starty is None:
                form = "Cannot guess first year for experiment %s: DR says:'%s' "
                if is_sset_not_None():
                    form += "and 'branch_year_in_child' is not provided in experiment's settings"
                raise Dr2xmlError(form % (exp_label, exp_startyear))
            else:
                return starty

    @staticmethod
    def find_exp_end_year(exp_endyear, end_year=False):
        """
        Find the end year of an experiment
        :param exp_endyear: experiment endyear
        :param end_year: specified end year
        :return: end year of the experiment
        """
        if end_year is not False:
            return end_year
        else:
            return convert_string_to_year(exp_endyear)

    def get_cmorvars_list(self, **kwargs):
        return dict()


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

    def __init__(self, from_dr=False, **kwargs):
        if from_dr:
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


class SimpleCMORVar(SimpleObject):
    """
    A class for unifying CMOR vars and home variables
    """
    def __init__(self, type=False, modeling_realm=list(), grids=[""], label=None, mipVarLabel=None,
                 label_without_psuffix=None, label_non_ambiguous=None, frequency=None, mipTable=None, positive=None,
                 description=None, stdname=None, units=None, long_name=None, other_dims_size=1,
                 cell_methods=None, cell_measures=None, spatial_shp=None, temporal_shp=None, experiment=None,
                 Priority=1, mip_era=False, prec="float", missing=1.e+20, cmvar=None, ref_var=None, mip=None,
                 sdims=dict(), comments=None, coordinates=None, cm=False, id=None, flag_meanings=None, flag_values=None,
                 **kwargs):
        self.type = type
        self.modeling_realm = modeling_realm
        self.set_modeling_realms = set()
        for realm in self.modeling_realm:
            self.set_modeling_realms = self.set_modeling_realms | set(realm.split(" "))
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
        self.flag_meanings = flag_meanings
        self.flag_values = flag_values
        super(SimpleCMORVar, self).__init__(**kwargs)
    
    def set_attributes(self, **kwargs):
        if "modeling_realm" in kwargs:
            modeling_realms = kwargs["modeling_realm"]
            if modeling_realms in ["", None]:
                modeling_realms = list()
            elif not isinstance(modeling_realms, list):
                modeling_realms = [modeling_realms, ]
            kwargs["modeling_realm"] = modeling_realms
            set_modeling_realms = set()
            for realm in modeling_realms:
                set_modeling_realms = set_modeling_realms | set(realm.split(" "))
            kwargs["set_modeling_realms"] = set_modeling_realms
        super().set_attributes(**kwargs)

    def __eq__(self, other):
        return self.label == other.label and self.modeling_realm == other.modeling_realm and \
               self.frequency == other.frequency and self.mipTable == other.mipTable and \
               self.temporal_shp == other.temporal_shp and self.spatial_shp == other.spatial_shp

    def __lt__(self, other):
        return self.label < other.label

    def __gt__(self, other):
        return self.label > other.label

    def correct_data_request(self):
        pass

    @classmethod
    def get_from_dr(cls, input_var, **kwargs):
        raise NotImplementedError()

    @classmethod
    def get_from_extra(cls, input_var, mip_era=None, freq=None, table=None, **kwargs):
        input_var_dict = dict(type="extra", mip_era=mip_era, label=input_var["out_name"],
                              mipVarLabel=input_var["out_name"], stdname=input_var.get("standard_name", ""),
                              long_name=input_var["long_name"], units=input_var["units"],
                              modeling_realm=[input_var["modeling_realm"], ], frequency=freq, mipTable=table,
                              cell_methods=input_var["cell_methods"], cell_measures=input_var["cell_measures"],
                              positive=input_var["positive"], Priority=float(input_var[mip_era.lower() + "_priority"]),
                              label_without_psuffix=input_var["out_name"],
                              coordinates=input_var.get("dimensions", None))
        return cls(**input_var_dict)


class SimpleDim(SimpleObject):
    """
    A class for unifying grid info coming from DR and extra_Tables
    """
    def __init__(self, label=False, zoom_label=False, stdname=False, long_name=False, positive=False, requested="",
                 value=False, out_name=False, units=False, is_zoom_of=False, bounds=False, boundsValues=False,
                 axis=False, type=False, coords=False, title=False, name=None, is_union_for=list(), altLabel=False,
                 boundsRequested=False, **kwargs):
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

    @classmethod
    def get_from_extra(cls, input_dim, label=None, **kwargs):
        input_dim_dict = dict(label=label, axis=input_dim["axis"], stdname=input_dim["standard_name"],
                              units=input_dim["units"], long_name=input_dim["long_name"],
                              out_name=input_dim["out_name"], positive=input_dim["positive"],
                              title=input_dim.get("title", input_dim["long_name"]),
                              requested=" ".join([ilev for ilev in input_dim["requested"]]).rstrip(),
                              value=input_dim["value"], type=input_dim["type"])
        return cls(**input_dim_dict)
