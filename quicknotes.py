#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""QuickNotes
A notes manager
"""

import sys
import os

import argparse

# Constants
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

APP_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATHS = {
    'root': f"{APP_PATH}",
    'data': f"{APP_PATH}/data",
    'cwd' : os.getcwd()
}

# App version
_version = None
with open(f'{APP_PATH}/VERSION', 'r') as vers:
    _version = vers.readline()

__version__ = _version.strip()

# Command line arguments
parser = argparse.ArgumentParser(prog='Squicknotes', description='A simple, fast and easy notes manager', epilog='Help and documentation at https://quicknotes.github.io/')

parser.add_argument('new', nargs='?', help='Create a new note')
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

_args = parser.parse_args()

# Entry point
def main(args):
    print(f'len(sys.argv): {len(sys.argv)}')
    return EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main(_args))
