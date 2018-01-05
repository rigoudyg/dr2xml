""" 
    Provide frequencies for a table name - Both in XIOS syntax and in CMIP6_CV 
    and also split_frequencies for the files hodling the whole of a table's variables 
    
    Rationale: Because CMIP6_CV does not (yet) provide the correspondance between a table name 
    and the corresponding frequency (albeit this is instrumental in DRS), and because 
    we need to translate anyway to XIOS syntax
"""

import sys


Cmip6Freq2XiosFreq={
    "subhr"     :"1ts",
    "subhrPt"   :"1ts",
    #
    "1hr"       :"1h",
    "hr"        :"1h",
    "3hr"       :"3h",
    "3hrPt"     :"3h",
    "6hr"       :"6h",
    "6hrPt"     :"6h",
    #
    "day"       :"1d",
    "5day"      :"5d",
    "10day"     :"10d",
    #
    "mon"       :"1mo",
    "yr"        :"1y",
    "dec"       :"10y",
    #
    "fx"        :"1d",
    #
    "monClim"   :"1d",
    "1hrClimMon":"1hr",
    }

def guess_freq_from_table_name(table):
    """ 
    Based on non-written CMIP6 conventions, deduce the frequency from the 
    table name; frequencies are in Xios syntax 

    Used for cases where the table is not a CMIP6 one
    """
    
    if   table=="E1hrClimMon"     : return "1h"
    #
    elif table[0:5]  =="subhr"    : return "1ts"
    elif table[-6:-1]=="subhr"    : return "1ts"
    elif table[-9:-1]=="subhrOff" : return "1ts"
    #
    elif table[0:3]  =="3hr"      : return "3h"
    elif table[-4:-1]=="3hr"      : return "3h" # CF3hr
    elif table[1:4]  =="3hr"      : return "3h" # E3hr, E3hrPt
    elif table[-6:-1]=="3hrPt"    : return "3h"   
    #
    elif table[0:3]  =="6hr"      : return "6h"
    elif table[1:4]  =="6hr"      : return "6h"
    elif table[-6:-1]=="6hrPt"    : return "6h"
    #
    elif table[0:3]  =="1hr"      : return "1h"
    elif table[-4:-1]=="1hr"      : return "1h"
    elif table[-3:-1]=="hr"       : return "1h"
    #
    elif table[-4:-1]=="day"      : return "1d"
    elif table[-6:-1]=="dayPt"    : return "1d"
    #
    elif table[-5:-1]=="5day"     : return "5d"
    #
    elif table[1:4]  =="mon"      : return "1mo"
    elif table[-4:-1]=="mon"      : return "1mo"
    elif table[-5:-1]=="monZ"     : return "1mo"
    elif table[-4:-1]=="Mon"      : return "1mo"
    elif table[-1:-5]=="Clim"     : return "1mo"
    #
    elif table[-3:-1]=="yr"       : return "1y" # Eyr, Oyr ...
    elif table[1:3]  =="yr"       : return "1y" # IyrAnt et al.
    #
    elif table[1:4]  =="dec"      : return "10y"
    #
    elif table[-3:-1]=="fx"       : return "1d"
    elif table[1:3]  =="fx"       : return "1d"
    #
    else :
        print "ERROR in guess_freq_from_table : cannot deduce frequency from table named %s"%table
        sys.exit(1)
    

