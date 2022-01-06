# -*- coding: utf-8 -*-

from typing import Any

from qn import qnfiles

class AppInit:
    """Main initializtion of quicknotes."""
    def __init__(self, app_paths: dict[str, str])->None:
        self.paths: dict[str, str] = app_paths
        self.settings: Any
        self.load_settings()

    def load_settings(self)->None:
        conf = qnfiles.JSONFile(f'{self.paths["data"]}/settings.json')
        self.settings = conf.get_json(f'{self.paths["data"]}/settings.json')
