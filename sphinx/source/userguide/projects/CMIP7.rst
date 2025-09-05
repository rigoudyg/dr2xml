Parameters available for project CMIP7
======================================

Unsorted parameters
-------------------
   Internal values
   ^^^^^^^^^^^^^^^
   .. glossary::
      :sorted:
      
      CFsubhr_frequency
         
         CFMIP has an elaborated requirement for defining subhr frequency; by default, dr2xml uses 1 time step.
         
         fatal: False
         
         default values:
            
            - laboratory[CFsubhr_frequency]
            - '1ts'
         
         num type: 'string'
         
      CV_experiment
         
         Controlled vocabulary file containing experiment characteristics.
         
         fatal: False
         
         default values: read_json_file('{}{}_experiment_id.json'.format(dict[cvspath], internal[project]))[experiment_id][internal[experiment_id]]
         
         num type: 'string'
         
      add_Gibraltar
         
         DR01.00.21 does not include Gibraltar strait, which is requested by OMIP. Can include it, if model provides it as last value of array.
         
         fatal: False
         
         default values:
            
            - laboratory[add_Gibraltar]
            - False
         
         num type: 'string'
         
      additional_allowed_model_components
         
         Dictionary which contains, for each model, the list of components whih can be used in addition to the declared ones.
         
         fatal: True
         
         default values: internal[CV_experiment][additional_allowed_model_components]
         
         num type: 'string'
         
      adhoc_policy_do_add_1deg_grid_for_tos
         
         Some scenario experiment in DR 01.00.21 do not request tos on 1 degree grid, while other do. If you use grid_policy=adhoc and had not changed the mapping of function. grids.lab_adhoc_grid_policy to grids.CNRM_grid_policy, next setting can force any tos request to also produce tos on a 1 degree grid.
         
         fatal: False
         
         default values:
            
            - laboratory[adhoc_policy_do_add_1deg_grid_for_tos]
            - False
         
         num type: 'string'
         
      allow_duplicates
         
         Should we allow for duplicate vars: two vars with same frequency, shape and realm, which differ only by the table. In DR01.00.21, this actually applies to very few fields (ps-Aermon, tas-ImonAnt, areacellg-IfxAnt).
         
         fatal: False
         
         default values:
            
            - laboratory[allow_duplicates]
            - True
         
         num type: 'string'
         
      allow_duplicates_in_same_table
         
         Should we allow for another type of duplicate vars : two vars with same name in same table (usually with different shapes). This applies to e.g. CMOR vars 'ua' and 'ua7h' in 6hPlevPt. Default to False, because CMIP6 rules does not allow to name output files differently in that case. If set to True, you should also set 'use_cmorvar_label_in_filename' to True to overcome the said rule.
         
         fatal: True
         
         default values:
            
            - laboratory[allow_duplicates_in_same_table]
            - False
         
         num type: 'string'
         
      allow_pseudo_standard_names
         
         DR has sn attributes for MIP variables. They can be real,CF-compliant, standard_names or pseudo_standard_names, i.e. not yet approved labels. Default is to use only CF ones.
         
         fatal: False
         
         default values:
            
            - laboratory[allow_pseudo_standard_names]
            - False
         
         num type: 'string'
         
      allow_tos_3hr_1deg
         
         When using select='no', Xios may enter an endless loop, which is solved if next setting is False.
         
         fatal: False
         
         default values:
            
            - laboratory[allow_tos_3hr_1deg]
            - True
         
         num type: 'string'
         
      branch_year_in_child
         
         In some instances, the experiment start year is not explicit or is doubtful in DR. See file doc/some_experiments_starty_in_DR01.00.21. You should then specify it, using next setting in order that requestItems analysis work in all cases. In some other cases, DR requestItems which apply to the experiment form its start does not cover its whole duration and have a wrong duration (computed based on a wrong start year); They necessitate to fix the start year.
         
         fatal: False
         
         default values: simulation[branch_year_in_child]
         
         num type: 'string'
         
      branching
         
          Describe the branching scheme for experiments involved in some 'branchedYears type' tslice (for details, see: http://clipc-services.ceda.ac.uk/dreq/index/Slice.html ). Just put the as key the common start year in child and as value the list of start years in parent for all members.A dictionary with models name as key and dictionary containing experiment,(branch year in child, list of branch year in parent) key values.
         
         fatal: False
         
         default values:
            
            - laboratory[branching][internal[source_id]]
            - {}
         
         num type: 'string'
         
      bypass_CV_components
         
         If the CMIP6 Controlled Vocabulary doesn't allow all the components you activate, you can set next toggle to True
         
         fatal: False
         
         default values:
            
            - laboratory[bypass_CV_components]
            - False
         
         num type: 'string'
         
      configuration
         
         Configuration used for this experiment. If there is no configuration in lab_settings which matches you case, please rather use next or next two entries: :term:`source_id` and, if needed, :term:`source_type`.
         
         fatal: True
         
         default values: simulation[configuration]
         
         num type: 'string'
         
      context
         
         Context associated with the xml file produced.
         
         fatal: True
         
         default values: dict[context]
         
         num type: 'string'
         
      debug_parsing
         
         In order to identify which xml files generates a problem, you can use this flag.
         
         fatal: False
         
         default values:
            
            - laboratory[debug_parsing]
            - False
         
         num type: 'string'
         
      dr2xml_manages_enddate
         
         A smart workflow will allow you to extend a simulation during it course and to complement the output files accordingly, by managing the 'end date' part in filenames. You can then set next setting to False.
         
         fatal: True
         
         default values:
            
            - laboratory[dr2xml_manages_enddate]
            - True
         
         num type: 'string'
         
      end_year
         
         If you want to carry on the experiment beyond the duration set in DR, and that all requestItems that apply to DR end year also apply later on, set 'end_year' You can also set it if you don't know if DR has a wrong value
         
         fatal: False
         
         default values:
            
            - simulation[end_year]
            - False
         
         num type: 'string'
         
      experiment_for_requests
         
         Experiment id to use for driving the use of the Data Request.
         
         fatal: True
         
         default values:
            
            - simulation[experiment_for_requests]
            - internal[experiment_id]
         
         num type: 'string'
         
      experiment_id
         
         Root experiment identifier.
         
         fatal: True
         
         default values: simulation[experiment_id]
         
         num type: 'string'
         
      filter_on_realization
         
         If you want to produce the same variables set for all members, set this parameter to False.
         
         fatal: False
         
         default values:
            
            - simulation[filter_on_realization]
            - laboratory[filter_on_realization]
            - True
         
         num type: 'string'
         
      fx_from_file
         
         You may provide some variables already horizontally remapped to some grid (i.e. Xios domain) in external files. The varname in file must match the referenced id in pingfile. Tested only for fixed fields. A dictionary with variable id as key and a dictionary as value: the key must be the grid id, the value a dictionary with the file for each resolution.
         
         fatal: False
         
         default values:
            
            - laboratory[fx_from_file]
            - []
         
         num type: 'string'
         
      grid_choice
         
         A dictionary which keys are models name and values the corresponding resolution.
         
         fatal: True
         
         default values: laboratory[grid_choice][internal[source_id]]
         
         num type: 'string'
         
      grid_policy
         
         The grid choice policy for output files.
         
         fatal: True
         
         default values:
            
            - laboratory[grid_policy]
            - False
         
         num type: 'string'
         
      grid_prefix
         
         Prefix of the dr2xml generated grid named to be used.
         
         fatal: True
         
         default values:
            
            - laboratory[grid_prefix]
            - internal[ping_variables_prefix]
         
         num type: 'string'
         
      grids
         
         Grids : per model resolution and per context :- CMIP6 qualifier (i.e. 'gn' or 'gr') for the main grid chosen (because you  may choose has main production grid a regular one, when the native grid is e.g. unstructured)- Xios id for the production grid (if it is not the native grid),- Xios id for the latitude axis used for zonal means (mist match latitudes for grid above)- resolution of the production grid (using CMIP6 conventions),- grid description
         
         fatal: True
         
         default values: laboratory[grids]
         
         num type: 'string'
         
      grids_dev
         
         Grids definition for dev variables.
         
         fatal: True
         
         default values:
            
            - laboratory[grids_dev]
            - {}
         
         num type: 'string'
         
      institution_id
         
         Institution identifier.
         
         fatal: True
         
         default values: laboratory[institution_id]
         
         num type: 'string'
         
      laboratory_used
         
         File which contains the settings to be used for a specific laboratory which is not present by default in dr2xml. Must contains at least the `lab_grid_policy` function.
         
         fatal: False
         
         default values:
            
            - laboratory[laboratory_used]
            - None
         
         num type: 'string'
         
      listof_home_vars
         
         Full path to the file which contains the list of home variables to be taken into account, in addition to the Data Request.
         
         fatal: False
         
         default values:
            
            - simulation[listof_home_vars]
            - laboratory[listof_home_vars]
            - None
         
         num type: 'string'
         
      max_split_freq
         
         The maximum number of years that should be putted in a single file.
         
         fatal: True
         
         default values:
            
            - simulation[max_split_freq]
            - laboratory[max_split_freq]
            - None
         
         num type: 'string'
         
      mips
         
         A dictionary in which keys are grid and values a set of strings corresponding to MIPs names.
         
         fatal: True
         
         default values: laboratory[mips]
         
         num type: 'string'
         
      nemo_sources_management_policy_master_of_the_world
         
         Set that to True if you use a context named 'nemo' and the corresponding model unduly sets a general freq_op AT THE FIELD_DEFINITION GROUP LEVEL. Due to Xios rules for inheritance, that behavior prevents inheriting specific freq_ops by reference from dr2xml generated field_definitions.
         
         fatal: True
         
         default values:
            
            - laboratory[nemo_sources_management_policy_master_of_the_world]
            - False
         
         num type: 'string'
         
      non_standard_attributes
         
         You may add a series of NetCDF attributes in all files for this simulation
         
         fatal: False
         
         default values:
            
            - laboratory[non_standard_attributes]
            - {}
         
         num type: 'string'
         
      non_standard_axes
         
         If your model has some axis which does not have all its attributes as in DR, and you want dr2xml to fix that it, give here the correspondence from model axis id to DR dim/grid id. For label dimensions you should provide the  list of labels, ordered as in your model, as second element of a pair. Label-type axes will be processed even if not quoted. Scalar dimensions are not concerned by this feature. A dictionary with (axis_id, axis_correct_id) or (axis_id, tuple of labels) as key, values.
         
         fatal: False
         
         default values:
            
            - laboratory[non_standard_axes]
            - {}
         
         num type: 'string'
         
      orography_field_name
         
         Name of the orography field name to be used to compute height over orog fields.
         
         fatal: False
         
         default values:
            
            - laboratory[orography_field_name]
            - 'orog'
         
         num type: 'string'
         
      orphan_variables
         
         A dictionary with (context name, list of variables) as (key,value) pairs, where the list indicates the variables to be re-affected to the key-context (initially affected to a realm falling in another context)
         
         fatal: True
         
         default values: laboratory[orphan_variables]
         
         num type: 'string'
         
      path_extra_tables
         
         Full path of the directory which contains extra tables.
         
         fatal: False
         
         default values:
            
            - simulation[path_extra_tables]
            - laboratory[path_extra_tables]
            - None
         
         num type: 'string'
         
      path_to_parse
         
         The path of the directory which, at run time, contains the root XML file (iodef.xml).
         
         fatal: False
         
         default values:
            
            - laboratory[path_to_parse]
            - './'
         
         num type: 'string'
         
      ping_variables_prefix
         
         The tag used to prefix the variables in the ‘field id’ namespaces of the ping file; may be an empty string.
         
         fatal: True
         
         default values: laboratory[ping_variables_prefix]
         
         num type: 'string'
         
      prefixed_orography_field_name
         
         Name of the orography field name to be used to compute height over orog fields prefixed with :term:`ping_variable_prefix`.
         
         fatal: False
         
         default values: '{}{}'.format(internal[ping_variables_prefix], internal[orography_field_name])
         
         num type: 'string'
         
      print_stats_per_var_label
         
         For an extended printout of selected CMOR variables, grouped by variable label.
         
         fatal: False
         
         default values:
            
            - laboratory[print_stats_per_var_label]
            - False
         
         num type: 'string'
         
      print_variables
         
         If the value is a list, only the file/field variables listed here will be put in output files. If boolean, tell if the file/field variables should be put in output files.
         
         fatal: False
         
         default values:
            
            - laboratory[print_variables]
            - True
         
         num type: 'string'
         
      project
         
         Project associated with the simulation.
         
         fatal: False
         
         default values:
            
            - laboratory[project]
            - 'CMIP6'
         
         num type: 'string'
         
      project_settings
         
         Project settings definition file to be used.
         
         fatal: False
         
         default values:
            
            - laboratory[project_settings]
            - internal[project]
         
         num type: 'string'
         
      realization_index
         
         Realization number.
         
         fatal: False
         
         default values:
            
            - simulation[realization_index]
            - '1'
         
         num type: 'string'
         
      realms_per_context
         
         A dictionary which keys are context names and values the lists of realms associated with each context
         
         fatal: True
         
         default values: laboratory[realms_per_context][internal[context]]
         
         num type: 'string'
         
      required_model_components
         
         Dictionary which gives, for each model name, the components that must be present.
         
         fatal: True
         
         default values: internal[CV_experiment][required_model_components]
         
         num type: 'string'
         
      sampling_timestep
         
         Basic sampling timestep set in your field definition (used to feed metadata 'interval_operation'). Should be a dictionary which keys are resolutions and values a context/timestep dictionary.
         
         fatal: True
         
         default values: laboratory[sampling_timestep]
         
         num type: 'string'
         
      save_project_settings
         
         The path of the file where the complete project settings will be written, if needed.
         
         fatal: False
         
         default values:
            
            - laboratory[save_project_settings]
            - None
         
         num type: 'string'
         
      sectors
         
         List of the sectors to be considered.
         
         fatal: False
         
         default values: laboratory[sectors]
         
         num type: 'string'
         
      simple_domain_grid_regexp
         
         If some grid is not defined in xml but by API, and is referenced by a field which is considered by the DR as having a singleton dimension, then: 1) it must be a grid which has only a domain 2) the domain name must be extractable from the grid_id using a regexp and a group number Example: using a pattern that returns full id except for a '_grid' suffix
         
         fatal: False
         
         default values: laboratory[simple_domain_grid_regexp]
         
         num type: 'string'
         
      sizes
         
         A dictionary which keys are resolution and values the associated grid size for atmosphere and ocean grids. The grid size looks like : ['nho', 'nlo', 'nha', 'nla', 'nlas', 'nls', 'nh1']. Used to compute file split frequency.
         
         fatal: True
         
         default values: laboratory[sizes][internal[grid_choice]]format_sizes()
         
         num type: 'string'
         
      source_id
         
         Name of the model used.
         
         fatal: True
         
         default values:
            
            - laboratory[configurations][internal[configuration]][0]
            - simulation[source_id]
         
         num type: 'string'
         
      source_type
         
         If the default source-type value for your source (:term:`source_types` from :term:`lab_and_model_settings`) does not fit, you may change it here. This should describe the model most directly responsible for the output. Sometimes it is appropriate to list two (or more) model types here, among AER, AGCM, AOGCM, BGC, CHEM, ISM, LAND, OGCM, RAD, SLAB e.g. amip , run with CNRM-CM6-1, should quote "AGCM AER". Also see note 14 of https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit
         
         fatal: True
         
         default values:
            
            - laboratory[configurations][internal[configuration]][1]
            - simulation[source_type]
            - laboratory[source_types][internal[source_id]]
         
         num type: 'string'
         
      special_timestep_vars
         
         This variable is used when some variables are computed with a period which is not the basic timestep. A dictionary which keys are non standard timestep and values the list of variables which are computed at this timestep.
         
         fatal: False
         
         default values:
            
            - laboratory[special_timestep_vars]
            - []
         
         num type: 'string'
         
      split_frequencies
         
         Path to the split frequencies file to be used.
         
         fatal: False
         
         default values:
            
            - simulation[split_frequencies]
            - laboratory[split_frequencies]
            - 'splitfreqs.dat'
         
         num type: 'string'
         
      synchronisation_frequency
         
         Frequency at which the synchronisation between buffer and filesystem is done.
         
         fatal: False
         
         default values: []
         
         num type: 'string'
         
      tierMax
         
         Number indicating the maximum tier to consider for experiments.
         
         fatal: True
         
         default values:
            
            - simulation[tierMax]
            - internal[tierMax_lset]
         
         num type: 'string'
         
      tierMax_lset
         
         Number indicating the maximum tier to consider for experiments from lab settings.
         
         fatal: True
         
         default values: laboratory[tierMax]
         
         num type: 'string'
         
      too_long_periods
         
         The CMIP6 frequencies that are unreachable for a single model run. Datafiles will be labelled with dates consistent with content (but not with CMIP6 requirements). Allowed values are only 'dec' and 'yr'.
         
         fatal: True
         
         default values:
            
            - laboratory[too_long_periods]
            - []
         
         num type: 'string'
         
      useAtForInstant
         
         Should xml output files use the `@` symbol for definitions for instant variables?
         
         fatal: False
         
         default values:
            
            - laboratory[useAtForInstant]
            - False
         
         num type: 'string'
         
      use_cmorvar_label_in_filename
         
         CMIP6 rule is that filenames includes the variable label, and that this variable label is not the CMORvar label, but 'MIPvar' label. This may lead to conflicts, e.g. for 'ua' and 'ua7h' in table 6hPlevPt; allows to avoid that, if set to True.
         
         fatal: True
         
         default values:
            
            - laboratory[use_cmorvar_label_in_filename]
            - False
         
         num type: 'string'
         
      use_union_zoom
         
         Say if you want to use XIOS union/zoom axis to optimize vertical interpolation requested by the DR.
         
         fatal: False
         
         default values:
            
            - laboratory[use_union_zoom]
            - False
         
         num type: 'string'
         
      vertical_interpolation_operation
         
         Operation done for vertical interpolation.
         
         fatal: False
         
         default values:
            
            - laboratory[vertical_interpolation_operation]
            - 'instant'
         
         num type: 'string'
         
      vertical_interpolation_sample_freq
         
         Time frequency of vertical interpolation.
         
         fatal: False
         
         default values: laboratory[vertical_interpolation_sample_freq]
         
         num type: 'string'
         
      xios_version
         
         Version of XIOS used.
         
         fatal: False
         
         default values:
            
            - laboratory[xios_version]
            - 2
         
         num type: 'string'
         
      year
         
         Year associated with the launch of dr2xml.
         
         fatal: True
         
         default values: dict[year]
         
         num type: 'string'
         
      zg_field_name
         
         Name of the geopotential height field name to be used to compute height over orog fields.
         
         fatal: False
         
         default values:
            
            - laboratory[zg_field_name]
            - 'zg'
         
         num type: 'string'
         
   Common values
   ^^^^^^^^^^^^^
   .. glossary::
      :sorted:
      
      HDL
         
         HDL associated with the project.
         
         fatal: False
         
         default values:
            
            - simulation[HDL]
            - laboratory[HDL]
            - '21.14100'
         
         num type: 'string'
         
      activity_id
         
         MIP(s) name(s).
         
         fatal: False
         
         default values:
            
            - simulation[activity_id]
            - laboratory[activity_id]
            - internal[CV_experiment][activity_id]
         
         num type: 'string'
         
      branch_method
         
         Branching procedure.
         
         fatal: False
         
         default values:
            
            - simulation[branch_method]
            - 'standard'
         
         num type: 'string'
         
      branch_month_in_parent
         
         Branch month in parent simulation with respect to its time axis.
         
         fatal: False
         
         default values:
            
            - simulation[branch_month_in_parent]
            - '1'
         
         num type: 'string'
         
      branch_year_in_parent
         
         Branch year in parent simulation with respect to its time axis.
         
         fatal: False
         
         default values: []
         
         skip values:
            
            - None
            - 'None'
            - ''
            - 'N/A'
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[experiment_id]
                        
                        check to do: 'eq'
                        
                        reference values: internal[branching]
                        
                     Condition:
                     
                        check value: simulation[branch_year_in_parent]
                        
                        check to do: 'eq'
                        
                        reference values: internal[branching][internal[experiment_id]][1]
                        
               
               value: simulation[branch_year_in_parent]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[experiment_id]
                        
                        check to do: 'neq'
                        
                        reference values: internal[branching]
                        
               
               value: simulation[branch_year_in_parent]
               
         
         num type: 'string'
         
      comment_lab
         
         A character string containing additional information about the models from laboratory settings. Will be complemented with the experiment's specific comment string.
         
         fatal: False
         
         default values:
            
            - laboratory[comment]
            - ''
         
         num type: 'string'
         
      comment_sim
         
         A character string containing additional information about the models from simulation settings. Will be complemented with the experiment's specific comment string.
         
         fatal: False
         
         default values:
            
            - simulation[comment]
            - ''
         
         num type: 'string'
         
      compression_level
         
         The compression level to be applied to NetCDF output files.
         
         fatal: False
         
         default values:
            
            - laboratory[compression_level]
            - '0'
         
         num type: 'string'
         
      contact
         
         Email address of the data producer.
         
         fatal: False
         
         default values:
            
            - simulation[contact]
            - laboratory[contact]
            - 'None'
         
         num type: 'string'
         
      convention_str
         
         Version of the conventions used.
         
         fatal: False
         
         default values: dr2xml.config.conventions
         
         num type: 'string'
         
      conventions_version
         
         Version of the conventions used.
         
         fatal: False
         
         default values: dr2xml.config.CMIP6_conventions_version
         
         num type: 'string'
         
      data_specs_version
         
         Version of the data request used.
         
         fatal: True
         
         default values: data_request.get_version()
         
         num type: 'string'
         
      date_range
         
         Date range format to be used in file definition names.
         
         fatal: False
         
         default values: '%start_date%-%end_date%'
         
         num type: 'string'
         
      description
         
         Description of the simulation.
         
         fatal: False
         
         default values:
            
            - simulation[description]
            - laboratory[description]
         
         num type: 'string'
         
      dr2xml_version
         
         Version of dr2xml used.
         
         fatal: False
         
         default values: dr2xml.config.version
         
         num type: 'string'
         
      experiment
         
         Name of the experiment.
         
         fatal: False
         
         default values: simulation[experiment]
         
         num type: 'string'
         
      expid_in_filename
         
         Experiment label to use in file names and attribute.
         
         fatal: False
         
         default values:
            
            - simulation[expid_in_filename]
            - internal[experiment_id]
         
         forbidden patterns: '.*_.*'
         
         num type: 'string'
         
      forcing_index
         
         Index for variant of forcing.
         
         fatal: False
         
         default values:
            
            - simulation[forcing_index]
            - '1'
         
         num type: 'string'
         
      history
         
         In case of replacement of previously produced data, description of any changes in the production chain.
         
         fatal: False
         
         default values:
            
            - simulation[history]
            - 'none'
         
         num type: 'string'
         
      info_url
         
         Location of documentation.
         
         fatal: False
         
         default values: laboratory[info_url]
         
         num type: 'string'
         
      initialization_index
         
         Index for variant of initialization method.
         
         fatal: False
         
         default values:
            
            - simulation[initialization_index]
            - '1'
         
         num type: 'string'
         
      institution
         
         Full name of the institution of the data producer.
         
         fatal: False
         
         default values:
            
            - laboratory[institution]
            - read_json_file('{}{}_institution_id.json'.format(dict[cvspath], internal[project]))[institution_id][internal[institution_id]]
         
         num type: 'string'
         
      license
         
         File where the license associated with the produced output files can be found.
         
         fatal: False
         
         default values: read_json_file('{}{}_license.json'.format(dict[cvspath], internal[project]))[license][0]
         
         num type: 'string'
         
      list_perso_dev_file
         
         Name of the file which will contain the list of the patterns of perso and dev output file definition.
         
         fatal: False
         
         default values: 'dr2xml_list_perso_and_dev_file_names'
         
         num type: 'string'
         
      member_id
         
         Id of the member done.
         
         fatal: False
         
         default values:
            
            - '{}-{}'.format(common[sub_experiment_id], common[variant_label])
            - common[variant_label]
         
         forbidden patterns: 'none-.*'
         
         num type: 'string'
         
      mip_era
         
         MIP associated with the simulation.
         
         fatal: False
         
         default values:
            
            - simulation[mip_era]
            - laboratory[mip_era]
         
         num type: 'string'
         
      output_level
         
         We can control the max output level set for all output files.
         
         fatal: False
         
         default values:
            
            - laboratory[output_level]
            - '10'
         
         num type: 'string'
         
      parent_activity_id
         
         Description of sub-experiment.
         
         fatal: False
         
         default values:
            
            - simulation[parent_activity_id]
            - simulation[activity_id]
            - laboratory[parent_activity_id]
            - laboratory[activity_id]
            - internal[CV_experiment][parent_activity_id]
         
         num type: 'string'
         
      parent_experiment_id
         
         Parent experiment identifier.
         
         fatal: False
         
         default values:
            
            - simulation[parent_experiment_id]
            - laboratory[parent_experiment_id]
            - internal[CV_experiment][parent_experiment_id]
         
         num type: 'string'
         
      parent_mip_era
         
         Parent’s associated MIP cycle.
         
         fatal: False
         
         default values: simulation[parent_mip_era]
         
         num type: 'string'
         
      parent_source_id
         
         Parent model identifier.
         
         fatal: False
         
         default values: simulation[parent_source_id]
         
         num type: 'string'
         
      parent_time_ref_year
         
         Reference year in parent simulation.
         
         fatal: False
         
         default values:
            
            - simulation[parent_time_ref_year]
            - '1850'
         
         num type: 'string'
         
      parent_time_units
         
         Time units used in parent.
         
         fatal: False
         
         default values: simulation[parent_time_units]
         
         num type: 'string'
         
      parent_variant_label
         
         Parent variant label.
         
         fatal: False
         
         default values: simulation[parent_variant_label]
         
         num type: 'string'
         
      physics_index
         
         Index for model physics variant.
         
         fatal: False
         
         default values:
            
            - simulation[physics_index]
            - '1'
         
         num type: 'string'
         
      prefix
         
         Prefix to be used for each file definition.
         
         fatal: True
         
         default values: dict[prefix]
         
         num type: 'string'
         
      references
         
         References associated with the simulation.
         
         fatal: False
         
         default values: laboratory[references]
         
         num type: 'string'
         
      source
         
         Name of the model.
         
         fatal: False
         
         default values:
            
            - read_json_file('{}{}_source_id.json'.format(dict[cvspath], internal[project]))[source_id][internal[source_id]]make_source_string('source_id'= internal[source_id])
            - laboratory[source]
         
         num type: 'string'
         
      sub_experiment
         
         Sub-experiment name.
         
         fatal: False
         
         default values:
            
            - simulation[sub_experiment]
            - 'none'
         
         num type: 'string'
         
      sub_experiment_id
         
         Sub-experiment identifier.
         
         fatal: False
         
         default values:
            
            - simulation[sub_experiment_id]
            - 'none'
         
         num type: 'string'
         
      variant_info
         
         It is recommended that some description be included to help identify major differences among variants, but care should be taken to record correct information.  dr2xml will add in all cases: 'Information provided by this attribute may in some cases be flawed. Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute.'
         
         fatal: False
         
         default values: simulation[variant_info]
         
         skip values: ''
         
         num type: 'string'
         
      variant_label
         
         Label of the variant done.
         
         fatal: False
         
         default values: 'r{}i{}p{}f{}'.format(internal[realization_index], common[initialization_index], common[physics_index], common[forcing_index])
         
         num type: 'string'
         
Data Request
------------
   Internal values
   ^^^^^^^^^^^^^^^
   .. glossary::
      :sorted:
      
      data_request_config
         
         Configuration file of the data request content to be used
         
         fatal: False
         
         default values:
            
            - laboratory[data_request_config]
            - '/home/rigoudyg/dev/DR2XML/dr2xml_source/dr2xml/dr_interface/CMIP7_config'
         
         num type: 'string'
         
      data_request_content_version
         
         Version of the data request content to be used
         
         fatal: False
         
         default values:
            
            - laboratory[data_request_content_version]
            - 'latest_stable'
         
         num type: 'string'
         
      data_request_path
         
         Path where the data request API used is placed.
         
         fatal: False
         
         default values:
            
            - laboratory[data_request_path]
            - None
         
         num type: 'string'
         
      data_request_used
         
         The Data Request infrastructure type which should be used.
         
         fatal: False
         
         default values:
            
            - laboratory[data_request_used]
            - 'CMIP6'
         
         num type: 'string'
         

File
----
   Internal values
   ^^^^^^^^^^^^^^^
   .. glossary::
      :sorted:
      
      bytes_per_float
         
         Estimate of number of bytes per floating value, given the chosen :term:`compression_level`.
         
         fatal: False
         
         default values:
            
            - laboratory[bytes_per_float]
            - 2
         
         num type: 'string'
         
      grouped_vars_per_file
         
         Variables to be grouped in the same output file (provided additional conditions are filled).
         
         fatal: False
         
         default values:
            
            - simulation[grouped_vars_per_file]
            - laboratory[grouped_vars_per_file]
            - []
         
         num type: 'string'
         
      max_file_size_in_floats
         
         The maximum size of generated files in number of floating values.
         
         fatal: False
         
         default values:
            
            - laboratory[max_file_size_in_floats]
            - 500000000.0
         
         num type: 'string'
         

Home data request
-----------------
   Internal values
   ^^^^^^^^^^^^^^^
   .. glossary::
      :sorted:
      
      perso_sdims_description
         
         A dictionary containing, for each perso or dev variables with a XY-perso shape, and for each vertical coordinate associated, the main attributes of the dimension.
         
         fatal: False
         
         default values:
            
            - simulation[perso_sdims_description]
            - {}
         
         num type: 'string'
         

Selection
---------
   Internal values
   ^^^^^^^^^^^^^^^
   .. glossary::
      :sorted:
      
      excluded_opportunities_lset
         
         List of the opportunities that will be excluded from outputs from laboratory settings.
         
         fatal: False
         
         default values:
            
            - laboratory[excluded_opportunities]
            - []
         
         num type: 'string'
         
      excluded_opportunities_sset
         
         List of the opportunities that will be excluded from outputs from simulation settings.
         
         fatal: False
         
         default values:
            
            - simulation[excluded_opportunities]
            - []
         
         num type: 'string'
         
      excluded_pairs_lset
         
         You can exclude some (variable, table) pairs from outputs. A list of tuple (variable, table) to be excluded from laboratory settings.
         
         fatal: False
         
         default values:
            
            - laboratory[excluded_pairs]
            - []
         
         num type: 'string'
         
      excluded_pairs_sset
         
         You can exclude some (variable, table) pairs from outputs. A list of tuple (variable, table) to be excluded from simulation settings.
         
         fatal: False
         
         default values:
            
            - simulation[excluded_pairs]
            - []
         
         num type: 'string'
         
      excluded_request_links
         
         List of links un data request that should not been followed (those request are not taken into account).
         
         fatal: False
         
         default values:
            
            - laboratory[excluded_request_links]
            - []
         
         num type: 'string'
         
      excluded_spshapes_lset
         
         The list of shapes that should be excluded (all variables in those shapes will be excluded from outputs).
         
         fatal: False
         
         default values:
            
            - laboratory[excluded_spshapes]
            - []
         
         num type: 'string'
         
      excluded_tables_lset
         
         List of the tables that will be excluded from outputs from laboratory settings.
         
         fatal: False
         
         default values:
            
            - laboratory[excluded_tables]
            - []
         
         num type: 'string'
         
      excluded_tables_sset
         
         List of the tables that will be excluded from outputs from simulation settings.
         
         fatal: False
         
         default values:
            
            - simulation[excluded_tables]
            - []
         
         num type: 'string'
         
      excluded_vargroups_lset
         
         List of the variables groups that will be excluded from outputs from laboratory settings.
         
         fatal: False
         
         default values:
            
            - laboratory[excluded_vargroups]
            - []
         
         num type: 'string'
         
      excluded_vargroups_sset
         
         List of the variables groups that will be excluded from outputs from simulation settings.
         
         fatal: False
         
         default values:
            
            - simulation[excluded_vargroups]
            - []
         
         num type: 'string'
         
      excluded_vars_lset
         
         List of CMOR variables to exclude from the result based on previous Data Request extraction from laboratory settings.
         
         fatal: False
         
         default values:
            
            - laboratory[excluded_vars]
            - []
         
         num type: 'string'
         
      excluded_vars_per_config
         
         A dictionary which keys are configurations and values the list of variables that must be excluded for each configuration.
         
         fatal: False
         
         default values:
            
            - laboratory[excluded_vars_per_config][internal[configuration]]
            - []
         
         num type: 'string'
         
      excluded_vars_sset
         
         List of CMOR variables to exclude from the result based on previous Data Request extraction from simulation settings.
         
         fatal: False
         
         default values:
            
            - simulation[excluded_vars]
            - []
         
         num type: 'string'
         
      included_opportunities
         
         List of opportunities that will be processed (all others will not).
         
         fatal: False
         
         default values:
            
            - simulation[included_opportunities]
            - internal[included_opportunities_lset]
         
         num type: 'string'
         
      included_opportunities_lset
         
         List of opportunities that will be processed (all others will not) from laboratory settings.
         
         fatal: False
         
         default values:
            
            - laboratory[included_opportunities]
            - []
         
         num type: 'string'
         
      included_request_links
         
         List of the request links that will be processed (all others will not).
         
         fatal: False
         
         default values:
            
            - laboratory[included_request_links]
            - []
         
         num type: 'string'
         
      included_tables
         
         List of tables that will be processed (all others will not).
         
         fatal: False
         
         default values:
            
            - simulation[included_tables]
            - internal[included_tables_lset]
         
         num type: 'string'
         
      included_tables_lset
         
         List of tables that will be processed (all others will not) from laboratory settings.
         
         fatal: False
         
         default values:
            
            - laboratory[included_tables]
            - []
         
         num type: 'string'
         
      included_vargroups
         
         List of variables groups that will be processed (all others will not).
         
         fatal: False
         
         default values:
            
            - simulation[included_vargroups]
            - internal[included_vargroups_lset]
         
         num type: 'string'
         
      included_vargroups_lset
         
         List of variables groups that will be processed (all others will not) from laboratory settings.
         
         fatal: False
         
         default values:
            
            - laboratory[included_vargroups]
            - []
         
         num type: 'string'
         
      included_vars
         
         Variables to be considered from the Data Request (all others will not)
         
         fatal: False
         
         default values:
            
            - simulation[included_vars]
            - internal[included_vars_lset]
         
         num type: 'string'
         
      included_vars_lset
         
         Variables to be considered from the Data Request (all others will not) from laboratory settings.
         
         fatal: False
         
         default values:
            
            - laboratory[included_vars]
            - []
         
         num type: 'string'
         
      max_priority
         
         Max variable priority level to be output (you may set 3 when creating ping_files while being more restrictive at run time).
         
         fatal: True
         
         default values:
            
            - simulation[max_priority]
            - internal[max_priority_lset]
         
         num type: 'string'
         
      max_priority_lset
         
         Max variable priority level to be output (you may set 3 when creating ping_files while being more restrictive at run time) from lab settings.
         
         fatal: True
         
         default values: laboratory[max_priority]
         
         num type: 'string'
         
      select
         
         Selection strategy for variables.
         
         fatal: True
         
         default values: dict[select]
         
         authorized values:
            
            - 'on_expt_and_year'
            - 'on_expt'
            - 'no'
         
         num type: 'string'
         
      select_excluded_opportunities
         
         Excluded opportunities for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: ['internal[excluded_opportunities_lset]', 'internal[excluded_opportunities_sset]']
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[excluded_opportunities_lset]
               
         
         num type: 'string'
         
      select_excluded_pairs
         
         Excluded pairs for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: ['internal[excluded_pairs_lset]', 'internal[excluded_pairs_sset]']
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[excluded_pairs_lset]
               
         
         num type: 'string'
         
      select_excluded_request_links
         
         Excluded request links for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[excluded_request_links]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: None
               
         
         num type: 'string'
         
      select_excluded_tables
         
         Excluded tables for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: ['internal[excluded_tables_lset]', 'internal[excluded_tables_sset]']
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[excluded_tables_lset]
               
         
         num type: 'string'
         
      select_excluded_vargroups
         
         Excluded variables groups for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: ['internal[excluded_vargroups_lset]', 'internal[excluded_vargroups_sset]']
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[excluded_vargroups_lset]
               
         
         num type: 'string'
         
      select_excluded_vars
         
         Excluded variables for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: ['internal[excluded_vars_lset]', 'internal[excluded_vars_sset]', 'internal[excluded_vars_per_config]']
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[excluded_vars_lset]
               
         
         num type: 'string'
         
      select_grid_choice
         
         Grid choice for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[grid_choice]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: 'LR'
               
         
         num type: 'string'
         
      select_included_opportunities
         
         Included opportunities for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[included_opportunities]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[included_opportunities_lset]
               
         
         num type: 'string'
         
      select_included_request_links
         
         Included request links for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[included_request_links]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: None
               
         
         num type: 'string'
         
      select_included_tables
         
         Included tables for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[included_tables]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[included_tables_lset]
               
         
         num type: 'string'
         
      select_included_vargroups
         
         Included variables groups for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[included_vargroups]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[included_vargroups_lset]
               
         
         num type: 'string'
         
      select_included_vars
         
         Included variables for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[included_vars]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[included_vars_lset]
               
         
         num type: 'string'
         
      select_max_priority
         
         Max priority for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[max_priority]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[max_priority_lset]
               
         
         num type: 'string'
         
      select_mips
         
         MIPs for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[mips][internal[select_grid_choice]]sort_mips()
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[mips]sort_mips()
               
         
         num type: 'string'
         
      select_on_expt
         
         Should data be selected on experiment?
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select]
                        
                        check to do: 'eq'
                        
                        reference values:
                              
                              - 'on_expt_and_year'
                              - 'on_expt'
                        
               
               value: True
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select]
                        
                        check to do: 'eq'
                        
                        reference values: 'no'
                        
               
               value: False
               
         
         num type: 'string'
         
      select_on_year
         
         Should data be selected on year?
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select]
                        
                        check to do: 'eq'
                        
                        reference values: 'on_expt_and_year'
                        
               
               value: internal[year]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select]
                        
                        check to do: 'eq'
                        
                        reference values:
                              
                              - 'no'
                              - 'on_expt'
                        
               
               value: None
               
         
         num type: 'string'
         
      select_sizes
         
         Sizes for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[sizes]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: None
               
         
         num type: 'string'
         
      select_tierMax
         
         tierMax for variable selection.
         
         fatal: True
         
         default values: []
         
         cases:
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: True
                        
               
               value: internal[tierMax]
               
            Case:
            
               conditions:
                     Condition:
                     
                        check value: internal[select_on_expt]
                        
                        check to do: 'eq'
                        
                        reference values: False
                        
               
               value: internal[tierMax_lset]
               
         
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
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         positive
            
            How is the axis oriented?
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         n_glo
            
            Number of values of this axis.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         value
            
            Value of the axis.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         axis_ref
            
            Reference axis.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         name
            
            Name of this axis.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         standard_name
            
            Standard name of the axis.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            authorized types: <class 'str'>
            
            num type: 'string'
            
         long_name
            
            Long name of this axis.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         prec
            
            Precision of the axis.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            num type: 'string'
            
         unit
            
            Unit of the axis.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         value
            
            Value of the axis.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         bounds
            
            Bounds of the axis.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         dim_name
            
            Name dimension of the axis.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         label
            
            Label of the axis.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         axis_type
            
            Axis type.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
   axis_definition
      
      XIOS axis_definition beacon
   axis_group
      
      XIOS axis_group beacon
      
      Attributes:
         prec
            
            Precision associated with the axis group.
            
            fatal: False
            
            default values: '8'
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            num type: 'string'
            
   context
      
      XIOS context beacon
      
      Comments:
         DR_version
            
            Version of the Data Request used
            
            fatal: False
            
            default values: '{} Data Request version {}'.format(internal[data_request_used], common[data_specs_version])
            
            num type: 'string'
            
         CV_version
            
            Controled vocabulary version used.
            
            fatal: False
            
            default values: 'CMIP6-CV version ??'
            
            num type: 'string'
            
         conventions_version
            
            Conventions version used.
            
            fatal: False
            
            default values: 'CMIP6_conventions_version {}'.format(common[conventions_version])
            
            num type: 'string'
            
         dr2xml_version
            
            Version of dr2xml used
            
            fatal: False
            
            default values: 'dr2xml version {}'.format(common[dr2xml_version])
            
            num type: 'string'
            
         lab_settings
            
            Laboratory settings used
            
            fatal: False
            
            default values: 'Lab_and_model settings***newline***{}'.format(laboratory)
            
            num type: 'string'
            
         simulation_settings
            
            Simulation_settings used
            
            fatal: False
            
            default values: 'Simulation settings***newline***{}'.format(simulation)
            
            num type: 'string'
            
         year
            
            Year used for the dr2xml's launch
            
            fatal: False
            
            default values: 'Year processed {}'.format(internal[year])
            
            num type: 'string'
            
      
      Attributes:
         id
            
            Id of the context
            
            fatal: False
            
            default values: internal[context]
            
            num type: 'string'
            
   domain
      
      XIOS domain beacon
      
      Attributes:
         id
            
            Id of the domain.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         ni_glo
            
            Number of points on i dimension.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         nj_glo
            
            Number of points on j dimension.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         type
            
            Type of the domain.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         prec
            
            Precision of the domain.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         lat_name
            
            Latitude axis name.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         lon_name
            
            Longitude axis name.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         dim_i_name
            
            Name of the i dimension.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         domain_ref
            
            Reference domain.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
   domain_definition
      
      XIOS domain_definition beacon
   domain_group
      
      XIOS domain_group beacon
      
      Attributes:
         prec
            
            Precision associated with the domain group.
            
            fatal: False
            
            default values: '8'
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            num type: 'string'
            
   duplicate_scalar
      
      XIOS duplicate_scalar beacon
   field
      
      XIOS field beacon (except for output fields)
      
      Attributes:
         id
            
            Id of the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         field_ref
            
            Id of the reference field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         name
            
            Name of the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         freq_op
            
            Frequency of the operation done on the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         freq_offset
            
            Offset to be applied on operations on the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         grid_ref
            
            Reference grid of the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         long_name
            
            Long name of the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         standard_name
            
            Standard name of the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         unit
            
            Unit of the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         operation
            
            Operation done on the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         detect_missing_value
            
            Should missing values of the field be detected by XIOS.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         prec
            
            Precision of the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
   field_definition
      
      XIOS field_definition beacon
   field_group
      
      XIOS field_group beacon
      
      Attributes:
         freq_op
            
            Frequency of the operation done on the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         freq_offset
            
            Offset to be applied on operations on the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
   field_output
      
      XIOS field beacon (only for output fields)
      
      Attributes:
         field_ref
            
            Reference field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         name
            
            Name of the field.
            
            fatal: False
            
            default values: variable.mipVarLabel
            
            num type: 'string'
            
         grid_ref
            
            Reference grid of the field.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         freq_offset
            
            Offset to be applied on operations on the field.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         detect_missing_value
            
            Should missing values of the field be detected by XIOS.
            
            fatal: False
            
            default values: 'True'
            
            num type: 'string'
            
         default_value
            
            Default value associated with the field.
            
            fatal: True
            
            default values: variable.prec
            
            authorized values:
               
               - '0'
               - '1.e+20'
            
            corrections:
               
               - '': '1.e+20'
               - 'float': '1.e+20'
               - 'real': '1.e+20'
               - 'double': '1.e+20'
               - 'integer': '0'
               - 'int': '0'
            
            num type: 'string'
            
         prec
            
            Precision of the field.
            
            fatal: True
            
            default values: variable.prec
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            num type: 'string'
            
         cell_methods
            
            Cell method associated with the field.
            
            fatal: False
            
            default values: variable.cell_methods
            
            num type: 'string'
            
         cell_methods_mode
            
            Mode associated with the cell method of the field.
            
            fatal: False
            
            default values: 'overwrite'
            
            num type: 'string'
            
         operation
            
            Operation performed on the field.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         freq_op
            
            Frequency of the operation done on the field.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         expr
            
            Expression used to compute the field.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
      
      Variables
         comment
            
            Comment associated with the field.
            
            fatal: False
            
            default values:
               
               - simulation[comments][variable.label]
               - laboratory[comments][variable.label]
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         standard_name
            
            Standard name of the field.
            
            fatal: False
            
            default values: variable.stdname
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         description
            
            Description associated with the field.
            
            fatal: False
            
            default values:
               
               - variable.description
               - 'None'
            
            skip values: ''
            
            num type: 'string'
            
         long_name
            
            Long name of the field.
            
            fatal: False
            
            default values: variable.long_name
            
            num type: 'string'
            
         positive
            
            Way the field should be interpreted.
            
            fatal: False
            
            default values: variable.positive
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         history
            
            History associated with the field.
            
            fatal: False
            
            default values: common[history]
            
            num type: 'string'
            
         units
            
            Units associated with the field.
            
            fatal: False
            
            default values: variable.units
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         cell_methods
            
            Cell method associated with the field.
            
            fatal: False
            
            default values: variable.cell_methods
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         cell_measures
            
            Cell measures associated with the field.
            
            fatal: False
            
            default values: variable.cell_measures
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         flag_meanings
            
            Flag meanings associated with the field.
            
            fatal: False
            
            default values: variable.flag_meanings
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         flag_values
            
            Flag values associated with the field.
            
            fatal: False
            
            default values: variable.flag_values
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         interval_operation
            
            Interval associated with the operation done on the field.
            
            fatal: False
            
            default values: []
            
            conditions:
               Condition:
               
                  check value: dict[operation]
                  
                  check to do: 'neq'
                  
                  reference values: 'once'
                  
            
            num type: 'string'
            
   file
      
      XIOS file beacon (except for output files)
      
      Attributes:
         id
            
            Id of the file.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         name
            
            File name.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         mode
            
            Mode in which the file will be open.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         output_freq
            
            Frequency of the outputs contained in the file.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         enabled
            
            Should the file be considered by XIOS.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
   file_definition
      
      XIOS file_definition beacon
      
      Attributes:
         type
            
            Type of file to be produced
            
            fatal: False
            
            default values: 'one_file'
            
            num type: 'string'
            
         enabled
            
            Should the file_definition be considered by XIOS
            
            fatal: False
            
            default values: 'true'
            
            num type: 'string'
            
   file_output
      
      XIOS file beacon (only for output files)
      
      Attributes:
         id
            
            Id of the output file
            
            fatal: False
            
            default values: '{}_{}_{}'.format(variable.label, dict[table_id], dict[grid_label])
            
            num type: 'string'
            
         name
            
            File name.
            
            fatal: True
            
            default values: build_filename('frequency'= variable.frequency, 'prefix'= common[prefix], 'table'= dict[table_id], 'source_id'= internal[source_id], 'expid_in_filename'= common[expid_in_filename], 'member_id'= common[member_id], 'grid_label'= dict[grid_label], 'date_range'= common[date_range], 'var_type'= variable.type, 'list_perso_dev_file'= common[list_perso_dev_file], 'label'= variable.label, 'mipVarLabel'= variable.mipVarLabel, 'use_cmorvar'= internal[use_cmorvar_label_in_filename])
            
            num type: 'string'
            
         output_freq
            
            Frequency of the outputs contained in the file.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         append
            
            Should the data be append to the file?
            
            fatal: False
            
            default values: 'true'
            
            num type: 'string'
            
         output_level
            
            Output level of the file.
            
            fatal: False
            
            default values: common[output_level]
            
            skip values:
               
               - 'None'
               - ''
               - None
            
            num type: 'string'
            
         compression_level
            
            Compression level of the file.
            
            fatal: False
            
            default values: common[compression_level]
            
            skip values:
               
               - 'None'
               - ''
               - None
            
            num type: 'string'
            
         split_freq
            
            Splitting frequency of the file.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            conditions:
               Condition:
               
                  check value: variable.frequency
                  
                  check to do: 'nmatch'
                  
                  reference values: '.*fx.*'
                  
            
            num type: 'string'
            
         split_freq_format
            
            Splitting frequency format of the file.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            conditions:
               Condition:
               
                  check value: variable.frequency
                  
                  check to do: 'nmatch'
                  
                  reference values: '.*fx.*'
                  
            
            num type: 'string'
            
         split_start_offset
            
            Splitting start offset of the file
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - 'False'
               - None
               - False
            
            conditions:
               Condition:
               
                  check value: variable.frequency
                  
                  check to do: 'nmatch'
                  
                  reference values: '.*fx.*'
                  
            
            num type: 'string'
            
         split_end_offset
            
            Splitting end offset of the file
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - 'False'
               - None
               - False
            
            conditions:
               Condition:
               
                  check value: variable.frequency
                  
                  check to do: 'nmatch'
                  
                  reference values: '.*fx.*'
                  
            
            num type: 'string'
            
         split_last_date
            
            Splitting last date of the file
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            conditions:
               Condition:
               
                  check value: variable.frequency
                  
                  check to do: 'nmatch'
                  
                  reference values: '.*fx.*'
                  
            
            num type: 'string'
            
         time_units
            
            Time units of the file.
            
            fatal: False
            
            default values: 'days'
            
            num type: 'string'
            
         time_counter_name
            
            Time counter name.
            
            fatal: False
            
            default values: 'time'
            
            num type: 'string'
            
         time_counter
            
            Time counter type.
            
            fatal: False
            
            default values: 'exclusive'
            
            num type: 'string'
            
         time_stamp_name
            
            Time stamp name.
            
            fatal: False
            
            default values: 'creation_date'
            
            num type: 'string'
            
         time_stamp_format
            
            Time stamp format.
            
            fatal: False
            
            default values: '%Y-%m-%dT%H:%M:%SZ'
            
            num type: 'string'
            
         uuid_name
            
            Unique identifier of the file name.
            
            fatal: False
            
            default values: 'tracking_id'
            
            num type: 'string'
            
         uuid_format
            
            Unique identifier of the file format.
            
            fatal: False
            
            default values: 'hdl:{}/%uuid%'.format(common[HDL])
            
            skip values:
               
               - 'None'
               - ''
               - None
            
            num type: 'string'
            
         convention_str
            
            Convention used for the file.
            
            fatal: False
            
            default values: common[convention_str]
            
            num type: 'string'
            
         synchronisation_frequency
            
            Frequency at which the synchornisation between buffer and filesystem is done.
            
            fatal: False
            
            default values: internal[synchronisation_frequency]
            
            skip values:
               
               - 'None'
               - ''
               - None
            
            num type: 'string'
            
      
      Variables
         activity_id
            
            Activity id associated with the simulation.
            
            fatal: False
            
            default values: common[activity_id]
            
            num type: 'string'
            
         contact
            
            Contact email.
            
            fatal: False
            
            default values: common[contact]
            
            skip values:
               
               - 'None'
               - ''
               - None
            
            num type: 'string'
            
         data_specs_version
            
            Version of the Data Request used.
            
            fatal: False
            
            default values: common[data_specs_version]
            
            num type: 'string'
            
         dr2xml_version
            
            Version of dr2xml used.
            
            fatal: False
            
            default values: common[dr2xml_version]
            
            num type: 'string'
            
         expid_in_filename
            
            Experiment id to be used in file name.
            
            output key: 'experiment_id'
            
            fatal: False
            
            default values: common[expid_in_filename]
            
            num type: 'string'
            
         description
            
            Description of the file.
            
            fatal: False
            
            default values:
               
               - common[description]
               - internal[CV_experiment][description]
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            conditions:
               Condition:
               
                  check value: internal[experiment_id]
                  
                  check to do: 'eq'
                  
                  reference values: common[expid_in_filename]
                  
            
            num type: 'string'
            
         title_desc
            
            Title of the file.
            
            output key: 'title'
            
            fatal: False
            
            default values:
               
               - common[description]
               - internal[CV_experiment][description]
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            conditions:
               Condition:
               
                  check value: internal[experiment_id]
                  
                  check to do: 'eq'
                  
                  reference values: common[expid_in_filename]
                  
            
            num type: 'string'
            
         experiment
            
            Experiment associated with the simulation.
            
            fatal: False
            
            default values:
               
               - common[experiment]
               - internal[CV_experiment][experiment]
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            conditions:
               Condition:
               
                  check value: internal[experiment_id]
                  
                  check to do: 'eq'
                  
                  reference values: common[expid_in_filename]
                  
            
            num type: 'string'
            
         external_variables
            
            External variables associated with the file.
            
            fatal: False
            
            default values: variable.cell_measuresbuild_external_variables()
            
            skip values: ''
            
            num type: 'string'
            
         forcing_index
            
            Forcing index associated with the simulation.
            
            fatal: False
            
            default values: common[forcing_index]
            
            num type: 'int'
            
         frequency
            
            Frequency associated with the file.
            
            fatal: False
            
            default values: variable.frequency
            
            num type: 'string'
            
         further_info_url
            
            Url to obtain further information associated with the simulation.
            
            fatal: False
            
            default values: 'https://furtherinfo.es-doc.org/{}.{}.{}.{}.{}.{}'.format(variable.mip_era, internal[institution_id], internal[source_id], common[expid_in_filename], common[sub_experiment_id], common[variant_label])
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            conditions:
               Condition:
               
                  check value: laboratory[mip_era]
                  
                  check to do: 'eq'
                  
               Condition:
               
                  check value: simulation[mip_era]
                  
                  check to do: 'eq'
                  
            
            num type: 'string'
            
         grid
            
            Id of the grid used in the file.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         grid_label
            
            Label of the grid used in the file.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         nominal_resolution
            
            Nominal resolution of the grid used in the file.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         comment
            
            Comment associated with the file.
            
            fatal: False
            
            default values: []
            
            skip values: ''
            
            cases:
               Case:
               
                  conditions:
                        Condition:
                        
                           check value: variable.comments
                           
                           check to do: 'neq'
                           
                           reference values:
                                 
                                 - ''
                                 - 'None'
                                 - None
                           
                  
                  value: '{}{}{}'.format(common[comment_lab], common[comment_sim], variable.comments)
                  
               Case:
               
                  conditions:
                        Condition:
                        
                           check value: common[comment_sim]
                           
                           check to do: 'neq'
                           
                           reference values:
                                 
                                 - ''
                                 - 'None'
                                 - None
                           
                        Condition:
                        
                           check value: common[comment_lab]
                           
                           check to do: 'neq'
                           
                           reference values:
                                 
                                 - ''
                                 - 'None'
                                 - None
                           
                  
                  value: '{}{}'.format(common[comment_lab], common[comment_sim])
                  
               Case:
               
                  conditions:
                        Condition:
                        
                           check value: common[comment_sim]
                           
                           check to do: 'neq'
                           
                           reference values:
                                 
                                 - ''
                                 - 'None'
                                 - None
                           
                  
                  value: common[comment_sim]
                  
               Case:
               
                  conditions:
                        Condition:
                        
                           check value: common[comment_lab]
                           
                           check to do: 'neq'
                           
                           reference values:
                                 
                                 - ''
                                 - 'None'
                                 - None
                           
                  
                  value: common[comment_lab]
                  
            
            num type: 'string'
            
         history
            
            History associated with the file.
            
            fatal: False
            
            default values: common[history]
            
            num type: 'string'
            
         initialization_index
            
            Initialization index associated with the simulation.
            
            fatal: False
            
            default values: common[initialization_index]
            
            num type: 'int'
            
         institution_id
            
            Institution id associated with the simulation.
            
            fatal: True
            
            default values: internal[institution_id]
            
            num type: 'string'
            
         institution
            
            Institution associated with the simulation.
            
            fatal: True
            
            default values: common[institution]
            
            num type: 'string'
            
         license
            
            License associated with the file.
            
            fatal: False
            
            default values: common[license]fill_license('institution_id'= internal[institution_id], 'info_url'= common[info_url])
            
            num type: 'string'
            
         mip_era
            
            MIP associated with the simulation.
            
            fatal: False
            
            default values:
               
               - common[mip_era]
               - variable.mip_era
            
            num type: 'string'
            
         parent_experiment_id
            
            Parent experiment id associated with the simulation.
            
            fatal: False
            
            default values: common[parent_experiment_id]
            
            conditions:
               Condition:
               
                  check value: common[parent_experiment_id]
                  
                  check to do: 'neq'
                  
                  reference values:
                        
                        - 'no parent'
                        - ''
                        - 'None'
                  
            
            num type: 'string'
            
         parent_mip_era
            
            MIP associated with the parent experiment.
            
            fatal: False
            
            default values:
               
               - common[parent_mip_era]
               - common[mip_era]
               - variable.mip_era
            
            conditions:
               Condition:
               
                  check value: common[parent_experiment_id]
                  
                  check to do: 'neq'
                  
                  reference values:
                        
                        - 'no parent'
                        - ''
                        - 'None'
                  
            
            num type: 'string'
            
         parent_activity_id
            
            Activity id associated with the parent experiment.
            
            fatal: False
            
            default values: common[parent_activity_id]
            
            conditions:
               Condition:
               
                  check value: common[parent_experiment_id]
                  
                  check to do: 'neq'
                  
                  reference values:
                        
                        - 'no parent'
                        - ''
                        - 'None'
                  
            
            num type: 'string'
            
         parent_source_id
            
            Model id of the parent experiment.
            
            fatal: False
            
            default values:
               
               - common[parent_source_id]
               - internal[source_id]
            
            conditions:
               Condition:
               
                  check value: common[parent_experiment_id]
                  
                  check to do: 'neq'
                  
                  reference values:
                        
                        - 'no parent'
                        - ''
                        - 'None'
                  
            
            num type: 'string'
            
         parent_time_units
            
            Time units of the parent experiment.
            
            fatal: False
            
            default values:
               
               - common[parent_time_units]
               - 'days since {}-01-01 00:00:00'.format(common[parent_time_ref_year])
            
            conditions:
               Condition:
               
                  check value: common[parent_experiment_id]
                  
                  check to do: 'neq'
                  
                  reference values:
                        
                        - 'no parent'
                        - ''
                        - 'None'
                  
            
            num type: 'string'
            
         parent_variant_label
            
            Variant label of the parent experiment.
            
            fatal: False
            
            default values:
               
               - common[parent_variant_label]
               - common[variant_label]
            
            conditions:
               Condition:
               
                  check value: common[parent_experiment_id]
                  
                  check to do: 'neq'
                  
                  reference values:
                        
                        - 'no parent'
                        - ''
                        - 'None'
                  
            
            num type: 'string'
            
         branch_method
            
            Branch method of the simulation.
            
            fatal: False
            
            default values: []
            
            cases:
               Case:
               
                  conditions:
                        Condition:
                        
                           check value: common[parent_experiment_id]
                           
                           check to do: 'neq'
                           
                           reference values:
                                 
                                 - 'no parent'
                                 - ''
                                 - 'None'
                           
                  
                  value: common[branch_method]
                  
               Case:
               
                  conditions: True
                  
                  value: 'no parent'
                  
            
            num type: 'string'
            
         branch_time_in_parent
            
            Branch time of the simulation in the parent's one.
            
            fatal: False
            
            default values:
               
               - compute_nb_days('year_ref'= common[parent_time_ref_year], 'year_branch'= common[branch_year_in_parent], 'month_branch'= common[branch_month_in_parent])
               - simulation[branch_time_in_parent]
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            conditions:
               Condition:
               
                  check value: common[parent_experiment_id]
                  
                  check to do: 'neq'
                  
                  reference values:
                        
                        - 'no parent'
                        - ''
                        - 'None'
                  
            
            num type: 'double'
            
         branch_time_in_child
            
            Branch time of the simulation in the child's one.
            
            fatal: False
            
            default values:
               
               - compute_nb_days('year_ref'= simulation[child_time_ref_year], 'year_branch'= simulation[branch_year_in_child])
               - simulation[branch_time_in_child]
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            conditions:
               Condition:
               
                  check value: common[parent_experiment_id]
                  
                  check to do: 'neq'
                  
                  reference values:
                        
                        - 'no parent'
                        - ''
                        - 'None'
                  
            
            num type: 'double'
            
         physics_index
            
            Physics index associated with the simulation.
            
            fatal: False
            
            default values: common[physics_index]
            
            num type: 'int'
            
         product
            
            Type of content of the file.
            
            fatal: False
            
            default values: 'model-output'
            
            num type: 'string'
            
         realization_index
            
            Realization index associated with the simulation.
            
            fatal: False
            
            default values: internal[realization_index]
            
            num type: 'int'
            
         realm
            
            Realm associated with the file.
            
            fatal: False
            
            default values: variable.modeling_realm<lambda>()
            
            corrections:
               
               - 'ocnBgChem': 'ocnBgchem'
            
            num type: 'string'
            
         references
            
            References associated with the simulation.
            
            fatal: False
            
            default values: common[references]
            
            num type: 'string'
            
         source
            
            Model associated with the simulation.
            
            fatal: True
            
            default values: common[source]
            
            num type: 'string'
            
         source_id
            
            Model id associated with the simulation.
            
            fatal: False
            
            default values: internal[source_id]
            
            num type: 'string'
            
         source_type
            
            Model type associated with the simulation.
            
            fatal: False
            
            default values: internal[source_type]
            
            num type: 'string'
            
         sub_experiment_id
            
            Id of the sub experiment associated with the simulation.
            
            fatal: False
            
            default values: common[sub_experiment_id]
            
            num type: 'string'
            
         sub_experiment
            
            Name of the sub experiment associated with the simulation.
            
            fatal: False
            
            default values: common[sub_experiment]
            
            num type: 'string'
            
         table_id
            
            Id of the table associated with the file.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         title
            
            Title of the file.
            
            fatal: False
            
            default values:
               
               - '{} model output prepared for {} and {} / {} simulation'.format(internal[source_id], internal[project], common[activity_id], simulation[expid_in_filename])
               - '{} model output prepared for {} / {} {}'.format(internal[source_id], internal[project], common[activity_id], internal[experiment_id])
            
            num type: 'string'
            
         variable_id
            
            Id of the variable contained in the file.
            
            fatal: False
            
            default values: variable.mipVarLabel
            
            num type: 'string'
            
         variant_info
            
            Variant information associated with the simulation.
            
            fatal: False
            
            default values: '. Information provided by this attribute may in some cases be flawed. Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute.'.format(common[variant_info])
            
            num type: 'string'
            
         variant_label
            
            Variant label associated with the simulation.
            
            fatal: False
            
            default values: common[variant_label]
            
            num type: 'string'
            
   generate_rectilinear_domain
      
      XIOS generate_rectilinear_domain beacon
   grid
      
      XIOS grid beacon
      
      Attributes:
         id
            
            Id of the grid.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
   grid_definition
      
      XIOS grid_definition beacon
   interpolate_axis
      
      XIOS interpolate_axis beacon
      
      Attributes:
         type
            
            Type of the interpolated axis.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         order
            
            Order of the interpolated axis.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         coordinate
            
            Coordinate of the interpolated axis.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
   interpolate_domain
      
      XIOS interpolate_domain beacon
      
      Attributes:
         type
            
            Type of the interpolated domain.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         order
            
            Order of the interpolation.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         renormalize
            
            Should the interpolated domain be renormalized?
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         mode
            
            Mode used for the interpolation.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         write_weight
            
            Should interpolation weights be written?
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         coordinate
            
            Coordinate of the interpolated domain.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
   scalar
      
      XIOS scalar beacon
      
      Attributes:
         id
            
            Id of the scalar.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         scalar_ref
            
            Reference scalar.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         name
            
            Name of the scalar.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         standard_name
            
            Standard name of the scalar.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         long_name
            
            Long name of the scalar.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         label
            
            Label of the scalar.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         prec
            
            Precision of the scalar.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            authorized values:
               
               - '2'
               - '4'
               - '8'
            
            corrections:
               
               - '': '4'
               - 'float': '4'
               - 'real': '4'
               - 'double': '8'
               - 'integer': '2'
               - 'int': '2'
            
            num type: 'string'
            
         value
            
            Value of the scalar.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         bounds
            
            Bounds of the scalar.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         bounds_name
            
            Bounds name of the scalar.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         axis_type
            
            Axis type of the scalar.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         positive
            
            Orientation of the scalar.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
            num type: 'string'
            
         unit
            
            Unit of the scalar.
            
            fatal: False
            
            default values: []
            
            skip values:
               
               - ''
               - 'None'
               - None
            
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
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
         type
            
            Encoding type of the variable's content.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            
   zoom_axis
      
      XIOS zoom_axis beacon
      
      Attributes:
         index
            
            Index of the zoomed axis.
            
            fatal: False
            
            default values: []
            
            num type: 'string'
            