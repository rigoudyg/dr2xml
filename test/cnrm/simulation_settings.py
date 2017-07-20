# -*- coding: iso-8859-15 -*-


simulation_settings_short={    
    "experiment_id"  : "historical",
    "activity_id"       : "CMIP", 
    "parent_experiment_id" : "piControl", # omit this setting (or set to 'no parent') if not applicable
                                          # (remaining parent attributes will be disregarded)
    "branch_method"        : "standard", # default value='standard', meaning ~ "select a start date" 
    "branch_time_in_parent": "365.0D0", # a double precision value, in parent time units, 
    "branch_time_in_child" : "0.0D0", # a double precision value, in child time units,
    "comments"             : {}
    }

simulation_settings={    
    # Dictionnary describing the necessary attributes for a given simulation

    # Warning : some lines are commented out in this example but should be 
    # un-commented in some cases. Read the comments !
    
    "source_id"      : "CNRM-CM6-1", # which model is used for this simulation
    #"experiment_id"  : "amip",
    "experiment_id"  : "historical",
    #"experiment_id"  : "Forced-Atmos-Land",
    #"experiment_id"  : "Coupled",
    #"experiment_id"  : "DCPP-C13",
    
    #"contact"        : "", set it only if it is specific to the simualtion
    #"project"        : "CMIP6",  #CMIP6 is the default

    #'source_type'    : "ESM" # If source_type is special only for this experiment (e.g. : AMIP)
                      #(i.e. not the same as in lab_and_model settings), you may tell that here

    # MIP specifying the experiment. For historical, it is CMIP6 itself
    # In a few cases it may be appropriate to include multiple activities in the activity_id 
    # (separated by single spaces).  
    # An example of this is  "LUMIP AerChemMIP"  for one of the land-use change experiments.
    "activity_id"       : "CMIP", # examples :  "PMIP" ,  "LS3MIP LUMIP" ; defaults to "CMIP6"
    
    # It is recommended that some description be included to help identify major differences among variants, 
    # but care should be taken to record correct information.  Prudence dictates that this attribute includes 
    # a warning along the following lines:   Information provided by this attribute may in some cases be flawed.#
    # Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute. 
    "variant_info"      : "Start date chosen so that variant r1i1p1f1 has the better fit with Krakatoa impact on tos " ,
    #
    "realization_index"    : 1, # Value may be omitted if = 1
    "initialization_index" : 1, # Value may be omitted if = 1
    "physics_index"        : 1, # Value may be omitted if = 1
    "forcing_index"        : 1, # Value may be omitted if = 1
    #
    # All about the parent experiment and branching scheme
    "parent_experiment_id" : "piControl", # omit this setting (or set to 'no parent') if not applicable
                                          # (other parent attributes below will then be disregarded)
    "branch_method"        : "standard", # default value='standard', meaning ~ "select a start date" 
    "branch_time_in_parent": "365.0D0", # a double precision value, in parent time units (days from ...)
    "branch_time_in_child" : "0.0D0", # a double precision value, in child_time_units (days from ...)
    #'parent_time_units'    : "" #in case it is not the same as child time units
    #'parent_variant_label' :""  #Default to 'same as child'. Other cases should be exceptional
    #"parent_mip_era"       : 'CMIP5'   # only in special cases (e.g. PMIP warm start from CMIP5/PMIP3 experiment)
    #'parent_activity   '   : 'CMIP'    # only in special cases, defaults to CMIP
    #'parent_source_id'     : 'CNRM-CM5.1' #only in special cases, where parent model is not the same model
    #
    "sub_experiment_id"    : "none", # Optional, default is 'none'; example : s1960. 
    "sub_experiment"       : "none", # Optional, default is 'none'
    "history"              : "none", #Used when a simulation is re-run, an output file is modified ....
    # A per-variable dict of comments which are specific to this simulation. It will replace  
    # the all-simulation comment present in lab_and_model_settings
    'comments'     : {
        #'tas' : 'tas diagnostic could have a special scheme in this simulation',
        }
    }
