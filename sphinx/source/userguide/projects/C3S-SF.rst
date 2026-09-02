Parameters available for project C3S-SF
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
         -    
         -    - 'cfsites': 
         -    
         -          
         -          - 'gn'
         -          - '100 km'
         -          - 'data sampled in model native grid by nearest neighbour method '
         -    - '1deg': 
         -    
         -          
         -          - 'gr1'
         -          - '1x1 degree'
         -          - 'data regridded to a CMIP6 standard 1x1 degree latxlon grid from the native grid'
         -    - '2deg': 
         -    
         -          
         -          - 'gr2'
         -          - '2x2 degree'
         -          - 'data regridded to a CMIP6 standard 2x2 degree latxlon grid from the native grid'
         -    - '100km': 
         -    
         -          
         -          - 'gr3'
         -          - '100 km'
         -          - 'data regridded to a CMIP6 standard 100 km resol grid from the native grid'
         -    - '50km': 
         -    
         -          
         -          - 'gr4'
         -          - '50 km'
         -          - 'data regridded to a CMIP6 standard 50 km resol grid from the native grid'
         -    - '25km': 
         -    
         -          
         -          - 'gr5'
         -          - '25 km'
         -          - 'data regridded to a CMIP6 standard 25 km resol grid from the native grid'
         -    - 'default': 
         -    
         -          
         -          - 'grx'
         -          - '?x? degree'
         -          - 'grid has no description - please fix DR_grid_to_grid_atts for grid %s'
      
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
   
   HDL
      
      HDL associated with the project.
      
      values:
         
         - simulation[HDL]
         - laboratory[HDL]
      
      num type: 'string'
      
   activity_id
      
      MIP(s) name(s).
      
      values:
         
         - simulation[activity_id]
         - laboratory[activity_id]
      
      num type: 'string'
      
   branch_method
      
      Branching procedure.
      
      values:
         
         - simulation[branch_method]
         - 'standard'
      
      forbidden values:
         
         - None
         - 'None'
         - ''
      
      num type: 'string'
      
   branch_month_in_parent
      
      Branch month in parent simulation with respect to its time axis.
      
      values:
         
         - simulation[branch_month_in_parent]
         - '1'
      
      num type: 'string'
      
   branch_year_in_parent
      
      Branch year in parent simulation with respect to its time axis.
      
      values:
         
         -    Condition:
         -    
         -       value to check: simulation[branch_year_in_parent]
         -       
         -       check to perform: 'eq'
         -       
         -       reference values: internal[branching][internal[experiment_id]][1]
         -       
         -       values: simulation[branch_year_in_parent]
         -       
         -    Condition:
         -    
         -       value to check: internal[experiment_id]
         -       
         -       check to perform: 'neq'
         -       
         -       reference values: internal[branching]
         -       
         -       values: simulation[branch_year_in_parent]
         -       
      
      forbidden values:
         
         - None
         - 'None'
         - ''
         - 'N/A'
      
      num type: 'string'
      
   comment_lset
      
      A character string containing additional information about the models from laboratory settings. Will be complemented with the experiment's specific comment string.
      
      values:
         
         - laboratory[comment]
         - ''
      
      num type: 'string'
      
   comment_sset
      
      A character string containing additional information about the models from simulation settings. Will be complemented with the experiment's specific comment string.
      
      values:
         
         - simulation[comment]
         - ''
      
      num type: 'string'
      
   commit
      
      Id of the commits associated with the model.
      
      values:
         
         - simulation[commit]
         - laboratory[commit]
      
      num type: 'string'
      
   compression_level
      
      The compression level to be applied to NetCDF output files."
      
      values:
         
         - laboratory[compression_level]
         - '0'
      
      num type: 'string'
      
   contact
      
      Email address of the data producer.
      
      values:
         
         - simulation[contact]
         - laboratory[contact]
         - 'None'
      
      num type: 'string'
      
   convention_str
      
      Version of the conventions used.
      
      values:
         
         - laboratory[convention_str]
      
      num type: 'string'
      
   data_request_version_string
      
      Version of the data request used.
      
      fatal: True
      
      values:
         
         - function from data_request named get_version({})
      
      num type: 'string'
      
   data_specs_version
      
      Version of the data request used.
      
      fatal: True
      
      values:
         
         - common[data_request_version_string]
      
      num type: 'string'
      
   date_range
      
      Date range format to be used in file definition names.
      
      values:
         
         - '%start_date%-%end_date%'
      
      num type: 'string'
      
   description
      
      Description of the simulation.
      
      values:
         
         - laboratory[description]
         - simulation[description]
      
      num type: 'string'
      
   dr2xml_version
      
      Version of dr2xml used.
      
      values:
         
         - config.version
      
      num type: 'string'
      
   experiment
      
      Name of the experiment.
      
      values:
         
         - simulation[experiment]
      
      num type: 'string'
      
   expid_in_filename
      
      Experiment label to use in file names and attribute.
      
      values:
         
         - simulation[expid_in_filename]
         - internal[experiment_id]
      
      forbidden patterns: '.*_.*'
      
      num type: 'string'
      
   forcing_index
      
      Index for variant of forcing.
      
      values:
         
         - simulation[forcing_index]
         - '1'
      
      num type: 'string'
      
   forecast_reference_time
      
      Reference time for the forecast done in the simulation.
      
      values:
         
         - simulation[forecast_reference_time]
      
      num type: 'string'
      
   forecast_type
      
      Type of forecast done.
      
      values:
         
         - simulation[forecast_type]
      
      num type: 'string'
      
   grid_mapping
      
      Grid mapping name.
      
      values:
         
         - simulation[grid_mapping]
      
      num type: 'string'
      
   history
      
      In case of replacement of previously produced data, description of any changes in the production chain.
      
      values:
         
         - simulation[history]
         - 'none'
      
      num type: 'string'
      
   info_url
      
      Location of documentation.
      
      values:
         
         - laboratory[info_url]
      
      num type: 'string'
      
   initialization_index
      
      Index for variant of initialization method.
      
      values:
         
         - simulation[initialization_index]
         - '1'
      
      num type: 'string'
      
   institution
      
      Full name of the institution of the data producer.
      
      values:
         
         - laboratory[institution]
      
      num type: 'string'
      
   keywords
      
      Keywords associated with the simulation.
      
      values:
         
         - simulation[keywords] formatted with function from self named join({})
         - laboratory[keywords] formatted with function from self named join({})
      
      num type: 'string'
      
   list_perso_dev_file
      
      Name of the file which will contain the list of the patterns of perso and dev output file definition.
      
      values:
         
         - 'dr2xml_list_perso_and_dev_file_names'
      
      num type: 'string'
      
   mip_era
      
      MIP associated with the simulation.
      
      values:
         
         - common[mip_era_sset]
         - common[mip_era_lset]
      
      forbidden values: None
      
      num type: 'string'
      
   mip_era_lset
      
      MIP associated with the simulation from laboratory settings.
      
      values:
         
         - laboratory[mip_era]
         - None
      
      num type: 'string'
      
   mip_era_sset
      
      MIP associated with the simulation from simulation settings.
      
      values:
         
         - simulation[mip_era]
         - None
      
      num type: 'string'
      
   output_level
      
      We can control the max output level set for all output files.
      
      values:
         
         - laboratory[output_level]
         - '10'
      
      num type: 'string'
      
   parent_activity_id
      
      Description of sub-experiment.
      
      values:
         
         - simulation[parent_activity_id]
         - simulation[activity_id]
         - laboratory[parent_activity_id]
         - laboratory[activity_id]
      
      num type: 'string'
      
   parent_experiment_id
      
      Parent experiment identifier.
      
      values:
         
         - simulation[parent_experiment_id]
         - laboratory[parent_experiment_id]
      
      num type: 'string'
      
   parent_mip_era
      
      Parent’s associated MIP cycle.
      
      values:
         
         - simulation[parent_mip_era]
      
      num type: 'string'
      
   parent_source_id
      
      Parent model identifier.
      
      values:
         
         - simulation[parent_source_id]
      
      num type: 'string'
      
   parent_time_ref_year
      
      Reference year in parent simulation.
      
      values:
         
         - simulation[parent_time_ref_year]
         - '1850'
      
      num type: 'string'
      
   parent_time_units
      
      Time units used in parent.
      
      values:
         
         - simulation[parent_time_units]
      
      num type: 'string'
      
   parent_variant_label
      
      Parent variant label.
      
      values:
         
         - simulation[parent_variant_label]
      
      num type: 'string'
      
   physics_index
      
      Index for model physics variant.
      
      values:
         
         - simulation[physics_index]
         - '1'
      
      num type: 'string'
      
   prefix
      
      Prefix to be used for each file definition.
      
      fatal: True
      
      values:
         
         - dict[prefix]
      
      num type: 'string'
      
   references
      
      References associated with the simulation.
      
      values:
         
         - laboratory[references]
      
      num type: 'string'
      
   source
      
      Name of the model.
      
      values:
         
         - laboratory[source]
      
      num type: 'string'
      
   sub_experiment
      
      Sub-experiment name.
      
      values:
         
         - simulation[sub_experiment]
         - 'none'
      
      num type: 'string'
      
   sub_experiment_id
      
      Sub-experiment identifier.
      
      values:
         
         - simulation[sub_experiment_id]
         - 'none'
      
      num type: 'string'
      
   summary
      
      Short explanation about the simulation.
      
      values:
         
         - simulation[summary]
         - laboratory[summary]
      
      num type: 'string'
      
   variant_info
      
      It is recommended that some description be included to help identify major differences among variants, but care should be taken to record correct information.  dr2xml will add in all cases: 'Information provided by this attribute may in some cases be flawed. Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute.'
      
      values:
         
         - simulation[variant_info]
      
      forbidden values: ''
      
      num type: 'string'
      
Project settings
----------------
.. glossary::
   :sorted:
   
   axis
      
      XIOS axis beacon
      
      Attributes:
         id
            
            Id of the axis.
            
            values:
               
               - attrs[id]
            
            num type: 'string'
            
         positive
            
            How is the axis oriented?
            
            values:
               
               - attrs[positive]
            
            num type: 'string'
            
         n_glo
            
            Number of values of this axis.
            
            values:
               
               - attrs[n_glo]
            
            num type: 'string'
            
         value
            
            Value of the axis.
            
            values:
               
               - attrs[value]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         axis_ref
            
            Reference axis.
            
            values:
               
               - attrs[axis_ref]
            
            num type: 'string'
            
         name
            
            Name of this axis.
            
            values:
               
               - attrs[name]
            
            num type: 'string'
            
         standard_name
            
            Standard name of the axis.
            
            values:
               
               - attrs[standard_name]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         long_name
            
            Long name of this axis.
            
            values:
               
               - attrs[long_name]
            
            num type: 'string'
            
         prec
            
            Precision of the axis.
            
            values:
               
               - attrs[prec]
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         unit
            
            Unit of the axis.
            
            values:
               
               - attrs[unit]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         value
            
            Value of the axis.
            
            values:
               
               - attrs[value]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         bounds
            
            Bounds of the axis.
            
            values:
               
               - attrs[bounds]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         dim_name
            
            Name dimension of the axis.
            
            values:
               
               - attrs[dim_name]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         label
            
            Label of the axis.
            
            values:
               
               - attrs[label]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         axis_type
            
            Axis type.
            
            values:
               
               - attrs[axis_type]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
   axis_definition
      
      XIOS axis_definition beacon
   axis_group
      
      XIOS axis_group beacon
      
      Attributes:
         prec
            
            Precision associated with the axis group.
            
            values:
               
               - attrs[prec]
               - '8'
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            num type: 'string'
            
   context
      
      XIOS context beacon
      
      Comments:
         DR_version
            
            Version of the Data Request used
            
            values:
               
               - function from self named format('data_request_used'= init[data_request_used], 'data_request_version_string'= common[data_request_version_string])
            
            num type: 'string'
            
         dr2xml_version
            
            Version of dr2xml used
            
            values:
               
               - function from self named format('dr2xml_version'= common[dr2xml_version])
            
            num type: 'string'
            
         lab_settings
            
            Laboratory settings used
            
            values:
               
               - function from self named format('laboratory'= laboratory)
            
            num type: 'string'
            
         simulation_settings
            
            Simulation_settings used
            
            values:
               
               - function from self named format('laboratory'= simulation)
            
            num type: 'string'
            
         year
            
            Year used for the dr2xml's launch
            
            values:
               
               - function from self named format('year'= internal[year])
            
            num type: 'string'
            
      
      Attributes:
         id
            
            Id of the context
            
            values:
               
               - internal[context]
            
            num type: 'string'
            
   domain
      
      XIOS domain beacon
      
      Attributes:
         id
            
            Id of the domain.
            
            values:
               
               - attrs[id]
            
            num type: 'string'
            
         ni_glo
            
            Number of point in i dimension.
            
            values:
               
               - attrs[ni_glo]
            
            num type: 'string'
            
         nj_glo
            
            Number of points in j dimension.
            
            values:
               
               - attrs[nj_glo]
            
            num type: 'string'
            
         type
            
            Type of the domain.
            
            values:
               
               - attrs[type]
            
            num type: 'string'
            
         prec
            
            Precision of the domain.
            
            values:
               
               - attrs[prec]
            
            num type: 'string'
            
         lat_name
            
            Latitude axis name.
            
            values:
               
               - attrs[lat_name]
            
            num type: 'string'
            
         lon_name
            
            Longitude axis name.
            
            values:
               
               - attrs[lon_name]
            
            num type: 'string'
            
         dim_i_name
            
            Name of the i dimension.
            
            values:
               
               - attrs[dim_i_name]
            
            num type: 'string'
            
         domain_ref
            
            Reference domain.
            
            values:
               
               - attrs[domain_ref]
            
            num type: 'string'
            
   domain_definition
      
      XIOS domain_definition beacon
   domain_group
      
      XIOS domain_group beacon
      
      Attributes:
         prec
            
            Precision associated with the domain group.
            
            values:
               
               - attrs[prec]
               - '8'
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            num type: 'string'
            
   duplicate_scalar
      
      XIOS duplicate_scalar beacon
   field
      
      XIOS field beacon (except for output fields)
      
      Attributes:
         id
            
            Id of the field.
            
            values:
               
               - attrs[id]
            
            num type: 'string'
            
         field_ref
            
            Id of the reference field.
            
            values:
               
               - attrs[field_ref]
            
            num type: 'string'
            
         name
            
            Name of the field.
            
            values:
               
               - attrs[name]
            
            num type: 'string'
            
         freq_op
            
            Frequency of the operation done on the field.
            
            values:
               
               - attrs[freq_op]
            
            num type: 'string'
            
         freq_offset
            
            Offset to be applied on operations on the field.
            
            values:
               
               - attrs[freq_offset]
            
            num type: 'string'
            
         grid_ref
            
            Reference grid of the field.
            
            values:
               
               - attrs[grid_ref]
            
            num type: 'string'
            
         long_name
            
            Long name of the field.
            
            values:
               
               - attrs[long_name]
            
            num type: 'string'
            
         standard_name
            
            Standard name of the field.
            
            values:
               
               - attrs[standard_name]
            
            num type: 'string'
            
         unit
            
            Unit of the field.
            
            values:
               
               - attrs[unit]
            
            num type: 'string'
            
         operation
            
            Operation done on the field.
            
            values:
               
               - attrs[operation]
            
            num type: 'string'
            
         detect_missing_value
            
            Should missing values of the field be detected by XIOS.
            
            values:
               
               - attrs[detect_missing_value]
            
            num type: 'string'
            
         prec
            
            Precision of the field.
            
            values:
               
               - attrs[prec]
            
            num type: 'string'
            
   field_definition
      
      XIOS field_definition beacon
   field_group
      
      XIOS field_group beacon
      
      Attributes:
         freq_op
            
            Frequency of the operation done on the field.
            
            values:
               
               - attrs[freq_op]
            
            num type: 'string'
            
         freq_offset
            
            Offset to be applied on operations on the field.
            
            values:
               
               - attrs[freq_offset]
            
            num type: 'string'
            
   field_output
      
      XIOS field beacon (only for output fields)
      
      Common:
         variable
            
            Variable information
            
            fatal: True
            
            values:
               
               - variable
            
            num type: 'string'
            
         variable_label
            
            Variable label
            
            fatal: True
            
            values:
               
               - common_tag[variable][label]
            
            target type: 'str'
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
      
      Attributes:
         field_ref
            
            Reference field.
            
            values:
               
               - attrs[field_ref]
            
            num type: 'string'
            
         name
            
            Name of the field.
            
            values:
               
               - attrs[name]
               - common_tag[variable][mipVarLabel]
            
            num type: 'string'
            
         grid_ref
            
            Reference grid of the field.
            
            values:
               
               - attrs[grid_ref]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         freq_offset
            
            Offset to be applied on operations on the field.
            
            values:
               
               - attrs[freq_offset]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         detect_missing_value
            
            Should missing values of the field be detected by XIOS.
            
            values:
               
               - attrs[detect_missing_value]
               - 'True'
            
            num type: 'string'
            
         default_value
            
            Default value associated with the field.
            
            fatal: True
            
            values:
               
               - attrs[default_value]
               - attrs[prec]
               - common_tag[variable][prec]
            
            corrections:
               
               - '': '1.e+20'
               - 'float': '1.e+20'
               - 'real': '1.e+20'
               - 'double': '1.e+20'
               - 'integer': '0'
               - 'int': '0'
            
            authorized values:
               
               - '0'
               - '1.e+20'
            
            num type: 'string'
            
         prec
            
            Precision of the field.
            
            fatal: True
            
            values:
               
               - attrs[prec]
               - common_tag[variable][prec]
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            num type: 'string'
            
         cell_methods
            
            Cell method associated with the field.
            
            values:
               
               - attrs[cell_methods]
               - common_tag[variable][cell_methods]
            
            num type: 'string'
            
         cell_methods_mode
            
            Mode associated with the cell method of the field.
            
            values:
               
               - attrs[cell_methods_mode]
               - 'overwrite'
            
            num type: 'string'
            
         operation
            
            Operation performed on the field.
            
            values:
               
               - attrs[operation]
            
            num type: 'string'
            
         freq_op
            
            Frequency of the operation done on the field.
            
            values:
               
               - attrs[freq_op]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         expr
            
            Expression used to compute the field.
            
            values:
               
               - attrs[expr]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
      
      Variables
         standard_name
            
            Standard name of the field.
            
            values:
               
               - attrs[standard_name]
               - common_tag[variable][stdname]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         long_name
            
            Long name of the field.
            
            values:
               
               - attrs[long_name]
               - common_tag[variable][long_name]
            
            num type: 'string'
            
         coordinates
            
            Coordinates of the output field.
            
            values:
               
               - attrs[coordinates]
               - variable.coordinates
            
            num type: 'string'
            
         grid_mapping
            
            Grid mapping associated with the file.
            
            values:
               
               - attrs[grid_mapping]
               - common[grid_mapping]
            
            num type: 'string'
            
         units
            
            Units associated with the field.
            
            values:
               
               - attrs[units]
               - common_tag[variable][units]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
   file
      
      XIOS file beacon (except for output files)
      
      Attributes:
         id
            
            Id of the file.
            
            values:
               
               - attrs[id]
            
            num type: 'string'
            
         name
            
            File name.
            
            values:
               
               - attrs[name]
            
            num type: 'string'
            
         mode
            
            Mode in which the file will be open.
            
            values:
               
               - attrs[mode]
            
            num type: 'string'
            
         output_freq
            
            Frequency of the outputs contained in the file.
            
            values:
               
               - attrs[output_freq]
            
            num type: 'string'
            
         enabled
            
            Should the file be considered by XIOS.
            
            values:
               
               - attrs[enabled]
            
            num type: 'string'
            
   file_definition
      
      XIOS file_definition beacon
      
      Attributes:
         type
            
            Type of file to be produced
            
            values:
               
               - attrs[type]
               - 'one_file'
            
            num type: 'string'
            
         enabled
            
            Should the file_definition be considered by XIOS
            
            values:
               
               - attrs[enabled]
               - 'true'
            
            num type: 'string'
            
   file_output
      
      XIOS file beacon (only for output files)
      
      Common:
         variable
            
            Variable information
            
            fatal: True
            
            values:
               
               - attrs[variable][0]
            
            num type: 'string'
            
         variable_label
            
            Variable label
            
            fatal: True
            
            values:
               
               - common_tag[variable][label]
            
            target type: 'str'
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
      
      Attributes:
         id
            
            Id of the output file
            
            fatal: True
            
            values:
               
               - attrs[id]
               - function from self named format('grid'= attrs[grid_label], 'table'= attrs[table_id], 'variable'= common_tag[variable_label])
            
            num type: 'string'
            
         name
            
            File name.
            
            fatal: True
            
            values:
               
               - function from functions_file named build_filename('frequency'= function from functions_file named convert_frequency('freq'= variable.frequency), 'expid_in_filename'= common[expid_in_filename], 'date_range'= common[date_range], 'list_perso_dev_file'= common[list_perso_dev_file], 'var_type'= variable.type, 'label'= variable.label, 'realm'= function from functions_file named convert_realm('realm'= variable.modeling_realm))
            
            num type: 'string'
            
         output_freq
            
            Frequency of the outputs contained in the file.
            
            values:
               
               - attrs[output_freq]
            
            num type: 'string'
            
         append
            
            Should the data be append to the file?
            
            values:
               
               - attrs[append]
               - 'true'
            
            num type: 'string'
            
         output_level
            
            Output level of the file.
            
            values:
               
               - attrs[output_level]
               - common[output_level]
            
            forbidden values:
               
               - 'None'
               - ''
               - None
               - 'undef'
            
            num type: 'string'
            
         compression_level
            
            Compression level of the file.
            
            values:
               
               - attrs[compression_level]
               - common[compression_level]
            
            forbidden values:
               
               - 'None'
               - ''
               - None
               - 'undef'
            
            num type: 'string'
            
         split_freq
            
            Splitting frequency of the file.
            
            values:
               
               -    Condition:
               -    
               -       value to check: common_tag[variable][frequency]
               -       
               -       check to perform: 'nmatch'
               -       
               -       reference values: '.*fx.*'
               -       
               -       values: attrs[split_freq]
               -       
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         split_freq_format
            
            Splitting frequency format of the file.
            
            values:
               
               -    Condition:
               -    
               -       value to check: common_tag[variable][frequency]
               -       
               -       check to perform: 'nmatch'
               -       
               -       reference values: '.*fx.*'
               -       
               -       values: attrs[split_freq_format]
               -       
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         split_start_offset
            
            Splitting start offset of the file
            
            values:
               
               -    Condition:
               -    
               -       value to check: common_tag[variable][frequency]
               -       
               -       check to perform: 'nmatch'
               -       
               -       reference values: '.*fx.*'
               -       
               -       values: attrs[split_start_offset]
               -       
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'False'
               - False
               - 'undef'
            
            num type: 'string'
            
         split_end_offset
            
            Splitting end offset of the file
            
            values:
               
               -    Condition:
               -    
               -       value to check: common_tag[variable][frequency]
               -       
               -       check to perform: 'nmatch'
               -       
               -       reference values: '.*fx.*'
               -       
               -       values: attrs[split_end_offset]
               -       
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'False'
               - False
               - 'undef'
            
            num type: 'string'
            
         split_last_date
            
            Splitting last date of the file
            
            values:
               
               -    Condition:
               -    
               -       value to check: common_tag[variable][frequency]
               -       
               -       check to perform: 'nmatch'
               -       
               -       reference values: '.*fx.*'
               -       
               -       values: attrs[split_last_date]
               -       
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         time_units
            
            Time units of the file.
            
            values:
               
               - attrs[ time_units]
               - 'days'
            
            num type: 'string'
            
         time_counter_name
            
            Time counter name.
            
            values:
               
               - attrs[time_counter_name]
               - 'time'
            
            num type: 'string'
            
         time_counter
            
            Time counter type.
            
            values:
               
               - attrs[time_counter]
               - 'exclusive'
            
            num type: 'string'
            
         time_stamp_name
            
            Time stamp name.
            
            values:
               
               - attrs[time_stamp_name]
               - 'creation_date'
            
            num type: 'string'
            
         time_stamp_format
            
            Time stamp format.
            
            values:
               
               - attrs[time_stamp_format]
               - '%Y-%m-%dT%H:%M:%SZ'
            
            num type: 'string'
            
         uuid_name
            
            Unique identifier of the file name.
            
            values:
               
               - attrs[uuid_name]
               - 'uuid'
            
            num type: 'string'
            
         uuid_format
            
            Unique identifier of the file format.
            
            values:
               
               - attrs[uuid_format]
               - '%uuid%'
            
            forbidden values:
               
               - 'None'
               - ''
               - None
               - 'undef'
            
            num type: 'string'
            
         convention_str
            
            Convention used for the file.
            
            values:
               
               - attrs[convention_str]
               - common[convention_str]
            
            num type: 'string'
            
         synchronisation_frequency
            
            Frequency at which the synchronisation between buffer and filesystem is done.
            
            values:
               
               - attrs[synchronisation_frequency]
               - internal[synchronisation_frequency]
            
            forbidden values:
               
               - 'None'
               - ''
               - None
               - 'undef'
            
            num type: 'string'
            
      
      Variables
         description
            
            Description of the file.
            
            values:
               
               -    Condition:
               -    
               -       value to check: internal[experiment_id]
               -       
               -       check to perform: 'eq'
               -       
               -       reference values: common[expid_in_filename]
               -       
               -       values:
               -             
               -             - attrs[description]
               -             - common[description]
               -       
            
            forbidden values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         title
            
            Title of the file.
            
            values:
               
               - attrs[title]
               - function from self named format('activity_id'= common[activity_id] formatted with function from self named join({}), 'expid_in_filename'= simulation[expid_in_filename], 'project'= init[project], 'source_id'= internal[source_id])
               - function from self named format('activity_id'= common[activity_id] formatted with function from self named join({}), 'experiment_id'= simulation[experiment_id], 'project'= init[project], 'source_id'= internal[source_id])
            
            num type: 'string'
            
         source
            
            Model associated with the simulation.
            
            values:
               
               - attrs[source]
               - common[source]
            
            num type: 'string'
            
         institution_id
            
            Institution id associated with the simulation.
            
            output key: 'institute_id'
            
            fatal: True
            
            values:
               
               - attrs[institution_id]
               - init[institution_id]
            
            num type: 'string'
            
         institution
            
            Institution associated with the simulation.
            
            fatal: True
            
            values:
               
               - attrs[institution]
               - common[institution]
            
            num type: 'string'
            
         contact
            
            Contact email.
            
            values:
               
               - attrs[contact]
               - common[contact]
            
            forbidden values:
               
               - 'None'
               - ''
               - None
            
            num type: 'string'
            
         project
            
            Project associated with the file.
            
            values:
               
               - attrs[project]
            
            num type: 'string'
            
         comment
            
            Comment associated with the file.
            
            values:
               
               - attrs[comment]
               - function from self named format('var'= ,    ,          Condition:,          ,             value to check: common_tag[variable][comments],             ,             check to perform: 'neq',             ,             reference values:,                   ,                   - 'None',                   - None,             ,             values: common_tag[variable][comments],             , 'lset'= ,    ,          Condition:,          ,             value to check: common[comment_lset],             ,             check to perform: 'neq',             ,             reference values:,                   ,                   - 'None',                   - None,             ,             values: common[comment_lset],             , 'sset'= ,    ,          Condition:,          ,             value to check: common[comment_sset],             ,             check to perform: 'neq',             ,             reference values:,                   ,                   - 'None',                   - None,             ,             values: common[comment_sset],             )
            
            forbidden values: ''
            
            num type: 'string'
            
         forecast_type
            
            Forecast type associated with the file.
            
            values:
               
               - attrs[forecast_type]
               - common[forecast_type]
            
            num type: 'string'
            
         realm
            
            Realm associated with the file.
            
            output key: 'modeling_realm'
            
            values:
               
               - function from functions_file named convert_realm('realm'= attrs[realm])
               - function from functions_file named convert_realm('realm'= variable.modeling_realm)
            
            num type: 'string'
            
         frequency
            
            Frequency associated with the file.
            
            values:
               
               - attrs[frequency]
               - common_tag[variable][frequency]
            
            num type: 'string'
            
         level_type
            
            Level type associated with the file.
            
            values:
               
               - attrs[level_type]
               - variable.level_type
            
            num type: 'string'
            
         history
            
            History associated with the file.
            
            values:
               
               - attrs[history]
               - common[history]
            
            num type: 'string'
            
         references
            
            References associated with the simulation.
            
            values:
               
               - attrs[references]
               - common[references]
            
            num type: 'string'
            
         commit
            
            Commit associated with the file.
            
            values:
               
               - attrs[commit]
               - common[commit]
            
            num type: 'string'
            
         summary
            
            Summary associated with the file.
            
            values:
               
               - attrs[summary]
               - common[summary]
            
            num type: 'string'
            
         keywords
            
            Keywords associated with the file.
            
            values:
               
               - attrs[keywords]
            
            num type: 'string'
            
         forecast_reference_time
            
            Forecast reference time associated with the file.
            
            values:
               
               - attrs[forecast_reference_time]
               - common[forecast_reference_time]
            
            num type: 'string'
            
   generate_rectilinear_domain
      
      XIOS generate_rectilinear_domain beacon
   grid
      
      XIOS grid beacon
      
      Attributes:
         id
            
            Id of the grid.
            
            values:
               
               - attrs[id]
            
            num type: 'string'
            
   grid_definition
      
      XIOS grid_definition beacon
   interpolate_axis
      
      TODO
      
      Attributes:
         type
            
            Type of the interpolated axis.
            
            values:
               
               - attrs[type]
            
            num type: 'string'
            
         order
            
            Order of the interpolated axis.
            
            values:
               
               - attrs[order]
            
            num type: 'string'
            
         coordinate
            
            Coordinate of the interpolated axis.
            
            values:
               
               - attrs[coordinate]
            
            num type: 'string'
            
   interpolate_domain
      
      XIOS interpolate_domain beacon
      
      Attributes:
         type
            
            Type of the interpolated domain.
            
            values:
               
               - attrs[type]
            
            num type: 'string'
            
         order
            
            Order of the interpolation.
            
            values:
               
               - attrs[order]
            
            num type: 'string'
            
         renormalize
            
            Should the interpolated domain be renormalized?
            
            values:
               
               - attrs[renormalize]
            
            num type: 'string'
            
         mode
            
            Mode used for the interpolation.
            
            values:
               
               - attrs[mode]
            
            num type: 'string'
            
         write_weight
            
            Should interpolation weights be written?
            
            values:
               
               - attrs[write_weight]
            
            num type: 'string'
            
         coordinate
            
            Coordinate of the interpolated domain.
            
            values:
               
               - attrs[coordinate]
            
            num type: 'string'
            
   scalar
      
      XIOS scalar beacon
      
      Attributes:
         id
            
            Id of the scalar.
            
            values:
               
               - attrs[id]
            
            num type: 'string'
            
         scalar_ref
            
            Reference scalar.
            
            values:
               
               - attrs[scalar_ref]
            
            num type: 'string'
            
         name
            
            Name of the scalar.
            
            values:
               
               - attrs[name]
            
            num type: 'string'
            
         standard_name
            
            Standard name of the scalar.
            
            values:
               
               - attrs[standard_name]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         long_name
            
            Long name of the scalar.
            
            values:
               
               - attrs[long_name]
            
            num type: 'string'
            
         label
            
            Label of the scalar.
            
            values:
               
               - attrs[label]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         prec
            
            Precision of the scalar.
            
            values:
               
               - attrs[prec]
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         value
            
            Value of the scalar.
            
            values:
               
               - attrs[value]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         bounds
            
            Bounds of the scalar.
            
            values:
               
               - attrs[bounds]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         bounds_name
            
            Bounds name of the scalar.
            
            values:
               
               - attrs[bounds_name]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         axis_type
            
            Axis type of the scalar.
            
            values:
               
               - attrs[axis_type]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         positive
            
            Orientation of the scalar.
            
            values:
               
               - attrs[positive]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
         unit
            
            Unit of the scalar.
            
            values:
               
               - attrs[unit]
            
            forbidden values:
               
               - ''
               - 'None'
               - None
               - 'undef'
            
            num type: 'string'
            
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
      
      Attributes:
         index
            
            Index of the zoomed axis.
            
            values:
               
               - attrs[index]
            
            num type: 'string'
            