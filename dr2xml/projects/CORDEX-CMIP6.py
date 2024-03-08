#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CORDEX python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.projects.projects_interface_definitions import ParameterSettings, ValueSettings, TagSettings, \
    FunctionSettings, ConditionSettings


def build_filename(frequency, prefix, source_id, expid_in_filename, date_range, var_type, list_perso_dev_file, label,
                   mipVarLabel, domain_id, driving_source_id, driving_variant_label, rcm_version_id, institution_id,
                   source_configuration_id, use_cmorvar=False):
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
    filename = "_".join(([elt for elt in [varname_for_filename, domain_id, driving_source_id, expid_in_filename,
                                          driving_variant_label, institution_id, source_id, rcm_version_id,
                                          source_configuration_id, frequency] if
                          len(str(elt)) > 0]))
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


parent_project_settings = "basics"

internal_values = dict(
    required_model_components=ParameterSettings(
        key="required_model_components",
        default_values=[
            list()
        ]
    ),
    additional_allowed_model_components=ParameterSettings(
        key="additional_allowed_model_components",
        default_values=[
            list()
        ]
    )
)

common_values = dict(
    conventions_version=ParameterSettings(
        key="conventions_version",
        default_values=[
            ValueSettings(key_type="config", keys="CMIP6_conventions_version")
        ],
        help="Version of the conventions used."
    ),
    HDL=ParameterSettings(
        key="HDL",
        default_values=[
            ValueSettings(key_type="simulation", keys="HDL"),
            ValueSettings(key_type="laboratory", keys="HDL"),
            "21.14103"
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
        ],
        help="Label of the variant done."
    ),
    domain=ParameterSettings(
        key="domain",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys=[
                    "domain",
                    ValueSettings(key_type="internal", keys="context")
                ]
            )
        ],
        help="Dictionary which contains, for each context, the associated domain."
    ),
    domain_id=ParameterSettings(
        key="domain_id",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys=[
                    "domain_id",
                    ValueSettings(key_type="internal", keys="context")
                ]
            )
        ],
        help="Dictionary which contains, for each context, the associated domain id."
    ),
    version_realisation=ParameterSettings(
        key="version_realisation",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="version_realisation"
            )
        ],
        help="Version of the realisation done."
    ),
    driving_source_id=ParameterSettings(
        key="driving_source_id",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_source_id"
            )
        ],
        help="Id of the driving model."
    ),
    driving_variant_label=ParameterSettings(
        key="driving_variant_label",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_variant_label"
            )
        ],
        help="Id of the driving variant."
    ),
    driving_experiment_id=ParameterSettings(
        key="driving_experiment_id",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_experiment_id"
            )
        ],
        help="Id of the experiment which drives the current simulation."
    ),
    driving_institution_id=ParameterSettings(
        key="driving_institution_id",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_institution_id"
            )
        ],
        help="Id of the institution of the driving model."
    ),
    driving_experiment=ParameterSettings(
        key="driving_experiment",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_experiment"
            )
        ],
        help="Id of the experiment which drives the current simulation."
    ),
    Lambert_conformal_longitude_of_central_meridian=ParameterSettings(
        key="Lambert_conformal_longitude_of_central_meridian",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="Lambert_conformal_longitude_of_central_meridian"
            )
        ],
        help="Longitude of central meridian of the Lambert conformal projection."
    ),
    Lambert_conformal_standard_parallel=ParameterSettings(
        key="Lambert_conformal_standard_parallel",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="Lambert_conformal_standard_parallel"
            )
        ],
        help="Standard parallel of the Lambert conformal projection."
    ),
    Lambert_conformal_latitude_of_projection_origin=ParameterSettings(
        key="Lambert_conformal_latitude_of_projection_origin",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="Lambert_conformal_latitude_of_projection_origin"
            )
        ],
        help="Latitude of central meridian of the Lambert conformal projection."
    ),
    rcm_version_id=ParameterSettings(
        key="rcm_version_id",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="rcm_version_id"
            )
        ],
        help="Version id of the regional model used."
    )
)

project_settings = dict(
    context=TagSettings(
        comments_list=["DR_version", "CV_version", "conventions_version", "dr2xml_version", "lab_settings",
                       "simulation_settings", "year"],
        comments_constraints=dict(
            CV_version=ParameterSettings(
                key="CV_version",
                help="Controled vocabulary version used.",
                default_values=["CMIP6-CV version ??", ]
            ),
            conventions_version=ParameterSettings(
                key="conventions_version",
                help="Conventions version used.",
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
                            source_id=ValueSettings(key_type="internal", keys="source_id"),
                            expid_in_filename=ValueSettings(key_type="common", keys="expid_in_filename"),
                            date_range=ValueSettings(key_type="common", keys="date_range"),
                            var_type=ValueSettings(key_type="variable", keys="type"),
                            list_perso_dev_file=ValueSettings(key_type="common", keys="list_perso_dev_file"),
                            label=ValueSettings(key_type="variable", keys="label"),
                            mipVarLabel=ValueSettings(key_type="variable", keys="mipVarLabel"),
                            use_cmorvar=ValueSettings(key_type="internal", keys="use_cmorvar_label_in_filename"),
                            domain_id=ValueSettings(key_type="common", keys="domain_id"),
                            driving_source_id=ValueSettings(key_type="common", keys="driving_source_id"),
                            driving_variant_label=ValueSettings(key_type="common", keys="driving_variant_label"),
                            rcm_version_id=ValueSettings(key_type="common", keys="rcm_version_id"),
                            institution_id=ValueSettings(key_type="common", keys="institution_id"),
                            source_configuration_id=ValueSettings(key_type="common", keys="source_configuration_id")
                        )
                    ))
                ],
                fatal=True
            )
        ),
        vars_list=["activity_id", "contact", "data_specs_version", "dr2xml_version", "expid_in_filename",
                   "external_variables", "frequency", "grid", "grid_label", "nominal_resolution", "comment", "history",
                   "institution_id", "domain", "domain_id", "driving_source_id", "driving_variant_label",
                   "driving_experiment_id", "driving_experiment", "driving_institution_id",
                   "Lambert_conformal_longitude_of_central_meridian", "Lambert_conformal_standard_parallel",
                   "Lambert_conformal_latitude_of_projection_origin", "institution", "parent_experiment_id",
                   "parent_mip_era", "parent_activity_id", "parent_source_id", "parent_time_units",
                   "parent_variant_label", "branch_time_in_parent", "branch_time_in_child", "product", "mip_era",
                   "realization_index", "realm", "references", "source", "source_id", "source_type", "table_id",
                   "title", "variable_id", "version_realisation"],
        vars_constraints=dict(
            variable_id=ParameterSettings(
                key="variable_id",
                default_values=[
                    ValueSettings(key_type="variable", keys="mipVarLabel")
                ]
            ),
            nominal_resolution=ParameterSettings(
                key="nominal_resolution",
                output_key="native_resolution",
                help="Nominal resolution of the model."
            ),
            driving_institution_id=ParameterSettings(
                key="driving_institution_id",
                help="Id of the institution of the driving model."
            ),
            version_realisation=ParameterSettings(
                key="version_realisation",
                default_values=[
                    ValueSettings(key_type="common", keys="version_realisation")
                ],
                help="Version of the realisation done."
            ),
            domain=ParameterSettings(
                key="domain",
                default_values=[
                    ValueSettings(key_type="common", keys="domain")
                ],
                help="Dictionary which contains, for each context, the associated domain."
            ),
            domain_id=ParameterSettings(
                key="domain_id",
                default_values=[
                    ValueSettings(key_type="common", keys="domain_id")
                ],
                help="Dictionary which contains, for each context, the associated domain id."
            ),
            driving_source_id=ParameterSettings(
                key="driving_source_id",
                default_values=[
                    ValueSettings(key_type="common", keys="driving_source_id")
                ],
                fatal=True,
                help="Member of the simulation which drives the simulation."
            ),
            driving_variant_label=ParameterSettings(
                key="driving_variant_label",
                default_values=[
                    ValueSettings(key_type="common", keys="driving_variant_label")
                ],
                fatal=True,
                help="Id of the driving variant."
            ),
            driving_experiment_id=ParameterSettings(
                key="driving_experiment_id",
                default_values=[
                    ValueSettings(key_type="common", keys="driving_experiment_id")
                ],
                fatal=True,
                help="Id of the experiment which drives the current simulation."
            ),
            driving_experiment=ParameterSettings(
                key="driving_experiment",
                default_values=[
                    ValueSettings(key_type="common", keys="driving_experiment")
                ],
                fatal=True,
                help="Id of the experiment which drives the current simulation."
            ),
            Lambert_conformal_longitude_of_central_meridian=ParameterSettings(
                key="Lambert_conformal_longitude_of_central_meridian",
                default_values=[
                    ValueSettings(key_type="common", keys="Lambert_conformal_longitude_of_central_meridian")
                ],
                skip_values=["", "None", None],
                conditions=[
                    ConditionSettings(
                        check_value=ValueSettings(key_type="internal", keys="context"),
                        check_to_do="eq", reference_values="surfex"
                    )
                ],
                help="Longitude of central meridian of the Lambert conformal projection."
            ),
            Lambert_conformal_standard_parallel=ParameterSettings(
                key="Lambert_conformal_standard_parallel",
                default_values=[
                    ValueSettings(key_type="common", keys="Lambert_conformal_standard_parallel")
                ],
                skip_values=["", "None", None],
                conditions=[
                    ConditionSettings(
                        check_value=ValueSettings(key_type="internal", keys="context"),
                        check_to_do="eq", reference_values="surfex"
                    )
                ],
                help="Standard parallel of the Lambert conformal projection."
            ),
            Lambert_conformal_latitude_of_projection_origin=ParameterSettings(
                key="Lambert_conformal_latitude_of_projection_origin",
                default_values=[
                    ValueSettings(key_type="common", keys="Lambert_conformal_latitude_of_projection_origin")
                ],
                skip_values=["", "None", None],
                conditions=[
                    ConditionSettings(
                        check_value=ValueSettings(key_type="internal", keys="context"),
                        check_to_do="eq", reference_values="surfex"
                    )
                ],
                help="Latitude of central meridian of the Lambert conformal projection."
            ),
            product=ParameterSettings(
                key="product",
                default_values=["output", ]
            ),
            source=ParameterSettings(
                key="source",
                fatal=True,
                output_key="project_id"
            ),
            source_id=ParameterSettings(
                key="source_id",
                output_key="model_id"
            ),
            title=ParameterSettings(
                key="title",
                default_values=[
                    ValueSettings(
                        key_type="combine",
                        keys=[
                            ValueSettings(key_type="internal", keys="source_id"),
                            "CMIP6",
                            ValueSettings(key_type="common", keys="activity_id"),
                            ValueSettings(key_type="simulation", keys="expid_in_filename")
                        ],
                        fmt="{} model output prepared for {} and {} / {} simulation"
                    ),
                    ValueSettings(
                        key_type="combine",
                        keys=[
                            ValueSettings(key_type="internal", keys="source_id"),
                            "CMIP6",
                            ValueSettings(key_type="common", keys="activity_id"),
                            ValueSettings(key_type="internal", keys="experiment_id")
                        ],
                        fmt="{} model output prepared for {} / {} {}"
                    )
                ]
            )
        )
    ),
    field_output=TagSettings(
        attrs_constraints=dict(
            cell_methods=ParameterSettings(
                key="cell_methods",
                corrections={
                    "area: time: mean": "time: mean"
                }
            )
        ),
        vars_list=["comment", "standard_name", "description", "long_name", "history", "units",
                   "cell_methods", "cell_measures", "flag_meanings", "flag_values", "grid_mapping"],
        vars_constraints=dict(
            grid_mapping=ParameterSettings(
                key="grid_mapping",
                help="Grid mapping associated with the file.",
                default_values=["Lambert_Conformal", ],
                conditions=[
                    ConditionSettings(check_value=ValueSettings(key_type="internal", keys="context"),
                                      check_to_do="eq", reference_values="surfex")
                ]
            ),
            cell_methods=ParameterSettings(
                key="cell_methods",
                corrections={
                    "area: time: mean": "time: mean"
                }
            )
        )
    )
)