#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""QuickNotes
A notes manager
"""

import sys
import os

from typing import Union, Any, Optional
import argparse

from qn.qninit import AppInit
from qn.qnmenus import MainMenu

# Constants
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

APP_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATHS = {
    "root": f"{APP_PATH}",
    "data": f"{APP_PATH}/data",
    "cwd" : os.getcwd()
}

# App version
_version = None
with open(f"{APP_PATH}/VERSION", 'r') as vers:
    _version = vers.readline()

__version__ = _version.strip()

# Command line arguments
def parse_args()->Union[argparse.Namespace, Any]:
    """
    Parsing command line arguments, only if `sys.argv > 1`

        Parameters:
            None

        Returns:
            arguments (argparse.Namespace): Arguments from command line
    """
    parser = argparse.ArgumentParser(prog="quicknotes", description="A simple, fast and easy notes manager", epilog="Help and documentation at https://quicknotes.github.io/")

    parser.add_argument("action", nargs=1, choices=["new", "read", "search", "edit", "config"], help="Main commands")
    parser.add_argument('-n', "--name", nargs='+', help="Provides a name (title) for one of the main commands")
    parser.add_argument('-c', "--category", nargs='+', help="Provides category(ies) for one of the main commands")
    parser.add_argument('-t', "--tags", nargs='+', help="Provides tag(s) for one of the main commands")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    return parser.parse_args()

# Entry point
def main()->int:
    if len(sys.argv) == 1:
        appinit = AppInit(APP_PATHS)
        colors = appinit.settings["theme"]
        mainmenu = MainMenu(colors)
    else:
        args = parse_args()

    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())
