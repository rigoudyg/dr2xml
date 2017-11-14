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
from table2freq import table2freq
#-from dr2xml import dr2xml_error

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
        return [""]
    elif policy=="native+DR": # Produce both in 'native' and DR grid
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
    if dq.inx.uid[cmvarid].label in [ "tos", "sos" ] :
        return [ g for g in grids if g in ["","1deg"]]
    else:
        ngrids=[ g for g in grids if g not in [ "1deg", "2deg", "100km", "50km" ]]
        #if "cfsites" in grids : return ["","cfsites"]
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
    # ['nho','nlo','nha','nla','nlas','nls','nh1']  /  nz = sc.mcfg['nlo']
    nb_cosp_sites=129 
    nb_curtain_sites=1000 # TBD : better estimate of 'curtain' size
    # TBD : better size estimates for atmosphere/ocean zonal means, and ocean transects 
    nb_lat=mcfg['nh1'] # TBC
    nb_lat_ocean=mcfg['nh1']
    ocean_transect_size=mcfg['nh1'] # TBC, mais comment le calculer ?
    #
    siz=0
    s=svar.spatial_shp
    if ( s == "XY-A" ): #Global field on model atmosphere levels
        siz=mcfg['nla']*mcfg['nha']
    elif ( s == "XY-AH" ): #Global field on model atmosphere half-levels
        siz=(mcfg['nla']+1)*mcfg['nha']
    elif ( s == "XY-P7T" ): #Global field (7 pressure tropospheric levels)
        siz=7*mcfg['nha']
    elif ( s[0:4] == "XY-P" ): #Global field (pressure levels)
        siz=int(s[4:])*mcfg['nha']
    elif ( s[0:4] == "XY-H" ): #Global field (altitudes)
        siz=int(s[4:])*mcfg['nha']

    elif ( s == "S-AH" ): #Atmospheric profiles (half levels) at specified sites
        siz=(mcfg['nla']+1)*nb_cosp_sites
    elif ( s == "S-A" ): #Atmospheric profiles at specified sites
        siz=mcfg['nla']*nb_cosp_sites
    elif ( s == "S-na" ): #Site (129 specified sites)
        siz=nb_cosp_sites

    elif ( s == "L-na" ): #COSP curtain
        siz=nb_curtain_sites        
    elif ( s == "L-H40" ): #Site profile (at 40 altitudes)
        siz=40*nb_curtain_sites        

    elif ( s == "Y-P19") : #Atmospheric Zonal Mean (on 19 pressure levels)
        #mpmoine_next_modif:field_size: nb_lat au lieu de nblat (vu par Arnaud)
        siz=nb_lat*19
    elif ( s == "Y-P39") : #Atmospheric Zonal Mean (on 39 pressure levels)
        siz=nb_lat*39
    elif ( s == "Y-A" ): #Zonal mean (on model levels)
        siz=nb_lat*mcfg['nla']
    elif ( s == "Y-na" ): #Zonal mean (on surface)
        siz=nb_lat
    elif ( s == "na-A" ): #Atmospheric profile (model levels)
        # mpmoine_correction:field_size: 'na-A' s'applique a des dims (alevel)+spectband mais aussi a (alevel,site) => *nb_cosp_sites
        siz=mcfg['nla']*nb_cosp_sites

    elif ( s == "XY-S" ): #Global field on soil levels
        siz=mcfg['nls']*mcfg['nha']
    
    elif ( s == "XY-O" ): #Global ocean field on model levels
        siz=mcfg['nlo']*mcfg['nho']

    elif ( s == "XY-na" ): #Global field (single level)
        siz=mcfg['nha']
        if svar.modeling_realm in \
           [ 'ocean', 'seaIce', 'ocean seaIce', 'ocnBgchem', 'seaIce ocean' ] : 
            siz=mcfg['nho']
        
    elif ( s == "YB-R" ): #Ocean Basin Meridional Section (on density surfaces)
        siz=mcfg['nlo']*nb_lat_ocean
    elif ( s == "YB-O" ): #Ocean Basin Meridional Section
        siz=mcfg['nlo']*nb_lat_ocean
    elif ( s == "YB-na" ): #Ocean Basin Zonal Mean
        siz=nb_lat_ocean

    elif ( s == "TR-na" ): #Ocean Transect
        siz=ocean_transect_size
    elif ( s == "TRS-na" ): #Sea-ice ocean transect
        siz=ocean_transect_size

    elif ( s == "na-na" ): #Global mean/constant
        siz=1

    return siz

# mpmoine_last_modif:split_frequency_for_variable: suppression de l'argument table
# mpmoine_next_modif:split_frequency_for_variable: passage de 'context' en argument pour recuperer le model_timestep
def split_frequency_for_variable(svar, lset, mcfg,context,printout=False):
    """
    Compute variable level split_freq and returns it as a string

    Method : if shape is basic, compute period using field size and a
    parameter from lset indicating max filesize, with some smart
    rounding.  Otherwise, use a fixed value which depends on shape, 
    with a default value

    """
    max_size=lset.get("max_file_size_in_floats",500*1.e6)
    size=field_size(svar, mcfg)
    # mpmoine_last_modif:split_frequency_for_variable: on ne passe plus par table2freq pour recuperer 
    # mpmoine_last_modif:split_frequency_for_variable: la frequence de la variable mais par svar.frequency
    freq=svar.frequency
    if (size != 0 ) : 
        # Try by years first
        size_per_year=size*timesteps_per_freq_and_duration(freq,365,lset["sampling_timestep"][context])
        nbyears=max_size/float(size_per_year)
        if printout : print "size per year=%s, size=%s, nbyears=%g"%(`size_per_year`,`size`,nbyears)
        if nbyears > 1. :
            if nbyears < 10:
                return("1y")
            elif nbyears < 50 :
                return("10y")
            elif nbyears < 100 :
                return("50y")
            elif nbyears < 200 :
                return("100y")
            else :
                return("200y")
        else: 
            # Try by month
            size_per_month=size*timesteps_per_freq_and_duration(freq,31,lset["sampling_timestep"][context])
            nbmonths=max_size/float(size_per_month)
            if nbmonths > 1. :
                return("1mo")
            else:
                # Try by day
                size_per_day=size*timesteps_per_freq_and_duration(freq,1,lset["sampling_timestep"][context])
                nbdays=max_size/float(size_per_day)
                if nbdays > 1. :
                    return("1d")
                else:
                    # mpmoine_last_modif:split_frequency_for_variable: on ne passe plus par table2freq pour recuperer
                    # mpmoine_last_modif:split_frequency_for_variable: la frequence de la variable mais par svar.frequency
                    raise(dr2xml_error("No way to put even a single day "+\
                        "of data in %g for frequency %s, var %s, table %s"%\
                        (max_size,freq,svar.label,svar.mipTable)))
    else:
      # mpmoine_zoom_modif:split_frequency_for_variable: print de warning si on arrive pas a calculer une split_freq
      print "Warning: field size is 0, cannot compute split frequency."
       
                
def timesteps_per_freq_and_duration(freq,nbdays,sampling_tstep):
    # This function returns the number of records within nbdays
    duration=0.
    # Translate freq strings to duration in days
    if freq=="3hr" : duration=1./8
    elif freq=="6hr" : duration=1./4
    elif freq=="day" : duration=1.
    # mpmoine_next_modif:timesteps_per_freq_and_duration: ajour de la frequence 'hr'
    elif freq=="1hr" or freq=="hr" : duration=1./24
    elif freq=="mon" : duration=31.
    elif freq=="yr" : duration=365.
    #mpmoine_next_modif:timesteps_per_freq_and_duration: ajout des cas frequence 'subhr' et 'dec'
    elif freq=="subhr" : duration=1./(86400./sampling_tstep)
    elif freq=="dec" : duration=10.*365
    # If freq actually translate to a duration, return
    # number of timesteps for number of days
    if duration != 0. : return float(nbdays)/duration
    # Otherwise , return a sensible value
    elif freq=="fx" : return 1.
    elif freq=="monClim" : return (int(float(nbdays)/365) + 1)* 12.
    elif freq=="dayClim" : return (int(float(nbdays)/365) + 1)* 365.
    elif freq=="1hrClimMon" : return (int(float(nbdays)/31) + 1) * 24.

    

