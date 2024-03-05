Parameters available for project dr2xml
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
   
   prefix
      
      TODO
      
      fatal: True
      
      default values:
         
         - dict['prefix']
      
      num type: 'string'
      
   root
      
      TODO
      
      fatal: True
      
      default values:
         
         - dict['root']
      
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
   
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': ['name', 'type'], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})
TagSettings({'dict_default': {'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}}, 'attrs_list': [], 'attrs_constraints': {}, 'vars_list': [], 'vars_constraints': {}, 'comments_list': [], 'comments_constraints': {}})