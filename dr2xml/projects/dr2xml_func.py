#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Function used for dr2xml projects
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from utilities.logger import get_logger


def format_sizes(*sizes):
	"""
	Transform into a dict the sizes values provided as ['nho', 'nlo', 'nha', 'nla', 'nlas', 'nls', 'nh1'], with:
	- nho: oce grid size
	- nlo : oce nb levels
	- nha: atm grid size
	- nla: atm nb levels
	- nlas:
	- nls : soil nb of levels
	- nh1 : number of latitude (atmosphere/ocean grids)
	Also provide others infor such as:
	- nb cosp sites (default 129)
	- nb lidar temp (default 40)
	- nb_parasol_refl (default 5)
	- nb isccp tau (default 7)
	- nb isccp pc (default 5)
	- nb curtains sites (default 1000)
	:param dict or list sizes: dict containing the sizes as a list or dict
	:return dict: dictionary containing sizes as a dict
	"""
	logger = get_logger()
	rep = dict(nho=None, nlo=None, nha=None, nla=None, nlas=None, nls=None, nh1=None,
	           nb_cosp_sites=129, nb_lidar_temp=40, nb_parasol_refl=5, nb_isccp_tau=7, nb_isccp_pc=7,
	           nb_curtain_sites=1000)
	if isinstance(sizes, (list, tuple)) and len(sizes) == 1 and isinstance(sizes[0], (dict, list, tuple)):
		sizes = sizes[0]
	if isinstance(sizes, (list, tuple)):
		mcfg = dict()
		for (key, val) in zip(['nho', 'nlo', 'nha', 'nla', 'nlas', 'nls', 'nh1'], sizes):
			mcfg[key] = val
		rep.update(mcfg)
	elif isinstance(sizes, dict):
		rep.update(sizes)
	else:
		logger.error("Unable to transform sizes to get relevant information.")
		raise ValueError("Unable to transform sizes to get relevant information.")
	issues_values = [elt for elt in rep if rep[elt] is None]
	if len(issues_values) > 0:
		logger.error(f"The values provided by sizes must not be None, issues with {issues_values}.")
		raise ValueError(f"The values provided by sizes must not be None, issues with {issues_values}.")
	return rep


def sort_mips(*mips):
	if isinstance(mips, (list, tuple)) and len(mips) == 1 and isinstance(mips[0], (dict, set, list)):
		mips = mips[0]
	elif len(mips) == 0:
		mips = list()
	rep = set()
	if isinstance(mips, dict):
		for grid in mips:
			rep = rep | mips[grid]
	else:
		rep = mips
	return sorted(list(rep))