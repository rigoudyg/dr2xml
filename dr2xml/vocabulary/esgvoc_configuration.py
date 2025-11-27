#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import json
from esgvoc.core import service
from utilities.logger import get_logger

def get_config_data(config_name, config_file="vocabulary.json"):
    logger = get_logger()
    with open(config_file) as config_fic:
        config_data = json.load(config_fic)
    rep = copy.deepcopy(config_data["dr2xml_default"])
    if config_name in config_data:
        rep.update(copy.deepcopy(config_data[config_name]))
    else:
        logger.warning("%s not in config file, use default" % config_name)
    return rep


def setup_esgvoc_config(config_name, project, config_file="vocabulary.json"):
    logger = get_logger()
    if config_name is not None:
        config_manager = service.get_config_manager()

        # Create minimal configuration with Universe and CMIP7
        config_data = get_config_data(config_name, config_file=config_file)

        # Check if config already exists
        if config_name in config_manager.list_configs():
            logger.debug("✅ ESGVoc already configured")
        else:
            config_manager.add_config(config_name, config_data)

        config_manager.switch_config(config_name)

        # Synchronize CVs
        service.current_state = service.get_state()
        service.current_state.synchronize_all()

        logger.debug(f"✅ ESGVoc configured with '{config_name}'")

        import esgvoc.api as ev
        if project not in ev.get_all_projects():
            logger.error("Could not find project %s in ESGVoc (%s)" % (project, ev.get_all_projects()))
            raise ValueError("Could not find project %s in ESGVoc (%s)" % (project, ev.get_all_projects()))
    else:
        logger.debug("No vocabulary configured.")
