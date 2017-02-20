print_DR_errors=False

#A class for unifying CMOR vars and home variables
class simple_CMORvar(object):
    def __init__(self):
        self.type           = 'perso' # Default case is HOMEvar.
        self.modeling_realm = None # Useful for both HOMEvar and CMORvar.
        self.grids          = [""] # Useful for CMORvar and updated HOMEvar.
        self.mipTable       = None # Useful for both HOMEvar and CMORvar.
        self.label          = None # Useful for both HOMEvar and CMORvar.
        self.label_without_area= None # Useful for both HOMEvar and CMORvar.
        self.frequency      = None # Useful for both HOMEvar and CMORvar.
        self.mipTable       = None # Useful for both HOMEvar and CMORvar.
        self.positive       = None # Useful for CMORvar and updated HOMEvar.
        self.description    = None # Useful for CMORvar and updated HOMEvar.
        self.stdname        = None # Useful for CMORvar and updated HOMEvar.
        self.stdunits       = None # Useful for CMORvar and updated HOMEvar.
        self.long_name      = None # Useful for CMORvar and updated HOMEvar.
        self.struct         = None
        self.cell_methods   = None
        #self.cell_measures  = None
        self.spatial_shp    = None # Only useful for HOMEvar.
        self.temporal_shp   = None # Only useful for HOMEvar.
        self.experiment     = None # Only useful for HOMEvar.
        self.mip            = None # Only useful for HOMEvar.
        self.Priority       = 1    # Will be changed using DR if it is a CMORvar
        

ambiguous_mipvarnames=None

# 2 dicts for processing home variables
spid2label={}
tmid2label={}

def read_homeVars_list(hmv_file,expid,mips):
    # File structure: name of attributes to read, number of header line 
    home_attrs=['type','label','modeling_realm','frequency','mipTable','temporal_shp','spatial_shp','experiment','mip']
    skip=3
    # Read file
    with open(hmv_file,"r") as fp:
        data=fp.readlines()
    # Build list of home variables
    homevars=[]
    nhv=0
    for line in data[skip:]:  
        line_split=line.split(';')
        nhv+=1
        home_var=simple_CMORvar()
        cc=-1
        for col in line_split:
            ccol=col.lstrip(' ').rstrip('\n\t ')
            if ccol!='': 
                cc+=1
                setattr(home_var,home_attrs[cc],ccol)
        home_var.label_with_area=home_var.label
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
    return homevars

def get_SpatialAndTemporal_Shapes(cmvar,dq):
    try:
        for struct in dq.coll['structure'].items:
            if struct.uid==cmvar.stid: 
                spatial_shape=spid2label[struct.spid]
                temporal_shape=tmid2label[struct.tmid]
                return [spatial_shape,temporal_shape]
    except:
        print("Error: "+cmvar.label+" "+cmvar.mipTable+\
                     "CMORvar: Structure of CMORvar NOT found!")
        return [False,False]
    print "DR error : No struct found for "+`cmvar`+" in table "+cmvar.mipTable
    return [False,False]

def process_homeVars(lset, sset,mip_vars_list,dq, printout=False):
    # Read HOME variables
    home_vars_list=read_homeVars_list(lset['listof_home_vars'],
                                      sset['experiment_id'],lset['mips'])
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
                    if printout: print "Info:",hv_info,\
                       "HOMEVar is not in the DataRequest."\
                       " => Taken into account."
                    mip_vars_list.append(updated_hv)
                else:
                    if printout:
                        print "Info:",hv_info,\
                            "HOMEVar is already in the DataRequest." \
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
                    if printout: print "Info:",hv_info,\
                       "HOMEVar is purely personnal. => Taken into account."
                    mip_vars_list.append(hv)
            else:
                if printout:
                    print "Error:",hv_info,"HOMEVar is anounced as perso,"\
                        " but in reality is cmor => Not taken into account."
                dr2xml_error("Abort: HOMEVar is anounced as perso but "\
                                 "should be cmor.")
        else:
            if printout:
                print "Error:",hv_info,"HOMEVar type",hv.type,\
                    "does not correspond to any known keyword."\
                    " => Not taken into account."
            dr2xml_error("Abort: unknown type keyword %provided "\
                         "for HOMEVar %s:"%`hv_info`)

def get_corresp_CMORvar(hmvar,dq):
    collect=dq.coll['CMORvar']
    count=0
    for cmvar in collect.items:
        # Consider case where no modeling_realm associated to the
        # current CMORvar as matching anymay. 
        #mpmoine# A mieux gerer avec les orphan_variables ?
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
        complement_svar_using_cmorvar(hmvar,cmvar_found,dq)
        return hmvar
    return False


def complement_svar_using_cmorvar(svar,cmvar,dq):
    """ 
    The label for SVAR will be suffixed by an area name it the 
    MIPvarname is ambiguous for that

    Used by get_corresp_CMORvar and by select_CMORvars_for_lab
    """
    global ambiguous_mipvarnames
    if ambiguous_mipvarnames is None :
        ambiguous_mipvarnames=analyze_ambiguous_MIPvarnames(dq)
        
    global spid2label
    if len(spid2label)==0 :
        for obj in dq.coll['spatialShape'].items: spid2label[obj.uid]=obj.label
        for obj in dq.coll['temporalShape'].items: tmid2label[obj.uid]=obj.label

    svar.frequency = cmvar.frequency
    svar.mipTable = cmvar.mipTable
    svar.Priority= cmvar.defaultPriority
    svar.positive = cmvar.positive
    [svar.spatial_shp,svar.temporal_shp]=get_SpatialAndTemporal_Shapes(cmvar,dq)
    mipvar = dq.inx.uid[cmvar.vid]
    svar.label = cmvar.label
    svar.label_without_area=mipvar.label
    svar.long_name = mipvar.title
    svar.modeling_realm = cmvar.modeling_realm
    if mipvar.description :
        svar.description = mipvar.description
    else:
        svar.description = mipvar.title
    svar.stdunits = mipvar.units
    try :
        st=dq.inx.uid[cmvar.stid]
        #print st.label
        try :
            svar.cm=dq.inx.uid[st.cmid].cell_methods
            svar.cell_methods=dq.inx.uid[st.cmid].cell_methods
        except:
            if print_DR_errors : print "Issue with cell_method for "+st.label
            svar.cell_methods=None
    except :
        if print_DR_errors :
            print "Issue with st.cmid in table % 10s for %s"%(cmvar.mipTable,cmvar.label)
        svar.cell_methods=None
        
    area=cellmethod2area(svar.cell_methods) 
    if area : 
        ambiguous=any( [ svar.label == alabel and svar.modeling_realm== arealm 
                   for (alabel,(arealm,lmethod)) in ambiguous_mipvarnames ])
        if ambiguous :
            # Special case for a set of land variables
            if not (svar.modeling_realm=='land' and svar.label[0]=='c'):
                svar.label=svar.label+"_"+area

    svar.type='cmor'
    stdname=None
    #
    try :
        stdname = dq.inx.uid[mipvar.sn]
    except:
        pass
        #print "Issue accessing sn for %s %s!"%(cmvar.label,cmvar.mipTable)
    if stdname and stdname._h.label == 'standardname':
            svar.stdname = stdname.uid
            #svar.stdunits = stdname.units
            #svar.description = stdname.description
    else :
        # If CF standard name is NOK, let us use MIP variables attributes
        svar.stdname = mipvar.label
    svar.struct=dq.inx.uid[cmvar.stid]


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

