
# coding: utf-8

## Create ping files based on lab choices

#### When using function cerate_ping_files with argiumnet exact=False, each ping file will adress all variables which realm includes or is included in one of the strings in a realms set  <br><br> e.g for set ['ocean','seaIce'], ping file 'ping_ocean_seaIce.xml' will includes variables which realm is either 'ocean' or 'seaIce' or 'ocean seaIce'

# In[1]:

allrealms=[ ['ocean'], ['seaIce'],['ocnBgchem'], [ 'atmos'], ['land'],['landIce'], ['atmosChem'],[ 'aerosol' ]]


### Lab settings

# In[2]:


# This dictionnary should be the same as the one used for creating file_defs.
# Here , we quoted only those entries useful for creating ping files
settings={
    'mips' : {'AerChemMIP','C4MIP','CFMIP','DAMIP', 'FAFMIP' , 'GeoMIP','GMMIP','ISMIP6',\
                      'LS3MIP','LUMIP','OMIP','PMIP','RFMIP','ScenarioMIP','CORDEX','SIMIP'},
    'max_priority' : 1,
    'tierMax'      : 3,
    "ping_variables_prefix" : "CMIP6_",
    # We account for a file listing the variables which the lab does not want to produce 
    # Format : MIP varname as first column, comment lines begin with '#'
    "excluded_vars_file":"/cnrm/est/USERS/senesi/public/CMIP6/data_request/cnrm/excluded_vars.txt",
    "excluded_vars" : None,
    }


#### Read excluded variables list

# In[3]:

l=[]
if settings["excluded_vars"] is None and settings["excluded_vars_file"] is not None :
    with open(settings["excluded_vars_file"],'r') as fv : varlines=fv.readlines()
    for line in varlines: 
        fields=line.split()
        if len(fields) > 0 : 
            first=fields[0]
            if first[0] != '#' :  l.append(first)
settings["excluded_vars"]=l
                       


# In[4]:

from dr2xml import select_CMORvars_for_lab, pingFileForRealmsList


### Select all variables to consider, based on lab settings

# In[5]:

svars=select_CMORvars_for_lab(settings, printout=True)


### Create ping files

# In[6]:

help(pingFileForRealmsList)


# In[12]:

realms=[ 'atmos', 'land','landIce','atmosChem','aerosol']
pingFileForRealmsList(realms,svars,comments=" ",exact=False,dummy=True,filename='ping_atmos.xml')
pingFileForRealmsList(realms,svars,comments="",exact=False,dummy=True,filename='ping_atmos_nocomments.xml')


# In[8]:

pingFileForRealmsList(['ocean','seaIce'],svars,comments=" ",exact=False,dummy=True,filename='ping_ocean.xml')


# In[9]:

get_ipython().system(u' head -n 5 ping_ocean.xml')


# In[11]:

for rs in allrealms :
    pingFileForRealmsList(rs,svars,prefix=settings['ping_variables_prefix'],comments=" ",exact=False)


# In[ ]:



