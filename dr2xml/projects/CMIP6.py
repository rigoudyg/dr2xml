#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CMIP6 python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.projects.projects_interface_definitions import ParameterSettings, ValueSettings, FunctionSettings, \
    TagSettings, ConditionSettings

parent_project_settings = "basics"


def make_source_string(source, source_id):
    """
    From the dic of sources in CMIP6-CV, Creates the string representation of a
    given model (source_id) according to doc on global_file_attributes, so :

    <modified source_id> (<year>): atmosphere: <model_name> (<technical_name>, <resolution_and_levels>);
    ocean: <model_name> (<technical_name>, <resolution_and_levels>); sea_ice: <model_name> (<technical_name>);
    land: <model_name> (<technical_name>); aerosol: <model_name> (<technical_name>);
    atmospheric_chemistry <model_name> (<technical_name>); ocean_biogeochemistry <model_name> (<technical_name>);
    land_ice <model_name> (<technical_name>);

    """
    # mpmoine_correction:make_source_string: pour lire correctement le fichier 'CMIP6_source_id.json'
    components = source['model_component']
    rep = source_id + " (" + source['release_year'] + "):"
    for realm in ["aerosol", "atmos", "atmosChem", "land", "ocean", "ocnBgchem", "seaIce"]:
        component = components[realm]
        description = component['description']
        if description != "none":
            rep = rep + "\n" + realm + ": " + description
    return rep


def build_filename(frequency, prefix, table, source_id, expid_in_filename, member_id, grid_label, date_range,
                   var_type, list_perso_dev_file, label, mipVarLabel, use_cmorvar=False):
    if "fx" in frequency:
        varname_for_filename = label
    else:
        if use_cmorvar:
            varname_for_filename = label
        else:
            varname_for_filename = mipVarLabel
        # DR21 has a bug with tsland : the MIP variable is named "ts"
        if label in ["tsland", ]:
            varname_for_filename = "tsland"
    filename = "_".join(([varname_for_filename, table, source_id, expid_in_filename, member_id, grid_label]))
    if var_type in ["perso", "dev"]:
        with open(list_perso_dev_file, mode="a", encoding="utf-8") as list_perso_and_dev:
            list_perso_and_dev.write(".*{}.*\n".format(filename))
    filename = prefix + filename
    if "fx" not in frequency:
        if frequency in ["1hrCM", "monC"]:
            suffix = "-clim"
        else:
            suffix = ""
        filename = "_".join([filename, date_range + suffix])
    return filename


def fill_license(value, institution_id, info_url):
    value = value.replace("<Your Centre Name>", institution_id)
    # TODO: Adapt next line
    value = value.replace("[NonCommercial-]", "NonCommercial-")
    value = value.replace("[ and at <some URL maintained by modeling group>]", " and at " + info_url)
    return value


internal_values = dict(
    required_model_components=ParameterSettings(
        key="required_model_components",
        default_values=[
            ValueSettings(
                key_type="internal",
                keys=["CV_experiment", "required_model_components"]
            )
        ]
    ),
    additional_allowed_model_components=ParameterSettings(
        key="additional_allowed_model_components",
        default_values=[
            ValueSettings(
                key_type="internal",
                keys=["CV_experiment", "additional_allowed_model_components"]
            )
        ]
    ),
    CV_experiment=ParameterSettings(
        key="CV_experiment",
        default_values=[
            ValueSettings(
                key_type="json",
                keys=[
                    "experiment_id",
                    ValueSettings(key_type="internal", keys="experiment_id")
                ],
                src=ValueSettings(
                    key_type="combine",
                    keys=[
                        ValueSettings(key_type="dict", keys="cvspath"),
                        ValueSettings(key_type="internal", keys="project")
                    ],
                    fmt="{}{}_experiment_id.json"
                )
            )
        ]
    )
)

common_values = dict(
    conventions_version=ParameterSettings(
        key="conventions_version",
        default_values=[
            ValueSettings(key_type="config", keys="CMIP6_conventions_version")
        ]
    ),
    activity_id=ParameterSettings(
        key="activity_id",
        default_values=[
            ValueSettings(key_type="simulation", keys="activity_id"),
            ValueSettings(key_type="laboratory", keys="activity_id"),
            ValueSettings(key_type="internal", keys=["CV_experiment", "activity_id"])
        ]
    ),
    parent_activity_id=ParameterSettings(
        key="parent_activity_id",
        default_values=[
            ValueSettings(key_type="simulation", keys="parent_activity_id"),
            ValueSettings(key_type="simulation", keys="activity_id"),
            ValueSettings(key_type="laboratory", keys="parent_activity_id"),
            ValueSettings(key_type="laboratory", keys="activity_id"),
            ValueSettings(key_type="internal", keys=["CV_experiment", "parent_activity_id"])
        ]
    ),
    HDL=ParameterSettings(
        key="HDL",
        default_values=[
            ValueSettings(key_type="simulation", keys="HDL"),
            ValueSettings(key_type="laboratory", keys="HDL"),
            "21.14100"
        ]
    ),
    source=ParameterSettings(
        key="source",
        default_values=[
            ValueSettings(
                key_type="json",
                keys=[
                    "source_id",
                    ValueSettings(key_type="internal", keys="source_id")
                ],
                src=ValueSettings(
                    key_type="combine",
                    keys=[
                        ValueSettings(key_type="dict", keys="cvspath"),
                        ValueSettings(key_type="internal", keys="project")
                    ],
                    fmt="{}{}_source_id.json"
                ),
                func=FunctionSettings(
                    func=make_source_string,
                    options=dict(source_id=ValueSettings(key_type="internal", keys="source_id"))
                )
            ),
            ValueSettings(key_type="laboratory", keys="source")
        ]
    ),
    institution=ParameterSettings(
        key="institution",
        default_values=[
            ValueSettings(key_type="laboratory", keys="institution"),
            ValueSettings(
                key_type="json",
                keys=[
                    "institution_id",
                    ValueSettings(key_type="internal", keys="institution_id")
                ],
                src=ValueSettings(
                    key_type="combine",
                    keys=[
                        ValueSettings(key_type="dict", keys="cvspath"),
                        ValueSettings(key_type="internal", keys="project")
                    ],
                    fmt="{}{}_institution_id.json"
                )
            )
        ]
    ),
    license=ParameterSettings(
        key="license",
        default_values=[
            ValueSettings(
                key_type="json",
                keys=["license", 0],
                src=ValueSettings(
                    key_type="combine",
                    keys=[
                        ValueSettings(key_type="dict", keys="cvspath"),
                        ValueSettings(key_type="internal", keys="project")
                    ],
                    fmt="{}{}_license.json"
                )
            )
        ]
    ),
    parent_experiment_id=ParameterSettings(
        key="parent_experiment_id",
        default_values=[
            ValueSettings(key_type="simulation", keys="parent_experiment_id"),
            ValueSettings(key_type="laboratory", keys="parent_experiment_id"),
            ValueSettings(key_type="internal", keys=["CV_experiment", "parent_experiment_id"])
        ]
    ),
    variant_label=ParameterSettings(
        key="variant_label",
        default_values=[
            ValueSettings(
                key_type="combine",
                keys=[
                    ValueSettings(key_type="internal", keys="realization_index"),
                    ValueSettings(key_type="common", keys="initialization_index"),
                    ValueSettings(key_type="common", keys="physics_index"),
                    ValueSettings(key_type="common", keys="forcing_index")
                ],
                fmt="r{}i{}p{}f{}"
            )
        ]
    ),
    member_id=ParameterSettings(
        key="member_id",
        default_values=[
            ValueSettings(
                key_type="combine",
                keys=[
                    ValueSettings(key_type="common", keys="sub_experiment_id"),
                    ValueSettings(key_type="common", keys="variant_label"),
                ],
                fmt="{}-{}"
            ),
            ValueSettings(key_type="common", keys="variant_label")
        ],
        forbidden_patterns=["none-.*", ]
    )
)

project_settings = dict(
    context=TagSettings(
        comments_list=["DR_version", "CV_version", "conventions_version", "dr2xml_version", "lab_settings",
                       "simulation_settings", "year"],
        comments_constraints=dict(
            CV_version=ParameterSettings(
                key="CV_version",
                default_values=["CMIP6-CV version ??", ]
            ),
            conventions_version=ParameterSettings(
                key="conventions_version",
                default_values=[
                    ValueSettings(key_type="common", keys="conventions_version", fmt="CMIP6_conventions_version {}")
                ]
            )
        )
    ),
    file_output=TagSettings(
        attrs_constraints=dict(
            name=ParameterSettings(
                key="name",
                default_values=[
                    ValueSettings(func=FunctionSettings(
                        func=build_filename,
                        options=dict(
                            frequency=ValueSettings(key_type="variable", keys="frequency"),
                            prefix=ValueSettings(key_type="common", keys="prefix"),
                            table=ValueSettings(key_type="dict", keys="table_id"),
                            source_id=ValueSettings(key_type="internal", keys="source_id"),
                            expid_in_filename=ValueSettings(key_type="common", keys="expid_in_filename"),
                            member_id=ValueSettings(key_type="common", keys="member_id"),
                            grid_label=ValueSettings(key_type="dict", keys="grid_label"),
                            date_range=ValueSettings(key_type="common", keys="date_range"),
                            var_type=ValueSettings(key_type="variable", keys="type"),
                            list_perso_dev_file=ValueSettings(key_type="common", keys="list_perso_dev_file"),
                            label=ValueSettings(key_type="variable", keys="label"),
                            mipVarLabel=ValueSettings(key_type="variable", keys="mipVarLabel"),
                            use_cmorvar=ValueSettings(key_type="internal", keys="use_cmorvar_label_in_filename")
                        )
                    ))
                ],
                fatal=True
            )
        ),
        vars_constraints=dict(
            variable_id=ParameterSettings(
                key="variable_id",
                default_values=[
                    ValueSettings(key_type="variable", keys="mipVarLabel")
                ]
            ),
            description=ParameterSettings(
                key="description",
                default_values=[
                    ValueSettings(key_type="common", keys="description"),
                    ValueSettings(key_type="internal", keys=["CV_experiment", "description"])
                ]
            ),
            title_desc=ParameterSettings(
                key="title_desc",
                default_values=[
                    ValueSettings(key_type="common", keys="description"),
                    ValueSettings(key_type="internal", keys=["CV_experiment", "description"])
                ]
            ),
            experiment=ParameterSettings(
                key="experiment",
                default_values=[
                    ValueSettings(key_type="common", keys="experiment"),
                    ValueSettings(key_type="internal", keys=["CV_experiment", "experiment"])
                ]
            ),
            CMIP6_CV_latest_tag=ParameterSettings(
                key="CMIP6_CV_latest_tag",
                default_values=[
                    ValueSettings(
                        key_type="json",
                        keys=["version_metadata", "latest_tag_metadata"],
                        src=ValueSettings(
                            key_type="combine",
                            keys=[
                                ValueSettings(key_type="dict", keys="cvspath"),
                                ValueSettings(key_type="internal", keys="project")
                            ],
                            fmt="{}{}_experiment_id.json"
                        )
                    ),
                    "no more value in CMIP6_CV"
                ]
            ),
            source=ParameterSettings(
                key="source",
                fatal=True
            ),
            further_info_url=ParameterSettings(
                key="further_info_url",
                default_values=[
                    ValueSettings(
                        key_type="combine",
                        keys=[
                            ValueSettings(key_type="variable", keys="mip_era"),
                            ValueSettings(key_type="internal", keys="institution_id"),
                            ValueSettings(key_type="internal", keys="source_id"),
                            ValueSettings(key_type="common", keys="expid_in_filename"),
                            ValueSettings(key_type="common", keys="sub_experiment_id"),
                            ValueSettings(key_type="common", keys="variant_label")
                        ],
                        fmt="https://furtherinfo.es-doc.org/{}.{}.{}.{}.{}.{}"
                    )
                ],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="laboratory", keys="mip_era"),
                                      check_to_do="eq", reference_values=list()),
                    ConditionSettings(check_value=ValueSettings(key_type="simulation", keys="mip_era"),
                                      check_to_do="eq", reference_values=list())
                ]
            ),
            license=ParameterSettings(
                key="license",
                default_values=[
                    ValueSettings(
                        key_type="common",
                        keys="license",
                        func=FunctionSettings(
                            func=fill_license,
                            options=dict(
                                institution_id=ValueSettings(key_type="internal", keys="institution_id"),
                                info_url=ValueSettings(key_type="common", keys="info_url")
                            )
                        )
                    )
                ]
            ),
            realm=ParameterSettings(
                key="realm",
                corrections=dict(
                    ocnBgChem="ocnBgchem"
                )
            )
        )
    )
)
