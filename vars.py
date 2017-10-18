# -*- coding: iso-8859-15 -*-
print_DR_errors=True
print_DR_stdname_errors=False

import sys,os
import json
from table2freq import table2freq
#-from dr2xml import dr2xml_error

# A class for unifying CMOR vars and home variables
# mpmoine_last_modif:simple_CMORvar: ajout des attributs 'mip_era', 'missing' et 'dimids'
# mpmoine_future_modif:simple_CMORvar: ajout de l'attribut 'label_without_psuffix' et suppresion de l'attribut dimids
# mpmoine_correction:simple_CMORvar: ajout de l'attribut 'label_non_ambiguous' 
class simple_CMORvar(object):
    def __init__(self):
        self.type           = False
        self.modeling_realm = None 
        self.grids          = [""] 
        self.label          = None  # taken equal to the CMORvar label
        self.label_without_area= None  # taken equal to MIPvar label
        self.label_without_psuffix= None
        self.label_non_ambiguous= None
        self.frequency      = None 
        self.mipTable       = None 
        self.positive       = None 
        self.description    = None 
        self.stdname        = None 
        self.stdunits       = None 
        self.long_name      = None 
        self.struct         = None
        self.sdims          = {}
        self.cell_methods   = None
        self.cell_measures  = None
        self.spatial_shp    = None 
        self.temporal_shp   = None 
        self.experiment     = None 
        self.mip            = None
        self.Priority       = 1     # Will be changed using DR or extra-Tables
        self.mip_era        = False # Later changed in projectname (uppercase) when appropriate
        self.missing        = 1.e+20
        self.cmvar          =None  # corresponding CMORvar, if any

# mpmoine_future_modif: nouvelle classe simple_Dim
# A class for unifying grid info coming from DR and extra_Tables
# mpmoine_future_modif:simple_Dim: ajout de l'attribut 'is_zoom_of'
# mpmoine_zoom_modif:simple_Dim: ajout de l'attribut 'zoom_label'
#
class simple_Dim(object):
    def __init__(self):
        self.label        = False
        self.zoom_label   = False
        self.stdname      = False
        self.long_name    = False
        self.positive     = False
        self.requested    = ""
        self.value        = False
        self.out_name     = False
        self.units        = False
        self.is_zoom_of   = False
        # SS : ajout bounds pour distinguer le cas de couches de pression
        self.bounds       = False
        # mpmoine_union_optim: simple_Dim: ajout de l'attribut 'is_union_for'
        self.is_union_for = []

# mpmoine_future_modif: liste des suffixes de noms de variables reperant un ou plusieurs niveaux pression
# List of multi and single pressure level suffixes for which we want the union/zoom axis mecanism turned on
# For not using union/zoom, set 'use_union_zoom' to False in lab settings

# SS : le jeu plev7c est un jeu de couches du simulateur ISCCP - pas d'interpolation
#multi_plev_suffixes=set(["10","19","23","27","39","3","3h","4","7c","7h","8","12"])
multi_plev_suffixes=set(["10","19","23","27","39","3","3h","4",     "7h","8","12"])

# SS : les niveaux 220, 560 et 840 sont des couches du simulateur ISCCP - pas d'interpolation
#single_plev_suffixes=set(["1000","200","220","500","560","700","840","850","100"])
single_plev_suffixes=set(["1000","200",      "500",      "700",      "850","100"])

ambiguous_mipvarnames=None

# 2 dicts for processing home variables
# mpmoine_last_modif: vars.py: spid2label et tmid2label ne sont plus utilises
# 2 dicts and 1 list for processing extra variables
dims2shape={}
dim2dimid={}
dr_single_levels=[]
stdName2mipvarLabel={}

# mpmoine_last_modif:read_homeVars_list: fonction modifiee pour accepter des extra_Tables
def read_homeVars_list(hmv_file,expid,mips,dq,path_extra_tables=None):
    """
    A function to get HOME variables that are not planned in the CMIP6 DataRequest but 
    the lab want to outpuut anyway
    
    Args:
      hmv_file (string) : a text file containing the list of home variables
      expid (string) : if willing to filter on a given experiment 
      mips (string)  : if willing to filter on  given mips
      path_extra_tables (string): path where to find extra Tables. Mandatory only if 
                                  there is'extra' lines in list of home variables.
    
    Returns:
      A list of 'simplified CMOR variables'
    """
    #
    # File structure: name of attributes to read, number of header line 
    home_attrs=['type','label','modeling_realm','frequency','mipTable','temporal_shp','spatial_shp','experiment','mip']
    skip=3
    if not os.path.exists(hmv_file): sys.exit("Abort: file for home variables does not exist: "+hmv_file)
    # Read file
    with open(hmv_file,"r") as fp:
        data=fp.readlines()
    # Build list of home variables
    homevars=[]
    extravars=[]
    for line in data[skip:]:  
        line_split=line.split(';')
        # get the Table full name 
        table=line_split[4].strip(' ')
        # overwrite  5th column with table name without prefix
        if table!='NONE': 
            if '_' not in table: sys.exit("Abort: a prefix is expected in extra Table name: "+table)
            line_split[4]=table.split('_')[1]
        hmv_type=line_split[0].strip(' ')
        if hmv_type!='extra':       
            home_var=simple_CMORvar()
            cc=-1
            for col in line_split:
                ccol=col.lstrip(' ').rstrip('\n\t ')
                if ccol!='': 
                    cc+=1
                    setattr(home_var,home_attrs[cc],ccol)
            home_var.label_with_area=home_var.label
            if hmv_type=='perso':
                home_var.mip_era='PERSO'
                # mpmoine_future_modif:read_homeVars_list: valorisation de home_var.label_without_psuffix
                home_var.label_without_psuffix=home_var.label
            if home_var.mip!="ANY":
                if home_var.mip in mips:
                    if home_var.experiment!="ANY":
                         if home_var.experiment==expid: homevars.append(home_var)
                    else: 
                        homevars.append(home_var)
            else:
                if home_var.experiment!="ANY":
                    if home_var.experiment==expid: homevars.append(home_var)
                else: 
                    homevars.append(home_var)
        else:
            extra_vars=read_extraTable(path_extra_tables,table,dq,printout=False)
            extravars.extend(extra_vars)    
    print "Number of 'cmor' and 'perso' among home variables: ",len(homevars)
    print "Number of 'extra' among home variables: ",len(extravars)
    homevars.extend(extravars) 
    return homevars 

# mpmoine_last_modif:read_extraTable: nouvelle fonction pour lire les extra_Tables
def read_extraTable(path,table,dq,printout=False):
    """
    A function to get variables contained in an EXTRA Table that are is planned in the CMIP6 DataRequest but 
    the lab want to output anyway. EXTRA Table is expected in JSON format, conform with the CMOR3 convention.
    
    Args:
      path (string) : the path where the extra table are located (must include the table name prefix, if any).
      table (string): table name (with its prefix, e.g. 'CMIP6_Amon', 'PRIMAVERA_Oday'). 
                      Table prefix, if present, is supposed to correspond to : '<mip_era>_'.
      printout (boolean,optional) : enhanced verbosity
    
    Returns:
      A list of 'simplified CMOR variables'
    """
    #
    if not dims2shape:
        for sshp in dq.coll['spatialShape'].items:
            dims2shape[sshp.dimensions]=sshp.label
        # mpmoine_future_modif:dims2shape: ajout a la main des correpondances dims->shapes Primavera qui ne sont pas couvertes par la DR
        # mpmoine_note: attention, il faut mettre a jour dim2shape a chaque fois qu'une nouvelle correpondance est introduite
        # mpmoine_note: attention, dans les extra-Tables
        dims2shape['longitude|latitude|height100m']='XY-na'
        # mpmoine_note: provisoire, XY-P12 juste pour exemple
        dims2shape['longitude|latitude|plev12']='XY-P12'
        # mpmoine_zoom_modif:dims2shape:: ajout de XY-P23 qui a disparu de la DR-00.00.04 mais est demande dans les tables Primavera
        dims2shape['longitude|latitude|plev23']='XY-P23'
        # mpmoine_zoom_modif:dims2shape:: ajout de XY-P10 qui n'est pas dans la DR mais demande dans les tables Primavera
        dims2shape['longitude|latitude|plev10']='XY-P10'
    #
    if not dim2dimid:
        for g in dq.coll['grids'].items:
            dim2dimid[g.label]=g.uid
    #
    # mpmoine_correction:read_extraTable: Solution de Martin Juckes du 04/05/2017 en utilisant cids necessaire a partir de la version 01.00.08 => plus besoin de la fonction 'cids2singlev'
    if not dr_single_levels:
        for struct in dq.coll['structure'].items:
            spshp = dq.inx.uid[ struct.spid ]
            if spshp.label=="XY-na" and 'cids' in struct.__dict__:
                 if  struct.cids[0] != '':    ## this line is needed prior to version 01.00.08.
                    c = dq.inx.uid[ struct.cids[0] ]
                    #if c.axis == 'Z': # mpmoine_note: non car je veux dans dr_single_levels toutes les dimensions singletons (ex. 'typenatgr'), par seulement les niveaux
                    dr_single_levels.append(c.label)
        # other single levels in extra Tables, not in DR
        # mpmoine: les ajouts ici correspondent  aux single levels Primavera.
        other_single_levels=['height50m','p100']
        dr_single_levels.extend(other_single_levels)
    #
    extravars=[]
    dr_slevs=dr_single_levels
    mip_era=table.split('_')[0]
    json_table=path+"/"+table+".json"
    json_coordinate=path+"/"+mip_era+"_coordinate.json"
    if not os.path.exists(json_table): sys.exit("Abort: file for extra Table does not exist: "+json_table)
    tbl=table.split('_')[1]
    with open(json_table,"r") as jt:
        json_tdata=jt.read()
        tdata=json.loads(json_tdata)
        # mpmoine_correction:read_extraTable: read_extraTable: ajout de precautions 'NOT-SET' pour certains attributs pour eviter les chaines vides qui font planter XIOS (">  <")
        for k,v in tdata["variable_entry"].iteritems(): 
            extra_var=simple_CMORvar()
            extra_var.type='extra'
            extra_var.mip_era=mip_era
            extra_var.label=v["out_name"].strip(' ')
            extra_var.stdname=v["standard_name"].strip(' ')
            extra_var.long_name=v["long_name"].strip(' ')
            extra_var.stdunits=v["units"].strip(' ')
            extra_var.modeling_realm=v["modeling_realm"].strip(' ')
            extra_var.frequency=table2freq[tbl][1]
            extra_var.mipTable=tbl
            extra_var.cell_methods=v["cell_methods"].strip(' ')
            extra_var.cell_measures=v["cell_measures"].strip(' ')
            extra_var.positive=v["positive"].strip(' ')
            prio=mip_era.lower()+"_priority"
            extra_var.Priority=float(v[prio])
            # Tranlate full-dimensions read in Table (e.g. "longitude latitude time p850")
            # into DR spatial-only dimensions (e.g. "longitude|latitude")
            dims=(v["dimensions"]).split(" ")
            # get the index of time dimension to supress, if any
            inddims_to_sup=[]
            ind_time=[]
            dsingle=None
            for d in dims:
                if "time" in d:
                    dtime=d
                    inddims_to_sup.append(dims.index(dtime))  
                    ind_time=[dims.index(dtime)]
                # get the index of single level to suppress, if any
                for sl in dr_slevs:
                    if d==sl: 
                        dsingle=d
                        inddims_to_sup.append(dims.index(dsingle))      
            # supress dimensions corresponding to time and single levels
            dr_dims=[d for i,d in enumerate(dims) if i not in inddims_to_sup]
            # supress only the dimension corresponding to time
            all_dr_dims=[d for i,d in enumerate(dims) if i not in ind_time]
            # rewrite dimension with DR convention
            drdims=""
            for d in dr_dims:
                if drdims: 
                    drdims=drdims+"|"+d
                else:
                    drdims=d
            if  dims2shape.has_key(drdims):
                extra_var.spatial_shp=dims2shape[drdims]
            else:
                # mpmoine_note: provisoire, on devrait toujours pouvoir associer une spatial shape a des dimensions.
                # mpmoine_note: Je rencontre ce cas pour l'instant avec les tables Primavera ou 
                # mpmoine_note: on a "latitude|longitude" au lieu de "longitude|latitude"
                print "Warning: spatial shape corresponding to ",drdims,"for variable",v["out_name"],\
                      "in Table",table," not found in DR."
            # list of spatial dimension identifiers
            # mpmoine_future_modif:read_extraTable: introduction de extra_var.sdims, ajout lecture des dimensions dans 
            # mpmoine_future_modif:read_extraTable: une table de coordinates quand pas trouvees dans la DR
            dr_dimids=[]
            for d in all_dr_dims:
                if dim2dimid.has_key(d):
                    dr_dimids.append(dim2dimid[d])
                    extra_dim=get_simpleDim_from_DimId(dim2dimid[d],dq)
                    extra_var.sdims.update({extra_dim.label:extra_dim})
                else:
                    extra_sdim=simple_Dim()
                    with open(json_coordinate,"r") as jc:
                        json_cdata=jc.read()
                        cdata=json.loads(json_cdata)
                        extra_sdim.label     =d
                        extra_sdim.stdname   =cdata["axis_entry"][d]["standard_name"]
                        extra_sdim.units     =cdata["axis_entry"][d]["units"]
                        extra_sdim.long_name =cdata["axis_entry"][d]["long_name"]
                        extra_sdim.out_name  =cdata["axis_entry"][d]["out_name"]
                        extra_sdim.positive  =cdata["axis_entry"][d]["positive"]
                        string_of_requested=""
                        for ilev in cdata["axis_entry"][d]["requested"]:
                            string_of_requested=string_of_requested+" "+ilev
                        extra_sdim.requested =string_of_requested.rstrip(" ") # values of multi vertical levels
                        extra_sdim.value     =cdata["axis_entry"][d]["value"] # value of single vertical level
                    extra_var.sdims.update({extra_sdim.label:extra_sdim})
                    print "Info: dimid corresponding to ",d,"for variable",v["out_name"],\
                          "in Table",table," not found in DR => read it in extra coordinates Table: ", extra_sdim.stdname,extra_sdim.requested
            # mpmoine_future_modif: read_extraTable: suppression de extra_var.dimids -> elargi avec extra_var.sdims
            # mpmoine_future_modif:read_extraTable: on renseigne l'attribut label_without_psuffix (doit etre fait apres la valorisation de sdims)
            extra_var.label_without_psuffix=Remove_pSuffix(extra_var,multi_plev_suffixes,single_plev_suffixes,realms='atmos aerosol atmosChem')
                
            extravars.append(extra_var)
    if printout: 
        print "Info: Number of variables in extra tables ",table,": ",len(extravars)
    return extravars 

def get_SpatialAndTemporal_Shapes(cmvar,dq):
    # mpmoine_last_modif:get_SpatialAndTemporal_Shapes: le try/except n'etait pas la bonne solution
    spatial_shape=False
    temporal_shape=False
    if cmvar.stid=="__struct_not_found_001__":
        if print_DR_errors :
            print "Warning: stid for ",cmvar.label," in table ",cmvar.mipTable," is a broken link to structure in DR: ", cmvar.stid
    else:
        for struct in dq.coll['structure'].items:
            if struct.uid==cmvar.stid: 
                 spatial_shape=dq.inx.uid[struct.spid].label
                 temporal_shape=dq.inx.uid[struct.tmid].label
    if print_DR_errors :
        if not spatial_shape: 
            print "Warning: spatial shape for ",cmvar.label," in table ",cmvar.mipTable," not found in DR."
        if not temporal_shape : 
            print "Warning: temporal shape for ",cmvar.label," in table ",cmvar.mipTable," not found in DR."
    return [spatial_shape,temporal_shape]

# mpmoine_last_modif: process_homeVars: argument supplementaire 'path_extra_tables' et expid au lieu de lset
def process_homeVars(lset,mip_vars_list,dq,expid=False,printout=False):
    printmore=False
    # Read HOME variables
    home_vars_list=read_homeVars_list(lset['listof_home_vars'],
                                     expid,lset['mips'],dq,lset['path_extra_tables'])
    for hv in home_vars_list: 
        hv_info={"varname":hv.label,"realm":hv.modeling_realm,
                 "freq":hv.frequency,"table":hv.mipTable}
        #if printout : print hv_info
        if hv.type=='cmor':
            # Complement each HOME variable with attributes got from 
            # the corresponding CMOR variable (if exist)
            updated_hv=get_corresp_CMORvar(hv,dq)
            if(updated_hv):
                already_in_dr=False
                for cmv in mip_vars_list:
                    matching=(cmv.label==updated_hv.label and \
                              cmv.modeling_realm==updated_hv.modeling_realm and \
                              cmv.frequency==updated_hv.frequency and \
                              cmv.mipTable==updated_hv.mipTable and \
                              cmv.temporal_shp==updated_hv.temporal_shp and \
                              cmv.spatial_shp==updated_hv.spatial_shp  )
                    if matching: already_in_dr=True

                # Corresponding CMOR Variable found 
                if not already_in_dr:
                    # Append HOME variable only if not already
                    # selected with the DataRequest
                    if printmore: print "Info:",hv_info,\
                       "HOMEVar is not in DR."\
                       " => Taken into account."
                    mip_vars_list.append(updated_hv)
                else:
                    if printmore:
                        print "Info:",hv_info,\
                            "HOMEVar is already in DR." \
                            " => Not taken into account."
            else:
                if printout:
                    print "Error:",hv_info,\
                        "HOMEVar announced as cmor but no corresponding "\
                        " CMORVar found => Not taken into account."
                    dr2xml_error("Abort: HOMEVar is cmor but no corresponding"\
                                 " CMORVar found.")
        elif hv.type=='perso':
            # Check if HOME variable anounced as 'perso' is in fact 'cmor'
            is_cmor=get_corresp_CMORvar(hv,dq)
            if not is_cmor:
                # Check if HOME variable differs from CMOR one only by shapes
                has_cmor_varname=any([ cmvar.label==hv.label for
                                       cmvar in dq.coll['CMORvar'].items])
                #hasCMORVarName(hv)
                if has_cmor_varname:
                    if printout:
                        print "Warning:",hv_info,"HOMEVar is anounced "\
                            " as perso, is not a CMORVar, but has a cmor name." \
                            " => Not taken into account."
                    dr2xml_error("Abort: HOMEVar is anounced as perso,"\
                                     " is not a CMORVar, but has a cmor name.")
                else:
                    if printmore: print "Info:",hv_info,\
                       "HOMEVar is purely personnal. => Taken into account."
                    mip_vars_list.append(hv)
            else:
                if printout:
                    print "Error:",hv_info,"HOMEVar is anounced as perso,"\
                        " but in reality is cmor => Not taken into account."
                dr2xml_error("Abort: HOMEVar is anounced as perso but "\
                                 "should be cmor.")
        # mpmoine_last_modif: process_homeVars: ajout du cas type='extra'
        elif hv.type=='extra':
            if hv.Priority<=lset["max_priority"]:
                if printmore: print "Info:",hv_info,"HOMEVar is read in an extra Table with priority " \
                               ,hv.Priority," => Taken into account."
                mip_vars_list.append(hv)
        else:
            if printout:
                print "Error:",hv_info,"HOMEVar type",hv.type,\
                    "does not correspond to any known keyword."\
                    " => Not taken into account."
            dr2xml_error("Abort: unknown type keyword provided "\
                         "for HOMEVar %s:"%`hv_info`)

def get_corresp_CMORvar(hmvar,dq):
    collect=dq.coll['CMORvar']
    count=0
    for cmvar in collect.items:
        # Consider case where no modeling_realm associated to the
        # current CMORvar as matching anymay. 
        # mpmoine_TBD: A mieux gerer avec les orphan_variables ?
        match_label=(cmvar.label==hmvar.label)
        match_freq=(cmvar.frequency==hmvar.frequency)
        match_table=(cmvar.mipTable==hmvar.mipTable)
        match_realm=(hmvar.modeling_realm in cmvar.modeling_realm.split(' '))
        empty_realm=(cmvar.modeling_realm=='') 
        matching=( match_label and match_freq and match_table and \
                   (match_realm or empty_realm) )
        if matching: 
            same_shapes=(get_SpatialAndTemporal_Shapes(cmvar,dq)==\
                         [hmvar.spatial_shp,hmvar.temporal_shp])
            if same_shapes:
                count+=1
                cmvar_found=cmvar
            else: 
                print "Error: ",[hmvar.label,hmvar.mipTable],\
                    "HOMEVar: Spatial and Temporal Shapes specified "\
                    "DO NOT match CMORvar ones." \
                    " -> Provided:",[hmvar.spatial_shp,hmvar.temporal_shp],\
                    'Expected:',get_SpatialAndTemporal_Shapes(cmvar,dq)
    if count==1: 
        complement_svar_using_cmorvar(hmvar,cmvar_found,dq,None)
        return hmvar
    return False

def complement_svar_using_cmorvar(svar,cmvar,dq,sn_issues):
    """ 
    The label for SVAR will be suffixed by an area name it the 
    MIPvarname is ambiguous for that

    Used by get_corresp_CMORvar and by select_CMORvars_for_lab
    """
    global ambiguous_mipvarnames
    if ambiguous_mipvarnames is None :
        ambiguous_mipvarnames=analyze_ambiguous_MIPvarnames(dq)
        
    # mpmoine_last_modif: spid2label et tmid2label ne sont plus utilises

    # mpmoine_future_modif:complement_svar_using_cmorvar: reorganisation des lignes de code

    # Get information form CMORvar
    svar.frequency = cmvar.frequency.rstrip(' ')
    svar.mipTable = cmvar.mipTable.rstrip(' ')
    svar.Priority= cmvar.defaultPriority
    svar.positive = cmvar.positive.rstrip(' ')
    svar.modeling_realm = cmvar.modeling_realm.rstrip(' ')
    svar.label = cmvar.label.rstrip(' ')
    [svar.spatial_shp,svar.temporal_shp]=get_SpatialAndTemporal_Shapes(cmvar,dq)
    svar.cmvar=cmvar

    # Get information from MIPvar
    # mpmoine_next_modif:complement_svar_using_cmorvar: gestion d'exception pour l'acces a la 'mipvar'
    try:
        mipvar = dq.inx.uid[cmvar.vid]
        svar.label_without_area=mipvar.label.rstrip(' ')
        # mpmoine_correction:complement_svar_using_cmorvar: le long_name doit etre le title de la CMORvar et non pas de la MIPvar
        #TBS# svar.long_name = mipvar.title
        svar.long_name = cmvar.title.rstrip(' ')
        if mipvar.description :
            svar.description = mipvar.description.rstrip(' ')
        else:
            svar.description = mipvar.title
        svar.stdunits = mipvar.units.rstrip(' ')
        sn=None
        try :
            sn=dq.inx.uid[mipvar.sn]
        except:
            pass
            #print "Issue accessing sn for %s %s!"%(cmvar.label,cmvar.mipTable)
        if sn:
            if sn._h.label == 'standardname':
                svar.stdname = sn.uid.rstrip(' ')
                #svar.stdunits = stdname.units
                #svar.description = stdname.description
            elif sn._h.label == 'remarks' :
                svar.stdname = sn.uid.rstrip(' ')
                if sn_issues is not None and svar.stdname=="missing" or 'pending' in svar.stdname :
                    if svar.stdname not in sn_issues : sn_issues[svar.stdname]=set()
                    sn_issues[svar.stdname].add(svar.label)
                    #print "for var %s, sn is %s"%(svar.label,svar.stdname)
            else:
                print "for var %s, sn._h.label=%s"%(svar.label,sn._h.label)
        else :
            # If CF standard name is NOK, let us use MIP variables attributes
            svar.stdname = mipvar.label.rstrip(' ')
            if print_DR_stdname_errors: 
                print "DR Error: issue with stdname for "+svar.label,"in",svar.mipTable," => take the MIPvar label instead."
    except:
        if print_DR_errors: 
            print "DR Error: issue with MIPvar for "+svar.label," => no label_without_area, long_name, stdname, description and units derived."
    #
    # Get information form Structure
    st=None
    try :
        st=dq.inx.uid[cmvar.stid]
    except :
        if print_DR_errors :
            print "DR Error: issue with stid for",svar.label, "in Table ",svar.mipTable,"  => no cell_methods, cell_measures, dimids and sdims derived."
    if st is not None :
        svar.struct=st
        try :
            svar.cm=dq.inx.uid[st.cmid].cell_methods
            svar.cell_methods=dq.inx.uid[st.cmid].cell_methods.rstrip(' ')
        except:
            if print_DR_errors: print "DR Error: issue with cell_method for "+st.label
            #TBS# svar.cell_methods=None
        try :
            svar.cell_measures=dq.inx.uid[cmvar.stid].cell_measures.rstrip(' ')
        except:
            if print_DR_errors: print "DR Error: Issue with cell_measures for "+`cmvar`
        # mpmoine_last_modif:complement_svar_using_cmorvar: on affecte ici svar.dimids (avant: dans create_xios_field_ref)
        # mpmoine_last_modif:complement_svar_using_cmorvar: provisoire, pour by-passer le cas d'une CMORvar qui n'a pas de structure associee ('dreqItem_remarks')
        # mpmoine_future_modif:complement_svar_using_cmorvar: on ne recherche les dimids que si on a pas affaire a une constante
        if svar.spatial_shp!="na-na":
            spid=None
            try:
                spid=dq.inx.uid[svar.struct.spid]
            except:
                if print_DR_errors :
                        print "DR Error: issue with spid for ",svar.label, "in Table ",svar.mipTable, " => no sdims derived."
                dimids=None
            if spid is not None :
                try:
                    # mpmoine_future_modif:complement_svar_using_cmorvar: suppression de svar.dimids -> elargi avec svar.sdims
                    dimids=spid.dimids
                except:
                    if print_DR_errors :
                        print "DR Error: issue with dimids for ",svar.label, "in Table ",svar.mipTable, " => no sdims derived."
                if dimids is not None :
                    # mpmoine_future_modif:complement_svar_using_cmorvar: on rajoute les single levels dans le traitement des dimensions (dimids->all_dimids)
                    all_dimids=dimids
                    # mpmoine_correction: Solution de Martin Juckes du 04/05/2017 en utilisant cids necessaire a partir de la version 01.00.08
                    if 'cids' in svar.struct.__dict__:
                        cids=svar.struct.cids
                        # when cids not empty, cids=('dim:p850',) or ('dim:typec4pft', 'dim:typenatgr') for e.g.; when empty , cids=('',).
                        if cids[0]!='':  ## this line is needed prior to version 01.00.08.
                            all_dimids+=cids
                    # mpmoine_future_modif:complement_svar_using_cmorvar: on rajoute les single levels dans le traitement des dimensions (dimids->all_dimids)  
                    for dimid in all_dimids:
                        # mpmoine_future_modif:complement_svar_using_cmorvar: on valorise svar.sdims avec la fonction get_simpleDim_from_DimId
                        sdim=get_simpleDim_from_DimId(dimid,dq)
                        svar.sdims.update({sdim.label:sdim})

    area=cellmethod2area(svar.cell_methods) 
    if area : 
        ambiguous=any( [ svar.label == alabel and svar.modeling_realm== arealm 
                   for (alabel,(arealm,lmethod)) in ambiguous_mipvarnames ])
        if ambiguous :
            # Special case for a set of land variables
            if not (svar.modeling_realm=='land' and svar.label[0]=='c'):
                # mpmoine_correction:complement_svar_using_cmorvar: la levee d'ambiguite par ajour de "_land" par ex., ne doit pas impacter le svar.label
                # mpmoine_correction:complement_svar_using_cmorvar: sinon le "_land " se retrouve dans le nom du fichier netcdf
                #TBS# svar.label=svar.label+"_"+area
                svar.label_non_ambiguous=svar.label+"_"+area
    # mpmoine_future_modif:complement_svar_using_cmorvar: on renseigne l'attribut label_without_psuffix (doit etre fait apres la valorisation de sdims)
    # mpmoine_further_zoom_modif:complement_svar_using_cmorvar: deplacement de Remove_pSuffix apres la levee d'ambiguite 'where something' (verifie: aucune des variables ambigues n'est demandee en plev)
    # removing pressure suffix must occur after raising ambuguities (add of area suffix) because this 2 processes cannot be cummulate at this stage. 
    # this is acceptable since none of the variables requeted on pressure levels have ambiguous names.
    svar.label_without_psuffix=Remove_pSuffix(svar,multi_plev_suffixes,single_plev_suffixes,realms='atmos aerosol atmosChem')
    #
    # Fix type and mip_era
    svar.type='cmor'
    #mpm_last_modif:complement_svar_using_cmorvar: mip_era='CMIP6' dans le cas CMORvar
    svar.mip_era='CMIP6'

# momoine_future_modif: nouvelle fonction get_simpleDim_from_DimId utilisee par complement_svar_using_cmorvar et read_extra_Tables
def get_simpleDim_from_DimId(dimid,dq):
    sdim=simple_Dim()
    d=dq.inx.uid[dimid]
    sdim.label=d.label
    sdim.positive=d.positive
    sdim.requested=d.requested 
    sdim.value=d.value
    try :
        sdim.stdname=dq.inx.uid[d.standardName].uid
    except:
        if print_DR_stdname_errors : print "Issue with standardname for dimid %s"%dimid
        sdim.stdname="No_std_name"
    sdim.long_name=d.title
    sdim.out_name=d.altLabel
    sdim.units=d.units
    sdim.bounds=d.bounds
    return sdim

# mpmoine_future_modif: nouvelle fonction Remove_pSuffix
def Remove_pSuffix(svar,mlev_sfxs,slev_sfxs,realms):
    #
    # remove suffixes only if both suffix of svar.label *and* suffix of one of the svar.dims.label  match the search suffix
    # to avoid truncation of variable names like 'ch4' requested on 'plev19', where '4' does not stand for a plev set
    #
    # mpmoine_zoom_modif:Remove_pSuffix: correction de la methode de suppression du suffixe de pression (corrige notamment ta23 -> ta2, 3 etant dans la liste des suffixes)
    import re
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    #
    # mpmoine_correction:write_xios_file_def:Remove_pSuffix: suppression des terminaisons en "Clim" le cas echant
    split_label=svar.label.split("Clim")
    label_out=split_label[0]
    #
    svar_realms=set(svar.modeling_realm.split())
    valid_realms=set(realms.split())
    if svar_realms.intersection(valid_realms):
        mvl=r.match(label_out)
        if mvl and any(label_out.endswith(s) for s in mlev_sfxs.union(slev_sfxs)):
            for sdim in svar.sdims.values(): 
                mdl=r.match(sdim.label)
                if mdl and mdl.group(2)==mvl.group(2): 
                     label_out=mvl.group(1)
    return label_out

def cellmethod2area(method) :
    """
    Analyze METHOD to identify if its part related to area includes 
    some key words which describe given area types
    """
    if method is None                 : return None
    if "where floating_ice_shelf"     in method : return "fisf"
    if "where grounded_ice_shelf"     in method : return "gisf"
    if "where snow over sea_ice area" in method : return "sosi"
    if "where ice_free_sea over sea " in method : return "ifs"
    if "where land"         in method : return "land"
    if "where sea_ice"      in method : return "si"
    if "where sea"          in method : return "sea"
    if "where snow"         in method : return "snow"
    if "where cloud"        in method : return "cloud"
    if "where landuse"      in method : return "lu"
    if "where ice_shelf"    in method : return "isf"

def analyze_ambiguous_MIPvarnames(dq):
    """
    Return the list of MIP varnames whose list of CMORvars for a single realm 
    show distinct values for the area part of the cell_methods
    """
    # Compute a dict which keys are MIP varnames and values = list 
    # of CMORvars items for the varname
    d=dict()
    for v in dq.coll['var'].items :
        if v.label not in d : d[v.label]=[]
        refs=dq.inx.iref_by_sect[v.uid].a['CMORvar']
        for r in refs :
            d[v.label].append(dq.inx.uid[r])
            #if v.label=="prra" : print "one prra"
    #print "d[prra]=",d["prra"]
    # Replace dic values by dic of cell_methods
    for vlabel in d:
        if len(d[vlabel]) > 1 :
            cvl=d[vlabel]
            d[vlabel]=dict()
            for cv in cvl: 
                st=dq.inx.uid[cv.stid]
                try :
                    cm=dq.inx.uid[st.cmid].cell_methods
                    # mpmoine_a_verifier: certaines de ces chaines n existent pas dans les cell_methods de la DR
                    cm1=cm.replace("time: mean","").replace("time: point","").\
                        replace(" within years  over years","") .\
                        replace('time: maximum within days  over days','').\
                        replace('time: minimum within days  over days','').\
                        replace('time: minimum','').\
                        replace('time: maximum','').\
                        replace('with samples ','')
                    realm=cv.modeling_realm
                    if realm=="ocean" or realm=="ocnBgchem" :
                        cm1=cm1.replace("area: mean where sea ","")
                    #if realm=='land':
                    #    cm1=cm1.replace('area: mean where land ','')
                    if True or "area:" in cm1 :
                        cm2=cm1 #.replace("area:","")
                        if realm not in d[vlabel]:
                            d[vlabel][realm] =[]
                        if cm2 not in d[vlabel][realm] :
                            d[vlabel][realm].append(cm2)
                        #if vlabel=="prra" : 
                        #    print "cm2=",cm2, d[vlabel]
                except : 
                    pass
                    #print "No cell method for %s %s"%(st.label,cv.label)
        else : d[vlabel]=None
    #for l in d : print l,d[l]
    #print "d[prra]=",d["prra"]
    #sd=d.keys() ; sd.sort()
    #for var in sd :
    #    if d[var] and any( [ len(l) > 1 for l in d[var].values() ]) :
    #        print "%20s %s"%(var,`d[var]`)
    #        pass
    # Analyze ambiguous cases regarding area part of the cell_method
    ambiguous=[]
    for vlabel in d:
        if d[vlabel]:
            #print vlabel,d[vlabel]
            for realm in d[vlabel] :
                if len(d[vlabel][realm])>1 and \
                   any([ "area" in cm for cm in d[vlabel][realm] ]):
                    ambiguous.append(( vlabel,(realm,d[vlabel][realm])))
    return ambiguous


def get_simplevar(dq,label,table):
    """ 
    Returns 'simplified variable' for a given CMORvar label and table
    """
    svar = simple_CMORvar()
    collect=dq.coll['CMORvar']
    psvar=None
    for cmvar in collect.items:
        if cmvar.mipTable==table and cmvar.label==label :
            psvar=cmvar
            break
    if psvar :
        complement_svar_using_cmorvar(svar,cmvar,dq,None)
        return svar
    
