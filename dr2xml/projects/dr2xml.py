#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dr2xml specific project settings
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.projects.projects_interface_definitions import ValueSettings, ParameterSettings, TagSettings


parent_project_settings = None

internal_values = dict(
	xios_version=ParameterSettings(
		key="xios_version",
		default_values=[
			ValueSettings(key_type="laboratory", keys="xios_version"),
			2
		]
	),
	synchronisation_frequency=ParameterSettings(
		key="synchronisation_frequency",
		default_value=[
			ValueSettings(key_type="simulation", keys="synchronisation_frequency"),
			ValueSettings(key_type="laboratory", keys="synchronisation_frequency"),
			None
		]
	),
	grouped_vars_per_file=ParameterSettings(
		key="grouped_vars_per_file",
		default_values=[
			ValueSettings(key_type="simulation", keys="grouped_vars_per_file"),
			ValueSettings(key_type="laboratory", keys="grouped_vars_per_file"),
			list()
		]
	),
	debug_parsing=ParameterSettings(
        key="debug_parsing",
		default_values=[
			ValueSettings(key_type="laboratory", keys="debug_parsing"),
			False
		]
	),
	project=ParameterSettings(
        key="project",
		default_values=[
			ValueSettings(key_type="laboratory", keys="project"),
			"CMIP6"
		]
	),
	project_settings=ParameterSettings(
        key="project_settings",
		default_values=[
			ValueSettings(key_type="laboratory", keys="project_settings"),
			ValueSettings(key_type="internal", keys="project")
		]
	),
    institution_id=ParameterSettings(
        key="institution_id",
        default_values=[
            ValueSettings(key_type="laboratory", keys="institution_id")
        ]
    ),
	context=ParameterSettings(
        key="context",
		default_values=[
			ValueSettings(key_type="dict", keys="context")
		],
		fatal=True
	),
	path_to_parse=ParameterSettings(
        key="path_to_parse",
		default_values=[
			ValueSettings(key_type="laboratory", keys="path_to_parse"),
			"./"
		]
	),
	use_union_zoom=ParameterSettings(
        key="use_union_zoom",
		default_values=[
			ValueSettings(key_type="laboratory", keys="use_union_zoom"),
			False
		]
	),
	print_stats_per_var_label=ParameterSettings(
        key="print_stats_per_var_label",
		default_values=[
			ValueSettings(key_type="laboratory", keys="print_stats_per_var_label"),
			False
		]
	),
	ping_variables_prefix=ParameterSettings(
        key="ping_variables_prefix",
		default_values=[
			ValueSettings(key_type="laboratory", keys="ping_variables_prefix")
		],
		fatal=True
	),
	split_frequencies=ParameterSettings(
        key="split_frequencies",
		default_values=[
			ValueSettings(key_type="simulation", keys="split_frequencies"),
			ValueSettings(key_type="laboratory", keys="split_frequencies"),
			"splitfreqs.dat"
		]
	),
	max_file_size_in_floats=ParameterSettings(
        key="max_file_size_in_floats",
		default_values=[
			ValueSettings(key_type="laboratory", keys="max_file_size_in_floats"),
			500 * 1.e6
		]
	),
	bytes_per_float=ParameterSettings(
        key="bytes_per_float",
		default_values=[
			ValueSettings(key_type="laboratory", keys="bytes_per_float"),
			2
		]
	),
	sampling_timestep=ParameterSettings(
        key="sampling_timestep",
		default_values=[
			ValueSettings(key_type="laboratory", keys="sampling_timestep")
		],
		fatal=True
	),
	tierMax_lset=ParameterSettings(
        key="tierMax_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="tierMax")
		],
		fatal=True
	),
	tierMax=ParameterSettings(
        key="tierMax",
		default_values=[
			ValueSettings(key_type="simulation", keys="tierMax"),
			ValueSettings(key_type="internal", keys="tierMax_lset")
		],
		fatal=True
	),
	max_priority_lset=ParameterSettings(
        key="max_priority_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="max_priority")
		],
		fatal=True
	),
	max_priority=ParameterSettings(
        key="max_priority",
		default_values=[
			ValueSettings(key_type="simulation", keys="max_priority"),
			ValueSettings(key_type="internal", keys="max_priority_lset")
		],
		fatal=True
	),
	grid_choice=ParameterSettings(
        key="grid_choice",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"grid_choice",
					ValueSettings(key_type="internal", keys="source_id")
				]
			)
		],
		fatal=True
	),
	configuration=ParameterSettings(
        key="configuration",
		default_values=[
			ValueSettings(key_type="simulation", keys="configuration")
		],
		fatal=True
	),
	source_id=ParameterSettings(
        key="source_id",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"configurations",
					ValueSettings(key_type="internal", keys="configuration"),
					0
				]
			),
			ValueSettings(key_type="simulation", keys="source_id")
		],
		fatal=True
	),
	sizes=ParameterSettings(
        key="sizes",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"sizes",
					ValueSettings(key_type="internal", keys="grid_choice")
				]
			)
		],
		fatal=True
	),
	mips=ParameterSettings(
        key="mips",
		default_values=[
			ValueSettings(key_type="laboratory", keys="mips")
		],
		fatal=True
	),
	excluded_request_links=ParameterSettings(
        key="excluded_request_links",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_request_links"),
			list()
		]
	),
	included_request_links=ParameterSettings(
        key="included_request_links",
		default_values=[
			ValueSettings(key_type="laboratory", keys="included_request_links"),
			list()
		]
	),
	excluded_tables_lset=ParameterSettings(
        key="excluded_tables_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_tables"),
			list()
		]
	),
	excluded_tables_sset=ParameterSettings(
        key="excluded_tables_sset",
		default_values=[
			ValueSettings(key_type="simulation", keys="excluded_tables"),
			list()
		]
	),
	excluded_spshapes_lset=ParameterSettings(
        key="excluded_spshapes_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_spshapes"),
			list()
		]
	),
	excluded_vars_lset=ParameterSettings(
        key="excluded_vars_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_vars"),
			list()
		]
	),
	excluded_vars_sset=ParameterSettings(
        key="excluded_vars_sset",
		default_values=[
			ValueSettings(key_type="simulation", keys="excluded_vars"),
			list()
		]
	),
	excluded_pairs_lset=ParameterSettings(
        key="excluded_pairs_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_pairs"),
			list()
		]
	),
	excluded_pairs_sset=ParameterSettings(
        key="excluded_pairs_sset",
		default_values=[
			ValueSettings(key_type="simulation", keys="excluded_pairs"),
			list()
		]
	),
	included_tables_lset=ParameterSettings(
        key="included_tables_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="included_tables"),
			list()
		]
	),
	included_tables=ParameterSettings(
        key="included_tables",
		default_values=[
			ValueSettings(key_type="simulation", keys="included_tables"),
			ValueSettings(key_type="internal", keys="included_tables_lset")
		]
	),
	included_vars_lset=ParameterSettings(
        key="included_vars_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="included_vars"),
			list()
		]
	),
	included_vars=ParameterSettings(
        key="included_vars",
		default_values=[
			ValueSettings(key_type="simulation", keys="included_vars"),
			ValueSettings(key_type="internal", keys="included_vars_lset")
		]
	),
	excluded_vars_per_config=ParameterSettings(
        key="excluded_vars_per_config",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"excluded_vars_per_config",
					ValueSettings(key_type="internal", keys="configuration")
				]
			),
			list()
		]
	),
	experiment_id=ParameterSettings(
        key="experiment_id",
		default_values=[
			ValueSettings(key_type="simulation", keys="experiment_id")
		],
		fatal=True
	),
	experiment_for_requests=ParameterSettings(
        key="experiment_for_requests",
		default_values=[
			ValueSettings(key_type="simulation", keys="experiment_for_requests"),
			ValueSettings(key_type="internal", keys="experiment_id")
		],
		fatal=True
	),
	branching=ParameterSettings(
        key="branching",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"branching",
					ValueSettings(key_type="internal", keys="source_id")
				],
			),
			dict()
		]
	),
	branch_year_in_child=ParameterSettings(
        key="branch_year_in_child",
		default_values=[
			ValueSettings(key_type="simulation", keys="branch_year_in_child")
		]
	),
	end_year=ParameterSettings(
        key="end_year",
		default_values=[
			ValueSettings(key_type="simulation", keys="end_year"),
			False
		]
	),
	allow_pseudo_standard_names=ParameterSettings(
        key="allow_pseudo_standard_names",
		default_values=[
			ValueSettings(key_type="laboratory", keys="allow_pseudo_standard_names"),
			False
		]
	),
	realization_index=ParameterSettings(
        key="realization_index",
		default_values=[
			ValueSettings(key_type="simulation", keys="realization_index"),
			"1"
		]
	),
	filter_on_realization=ParameterSettings(
        key="filter_on_realization",
		default_values=[
			ValueSettings(key_type="simulation", keys="filter_on_realization"),
			ValueSettings(key_type="laboratory", keys="filter_on_realization"),
			True
		]
	),
	listof_home_vars=ParameterSettings(
        key="listof_home_vars",
		default_values=[
			ValueSettings(key_type="simulation", keys="listof_home_vars"),
			ValueSettings(key_type="laboratory", keys="listof_home_vars"),
			None
		]
	),
	path_extra_tables=ParameterSettings(
        key="path_extra_tables",
		default_values=[
			ValueSettings(key_type="simulation", keys="path_extra_tables"),
			ValueSettings(key_type="laboratory", keys="path_extra_tables"),
			None
		]
	),
	allow_duplicates=ParameterSettings(
        key="allow_duplicates",
		default_values=[
			ValueSettings(key_type="laboratory", keys="allow_duplicates"),
			True
		]
	),
	orphan_variables=ParameterSettings(
        key="orphan_variables",
		default_values=[
			ValueSettings(key_type="laboratory", keys="orphan_variables")
		],
		fatal=True
	),
	too_long_periods=ParameterSettings(
        key="too_long_periods",
		default_values=[
			ValueSettings(key_type="laboratory", keys="too_long_periods"),
			list()
		],
		fatal=True
	),
	CFsubhr_frequency=ParameterSettings(
        key="CFsubhr_frequency",
		default_values=[
			ValueSettings(key_type="laboratory", keys="CFsubhr_frequency"),
			"1ts"
		]
	),
	simple_domain_grid_regexp=ParameterSettings(
        key="simple_domain_grid_regexp",
		default_values=[
			ValueSettings(key_type="laboratory", keys="simple_domain_grid_regexp")
		]
	),
	vertical_interpolation_operation=ParameterSettings(
        key="vertical_interpolation_operation",
		default_values=[
			ValueSettings(key_type="laboratory", keys="vertical_interpolation_operation"),
			"instant"
		]
	),
	vertical_interpolation_sample_freq=ParameterSettings(
        key="vertical_interpolation_sample_freq",
		default_values=[
			ValueSettings(key_type="laboratory", keys="vertical_interpolation_sample_freq")
		]
	),
	sectors=ParameterSettings(
        key="sectors",
		default_values=[
			ValueSettings(key_type="laboratory", keys="sectors")
		]
	),
	non_standard_axes=ParameterSettings(
        key="non_standard_axes",
		default_values=[
			ValueSettings(key_type="laboratory", keys="non_standard_axes"),
			dict()
		]
	),
	add_Gibraltar=ParameterSettings(
        key="add_Gibraltar",
		default_values=[
			ValueSettings(key_type="laboratory", keys="add_Gibraltar"),
			False
		]
	),
	grid_policy=ParameterSettings(
        key="grid_policy",
		default_values=[
			ValueSettings(key_type="laboratory", keys="grid_policy"),
			False
		],
		fatal=True
	),
	allow_tos_3hr_1deg=ParameterSettings(
        key="allow_tos_3hr_1deg",
		default_values=[
			ValueSettings(key_type="laboratory", keys="allow_tos_3hr_1deg"),
			True
		]
	),
	adhoc_policy_do_add_1deg_grid_for_tos=ParameterSettings(
        key="adhoc_policy_do_add_1deg_grid_for_tos",
		default_values=[
			ValueSettings(key_type="laboratory", keys="adhoc_policy_do_add_1deg_grid_for_tos"),
			False
		]
	),
	fx_from_file=ParameterSettings(
        key="fx_from_file",
		default_values=[
			ValueSettings(key_type="laboratory", keys="fx_from_file"),
			list()
		]
	),
	orography_field_name=ParameterSettings(
        key="orography_field_name",
		default_values=[
			ValueSettings(key_type="laboratory", keys="orography_field_name"),
			"CMIP6_orog"
		]
	),
	zg_field_name=ParameterSettings(
        key="zg_field_name",
		default_values=[
			ValueSettings(key_type="laboratory", keys="zg_field_name"),
			"zg"
		]
	),
	print_variables=ParameterSettings(
        key="print_variables",
		default_values=[
			ValueSettings(key_type="laboratory", keys="print_variables"),
			True
		]
	),
	grids_dev=ParameterSettings(
        key="grids_dev",
		default_values=[
			ValueSettings(key_type="laboratory", keys="grids_dev"),
			dict()
		],
		fatal=True
	),
	grids=ParameterSettings(
        key="grids",
		default_values=[
			ValueSettings(key_type="laboratory", keys="grids")
		],
		fatal=True
	),
	required_model_components=ParameterSettings(
        key="required_model_components",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"required_model_components",
					ValueSettings(key_type="internal", keys="source_id")
				]
			),
			list()
		],
		fatal=True
	),
	additional_allowed_model_components=ParameterSettings(
        key="additional_allowed_model_components",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"additional_allowed_model_components",
					ValueSettings(key_type="internal", keys="source_id")
				]
			),
			list()
		],
		fatal=True
	),
	max_split_freq=ParameterSettings(
        key="max_split_freq",
		default_values=[
			ValueSettings(key_type="simulation", keys="max_split_freq"),
			ValueSettings(key_type="laboratory", keys="max_split_freq"),
			None
		],
		fatal=True
	),
	dr2xml_manages_enddate=ParameterSettings(
        key="dr2xml_manages_enddate",
		default_values=[
			ValueSettings(key_type="laboratory", keys="dr2xml_manages_enddate"),
			True
		],
		fatal=True
	),
	non_standard_attributes=ParameterSettings(
        key="non_standard_attributes",
		default_values=[
			ValueSettings(key_type="laboratory", keys="non_standard_attributes"),
			dict()
		]
	),
	allow_duplicates_in_same_table=ParameterSettings(
        key="allow_duplicates_in_same_table",
		default_values=[
			ValueSettings(key_type="laboratory", keys="allow_duplicates_in_same_table"),
			False
		],
		fatal=True
	),
	use_cmorvar_label_in_filename=ParameterSettings(
        key="use_cmorvar_label_in_filename",
		default_values=[
			ValueSettings(key_type="laboratory", keys="use_cmorvar_label_in_filename"),
			False
		],
		fatal=True
	),
	nemo_sources_management_policy_master_of_the_world=ParameterSettings(
        key="nemo_sources_management_policy_master_of_the_world",
		default_values=[
			ValueSettings(key_type="laboratory", keys="nemo_sources_management_policy_master_of_the_world"),
			False
		],
		fatal=True
	),
	special_timestep_vars=ParameterSettings(
        key="special_timestep_vars",
		default_values=[
			ValueSettings(key_type="laboratory", keys="special_timestep_vars"),
			list()
		]
	),
	useAtForInstant=ParameterSettings(
        key="useAtForInstant",
		default_values=[
			ValueSettings(key_type="laboratory", keys="useAtForInstant"),
			False
		]
	),
	bypass_CV_components=ParameterSettings(
        key="bypass_CV_components",
		default_values=[
			ValueSettings(key_type="laboratory", keys="bypass_CV_components"),
			False
		]
	),
	data_request_used=ParameterSettings(
        key="data_request_used",
		default_values=[
			ValueSettings(key_type="laboratory", keys="data_request_used"),
			"CMIP6"
		]
	),
	laboratory_used=ParameterSettings(
        key="laboratory_used",
		default_values=[
			ValueSettings(key_type="laboratory", keys="laboratory_used"),
			None
		]
	),
	save_project_settings=ParameterSettings(
        key="save_project_settings",
		default_values=[
			ValueSettings(key_type="laboratory", keys="save_project_settings"),
			None
		]
	),
	perso_sdims_description=ParameterSettings(
        key="perso_sdims_description",
		default_values=[
			ValueSettings(key_type="simulation", keys="perso_sdims_description"),
			dict()
		]
	),
	realms_per_context=ParameterSettings(
        key="realms_per_context",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"realms_per_context",
					ValueSettings(key_type="internal", keys="context")
				]
			)
		],
		fatal=True
	),
	source_type=ParameterSettings(
        key="source_type",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"configurations",
					ValueSettings(key_type="internal", keys="configuration"),
					1
				]
			),
			ValueSettings(key_type="simulation", keys="source_type"),
			ValueSettings(
				key_type="laboratory",
				keys=[
					"source_types",
					ValueSettings(key_type="internal", keys="source_id")
				]
			)
		],
		fatal=True
	)
)

common_values = dict(
	prefix=ParameterSettings(
        key="prefix",
		default_values=[
			ValueSettings(key_type="dict", keys="prefix")
		],
		fatal=True
	),
	year=ParameterSettings(
        key="year",
		default_values=[
			ValueSettings(key_type="dict", keys="year")
		],
		fatal=True
	),
	root=ParameterSettings(
        key="root",
		default_values=[
			ValueSettings(key_type="dict", keys="root")
		],
		fatal=True
	)
)

project_settings = dict(
	context=TagSettings(),
	file_definition=TagSettings(),
	file=TagSettings(),
	file_output=TagSettings(),
	field_definition=TagSettings(),
	field_group=TagSettings(),
	field=TagSettings(),
	field_output=TagSettings(),
	grid=TagSettings(),
	grid_definition=TagSettings(),
	axis=TagSettings(),
	zoom_axis=TagSettings(),
	interpolate_axis=TagSettings(),
	axis_definition=TagSettings(),
	axis_group=TagSettings(),
	temporal_splitting=TagSettings(),
	domain=TagSettings(),
	generate_rectilinear_domain=TagSettings(),
	interpolate_domain=TagSettings(),
	domain_definition=TagSettings(),
	domain_group=TagSettings(),
	scalar=TagSettings(),
	duplicate_scalar=TagSettings(),
	scalar_definition=TagSettings(),
	variable=TagSettings(attrs_list=["name", "type"])
)
