""" 
    Provide frequencies for a table name - Both in XIOS syntax and in CMIP6_CV 
    and also split_frequencies for the files hodling the whole of a table's variables 
    
    Rationale: Because CMIP6_CV does not (yet) provide the correspondance between a table name 
    and the corresponding frequency (albeit this is instrumental in DRS), and because 
    we need to translate anyway to XIOS syntax
"""

table2freq={
    "3hr"      : ("3h","3hr"),

    "6hrLev"   : ("6h","6hr"),
    "6hrPlev"  : ("6h","6hr"),
    "6hrPlevPt": ("6h","6hr"),

    "AERday"   :  ("1d","day"),
    "AERfx"    : ("1d","fx"),
    # mpmoine_next_modif: frequence CMIP6 pour AERhr = 'hr' et non '1hr'
    #TBD: remplacer "hr" par "1hr" selon reponse de D. Nadeau a l'issue https://github.com/PCMDI/cmip6-cmor-tables/issues/59
    "AERhr"    : ("1h","hr"),
    "AERmon"   : ("1mo","mon"),
    "AERmonZ"  : ("1mo","mon"),

    "Amon"     : ("1mo","mon"),

    "CF3hr"    : ("3h","3hr"),
    "CFday"    : ("1d","day"),
    "CFmon"    : ("1mo","mon"),
    # mpmoine_next_modif: table2freq: frequence pour les tables subhr
    # mpmoine_future_modif: table2freq: la syntaxe xios pour le subhr est '1ts' et non 'instant' (vu par Arnaud)
    "CFsubhr"  : ("1ts","subhr"),
    "CFsubhrOff": ("1ts","subhr"),
    "E1hr"     : ("1h","1hr"),
     # mpmoine_future_modif: table2freq: la syntaxe xios pour 1hr est '1h' et non '1hr'
    "E1hrClimMon" : ("1h","1hr"),
    "E3hr"     : ("3h","3hr"),
    "E3hrPt"   : ("3h","3hr"),
    "E6hrZ"    : ("6h","6hr"),
    "Eday"     :("1d","day"),
    "EdayZ"    :("1d","day"),
    "Efx"      :("1d","fx"),
    "Emon"     : ("1mo","mon"),
    "EmonZ"    : ("1mo","mon"),
    # mpmoine_next_modif: table2freq: frequence pour les tables subhr
    # mpmoine_future_modif: table2freq: la syntaxe pour le subhe est '1ts' et non 'instant' (vu par Arnaud)
    "Esubhr"   : ("1ts","subhr"),
    "Eyr"      : ("1y","yr"),

    "IfxAnt"   :("1d","fx"),
    "IfxGre"   :("1d","fx"),
    "ImonAnt"  :("1mo","mon"),
    "ImonGre"  :("1mo","mon"),
    "IyrAnt"   :("1y","yr"),
    "IyrGre"   :("1y","yr"),
    
    "LImon"    : ("1mo","mon"),
    "Lmon"     : ("1mo","mon"),

    "Oclim"    : ("1d","monClim"),
    "Oday"     : ("1d","day"),
    "Odec"     : ("10y","dec"),
    "Ofx"      : ("1d","fx"),
    "Omon"     : ("1mo","mon"),
    "Oyr"      : ("1y","yr"),

    "SIday"    : ("1d","day"),
    "SImon"    : ("1mo","mon"),

    "day"      : ("1d","day"),
    "fx"       : ("1d","fx"),

    # mpmoine_last_modif: table2freq: ajout des tables Primavera
    "Prim1hr"  : ("1h","1hr"),
    "Prim3hr"  : ("3h","3hr"),
    "Prim3hrPt": ("3h","3hr"),
    "Prim6hr"  : ("6h","6hr"),
    "Prim6hrPt": ("6h","6hr"),
    "PrimO6hr" : ("6h","6hr"),
    "PrimOday" : ("1d","day"),
    "PrimOmon" : ("1mo","mon"),
    "PrimSIday": ("1d","day"),
    "Primday"  : ("1d","day"),
    "PrimdayPt": ("1d","day"),
    "Primmon"  : ("1mo","mon"),
    "PrimmonZ" : ("1mo","mon"),

    "Myproday"  : ("1d","day"),
    "testAmon"  : ("1mo","mon"),

}

table2splitfreq={
    "E3hrPt"     : "1mo" , #3-hourly (instantaneous, extension) [3hr] (22 variables)
    "E3hr"       : "1mo" , #3-hourly (time mean, extension) [3hr] (57 variables)
    "CF3hr"      : "1mo" , #3-hourly associated with cloud forcing [3hr] (43 variables)
    "3hr"        : "1mo" , #3-hourly data [3hr] (23 variables)
    "E6hrZ"      : "1mo" , #6-hourly Zonal Mean (extension) [6hr] (2 variables)
    "6hrPlevPt"  : "1mo" , #6-hourly atmospheric data on pressure levels (instantaneous) [6hr] (31 variables)
    "6hrPlev"    : "1mo" , #6-hourly atmospheric data on pressure levels (time mean) [6hr] (29 variables)
    "6hrLev"     : "1mo" , #6-hourly data on atmospheric model levels [6hr] (10 variables)
    "IyrAnt"     : "100y" , #Annual fields on the Antarctic ice sheet [yr] (33 variables)
    "IyrGre"     : "100y" , #Annual fields on the Greenland ice sheet [yr] (33 variables)
    "Oyr"        : "10y" , #Annual ocean variables [yr] (125 variables)
    "Eday"       : "1mo" , #Daily (time mean, extension) [day] (123 variables)
    "Eyr"        : "10y" , #Daily (time mean, extension) [yr] (22 variables)
    "day"        : "1mo" , #Daily Data (extension - contains both atmospheric and oceanographic data) [day] (35 variables)
    "Oday"       : "1mo" , #Daily ocean data [day] (6 variables)
    "EdayZ"      : "1mo" , #Daily Zonal Mean (extension) [day] (15 variables)
    "AERday"     : "1mo" , #Daily atmospheric chemistry and aerosol data [day] (10 variables)
    "CFday"      : "1mo" , #Daily data associated with cloud forcing [day] (36 variables)
    "SIday"      : "1mo" , #Daily sea-ice data [day] (8 variables)
    "Odec"       : "100y" , #Decadal ocean data [decadal] (24 variables)
    "CFsubhr"    : "1mo" , #Diagnostics for cloud forcing analysis at specific sites [subhr] (37 variables)
    "Efx"        : "1y" ,  #Fixed (extension) [fx] (21 variables)
    "AERfx"      : "1y" ,  #Fixed atmospheric chemistry and aerosol data [fx] (1 variables)
    "IfxAnt"     : "1y" ,  #Fixed fields on the Antarctic ice sheet [fx] (4 variables)
    "IfxGre"     : "1y" ,  #Fixed fields on the Greenland ice sheet [fx] (4 variables)
    "Ofx"        : "1y" ,  #Fixed ocean data [fx] (6 variables)
    "E1hr"       : "1mo" , #Hourly Atmospheric Data (extension) [1hr] (16 variables)
    "AERhr"      : "1mo" , #Hourly atmospheric chemistry and aerosol data [hr] (5 variables)
    "E1hrClimMon": "100y" , #Diurnal Cycle [1hrClimMon] (5 variables)
    "Emon"       : "10y" , #Monthly (time mean, extension) [mon] (385 variables)
    "Oclim"      : "10y" , #Monthly climatologies of ocean data [monClim] (34 variables)
    "SImon"      : "10y" , #Monthly sea-ice data [mon] (89 variables)
    "CFsubhrOff" : "1mo" , #Offline diagnostics for cloud forcing analysis [subhr] (9 variables)
    "AERmon"     : "10y" , #Monthly atmospheric chemistry and aerosol data [mon] (126 variables)
    "AERmonZ"    : "10y" , #Monthly atmospheric chemistry and aerosol data [mon] (16 variables)
    "Amon"       : "10y" , #Monthly atmospheric data [mon] (75 variables)
    "CFmon"      : "10y" , #Monthly data associated with cloud forcing [mon] (56 variables)
    "LImon"      : "10y" , #Monthly fields for the terrestrial cryosphere [mon] (37 variables)
    "ImonAnt"    : "10y" , #Monthly fields on the Antarctic ice sheet [mon] (28 variables)
    "ImonGre"    : "10y" , #Monthly fields on the Greenland ice sheet [mon] (28 variables)
    "Lmon"       : "10y" , #Monthly land surface and soil model fields [mon] (54 variables)
    "Omon"       : "10y" , #Monthly ocean data [mon] (294 variables)
    "EmonZ"      : "10y" , #Monthly zonal means (time mean, extension) [mon] (31 variables)
    "Esubhr"     : "10y" , #Sub-hourly (extension) [subhr] (32 variables)
    "fx"         : "1y" ,  #Fixed variables [fx] (10 variables)

    #mpmoine_last_modif: table2splitfreq: ajout des tables Primavera
    "Prim1hr"  : "1mo",
    "Prim3hr"  : "1mo",
    "Prim3hrPt": "1mo",
    "Prim6hr"  : "1mo",
    "Prim6hrPt": "1mo",
    "PrimO6hr" : "1mo",
    "PrimOday" : "1mo",
    "PrimOmon" : "10y",
    "PrimSIday": "1mo",
    "Primday"  : "1mo",
    "PrimdayPt": "1mo",
    "Primmon"  : "10y",
    "PrimmonZ" : "10y",

    "Myproday" : "1mo",

}

# mpmoine_last_modif: table2freq.py: nouveau: cmipFreq2xiosFreq
cmipFreq2xiosFreq={}
for v in table2freq.values():
    if not cmipFreq2xiosFreq.has_key(v[1]): cmipFreq2xiosFreq[v[1]]=v[0]

