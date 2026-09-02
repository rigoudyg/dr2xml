Parameters available for project dr2xml
=======================================

Init values
---------------
.. glossary::
   :sorted:
   
   data_request_config
      
      Configuration file of the data request content to be used.
      
      values:
         
         - laboratory[data_request_config]
         - '__package-root__/dr_interface/CMIP7_config'
      
      num type: 'string'
      
   data_request_content_version
      
      Version of the data request content to be used.
      
      values:
         
         - laboratory[data_request_content_version]
         - 'latest_stable'
      
      num type: 'string'
      
   data_request_path
      
      Path where the data request API used is placed.
      
      values:
         
         - laboratory[data_request_path]
         - None
      
      num type: 'string'
      
   data_request_used
      
      The Data Request infrastructure type which should be used.
      
      values:
         
         - laboratory[data_request_used]
         - 'CMIP6'
      
      num type: 'string'
      
   institution_id
      
      Institution identifier.
      
      fatal: True
      
      values:
         
         - laboratory[institution_id]
      
      num type: 'string'
      
   laboratory_used
      
      File which contains the settings to be used for a specific laboratory which is not present by default in dr2xml. Must contains at least the `lab_grid_policy` function.
      
      values:
         
         - laboratory[laboratory_used]
         - None
      
      num type: 'string'
      
   project
      
      Project associated with the simulation.
      
      values:
         
         - laboratory[project]
         - 'CMIP6'
      
      num type: 'string'
      
   project_settings
      
      Project settings definition file to be used.
      
      values:
         
         - laboratory[project_settings]
         - init[project]
      
      num type: 'string'
      
   save_project_settings
      
      The path of the file where the complete project settings will be written, if needed.
      
      values:
         
         - laboratory[save_project_settings]
         - None
      
      num type: 'string'
      
   vocabulary_config
      
      Configuration file of the vocabulary to be used.
      
      values:
         
         - laboratory[vocabulary_config]
         - '__package-root__/vocabulary/vocabulary.json'
      
      num type: 'string'
      
   vocabulary_project
      
      The vocabulary project which should be used.
      
      values:
         
         - laboratory[vocabulary_project] formatted with function from self named lower({})
         - init[project] formatted with function from self named lower({})
      
      num type: 'string'
      
   vocabulary_used
      
      The vocabulary infrastructure type which should be used.
      
      values:
         
         - laboratory[vocabulary_used]
         - None
      
      num type: 'string'
      
Internal values
---------------
.. glossary::
   :sorted:
   
   CFsubhr_frequency
      
      CFMIP has an elaborated requirement for defining subhr frequency; by default, dr2xml uses 1 time step.
      
      values:
         
         - laboratory[CFsubhr_frequency]
         - '1ts'
      
      num type: 'string'
      
   add_Gibraltar
      
      DR01.00.21 does not include Gibraltar strait, which is requested by OMIP. Can include it, if model provides it as last value of array.
      
      values:
         
         - laboratory[add_Gibraltar]
         - False
      
      num type: 'string'
      
   additional_allowed_model_components
      
      Dictionary which contains, for each model, the list of components whih can be used in addition to the declared ones.
      
      fatal: True
      
      values:
         
         - laboratory[additional_allowed_components][internal[source_id]]
         - []
      
      num type: 'string'
      
   adhoc_policy_do_add_1deg_grid_for_tos
      
      Some scenario experiment in DR 01.00.21 do not request tos on 1 degree grid, while other do. If you use grid_policy=adhoc and had not changed the mapping of function. grids.lab_adhoc_grid_policy to grids.CNRM_grid_policy, next setting can force any tos request to also produce tos on a 1 degree grid.
      
      values:
         
         - laboratory[adhoc_policy_do_add_1deg_grid_for_tos]
         - False
      
      num type: 'string'
      
   allow_duplicates
      
      Should we allow for duplicate vars: two vars with same frequency, shape and realm, which differ only by the table. In DR01.00.21, this actually applies to very few fields (ps-Aermon, tas-ImonAnt, areacellg-IfxAnt).
      
      values:
         
         - laboratory[allow_duplicates]
         - True
      
      num type: 'string'
      
   allow_duplicates_in_same_table
      
      Should we allow for another type of duplicate vars : two vars with same name in same table (usually with different shapes). This applies to e.g. CMOR vars 'ua' and 'ua7h' in 6hPlevPt. Default to False, because CMIP6 rules does not allow to name output files differently in that case. If set to True, you should also set 'use_cmorvar_label_in_filename' to True to overcome the said rule.
      
      fatal: True
      
      values:
         
         - laboratory[allow_duplicates_in_same_table]
         - False
      
      num type: 'string'
      
   allow_pseudo_standard_names
      
      DR has sn attributes for MIP variables. They can be real,CF-compliant, standard_names or pseudo_standard_names, i.e. not yet approved labels. Default is to use only CF ones.
      
      values:
         
         - laboratory[allow_pseudo_standard_names]
         - False
      
      num type: 'string'
      
   allow_tos_3hr_1deg
      
      When using select='no', Xios may enter an endless loop, which is solved if next setting is False.
      
      values:
         
         - laboratory[allow_tos_3hr_1deg]
         - True
      
      num type: 'string'
      
   branch_year_in_child
      
      In some instances, the experiment start year is not explicit or is doubtful in DR. See file doc/some_experiments_starty_in_DR01.00.21. You should then specify it, using next setting in order that requestItems analysis work in all cases. In some other cases, DR requestItems which apply to the experiment form its start does not cover its whole duration and have a wrong duration (computed based on a wrong start year); They necessitate to fix the start year.
      
      values:
         
         - simulation[branch_year_in_child]
      
      num type: 'string'
      
   branching
      
      Describe the branching scheme for experiments involved in some 'branchedYears type' tslice (for details, see: http://clipc-services.ceda.ac.uk/dreq/index/Slice.html ). Just put the as key the common start year in child and as value the list of start years in parent for all members.A dictionary with models name as key and dictionary containing experiment,(branch year in child, list of branch year in parent) key values.
      
      values:
         
         - laboratory[branching][internal[source_id]]
         - {}
      
      num type: 'string'
      
   bypass_CV_components
      
      If the CMIP6 Controlled Vocabulary doesn't allow all the components you activate, you can set next toggle to True
      
      values:
         
         - laboratory[bypass_CV_components]
         - False
      
      num type: 'string'
      
   bytes_per_float
      
      Estimate of number of bytes per floating value, given the chosen :term:`compression_level`.
      
      values:
         
         - laboratory[bytes_per_float]
         - 2
      
      num type: 'string'
      
   configuration
      
      Configuration used for this experiment. If there is no configuration in lab_settings which matches you case, please rather use next or next two entries: :term:`source_id` and, if needed, :term:`source_type`.
      
      fatal: True
      
      values:
         
         - simulation[configuration]
      
      num type: 'string'
      
   context
      
      Context associated with the xml file produced.
      
      fatal: True
      
      values:
         
         - dict[context]
      
      num type: 'string'
      
   create_csv_file
      
      Pattern containing context if a csv file should be produced, else False.
      
      values:
         
         - laboratory[create_csv_file]
         - False
      
      num type: 'string'
      
   debug_parsing
      
      In order to identify which xml files generates a problem, you can use this flag.
      
      values:
         
         - laboratory[debug_parsing]
         - False
      
      num type: 'string'
      
   default_region
      
      Default region to be used
      
      values:
         
         - laboratory[default_region]
         - 'default'
      
      num type: 'string'
      
   dr2xml_manages_enddate
      
      A smart workflow will allow you to extend a simulation during it course and to complement the output files accordingly, by managing the 'end date' part in filenames. You can then set next setting to False.
      
      values:
         
         - laboratory[dr2xml_manages_enddate]
         - True
      
      num type: 'string'
      
   end_year
      
      If you want to carry on the experiment beyond the duration set in DR, and that all requestItems that apply to DR end year also apply later on, set 'end_year' You can also set it if you don't know if DR has a wrong value
      
      values:
         
         - simulation[end_year]
         - False
      
      num type: 'string'
      
   excluded_dimensions
      
      List of dimensions to be excluded.
      
      values:
         
         - laboratory[excluded_dimensions]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_expgroups_lset
      
      List of the experiments groups that will be excluded from outputs from laboratory settings.
      
      values:
         
         - laboratory[excluded_expgroups]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_expgroups_sset
      
      List of the experiments groups that will be excluded from outputs from simulation settings.
      
      values:
         
         - simulation[excluded_expgroups]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_opportunities_lset
      
      List of the opportunities that will be excluded from outputs from laboratory settings.
      
      values:
         
         - laboratory[excluded_opportunities]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_opportunities_sset
      
      List of the opportunities that will be excluded from outputs from simulation settings.
      
      values:
         
         - simulation[excluded_opportunities]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_pairs_lset
      
      You can exclude some (variable, table) pairs from outputs. A list of tuple (variable, table) to be excluded from laboratory settings.
      
      values:
         
         - laboratory[excluded_pairs]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_pairs_sset
      
      You can exclude some (variable, table) pairs from outputs. A list of tuple (variable, table) to be excluded from simulation settings.
      
      values:
         
         - simulation[excluded_pairs]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_regions
      
      List of regions to be excluded.
      
      values:
         
         - laboratory[excluded_regions]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_request_links
      
      List of links un data request that should not been followed (those request are not taken into account).
      
      values:
         
         - laboratory[excluded_request_links]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_spshapes_lset
      
      The list of shapes that should be excluded (all variables in those shapes will be excluded from outputs).
      
      values:
         
         - laboratory[excluded_spshapes]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_tables_lset
      
      List of the tables that will be excluded from outputs from laboratory settings.
      
      values:
         
         - laboratory[excluded_tables]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_tables_sset
      
      List of the tables that will be excluded from outputs from simulation settings.
      
      values:
         
         - simulation[excluded_tables]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_tpshapes_lset
      
      The list of shapes that should be excluded (all variables in those shapes will be excluded from outputs).
      
      values:
         
         - laboratory[excluded_tpshapes]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_vargroups_lset
      
      List of the variables groups that will be excluded from outputs from laboratory settings.
      
      values:
         
         - laboratory[excluded_vargroups]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_vargroups_sset
      
      List of the variables groups that will be excluded from outputs from simulation settings.
      
      values:
         
         - simulation[excluded_vargroups]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_vars_lset
      
      List of CMOR variables to exclude from the result based on previous Data Request extraction from laboratory settings.
      
      values:
         
         - laboratory[excluded_vars]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_vars_per_config
      
      A dictionary which keys are configurations and values the list of variables that must be excluded for each configuration.
      
      values:
         
         - laboratory[excluded_vars_per_config][internal[configuration]]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   excluded_vars_per_frequency
      
      A dictionary which keys are frequencies and values the list of variables that must be excluded for each frequency.
      
      values:
         
         - laboratory[excluded_vars_per_frequency]
         - {}
      
      target type: 'dict'
      
      num type: 'string'
      
   excluded_vars_per_shape
      
      A dictionary which keys are shapes and values the list of variables that must be excluded for each shape.
      
      values:
         
         - laboratory[excluded_vars_per_shape]
         - {}
      
      target type: 'dict'
      
      num type: 'string'
      
   excluded_vars_sset
      
      List of CMOR variables to exclude from the result based on previous Data Request extraction from simulation settings.
      
      values:
         
         - simulation[excluded_vars]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   experiment_for_requests
      
      Experiment id to use for driving the use of the Data Request.
      
      fatal: True
      
      values:
         
         - simulation[experiment_for_requests]
         - internal[experiment_id]
      
      num type: 'string'
      
   experiment_id
      
      Root experiment identifier
      
      fatal: True
      
      values:
         
         - simulation[experiment_id]
      
      num type: 'string'
      
   extravar_regions
      
      Dictionnary containing the default values for region for each variables
      
      values:
         
         - laboratory[extravar_regions]
         -    
         -    - 'default': 'default'
      
      target type: 'dict'
      
      num type: 'string'
      
   filter_on_realization
      
      If you want to produce the same variables set for all members, set this parameter to False.
      
      values:
         
         - simulation[filter_on_realization]
         - laboratory[filter_on_realization]
         - True
      
      num type: 'string'
      
   fx_from_file
      
      You may provide some variables already horizontally remapped to some grid (i.e. Xios domain) in external files. The varname in file must match the referenced id in pingfile. Tested only for fixed fields. A dictionary with variable id as key and a dictionary as value: the key must be the grid id, the value a dictionary with the file for each resolution.
      
      values:
         
         - laboratory[fx_from_file]
         - []
      
      num type: 'string'
      
   grid_choice
      
      A dictionary which keys are models name and values the corresponding resolution.
      
      fatal: True
      
      values:
         
         - laboratory[grid_choice][internal[source_id]]
      
      num type: 'string'
      
   grid_policy
      
      The grid choice policy for output files.
      
      fatal: True
      
      values:
         
         - laboratory[grid_policy]
         - False
      
      num type: 'string'
      
   grid_prefix
      
      Prefix of the dr2xml generated grid named to be used.
      
      fatal: True
      
      values:
         
         - laboratory[grid_prefix]
         - internal[ping_variables_prefix]
      
      num type: 'string'
      
   grids
      
      Grids : per model resolution and per context :\n- CMIP6 qualifier (i.e. 'gn' or 'gr') for the main grid chosen (because you  may choose has main production grid a regular one, when the native grid is e.g. unstructured)\n- Xios id for the production grid (if it is not the native grid)\n- Xios id for the latitude axis used for zonal means (mist match latitudes for grid above)\n- resolution of the production grid (using CMIP6 conventions)\n- grid description
      
      fatal: True
      
      values:
         
         - function from functions_file named format_grids('grids'= laboratory[grids], 'variables_per_grid_type'= internal[variables_per_grid_type])
      
      num type: 'string'
      
   grids_default_DR
      
      DR default grids
      
      fatal: True
      
      values:
         
         - laboratory[grids_default_DR]
      
      num type: 'string'
      
   grids_dev
      
      Grids definition for dev variables.
      
      fatal: True
      
      values:
         
         - laboratory[grids_dev]
         - {}
      
      num type: 'string'
      
   grouped_vars_per_file
      
      Variables to be grouped in the same output file (provided additional conditions are filled).
      
      values:
         
         - simulation[grouped_vars_per_file]
         - laboratory[grouped_vars_per_file]
         - []
      
      num type: 'string'
      
   included_expgroups
      
      List of experiments groups that will be processed (all others will not).
      
      values:
         
         - simulation[included_expgroups]
         - internal[included_expgroups_lset]
      
      target type: 'list'
      
      num type: 'string'
      
   included_expgroups_lset
      
      List of experiments groups that will be processed (all others will not) from laboratory settings.
      
      values:
         
         - laboratory[included_expgroups]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   included_opportunities
      
      List of opportunities that will be processed (all others will not).
      
      values:
         
         - simulation[included_opportunities]
         - internal[included_opportunities_lset]
      
      target type: 'list'
      
      num type: 'string'
      
   included_opportunities_lset
      
      List of opportunities that will be processed (all others will not) from laboratory settings.
      
      values:
         
         - laboratory[included_opportunities]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   included_request_links
      
      List of the request links that will be processed (all others will not).
      
      values:
         
         - laboratory[included_request_links]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   included_tables
      
      List of tables that will be processed (all others will not).
      
      values:
         
         - simulation[included_tables]
         - internal[included_tables_lset]
      
      target type: 'list'
      
      num type: 'string'
      
   included_tables_lset
      
      List of tables that will be processed (all others will not) from laboratory settings.
      
      values:
         
         - laboratory[included_tables]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   included_vargroups
      
      List of variables groups that will be processed (all others will not).
      
      values:
         
         - simulation[included_vargroups]
         - internal[included_vargroups_lset]
      
      target type: 'list'
      
      num type: 'string'
      
   included_vargroups_lset
      
      List of variables groups that will be processed (all others will not) from laboratory settings.
      
      values:
         
         - laboratory[included_vargroups]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   included_vars
      
      Variables to be considered from the Data Request (all others will not)
      
      values:
         
         - simulation[included_vars]
         - internal[included_vars_lset]
      
      target type: 'list'
      
      num type: 'string'
      
   included_vars_lset
      
      Variables to be considered from the Data Request (all others will not) from laboratory settings.
      
      values:
         
         - laboratory[included_vars]
         - []
      
      target type: 'list'
      
      num type: 'string'
      
   listof_home_vars
      
      Full path to the file which contains the list of home variables to be taken into account, in addition to the Data Request.
      
      values:
         
         - simulation[listof_home_vars]
         - laboratory[listof_home_vars]
         - None
      
      num type: 'string'
      
   max_file_size_in_floats
      
      The maximum size of generated files in number of floating values.
      
      values:
         
         - laboratory[max_file_size_in_floats]
         - 500000000.0
      
      num type: 'string'
      
   max_priority
      
      Max variable priority level to be output (you may set 3 when creating ping_files while being more restrictive at run time).
      
      fatal: True
      
      values:
         
         - simulation[max_priority]
         - internal[max_priority_lset]
      
      num type: 'string'
      
   max_priority_lset
      
      Max variable priority level to be output (you may set 3 when creating ping_files while being more restrictive at run time) from lab settings.
      
      fatal: True
      
      values:
         
         - laboratory[max_priority]
      
      num type: 'string'
      
   max_priority_per_frequency
      
      Max variable priority level per frequency to be output from lab settings.
      
      fatal: True
      
      values:
         
         - simulation[max_priority_per_frequency]
         - laboratory[max_priority_per_frequency]
         - {}
      
      target type: 'dict'
      
      num type: 'string'
      
   max_split_freq
      
      The maximum number of years that should be putted in a single file.
      
      values:
         
         - simulation[max_split_freq]
         - laboratory[max_split_freq]
         - None
      
      num type: 'string'
      
   mips
      
      A dictionary in which keys are grid and values a set of strings corresponding to MIPs names.
      
      fatal: True
      
      values:
         
         - laboratory[mips]
      
      num type: 'string'
      
   nemo_sources_management_policy_master_of_the_world
      
      Set that to True if you use a context named 'nemo' and the corresponding model unduly sets a general freq_op AT THE FIELD_DEFINITION GROUP LEVEL. Due to Xios rules for inheritance, that behavior prevents inheriting specific freq_ops by reference from dr2xml generated field_definitions.
      
      fatal: True
      
      values:
         
         - laboratory[nemo_sources_management_policy_master_of_the_world]
         - False
      
      num type: 'string'
      
   non_standard_attributes
      
      You may add a series of NetCDF attributes in all files for this simulation.
      
      values:
         
         - laboratory[non_standard_attributes]
         - {}
      
      num type: 'string'
      
   non_standard_axes
      
      If your model has some axis which does not have all its attributes as in DR, and you want dr2xml to fix that it, give here the correspondence from model axis id to DR dim/grid id. For label dimensions you should provide the  list of labels, ordered as in your model, as second element of a pair. Label-type axes will be processed even if not quoted. Scalar dimensions are not concerned by this feature. A dictionary with (axis_id, axis_correct_id) or (axis_id, tuple of labels) as key, values.
      
      values:
         
         - laboratory[non_standard_axes]
         - {}
      
      num type: 'string'
      
   orography_field_name
      
      Name of the orography field name to be used to compute height over orog fields.
      
      values:
         
         - laboratory[orography_field_name]
         - 'orog'
      
      num type: 'string'
      
   orphan_variables
      
      A dictionary with (context name, list of variables) as (key,value) pairs, where the list indicates the variables to be re-affected to the key-context (initially affected to a realm falling in another context).
      
      fatal: True
      
      values:
         
         - laboratory[orphan_variables]
      
      num type: 'string'
      
   path_extra_tables
      
      Full path of the directory which contains extra tables.
      
      values:
         
         - simulation[path_extra_tables]
         - laboratory[path_extra_tables]
         - None
      
      num type: 'string'
      
   path_to_parse
      
      The path of the directory which, at run time, contains the root XML file (iodef.xml).
      
      values:
         
         - laboratory[path_to_parse]
         - './'
      
      num type: 'string'
      
   perso_sdims_description
      
      A dictionary containing, for each perso or dev variables with a XY-perso shape, and for each vertical coordinate associated, the main attributes of the dimension.
      
      values:
         
         - simulation[perso_sdims_description]
         - {}
      
      num type: 'string'
      
   ping_variables_prefix
      
      The tag used to prefix the variables in the ‘field id’ namespaces of the ping file; may be an empty string.
      
      fatal: True
      
      values:
         
         - laboratory[ping_variables_prefix]
      
      num type: 'string'
      
   prefixed_orography_field_name
      
      Name of the orography field name to be used to compute height over orog fields prefixed with :term:`ping_variable_prefix`.
      
      values:
         
         - function from self named format('prefix'= internal[ping_variables_prefix], 'variable'= internal[orography_field_name])
      
      num type: 'string'
      
   print_stats_per_var_label
      
      For an extended printout of selected CMOR variables, grouped by variable label.
      
      values:
         
         - laboratory[print_stats_per_var_label]
         - False
      
      num type: 'string'
      
   print_variables
      
      If the value is a list, only the file/field variables listed here will be put in output files. If boolean, tell if the file/field variables should be put in output files.
      
      values:
         
         - laboratory[print_variables]
         - True
      
      num type: 'string'
      
   realization_index
      
      Realization number.
      
      values:
         
         - simulation[realization_index]
         - '1'
      
      num type: 'string'
      
   realms_per_context
      
      A dictionary which keys are context names and values the lists of realms associated with each context.
      
      fatal: True
      
      values:
         
         - laboratory[realms_per_context][internal[context]]
      
      num type: 'string'
      
   required_model_components
      
      Dictionary which gives, for each model name, the components that must be present.
      
      fatal: True
      
      values:
         
         - laboratory[required_model_components][internal[source_id]]
         - []
      
      num type: 'string'
      
   sampling_timestep
      
      Basic sampling timestep set in your field definition (used to feed metadata 'interval_operation'). Should be a dictionary which keys are resolutions and values a context/timestep dictionary.
      
      fatal: True
      
      values:
         
         - laboratory[sampling_timestep]
         - 2
      
      num type: 'string'
      
   sectors
      
      List of the sectors to be considered.
      
      values:
         
         - laboratory[sectors]
      
      num type: 'string'
      
   select
      
      Selection strategy for variables.
      
      fatal: True
      
      values:
         
         - dict[select]
      
      corrections:
         
         - '': 'on_expt_and_year'
      
      authorized values:
         
         - 'on_expt_and_year'
         - 'on_expt'
         - 'on_inc_and_exc'
         - 'no'
      
      num type: 'string'
      
   select_excluded_dimensions
      
      Excluded dimensions for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[excluded_dimensions]
         -       
      
      target type: 'list'
      
      num type: 'string'
      
   select_excluded_expgroups
      
      Excluded experiments groups for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: merge_lists()
         -       
      
      num type: 'string'
      
   select_excluded_opportunities
      
      Excluded opportunities for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: merge_lists()
         -       
      
      num type: 'string'
      
   select_excluded_pairs
      
      Excluded pairs for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: merge_lists()
         -       
      
      num type: 'string'
      
   select_excluded_regions
      
      Excluded regions for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[excluded_regions]
         -       
      
      num type: 'string'
      
   select_excluded_request_links
      
      Excluded request links for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[excluded_request_links]
         -       
      
      num type: 'string'
      
   select_excluded_tables
      
      Excluded tables for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: merge_lists()
         -       
      
      num type: 'string'
      
   select_excluded_vargroups
      
      Excluded variables groups for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: merge_lists()
         -       
      
      num type: 'string'
      
   select_excluded_vars
      
      Excluded variables for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: merge_lists()
         -       
      
      num type: 'string'
      
   select_grid_choice
      
      Grid choice for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_expt]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[grid_choice]
         -       
      
      num type: 'string'
      
   select_included_expgroups
      
      Included experiments groups for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[included_expgroups]
         -       
      
      num type: 'string'
      
   select_included_opportunities
      
      Included opportunities for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[included_opportunities]
         -       
      
      num type: 'string'
      
   select_included_request_links
      
      Included request links for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[included_request_links]
         -       
      
      num type: 'string'
      
   select_included_tables
      
      Included tables for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[included_tables]
         -       
      
      num type: 'string'
      
   select_included_vargroups
      
      Included variable groups for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[included_vargroups]
         -       
      
      num type: 'string'
      
   select_included_vars
      
      Included variables for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[included_vars]
         -       
      
      num type: 'string'
      
   select_max_priority
      
      Max priority for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_expt]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[max_priority]
         -       
      
      num type: 'string'
      
   select_max_priority_per_frequency
      
      Max priority per frequency for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[max_priority_per_frequency]
         -       
      
      target type: 'dict'
      
      num type: 'string'
      
   select_mips
      
      MIPs for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_inc_and_exc]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: function from functions_file named sort_mips('mips'= internal[mips][internal[select_grid_choice]])
         -       
      
      num type: 'string'
      
   select_on_expt
      
      Should data be selected on experiment?
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values:
         -             
         -             - 'on_expt_and_year'
         -             - 'on_expt'
         -       
         -       values: True
         -       
      
      num type: 'string'
      
   select_on_inc_and_exc
      
      Should data be selected on inclusions and exclusions?
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values:
         -             
         -             - 'on_expt_and_year'
         -             - 'on_expt'
         -             - 'on_inc_and_exc'
         -       
         -       values: True
         -       
      
      num type: 'string'
      
   select_on_year
      
      Should data be selected on year?
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: 'on_expt_and_year'
         -       
         -       values: True
         -       
      
      num type: 'string'
      
   select_sizes
      
      Sizes for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_expt]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[sizes]
         -       
      
      target type: 'dict'
      
      num type: 'string'
      
   select_tierMax
      
      tierMax for variable selection.
      
      fatal: True
      
      values:
         
         -    Condition:
         -    
         -       value to check: internal[select_on_expt]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: True
         -       
         -       values: internal[tierMax]
         -       
      
      num type: 'string'
      
   simple_domain_grid_regexp
      
      If some grid is not defined in xml but by API, and is referenced by a field which is considered by the DR as having a singleton dimension, then: \n1) it must be a grid which has only a domain \n2) the domain name must be extractable from the grid_id using a regexp and a group number \nExample: using a pattern that returns full id except for a '_grid' suffix
      
      values:
         
         - laboratory[simple_domain_grid_regexp]
      
      num type: 'string'
      
   sizes
      
      A dictionary which keys are resolution and values the associated grid size for atmosphere and ocean grids. The grid size looks like : ['nho', 'nlo', 'nha', 'nla', 'nlas', 'nls', 'nh1']. Used to compute file split frequency.
      
      fatal: True
      
      values:
         
         - function from functions_file named format_sizes('sizes'= laboratory[sizes][internal[grid_choice]])
      
      num type: 'string'
      
   source_id
      
      Name of the model used.
      
      fatal: True
      
      values:
         
         - laboratory[configurations][internal[configuration]][0]
         - simulation[source_id]
      
      num type: 'string'
      
   source_type
      
      If the default source-type value for your source (:term:`source_types` from :term:`lab_and_model_settings`) does not fit, you may change it here. This should describe the model most directly responsible for the output. Sometimes it is appropriate to list two (or more) model types here, among AER, AGCM, AOGCM, BGC, CHEM, ISM, LAND, OGCM, RAD, SLAB e.g. amip , run with CNRM-CM6-1, should quote \"AGCM AER\". Also see note 14 of https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit
      
      fatal: True
      
      values:
         
         - laboratory[configurations][internal[configuration]][1]
         - simulation[source_type]
         - laboratory[source_types][internal[source_id]]
      
      num type: 'string'
      
   special_timestep_vars
      
      This variable is used when some variables are computed with a period which is not the basic timestep. A dictionary which keys are non standard timestep and values the list of variables which are computed at this timestep.
      
      values:
         
         - laboratory[special_timestep_vars]
         - []
      
      num type: 'string'
      
   split_frequencies
      
      Path to the split frequencies file to be used.
      
      values:
         
         - simulation[split_frequencies]
         - laboratory[split_frequencies]
         - 'splitfreqs.dat'
      
      num type: 'string'
      
   synchronisation_frequency
      
      Frequency at which the synchronisation between buffer and filesystem is done.
      
      values:
         
         - simulation[synchronisation_frequency]
         - laboratory[synchronisation_frequency]
         - None
      
      num type: 'string'
      
   tierMax
      
      Number indicating the maximum tier to consider for experiments.
      
      fatal: True
      
      values:
         
         - simulation[tierMax]
         - internal[tierMax_lset]
      
      num type: 'string'
      
   tierMax_lset
      
      Number indicating the maximum tier to consider for experiments from lab settings.
      
      fatal: True
      
      values:
         
         - laboratory[tierMax]
      
      num type: 'string'
      
   too_long_periods
      
      The CMIP6 frequencies that are unreachable for a single model run. Datafiles will be labelled with dates consistent with content (but not with CMIP6 requirements). Allowed values are only 'dec' and 'yr'.
      
      fatal: True
      
      values:
         
         - laboratory[too_long_periods]
         - []
      
      num type: 'string'
      
   update_grid_label
      
      Should grid label be updated according to table?
      
      values:
         
         - laboratory[update_grid_label]
         - True
      
      num type: 'string'
      
   useAtForInstant
      
      Should xml output files use the `@` symbol for definitions for instant variables?
      
      values:
         
         - laboratory[useAtForInstant]
         - False
      
      num type: 'string'
      
   use_cmorvar_label_in_filename
      
      CMIP6 rule is that filenames includes the variable label, and that this variable label is not the CMORvar label, but 'MIPvar' label. This may lead to conflicts, e.g. for 'ua' and 'ua7h' in table 6hPlevPt; allows to avoid that, if set to True.
      
      fatal: True
      
      values:
         
         - laboratory[use_cmorvar_label_in_filename]
         - False
      
      num type: 'string'
      
   use_union_zoom
      
      Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR.
      
      values:
         
         - laboratory[use_union_zoom]
         - False
      
      num type: 'string'
      
   variables_per_grid_type
      
      List of variables associated with a grid type
      
      values:
         
         - laboratory[variables_per_grid_type]
         - {}
      
      target type: 'dict'
      
      num type: 'string'
      
   vertical_interpolation_operation
      
      Operation done for vertical interpolation.
      
      values:
         
         - laboratory[vertical_interpolation_operation]
         - 'instant'
      
      num type: 'string'
      
   vertical_interpolation_sample_freq
      
      Time frequency of vertical interpolation.
      
      values:
         
         - laboratory[vertical_interpolation_sample_freq]
      
      num type: 'string'
      
   write_split_freq
      
      Should a split_freq file be generated with values computed by dr2xml?
      
      values:
         
         - laboratory[write_split_freq]
         - False
      
      forbidden values:
         
         - None
         - 'None'
         - ''
      
      num type: 'string'
      
   xios_version
      
      Version of XIOS used.
      
      values:
         
         - laboratory[xios_version]
         - 2
      
      num type: 'string'
      
   year
      
      Year associated with the launch of dr2xml.
      
      fatal: True
      
      values:
         
         - dict[year]
      
      num type: 'string'
      
   zg_field_name
      
      Name of the geopotential height field name to be used to compute height over orog fields.
      
      values:
         
         - laboratory[zg_field_name]
         - 'zg'
      
      num type: 'string'
      
Common values
-------------
.. glossary::
   :sorted:
   
   prefix
      
      Prefix to be used for each file definition.
      
      fatal: True
      
      values:
         
         - dict[prefix]
      
      num type: 'string'
      
Project settings
----------------
.. glossary::
   :sorted:
   
   axis
      
      XIOS axis beacon
   axis_definition
      
      XIOS axis_definition beacon
   axis_group
      
      XIOS axis_group beacon
   context
      
      XIOS context beacon
   domain
      
      XIOS domain beacon
   domain_definition
      
      XIOS domain_definition beacon
   domain_group
      
      XIOS domain_group beacon
   duplicate_scalar
      
      XIOS duplicate_scalar beacon
   field
      
      XIOS field beacon (except for output fields)
   field_definition
      
      XIOS field_definition beacon
   field_group
      
      XIOS field_group beacon
   field_output
      
      XIOS field beacon (only for output fields)
   file
      
      XIOS file beacon (except for output files)
   file_definition
      
      XIOS file_definition beacon
   file_output
      
      XIOS file beacon (only for output files)
   generate_rectilinear_domain
      
      XIOS generate_rectilinear_domain beacon
   grid
      
      XIOS grid beacon
   grid_definition
      
      XIOS grid_definition beacon
   interpolate_axis
      
      TODO
   interpolate_domain
      
      XIOS interpolate_domain beacon
   scalar
      
      XIOS scalar beacon
   scalar_definition
      
      XIOS scalar_definition beacon
   temporal_splitting
      
      XIOS temporal_splitting beacon
   variable
      
      XIOS variable beacon
      
      Attributes:
         name
            
            Content of the variable
            
            fatal: True
            
            values:
               
               - attrs[name]
            
            num type: 'string'
            
         type
            
            Encoding type of the variable's content.
            
            fatal: True
            
            values:
               
               - attrs[type]
            
            num type: 'string'
            
   zoom_axis
      
      XIOS zoom_axis beacon