#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CMIP6 python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.projects.projects_interface_definitions import ParameterSettings, ValueSettings, FunctionSettings, \
    TagSettings, ConditionSettings

parent_project_settings = "basics"


def build_filename(expid_in_filename, realm, frequency, label, date_range, var_type, list_perso_dev_file):
    if isinstance(realm, (list, tuple)):
        realm = realm[0]
    filename = "_".join(([expid_in_filename, realm, frequency, label]))
    if var_type in ["perso", "dev"]:
        with open(list_perso_dev_file, mode="a", encoding="utf-8") as list_perso_and_dev:
            list_perso_and_dev.write("{}.*\n".format(filename))
    filename = "_".join([filename, date_range + ".nc"])
    return filename


def convert_frequency(freq):
    if freq.endswith("hr"):
        freq = freq.replace("hr", "hourly")
    elif freq.endswith("h"):
        freq = freq.replace("h", "hourly")
    elif freq in ["day", ]:
        freq = "daily"
    elif freq in ["mon", ]:
        freq = "monthly"
    return freq


def convert_realm(realm):
    if realm in ["ocean", "seaIce"]:
        realm = "nemo",
    if realm in ["land", ]:
        realm = "atmo"
    return realm


def build_string_from_list(args):
    return ", ".join(args)


internal_values = dict()

common_values = dict(
    grid_mapping=ParameterSettings(
        key="grid_mapping",
        default_values=[
            ValueSettings(key_type="simulation", keys="grid_mapping")
        ]
    ),
    forecast_reference_time=ParameterSettings(
        key="forecast_reference_time",
        default_values=[
            ValueSettings(key_type="simulation", keys="forecast_reference_time")
        ]
    ),
    forecast_type=ParameterSettings(
        key="forecast_type",
        default_values=[
            ValueSettings(key_type="simulation", keys="forecast_type")
        ]
    ),
    convention_str=ParameterSettings(
        key="convention_str",
        default_values=[
            ValueSettings(key_type="laboratory", keys="convention_str")
        ]
    ),
    commit=ParameterSettings(
        key="commit",
        default_values=[
            ValueSettings(key_type="simulation", keys="commit"),
            ValueSettings(key_type="laboratory", keys="commit")
        ]
    ),
    summary=ParameterSettings(
        key="summary",
        default_values=[
            ValueSettings(key_type="simulation", keys="summary"),
            ValueSettings(key_type="laboratory", keys="summary")
        ]
    ),
    keywords=ParameterSettings(
        key="keywords",
        default_values=[
            ValueSettings(key_type="simulation", keys="keywords",
                          func=FunctionSettings(func=build_string_from_list)),
            ValueSettings(key_type="laboratory", keys="summary",
                          func=FunctionSettings(func=build_string_from_list))
        ]
    )
)

project_settings = dict(
    file_output=TagSettings(
        attrs_constraints=dict(
            name=ParameterSettings(
                key="name",
                default_values=[
                    ValueSettings(func=FunctionSettings(
                        func=build_filename,
                        options=dict(
                            frequency=ValueSettings(key_type="variable", keys="frequency",
                                                    func=FunctionSettings(func=convert_frequency)),
                            expid_in_filename=ValueSettings(key_type="common", keys="expid_in_filename"),
                            date_range=ValueSettings(key_type="common", keys="date_range"),
                            list_perso_dev_file=ValueSettings(key_type="common", keys="list_perso_dev_file"),
                            var_type=ValueSettings(key_type="variable", keys="type"),
                            label=ValueSettings(key_type="variable", keys="label"),
                            realm=ValueSettings(key_type="variable", keys="modeling_realm",
                                                    func=FunctionSettings(func=convert_realm))
                        )
                    ))
                ],
                fatal=True
            ),
            uuid_name=ParameterSettings(
                key="uuid_name",
                default_values=["uuid", ]
            ),
            uuid_format=ParameterSettings(
                key="uuid_format",
                default_values=["%uuid%", ]
            )
        ),
        vars_list=["description", "title", "source", "institution_id", "institution", "contact", "project", "comment",
                   "forecast_type", "realm", "frequency", "level_type", "history", "references", "commit", "summary",
                   "keywords", "forecast_reference_time"],
        vars_constraints=dict(
            institution_id=ParameterSettings(
                key="institution_id",
                output_key="institute_id"
            ),
            forecast_type=ParameterSettings(
                key="forecast_type",
                default_values=[
                    ValueSettings(key_type="common", keys="forecast_type")
                ]
            ),
            realm=ParameterSettings(
                key="realm",
                output_key="modeling_realm",
                default_values=[
                    ValueSettings(key_type="variable", keys="modeling_realm", func=FunctionSettings(func=convert_realm))
                ]
            ),
            level_type=ParameterSettings(
                key="level_type",
                default_values=[
                    ValueSettings(key_tyoe="variable", keys="level_type")
                ]
            ),
            commit=ParameterSettings(
                key="commit",
                default_values=[
                    ValueSettings(key_type="common", keys="commit")
                ]
            ),
            summary=ParameterSettings(
                key="summary",
                default_values=[
                    ValueSettings(key_type="common", keys="summary")
                ]
            ),
            forecast_reference_time=ParameterSettings(
                key="forecast_reference_time",
                default_values=[
                    ValueSettings(key_type="common", keys="forecast_reference_time")
                ]
            )
        )
    ),
    field_output=TagSettings(
        vars_list=["standard_name", "long_name", "coordinates", "grid_mapping", "units"],
        vars_constraints=dict(
            grid_mapping=ParameterSettings(
                key="grid_mapping",
                default_values=[
                    ValueSettings(key_type="common", keys="grid_mapping")
                ]
            ),
            coordinates=ParameterSettings(
                key="coordinates",
                default_values=[
                    ValueSettings(key_type="variable", keys="coordinates")
                ]
            )
        )
    )
)
