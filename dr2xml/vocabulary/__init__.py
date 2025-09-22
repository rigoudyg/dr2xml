#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from dr2xml.settings_interface import get_settings_values
from .esgvoc_configuration import setup_esgvoc_config


def get_vocabulary():
	vocabulary_project = get_settings_values("internal", "vocabulary_project")
	vocabulary_config = get_settings_values("internal", "vocabulary_project_config")

	setup_esgvoc_config(config_name=vocabulary_project, config_file=vocabulary_config)

	import esgvoc.api as ev

	return ev