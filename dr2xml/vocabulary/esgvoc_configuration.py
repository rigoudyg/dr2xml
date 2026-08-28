#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import copy
import json
import os

from utilities.logger import get_logger

def get_config_data(config_name, project, config_file="vocabulary.json"):
    logger = get_logger()
    with open(config_file) as config_fic:
        config_data = json.load(config_fic)
    rep = copy.deepcopy(config_data["dr2xml_default"])
    if config_name in config_data:
        rep.update(copy.deepcopy(config_data[config_name]))
    else:
        logger.warning("%s not in config file, use default" % config_name)
    project_rep = copy.deepcopy(rep["default"])
    project_rep.update(copy.deepcopy(rep.get(project, dict())))
    return project_rep


def setup_esgvoc_config(config_name, project, config_file="vocabulary.json"):
    logger = get_logger()
    if config_name is not None:
        # Create minimal configuration with Universe and CMIP7
        config_data = get_config_data(config_name, project, config_file=config_file)
        os.environ["ESGVOC_HOME"] = config_data["database_directory"]
        os.environ["ESGVOC_OFFLINE"] = str(config_data.get("offline", False)).upper()
        from esgvoc.core.service.user_state import UserState
        from esgvoc.core.db_fetcher import DBFetcher
        state = UserState.load()
        fetcher = DBFetcher()

        def _install_and_activate(fetcher, state, project_id, version):
            """Télécharge si nécessaire, puis active la version."""
            try:
                snapshot = fetcher.get_snapshot(project_id, version=version)
                version = snapshot.version
            except Exception:
                snapshot = None
            target = UserState.db_path(project_id, version)

            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                fetcher.download_db(snapshot, target)

            dict_activate = dict(
                source="registry"
            )
            if snapshot is not None:
                dict_activate["checksum"] = snapshot.checksum_sha256
            state.set_active(
                project_id,
                version,
                **dict_activate
            )

        _install_and_activate(fetcher, state, "universe", config_data.get("universe_version", "latest"))
        _install_and_activate(fetcher, state, project, config_data.get("project_version", "latest"))

        import esgvoc.api as ev
        return ev
    else:
        logger.debug("No vocabulary configured.")
