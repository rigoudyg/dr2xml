
# coding: utf-8

## Create ping files based on lab choices

#### When using function cerate_ping_files with argiumnet exact=False, each ping file will adress all variables which realm includes or is included in one of the strings in a realms set  <br><br> e.g for set ['ocean','seaIce'], ping file 'ping_ocean_seaIce.xml' will includes variables which realm is either 'ocean' or 'seaIce' or 'ocean seaIce'

# In[1]:

allrealms=[ ['ocean'], ['seaIce'],['ocnBgchem'], [ 'atmos'], ['land'],['landIce'], ['atmosChem'],[ 'aerosol' ]]


### Lab settings

# In[14]:


# This dictionnary should be the same as the one used for creating file_defs.
# Here , we quoted only those entries useful for creating ping files
settings={
    'mips_CNRM' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
                      'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
    'mips' : {"CMIP6", "AerChemMIP", "C4MIP", "CFMIP", "DAMIP", "DCPP", "FAFMIP", "GeoMIP", "GMMIP", 
              "HighResMIP", "ISMIP6", "LS3MIP", "LUMIP", "OMIP", "PDRMIP", "PMIP", "RFMIP", "ScenarioMIP", 
              "SolarMIP", "VolMIP", "CORDEX", "DynVar", "SIMIP", "VIACSAB", "SPECS", "CCMI", "CMIP5", 
              "CMIP", "DECK"},
    'max_priority' : 3,
    'tierMax'      : 3,
    "ping_variables_prefix" : "CMIP6_",
    # We account for a file listing the variables which the lab does not want to produce 
    # Format : MIP varname as first column, comment lines begin with '#'
    "excluded_vars_file":"/cnrm/est/USERS/senesi/public/CMIP6/data_request/cnrm/excluded_vars.txt",
    "excluded_vars" : None,
    }


                
                
### List of sets of realms for which ping files must be generated

#### Read excluded variables list

# In[15]:

l=[]
if settings["excluded_vars"] is None and settings["excluded_vars_file"] is not None :
    with open(settings["excluded_vars_file"],'r') as fv : varlines=fv.readlines()
    for line in varlines: 
        fields=line.split()
        if len(fields) > 0 : 
            first=fields[0]
            if first[0] != '#' :  l.append(first)
settings["excluded_vars"]=l
                       


### For getting a comprehensive ping file, reset the excluded_var list to None

# In[16]:

settings["excluded_vars"]=[]


# In[17]:

from dr2xml import select_CMORvars_for_lab, pingFileForRealmsList


### Select all variables to consider, based on lab settings

# In[18]:

svars=select_CMORvars_for_lab(settings, printout=True)


### Create ping files

# In[19]:

help(pingFileForRealmsList)


# In[22]:

realms=[ 'atmos', 'land','landIce','atmosChem','aerosol']
pingFileForRealmsList(realms,svars,comments=" ",exact=False,dummy=True,filename='ping_atmos_and_co.xml')
#pingFileForRealmsList(realms,svars,comments="",exact=False,dummy=True,filename='ping_atmos_nocomments.xml')


# In[23]:

pingFileForRealmsList(['ocean','seaIce'],svars,comments=" ",exact=False,dummy=True,filename='ping_ocean_seaice.xml')


# In[24]:

get_ipython().system(u' head -n 5 ping_ocean_seaice.xml')


# In[25]:

for rs in allrealms :
    pingFileForRealmsList(rs,svars,prefix=settings['ping_variables_prefix'],comments=" ",exact=False, dummy=True)


# In[ ]:



