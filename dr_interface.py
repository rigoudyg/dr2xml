#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Interface between the Data Request and dr2xml.
"""


from scope import dreqQuery
import dreq


dq = dreq.loadDreq()
print_DR_errors = True


def get_uid(id=None):
    if id is None:
        return dq.inx.uid
    else:
        return dq.inx.uid[id]


def get_request_by_id_by_sect(id, request):
    return dq.inx.iref_by_sect[id].a[request]


def get_experiment_label(experiment):
    return dq.inx.experiment.label[experiment][0]


def get_collection(collection):
    return dq.coll[collection]


def get_CMORvarId_by_label(label):
    return dq.inx.CMORvar.label[label]


def initialize_sc(tierMax):
    return dreqQuery(dq=dq, tierMax=tierMax)


def get_DR_version():
    return dq.version
