#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.settings_interface import get_settings_values


vocab = None


def load_vocabulary():
	vocabulary_used = get_settings_values("init", "vocabulary_used")
	vocabulary_project = get_settings_values("init", "vocabulary_project")
	vocabulary_config = get_settings_values("init", "vocabulary_config")

	if vocabulary_project is not None:
		from .esgvoc_configuration import setup_esgvoc_config
		global vocab
		vocab = setup_esgvoc_config(config_name=vocabulary_used, project=vocabulary_project, config_file=vocabulary_config)


def get_vocabulary():
	return vocab

def get_version():
	import esgvoc
	return esgvoc.__version__