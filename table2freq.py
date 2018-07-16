""" 
    Provide frequencies for a table name - Both in XIOS syntax and in CMIP6_CV 
    and also split_frequencies for the files hodling the whole of a table's variables 
    
    Rationale: Because CMIP6_CV does not (yet) provide the correspondance between a table name 
    and the corresponding frequency (albeit this is instrumental in DRS), and because 
    we need to translate anyway to XIOS syntax
"""

import sys


def Cmip6Freq2XiosFreq(freq,table,lset) :
    if freq in [ "subhr", "subhrPt" ] :
        if table=="CFsubhr" : rep=lset.get("CFsubhr_frequency","1ts")
        elif table is None :
                print "Issue in dr2xml with table None and freq=",freq
                sys.exit(0)
        else:
            rep="1ts"
    else:
        corresp={
            "1hr"       :"1h",
            "1hrPt"     :"1h",
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
            "monPt"     :"1mo",
            #
            "yr"        :"1y",
            "yrPt"      :"1y",
            #
            "dec"       :"10y",
            #
            "fx"        :"1d",
            #
            "monC"      :"1mo",
            "1hrCM"     :"1mo",
        }
        rep=corresp[freq]
    return rep
    

def old_guess_freq_from_table_name(table):
    """ 
    Based on non-written CMIP6 conventions, deduce the frequency from the 
    table name; returned frequencies are in CMIP6 syntax 

    Used for cases where the table is not a CMIP6 one
    """
    
    if table=="E1hrClimMon"     : return "1hr"
    #
    elif table[0:5]=="subhr"    : return "subhr"
    elif table[-5:]=="subhr"    : return "subhr"
    elif table[-8:]=="subhrOff" : return "subhr"
    #
    elif table[0:3]=="3hr"      : return "3hr"
    elif table[-3:]=="3hr"      : return "3hr" # CF3hr
    elif table[1:4]=="3hr"      : return "3hr" # E3hr, E3hrPt
    elif table[-5:]=="3hrPt"    : return "3hr"   
    #
    elif table[0:3]=="6hr"      : return "6hr"
    elif table[1:4]=="6hr"      : return "6hr"
    elif table[-5:]=="6hrPt"    : return "6hr"
    elif table[-3:]=="6hr"      : return "6hr"
    #
    elif table[0:3]=="1hr"      : return "1hr"
    elif table[0:5]=="1hrPt"    : return "1hr"
    elif table[-3:]=="1hr"      : return "1hr"
    elif table[-5:]=="1hrPt"    : return "1hr"
    elif table[-2:]=="hr"       : return "1hr"
    #
    elif table[-4:]=="5day"     : return "5d"
    #
    elif table[-3:]=="day"      : return "day"
    elif table[-5:]=="dayPt"    : return "day"
    #
    elif table[1:4]=="mon"      : return "mon"
    elif table[-3:]=="mon"      : return "mon"
    elif table[-4:]=="monZ"     : return "mon"
    elif table[-3:]=="Mon"      : return "mon"
    elif table[-4:]=="Clim"     : return "mon"
    #
    elif table[-2:]=="yr"       : return "yr" # Eyr, Oyr ...
    elif table[1:3]=="yr"       : return "yr" # IyrAnt et al.
    #
    elif table[1:4]=="dec"      : return "dec"
    #
    elif table[-2:]=="fx"       : return "fx"
    elif table[1:3]=="fx"       : return "fx"
    elif table[0:2]=="fx"       : return "fx"
    #
    else :
        print "ERROR in guess_freq_from_table : cannot deduce frequency from table named %s"%table
        sys.exit(1)

def guess_freq_from_table_name(table):
    """ 
    Based on non-written CMIP6 conventions, deduce the frequency from the 
    table name; returned frequencies are in CMIP6 syntax 

    Used for cases where the table is not a CMIP6 one
    """
    if "subhr"  in table   : return "subhr"
    elif "1hr"  in table   : return "1hr"
    elif "3hr"  in table   : return "3hr"
    elif "6hr"  in table   : return "6hr"
    elif "hr"   in table   : return "1hr"
    elif "5day" in table   : return "5d"
    elif "day"  in table   : return "day"
    elif "mon"  in table   : return "mon"
    elif "yr"   in table   : return "yr"
    elif "dec"  in table   : return "dec"
    elif "fx"   in table   : return "fx"
    else :
        print "ERROR in guess_freq_from_table : cannot deduce frequency from table named %s"%table
        sys.exit(1)

def longest_possible_period(freq,too_long_periods):
    """
    Returns the longest period/frequency acessible given the value of too_long_periods
    Input and output freqs follow Xios syntax
    Too_long_periods follow CMIP6 syntax (i.e.  : dec, "yr" )
    """
    if freq=="10y" and any ([ 'dec' in f for f in too_long_periods ]) :
        return longest_possible_period("1y",too_long_periods)
    elif freq=="1y" and any ([ 'yr' in f for f in too_long_periods ]) :
        return longest_possible_period("1mo",too_long_periods)
    else :
        return freq
