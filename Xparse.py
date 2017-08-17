# coding: utf-8

# Whats' necessary for reading XIOS xml file and process attribute's inheritance for
# being able to request the grid_ref for any valid XIOS 'field' object

# Main useful functions :
#   <opaque>    context = init_context(context_name,printout=False)
#   <ET object>    grid = d2grid(field_id,context,printout=False)

import os, os.path, re, sys
import xml.etree.ElementTree as ET

# Define for each object kind those attributes useful for grid inheritance 
attributes=dict()
attributes['field']=[ 'grid_ref', 'field_ref' ]
attributes['field_definition']=attributes['field']
attributes['field_group']=attributes['field']
attributes['grid']=['axis_ref' , 'domain_ref', 'grid_ref']
attributes['grid_group']=attributes['grid']
attributes['context']=[]
attributes['axis']=['axis_ref']
#attributes['axis_definition']=[]  #attributes['domain_definition']=[]
#attributes['grid_definition']=[]  #attributes['calendar']=[]

# mpmoine_amelioration: ajout de l'argument 'path_parse' a la fonction read_src pour pouvoir lire les context.xml d'Arnaud
def read_src(elt,path_parse,printout=False, level=0, dont_read=[]) :
    """
    Recursively reads the subfiles indicated by tag 'src' in childs of ELT
    """
    childs=[]
    for child in elt :
        if 'src' in child.attrib :
            # mpmoine_amelioration:read_src: ajout de path_parse pour acceder aux context_<X>.xml
            src=child.attrib['src']
            if src[0] != "/" :
                if path_parse != "./" :
                    filen=path_parse+"/"+src
                else :
                    filen=src
            else:
                filen=src
            skip=False
            for prefix in dont_read :
                if os.path.basename(filen)[0:len(prefix)]==prefix :
                    print "Skipping %s"%filen
                    skip=True
            if skip : continue
            # mpmoine_correction: read_src: gestion du type de codage XML pour pouvoir lire les context.xml d'Arnaud
            if printout : print level*"\t"+"Reading %s"%filen
            et=ET.parse(filen).getroot()
            if printout :
                print level*"\t"+"Reading %s, %s=%s"%(filen,et.tag,gattrib(et,'id','no_id'))
            for el in et :
                if printout :
                    print (level+1)*"\t"+"Storing %s in %s id=%s"%(
                        el.tag,child.tag,gattrib(child,'id','no_id'))
                child.append(el)
    for child in elt :
        #print level*"\t"+"Recursing on %s %s"%(child.tag,gattrib(child,'id','no_id'))
        read_src(child,path_parse,printout,level+1,dont_read)

def gattrib(e,attrib_name,default=None):
    if attrib_name in e.attrib : return e.attrib[attrib_name]
    else : return default

def merge_sons(elt,printout=False, level=0):
    """
    Merge all mergeable childs of  ELT based on tag, or
    on tag+id when tag is 'context' or 'field' or '..._group'
    """
    toremove=[]
    # Using a dict with first instance of an elt for each tag (or tag+id)
    bytag=dict()
    tags_to_merge=[ 'context', 'file_definition', 'field_definition',
                    'axis_definition', 'grid_definition' , 'calendar' , 'field' ,
                    'field_group' , 'file_group' ]
    for child in elt :
        if child.tag not in tags_to_merge : continue
        if child.tag not in [ 'context', 'field' ] and '_group' not in child.tag : 
            tag=child.tag
        else :
            if 'id' in child.attrib :
                tag=child.tag+"_"+child.attrib['id']
            else :
                continue # do not merge attributes for anonymous fields
        if tag not in bytag : bytag[tag]=child
        else:
            if child != bytag[tag] : 
                if 'src' in child.attrib : name=child.attrib['src']
                else :
                    if 'id' in child.attrib : name=child.attrib['id']
                    else : name='no_id'
                if (printout) :
                    print level*"\t"+"Moving %s %s content to %s"%( child.tag,name,tag) 
                #
                # Move childs from secondary entry to first entry (brother)
                for sub in child : bytag[tag].append(sub)
                # Update attributes, too 
                for a in child.attrib : bytag[tag].attrib[a]=child.attrib[a]
                toremove.append(child)
    for child in toremove : 
        if printout : print "removing one %s child : %s"%(`elt`,`child`)
        elt.remove(child)
    # Recursion
    for child in elt :
        if printout : print level*"\t"+"%s %s"%(child.tag,child.attrib.get('id','no_id'))
        merge_sons(child,printout,level+1)

def solve_downward(attrib,elt,value=None,printout=False,level=0) :
    """ propagate attribute ATTRIB 's VALUE downward of ELT, 
    setting recursively it for all childs to the parent value or 
    to the value encountered in an intermediate node
    """
    for child in elt :
        value_down=value
        if printout : print level*"\t"+" solving on "+`child`,
        if attrib in attributes.get(child.tag,[]) :
            if attrib not in child.attrib :
                if value is not None :
                    child.attrib[attrib]=value
                    if printout : print " set :"+value
                else:
                    if printout : print " pass"
            else:
                value_down=child.attrib[attrib]
                if printout : print " get :"+value_down
        else:
            if printout : print
        solve_downward(attrib,child,value_down,printout,level+1)

def make_index(elt,index=None,printout=False,level=0):
    """
    Create an index of all elements having an id in ELT childs recursively
    and complement attributes and children of these indexed objects when 
    crossing their id multiple times
    """
    if index is None : index=dict()
    for child in elt :
        if 'id' in child.attrib :
            the_id=child.attrib['id']
            if printout : print level*"\t"+" indexing "+the_id,
            if the_id in index :
                if printout : print " (merging)"
                # Update indexed object with current attributes
                for a in child.attrib : index[the_id].attrib[a]=child.attrib[a]
                # Add child chidlren to indexed objects
                for sub in child :  index[the_id].append(sub)
            else:
                if printout : print " init index"
                index[the_id]=child
        #else:
        #    if printout : print 
    for child in elt :
        make_index(child,index,printout,level+1)
    return(index)

def attrib_by_ref(elt,attrib,index,printout,level):
        """
        Provide ATTRIB value for ELT' id using its references 
        and objects's dict INDEX
        """
        for a in elt.attrib :
            if '_ref' in a :
                refid=elt.attrib[a]
                if printout : print "\n"+(level+1)*"\t"+a+" -> "+refid,
                try :
                    ref=index[refid]
                    if attrib in ref.attrib:
                        rep=ref.attrib[attrib]
                        if printout : print " ---> !! GOT : "+rep+ " !!!"
                        return rep
                    else :
                        rep=attrib_by_ref(ref,attrib,index,printout,level+1)
                        if rep : return rep
                except :
                    if not refid.startswith("dummy_"):
                        print "Error : reference '%s' is invalid"%refid
                        sys.exit(1)

def solve_by_ref(attrib,index,elt,printout=False,level=0) :
    """ 
    Solve remainig attributes by ref, otherwise by default value
    """
    got_one=0
    for child in elt :
        if type(child) != type('') and child.tag != 'variable' :
            if 'id' in child.attrib : name=child.attrib['id']
            else : name=`child`
            if printout : print level*"\t"+attrib+" by_ref on  "+name,
            #
            if child.tag in attributes and attrib in attributes[child.tag] :
                if attrib not in child.attrib :
                    byref=attrib_by_ref(child,attrib,index,printout,level)
                    if byref :
                        #if printout : print ", setting byref to "+byref,
                        child.attrib[attrib]=byref
                        got_one=got_one+1
                    else :
                        if printout : print
                else: 
                    if printout : print ", already set : %s"%child.attrib[attrib]
                got=solve_by_ref(attrib,index,child,printout,level+1)
                got_one=got_one+got
            else: 
                if printout : print " : N/A"
    return got_one
        
def select_context(rootel,context_id):
        for context in rootel :
            if 'id' in context.attrib and context.attrib['id']==context_id :
                return context

# mpmoine_amelioration: ajout de l'argument 'path_parse' a la fonction init_context
def init_context(context_id,path_parse,printout=False):
    # mpmoine_merge_dev2_v0.12:init_context: ajout de "./parse/" pour acceder a iodef.xml
    xmldef=path_parse+"iodef.xml"
    if printout: print "Parsing %s ..."%xmldef,
    rootel=ET.parse(xmldef).getroot()
    # mpmoine_amelioration:init_context: ajout de l'argument 'path_parse' a la fonction read_src
    if printout: print "sourcing files  ...",
    read_src(rootel,path_parse,printout=printout,dont_read=["dr2xml_"])
    merge_sons(rootel,printout)
    rootel=select_context(rootel,context_id)
    if rootel is not None :
        refs=[ "grid_ref", "domain_ref", "axis_ref", "field_ref" ] 
        for ref in refs: 
            solve_downward(ref,rootel,None)
        #ET.dump(rootel)
        index=make_index(rootel,None,printout)
        for ref in refs : 
            while True :
                n=solve_by_ref(ref,index,rootel,printout)
                if printout : print "%d refs solved"%n
                if n==0 : break
        #ET.dump(rootel)
        return (index)
    else:
        print "Xparse::init_context : context %s not found in %s"%(context_id,xmldef)

def id2grid(field_id,index,printout=False) :
    """ 
    Returns the list of Element composing the grid IOXof a field
    """
    if field_id in index : 
        attrib=index[field_id].attrib
        if 'grid_ref' in attrib :
            grid_ref_field_id=attrib['grid_ref']
            if grid_ref_field_id in index :
                return index[grid_ref_field_id] 
            else:
                if printout: print("field %s reference is %s but has no grid"%(field_id,grid_ref_field_id))
        else:
            if printout: print("field %s has no grid_ref"%(field_id))
    else:
        if printout: print("field %s is not known"%field_id)

if False :
    
    nemo=init_context('nemo',False)
    #print nemo.keys()
    grid=id2grid("CMIP6_O18sw",nemo,True)
    print grid.attrib['id'] ; print


    arpsfx=init_context('arpsfx',False)
    grid=id2grid("CMIP6_cdnc",arpsfx,True)
    #grid=None
    if grid is not None: 
        #print "Grid id is :"+grid.attrib['id']
        print ET.tostring(grid);     
        grid_string=ET.tostring(grid)
        new_grid_string=re.sub('axis_ref= *.([\w_])*.','axis_ref="axis_autre"',grid_string)
        print new_grid_string




