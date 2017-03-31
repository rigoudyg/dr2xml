#!/usr/bin/python

from settings import lab_and_model_settings, simulation_settings, my_cvspath
from dr2xml import select_CMORvars_for_lab, pingFileForRealmsList, generate_file_defs
#
lab_and_model_settings["excluded_vars"]=[]
#


if True :
    context='arpsfx'
    realms=lab_and_model_settings['realms_per_context'][context]
    svars=select_CMORvars_for_lab(lab_and_model_settings, printout=True)
    #pingFileForRealmsList(context,realms,svars,comments=False,exact=False,dummy=True, 
    pingFileForRealmsList(context,realms,svars,comments=" ",exact=False,dummy=True, 
                      prefix=lab_and_model_settings['ping_variables_prefix'],
                      filename='./ping_%s.xml'%context,dummy_with_shape=True)
    generate_file_defs(lab_and_model_settings, simulation_settings,year=2000,context=context,
                   pingfile="./ping_%s.xml"%context, printout=True, 
                   cvs_path=my_cvspath,dummies='include', dirname="./",prefix="outputs/")


if False :
    context='nemo'
    realms=lab_and_model_settings['realms_per_context'][context]
    svars=select_CMORvars_for_lab(lab_and_model_settings, printout=True)
    pingFileForRealmsList(context,realms,svars,comments=" ",exact=False,dummy=True, 
                      prefix=lab_and_model_settings['ping_variables_prefix'],
                      filename='./ping_%s.xml'%context,dummy_with_shape=True)
    generate_file_defs(lab_and_model_settings, simulation_settings,year=2000,context=context,
                   pingfile="./ping_%s.xml"%context, printout=True, 
                   cvs_path=my_cvspath,dummies='include', dirname="./",prefix="outputs/")
