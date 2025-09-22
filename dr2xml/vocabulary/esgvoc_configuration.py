#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import json
from esgvoc.core import service

def get_config_data(config_name, config_file="vocabulary.json"):
    with open(config_file) as config_fic:
        config_data = json.load(config_fic)
    rep = copy.deepcopy(config_data["default"])
    if config_name not in config_data:
        rep.update(copy.deepcopy(config_data[config_name]))
    return rep


def setup_esgvoc_config(config_name, config_file="vocabulary.json"):
    if config_name is not None:
        config_manager = service.get_config_manager()

        # Create minimal configuration with Universe and CMIP7
        config_data = get_config_data(config_name, config_file=config_file)

        # Check if config already exists
        if config_name in config_manager.list_configs():
            print("✅ ESGVoc already configured")
        else:
            config_manager.add_config(config_name, config_data)

        config_manager.switch_config(config_name)

        # Synchronize CVs
        service.current_state = service.get_state()
        service.current_state.synchronize_all()

        print(f"✅ ESGVoc configured with '{config_name}'")
    else:
        print("No vocabulary configured.")