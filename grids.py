"""
Management of output grids 

Principles : the Data Request may specify which grid to use : either native or a common, regular, one. This specifed per requestLink, which means per set of variables and experiments. 

dr2xml allows for the lab to choose among various policy  :
   - DR or None : always follow DR spec
   - native     : never not follow DR spec (always use native or close-to-native grid)
   - native+DR  : always produce on the union of grids
   - adhoc      : decide on each case, based on CMORvar attributes, using a 
                  lab-specific scheme implemented in a lab-provided Python 
                  function which should replace function lab_adhoc_grid_policy

Also : management of fields size/split_frequency 

"""

compression_factor=None
splitfreqs=None

    
def normalize(grid) :
    """ in DR 1.0.2, values are :  
    ['', 'model grid', '100km', '50km or smaller', 'cfsites', '1deg', '2deg', '25km or smaller', 'native']
    """
    if grid in [ "native", "model grid", "" ] : return ""
    return grid.replace(" or smaller","")

def decide_for_grids(cmvarid,grids,lset,dq):
    """
    Decide which set of grids a given variable should be produced on
    
    CMVARID is uid of the CMORvar
    GRIDS is a list of strings for grid as specified in requestLink 
    LSET is the laboratory settings dictionnary. It carries a policy re. grids
    
    Returns a list of grid strings (with some normalization) (see below)
    
    TBD : use Martin's acronyms for grid policy
    """
    # Normalize and remove duplicates in grids list
    ngrids=map(normalize,grids)
    sgrids=set()
    for g in ngrids : sgrids.add(g)
    ngrids=list(sgrids)
    #
    policy=lset.get("grid_policy")
    if policy is None or policy=="DR": # Follow DR spec
        return ngrids
    elif policy=="native": # Follow lab grids choice (gr or gn depending on context - see lset['grids"])
        if ngrids==['cfsites'] : return ngrids
        else: return [""]
    elif policy=="native+DR": # Produce both in 'native' and DR grid
        if ngrids==['cfsites'] : return ngrids
        else: 
            sgrids.add('')
            return list(sgrids)
    elif policy=="adhoc" :
        return lab_adhoc_grid_policy(cmvarid,ngrids,lset,dq)
    else :
        dr2xml_error("Invalid grid policy %s"%policy)

def lab_adhoc_grid_policy(cmvarid,grids,lset,dq) :
    """
    Decide , in a lab specific way, which set of grids a given
    variable should be produced on You should re-engine code below to
    your own decision scheme, if the schemes of the standard grid
    policy choices (see fucntion decide_for_grid) do not fit

    CMVARID is uid of the CMORvar
    GRIDS is a list of strings for grid as specified in requestLink (with some normalization)
    LSET is the laboratory settings dictionnary. It carries a policy re. grids
    
    Returns either a single grid string or a list of such strings
    """
    return CNRM_grid_policy(cmvarid,grids,lset,dq) 

def CNRM_grid_policy(cmvarid,grids,lset,dq) : #TBD
    """
    See doc of lab_adhoc_grid_policy
    """
    if dq.inx.uid[cmvarid].label in [ "sos" ] :
        return [ g for g in grids if g in ["","1deg"]]
    elif dq.inx.uid[cmvarid].label in [ "tos" ] and \
         ( dq.inx.uid[cmvarid].mipTable not in [ "3hr" ] or lset.get("allow_tos_3hr_1deg",True)):
        return [ g for g in grids if g in ["","1deg"]]
    else:
        ngrids=[ g for g in grids if g not in [ "1deg", "2deg", "100km", "50km" ]]
        #if "cfsites" in grids : return ["","cfsites"]
        if ngrids == [] : ngrids=[ "" ] # We should at least provide native grid
        return ngrids


def DRgrid2gridatts(grid) :
     """ Returns label, resolution, description for a DR grid name"""
     if grid=="cfsites" : return ("gn","100 km", \
                               "data sampled in model native grid by nearest neighbour method ")
     if grid=="1deg" : return ("gr1","1x1 degree", \
                               "data regridded to a CMIP6 standard 1x1 degree latxlon grid from the native grid")
     if grid=="2deg" : return ("gr2","2x2 degree", \
                               "data regridded to a CMIP6 standard 2x2 degree latxlon grid from the native grid")
     if grid=="100km" : return ("gr3","100 km", \
                               "data regridded to a CMIP6 standard 100 km resol grid from the native grid")
     if grid=="50km"  : return ("gr4","50 km", \
                               "data regridded to a CMIP6 standard 50 km resol grid from the native grid")
     if grid=="25km"  : return ("gr5","25 km", \
                               "data regridded to a CMIP6 standard 25 km resol grid from the native grid")
     return("grx","?x? degree", "grid has no description- please fix DRgrid2gridatts for grid %s"%grid)


def field_size(svar, mcfg):

    # COmputing field size is basee on the fact that sptial dimensions
    # are deduced from spatial shape and values in mcfg, while
    # attribute other_dims_size of the variable indicates he prodcut
    # of the non-spatial dimensions sizes

    # ['nho','nlo','nha','nla','nlas','nls','nh1'] / nz = sc.mcfg['nlo']

    nb_lat=mcfg['nh1'] 
    nb_lat_ocean=mcfg['nh1']
    atm_grid_size=mcfg['nha']
    atm_nblev=mcfg['nla']
    soil_nblev=mcfg['nls']
    oce_nblev=mcfg['nlo']
    oce_grid_size=mcfg['nho']
    # TBD : dimension sizes below should be derived from DR query
    nb_cosp_sites=129 
    nb_lidar_temp=40
    nb_parasol_refl=5
    nb_isccp_tau=7
    nb_isccp_pc=7
    nb_curtain_sites=1000 
    #
    siz=0
    s=svar.spatial_shp
    if ( s == "XY-A" ): #Global field on model atmosphere levels
        siz=atm_nblev*atm_grid_size
    elif ( s == "XY-AH" ): #Global field on model atmosphere half-levels
        siz=(atm_nblev+1)*atm_grid_size
    elif ( s[0:4] == "XY-P" ): #Global field (pressure levels)
        if "jpdftaure" in svar.label :
            siz=atm_grid_size
        else:
            siz=atm_grid_size*svar.other_dims_size
    elif ( s[0:4] == "XY-H" ): #Global field (altitudes)
        siz=atm_grid_size*svar.other_dims_size
    elif ( s == "S-AH" ): #Atmospheric profiles (half levels) at specified sites
        siz=(atm_nblev+1)*nb_cosp_sites
    elif ( s == "S-A" ): #Atmospheric profiles at specified sites
        siz=atm_nblev*nb_cosp_sites
    elif ( s == "S-na" ): #Site (129 specified sites)
        siz=nb_cosp_sites

    elif ( s == "L-na" ): #COSP curtain
        siz=nb_curtain_sites        
    elif ( s == "L-H40" ): #Site profile (at 40 altitudes)
        siz=nb_curtain_sites*svar.other_dims_size

    elif ( s == "Y-P19") : #Atmospheric Zonal Mean (on 19 pressure levels)
        siz=nb_lat*svar.other_dims_size
    elif ( s == "Y-P39") : #Atmospheric Zonal Mean (on 39 pressure levels)
        siz=nb_lat*svar.other_dims_size

    elif ( s == "Y-A" ): #Zonal mean (on model levels)
        siz=nb_lat*atm_nblev
    elif ( s == "Y-na" ): #Zonal mean (on surface)
        siz=nb_lat
    elif ( s == "na-A" ): #Atmospheric profile (model levels)
        # mpmoine_correction:field_size: 'na-A' s'applique a des dims (alevel)+spectband mais aussi a (alevel,site) => *nb_cosp_sites
        siz=atm_nblev*nb_cosp_sites

    elif ( s == "XY-S" ): #Global field on soil levels
        siz=soil_nblev*atm_grid_size
    
    elif ( s == "XY-SN" ): #TBD : restore correct size for fields on snow levels (was supposed to be size 1, for tsnl)
        siz=atm_grid_size
    
    elif ( s == "XY-O" ): #Global ocean field on model levels
        siz=oce_nblev*oce_grid_size

    elif ( s == "XY-na" ): #Global field (single level)
        siz=atm_grid_size
        if svar.modeling_realm in \
           [ 'ocean', 'seaIce', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean' ] : 
            siz=oce_grid_size
        siz*=svar.other_dims_size
    elif ( s == "XY-temp" ): #Global field (lidar_temp)
        siz=atm_grid_size*nb_lidar_temp
    elif ( s == "XY-sza5" ): #Global field (parasol_refl)
        siz=atm_grid_size*nb_parasol_refl
    elif ( s == "XY-tau|plev7c" ): #Global field (isccp_tau x isccp_pc)
        siz=atm_grid_size*nb_isccp_tau*nb_isccp_pc

    elif ( s == "YB-R" ): #Ocean Basin Meridional Section (on density surfaces)
        siz=oce_nblev*nb_lat_ocean
    elif ( s == "YB-O" ): #Ocean Basin Meridional Section
        siz=oce_nblev*nb_lat_ocean
    elif ( s == "YB-na" ): #Ocean Basin Zonal Mean
        siz=nb_lat_ocean

    elif ( s == "TR-na" ): #Ocean Transect
        siz=svar.other_dims_size
    elif ( s == "TRS-na" ): #Sea-ice ocean transect
        siz=svar.other_dims_size

    elif ( s == "na-na" ): #Global mean/constant
        siz=1

    if siz==0 :
        raise dr2xml_grids_error("Cannot compute field_size for var %s"%(svar.label))

    return siz

def split_frequency_for_variable(svar, lset, grid, mcfg,context,printout=False):
    """
    Compute variable level split_freq and returns it as a string

    Method : if shape is basic, compute period using field size and a
    parameter from lset indicating max filesize, with some smart
    rounding.  Otherwise, use a fixed value which depends on shape, 
    with a default value

    """
    global splitfreqs
    if splitfreqs is None : read_splitfreqs()
    if splitfreqs and svar.label in splitfreqs and \
       svar.mipTable in splitfreqs[svar.label] :
        return splitfreqs[svar.label][svar.mipTable]
    #
    max_size=lset.get("max_file_size_in_floats",500*1.e6)
    #
    global compression_factor
    size=field_size(svar, mcfg)*lset.get("bytes_per_float",2)
    if compression_factor is None : read_compression_factors()
    if compression_factor and svar.label in compression_factor and \
       svar.mipTable in compression_factor[svar.label] :
        if printout : print "Dividing size of %s by %g : %g -> %g"%(svar.label,\
                compression_factor[svar.label][svar.mipTable],size,\
                (size+0.)/compression_factor[svar.label][svar.mipTable])
        size = (size+0.)/compression_factor[svar.label][svar.mipTable]
    #else:
    #    # Some COSP outputs are highly compressed
    #    if 'cfad' in svar.label : size/=10.
    #    if 'clmisr' in svar.label : size/=10.

    if (size != 0 ) : 
        freq=svar.frequency
        sts=lset["sampling_timestep"][grid][context]
        # Try by years first
        size_per_year=size*timesteps_per_freq_and_duration(freq,365,sts)
        nbyears=max_size/float(size_per_year)
        if printout : print "size per year=%s, size=%s, nbyears=%g"%(`size_per_year`,`size`,nbyears)
        if nbyears > 1. :
            if   nbyears > 500 : return "500y"
            elif nbyears > 250 : return "250y"
            elif nbyears > 100 : return "100y"
            elif nbyears >  50 : return  "50y"
            elif nbyears >  25 : return  "25y"
            elif nbyears >  10 : return  "10y"
            elif nbyears >   5 : return   "5y"
            elif nbyears >   2 : return   "2y"
            else : return "1y"
        else: 
            # Try by month
            size_per_month=size*timesteps_per_freq_and_duration(freq,31,sts)
            nbmonths=max_size/float(size_per_month)
            if nbmonths > 6. :
                return("6mo")
            elif nbmonths > 4. :
                return("4mo")
            elif nbmonths > 3. :
                return("3mo")
            elif nbmonths > 0.7 :
                return("1mo")
            else:
                # Try by day
                size_per_day=size*timesteps_per_freq_and_duration(freq,1,sts)
                nbdays=max_size/float(size_per_day)
                if nbdays > 1. :
                    return("1d")
                else:
                    raise(dr2xml_grids_error("No way to put even a single day "+\
                        "of data in %g for frequency %s, var %s, table %s"%\
                        (max_size,freq,svar.label,svar.mipTable)))
    else:
      raise dr2xml_grids_error("Warning: field_size returns 0 for var %s, cannot compute split frequency."%(svar.label))
       
                
def timesteps_per_freq_and_duration(freq,nbdays,sampling_tstep):
    # This function returns the number of records within nbdays
    duration=0.
    # Translate freq strings to duration in days
    if   freq=="3hr" or freq=="3hrPt" or freq=="3h" : duration=1./8
    elif freq=="6hr" or freq=="6hrPt" or freq=="6h" : duration=1./4
    elif freq=="day" or freq=="1d"                  : duration=1.
    elif freq=="5day" or freq=="5d"                 : duration=5.
    elif freq=="10day" or freq=="10d"               : duration=10.
    elif freq=="1hr" or freq=="hr" or freq=="1hrPt" or freq=="1h" : duration=1./24
    elif freq=="mon" or freq=="monPt" or freq=="monC" or freq=="1mo" : duration=31.
    elif freq=="yr"  or freq=="yrPt" or freq=="1y"  : duration=365.
    # TBD ; use setting's value for CFsubhr_frequency
    elif freq=="subhr" or freq=="subhrPt" or freq=="1ts" : duration=1./(86400./sampling_tstep) 
    elif freq=="dec" or freq=="10y"                  : duration=10.*365
    #
    # If freq actually translate to a duration, return
    # number of timesteps for number of days
    #
    if duration != 0. : return float(nbdays)/duration
    # Otherwise , return a sensible value
    elif freq=="fx" : return 1.
    #elif freq=="monClim" : return (int(float(nbdays)/365) + 1)* 12.
    #elif freq=="dayClim" : return (int(float(nbdays)/365) + 1)* 365.
    #elif freq=="1hrClimMon" : return (int(float(nbdays)/31) + 1) * 24.
    elif freq=="1hrCM" : return (int(float(nbdays)/31) + 1) * 24.
    else : raise(dr2xml_grids_error("Frequency %s is not handled"%freq))
    

def read_compression_factors():
    """
    read compression factors: first column is variable label, second 
    column is mipTabe; third column is a correction factor due to 
    compression efficiency for that variable (good compression <-> high value); 
    They should be evaluated on test runs, and applied on runs with 
    the same compression_level setting
    This factor is applied above the bytes_per_float setting
    """
    global compression_factor
    # No need to reread or try for ever
    if compression_factor is not None : return
    try:
        fact=open("compression_factors.dat","r")
    except:
        compression_factor=False
        return
    lines=fact.readlines()
    compression_factor=dict()
    for line in lines :
        if line[0]=='#' : continue
        varlabel=line.split()[0]
        table=line.split()[1]
        factor=float(line.split()[2])
        if varlabel not in compression_factor :
            compression_factor[varlabel]=dict()
        # Keep smallest factor for each variablelabel
        if table not in compression_factor[varlabel] or \
           compression_factor[varlabel][table] > factor :
            compression_factor[varlabel][table]=factor

def read_splitfreqs():
    """
    read split_frequencies: first column is variable label, second 
    column is mipTabe; third column is the split_freq
    """
    global splitfreqs
    # No need to reread or try for ever
    if splitfreqs is not None : return
    try:
        freq=open("splitfreqs.dat","r")
        print "Reading split_freqs from file"
    except:
        splitfreqs=False
        return
    lines=freq.readlines()
    freq.close()
    splitfreqs=dict()
    for line in lines :
        if line[0]=='#' : continue
        varlabel=line.split()[0]
        table=line.split()[1]
        freq=line.split()[2]
        if varlabel not in splitfreqs :
            splitfreqs[varlabel]=dict()
        # Keep smallest factor for each variablelabel
        if table not in splitfreqs[varlabel] :
            splitfreqs[varlabel][table]=freq

class dr2xml_grids_error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
    def __str__(self):
        return `self.valeur`
