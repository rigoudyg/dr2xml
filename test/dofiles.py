#!/usr/bin/python

from settings import lab_and_model_settings, simulation_settings, my_cvspath
from dr2xml import select_CMORvars_for_lab, pingFileForRealmsList, generate_file_defs
#
lab_and_model_settings["excluded_vars"]=[]
#
svars=select_CMORvars_for_lab(lab_and_model_settings, printout=True)
context='arpsfx'
realms=lab_and_model_settings['realms_per_context'][context]
pingFileForRealmsList(context,realms,svars,comments=" ",exact=False,dummy=True, 
                      prefix=lab_and_model_settings['ping_variables_prefix'],
                      filename='./ping_arpsfx.xml',dummy_with_shape=True)

generate_file_defs(lab_and_model_settings, simulation_settings,year=2000,context='arpsfx',
                   pingfile="./ping_arpsfx.xml", printout=True, 
                   cvs_path=my_cvspath,dummies='include', dirname="./",prefix="outputs/")

if False : generate_file_defs(lab_and_model_settings, simulation_settings,year=2000,context='nemo',
                   pingfile="./ping_nemo.xml", printout=True, 
                   cvs_path=my_cvspath,dummies='include', dirname="./",prefix="outputs/")
