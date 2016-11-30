""" 
    Provide frequencies for a table name - Both in XIOS syntax and in CMIP6_CV 
    
    Rationale: Because CMIP6_CV does not (yet) provide the correspondance between a table name 
    and the corresponding frequency (albeit this is instrumental in DRS), and because 
    we need to translate anyway to XIOS syntax
"""

table2freq={
    "3hr"  : ("3h","3hr"),
    "3hrpt": ("3h","3hr"),
    "6hr"  : ("6h","6hr"),
    "6hrpt": ("6h","6hr"),
    "6hrPlev": ("6h","6hr"),
    "6hrLev": ("6h","6hr"),
    "6hrPlevpt": ("6h","6hr"),
    "day"  : ("1d","day"),
    "Aday" : ("1d","day"),
    "Amon" : ("1mo","mon"),
    "AmonAdj": ("TBD","TBD"),
    "LImon": ("1mo","mon"),
    "Lmon" : ("1mo","mon"),
    "OImon": ("1mo","mon"),
    "Oclim": ("once","monClim"),
    "Oday" : ("1d","day"),
    "Odec" : ("1y","yr"),
    "Omon" : ("1mo","mon"),
    "Oyr"  : ("1y","yr"),
    "aero" : ("TBD","TBD"),
    "aermonthly" :("1mo","mon"),
    "aerdaily" :("1d","day"),
    "cfMon": ("1mo","mon"),
    "cfDay": ("1d","day"),
    "cfOff": ("TBD","TBD"),
    "cfSites": ("TBD","TBD"),
    "fx"   : ("once","fx"),
    "Ofx"  : ("once","fx"),
    "emYr" : ("1y","yr"),
    "emMon": ("1mo","mon"),
    "emMonZ": ("1mo","mon"),
    "emMonclim": ("1mo","mon"),
    "em3hr" :("3h","3hr"),
    "emDayZ" :("1d","day"),
    "emFx" :("once","fx"),
    "emDay" :("1d","day"),
    "emDaypt" :("1d","day"),
    "SImon" : ("1mo","mon"),
    "SIday" : ("1d","day"),
    "SPECS_OImon" : ("1mo","mon"),
    "SPECS_Omon" :("1mo","mon"),
    "LImongre" :("1mo","mon"),
    "LImonant" :("1mo","mon"),

}

