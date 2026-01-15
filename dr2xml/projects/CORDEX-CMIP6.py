#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CORDEX python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.projects.projects_interface_definitions import ParameterSettings, ValueSettings, TagSettings, \
    FunctionSettings, ConditionSettings


def build_filename(frequency, prefix, source_id, expid_in_filename, date_range, var_type, list_perso_dev_file, label,
                   mipVarLabel, domain_id, driving_source_id, driving_variant_label, institution_id,
                   version_realization, use_cmorvar=False):
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
                                          driving_variant_label, institution_id, source_id,
                                          version_realization, frequency] if
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
            "CF-1.11",
            ValueSettings(key_type="laboratory", keys="conventions_version")
        ]
    ),
    HDL=ParameterSettings(
        key="HDL",
        default_values=[
            ValueSettings(key_type="simulation", keys="HDL"),
            ValueSettings(key_type="laboratory", keys="HDL"),
            "21.14103"
        ]
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
        ]
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
        ]
    ),
    driving_experiment=ParameterSettings(
        key="driving_experiment",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_experiment"
            )
        ]
    ),
    driving_experiment_id=ParameterSettings(
        key="driving_experiment_id",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_experiment_id"
            )
        ]
    ),
    driving_institution_id=ParameterSettings(
        key="driving_institution_id",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_institution_id"
            )
        ]
    ),
    driving_source_id=ParameterSettings(
        key="driving_source_id",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_source_id"
            )
        ]
    ),
    driving_variant_label=ParameterSettings(
        key="driving_variant_label",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="driving_variant_label"
            )
        ]
    ),
    version_realization=ParameterSettings(
        key="version_realization",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="version_realization"
            ),
            "v1-r1"
        ]
    ),
    Lambert_conformal_longitude_of_central_meridian=ParameterSettings(
        key="Lambert_conformal_longitude_of_central_meridian",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="Lambert_conformal_longitude_of_central_meridian"
            )
        ]
    ),
    Lambert_conformal_standard_parallel=ParameterSettings(
        key="Lambert_conformal_standard_parallel",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="Lambert_conformal_standard_parallel"
            )
        ]
    ),
    Lambert_conformal_latitude_of_projection_origin=ParameterSettings(
        key="Lambert_conformal_latitude_of_projection_origin",
        default_values=[
            ValueSettings(
                key_type="simulation",
                keys="Lambert_conformal_latitude_of_projection_origin"
            )
        ]
    ),
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
                            institution_id=ValueSettings(key_type="internal", keys="institution_id"),
                            version_realization=ValueSettings(key_type="common", keys="version_realization")
                        )
                    ))
                ],
                fatal=True
            )
        ),
        vars_list=["activity_id", "comment", "contact", "conventions_version", "dr2xml_version", 
                    "domain", "domain_id", 
                   "driving_experiment", "driving_experiment_id", "driving_institution_id",
                   "driving_source_id", "driving_variant_label",
                   "expid_in_filename", # EXPID
                   "external_variables", "frequency", "grid",
                   "history","institution","institution_id",
                   "Lambert_conformal_longitude_of_central_meridian", "Lambert_conformal_standard_parallel",
                   "Lambert_conformal_latitude_of_projection_origin",
                   "license",  "mip_era", "nominal_resolution",
                   "product", "project_id",
                   "realm", "references", "source", "source_id", "source_type", 
                   "title", "variable_id", "version_realization"],
        # rajoutés par xios : creation_date,   tracking_id
        vars_constraints=dict(
            variable_id=ParameterSettings(
                key="variable_id",
                default_values=[
                    ValueSettings(key_type="variable", keys="mipVarLabel")
                ]
            ),
            nominal_resolution=ParameterSettings(
                key="nominal_resolution",
                output_key="native_resolution"
            ),
            version_realization=ParameterSettings(
                key="version_realization",
                default_values=[
                    ValueSettings(key_type="common", keys="version_realization")
                ]
            ),
            conventions_version=ParameterSettings(
                key="conventions_version",
                default_values=[
                    ValueSettings(key_type="common", keys="conventions_version")
                ],
                output_key="Conventions"
            ),
            domain=ParameterSettings(
                key="domain",
                default_values=[
                    ValueSettings(key_type="common", keys="domain")
                ]
            ),
            domain_id=ParameterSettings(
                key="domain_id",
                default_values=[
                    ValueSettings(key_type="common", keys="domain_id")
                ]
            ),
            driving_source_id=ParameterSettings(
                key="driving_source_id",
                default_values=[
                    ValueSettings(key_type="common", keys="driving_source_id")
                ],
                fatal=True
            ),
            driving_variant_label=ParameterSettings(
                key="driving_variant_label",
                default_values=[
                    ValueSettings(key_type="common", keys="driving_variant_label")
                ],
                fatal=True
            ),
            driving_experiment_id=ParameterSettings(
                key="driving_experiment_id",
                default_values=[
                    ValueSettings(key_type="common", keys="driving_experiment_id")
                ],
                fatal=True
            ),
            driving_experiment=ParameterSettings(
                key="driving_experiment",
                default_values=[
                    ValueSettings(key_type="common", keys="driving_experiment")
                ],
                fatal=True
            ),
            driving_institution_id=ParameterSettings(
                key="driving_institution_id",
                default_values=[
                    ValueSettings(key_type="common", keys="driving_institution_id")
                ],
                fatal=True
            ),
            further_info_url=ParameterSettings(
                key="further_info_url",
                default_values=[
                    ValueSettings(key_type="laboratory", keys="info_url"),
                ]
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
                ]
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
                ]
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
                ]
            ),
            license=ParameterSettings(
                key="license",
                default_values=[
                    ValueSettings(key_type="laboratory", keys="license"),
                ]
            ),
            mip_era=ParameterSettings(
                key="mip_era",
                default_values=[
                    ValueSettings(key_type="simulation", keys="mip_era"),
                    ValueSettings(key_type="laboratory", keys="mip_era"),
                    "CMIP6"
                ]
            ),
            product=ParameterSettings(
                key="product",
                default_values=["model-output", ]
            ),
            project_id=ParameterSettings(
                key="project_id",
                default_values=["CORDEX-CMIP6", ]
            ),
            source_id=ParameterSettings(
                key="source_id",
                default_values=[
                    ValueSettings(key_type="simulation", keys="source_id"),
                ]
            ),
            source=ParameterSettings(
                key="source",
                default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"source_description",
					ValueSettings(key_type="internal", keys="source_id")
				]
			)
                ]
            ),
            source_type=ParameterSettings(
                key="source_type",
                default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"source_types",
					ValueSettings(key_type="internal", keys="source_id")
				]
			)
                ]
            ),
            title=ParameterSettings(
                key="title",
                default_values=[
                    ValueSettings(
                        key_type="combine",
                        keys=[
                            ValueSettings(key_type="internal", keys="source_id"),
                            "CORDEX-CMIP6",
                            ValueSettings(key_type="common", keys="expid_in_filename"),
                            ValueSettings(key_type="common", keys="driving_experiment")
                        ],
                        fmt="{} model output prepared for {} / {} simulation driven by {}"
                    ),
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
                default_values=["crs", ],
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
