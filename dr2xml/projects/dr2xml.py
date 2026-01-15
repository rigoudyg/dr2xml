#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dr2xml specific project settings
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import os.path

from dr2xml.projects.projects_interface_definitions import ValueSettings, ParameterSettings, TagSettings, \
	FunctionSettings, CaseSettings, ConditionSettings
from utilities.logger import get_logger

parent_project_settings = None


def format_sizes(*sizes):
	"""
	Transform into a dict the sizes values provided as ['nho', 'nlo', 'nha', 'nla', 'nlas', 'nls', 'nh1'], with:
	- nho: oce grid size
	- nlo : oce nb levels
	- nha: atm grid size
	- nla: atm nb levels
	- nlas:
	- nls : soil nb of levels
	- nh1 : number of latitude (atmosphere/ocean grids)
	Also provide others infor such as:
	- nb cosp sites (default 129)
	- nb lidar temp (default 40)
	- nb_parasol_refl (default 5)
	- nb isccp tau (default 7)
	- nb isccp pc (default 5)
	- nb curtains sites (default 1000)
	:param dict or list sizes: dict containing the sizes as a list or dict
	:return dict: dictionary containing sizes as a dict
	"""
	logger = get_logger()
	rep = dict(nho=None, nlo=None, nha=None, nla=None, nlas=None, nls=None, nh1=None,
	           nb_cosp_sites=129, nb_lidar_temp=40, nb_parasol_refl=5, nb_isccp_tau=7, nb_isccp_pc=7,
	           nb_curtain_sites=1000)
	if isinstance(sizes, (list, tuple)) and len(sizes) == 1 and isinstance(sizes[0], (dict, list, tuple)):
		sizes = sizes[0]
	if isinstance(sizes, (list, tuple)):
		mcfg = dict()
		for (key, val) in zip(['nho', 'nlo', 'nha', 'nla', 'nlas', 'nls', 'nh1'], sizes):
			mcfg[key] = val
		rep.update(mcfg)
	elif isinstance(sizes, dict):
		rep.update(sizes)
	else:
		logger.error("Unable to transform sizes to get relevant information.")
		raise ValueError("Unable to transform sizes to get relevant information.")
	issues_values = [elt for elt in rep if rep[elt] is None]
	if len(issues_values) > 0:
		logger.error(f"The values provided by sizes must not be None, issues with {issues_values}.")
		raise ValueError(f"The values provided by sizes must not be None, issues with {issues_values}.")
	return rep


def sort_mips(*mips):
	if isinstance(mips, (list, tuple)) and len(mips) == 1 and isinstance(mips[0], (dict, set, list)):
		mips = mips[0]
	elif len(mips) == 0:
		mips = list()
	rep = set()
	if isinstance(mips, dict):
		for grid in mips:
			rep = rep | mips[grid]
	else:
		rep = mips
	return sorted(list(rep))


internal_values = dict(
	xios_version=ParameterSettings(
		key="xios_version",
		default_values=[
			ValueSettings(key_type="laboratory", keys="xios_version"),
			2
		],
		help="Version of XIOS used."
	),
	synchronisation_frequency=ParameterSettings(
		key="synchronisation_frequency",
		help="Frequency at which the synchornisation between buffer and filesystem is done.",
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
		],
		help="Variables to be grouped in the same output file (provided additional conditions are filled)."
	),
	debug_parsing=ParameterSettings(
        key="debug_parsing",
		default_values=[
			ValueSettings(key_type="laboratory", keys="debug_parsing"),
			False
		],
		help="In order to identify which xml files generates a problem, you can use this flag."
	),
	project=ParameterSettings(
        key="project",
		default_values=[
			ValueSettings(key_type="laboratory", keys="project"),
			"CMIP6"
		],
		help="Project associated with the simulation."
	),
	project_settings=ParameterSettings(
        key="project_settings",
		default_values=[
			ValueSettings(key_type="laboratory", keys="project_settings"),
			ValueSettings(key_type="internal", keys="project")
		],
		help="Project settings definition file to be used."
	),
    institution_id=ParameterSettings(
        key="institution_id",
        default_values=[
            ValueSettings(key_type="laboratory", keys="institution_id")
        ],
	    fatal=True,
	    help="Institution identifier."
    ),
	context=ParameterSettings(
        key="context",
		default_values=[
			ValueSettings(key_type="dict", keys="context")
		],
		fatal=True,
		help="Context associated with the xml file produced."
	),
	select=ParameterSettings(
        key="select",
		default_values=[
			ValueSettings(key_type="dict", keys="select")
		],
		authorized_values=["on_expt_and_year", "on_expt", "no"],
		fatal=True,
		help="Selection strategy for variables."
	),
	select_on_expt=ParameterSettings(
		key="select_on_expt",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select"),
				                             check_to_do="eq",
				                             reference_values=["on_expt_and_year", "on_expt"]),
				value=True
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select"),
				                             check_to_do="eq",
				                             reference_values=["no", ]),
				value=False
			)
		],
		fatal=True,
		help="Should data be selected on experiment?"
	),
	select_on_year=ParameterSettings(
		key="select_on_year",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select"),
				                             check_to_do="eq",
				                             reference_values=["on_expt_and_year", ]),
				value=ValueSettings(key_type="internal", keys="year")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select"),
				                             check_to_do="eq",
				                             reference_values=["no", "on_expt"]),
				value=None
			)
		],
		fatal=True,
		help="Should data be selected on year?"
	),
	select_grid_choice=ParameterSettings(
		key="select_grid_choice",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="grid_choice")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value="LR"
			)
		],
		fatal=True,
		help="Grid choice for variable selection."
	),
	select_sizes=ParameterSettings(
		key="select_sizes",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="sizes")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=None
			)
		],
		fatal=True,
		help="Sizes for variable selection."
	),
	select_max_priority=ParameterSettings(
		key="select_max_priority",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="max_priority")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="max_priority_lset")
			)
		],
		fatal=True,
		help="Max priority for variable selection."
	),
	select_tierMax=ParameterSettings(
		key="select_tierMax",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="tierMax")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="tierMax_lset")
			)
		],
		fatal=True,
		help="tierMax for variable selection."
	),
	select_included_vars=ParameterSettings(
		key="select_included_vars",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="included_vars")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="included_vars_lset")
			)
		],
		fatal=True,
		help="Included variables for variable selection."
	),
	select_included_tables=ParameterSettings(
		key="select_included_tables",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="included_tables")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="included_tables_lset")
			)
		],
		fatal=True,
		help="Included tables for variable selection."
	),
	select_included_opportunities=ParameterSettings(
		key="select_included_opportunities",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="included_opportunities")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="included_opportunities_lset")
			)
		],
		fatal=True,
		help="Included opportunities for variable selection."
	),
	select_included_vargroups=ParameterSettings(
		key="select_included_vargroups",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="included_vargroups")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="included_vargroups_lset")
			)
		],
		fatal=True,
		help="Included variables groups for variable selection."
	),
	select_included_request_links=ParameterSettings(
		key="select_included_request_links",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="included_request_links")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=None
			)
		],
		fatal=True,
		help="Included request links for variable selection."
	),
	select_excluded_request_links=ParameterSettings(
		key="select_excluded_request_links",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal", keys="excluded_request_links")
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=None
			)
		],
		fatal=True,
		help="Excluded request links for variable selection."
	),
	select_excluded_vars=ParameterSettings(
		key="select_excluded_vars",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="merge",
				                    keys=[
					                    ValueSettings(key_type="internal", keys="excluded_vars_lset"),
					                    ValueSettings(key_type="internal", keys="excluded_vars_sset"),
					                    ValueSettings(key_type="internal", keys="excluded_vars_per_config")
				                    ])
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="excluded_vars_lset")
			)
		],
		fatal=True,
		help="Excluded variables for variable selection."
	),
	select_excluded_tables=ParameterSettings(
		key="select_excluded_tables",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="merge",
				                    keys=[
					                    ValueSettings(key_type="internal", keys="excluded_tables_lset"),
					                    ValueSettings(key_type="internal", keys="excluded_tables_sset")
				                    ])
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="excluded_tables_lset")
			)
		],
		fatal=True,
		help="Excluded tables for variable selection."
	),
	select_excluded_opportunities=ParameterSettings(
		key="select_excluded_opportunities",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="merge",
				                    keys=[
					                    ValueSettings(key_type="internal", keys="excluded_opportunities_lset"),
					                    ValueSettings(key_type="internal", keys="excluded_opportunities_sset")
				                    ])
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="excluded_opportunities_lset")
			)
		],
		fatal=True,
		help="Excluded opportunities for variable selection."
	),
	select_excluded_vargroups=ParameterSettings(
		key="select_excluded_vargroups",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="merge",
				                    keys=[
					                    ValueSettings(key_type="internal", keys="excluded_vargroups_lset"),
					                    ValueSettings(key_type="internal", keys="excluded_vargroups_sset")
				                    ])
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="excluded_vargroups_lset")
			)
		],
		fatal=True,
		help="Excluded variables groups for variable selection."
	),
	select_excluded_pairs=ParameterSettings(
		key="select_excluded_pairs",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="merge",
				                    keys=[
					                    ValueSettings(key_type="internal", keys="excluded_pairs_lset"),
					                    ValueSettings(key_type="internal", keys="excluded_pairs_sset")
				                    ])
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="excluded_pairs_lset")
			)
		],
		fatal=True,
		help="Excluded pairs for variable selection."
	),
	select_mips=ParameterSettings(
        key="select_mips",
		cases=[
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=True),
				value=ValueSettings(key_type="internal",
				                    keys=[
					                    "mips",
					                    ValueSettings(key_type="internal", keys="select_grid_choice")
				                    ],
				                    func=sort_mips)
			),
			CaseSettings(
				conditions=ConditionSettings(check_value=ValueSettings(key_type="internal", keys="select_on_expt"),
				                             check_to_do="eq",
				                             reference_values=False),
				value=ValueSettings(key_type="internal", keys="mips", func=sort_mips)
			)
		],
		fatal=True,
		help="MIPs for variable selection."
	),
	path_to_parse=ParameterSettings(
        key="path_to_parse",
		default_values=[
			ValueSettings(key_type="laboratory", keys="path_to_parse"),
			"./"
		],
		help="The path of the directory which, at run time, contains the root XML file (iodef.xml)."
	),
	use_union_zoom=ParameterSettings(
        key="use_union_zoom",
		default_values=[
			ValueSettings(key_type="laboratory", keys="use_union_zoom"),
			False
		],
		help="Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR."
	),
	print_stats_per_var_label=ParameterSettings(
        key="print_stats_per_var_label",
		default_values=[
			ValueSettings(key_type="laboratory", keys="print_stats_per_var_label"),
			False
		],
		help="For an extended printout of selected CMOR variables, grouped by variable label."
	),
	ping_variables_prefix=ParameterSettings(
        key="ping_variables_prefix",
		default_values=[
			ValueSettings(key_type="laboratory", keys="ping_variables_prefix")
		],
		fatal=True,
		help="The tag used to prefix the variables in the ‘field id’ namespaces of the ping file; may be an empty string."
	),
	grid_prefix=ParameterSettings(
        key="grid_prefix",
		default_values=[
			ValueSettings(key_type="laboratory", keys="grid_prefix"),
			ValueSettings(key_type="internal", keys="ping_variables_prefix")
		],
		fatal=True,
		help="Prefix of the dr2xml generated grid named to be used."
	),
	split_frequencies=ParameterSettings(
        key="split_frequencies",
		default_values=[
			ValueSettings(key_type="simulation", keys="split_frequencies"),
			ValueSettings(key_type="laboratory", keys="split_frequencies"),
			"splitfreqs.dat"
		],
		help="Path to the split frequencies file to be used."
	),
	max_file_size_in_floats=ParameterSettings(
        key="max_file_size_in_floats",
		default_values=[
			ValueSettings(key_type="laboratory", keys="max_file_size_in_floats"),
			500 * 1.e6
		],
		help="The maximum size of generated files in number of floating values."
	),
	bytes_per_float=ParameterSettings(
        key="bytes_per_float",
		default_values=[
			ValueSettings(key_type="laboratory", keys="bytes_per_float"),
			2
		],
		help="Estimate of number of bytes per floating value, given the chosen :term:`compression_level`."
	),
	sampling_timestep=ParameterSettings(
        key="sampling_timestep",
		default_values=[
			ValueSettings(key_type="laboratory", keys="sampling_timestep")
		],
		fatal=True,
		help="Basic sampling timestep set in your field definition (used to feed metadata 'interval_operation'). "
		     "Should be a dictionary which keys are resolutions and values a context/timestep dictionary."
	),
	tierMax_lset=ParameterSettings(
        key="tierMax_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="tierMax")
		],
		fatal=True,
		help="Number indicating the maximum tier to consider for experiments from lab settings."
	),
	tierMax=ParameterSettings(
        key="tierMax",
		default_values=[
			ValueSettings(key_type="simulation", keys="tierMax"),
			ValueSettings(key_type="internal", keys="tierMax_lset")
		],
		fatal=True,
		help="Number indicating the maximum tier to consider for experiments."
	),
	max_priority_lset=ParameterSettings(
        key="max_priority_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="max_priority")
		],
		fatal=True,
		help="Max variable priority level to be output (you may set 3 when creating ping_files while being more "
		     "restrictive at run time) from lab settings."
	),
	max_priority=ParameterSettings(
        key="max_priority",
		default_values=[
			ValueSettings(key_type="simulation", keys="max_priority"),
			ValueSettings(key_type="internal", keys="max_priority_lset")
		],
		fatal=True,
		help="Max variable priority level to be output (you may set 3 when creating ping_files while being more "
		     "restrictive at run time)."
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
		fatal=True,
		help="A dictionary which keys are models name and values the corresponding resolution."
	),
	configuration=ParameterSettings(
        key="configuration",
		default_values=[
			ValueSettings(key_type="simulation", keys="configuration")
		],
		fatal=True,
		help="Configuration used for this experiment. "
		     "If there is no configuration in lab_settings which matches you case, please rather use next or next two "
		     "entries: :term:`source_id` and, if needed, :term:`source_type`."
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
		fatal=True,
		help="Name of the model used."
	),
	sizes=ParameterSettings(
        key="sizes",
		default_values=[
			ValueSettings(
				key_type="laboratory",
				keys=[
					"sizes",
					ValueSettings(key_type="internal", keys="grid_choice")
				],
				func=FunctionSettings(func=format_sizes)
			)
		],
		fatal=True,
		help="A dictionary which keys are resolution and values the associated grid size for atmosphere and ocean "
		     "grids. The grid size looks like : ['nho', 'nlo', 'nha', 'nla', 'nlas', 'nls', 'nh1']. Used to compute "
		     "file split frequency."
	),
	mips=ParameterSettings(
        key="mips",
		default_values=[
			ValueSettings(key_type="laboratory", keys="mips")
		],
		fatal=True,
		help="A dictionary in which keys are grid and values a set of strings corresponding to MIPs names."
	),
	excluded_request_links=ParameterSettings(
        key="excluded_request_links",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_request_links"),
			list()
		],
		target_type="list",
		help="List of links un data request that should not been followed (those request are not taken into account)."
	),
	included_request_links=ParameterSettings(
        key="included_request_links",
		default_values=[
			ValueSettings(key_type="laboratory", keys="included_request_links"),
			list()
		],
		target_type="list",
		help="List of the request links that will be processed (all others will not)."
	),
	excluded_tables_lset=ParameterSettings(
        key="excluded_tables_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_tables"),
			list()
		],
		target_type="list",
		help="List of the tables that will be excluded from outputs from laboratory settings."
	),
	excluded_tables_sset=ParameterSettings(
        key="excluded_tables_sset",
		default_values=[
			ValueSettings(key_type="simulation", keys="excluded_tables"),
			list()
		],
		target_type="list",
		help="List of the tables that will be excluded from outputs from simulation settings."
	),
	excluded_spshapes_lset=ParameterSettings(
        key="excluded_spshapes_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_spshapes"),
			list()
		],
		target_type="list",
		help="The list of shapes that should be excluded (all variables in those shapes will be excluded from outputs)."
	),
	excluded_vars_lset=ParameterSettings(
        key="excluded_vars_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_vars"),
			list()
		],
		target_type="list",
		help="List of CMOR variables to exclude from the result based on previous Data Request extraction from "
		     "laboratory settings."
	),
	excluded_vars_sset=ParameterSettings(
        key="excluded_vars_sset",
		default_values=[
			ValueSettings(key_type="simulation", keys="excluded_vars"),
			list()
		],
		target_type="list",
		help="List of CMOR variables to exclude from the result based on previous Data Request extraction from "
		     "simulation settings."
	),
	excluded_pairs_lset=ParameterSettings(
        key="excluded_pairs_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_pairs"),
			list()
		],
		target_type="list",
		help="You can exclude some (variable, table) pairs from outputs. "
		     "A list of tuple (variable, table) to be excluded from laboratory settings."
	),
	excluded_pairs_sset=ParameterSettings(
        key="excluded_pairs_sset",
		default_values=[
			ValueSettings(key_type="simulation", keys="excluded_pairs"),
			list()
		],
		target_type="list",
		help="You can exclude some (variable, table) pairs from outputs. "
		     "A list of tuple (variable, table) to be excluded from simulation settings."
	),
	included_tables_lset=ParameterSettings(
        key="included_tables_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="included_tables"),
			list()
		],
		target_type="list",
		help="List of tables that will be processed (all others will not) from laboratory settings."
	),
	included_tables=ParameterSettings(
        key="included_tables",
		default_values=[
			ValueSettings(key_type="simulation", keys="included_tables"),
			ValueSettings(key_type="internal", keys="included_tables_lset")
		],
		target_type="list",
		help="List of tables that will be processed (all others will not)."
	),
	included_vars_lset=ParameterSettings(
        key="included_vars_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="included_vars"),
			list()
		],
		target_type="list",
		help="Variables to be considered from the Data Request (all others will not) from laboratory settings."
	),
	included_vars=ParameterSettings(
        key="included_vars",
		default_values=[
			ValueSettings(key_type="simulation", keys="included_vars"),
			ValueSettings(key_type="internal", keys="included_vars_lset")
		],
		target_type="list",
		help="Variables to be considered from the Data Request (all others will not)"
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
		],
		help="A dictionary which keys are configurations and values the list of variables that must be excluded for "
		     "each configuration."
	),
	included_opportunities_lset=ParameterSettings(
        key="included_opportunities_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="included_opportunities"),
			list()
		],
		target_type="list",
		help="List of opportunities that will be processed (all others will not) from laboratory settings."
	),
	included_opportunities=ParameterSettings(
        key="included_opportunities",
		default_values=[
			ValueSettings(key_type="simulation", keys="included_opportunities"),
			ValueSettings(key_type="internal", keys="included_opportunities_lset")
		],
		target_type="list",
		help="List of opportunities that will be processed (all others will not)."
	),
	included_vargroups_lset=ParameterSettings(
        key="included_vargroups_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="included_vargroups"),
			list()
		],
		target_type="list",
		help="List of variables groups that will be processed (all others will not) from laboratory settings."
	),
	included_vargroups=ParameterSettings(
        key="included_vargroups",
		default_values=[
			ValueSettings(key_type="simulation", keys="included_vargroups"),
			ValueSettings(key_type="internal", keys="included_vargroups_lset")
		],
		target_type="list",
		help="List of variables groups that will be processed (all others will not)."
	),
	excluded_opportunities_lset=ParameterSettings(
        key="excluded_opportunities_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_opportunities"),
			list()
		],
		target_type="list",
		help="List of the opportunities that will be excluded from outputs from laboratory settings."
	),
	excluded_opportunities_sset=ParameterSettings(
        key="excluded_opportunities_sset",
		default_values=[
			ValueSettings(key_type="simulation", keys="excluded_opportunities"),
			list()
		],
		target_type="list",
		help="List of the opportunities that will be excluded from outputs from simulation settings."
	),
	excluded_vargroups_lset=ParameterSettings(
        key="excluded_vargroups_lset",
		default_values=[
			ValueSettings(key_type="laboratory", keys="excluded_vargroups"),
			list()
		],
		target_type="list",
		help="List of the variables groups that will be excluded from outputs from laboratory settings."
	),
	excluded_vargroups_sset=ParameterSettings(
        key="excluded_vargroups_sset",
		default_values=[
			ValueSettings(key_type="simulation", keys="excluded_vargroups"),
			list()
		],
		target_type="list",
		help="List of the variables groups that will be excluded from outputs from simulation settings."
	),
	experiment_id=ParameterSettings(
        key="experiment_id",
		default_values=[
			ValueSettings(key_type="simulation", keys="experiment_id")
		],
		fatal=True,
		help="Root experiment identifier."
	),
	experiment_for_requests=ParameterSettings(
        key="experiment_for_requests",
		default_values=[
			ValueSettings(key_type="simulation", keys="experiment_for_requests"),
			ValueSettings(key_type="internal", keys="experiment_id")
		],
		fatal=True,
		help="Experiment id to use for driving the use of the Data Request."
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
		],
		help=" Describe the branching scheme for experiments involved in some 'branchedYears type' tslice "
		     "(for details, see: http://clipc-services.ceda.ac.uk/dreq/index/Slice.html ). "
		     "Just put the as key the common start year in child and as value the list of start years in parent "
		     "for all members."
		     "A dictionary with models name as key and dictionary containing experiment,"
		     "(branch year in child, list of branch year in parent) key values."
	),
	branch_year_in_child=ParameterSettings(
        key="branch_year_in_child",
		default_values=[
			ValueSettings(key_type="simulation", keys="branch_year_in_child")
		],
		help="In some instances, the experiment start year is not explicit or is doubtful in DR. See "
		     "file doc/some_experiments_starty_in_DR01.00.21. You should then specify it, using next setting "
		     "in order that requestItems analysis work in all cases. "
		     "In some other cases, DR requestItems which apply to the experiment form its start does not "
		     "cover its whole duration and have a wrong duration (computed based on a wrong start year); "
		     "They necessitate to fix the start year."
	),
	end_year=ParameterSettings(
        key="end_year",
		default_values=[
			ValueSettings(key_type="simulation", keys="end_year"),
			False
		],
		help="If you want to carry on the experiment beyond the duration set in DR, and that all "
		     "requestItems that apply to DR end year also apply later on, set 'end_year' "
		     "You can also set it if you don't know if DR has a wrong value"
	),
	allow_pseudo_standard_names=ParameterSettings(
        key="allow_pseudo_standard_names",
		default_values=[
			ValueSettings(key_type="laboratory", keys="allow_pseudo_standard_names"),
			False
		],
		help="DR has sn attributes for MIP variables. They can be real,CF-compliant, standard_names or "
		     "pseudo_standard_names, i.e. not yet approved labels. Default is to use only CF ones."
	),
	realization_index=ParameterSettings(
        key="realization_index",
		default_values=[
			ValueSettings(key_type="simulation", keys="realization_index"),
			"1"
		],
		help="Realization number."
	),
	filter_on_realization=ParameterSettings(
        key="filter_on_realization",
		default_values=[
			ValueSettings(key_type="simulation", keys="filter_on_realization"),
			ValueSettings(key_type="laboratory", keys="filter_on_realization"),
			True
		],
		help="If you want to produce the same variables set for all members, set this parameter to False."
	),
	listof_home_vars=ParameterSettings(
        key="listof_home_vars",
		default_values=[
			ValueSettings(key_type="simulation", keys="listof_home_vars"),
			ValueSettings(key_type="laboratory", keys="listof_home_vars"),
			None
		],
		help="Full path to the file which contains the list of home variables to be taken into account, "
		     "in addition to the Data Request."
	),
	path_extra_tables=ParameterSettings(
        key="path_extra_tables",
		default_values=[
			ValueSettings(key_type="simulation", keys="path_extra_tables"),
			ValueSettings(key_type="laboratory", keys="path_extra_tables"),
			None
		],
		help="Full path of the directory which contains extra tables."
	),
	allow_duplicates=ParameterSettings(
        key="allow_duplicates",
		default_values=[
			ValueSettings(key_type="laboratory", keys="allow_duplicates"),
			True
		],
		help="Should we allow for duplicate vars: two vars with same frequency, shape and realm, which differ only by "
		     "the table. In DR01.00.21, this actually applies to very few fields "
		     "(ps-Aermon, tas-ImonAnt, areacellg-IfxAnt)."
	),
	orphan_variables=ParameterSettings(
        key="orphan_variables",
		default_values=[
			ValueSettings(key_type="laboratory", keys="orphan_variables")
		],
		fatal=True,
		help="A dictionary with (context name, list of variables) as (key,value) pairs, "
		     "where the list indicates the variables to be re-affected to the key-context "
		     "(initially affected to a realm falling in another context)"
	),
	too_long_periods=ParameterSettings(
        key="too_long_periods",
		default_values=[
			ValueSettings(key_type="laboratory", keys="too_long_periods"),
			list()
		],
		fatal=True,
		help="The CMIP6 frequencies that are unreachable for a single model run. Datafiles will "
		     "be labelled with dates consistent with content (but not with CMIP6 requirements). "
		     "Allowed values are only 'dec' and 'yr'."
	),
	CFsubhr_frequency=ParameterSettings(
        key="CFsubhr_frequency",
		default_values=[
			ValueSettings(key_type="laboratory", keys="CFsubhr_frequency"),
			"1ts"
		],
		help="CFMIP has an elaborated requirement for defining subhr frequency; by default, dr2xml uses 1 time step."
	),
	simple_domain_grid_regexp=ParameterSettings(
        key="simple_domain_grid_regexp",
		default_values=[
			ValueSettings(key_type="laboratory", keys="simple_domain_grid_regexp")
		],
		help="If some grid is not defined in xml but by API, and is referenced by a "
		     "field which is considered by the DR as having a singleton dimension, then: "
		     "1) it must be a grid which has only a domain "
		     "2) the domain name must be extractable from the grid_id using a regexp and a group number "
		     "Example: using a pattern that returns full id except for a '_grid' suffix"
	),
	vertical_interpolation_operation=ParameterSettings(
        key="vertical_interpolation_operation",
		default_values=[
			ValueSettings(key_type="laboratory", keys="vertical_interpolation_operation"),
			"instant"
		],
		help="Operation done for vertical interpolation."
	),
	vertical_interpolation_sample_freq=ParameterSettings(
        key="vertical_interpolation_sample_freq",
		default_values=[
			ValueSettings(key_type="laboratory", keys="vertical_interpolation_sample_freq")
		],
		help="Time frequency of vertical interpolation."
	),
	sectors=ParameterSettings(
        key="sectors",
		default_values=[
			ValueSettings(key_type="laboratory", keys="sectors")
		],
		help="List of the sectors to be considered."
	),
	non_standard_axes=ParameterSettings(
        key="non_standard_axes",
		default_values=[
			ValueSettings(key_type="laboratory", keys="non_standard_axes"),
			dict()
		],
		help="If your model has some axis which does not have all its attributes as in DR, and you want dr2xml to fix "
		     "that it, give here the correspondence from model axis id to DR dim/grid id. For label dimensions you "
		     "should provide the  list of labels, ordered as in your model, as second element of a pair. "
		     "Label-type axes will be processed even if not quoted. "
		     "Scalar dimensions are not concerned by this feature. "
		     "A dictionary with (axis_id, axis_correct_id) or (axis_id, tuple of labels) as key, values."
	),
	add_Gibraltar=ParameterSettings(
        key="add_Gibraltar",
		default_values=[
			ValueSettings(key_type="laboratory", keys="add_Gibraltar"),
			False
		],
		help="DR01.00.21 does not include Gibraltar strait, which is requested by OMIP. "
		     "Can include it, if model provides it as last value of array."
	),
	grid_policy=ParameterSettings(
        key="grid_policy",
		default_values=[
			ValueSettings(key_type="laboratory", keys="grid_policy"),
			False
		],
		fatal=True,
		help="The grid choice policy for output files."
	),
	allow_tos_3hr_1deg=ParameterSettings(
        key="allow_tos_3hr_1deg",
		default_values=[
			ValueSettings(key_type="laboratory", keys="allow_tos_3hr_1deg"),
			True
		],
		help="When using select='no', Xios may enter an endless loop, which is solved if next setting is False."
	),
	adhoc_policy_do_add_1deg_grid_for_tos=ParameterSettings(
        key="adhoc_policy_do_add_1deg_grid_for_tos",
		default_values=[
			ValueSettings(key_type="laboratory", keys="adhoc_policy_do_add_1deg_grid_for_tos"),
			False
		],
		help="Some scenario experiment in DR 01.00.21 do not request tos on 1 degree grid, while other do. "
		     "If you use grid_policy=adhoc and had not changed the mapping of function. "
		     "grids.lab_adhoc_grid_policy to grids.CNRM_grid_policy, next setting can force any tos request "
		     "to also produce tos on a 1 degree grid."
	),
	fx_from_file=ParameterSettings(
        key="fx_from_file",
		default_values=[
			ValueSettings(key_type="laboratory", keys="fx_from_file"),
			list()
		],
		help="You may provide some variables already horizontally remapped to some grid (i.e. Xios domain) in external "
		     "files. The varname in file must match the referenced id in pingfile. Tested only for fixed fields. "
		     "A dictionary with variable id as key and a dictionary as value: "
		     "the key must be the grid id, the value a dictionary with the file for each resolution."
	),
	prefixed_orography_field_name=ParameterSettings(
        key="prefixed_orography_field_name",
		default_values=[
			ValueSettings(key_type="combine",
			              keys=[
				              ValueSettings(key_type="internal", keys="ping_variables_prefix"),
				              ValueSettings(key_type="internal", keys="orography_field_name")
			              ],
			              fmt="{}{}"),
		],
		help="Name of the orography field name to be used to compute height over orog fields prefixed with "
		     ":term:`ping_variable_prefix`."
	),
	orography_field_name=ParameterSettings(
        key="orography_field_name",
		default_values=[
			ValueSettings(key_type="laboratory", keys="orography_field_name"),
			"orog"
		],
		help="Name of the orography field name to be used to compute height over orog fields."
	),
	zg_field_name=ParameterSettings(
        key="zg_field_name",
		default_values=[
			ValueSettings(key_type="laboratory", keys="zg_field_name"),
			"zg"
		],
		help="Name of the geopotential height field name to be used to compute height over orog fields."
	),
	print_variables=ParameterSettings(
        key="print_variables",
		default_values=[
			ValueSettings(key_type="laboratory", keys="print_variables"),
			True
		],
		help="If the value is a list, only the file/field variables listed here will be put in output files. "
		     "If boolean, tell if the file/field variables should be put in output files."
	),
	grids_dev=ParameterSettings(
        key="grids_dev",
		default_values=[
			ValueSettings(key_type="laboratory", keys="grids_dev"),
			dict()
		],
		fatal=True,
		help="Grids definition for dev variables."
	),
	grids=ParameterSettings(
        key="grids",
		default_values=[
			ValueSettings(key_type="laboratory", keys="grids")
		],
		fatal=True,
		help="Grids : per model resolution and per context :"
		     "- CMIP6 qualifier (i.e. 'gn' or 'gr') for the main grid chosen (because you"
		     "  may choose has main production grid a regular one, when the native grid is e.g. unstructured)"
		     "- Xios id for the production grid (if it is not the native grid),"
		     "- Xios id for the latitude axis used for zonal means (mist match latitudes for grid above)"
		     "- resolution of the production grid (using CMIP6 conventions),"
		     "- grid description"
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
		fatal=True,
		help="Dictionary which gives, for each model name, the components that must be present."
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
		fatal=True,
		help="Dictionary which contains, for each model, the list of components whih can be used in addition to the "
		     "declared ones."
	),
	max_split_freq=ParameterSettings(
        key="max_split_freq",
		default_values=[
			ValueSettings(key_type="simulation", keys="max_split_freq"),
			ValueSettings(key_type="laboratory", keys="max_split_freq"),
			None
		],
		fatal=True,
		help="The maximum number of years that should be putted in a single file."
	),
	dr2xml_manages_enddate=ParameterSettings(
        key="dr2xml_manages_enddate",
		default_values=[
			ValueSettings(key_type="laboratory", keys="dr2xml_manages_enddate"),
			True
		],
		fatal=True,
		help="A smart workflow will allow you to extend a simulation during it course and to complement the output "
		     "files accordingly, by managing the 'end date' part in filenames. "
		     "You can then set next setting to False."
	),
	non_standard_attributes=ParameterSettings(
        key="non_standard_attributes",
		default_values=[
			ValueSettings(key_type="laboratory", keys="non_standard_attributes"),
			dict()
		],
		help="You may add a series of NetCDF attributes in all files for this simulation"
	),
	allow_duplicates_in_same_table=ParameterSettings(
        key="allow_duplicates_in_same_table",
		default_values=[
			ValueSettings(key_type="laboratory", keys="allow_duplicates_in_same_table"),
			False
		],
		fatal=True,
		help="Should we allow for another type of duplicate vars : two vars with same name in same table "
		     "(usually with different shapes). This applies to e.g. CMOR vars 'ua' and 'ua7h' in "
		     "6hPlevPt. Default to False, because CMIP6 rules does not allow to name output files differently in that "
		     "case. If set to True, you should also set 'use_cmorvar_label_in_filename' to True to overcome the said "
		     "rule."
	),
	use_cmorvar_label_in_filename=ParameterSettings(
        key="use_cmorvar_label_in_filename",
		default_values=[
			ValueSettings(key_type="laboratory", keys="use_cmorvar_label_in_filename"),
			False
		],
		fatal=True,
		help="CMIP6 rule is that filenames includes the variable label, and that this variable label is not the CMORvar "
		     "label, but 'MIPvar' label. This may lead to conflicts, e.g. for 'ua' and 'ua7h' in table 6hPlevPt; "
		     "allows to avoid that, if set to True."
	),
	nemo_sources_management_policy_master_of_the_world=ParameterSettings(
        key="nemo_sources_management_policy_master_of_the_world",
		default_values=[
			ValueSettings(key_type="laboratory", keys="nemo_sources_management_policy_master_of_the_world"),
			False
		],
		fatal=True,
		help="Set that to True if you use a context named 'nemo' and the corresponding model unduly sets "
		     "a general freq_op AT THE FIELD_DEFINITION GROUP LEVEL. Due to Xios rules for inheritance, "
		     "that behavior prevents inheriting specific freq_ops by reference from dr2xml generated field_definitions."
	),
	special_timestep_vars=ParameterSettings(
        key="special_timestep_vars",
		default_values=[
			ValueSettings(key_type="laboratory", keys="special_timestep_vars"),
			list()
		],
		help="This variable is used when some variables are computed with a period which is not the basic timestep. "
		     "A dictionary which keys are non standard timestep and values the list of variables "
		     "which are computed at this timestep."
	),
	useAtForInstant=ParameterSettings(
        key="useAtForInstant",
		default_values=[
			ValueSettings(key_type="laboratory", keys="useAtForInstant"),
			False
		],
		help="Should xml output files use the `@` symbol for definitions for instant variables?"
	),
	bypass_CV_components=ParameterSettings(
        key="bypass_CV_components",
		default_values=[
			ValueSettings(key_type="laboratory", keys="bypass_CV_components"),
			False
		],
		help="If the CMIP6 Controlled Vocabulary doesn't allow all the components you activate, you can set "
		     "next toggle to True"
	),
	data_request_used=ParameterSettings(
        key="data_request_used",
		default_values=[
			ValueSettings(key_type="laboratory", keys="data_request_used"),
			"CMIP6"
		],
		help="The Data Request infrastructure type which should be used."
	),
	data_request_path=ParameterSettings(
        key="data_request_path",
		default_values=[
			ValueSettings(key_type="laboratory", keys="data_request_path"),
			None
		],
		help="Path where the data request API used is placed."
	),
	data_request_content_version=ParameterSettings(
		key="data_request_content_version",
		default_values=[
			ValueSettings(key_type="laboratory", keys="data_request_content_version"),
			"latest_stable"
		],
		help="Version of the data request content to be used"
	),
	data_request_config=ParameterSettings(
		key="data_request_config",
		default_values=[
			ValueSettings(key_type="laboratory", keys="data_request_config"),
			os.sep.join([os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dr_interface", "CMIP7_config"])
		],
		help="Configuration file of the data request content to be used"
	),
	laboratory_used=ParameterSettings(
        key="laboratory_used",
		default_values=[
			ValueSettings(key_type="laboratory", keys="laboratory_used"),
			None
		],
		help="File which contains the settings to be used for a specific laboratory which is not present by default in "
		     "dr2xml. Must contains at least the `lab_grid_policy` function."
	),
	save_project_settings=ParameterSettings(
        key="save_project_settings",
		default_values=[
			ValueSettings(key_type="laboratory", keys="save_project_settings"),
			None
		],
		help="The path of the file where the complete project settings will be written, if needed."
	),
	perso_sdims_description=ParameterSettings(
        key="perso_sdims_description",
		default_values=[
			ValueSettings(key_type="simulation", keys="perso_sdims_description"),
			dict()
		],
		help="A dictionary containing, for each perso or dev variables with a XY-perso shape, and for each vertical "
		     "coordinate associated, the main attributes of the dimension."
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
		fatal=True,
		help="A dictionary which keys are context names and values the lists of realms associated with each context"
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
		fatal=True,
		help="If the default source-type value for your source "
		     "(:term:`source_types` from :term:`lab_and_model_settings`) "
		     "does not fit, you may change it here. "
		     "This should describe the model most directly responsible for the output. "
		     "Sometimes it is appropriate to list two (or more) model types here, among AER, AGCM, AOGCM, BGC, CHEM, "
		     "ISM, LAND, OGCM, RAD, SLAB e.g. amip , run with CNRM-CM6-1, should quote \"AGCM AER\". "
		     "Also see note 14 of https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit"
	),
	year=ParameterSettings(
        key="year",
		default_values=[
			ValueSettings(key_type="dict", keys="year")
		],
		fatal=True,
		help="Year associated with the launch of dr2xml."
	)
)

common_values = dict(
	prefix=ParameterSettings(
        key="prefix",
		default_values=[
			ValueSettings(key_type="dict", keys="prefix")
		],
		fatal=True,
		help="Prefix to be used for each file definition."
	)
)

project_settings = dict(
	context=TagSettings(
		key="context",
		help="XIOS context beacon"
	),
	file_definition=TagSettings(
		key="file_definition",
		help="XIOS file_definition beacon"
	),
	file=TagSettings(
		key="file",
		help="XIOS file beacon (except for output files)"
	),
	file_output=TagSettings(
		key="file_output",
		help="XIOS file beacon (only for output files)"
	),
	field_definition=TagSettings(
		key="field_definition",
		help="XIOS field_definition beacon"
	),
	field_group=TagSettings(
		key="field_group",
		help="XIOS field_group beacon"
	),
	field=TagSettings(
		key="field",
		help="XIOS field beacon (except for output fields)"
	),
	field_output=TagSettings(
		key="field_output",
		help="XIOS field beacon (only for output fields)"
	),
	grid=TagSettings(
		key="grid",
		help="XIOS grid beacon"
	),
	grid_definition=TagSettings(
		key="grid_definition",
		help="XIOS grid_definition beacon"
	),
	axis=TagSettings(
		key="axis",
		help="XIOS axis beacon"
	),
	zoom_axis=TagSettings(
		key="zoom_axis",
		help="XIOS zoom_axis beacon"
	),
	interpolate_axis=TagSettings(
		key="interpolate_axis",
		help="XIOS interpolate_axis beacon"
	),
	axis_definition=TagSettings(
		key="axis_definition",
		help="XIOS axis_definition beacon"
	),
	axis_group=TagSettings(
		key="axis_group",
		help="XIOS axis_group beacon"
	),
	temporal_splitting=TagSettings(
		key="temporal_splitting",
		help="XIOS temporal_splitting beacon"
	),
	domain=TagSettings(
		key="domain",
		help="XIOS domain beacon"
	),
	generate_rectilinear_domain=TagSettings(
		key="generate_rectilinear_domain",
		help="XIOS generate_rectilinear_domain beacon"
	),
	interpolate_domain=TagSettings(
		key="interpolate_domain",
		help="XIOS interpolate_domain beacon"
	),
	domain_definition=TagSettings(
		key="domain_definition",
		help="XIOS domain_definition beacon"
	),
	domain_group=TagSettings(
		key="domain_group",
		help="XIOS domain_group beacon"
	),
	scalar=TagSettings(
		key="scalar",
		help="XIOS scalar beacon"
	),
	duplicate_scalar=TagSettings(
		key="duplicate_scalar",
		help="XIOS duplicate_scalar beacon"
	),
	scalar_definition=TagSettings(
		key="scalar_definition",
		help="XIOS scalar_definition beacon"
	),
	variable=TagSettings(
		key="variable",
		help="XIOS variable beacon",
		attrs_list=["name", "type"],
		attrs_constraints=dict(
			name=ParameterSettings(
				key="name",
				help="Content of the variable"
			),
			type=ParameterSettings(
				key="type",
				help="Encoding type of the variable's content."
			)
		)
	)
)
