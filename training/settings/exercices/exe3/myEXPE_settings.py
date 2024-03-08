# -*- coding: iso-8859-15 -*-

# An example of settings for a CMIP6 experiment/simulation, for use by dr2xml
# It complies with dr2xml v1.00. It complements another settings file, relevant
# for laboratory and model settings
# See refs at bottom

simulation_settings={    

    #----------------------------------------------------------------------------------------------  
    #----- MODEL USED:
    #---------------------------------------------------------------------------------------------- 
   
    "configuration"  : "AOGCM"  ,
    #>>>"source_id"      : "CNRM-CM6-1",

    #----------------------------------------------------------------------------------------------  
    #----- CURRENT EXPERIMENT:
    #---------------------------------------------------------------------------------------------- 
    
    # DR experiment name to process. See http://clipc-services.ceda.ac.uk/dreq/index/experiment.html
    "experiment_id"  : "historical",
    
    # Describing the member - Values may be omitted if = 1
    "realization_index"    : 1, 
    #>>>"initialization_index" : 1, 
    #>>>"physics_index"        : 1, 
    #>>>"forcing_index"        : 1,           # should be 2 for all CMIP6 experiments, until further notice...
    
    # Describe simulation times
    'child_time_ref_year'  : 1850,            # FIXED, because must be consistent with arpsfx.xml et al.
    "branch_year_in_child" : 1850,            # this is the start year of this 'child simulation', in its calendar. 
    #"branch_month_in_child" : 1,             # this is the start month, default: 1=Ja
    "branch_year_in_parent": 2600,            # branching year if a parent exists 
    
    #---------------------------------------------------------------------------------------------- 
    #----- RELATED EXPERIMENTS AND BRANCHING SCHEME:
    #----------------------------------------------------------------------------------------------  
    
    # All about the parent experiment (if any)
    #>>>'parent_variant_label' :""            # default:'same as child', other cases should be exceptional
    #>>>"parent_mip_era"       : 'CMIP5'      # set it only in special cases (e.g. PMIP warm start from CMIP5/PMIP3 experiment)
    #>>>'parent_source_id'     : 'CNRM-CM5.1' # set it only in special cases, where parent model is not the same model
    #>>>'parent_time_ref_year' : 1850,        # FIXED, because must be consistent with arpsfx.xml et al.
    
    # All about subexperiment (if any)
    #>>>"sub_experiment_id" : "",             # optional, default is 'none'; example : s1960. 
    #>>>"sub_experiment"    : "",             # optional, default is 'none'
    
    # All about the branching scheme (if any)
    #>>>"branch_method"     : "",             # default value='standard' meaning ~ "select a start date" 
                                              # (this is not necessarily the parent start date
    
    #----------------------------------------------------------------------------------------------  
    #----- EXCLUDED(INCLUDED) FROM(IN) THE PRODUCTION:
    #----------------------------------------------------------------------------------------------  
    
    # For some experiments (e.g. concentration-driven historical in AESM config), the only way to 
    # avoid producing useless fields is to explictly exclude variables (in addition to those in lab_settings)
    #>>>'excluded_vars' : [],
    
    # It can be handy to exclude some Tables at the experiment level. They are added to the lab-level set
    #>>>"excluded_tables" : [],
    
    # You can specifically exclude some pairs (vars,tables), here in experiment settings
    # They will be added to the lab-settings list of excluded pairs 
    #>>> "excluded_pairs" : []

    #... or alternatively specify what to include (This has precedence over the excluded stuff)
    # variables to process. This has precedence over the excluded_vars stuff
    "included_vars" : ["tas"],
    "included_tables"  : ["Amon"],

    #----------------------------------------------------------------------------------------------  
    #----- ADDITIONAL NETCDF ATTRIBUTES TO WRITE IN OUTPUT FILES:
    #---------------------------------------------------------------------------------------------- 
    
    # Additional information about the experiment, e.g. how you did interpret the expt design)
    #>>>"comment" : "" ,
    
    # It is recommended that some description be included to help identify major differences 
    # among variants (members), but care should be taken to record correct information.  
    #>>>"variant_info" : "" ,
    
    # A per-variable dict of comments which are specific to this simulation. It will replace  
    # the all-simulation comment present in lab_and_model_settings
    'comments' : {
    #>>>    #'tas' : 'tas diagnostic could have a special scheme in this simulation',
        },
    
    # General history of the simulation (if any)
    #>>>"history" : "",                       # used when a simulation is re-run, an output file is modified ....
    
    
    }

#----------------------------------------------------------------------------------------------  
#----- REFERENCES:
#---------------------------------------------------------------------------------------------- 

# The reference documents are listed in top level document :https://pcmdi.llnl.gov/CMIP6/Guide/
# Of interest :
#   - paragraph 5 of https://pcmdi.llnl.gov/CMIP6/Guide/modelers.html
#   - CMIP6 Data Request , in browsable format: http://clipc-services.ceda.ac.uk/dreq/index.html

