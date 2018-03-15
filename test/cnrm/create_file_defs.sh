#!/bin/bash
#
#
# Create XIOS file_defs for each context described in file in arg3 ,
# for the simulation described by file in arg4
# and accounting for a few other args
#
# Assumes that a full set of xml files is available in current dir,
# including ping_files (named like ping_<context>*.xml)
#
# Output files are named after pattern dr2xml_<context>.xml
#
[ ${setx:-0} -eq 1 ] && echo "Entering create_file_defs.sh" && set -x

dummies=$1 ;  # See dr2xml doc : forbid/skip/include
EXPID=$2 ;  # The value for an attribute 'EXPID' in datafiles
ln -sf $3 lab_and_model_settings_tmp.py ; 
ln -sf $4 simulation_settings_tmp.py ; 
year=$5 ;  # year that will be simulated
enddate=$6 ;   # simulation end date - YYYYMMDD - must be at 00h next day
ncdir=${7:-@IOXDIR@/} ;   # Directory for data output files
print=${8:-1} ;  # Want some reporting ?
homedr="$9" ;  # Filenames for a 'home' data request - optional
path_extra_tables=${10} # Filename for a 'home' data request - optional
#
select=${select:-""} # For debug purpose  : can be "" "on_expt" and "no"
#dummies=include
#
# Set paths for all software components
#
root=$(cd $(dirname $0) ; pwd)
dr2xmlpath=${altdr2xmlpath:-$root}
md5=$(md5sum -b $dr2xmlpath/dr2xml.py | cut -f 1 -d " ")
CMIP6=${CMIP6:-$root/../..}
cvspath=${cvspath:-$CMIP6/externals/CMIP6_CVs}
DRpath=${DRpath:-$CMIP6/externals/DR01.00.21/dreqPy}
#
export PATH=/opt/softs/libraries/GCC5.3.0/git-2.11.0/bin:$PATH 
export GIT_EXEC_PATH=/opt/softs/libraries/GCC5.3.0/git-2.11.0/libexec/git-core
CVtag=cv=$(cd $cvspath ; git describe HEAD ) 

export PYTHONPATH=$dr2xmlpath:$DRpath:$PYTHONPATH
#
# Identify which ping_files are used (according to $(pwd)/iodef.xml)
#
pings=$(grep "ping_.*\.xml" iodef.xml | grep -v "<!--" | sed -r -e 's/.*(ping_.*xml).*/\1/g' | tr "\n" " ")
#
# Create Python script for using dr2xml's generate_file_defs()
#
cat >create_file_defs.tmp.py  <<-EOF
	#!/usr/bin/python
	from lab_and_model_settings_tmp import lab_and_model_settings
	from simulation_settings_tmp import simulation_settings
	from dr2xml import generate_file_defs
	import sys, os, traceback
	#print "* CMIP6_CV commit : "
	#os.system("cd $cvspath ; git log --oneline | head -n 1 | cut -d\  -f 1")
	#print
	#
	if $print=="1" : printout=True
	else : printout=False
	#
	if "$homedr" : 
	  simulation_settings['listof_home_vars']="$homedr"
	if "$path_extra_tables" : 
	  simulation_settings['path_extra_tables']="$path_extra_tables" 
	config=simulation_settings['configuration']
	configuration_triplet=lab_and_model_settings['configurations'][config]
	config_unused=configuration_triplet[2]
	exp_unused=simulation_settings.get('unused_contexts',[])
	#print "exp_unsued=",exp_unused," config_unused=",config_unused
	contexts=[ c for c in lab_and_model_settings['realms_per_context'] \
	  if c not in exp_unused and c not in config_unused ]
	for context in contexts :
	    ok=generate_file_defs(lab_and_model_settings,
	                       simulation_settings,
	                       year       = $year,
	                       enddate    = "$enddate",
	                       context    = context,
	                       pingfiles  = "$pings",
	                       printout   = $print, 
	                       cvs_path   = "${cvspath}/",
	                       dummies    = "$dummies",
	                       dirname    = "./",
	                       prefix     = "$ncdir",
                               attributes = [ ("EXPID","$EXPID") , ("CMIP6_CV_version", "$CVtag"), ("dr2xml_md5sum", "$md5") ],
                               select     = "$select"
                               )
	#if not ok : sys.exit(1)
	EOF


[[ $(uname -n) == beaufix* ]] && module load python/2.7.5-2 2>/dev/null
[[ $(uname -n) == prolix*  ]] && module load python/2.7.5   2>/dev/null
python create_file_defs.tmp.py
ret=$?
rm create_file_defs.tmp.py simulation_settings_tmp.py lab_and_model_settings_tmp.py
exit $ret
