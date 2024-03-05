Parameters available for project basics
=======================================

Internal values
---------------
.. glossary::
   :sorted:
   
   CFsubhr_frequency
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['CFsubhr_frequency']
         - '1ts'
      
      num type: 'string'
      
   add_Gibraltar
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['add_Gibraltar']
         - False
      
      num type: 'string'
      
   additional_allowed_model_components
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['additional_allowed_model_components'][internal['source_id']]
         - []
      
      num type: 'string'
      
   adhoc_policy_do_add_1deg_grid_for_tos
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['adhoc_policy_do_add_1deg_grid_for_tos']
         - False
      
      num type: 'string'
      
   allow_duplicates
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['allow_duplicates']
         - True
      
      num type: 'string'
      
   allow_duplicates_in_same_table
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['allow_duplicates_in_same_table']
         - False
      
      num type: 'string'
      
   allow_pseudo_standard_names
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['allow_pseudo_standard_names']
         - False
      
      num type: 'string'
      
   allow_tos_3hr_1deg
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['allow_tos_3hr_1deg']
         - True
      
      num type: 'string'
      
   branch_year_in_child
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['branch_year_in_child']
      
      num type: 'string'
      
   branching
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['branching'][internal['source_id']]
         - {}
      
      num type: 'string'
      
   bypass_CV_components
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['bypass_CV_components']
         - False
      
      num type: 'string'
      
   bytes_per_float
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['bytes_per_float']
         - 2
      
      num type: 'string'
      
   configuration
      
      TODO
      
      fatal: True
      
      default values:
         
         - simulation['configuration']
      
      num type: 'string'
      
   context
      
      TODO
      
      fatal: True
      
      default values:
         
         - dict['context']
      
      num type: 'string'
      
   data_request_path
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['data_request_path']
         - None
      
      num type: 'string'
      
   data_request_used
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['data_request_used']
         - 'CMIP6'
      
      num type: 'string'
      
   debug_parsing
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['debug_parsing']
         - False
      
      num type: 'string'
      
   dr2xml_manages_enddate
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['dr2xml_manages_enddate']
         - True
      
      num type: 'string'
      
   end_year
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['end_year']
         - False
      
      num type: 'string'
      
   excluded_pairs_lset
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['excluded_pairs']
         - []
      
      num type: 'string'
      
   excluded_pairs_sset
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['excluded_pairs']
         - []
      
      num type: 'string'
      
   excluded_request_links
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['excluded_request_links']
         - []
      
      num type: 'string'
      
   excluded_spshapes_lset
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['excluded_spshapes']
         - []
      
      num type: 'string'
      
   excluded_tables_lset
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['excluded_tables']
         - []
      
      num type: 'string'
      
   excluded_tables_sset
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['excluded_tables']
         - []
      
      num type: 'string'
      
   excluded_vars_lset
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['excluded_vars']
         - []
      
      num type: 'string'
      
   excluded_vars_per_config
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['excluded_vars_per_config'][internal['configuration']]
         - []
      
      num type: 'string'
      
   excluded_vars_sset
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['excluded_vars']
         - []
      
      num type: 'string'
      
   experiment_for_requests
      
      TODO
      
      fatal: True
      
      default values:
         
         - simulation['experiment_for_requests']
         - internal['experiment_id']
      
      num type: 'string'
      
   experiment_id
      
      TODO
      
      fatal: True
      
      default values:
         
         - simulation['experiment_id']
      
      num type: 'string'
      
   filter_on_realization
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['filter_on_realization']
         - laboratory['filter_on_realization']
         - True
      
      num type: 'string'
      
   fx_from_file
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['fx_from_file']
         - []
      
      num type: 'string'
      
   grid_choice
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['grid_choice'][internal['source_id']]
      
      num type: 'string'
      
   grid_policy
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['grid_policy']
         - False
      
      num type: 'string'
      
   grid_prefix
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['grid_prefix']
         - internal['ping_variables_prefix']
      
      num type: 'string'
      
   grids
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['grids']
      
      num type: 'string'
      
   grids_dev
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['grids_dev']
         - {}
      
      num type: 'string'
      
   grouped_vars_per_file
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['grouped_vars_per_file']
         - laboratory['grouped_vars_per_file']
         - []
      
      num type: 'string'
      
   included_request_links
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['included_request_links']
         - []
      
      num type: 'string'
      
   included_tables
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['included_tables']
         - internal['included_tables_lset']
      
      num type: 'string'
      
   included_tables_lset
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['included_tables']
         - []
      
      num type: 'string'
      
   included_vars
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['included_vars']
         - internal['included_vars_lset']
      
      num type: 'string'
      
   included_vars_lset
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['included_vars']
         - []
      
      num type: 'string'
      
   institution_id
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['institution_id']
      
      num type: 'string'
      
   laboratory_used
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['laboratory_used']
         - None
      
      num type: 'string'
      
   listof_home_vars
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['listof_home_vars']
         - laboratory['listof_home_vars']
         - None
      
      num type: 'string'
      
   max_file_size_in_floats
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['max_file_size_in_floats']
         - 500000000.0
      
      num type: 'string'
      
   max_priority
      
      TODO
      
      fatal: True
      
      default values:
         
         - simulation['max_priority']
         - internal['max_priority_lset']
      
      num type: 'string'
      
   max_priority_lset
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['max_priority']
      
      num type: 'string'
      
   max_split_freq
      
      TODO
      
      fatal: True
      
      default values:
         
         - simulation['max_split_freq']
         - laboratory['max_split_freq']
         - None
      
      num type: 'string'
      
   mips
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['mips']
      
      num type: 'string'
      
   nemo_sources_management_policy_master_of_the_world
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['nemo_sources_management_policy_master_of_the_world']
         - False
      
      num type: 'string'
      
   non_standard_attributes
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['non_standard_attributes']
         - {}
      
      num type: 'string'
      
   non_standard_axes
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['non_standard_axes']
         - {}
      
      num type: 'string'
      
   orography_field_name
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['orography_field_name']
         - 'CMIP6_orog'
      
      num type: 'string'
      
   orphan_variables
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['orphan_variables']
      
      num type: 'string'
      
   path_extra_tables
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['path_extra_tables']
         - laboratory['path_extra_tables']
         - None
      
      num type: 'string'
      
   path_to_parse
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['path_to_parse']
         - './'
      
      num type: 'string'
      
   perso_sdims_description
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['perso_sdims_description']
         - {}
      
      num type: 'string'
      
   ping_variables_prefix
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['ping_variables_prefix']
      
      num type: 'string'
      
   print_stats_per_var_label
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['print_stats_per_var_label']
         - False
      
      num type: 'string'
      
   print_variables
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['print_variables']
         - True
      
      num type: 'string'
      
   project
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['project']
         - 'CMIP6'
      
      num type: 'string'
      
   project_settings
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['project_settings']
         - internal['project']
      
      num type: 'string'
      
   realization_index
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['realization_index']
         - '1'
      
      num type: 'string'
      
   realms_per_context
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['realms_per_context'][internal['context']]
      
      num type: 'string'
      
   required_model_components
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['required_model_components'][internal['source_id']]
         - []
      
      num type: 'string'
      
   sampling_timestep
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['sampling_timestep']
      
      num type: 'string'
      
   save_project_settings
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['save_project_settings']
         - None
      
      num type: 'string'
      
   sectors
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['sectors']
      
      num type: 'string'
      
   simple_domain_grid_regexp
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['simple_domain_grid_regexp']
      
      num type: 'string'
      
   sizes
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['sizes'][internal['grid_choice']]
      
      num type: 'string'
      
   source_id
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['configurations'][internal['configuration']][0]
         - simulation['source_id']
      
      num type: 'string'
      
   source_type
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['configurations'][internal['configuration']][1]
         - simulation['source_type']
         - laboratory['source_types'][internal['source_id']]
      
      num type: 'string'
      
   special_timestep_vars
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['special_timestep_vars']
         - []
      
      num type: 'string'
      
   split_frequencies
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['split_frequencies']
         - laboratory['split_frequencies']
         - 'splitfreqs.dat'
      
      num type: 'string'
      
   tierMax
      
      TODO
      
      fatal: True
      
      default values:
         
         - simulation['tierMax']
         - internal['tierMax_lset']
      
      num type: 'string'
      
   tierMax_lset
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['tierMax']
      
      num type: 'string'
      
   too_long_periods
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['too_long_periods']
         - []
      
      num type: 'string'
      
   useAtForInstant
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['useAtForInstant']
         - False
      
      num type: 'string'
      
   use_cmorvar_label_in_filename
      
      TODO
      
      fatal: True
      
      default values:
         
         - laboratory['use_cmorvar_label_in_filename']
         - False
      
      num type: 'string'
      
   use_union_zoom
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['use_union_zoom']
         - False
      
      num type: 'string'
      
   vertical_interpolation_operation
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['vertical_interpolation_operation']
         - 'instant'
      
      num type: 'string'
      
   vertical_interpolation_sample_freq
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['vertical_interpolation_sample_freq']
      
      num type: 'string'
      
   xios_version
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['xios_version']
         - 2
      
      num type: 'string'
      
   zg_field_name
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['zg_field_name']
         - 'zg'
      
      num type: 'string'
      
Common values
-------------
.. glossary::
   :sorted:
   
   HDL
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['HDL']
         - laboratory['HDL']
      
      num type: 'string'
      
   activity_id
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['activity_id']
         - laboratory['activity_id']
      
      num type: 'string'
      
   branch_method
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['branch_method']
         - 'standard'
      
      num type: 'string'
      
   branch_month_in_parent
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['branch_month_in_parent']
         - '1'
      
      num type: 'string'
      
   branch_year_in_parent
      
      TODO
      
      fatal: False
      
      default values: []
      
      skip values:
         
         - None
         - 'None'
         - ''
         - 'N/A'
      
      cases:
         
         - CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'eq', 'reference_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['branching'], 'fmt': None, 'src': None, 'func': None})]}), ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['branch_year_in_parent'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'eq', 'reference_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['branching', ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None}), 1], 'fmt': None, 'src': None, 'func': None})]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['branch_year_in_parent'], 'fmt': None, 'src': None, 'func': None})})
         - CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['branching'], 'fmt': None, 'src': None, 'func': None})]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['branch_year_in_parent'], 'fmt': None, 'src': None, 'func': None})})
      
      num type: 'string'
      
   comment_lab
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['comment']
         - ''
      
      num type: 'string'
      
   comment_sim
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['comment']
         - ''
      
      num type: 'string'
      
   compression_level
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['compression_level']
         - '0'
      
      num type: 'string'
      
   contact
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['contact']
         - laboratory['contact']
         - 'None'
      
      num type: 'string'
      
   convention_str
      
      TODO
      
      fatal: False
      
      default values:
         
         - ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'config', 'keys': ['conventions'], 'fmt': None, 'src': None, 'func': None})
      
      num type: 'string'
      
   data_specs_version
      
      TODO
      
      fatal: True
      
      default values:
         
         - data_request.get_version()
      
      num type: 'string'
      
   date_range
      
      TODO
      
      fatal: False
      
      default values:
         
         - '%start_date%-%end_date%'
      
      num type: 'string'
      
   description
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['description']
         - laboratory['description']
      
      num type: 'string'
      
   dr2xml_version
      
      TODO
      
      fatal: False
      
      default values:
         
         - ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'config', 'keys': ['version'], 'fmt': None, 'src': None, 'func': None})
      
      num type: 'string'
      
   experiment
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['experiment']
      
      num type: 'string'
      
   expid_in_filename
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['expid_in_filename']
         - internal['experiment_id']
      
      forbidden patterns:
         
         - '.*_.*'
      
      num type: 'string'
      
   forcing_index
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['forcing_index']
         - '1'
      
      num type: 'string'
      
   history
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['history']
         - 'none'
      
      num type: 'string'
      
   info_url
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['info_url']
      
      num type: 'string'
      
   initialization_index
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['initialization_index']
         - '1'
      
      num type: 'string'
      
   institution
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['institution']
      
      num type: 'string'
      
   list_perso_dev_file
      
      TODO
      
      fatal: False
      
      default values:
         
         - 'dr2xml_list_perso_and_dev_file_names'
      
      num type: 'string'
      
   mip_era
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['mip_era']
         - laboratory['mip_era']
      
      num type: 'string'
      
   output_level
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['output_level']
         - '10'
      
      num type: 'string'
      
   parent_activity_id
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['parent_activity_id']
         - simulation['activity_id']
         - laboratory['parent_activity_id']
         - laboratory['activity_id']
      
      num type: 'string'
      
   parent_experiment_id
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['parent_experiment_id']
         - laboratory['parent_experiment_id']
      
      num type: 'string'
      
   parent_mip_era
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['parent_mip_era']
      
      num type: 'string'
      
   parent_source_id
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['parent_source_id']
      
      num type: 'string'
      
   parent_time_ref_year
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['parent_time_ref_year']
         - '1850'
      
      num type: 'string'
      
   parent_time_units
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['parent_time_units']
      
      num type: 'string'
      
   parent_variant_label
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['parent_variant_label']
      
      num type: 'string'
      
   physics_index
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['physics_index']
         - '1'
      
      num type: 'string'
      
   prefix
      
      TODO
      
      fatal: True
      
      default values:
         
         - dict['prefix']
      
      num type: 'string'
      
   references
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['references']
      
      num type: 'string'
      
   root
      
      TODO
      
      fatal: True
      
      default values:
         
         - dict['root']
      
      num type: 'string'
      
   source
      
      TODO
      
      fatal: False
      
      default values:
         
         - laboratory['source']
      
      num type: 'string'
      
   sub_experiment
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['sub_experiment']
         - 'none'
      
      num type: 'string'
      
   sub_experiment_id
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['sub_experiment_id']
         - 'none'
      
      num type: 'string'
      
   variant_info
      
      TODO
      
      fatal: False
      
      default values:
         
         - simulation['variant_info']
      
      skip values:
         
         - ''
      
      num type: 'string'
      
   year
      
      TODO
      
      fatal: True
      
      default values:
         
         - dict['year']
      
      num type: 'string'
      
Project settings
----------------
.. glossary::
   :sorted:
   
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {'axis_type': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'axis_type', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'axis_type', 'help': 'TODO'}), 'standard_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': <class 'str'>, 'corrections': {}, 'output_key': 'standard_name', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'standard_name', 'help': 'TODO'}), 'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'prec', 'help': 'TODO'}), 'unit': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'unit', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'unit', 'help': 'TODO'}), 'bounds': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'bounds', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'bounds', 'help': 'TODO'}), 'dim_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'dim_name', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'dim_name', 'help': 'TODO'}), 'label': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'label', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'label', 'help': 'TODO'}), 'value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'value', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'value', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['id', 'positive', 'n_glo', 'value', 'axis_ref', 'name', 'standard_name', 'long_name', 'prec', 'unit', 'value', 'bounds', 'dim_name', 'label', 'axis_type'], 'attrs_constraints': {'axis_type': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'axis_type', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'axis_type', 'help': 'TODO'}), 'standard_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': <class 'str'>, 'corrections': {}, 'output_key': 'standard_name', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'standard_name', 'help': 'TODO'}), 'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'prec', 'help': 'TODO'}), 'unit': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'unit', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'unit', 'help': 'TODO'}), 'bounds': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'bounds', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'bounds', 'help': 'TODO'}), 'dim_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'dim_name', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'dim_name', 'help': 'TODO'}), 'label': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'label', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'label', 'help': 'TODO'}), 'value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'value', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'value', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['8'], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'prec', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['prec'], 'attrs_constraints': {'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['8'], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'prec', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {'id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['context'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'id', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {'DR_version': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['data_specs_version'], 'fmt': 'CMIP6 Data Request version {}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'DR_version', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'DR_version', 'help': 'TODO'}), 'dr2xml_version': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['dr2xml_version'], 'fmt': 'dr2xml version {}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'dr2xml_version', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'dr2xml_version', 'help': 'TODO'}), 'lab_settings': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'laboratory', 'keys': [], 'fmt': 'Lab_and_model settings\n{}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'lab_settings', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'lab_settings', 'help': 'TODO'}), 'simulation_settings': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': [], 'fmt': 'Simulation settings\n{}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'simulation_settings', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'simulation_settings', 'help': 'TODO'}), 'year': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['year'], 'fmt': 'Year processed {}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'year', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'year', 'help': 'TODO'})}}, 'attrs_list': ['id'], 'attrs_constraints': {'id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['context'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'id', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': ['DR_version', 'dr2xml_version', 'lab_settings', 'simulation_settings', 'year'], 'comments_constraints': {'DR_version': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['data_specs_version'], 'fmt': 'CMIP6 Data Request version {}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'DR_version', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'DR_version', 'help': 'TODO'}), 'dr2xml_version': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['dr2xml_version'], 'fmt': 'dr2xml version {}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'dr2xml_version', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'dr2xml_version', 'help': 'TODO'}), 'lab_settings': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'laboratory', 'keys': [], 'fmt': 'Lab_and_model settings\n{}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'lab_settings', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'lab_settings', 'help': 'TODO'}), 'simulation_settings': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': [], 'fmt': 'Simulation settings\n{}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'simulation_settings', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'simulation_settings', 'help': 'TODO'}), 'year': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['year'], 'fmt': 'Year processed {}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'year', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'year', 'help': 'TODO'})}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['id', 'ni_glo', 'nj_glo', 'type', 'prec', 'lat_name', 'lon_name', 'dim_i_name', 'domain_ref'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['8'], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'prec', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['prec'], 'attrs_constraints': {'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['8'], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'prec', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['id', 'field_ref', 'name', 'freq_op', 'freq_offset', 'grid_ref', 'long_name', 'standard_name', 'unit', 'operation', 'detect_missing_value', 'prec'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['freq_op', 'freq_offset'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {'name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['mipVarLabel'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'name', 'help': 'TODO'}), 'grid_ref': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'grid_ref', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'grid_ref', 'help': 'TODO'}), 'freq_offset': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'freq_offset', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'freq_offset', 'help': 'TODO'}), 'freq_op': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'freq_op', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'freq_op', 'help': 'TODO'}), 'expr': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'expr', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'expr', 'help': 'TODO'}), 'cell_methods_mode': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['overwrite'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'cell_methods_mode', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'cell_methods_mode', 'help': 'TODO'}), 'cell_methods': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['cell_methods'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'cell_methods', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'cell_methods', 'help': 'TODO'}), 'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['prec'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': True, 'fatal': True, 'key': 'prec', 'help': 'TODO'}), 'default_value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['prec'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': ['0', '1.e+20'], 'authorized_types': [], 'corrections': {'': '1.e+20', 'float': '1.e+20', 'real': '1.e+20', 'double': '1.e+20', 'integer': '0', 'int': '0'}, 'output_key': 'default_value', 'num_type': 'string', 'is_default': True, 'fatal': True, 'key': 'default_value', 'help': 'TODO'}), 'detect_missing_value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['True'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'detect_missing_value', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'detect_missing_value', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {'standard_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['stdname'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'standard_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'standard_name', 'help': 'TODO'}), 'description': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [''], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['description'], 'fmt': None, 'src': None, 'func': None}), 'None'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'description', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'description', 'help': 'TODO'}), 'long_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['long_name'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'long_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'long_name', 'help': 'TODO'}), 'history': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['history'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'history', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'history', 'help': 'TODO'}), 'comment': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['comments', ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['label'], 'fmt': None, 'src': None, 'func': None})], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'laboratory', 'keys': ['comments', ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['label'], 'fmt': None, 'src': None, 'func': None})], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'comment', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'comment', 'help': 'TODO'}), 'positive': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['positive'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'positive', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'positive', 'help': 'TODO'}), 'detect_missing_value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['none'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'detect_missing_value', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'detect_missing_value', 'help': 'TODO'}), 'units': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['units'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'units', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'units', 'help': 'TODO'}), 'cell_methods': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['cell_methods'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'cell_methods', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'cell_methods', 'help': 'TODO'}), 'cell_measures': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['cell_measures'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'cell_measures', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'cell_measures', 'help': 'TODO'}), 'flag_meanings': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['flag_meanings'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'flag_meanings', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'flag_meanings', 'help': 'TODO'}), 'flag_values': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['flag_values'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'flag_values', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'flag_values', 'help': 'TODO'}), 'interval_operation': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'dict', 'keys': ['operation'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['once']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'interval_operation', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'interval_operation', 'help': 'TODO'})}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['field_ref', 'name', 'grid_ref', 'freq_offset', 'detect_missing_value', 'default_value', 'prec', 'cell_methods', 'cell_methods_mode', 'operation', 'freq_op', 'expr'], 'attrs_constraints': {'name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['mipVarLabel'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'name', 'help': 'TODO'}), 'grid_ref': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'grid_ref', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'grid_ref', 'help': 'TODO'}), 'freq_offset': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'freq_offset', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'freq_offset', 'help': 'TODO'}), 'freq_op': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'freq_op', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'freq_op', 'help': 'TODO'}), 'expr': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'expr', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'expr', 'help': 'TODO'}), 'cell_methods_mode': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['overwrite'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'cell_methods_mode', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'cell_methods_mode', 'help': 'TODO'}), 'cell_methods': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['cell_methods'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'cell_methods', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'cell_methods', 'help': 'TODO'}), 'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['prec'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': True, 'fatal': True, 'key': 'prec', 'help': 'TODO'}), 'default_value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['prec'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': ['0', '1.e+20'], 'authorized_types': [], 'corrections': {'': '1.e+20', 'float': '1.e+20', 'real': '1.e+20', 'double': '1.e+20', 'integer': '0', 'int': '0'}, 'output_key': 'default_value', 'num_type': 'string', 'is_default': True, 'fatal': True, 'key': 'default_value', 'help': 'TODO'}), 'detect_missing_value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['True'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'detect_missing_value', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'detect_missing_value', 'help': 'TODO'})}, 'vars_list': ['comment', 'standard_name', 'description', 'long_name', 'positive', 'history', 'units', 'cell_methods', 'cell_measures', 'flag_meanings', 'flag_values', 'interval_operation'], 'vars_constraints': {'standard_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['stdname'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'standard_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'standard_name', 'help': 'TODO'}), 'description': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [''], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['description'], 'fmt': None, 'src': None, 'func': None}), 'None'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'description', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'description', 'help': 'TODO'}), 'long_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['long_name'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'long_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'long_name', 'help': 'TODO'}), 'history': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['history'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'history', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'history', 'help': 'TODO'}), 'comment': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['comments', ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['label'], 'fmt': None, 'src': None, 'func': None})], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'laboratory', 'keys': ['comments', ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['label'], 'fmt': None, 'src': None, 'func': None})], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'comment', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'comment', 'help': 'TODO'}), 'positive': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['positive'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'positive', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'positive', 'help': 'TODO'}), 'detect_missing_value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['none'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'detect_missing_value', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'detect_missing_value', 'help': 'TODO'}), 'units': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['units'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'units', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'units', 'help': 'TODO'}), 'cell_methods': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['cell_methods'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'cell_methods', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'cell_methods', 'help': 'TODO'}), 'cell_measures': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['cell_measures'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'cell_measures', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'cell_measures', 'help': 'TODO'}), 'flag_meanings': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['flag_meanings'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'flag_meanings', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'flag_meanings', 'help': 'TODO'}), 'flag_values': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['flag_values'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'flag_values', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'flag_values', 'help': 'TODO'}), 'interval_operation': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'dict', 'keys': ['operation'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['once']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'interval_operation', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'interval_operation', 'help': 'TODO'})}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['id', 'name', 'mode', 'output_freq', 'enabled'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {'type': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['one_file'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'type', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'type', 'help': 'TODO'}), 'enabled': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['true'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'enabled', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'enabled', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['type', 'enabled'], 'attrs_constraints': {'type': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['one_file'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'type', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'type', 'help': 'TODO'}), 'enabled': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['true'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'enabled', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'enabled', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {'id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['label'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'dict', 'keys': ['table_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'dict', 'keys': ['grid_label'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{}_{}_{}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'id', 'help': 'TODO'}), 'split_freq': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_freq', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_freq', 'help': 'TODO'}), 'split_freq_format': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_freq_format', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_freq_format', 'help': 'TODO'}), 'split_start_offset': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', 'False', None, False], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_start_offset', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_start_offset', 'help': 'TODO'}), 'split_end_offset': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', 'False', None, False], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_end_offset', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_end_offset', 'help': 'TODO'}), 'split_last_date': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_last_date', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_last_date', 'help': 'TODO'}), 'append': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['true'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'append', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'append', 'help': 'TODO'}), 'time_units': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['days'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_units', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_units', 'help': 'TODO'}), 'time_counter_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['time'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_counter_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_counter_name', 'help': 'TODO'}), 'time_counter': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['exclusive'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_counter', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_counter', 'help': 'TODO'}), 'time_stamp_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['creation_date'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_stamp_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_stamp_name', 'help': 'TODO'}), 'time_stamp_format': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['%Y-%m-%dT%H:%M:%SZ'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_stamp_format', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_stamp_format', 'help': 'TODO'}), 'uuid_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['tracking_id'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'uuid_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'uuid_name', 'help': 'TODO'}), 'uuid_format': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['None', '', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['HDL'], 'fmt': 'hdl:{}/%uuid%', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'uuid_format', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'uuid_format', 'help': 'TODO'}), 'convention_str': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['convention_str'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'convention_str', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'convention_str', 'help': 'TODO'}), 'output_level': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['None', '', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['output_level'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'output_level', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'output_level', 'help': 'TODO'}), 'compression_level': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['None', '', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['compression_level'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'compression_level', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'compression_level', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {'contact': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['None', '', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['contact'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'contact', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'contact', 'help': 'TODO'}), 'data_specs_version': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['data_specs_version'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'data_specs_version', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'data_specs_version', 'help': 'TODO'}), 'dr2xml_version': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['dr2xml_version'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'dr2xml_version', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'dr2xml_version', 'help': 'TODO'}), 'expid_in_filename': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'experiment_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'expid_in_filename', 'help': 'TODO'}), 'description': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'eq', 'reference_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})]})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['description'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'description', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'description', 'help': 'TODO'}), 'title_desc': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'eq', 'reference_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})]})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['description'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'title', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'title_desc', 'help': 'TODO'}), 'experiment': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'eq', 'reference_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})]})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['experiment'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'experiment', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'experiment', 'help': 'TODO'}), 'external_variables': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [''], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['cell_measures'], 'fmt': None, 'src': None, 'func': FunctionSettings({'func': <function build_external_variables at 0x7f5c3424baf0>, 'options': {}})})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'external_variables', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'external_variables', 'help': 'TODO'}), 'forcing_index': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['forcing_index'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'forcing_index', 'num_type': 'int', 'is_default': True, 'fatal': False, 'key': 'forcing_index', 'help': 'TODO'}), 'further_info_url': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'further_info_url', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'further_info_url', 'help': 'TODO'}), 'history': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['history'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'history', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'history', 'help': 'TODO'}), 'initialization_index': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['initialization_index'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'initialization_index', 'num_type': 'int', 'is_default': True, 'fatal': False, 'key': 'initialization_index', 'help': 'TODO'}), 'institution': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['institution'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'institution', 'num_type': 'string', 'is_default': True, 'fatal': True, 'key': 'institution', 'help': 'TODO'}), 'institution_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['institution_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'institution_id', 'num_type': 'string', 'is_default': True, 'fatal': True, 'key': 'institution_id', 'help': 'TODO'}), 'mip_era': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['mip_era'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['mip_era'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'mip_era', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'mip_era', 'help': 'TODO'}), 'parent_experiment_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_experiment_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_experiment_id', 'help': 'TODO'}), 'parent_mip_era': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_mip_era'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['mip_era'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['mip_era'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_mip_era', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_mip_era', 'help': 'TODO'}), 'parent_activity_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_activity_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_activity_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_activity_id', 'help': 'TODO'}), 'parent_source_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_source_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_source_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_source_id', 'help': 'TODO'}), 'parent_time_units': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_time_units'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_time_ref_year'], 'fmt': 'days since {}-01-01 00:00:00', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_time_units', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_time_units', 'help': 'TODO'}), 'parent_variant_label': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_variant_label'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['variant_label'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_variant_label', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_variant_label', 'help': 'TODO'}), 'branch_time_in_parent': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': FunctionSettings({'func': <function compute_nb_days at 0x7f5c3424bb80>, 'options': {'year_ref': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_time_ref_year'], 'fmt': None, 'src': None, 'func': None}), 'year_branch': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['branch_year_in_parent'], 'fmt': None, 'src': None, 'func': None}), 'month_branch': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['branch_month_in_parent'], 'fmt': None, 'src': None, 'func': None})}})}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['branch_time_in_parent'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'branch_time_in_parent', 'num_type': 'double', 'is_default': True, 'fatal': False, 'key': 'branch_time_in_parent', 'help': 'TODO'}), 'branch_time_in_child': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': FunctionSettings({'func': <function compute_nb_days at 0x7f5c3424bb80>, 'options': {'year_ref': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['child_time_ref_year'], 'fmt': None, 'src': None, 'func': None}), 'year_branch': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['branch_year_in_child'], 'fmt': None, 'src': None, 'func': None})}})}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['branch_time_in_child'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'branch_time_in_child', 'num_type': 'double', 'is_default': True, 'fatal': False, 'key': 'branch_time_in_child', 'help': 'TODO'}), 'branch_method': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['branch_method'], 'fmt': None, 'src': None, 'func': None})}), CaseSettings({'conditions': [True], 'value': 'no parent'})], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'branch_method', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'branch_method', 'help': 'TODO'}), 'physics_index': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['physics_index'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'physics_index', 'num_type': 'int', 'is_default': True, 'fatal': False, 'key': 'physics_index', 'help': 'TODO'}), 'product': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['model-output'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'product', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'product', 'help': 'TODO'}), 'realization_index': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['realization_index'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'realization_index', 'num_type': 'int', 'is_default': True, 'fatal': False, 'key': 'realization_index', 'help': 'TODO'}), 'references': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['references'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'references', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'references', 'help': 'TODO'}), 'sub_experiment_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['sub_experiment_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'sub_experiment_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'sub_experiment_id', 'help': 'TODO'}), 'sub_experiment': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['sub_experiment'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'sub_experiment', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'sub_experiment', 'help': 'TODO'}), 'variant_info': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['variant_info'], 'fmt': '. Information provided by this attribute may in some cases be flawed. Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute.', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'variant_info', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'variant_info', 'help': 'TODO'}), 'realm': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['modeling_realm'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'realm', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'realm', 'help': 'TODO'}), 'frequency': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'frequency', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'frequency', 'help': 'TODO'}), 'comment': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [''], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['comments'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['comments'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{}{}{}', 'src': None, 'func': None})}), CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]}), ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{}{}', 'src': None, 'func': None})}), CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None})}), CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None})})], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'comment', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'comment', 'help': 'TODO'}), 'variant_label': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['variant_label'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'variant_label', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'variant_label', 'help': 'TODO'}), 'activity_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['activity_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'activity_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'activity_id', 'help': 'TODO'}), 'source': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['source'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'source', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'source', 'help': 'TODO'}), 'source_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'source_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'source_id', 'help': 'TODO'}), 'source_type': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_type'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'source_type', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'source_type', 'help': 'TODO'}), 'title': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['project'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['activity_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{} model output prepared for {} and {} / {} simulation', 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['project'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['activity_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{} model output prepared for {} / {} {}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'title', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'title', 'help': 'TODO'})}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['id', 'name', 'output_freq', 'append', 'output_level', 'compression_level', 'split_freq', 'split_freq_format', 'split_start_offset', 'split_end_offset', 'split_last_date', 'time_units', 'time_counter_name', 'time_counter', 'time_stamp_name', 'time_stamp_format', 'uuid_name', 'uuid_format', 'convention_str'], 'attrs_constraints': {'id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['label'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'dict', 'keys': ['table_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'dict', 'keys': ['grid_label'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{}_{}_{}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'id', 'help': 'TODO'}), 'split_freq': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_freq', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_freq', 'help': 'TODO'}), 'split_freq_format': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_freq_format', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_freq_format', 'help': 'TODO'}), 'split_start_offset': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', 'False', None, False], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_start_offset', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_start_offset', 'help': 'TODO'}), 'split_end_offset': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', 'False', None, False], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_end_offset', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_end_offset', 'help': 'TODO'}), 'split_last_date': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'nmatch', 'reference_values': ['.*fx.*']})], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'split_last_date', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'split_last_date', 'help': 'TODO'}), 'append': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['true'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'append', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'append', 'help': 'TODO'}), 'time_units': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['days'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_units', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_units', 'help': 'TODO'}), 'time_counter_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['time'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_counter_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_counter_name', 'help': 'TODO'}), 'time_counter': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['exclusive'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_counter', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_counter', 'help': 'TODO'}), 'time_stamp_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['creation_date'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_stamp_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_stamp_name', 'help': 'TODO'}), 'time_stamp_format': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['%Y-%m-%dT%H:%M:%SZ'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'time_stamp_format', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'time_stamp_format', 'help': 'TODO'}), 'uuid_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['tracking_id'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'uuid_name', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'uuid_name', 'help': 'TODO'}), 'uuid_format': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['None', '', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['HDL'], 'fmt': 'hdl:{}/%uuid%', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'uuid_format', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'uuid_format', 'help': 'TODO'}), 'convention_str': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['convention_str'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'convention_str', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'convention_str', 'help': 'TODO'}), 'output_level': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['None', '', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['output_level'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'output_level', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'output_level', 'help': 'TODO'}), 'compression_level': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['None', '', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['compression_level'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'compression_level', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'compression_level', 'help': 'TODO'})}, 'vars_list': ['activity_id', 'contact', 'data_specs_version', 'dr2xml_version', 'expid_in_filename', 'description', 'title_desc', 'experiment', 'external_variables', 'forcing_index', 'frequency', 'further_info_url', 'grid', 'grid_label', 'nominal_resolution', 'comment', 'history', 'initialization_index', 'institution_id', 'institution', 'license', 'mip_era', 'parent_experiment_id', 'parent_mip_era', 'parent_activity_id', 'parent_source_id', 'parent_time_units', 'parent_variant_label', 'branch_method', 'branch_time_in_parent', 'branch_time_in_child', 'physics_index', 'product', 'realization_index', 'realm', 'references', 'source', 'source_id', 'source_type', 'sub_experiment_id', 'sub_experiment', 'table_id', 'title', 'variable_id', 'variant_info', 'variant_label'], 'vars_constraints': {'contact': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['None', '', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['contact'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'contact', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'contact', 'help': 'TODO'}), 'data_specs_version': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['data_specs_version'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'data_specs_version', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'data_specs_version', 'help': 'TODO'}), 'dr2xml_version': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['dr2xml_version'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'dr2xml_version', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'dr2xml_version', 'help': 'TODO'}), 'expid_in_filename': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'experiment_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'expid_in_filename', 'help': 'TODO'}), 'description': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'eq', 'reference_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})]})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['description'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'description', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'description', 'help': 'TODO'}), 'title_desc': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'eq', 'reference_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})]})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['description'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'title', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'title_desc', 'help': 'TODO'}), 'experiment': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'eq', 'reference_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})]})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['experiment'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'experiment', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'experiment', 'help': 'TODO'}), 'external_variables': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [''], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['cell_measures'], 'fmt': None, 'src': None, 'func': FunctionSettings({'func': <function build_external_variables at 0x7f5c3424baf0>, 'options': {}})})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'external_variables', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'external_variables', 'help': 'TODO'}), 'forcing_index': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['forcing_index'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'forcing_index', 'num_type': 'int', 'is_default': True, 'fatal': False, 'key': 'forcing_index', 'help': 'TODO'}), 'further_info_url': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'further_info_url', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'further_info_url', 'help': 'TODO'}), 'history': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['history'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'history', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'history', 'help': 'TODO'}), 'initialization_index': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['initialization_index'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'initialization_index', 'num_type': 'int', 'is_default': True, 'fatal': False, 'key': 'initialization_index', 'help': 'TODO'}), 'institution': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['institution'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'institution', 'num_type': 'string', 'is_default': True, 'fatal': True, 'key': 'institution', 'help': 'TODO'}), 'institution_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['institution_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'institution_id', 'num_type': 'string', 'is_default': True, 'fatal': True, 'key': 'institution_id', 'help': 'TODO'}), 'mip_era': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['mip_era'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['mip_era'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'mip_era', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'mip_era', 'help': 'TODO'}), 'parent_experiment_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_experiment_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_experiment_id', 'help': 'TODO'}), 'parent_mip_era': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_mip_era'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['mip_era'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['mip_era'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_mip_era', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_mip_era', 'help': 'TODO'}), 'parent_activity_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_activity_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_activity_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_activity_id', 'help': 'TODO'}), 'parent_source_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_source_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_source_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_source_id', 'help': 'TODO'}), 'parent_time_units': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_time_units'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_time_ref_year'], 'fmt': 'days since {}-01-01 00:00:00', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_time_units', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_time_units', 'help': 'TODO'}), 'parent_variant_label': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_variant_label'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['variant_label'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'parent_variant_label', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'parent_variant_label', 'help': 'TODO'}), 'branch_time_in_parent': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': FunctionSettings({'func': <function compute_nb_days at 0x7f5c3424bb80>, 'options': {'year_ref': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_time_ref_year'], 'fmt': None, 'src': None, 'func': None}), 'year_branch': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['branch_year_in_parent'], 'fmt': None, 'src': None, 'func': None}), 'month_branch': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['branch_month_in_parent'], 'fmt': None, 'src': None, 'func': None})}})}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['branch_time_in_parent'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'branch_time_in_parent', 'num_type': 'double', 'is_default': True, 'fatal': False, 'key': 'branch_time_in_parent', 'help': 'TODO'}), 'branch_time_in_child': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': FunctionSettings({'func': <function compute_nb_days at 0x7f5c3424bb80>, 'options': {'year_ref': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['child_time_ref_year'], 'fmt': None, 'src': None, 'func': None}), 'year_branch': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['branch_year_in_child'], 'fmt': None, 'src': None, 'func': None})}})}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['branch_time_in_child'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'branch_time_in_child', 'num_type': 'double', 'is_default': True, 'fatal': False, 'key': 'branch_time_in_child', 'help': 'TODO'}), 'branch_method': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['parent_experiment_id'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['no parent', '', 'None']})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['branch_method'], 'fmt': None, 'src': None, 'func': None})}), CaseSettings({'conditions': [True], 'value': 'no parent'})], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'branch_method', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'branch_method', 'help': 'TODO'}), 'physics_index': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['physics_index'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'physics_index', 'num_type': 'int', 'is_default': True, 'fatal': False, 'key': 'physics_index', 'help': 'TODO'}), 'product': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': ['model-output'], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'product', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'product', 'help': 'TODO'}), 'realization_index': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['realization_index'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'realization_index', 'num_type': 'int', 'is_default': True, 'fatal': False, 'key': 'realization_index', 'help': 'TODO'}), 'references': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['references'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'references', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'references', 'help': 'TODO'}), 'sub_experiment_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['sub_experiment_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'sub_experiment_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'sub_experiment_id', 'help': 'TODO'}), 'sub_experiment': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['sub_experiment'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'sub_experiment', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'sub_experiment', 'help': 'TODO'}), 'variant_info': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['variant_info'], 'fmt': '. Information provided by this attribute may in some cases be flawed. Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute.', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'variant_info', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'variant_info', 'help': 'TODO'}), 'realm': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['modeling_realm'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'realm', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'realm', 'help': 'TODO'}), 'frequency': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['frequency'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'frequency', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'frequency', 'help': 'TODO'}), 'comment': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [''], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['comments'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'variable', 'keys': ['comments'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{}{}{}', 'src': None, 'func': None})}), CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]}), ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{}{}', 'src': None, 'func': None})}), CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_sim'], 'fmt': None, 'src': None, 'func': None})}), CaseSettings({'conditions': [ConditionSettings({'check_value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None}), 'check_to_do': 'neq', 'reference_values': ['', 'None', None]})], 'value': ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['comment_lab'], 'fmt': None, 'src': None, 'func': None})})], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'comment', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'comment', 'help': 'TODO'}), 'variant_label': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['variant_label'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'variant_label', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'variant_label', 'help': 'TODO'}), 'activity_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['activity_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'activity_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'activity_id', 'help': 'TODO'}), 'source': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['source'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'source', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'source', 'help': 'TODO'}), 'source_id': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_id'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'source_id', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'source_id', 'help': 'TODO'}), 'source_type': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_type'], 'fmt': None, 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'source_type', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'source_type', 'help': 'TODO'}), 'title': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['project'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['activity_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'simulation', 'keys': ['expid_in_filename'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{} model output prepared for {} and {} / {} simulation', 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'combine', 'keys': [ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['source_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['project'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'common', 'keys': ['activity_id'], 'fmt': None, 'src': None, 'func': None}), ValueSettings({'dict_default': {'key_type': None, 'keys': [], 'fmt': None, 'src': None, 'func': None}, 'key_type': 'internal', 'keys': ['experiment_id'], 'fmt': None, 'src': None, 'func': None})], 'fmt': '{} model output prepared for {} / {} {}', 'src': None, 'func': None})], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'title', 'num_type': 'string', 'is_default': True, 'fatal': False, 'key': 'title', 'help': 'TODO'})}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['id'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['type', 'order', 'coordinate'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['type', 'order', 'renormalize', 'mode', 'write_weight', 'coordinate'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {'standard_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'standard_name', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'standard_name', 'help': 'TODO'}), 'axis_type': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'axis_type', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'axis_type', 'help': 'TODO'}), 'unit': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'unit', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'unit', 'help': 'TODO'}), 'label': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'label', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'label', 'help': 'TODO'}), 'bounds': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'bounds', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'bounds', 'help': 'TODO'}), 'bounds_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'bounds_name', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'bounds_name', 'help': 'TODO'}), 'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'prec', 'help': 'TODO'}), 'value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'value', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'value', 'help': 'TODO'}), 'positive': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'positive', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'positive', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['id', 'scalar_ref', 'name', 'standard_name', 'long_name', 'label', 'prec', 'value', 'bounds', 'bounds_name', 'axis_type', 'positive', 'unit'], 'attrs_constraints': {'standard_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'standard_name', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'standard_name', 'help': 'TODO'}), 'axis_type': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'axis_type', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'axis_type', 'help': 'TODO'}), 'unit': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'unit', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'unit', 'help': 'TODO'}), 'label': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'label', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'label', 'help': 'TODO'}), 'bounds': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'bounds', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'bounds', 'help': 'TODO'}), 'bounds_name': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'bounds_name', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'bounds_name', 'help': 'TODO'}), 'prec': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': ['2', '4', '8'], 'authorized_types': [], 'corrections': {'': '4', 'float': '4', 'real': '4', 'double': '8', 'integer': '2', 'int': '2'}, 'output_key': 'prec', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'prec', 'help': 'TODO'}), 'value': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'value', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'value', 'help': 'TODO'}), 'positive': ParameterSettings({'dict_default': {'skip_values': [], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': None, 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': None, 'help': 'TODO'}, 'skip_values': ['', 'None', None], 'forbidden_patterns': [], 'conditions': [], 'default_values': [], 'cases': [], 'authorized_values': [], 'authorized_types': [], 'corrections': {}, 'output_key': 'positive', 'num_type': 'string', 'is_default': False, 'fatal': False, 'key': 'positive', 'help': 'TODO'})}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['name', 'type'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['index'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})