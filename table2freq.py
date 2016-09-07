""" 
    Provide frequencies for a table name - Both in XIOS syntax and in CMIP6_CV 
    
    Rationale: Because CMIP6_CV does not (yet) provide the correspondance between a table name 
    and the corresponding frequency (albiet this is instrumental in DRS), and because 
    we need to translate anyway to XIOS syntax
"""

table2freq={
    "3hr"  : ("3h","3hr"),
    "3hrpt": ("3h","3hr"),
    "6hr"  : ("6h","6hr"),
    "6hrpt": ("6h","6hr"),
    "day"  : ("1d","day"),
    "Aday" : ("1d","day"),
    "Amon" : ("1mo","mon"),
    "LImon": ("1mo","mon"),
    "Lmon" : ("1mo","mon"),
    "OImon": ("1mo","mon"),
    "Oclim": ("once","monClim"),
    "Oday" : ("1d","day"),
    "Odec" : ("1y","yr"),
    "Omon" : ("1mo","mon"),
    "Oyr"  : ("1y","yr"),
    "aero" : ("TBD","TBD"),
    "cfOff": ("TBD","TBD"),
    "cfSites": ("TBD","TBD"),
    "fx"   : ("once","fx"),
    "emYr" : ("1y","yr"),
    "emMon": ("1mo","mon"),
    "emMonZ": ("1mo","mon"),
    "emMonclim": ("1mo","mon"),
    "SImon" : ("1mo","mon"),
    "SIday" : ("1d","day"),
}

