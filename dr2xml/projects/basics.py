#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basics python tools
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import datetime
import re

import six

from dr2xml.projects.projects_interface_definitions import ValueSettings, ParameterSettings, TagSettings, ConditionSettings, \
	FunctionSettings, CaseSettings


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
		skip_values=[None, "None", "", "N/A"]
	),
	description=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="description"),
			ValueSettings(key_type="laboratory", keys="description")
		]
	),
	date_range=ParameterSettings(
		default_values=["%start_date%-%end_date%", ]
	),
	list_perso_dev_file=ParameterSettings(
		default_values=["dr2xml_list_perso_and_dev_file_names", ]
	),
	info_url=ParameterSettings(
		default_values=[
			ValueSettings(key_type="laboratory", keys="info_url")
		]
	),
	expid_in_filename=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="expid_in_filename"),
			ValueSettings(key_type="internal", keys="experiment_id")
		],
		forbidden_patterns=[".*_.*", ]
	),
	experiment=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="experiment")
		]
	),
	forcing_index=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="forcing_index"),
			"1"
		]
	),
	history=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="history"),
			"none"
		]
	),
	initialization_index=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="initialization_index"),
			"1"
		]
	),
	branch_method=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="branch_method"),
			"standard"
		]
	),
	parent_mip_era=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="parent_mip_era")
		]
	),
	parent_source_id=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="parent_source_id")
		]
	),
	parent_time_units=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="parent_time_units")
		]
	),
	parent_time_ref_year=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="parent_time_ref_year"),
			"1850"
		]
	),
	branch_month_in_parent=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="branch_month_in_parent"),
			"1"
		]
	),
	parent_variant_label=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="parent_variant_label")
		]
	),
	physics_index=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="physics_index"),
			"1"
		]
	),
	sub_experiment_id=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="sub_experiment_id"),
			"none"
		]
	),
	sub_experiment=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="sub_experiment"),
			"none"
		]
	),
	variant_info=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="variant_info")
		],
		skip_values=["", ]
	),
	comment_sim=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="comment"),
			""
		]
	),
	comment_lab=ParameterSettings(
		default_values=[
			ValueSettings(key_type="laboratory", keys="comment"),
			""
		]
	),
	institution_id=ParameterSettings(
		default_values=[
			ValueSettings(key_type="laboratory", keys="institution_id")
		]
	),
	references=ParameterSettings(
		default_values=[
			ValueSettings(key_type="laboratory", keys="references")
		]
	),
	compression_level=ParameterSettings(
		default_values=[
			ValueSettings(key_type="laboratory", keys="compression_level"),
			"0"
		]
	),
	output_level=ParameterSettings(
		default_values=[
			ValueSettings(key_type="laboratory", keys="output_level"),
			"10"
		]
	),
	source=ParameterSettings(
		default_values=[
			ValueSettings(key_type="laboratory", keys="source")
		]
	),
	institution=ParameterSettings(
		default_values=[
			ValueSettings(key_type="laboratory", keys="institution")
		]
	),
	contact=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="contact"),
			ValueSettings(key_type="laboratory", keys="contact"),
			"None"
		]
	),
	HDL=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="HDL"),
			ValueSettings(key_type="laboratory", keys="HDL")
		]
	),
	mip_era=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="mip_era"),
			ValueSettings(key_type="laboratory", keys="mip_era")
		]
	),
	activity_id=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="activity_id"),
			ValueSettings(key_type="laboratory", keys="activity_id")
		]
	),
	parent_activity_id=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="parent_activity_id"),
			ValueSettings(key_type="simulation", keys="activity_id"),
			ValueSettings(key_type="laboratory", keys="parent_activity_id"),
			ValueSettings(key_type="laboratory", keys="activity_id")
		]
	),
	parent_experiment_id=ParameterSettings(
		default_values=[
			ValueSettings(key_type="simulation", keys="parent_experiment_id"),
			ValueSettings(key_type="laboratory", keys="parent_experiment_id")
		]
	),
	convention_str=ParameterSettings(
		default_values=[
			ValueSettings(key_type="config", keys="conventions")
		]
	),
	dr2xml_version=ParameterSettings(
		default_values=[
			ValueSettings(key_type="config", keys="version")
		]
	),
	data_specs_version=ParameterSettings(
		default_values=[
			ValueSettings(key_type="DR_version")
		]
	)
)


project_settings = dict(
	context=TagSettings(
		attrs_list=["id", ],
		attrs_constraints=dict(
			id=ParameterSettings(
				default_values=[
					ValueSettings(key_type="internal", keys="context")
				]
			),
		),
		comments_list=["DR_version", "dr2xml_version", "lab_settings", "simulation_settings", "year"],
		comments_constraints=dict(
			DR_version=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="data_specs_version", fmt="CMIP6 Data Request version {}")
				]
			),
			dr2xml_version=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="dr2xml_version", fmt="dr2xml version {}")
				]
			),
			lab_settings=ParameterSettings(
				default_values=[
					ValueSettings(key_type="laboratory", fmt="Lab_and_model settings\n{}")
				]
			),
			simulation_settings=ParameterSettings(
				default_values=[
					ValueSettings(key_type="simulation", fmt="Simulation settings\n{}")
				]
			),
			year=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="year", fmt="Year processed {}")
				]
			)
		)
	),
	file_definition=TagSettings(
		attrs_list=["type", "enabled"],
		attrs_constraints=dict(
			type=ParameterSettings(
				default_values=["one_file", ]
			),
			enabled=ParameterSettings(
				default_values=["true", ]
			)
		)
	),
	file=TagSettings(
		attrs_list=["id", "name", "mode", "output_freq", "enabled"]
	),
	file_output=TagSettings(
		attrs_list=["id", "name", "output_freq", "append", "output_level", "compression_level", "split_freq",
		            "split_freq_format", "split_start_offset", "split_end_offset", "split_last_date", "time_units",
		            "time_counter_name", "time_counter", "time_stamp_name", "time_stamp_format", "uuid_name",
		            "uuid_format", "convention_str"],
		attrs_constraints=dict(
			split_freq=ParameterSettings(
				skip_values=["", "None", None],
				conditions=[
					ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
					                  check_to_do="nmatch", reference_values=".*fx.*")
				]
			),
			split_freq_format=ParameterSettings(
				skip_values=["", "None", None],
				conditions=[
					ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
					                  check_to_do="nmatch", reference_values=".*fx.*")
				]
			),
			split_start_offset=ParameterSettings(
				skip_values=["", "None", "False", None, False],
				conditions=[
					ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
					                  check_to_do="nmatch", reference_values=".*fx.*")
				]
			),
			split_end_offset=ParameterSettings(
				skip_values=["", "None", "False", None, False],
				conditions=[
					ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
					                  check_to_do="nmatch", reference_values=".*fx.*")
				]
			),
			split_last_date=ParameterSettings(
				skip_values=["", "None", None],
				conditions=[
					ConditionSettings(check_value=ValueSettings(key_type="variable", keys="frequency"),
					                  check_to_do="nmatch", reference_values=".*fx.*")
				]
			),
			append=ParameterSettings(
				default_values=["true", ]
			),
			time_units=ParameterSettings(
				default_values=["days", ]
			),
			time_counter_name=ParameterSettings(
				default_values=["time", ]
			),
			time_counter=ParameterSettings(
				default_values=["exclusive", ]
			),
			time_stamp_name=ParameterSettings(
				default_values=["creation_date", ]
			),
			time_stamp_format=ParameterSettings(
				default_values=["%Y-%m-%dT%H:%M:%SZ", ]
			),
			uuid_name=ParameterSettings(
				default_values=["tracking_id", ]
			),
			uuid_format=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="HDL", fmt="hdl:{}/%uuid%")
				],
				skip_values=["None", "", None]
			),
			convention_str=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="convention_str")
				]
			),
			output_level=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="output_level")
				],
				skip_values=["None", "", None]
			),
			compression_level=ParameterSettings(
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
			contact=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="contact")
				],
				skip_values=["None", "", None]
			),
			data_specs_version=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="data_specs_version")
				]
			),
			dr2xml_version=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="dr2xml_version")
				]
			),
			expid_in_filename=ParameterSettings(
				output_key="experiment_id",
				default_values=[
					ValueSettings(key_type="common", keys="expid_in_filename")
				]
			),
			description=ParameterSettings(
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
				skip_values=["", ],
				default_values=[
					ValueSettings(key_type="variable", keys="cell_measures",
					              func=FunctionSettings(func=build_external_variables))
				]
			),
			forcing_index=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="forcing_index")
				],
				num_type="int"
			),
			further_info_url=ParameterSettings(
				skip_values=["", "None", None]
			),
			history=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="history")
				]
			),
			initialization_index=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="initialization_index")
				],
				num_type="int"
			),
			institution=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="institution")
				],
				fatal=True
			),
			institution_id=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="institution_id")
				],
				fatal=True
			),
			mip_era=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="mip_era"),
					ValueSettings(key_type="variable", keys="mip_era")
				]
			),
			parent_experiment_id=ParameterSettings(
				conditions=[
					ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
					                  check_to_do="neq", reference_values=["no parent", "", "None"])
				],
				default_values=[
					ValueSettings(key_type="common", keys="parent_experiment_id")
				]
			),
			parent_mip_era=ParameterSettings(
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
				conditions=[
					ConditionSettings(check_value=ValueSettings(key_type="common", keys="parent_experiment_id"),
					                  check_to_do="neq", reference_values=["no parent", "", "None"])
				],
				default_values=[
					ValueSettings(key_type="common", keys="parent_activity_id")
				]
			),
			parent_source_id=ParameterSettings(
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
				default_values=[
					ValueSettings(key_type="common", keys="physics_index")
				],
				num_type="int"
			),
			product=ParameterSettings(
				default_values=["model-output", ]
			),
			realization_index=ParameterSettings(
				default_values=[
					ValueSettings(key_type="internal", keys="realization_index")
				],
				num_type="int"
			),
			references=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="references")
				]
			),
			sub_experiment_id=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="sub_experiment_id")
				]
			),
			sub_experiment=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="sub_experiment")
				]
			),
			variant_info=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="variant_info",
					              fmt=". Information provided by this attribute may in some cases be flawed. "
					                  "Users can find more comprehensive and up-to-date documentation via the "
					                  "further_info_url global attribute.")
				]
			),
			realm=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="modeling_realm")
				]
			),
			frequency=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="frequency")
				]
			),
			comment=ParameterSettings(
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
				default_values=[
					ValueSettings(key_type="common", keys="variant_label")
				]
			),
			activity_id=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="activity_id")
				]
			),
			source=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="source")
				]
			),
			source_id=ParameterSettings(
				default_values=[
					ValueSettings(key_type="internal", keys="source_id")
				]
			),
			source_type=ParameterSettings(
				default_values=[
					ValueSettings(key_type="internal", keys="source_type")
				]
			),
			title=ParameterSettings(
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
		attrs_list=["freq_op", "freq_offset"]
	),
	field=TagSettings(
		attrs_list=["id", "field_ref", "name", "freq_op", "freq_offset", "grid_ref", "long_name", "standard_name",
		            "unit", "operation", "detect_missing_value", "prec"]
	),
	field_output=TagSettings(
		attrs_list=["field_ref", "name", "grid_ref", "freq_offset", "detect_missing_value", "default_value", "prec",
		            "cell_methods", "cell_methods_mode", "operation", "freq_op", "expr"],
		attrs_constraints=dict(
			name=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="mipVarLabel")
				]
			),
			grid_ref=ParameterSettings(
				skip_values=["", "None", None]
			),
			freq_offset=ParameterSettings(
				skip_values=["", "None", None]
			),
			freq_op=ParameterSettings(
				skip_values=["", "None", None]
			),
			expr=ParameterSettings(
				skip_values=["", "None", None]
			),
			cell_methods_mode=ParameterSettings(
				default_values=["overwrite", ]
			),
			cell_methods=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="cell_methods")
				]
			),
			prec=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="prec")
				],
				authorized_values=["2", "4", "8"],
				corrections={
					"": "4",
					"float": "4",
					"real": "4",
					"double": "2",
					"integer": "2",
					"int": "2"
				},
				fatal=True
			),
			default_value=ParameterSettings(
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
				default_values=["True", ]
			)
		),
		vars_list=["comment", "standard_name", "description", "long_name", "positive", "history", "units",
		           "cell_methods", "cell_measures", "flag_meanings", "flag_values", "interval_operation"],
		vars_constraints=dict(
			standard_name=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="stdname")
				],
				skip_values=["", "None", None]
			),
			description=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="description"),
					"None"
				],
				skip_values=["", ]
			),
			long_name=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="long_name")
				]
			),
			history=ParameterSettings(
				default_values=[
					ValueSettings(key_type="common", keys="history")
				]
			),
			comment=ParameterSettings(
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
				default_values=[
					ValueSettings(key_type="variable", keys="positive")
				],
				skip_values=["", "None", None]
			),
			detect_missing_value=ParameterSettings(
				default_values=["none", ]
			),
			units=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="units")
				],
				skip_values=["", "None", None]
			),
			cell_methods=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="cell_methods")
				],
				skip_values=["", "None", None]
			),
			cell_measures=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys="cell_measures")
				],
				skip_values=["", "None", None]
			),
			flag_meanings=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys=["struct", "flag_meanings"])
				],
				skip_values=["", "None", None]
			),
			flag_values=ParameterSettings(
				default_values=[
					ValueSettings(key_type="variable", keys=["struct", "flag_values"])
				],
				skip_values=["", "None", None]
			),
			interval_operation=ParameterSettings(
				conditions=[
					ConditionSettings(check_value=ValueSettings(key_type="dict", keys="operation"),
					                  check_to_do="neq", reference_values="once")
				]
			)
		)
	),
	grid=TagSettings(
		attrs_list=["id", ]
	),
	axis=TagSettings(
		attrs_list=["id", "positive", "n_glo", "value", "axis_ref", "name", "standard_name", "long_name", "prec",
		            "unit", "value", "bounds", "dim_name", "label", "axis_type"],
		attrs_constraints=dict(
			axis_type=ParameterSettings(
				skip_values=["", "None", None]
			),
			standard_name=ParameterSettings(
				skip_values=["", "None", None],
				authorized_types=[str, ]
			),
			prec=ParameterSettings(
				skip_values=["", "None", None]
			),
			unit=ParameterSettings(
				skip_values=["", "None", None]
			),
			bounds=ParameterSettings(
				skip_values=["", "None", None]
			),
			dim_name=ParameterSettings(
				skip_values=["", "None", None]
			),
			label=ParameterSettings(
				skip_values=["", "None", None]
			),
			value=ParameterSettings(
				skip_values=["", "None", None]
			)
		)
	),
	zoom_axis=TagSettings(
		attrs_list=["index", ]
	),
	interpolate_axis=TagSettings(
		attrs_list=["type", "order", "coordinate"]
	),
	axis_group=TagSettings(
		attrs_list=["prec", ],
		attrs_constraints=dict(
			prec=ParameterSettings(
				default_values=["8", ]
			)
		)
	),
	domain=TagSettings(
		attrs_list=["id", "ni_glo", "nj_glo", "type", "prec", "lat_name", "lon_name", "dim_i_name","domain_ref"]
	),
	interpolate_domain=TagSettings(
		attrs_list=["type", "order", "renormalize", "mode", "write_weight", "coordinate"]
	),
	domain_group=TagSettings(
		attrs_list=["prec", ],
		attrs_constraints=dict(
			prec=ParameterSettings(
				default_values=["8", ]
			)
		)
	),
	scalar=TagSettings(
		attrs_list=["id", "scalar_ref", "name", "standard_name", "long_name", "label", "prec", "value", "bounds",
		            "bounds_name", "axis_type", "positive", "unit"],
		attrs_constraints=dict(
			standard_name=ParameterSettings(
				skip_values=["", "None", None]
			),
			axis_type=ParameterSettings(
				skip_values=["", "None", None]
			),
			unit=ParameterSettings(
				skip_values=["", "None", None]
			),
			label=ParameterSettings(
				skip_values=["", "None", None]
			),
			bounds=ParameterSettings(
				skip_values=["", "None", None]
			),
			bounds_name=ParameterSettings(
				skip_values=["", "None", None]
			),
			prec=ParameterSettings(
				skip_values=["", "None", None]
			),
			value=ParameterSettings(
				skip_values=["", "None", None]
			),
			positive=ParameterSettings(
				skip_values=["", "None", None]
			)
		)
	)
)
