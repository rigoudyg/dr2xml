#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basics python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import datetime
import re

import six

from dr2xml.projects.projects_interface_definitions import ValueSettings, ParameterSettings, TagSettings, \
    ConditionSettings, FunctionSettings, CaseSettings

parent_project_settings = "dr2xml"


def build_external_variables(cell_measures):
    #
    # CF rule : if the file variable has a cell_measures attribute, and
    # the corresponding 'measure' variable is not included in the file,
    # it must be quoted as external_variable
    external_variables = list()
    if "area:" in cell_measures:
        external_variables.append(re.sub(".*area: ([^ ]*).*", r'\1', cell_measures))
    if "volume:" in cell_measures:
        external_variables.append(re.sub(".*volume: ([^ ]*).*", r'\1', cell_measures))
    return " ".join(external_variables)


def compute_nb_days(year_ref, year_branch, month_ref=1, month_branch=1, day_ref=1, day_branch=1):
    if isinstance(year_ref, six.string_types):
        year_ref = int(year_ref)
    if isinstance(month_ref, six.string_types):
        month_ref = int(month_ref)
    if isinstance(day_ref, six.string_types):
        day_ref = int(day_ref)
    if isinstance(year_branch, six.string_types):
        year_branch = int(year_branch)
    if isinstance(month_branch, six.string_types):
        month_branch = int(month_branch)
    if isinstance(day_branch, six.string_types):
        day_branch = int(day_branch)
    date_ref = datetime.datetime(year_ref, month_ref, day_ref)
    date_branch = datetime.datetime(year_branch, month_branch, day_branch)
    nb_days = (date_branch - date_ref).days
    return "{}.0D".format(nb_days)


internal_values = dict()

common_values = dict(
    branch_year_in_parent=ParameterSettings(
        key="branch_year_in_parent",
        cases=[
            CaseSettings(
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="internal", keys="experiment_id"),
                                      check_to_do="eq",
                                      reference_values=ValueSettings(key_type="internal", keys="branching")
                                      ),
                    ConditionSettings(check_value=ValueSettings(key_type="simulation", keys="branch_year_in_parent"),
                                      check_to_do="eq",
                                      reference_values=ValueSettings(
                                          key_type="internal",
                                          keys=[
                                              "branching",
                                              ValueSettings(key_type="internal", keys="experiment_id"),
                                              1
                                          ]
                                      )
                                      )
                ],
                value=ValueSettings(key_type="simulation", keys="branch_year_in_parent")
            ),
            CaseSettings(
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="internal", keys="experiment_id"),
                                      check_to_do="neq",
                                      reference_values=ValueSettings(key_type="internal", keys="branching")
                                      )
                ],
                value=ValueSettings(key_type="simulation", keys="branch_year_in_parent")
            )
        ],
        skip_values=[None, "None", "", "N/A"],
        help="Branch year in parent simulation with respect to its time axis."
    ),
    description=ParameterSettings(
        key="description",
        default_values=[
            ValueSettings(key_type="simulation", keys="description"),
            ValueSettings(key_type="laboratory", keys="description")
        ],
        help="Description of the simulation."
    ),
    date_range=ParameterSettings(
        key="date_range",
        default_values=["%start_date%-%end_date%", ],
        help="Date range format to be used in file definition names."
    ),
    list_perso_dev_file=ParameterSettings(
        key="list_perso_dev_file",
        default_values=["dr2xml_list_perso_and_dev_file_names", ],
        help="Name of the file which will contain the list of the patterns of perso and dev output file definition."
    ),
    info_url=ParameterSettings(
        key="info_url",
        default_values=[
            ValueSettings(key_type="laboratory", keys="info_url")
        ],
        help="Location of documentation."
    ),
    expid_in_filename=ParameterSettings(
        key="expid_in_filename",
        default_values=[
            ValueSettings(key_type="simulation", keys="expid_in_filename"),
            ValueSettings(key_type="internal", keys="experiment_id")
        ],
        forbidden_patterns=[".*_.*", ],
        help="Experiment label to use in file names and attribute."
    ),
    experiment=ParameterSettings(
        key="experiment",
        default_values=[
            ValueSettings(key_type="simulation", keys="experiment")
        ],
        help="Name of the experiment."
    ),
    forcing_index=ParameterSettings(
        key="forcing_index",
        default_values=[
            ValueSettings(key_type="simulation", keys="forcing_index"),
            "1"
        ],
        help="Index for variant of forcing."
    ),
    history=ParameterSettings(
        key="history",
        default_values=[
            ValueSettings(key_type="simulation", keys="history"),
            "none"
        ],
        help="In case of replacement of previously produced data, description of any changes in the production chain."
    ),
    initialization_index=ParameterSettings(
        key="initialization_index",
        default_values=[
            ValueSettings(key_type="simulation", keys="initialization_index"),
            "1"
        ],
        help="Index for variant of initialization method."
    ),
    branch_method=ParameterSettings(
        key="branch_method",
        default_values=[
            ValueSettings(key_type="simulation", keys="branch_method"),
            "standard"
        ],
        help="Branching procedure."
    ),
    parent_mip_era=ParameterSettings(
        key="parent_mip_era",
        default_values=[
            ValueSettings(key_type="simulation", keys="parent_mip_era")
        ],
        help="Parent’s associated MIP cycle."
    ),
    parent_source_id=ParameterSettings(
        key="parent_source_id",
        default_values=[
            ValueSettings(key_type="simulation", keys="parent_source_id")
        ],
        help="Parent model identifier."
    ),
    parent_time_units=ParameterSettings(
        key="parent_time_units",
        default_values=[
            ValueSettings(key_type="simulation", keys="parent_time_units")
        ],
        help="Time units used in parent."
    ),
    parent_time_ref_year=ParameterSettings(
        key="parent_time_ref_year",
        default_values=[
            ValueSettings(key_type="simulation", keys="parent_time_ref_year"),
            "1850"
        ],
        help="Reference year in parent simulation."
    ),
    branch_month_in_parent=ParameterSettings(
        key="branch_month_in_parent",
        default_values=[
            ValueSettings(key_type="simulation", keys="branch_month_in_parent"),
            "1"
        ],
        help="Branch month in parent simulation with respect to its time axis."
    ),
    parent_variant_label=ParameterSettings(
        key="parent_variant_label",
        default_values=[
            ValueSettings(key_type="simulation", keys="parent_variant_label")
        ],
        help="Parent variant label."
    ),
    physics_index=ParameterSettings(
        key="physics_index",
        default_values=[
            ValueSettings(key_type="simulation", keys="physics_index"),
            "1"
        ],
        help="Index for model physics variant."
    ),
    sub_experiment_id=ParameterSettings(
        key="sub_experiment_id",
        default_values=[
            ValueSettings(key_type="simulation", keys="sub_experiment_id"),
            "none"
        ],
        help="Sub-experiment identifier."
    ),
    sub_experiment=ParameterSettings(
        key="sub_experiment",
        default_values=[
            ValueSettings(key_type="simulation", keys="sub_experiment"),
            "none"
        ],
        help="Sub-experiment name."
    ),
    variant_info=ParameterSettings(
        key="variant_info",
        default_values=[
            ValueSettings(key_type="simulation", keys="variant_info")
        ],
        skip_values=["", ],
        help="It is recommended that some description be included to help identify major differences among variants, "
             "but care should be taken to record correct information.  dr2xml will add in all cases: "
             "'Information provided by this attribute may in some cases be flawed. Users can find more comprehensive "
             "and up-to-date documentation via the further_info_url global attribute.'"
    ),
    comment_sim=ParameterSettings(
        key="comment_sim",
        default_values=[
            ValueSettings(key_type="simulation", keys="comment"),
            ""
        ],
        help="A character string containing additional information about the models from simulation settings. "
             "Will be complemented with the experiment's specific comment string."
    ),
    comment_lab=ParameterSettings(
        key="comment_lab",
        default_values=[
            ValueSettings(key_type="laboratory", keys="comment"),
            ""
        ],
        help="A character string containing additional information about the models from laboratory settings. "
             "Will be complemented with the experiment's specific comment string."
    ),
    references=ParameterSettings(
        key="references",
        default_values=[
            ValueSettings(key_type="laboratory", keys="references")
        ],
        help="References associated with the simulation."
    ),
    compression_level=ParameterSettings(
        key="compression_level",
        default_values=[
            ValueSettings(key_type="laboratory", keys="compression_level"),
            "0"
        ],
        help="The compression level to be applied to NetCDF output files."
    ),
    output_level=ParameterSettings(
        key="output_level",
        default_values=[
            ValueSettings(key_type="laboratory", keys="output_level"),
            "10"
        ],
        help="We can control the max output level set for all output files."
    ),
    source=ParameterSettings(
        key="source",
        default_values=[
            ValueSettings(key_type="laboratory", keys="source")
        ],
        help="Name of the model."
    ),
    institution=ParameterSettings(
        key="institution",
        default_values=[
            ValueSettings(key_type="laboratory", keys="institution")
        ],
        help="Full name of the institution of the data producer."
    ),
    contact=ParameterSettings(
        key="contact",
        default_values=[
            ValueSettings(key_type="simulation", keys="contact"),
            ValueSettings(key_type="laboratory", keys="contact"),
            "None"
        ],
        help="Email address of the data producer."
    ),
    HDL=ParameterSettings(
        key="HDL",
        default_values=[
            ValueSettings(key_type="simulation", keys="HDL"),
            ValueSettings(key_type="laboratory", keys="HDL")
        ],
        help="HDL associated with the project."
    ),
    mip_era=ParameterSettings(
        key="mip_era",
        default_values=[
            ValueSettings(key_type="simulation", keys="mip_era"),
            ValueSettings(key_type="laboratory", keys="mip_era")
        ],
        help="MIP associated with the simulation."
    ),
    activity_id=ParameterSettings(
        key="activity_id",
        default_values=[
            ValueSettings(key_type="simulation", keys="activity_id"),
            ValueSettings(key_type="laboratory", keys="activity_id")
        ],
        help="MIP(s) name(s)."
    ),
    parent_activity_id=ParameterSettings(
        key="parent_activity_id",
        default_values=[
            ValueSettings(key_type="simulation", keys="parent_activity_id"),
            ValueSettings(key_type="simulation", keys="activity_id"),
            ValueSettings(key_type="laboratory", keys="parent_activity_id"),
            ValueSettings(key_type="laboratory", keys="activity_id")
        ],
        help="Description of sub-experiment."
    ),
    parent_experiment_id=ParameterSettings(
        key="parent_experiment_id",
        default_values=[
            ValueSettings(key_type="simulation", keys="parent_experiment_id"),
            ValueSettings(key_type="laboratory", keys="parent_experiment_id")
        ],
        help="Parent experiment identifier."
    ),
    convention_str=ParameterSettings(
        key="convention_str",
        default_values=[
            ValueSettings(key_type="config", keys="conventions")
        ],
        help="Version of the conventions used."
    ),
    dr2xml_version=ParameterSettings(
        key="dr2xml_version",
        default_values=[
            ValueSettings(key_type="config", keys="version")
        ],
        help="Version of dr2xml used."
    ),
    data_specs_version=ParameterSettings(
        key="data_specs_version",
        default_values=[
            ValueSettings(key_type="data_request", keys=["get_version", "__call__"])
        ],
        fatal=True,
        help="Version of the data request used."
    )
)

project_settings = dict(
    context=TagSettings(
        attrs_list=["id", ],
        attrs_constraints=dict(
            id=ParameterSettings(
                key="id",
                help="Id of the context",
                default_values=[
                    ValueSettings(key_type="internal", keys="context")
                ]
            ),
        ),
        comments_list=["DR_version", "dr2xml_version", "lab_settings", "simulation_settings", "year"],
        comments_constraints=dict(
            DR_version=ParameterSettings(
                key="DR_version",
                help="Version of the Data Request used",
                default_values=[
                    ValueSettings(key_type="common", keys="data_specs_version", fmt="CMIP6 Data Request version {}")
                ]
            ),
            dr2xml_version=ParameterSettings(
                key="dr2xml_version",
                help="Version of dr2xml used",
                default_values=[
                    ValueSettings(key_type="common", keys="dr2xml_version", fmt="dr2xml version {}")
                ]
            ),
            lab_settings=ParameterSettings(
                key="lab_settings",
                help="Laboratory settings used",
                default_values=[
                    ValueSettings(key_type="laboratory", fmt="Lab_and_model settings\n{}")
                ]
            ),
            simulation_settings=ParameterSettings(
                key="simulation_settings",
                help="Simulation_settings used",
                default_values=[
                    ValueSettings(key_type="simulation", fmt="Simulation settings\n{}")
                ]
            ),
            year=ParameterSettings(
                key="year",
                help="Year used for the dr2xml's launch",
                default_values=[
                    ValueSettings(key_type="internal", keys="year", fmt="Year processed {}")
                ]
            )
        )
    ),
    file_definition=TagSettings(
        attrs_list=["type", "enabled"],
        attrs_constraints=dict(
            type=ParameterSettings(
                key="type",
                help="Type of file to be produced",
                default_values=["one_file", ]
            ),
            enabled=ParameterSettings(
                key="enabled",
                help="Should the file_definition be considered by XIOS",
                default_values=["true", ]
            )
        )
    ),
    file=TagSettings(
        attrs_list=["id", "name", "mode", "output_freq", "enabled"],
        attrs_constraints=dict(
            id=ParameterSettings(
                key="id",
                help="Id of the file."
            ),
            name=ParameterSettings(
                key="name",
                help="File name."
            ),
            mode=ParameterSettings(
                key="mode",
                help="Mode in which the file will be open."
            ),
            output_freq=ParameterSettings(
                key="output_freq",
                help="Frequency of the outputs contained in the file."
            ),
            enabled=ParameterSettings(
                key="enabled",
                help="Should the file be considered by XIOS."
            )
        )
    ),
    file_output=TagSettings(
        attrs_list=["id", "name", "output_freq", "append", "output_level", "compression_level", "split_freq",
                    "split_freq_format", "split_start_offset", "split_end_offset", "split_last_date", "time_units",
                    "time_counter_name", "time_counter", "time_stamp_name", "time_stamp_format", "uuid_name",
                    "uuid_format", "convention_str", "synchronisation_frequency"],
        attrs_constraints=dict(
            id=ParameterSettings(
                key="id",
                help="Id of the output file",
                default_values=[
                    ValueSettings(
                        key_type="combine",
                        keys=[
                            ValueSettings(key_type="variable", keys="label"),
                            ValueSettings(key_type="dict", keys="table_id"),
                            ValueSettings(key_type="dict", keys="grid_label")
                        ],
                        fmt="{}_{}_{}"
                    )
                ]
            ),
            name=ParameterSettings(
                key="name",
                help="File name."
            ),
            output_freq=ParameterSettings(
                key="output_freq",
                help="Frequency of the outputs contained in the file."
            ),
            split_freq=ParameterSettings(
                key="split_freq",
                help="Splitting frequency of the file.",
                skip_values=["", "None", None],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
                                      check_to_do="nmatch", reference_values=".*fx.*")
                ]
            ),
            split_freq_format=ParameterSettings(
                key="split_freq_format",
                help="Splitting frequency format of the file.",
                skip_values=["", "None", None],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
                                      check_to_do="nmatch", reference_values=".*fx.*")
                ]
            ),
            split_start_offset=ParameterSettings(
                key="split_start_offset",
                help="Splitting start offset of the file",
                skip_values=["", "None", "False", None, False],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
                                      check_to_do="nmatch", reference_values=".*fx.*")
                ]
            ),
            split_end_offset=ParameterSettings(
                key="split_end_offset",
                help="Splitting end offset of the file",
                skip_values=["", "None", "False", None, False],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
                                      check_to_do="nmatch", reference_values=".*fx.*")
                ]
            ),
            split_last_date=ParameterSettings(
                key="split_last_date",
                help="Splitting last date of the file",
                skip_values=["", "None", None],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
                                      check_to_do="nmatch", reference_values=".*fx.*")
                ]
            ),
            append=ParameterSettings(
                key="append",
                help="Should the data be append to the file?",
                default_values=["true", ]
            ),
            time_units=ParameterSettings(
                key="time_units",
                help="Time units of the file.",
                default_values=["days", ]
            ),
            time_counter_name=ParameterSettings(
                key="time_counter_name",
                help="Time counter name.",
                default_values=["time", ]
            ),
            time_counter=ParameterSettings(
                key="time_counter",
                help="Time counter type.",
                default_values=["exclusive", ]
            ),
            time_stamp_name=ParameterSettings(
                key="time_stamp_name",
                help="Time stamp name.",
                default_values=["creation_date", ]
            ),
            time_stamp_format=ParameterSettings(
                key="time_stamp_format",
                help="Time stamp format.",
                default_values=["%Y-%m-%dT%H:%M:%SZ", ]
            ),
            uuid_name=ParameterSettings(
                key="uuid_name",
                help="Unique identifier of the file name.",
                default_values=["tracking_id", ]
            ),
            uuid_format=ParameterSettings(
                key="uuid_format",
                help="Unique identifier of the file format.",
                default_values=[
                    ValueSettings(key_type="common", keys="HDL", fmt="hdl:{}/%uuid%")
                ],
                skip_values=["None", "", None]
            ),
            synchronisation_frequency=ParameterSettings(
                key="synchronisation_frequency",
                default_values=[
                    ValueSettings(key_type="internal", keys="synchronisation_frequency")
                ],
                skip_values=["None", "", None],
                help="Frequency at which the synchornisation between buffer and filesystem is done."
            ),
            convention_str=ParameterSettings(
                key="convention_str",
                help="Convention used for the file.",
                default_values=[
                    ValueSettings(key_type="common", keys="convention_str")
                ]
            ),
            output_level=ParameterSettings(
                key="output_level",
                help="Output level of the file.",
                default_values=[
                    ValueSettings(key_type="common", keys="output_level")
                ],
                skip_values=["None", "", None]
            ),
            compression_level=ParameterSettings(
                key="compression_level",
                help="Compression level of the file.",
                default_values=[
                    ValueSettings(key_type="common", keys="compression_level")
                ],
                skip_values=["None", "", None]
            )
        ),
        vars_list=["activity_id", "contact", "data_specs_version", "dr2xml_version", "expid_in_filename", "description",
                   "title_desc", "experiment", "external_variables", "forcing_index", "frequency", "further_info_url",
                   "grid", "grid_label", "nominal_resolution", "comment", "history", "initialization_index",
                   "institution_id", "institution", "license", "mip_era", "parent_experiment_id", "parent_mip_era",
                   "parent_activity_id", "parent_source_id", "parent_time_units", "parent_variant_label",
                   "branch_method", "branch_time_in_parent", "branch_time_in_child", "physics_index", "product",
                   "realization_index", "realm", "references", "source", "source_id", "source_type",
                   "sub_experiment_id", "sub_experiment", "table_id", "title", "variable_id", "variant_info",
                   "variant_label"],
        vars_constraints=dict(
            grid=ParameterSettings(
                key="grid",
                help="Id of the grid used in the file."
            ),
            grid_label=ParameterSettings(
                key="grid_label",
                help="Label of the grid used in the file."
            ),
            nominal_resolution=ParameterSettings(
                key="nominal_resolution",
                help="Nominal resolution of the grid used in the file."
            ),
            license=ParameterSettings(
                key="license",
                help="License associated with the file."
            ),
            table_id=ParameterSettings(
                key="table_id",
                help="Id of the table associated with the file."
            ),
            variable_id=ParameterSettings(
                key="variable_id",
                help="Id of the variable contained in the file."
            ),
            contact=ParameterSettings(
                key="contact",
                help="Contact email.",
                default_values=[
                    ValueSettings(key_type="common", keys="contact")
                ],
                skip_values=["None", "", None]
            ),
            data_specs_version=ParameterSettings(
                key="data_specs_version",
                help="Version of the Data Request used.",
                default_values=[
                    ValueSettings(key_type="common", keys="data_specs_version")
                ]
            ),
            dr2xml_version=ParameterSettings(
                key="dr2xml_version",
                help="Version of dr2xml used.",
                default_values=[
                    ValueSettings(key_type="common", keys="dr2xml_version")
                ]
            ),
            expid_in_filename=ParameterSettings(
                key="expid_in_filename",
                help="Experiment id to be used in file name.",
                output_key="experiment_id",
                default_values=[
                    ValueSettings(key_type="common", keys="expid_in_filename")
                ]
            ),
            description=ParameterSettings(
                key="description",
                help="Description of the file.",
                skip_values=["", "None", None],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="internal", keys="experiment_id"),
                                      check_to_do="eq",
                                      reference_values=ValueSettings(key_type="common", keys="expid_in_filename"))
                ],
                default_values=[
                    ValueSettings(key_type="common", keys="description")
                ]
            ),
            title_desc=ParameterSettings(
                key="title_desc",
                help="Title of the file.",
                output_key="title",
                skip_values=["", "None", None],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="internal", keys="experiment_id"),
                                      check_to_do="eq",
                                      reference_values=ValueSettings(key_type="common", keys="expid_in_filename"))
                ],
                default_values=[
                    ValueSettings(key_type="common", keys="description")
                ]
            ),
            experiment=ParameterSettings(
                key="experiment",
                help="Experiment associated with the simulation.",
                skip_values=["", "None", None],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="internal", keys="experiment_id"),
                                      check_to_do="eq",
                                      reference_values=ValueSettings(key_type="common", keys="expid_in_filename"))
                ],
                default_values=[
                    ValueSettings(key_type="common", keys="experiment")
                ]
            ),
            external_variables=ParameterSettings(
                key="external_variables",
                help="External variables associated with the file.",
                skip_values=["", ],
                default_values=[
                    ValueSettings(key_type="variable", keys="cell_measures",
                                  func=FunctionSettings(func=build_external_variables))
                ]
            ),
            forcing_index=ParameterSettings(
                key="forcing_index",
                help="Forcing index associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="forcing_index")
                ],
                num_type="int"
            ),
            further_info_url=ParameterSettings(
                key="further_info_url",
                help="Url to obtain further information associated with the simulation.",
                skip_values=["", "None", None]
            ),
            history=ParameterSettings(
                key="history",
                help="History associated with the file.",
                default_values=[
                    ValueSettings(key_type="common", keys="history")
                ]
            ),
            initialization_index=ParameterSettings(
                key="initialization_index",
                help="Initialization index associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="initialization_index")
                ],
                num_type="int"
            ),
            institution=ParameterSettings(
                key="institution",
                help="Institution associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="institution")
                ],
                fatal=True
            ),
            institution_id=ParameterSettings(
                key="institution_id",
                help="Institution id associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="internal", keys="institution_id")
                ],
                fatal=True
            ),
            mip_era=ParameterSettings(
                key="mip_era",
                help="MIP associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="mip_era"),
                    ValueSettings(key_type="variable", keys="mip_era")
                ]
            ),
            parent_experiment_id=ParameterSettings(
                key="parent_experiment_id",
                help="Parent experiment id associated with the simulation.",
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
                                      check_to_do="neq", reference_values=["no parent", "", "None"])
                ],
                default_values=[
                    ValueSettings(key_type="common", keys="parent_experiment_id")
                ]
            ),
            parent_mip_era=ParameterSettings(
                key="parent_mip_era",
                help="MIP associated with the parent experiment.",
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
                                      check_to_do="neq", reference_values=["no parent", "", "None"])
                ],
                default_values=[
                    ValueSettings(key_type="common", keys="parent_mip_era"),
                    ValueSettings(key_type="common", keys="mip_era"),
                    ValueSettings(key_type="variable", keys="mip_era")
                ]
            ),
            parent_activity_id=ParameterSettings(
                key="parent_activity_id",
                help="Activity id associated with the parent experiment.",
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
                                      check_to_do="neq", reference_values=["no parent", "", "None"])
                ],
                default_values=[
                    ValueSettings(key_type="common", keys="parent_activity_id")
                ]
            ),
            parent_source_id=ParameterSettings(
                key="parent_source_id",
                help="Model id of the parent experiment.",
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
                                      check_to_do="neq", reference_values=["no parent", "", "None"])
                ],
                default_values=[
                    ValueSettings(key_type="common", keys="parent_source_id"),
                    ValueSettings(key_type="internal", keys="source_id")
                ]
            ),
            parent_time_units=ParameterSettings(
                key="parent_time_units",
                help="Time units of the parent experiment.",
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
                                      check_to_do="neq", reference_values=["no parent", "", "None"])
                ],
                default_values=[
                    ValueSettings(key_type="common", keys="parent_time_units"),
                    ValueSettings(key_type="common", keys="parent_time_ref_year", fmt="days since {}-01-01 00:00:00")
                ]
            ),
            parent_variant_label=ParameterSettings(
                key="parent_variant_label",
                help="Variant label of the parent experiment.",
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
                                      check_to_do="neq", reference_values=["no parent", "", "None"])
                ],
                default_values=[
                    ValueSettings(key_type="common", keys="parent_variant_label"),
                    ValueSettings(key_type="common", keys="variant_label")
                ]
            ),
            branch_time_in_parent=ParameterSettings(
                key="branch_time_in_parent",
                help="Branch time of the simulation in the parent's one.",
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
                                      check_to_do="neq", reference_values=["no parent", "", "None"])
                ],
                num_type="double",
                skip_values=["", "None", None],
                default_values=[
                    ValueSettings(func=FunctionSettings(
                        func=compute_nb_days,
                        options=dict(
                            year_ref=ValueSettings(key_type="common", keys="parent_time_ref_year"),
                            year_branch=ValueSettings(key_type="common", keys="branch_year_in_parent"),
                            month_branch=ValueSettings(key_type="common", keys="branch_month_in_parent")
                        ))),
                    ValueSettings(key_type="simulation", keys="branch_time_in_parent")
                ]
            ),
            branch_time_in_child=ParameterSettings(
                key="branch_time_in_child",
                help="Branch time of the simulation in the child's one.",
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
                                      check_to_do="neq", reference_values=["no parent", "", "None"])
                ],
                num_type="double",
                skip_values=["", "None", None],
                default_values=[
                    ValueSettings(func=FunctionSettings(
                        func=compute_nb_days,
                        options=dict(
                            year_ref=ValueSettings(key_type="simulation", keys="child_time_ref_year"),
                            year_branch=ValueSettings(key_type="simulation", keys="branch_year_in_child")
                        ))),
                    ValueSettings(key_type="simulation", keys="branch_time_in_child")
                ]
            ),
            branch_method=ParameterSettings(
                key="branch_method",
                help="Branch method of the simulation.",
                cases=[
                    CaseSettings(
                        conditions=[
                            ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
                                              check_to_do="neq", reference_values=["no parent", "", "None"])
                        ],
                        value=ValueSettings(key_type="common", keys="branch_method")
                    ),
                    CaseSettings(conditions=True, value="no parent")
                ]
            ),
            physics_index=ParameterSettings(
                key="physics_index",
                help="Physics index associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="physics_index")
                ],
                num_type="int"
            ),
            product=ParameterSettings(
                key="product",
                help="Type of content of the file.",
                default_values=["model-output", ]
            ),
            realization_index=ParameterSettings(
                key="realization_index",
                help="Realization index associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="internal", keys="realization_index")
                ],
                num_type="int"
            ),
            references=ParameterSettings(
                key="references",
                help="References associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="references")
                ]
            ),
            sub_experiment_id=ParameterSettings(
                key="sub_experiment_id",
                help="Id of the sub experiment associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="sub_experiment_id")
                ]
            ),
            sub_experiment=ParameterSettings(
                key="sub_experiment",
                help="Name of the sub experiment associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="sub_experiment")
                ]
            ),
            variant_info=ParameterSettings(
                key="variant_info",
                help="Variant information associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="variant_info",
                                  fmt=". Information provided by this attribute may in some cases be flawed. "
                                      "Users can find more comprehensive and up-to-date documentation via the "
                                      "further_info_url global attribute.")
                ]
            ),
            realm=ParameterSettings(
                key="realm",
                help="Realm associated with the file.",
                default_values=[
                    ValueSettings(key_type="variable", keys="modeling_realm")
                ]
            ),
            frequency=ParameterSettings(
                key="frequency",
                help="Frequency associated with the file.",
                default_values=[
                    ValueSettings(key_type="variable", keys="frequency")
                ]
            ),
            comment=ParameterSettings(
                key="comment",
                help="Comment associated with the file.",
                skip_values=["", ],
                cases=[
                    CaseSettings(
                        conditions=[
                            ConditionSettings(check_value=ValueSettings(key_type="variable", keys="comments"),
                                              check_to_do="neq", reference_values=["", "None", None])
                        ],
                        value=ValueSettings(
                            key_type="combine",
                            keys=[
                                ValueSettings(key_type="common", keys="comment_lab"),
                                ValueSettings(key_type="common", keys="comment_sim"),
                                ValueSettings(key_type="variable", keys="comments")
                            ],
                            fmt="{}{}{}"
                        )
                    ),
                    CaseSettings(
                        conditions=[
                            ConditionSettings(check_value=ValueSettings(key_type="common", keys="comment_sim"),
                                              check_to_do="neq", reference_values=["", "None", None]),
                            ConditionSettings(check_value=ValueSettings(key_type="common", keys="comment_lab"),
                                              check_to_do="neq", reference_values=["", "None", None])
                        ],
                        value=ValueSettings(
                            key_type="combine",
                            keys=[
                                ValueSettings(key_type="common", keys="comment_lab"),
                                ValueSettings(key_type="common", keys="comment_sim")
                            ],
                            fmt="{}{}"
                        )
                    ),
                    CaseSettings(
                        conditions=[
                            ConditionSettings(check_value=ValueSettings(key_type="common", keys="comment_sim"),
                                              check_to_do="neq", reference_values=["", "None", None])
                        ],
                        value=ValueSettings(key_type="common", keys="comment_sim")
                    ),
                    CaseSettings(
                        conditions=[
                            ConditionSettings(check_value=ValueSettings(key_type="common", keys="comment_lab"),
                                              check_to_do="neq", reference_values=["", "None", None])
                        ],
                        value=ValueSettings(key_type="common", keys="comment_lab")
                    )
                ]
            ),
            variant_label=ParameterSettings(
                key="variant_label",
                help="Variant label associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="variant_label")
                ]
            ),
            activity_id=ParameterSettings(
                key="activity_id",
                help="Activity id associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="activity_id")
                ]
            ),
            source=ParameterSettings(
                key="source",
                help="Model associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="common", keys="source")
                ]
            ),
            source_id=ParameterSettings(
                key="source_id",
                help="Model id associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="internal", keys="source_id")
                ]
            ),
            source_type=ParameterSettings(
                key="source_type",
                help="Model type associated with the simulation.",
                default_values=[
                    ValueSettings(key_type="internal", keys="source_type")
                ]
            ),
            title=ParameterSettings(
                key="title",
                help="Title of the file.",
                default_values=[
                    ValueSettings(
                        key_type="combine",
                        keys=[
                            ValueSettings(key_type="internal", keys="source_id"),
                            ValueSettings(key_type="internal", keys="project"),
                            ValueSettings(key_type="common", keys="activity_id"),
                            ValueSettings(key_type="simulation", keys="expid_in_filename")
                        ],
                        fmt="{} model output prepared for {} and {} / {} simulation"
                    ),
                    ValueSettings(
                        key_type="combine",
                        keys=[
                            ValueSettings(key_type="internal", keys="source_id"),
                            ValueSettings(key_type="internal", keys="project"),
                            ValueSettings(key_type="common", keys="activity_id"),
                            ValueSettings(key_type="internal", keys="experiment_id")
                        ],
                        fmt="{} model output prepared for {} / {} {}"
                    )
                ]
            )
        )
    ),
    field_group=TagSettings(
        attrs_list=["freq_op", "freq_offset"],
        attrs_constraints=dict(
            freq_op=ParameterSettings(
                key="freq_op",
                help="Frequency of the operation done on the field."
            ),
            freq_offset=ParameterSettings(
                key="freq_offset",
                help="Offset to be applied on operations on the field."
            )
        )
    ),
    field=TagSettings(
        attrs_list=["id", "field_ref", "name", "freq_op", "freq_offset", "grid_ref", "long_name", "standard_name",
                    "unit", "operation", "detect_missing_value", "prec"],
        attrs_constraints=dict(
            id=ParameterSettings(
                key="id",
                help="Id of the field."
            ),
            field_ref=ParameterSettings(
                key="field_ref",
                help="Id of the reference field."
            ),
            name=ParameterSettings(
                key="name",
                help="Name of the field."
            ),
            freq_op=ParameterSettings(
                key="freq_op",
                help="Frequency of the operation done on the field."
            ),
            freq_offset=ParameterSettings(
                key="freq_offset",
                help="Offset to be applied on operations on the field."
            ),
            grid_ref=ParameterSettings(
                key="grid_ref",
                help="Reference grid of the field."
            ),
            long_name=ParameterSettings(
                key="long_name",
                help="Long name of the field."
            ),
            standard_name=ParameterSettings(
                key="standard_name",
                help="Standard name of the field."
            ),
            unit=ParameterSettings(
                key="unit",
                help="Unit of the field."
            ),
            operation=ParameterSettings(
                key="operation",
                help="Operation done on the field."
            ),
            detect_missing_value=ParameterSettings(
                key="detect_missing_value",
                help="Should missing values of the field be detected by XIOS."
            ),
            prec=ParameterSettings(
                key="prec",
                help="Precision of the field."
            )
        )
    ),
    field_output=TagSettings(
        attrs_list=["field_ref", "name", "grid_ref", "freq_offset", "detect_missing_value", "default_value", "prec",
                    "cell_methods", "cell_methods_mode", "operation", "freq_op", "expr"],
        attrs_constraints=dict(
            name=ParameterSettings(
                key="name",
                help="Name of the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="mipVarLabel")
                ]
            ),
            field_ref=ParameterSettings(
                key="field_ref",
                help="Reference field."
            ),
            operation=ParameterSettings(
                key="operation",
                help="Operation performed on the field."
            ),
            grid_ref=ParameterSettings(
                key="grid_ref",
                help="Reference grid of the field.",
                skip_values=["", "None", None]
            ),
            freq_offset=ParameterSettings(
                key="freq_offset",
                help="Offset to be applied on operations on the field.",
                skip_values=["", "None", None]
            ),
            freq_op=ParameterSettings(
                key="freq_op",
                help="Frequency of the operation done on the field.",
                skip_values=["", "None", None]
            ),
            expr=ParameterSettings(
                key="expr",
                help="Expression used to compute the field.",
                skip_values=["", "None", None]
            ),
            cell_methods_mode=ParameterSettings(
                key="cell_methods_mode",
                help="Mode associated with the cell method of the field.",
                default_values=["overwrite", ]
            ),
            cell_methods=ParameterSettings(
                key="cell_methods",
                help="Cell method associated with the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="cell_methods")
                ]
            ),
            prec=ParameterSettings(
                key="prec",
                help="Precision of the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="prec")
                ],
                authorized_values=["2", "4", "8"],
                corrections={
                    "": "4",
                    "float": "4",
                    "real": "4",
                    "double": "8",
                    "integer": "2",
                    "int": "2"
                },
                fatal=True
            ),
            default_value=ParameterSettings(
                key="default_value",
                help="Default value associated with the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="prec")
                ],
                authorized_values=["0", "1.e+20"],
                corrections={
                    "": "1.e+20",
                    "float": "1.e+20",
                    "real": "1.e+20",
                    "double": "1.e+20",
                    "integer": "0",
                    "int": "0"
                },
                fatal=True
            ),
            detect_missing_value=ParameterSettings(
                key="detect_missing_value",
                help="Should missing values of the field be detected by XIOS.",
                default_values=["True", ]
            )
        ),
        vars_list=["comment", "standard_name", "description", "long_name", "positive", "history", "units",
                   "cell_methods", "cell_measures", "flag_meanings", "flag_values", "interval_operation"],
        vars_constraints=dict(
            standard_name=ParameterSettings(
                key="standard_name",
                help="Standard name of the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="stdname")
                ],
                skip_values=["", "None", None]
            ),
            description=ParameterSettings(
                key="description",
                help="Description associated with the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="description"),
                    "None"
                ],
                skip_values=["", ]
            ),
            long_name=ParameterSettings(
                key="long_name",
                help="Long name of the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="long_name")
                ]
            ),
            history=ParameterSettings(
                key="history",
                help="History associated with the field.",
                default_values=[
                    ValueSettings(key_type="common", keys="history")
                ]
            ),
            comment=ParameterSettings(
                key="comment",
                help="Comment associated with the field.",
                default_values=[
                    ValueSettings(
                        key_type="simulation",
                        keys=[
                            "comments",
                            ValueSettings(key_type="variable", keys="label")
                        ]
                    ),
                    ValueSettings(
                        key_type="laboratory",
                        keys=[
                            "comments",
                            ValueSettings(key_type="variable", keys="label")
                        ]
                    )
                ],
                skip_values=["", "None", None]
            ),
            positive=ParameterSettings(
                key="positive",
                help="Way the field should be interpreted.",
                default_values=[
                    ValueSettings(key_type="variable", keys="positive")
                ],
                skip_values=["", "None", None]
            ),
            detect_missing_value=ParameterSettings(
                key="detect_missing_value",
                help="Should missing values of the field be detected by XIOS.",
                default_values=["none", ]
            ),
            units=ParameterSettings(
                key="units",
                help="Units associated with the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="units")
                ],
                skip_values=["", "None", None]
            ),
            cell_methods=ParameterSettings(
                key="cell_methods",
                help="Cell method associated with the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="cell_methods")
                ],
                skip_values=["", "None", None]
            ),
            cell_measures=ParameterSettings(
                key="cell_measures",
                help="Cell measures associated with the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="cell_measures")
                ],
                skip_values=["", "None", None]
            ),
            flag_meanings=ParameterSettings(
                key="flag_meanings",
                help="Flag meanings associated with the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="flag_meanings")
                ],
                skip_values=["", "None", None]
            ),
            flag_values=ParameterSettings(
                key="flag_values",
                help="Flag values associated with the field.",
                default_values=[
                    ValueSettings(key_type="variable", keys="flag_values")
                ],
                skip_values=["", "None", None]
            ),
            interval_operation=ParameterSettings(
                key="interval_operation",
                help="Interval associated with the operation done on the field.",
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="dict", keys="operation"),
                                      check_to_do="neq", reference_values="once")
                ]
            )
        )
    ),
    grid=TagSettings(
        attrs_list=["id", ],
        attrs_constraints=dict(
            id=ParameterSettings(
                key="id",
                help="Id of the grid."
            )
        )
    ),
    axis=TagSettings(
        attrs_list=["id", "positive", "n_glo", "value", "axis_ref", "name", "standard_name", "long_name", "prec",
                    "unit", "value", "bounds", "dim_name", "label", "axis_type"],
        attrs_constraints=dict(
            id=ParameterSettings(
                key="id",
                help="Id of the axis."
            ),
            positive=ParameterSettings(
                key="positive",
                help="How is the axis oriented?"
            ),
            n_glo=ParameterSettings(
                key="n_glo",
                help="Number of values of this axis."
            ),
            axis_ref=ParameterSettings(
                key="axis_ref",
                help="Reference axis."
            ),
            name=ParameterSettings(
                key="name",
                help="Name of this axis."
            ),
            long_name=ParameterSettings(
                key="long_name",
                help="Long name of this axis."
            ),
            axis_type=ParameterSettings(
                key="axis_type",
                help="Axis type.",
                skip_values=["", "None", None]
            ),
            standard_name=ParameterSettings(
                key="standard_name",
                help="Standard name of the axis.",
                skip_values=["", "None", None],
                authorized_types=[str, ]
            ),
            prec=ParameterSettings(
                key="prec",
                help="Precision of the axis.",
                skip_values=["", "None", None],
                authorized_values=["2", "4", "8"],
                corrections={
                    "": "4",
                    "float": "4",
                    "real": "4",
                    "double": "8",
                    "integer": "2",
                    "int": "2"
                },
            ),
            unit=ParameterSettings(
                key="unit",
                help="Unit of the axis.",
                skip_values=["", "None", None]
            ),
            bounds=ParameterSettings(
                key="bounds",
                help="Bounds of the axis.",
                skip_values=["", "None", None]
            ),
            dim_name=ParameterSettings(
                key="dim_name",
                help="Name dimension of the axis.",
                skip_values=["", "None", None]
            ),
            label=ParameterSettings(
                key="label",
                help="Label of the axis.",
                skip_values=["", "None", None]
            ),
            value=ParameterSettings(
                key="value",
                help="Value of the axis.",
                skip_values=["", "None", None]
            )
        )
    ),
    zoom_axis=TagSettings(
        attrs_list=["index", ],
        attrs_constraints=dict(
            index=ParameterSettings(
                key="index",
                help="Index of the zoomed axis."
            )
        )
    ),
    interpolate_axis=TagSettings(
        attrs_list=["type", "order", "coordinate"],
        attrs_constraints=dict(
            type=ParameterSettings(
                key="type",
                help="Type of the interpolated axis."
            ),
            order=ParameterSettings(
                key="order",
                help="Order of the interpolated axis."
            ),
            coordinate=ParameterSettings(
                key="coordinate",
                help="Coordinate of the interpolated axis."
            )
        )
    ),
    axis_group=TagSettings(
        attrs_list=["prec", ],
        attrs_constraints=dict(
            prec=ParameterSettings(
                key="prec",
                help="Precision associated with the axis group.",
                default_values=["8", ],
                authorized_values=["2", "4", "8"],
                corrections={
                    "": "4",
                    "float": "4",
                    "real": "4",
                    "double": "8",
                    "integer": "2",
                    "int": "2"
                },
            )
        )
    ),
    domain=TagSettings(
        attrs_list=["id", "ni_glo", "nj_glo", "type", "prec", "lat_name", "lon_name", "dim_i_name", "domain_ref"],
        attrs_constraints=dict(
            id=ParameterSettings(
                key="id",
                help="Id of the domain."
            ),
            ni_glo=ParameterSettings(
                key="ni_glo",
                help="Number of points on i dimension."
            ),
            nj_glo=ParameterSettings(
                key="nj_glo",
                help="Number of points on j dimension."
            ),
            type=ParameterSettings(
                key="type",
                help="Type of the domain."
            ),
            prec=ParameterSettings(
                key="prec",
                help="Precision of the domain."
            ),
            lat_name=ParameterSettings(
                key="lat_name",
                help="Latitude axis name."
            ),
            lon_name=ParameterSettings(
                key="lon_name",
                help="Longitude axis name."
            ),
            dim_i_name=ParameterSettings(
                key="dim_i_name",
                help="Name of the i dimension."
            ),
            domain_ref=ParameterSettings(
                key="domain_ref",
                help="Reference domain."
            )
        )
    ),
    interpolate_domain=TagSettings(
        attrs_list=["type", "order", "renormalize", "mode", "write_weight", "coordinate"],
        attrs_constraints=dict(
            type=ParameterSettings(
                key="type",
                help="Type of the interpolated domain."
            ),
            order=ParameterSettings(
                key="order",
                help="Order of the interpolation."
            ),
            renormalize=ParameterSettings(
                key="renormalize",
                help="Should the interpolated domain be renormalized?"
            ),
            mode=ParameterSettings(
                key="mode",
                help="Mode used for the interpolation."
            ),
            write_weight=ParameterSettings(
                key="write_weight",
                help="Should interpolation weights be written?"
            ),
            coordinate=ParameterSettings(
                key="coordinate",
                help="Coordinate of the interpolated domain."
            )
        )
    ),
    domain_group=TagSettings(
        attrs_list=["prec", ],
        attrs_constraints=dict(
            prec=ParameterSettings(
                key="prec",
                help="Precision associated with the domain group.",
                default_values=["8", ],
                authorized_values=["2", "4", "8"],
                corrections={
                    "": "4",
                    "float": "4",
                    "real": "4",
                    "double": "8",
                    "integer": "2",
                    "int": "2"
                },
            )
        )
    ),
    scalar=TagSettings(
        attrs_list=["id", "scalar_ref", "name", "standard_name", "long_name", "label", "prec", "value", "bounds",
                    "bounds_name", "axis_type", "positive", "unit"],
        attrs_constraints=dict(
            id=ParameterSettings(
                key="id",
                help="Id of the scalar."
            ),
            scalar_ref=ParameterSettings(
                key="scalar_ref",
                help="Reference scalar."
            ),
            name=ParameterSettings(
                key="name",
                help="Name of the scalar."
            ),
            long_name=ParameterSettings(
                key="long_name",
                help="Long name of the scalar."
            ),
            standard_name=ParameterSettings(
                key="standard_name",
                help="Standard name of the scalar.",
                skip_values=["", "None", None]
            ),
            axis_type=ParameterSettings(
                key="axis_type",
                help="Axis type of the scalar.",
                skip_values=["", "None", None]
            ),
            unit=ParameterSettings(
                key="unit",
                help="Unit of the scalar.",
                skip_values=["", "None", None]
            ),
            label=ParameterSettings(
                key="label",
                help="Label of the scalar.",
                skip_values=["", "None", None]
            ),
            bounds=ParameterSettings(
                key="bounds",
                help="Bounds of the scalar.",
                skip_values=["", "None", None]
            ),
            bounds_name=ParameterSettings(
                key="bounds_name",
                help="Bounds name of the scalar.",
                skip_values=["", "None", None]
            ),
            prec=ParameterSettings(
                key="prec",
                help="Precision of the scalar.",
                skip_values=["", "None", None],
                authorized_values=["2", "4", "8"],
                corrections={
                    "": "4",
                    "float": "4",
                    "real": "4",
                    "double": "8",
                    "integer": "2",
                    "int": "2"
                },
            ),
            value=ParameterSettings(
                key="value",
                help="Value of the scalar.",
                skip_values=["", "None", None]
            ),
            positive=ParameterSettings(
                key="positive",
                help="Orientation of the scalar.",
                skip_values=["", "None", None]
            )
        )
    )
)
