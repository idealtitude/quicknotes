#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""STARTER
Documentation, main docstring
"""

import sys
import os
#import typing
import argparse

# App version
__version__ = '0.0.1'

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Command line arguments
APP_PATH = os.path.dirname(os.path.realpath(__file__))
APP_CWD = os.getcwd()

parser = argparse.ArgumentParser(prog='STARTER', description='STARTER', epilog='Help and documentation at STARTER')

parser.add_argument('arg1', nargs=1, help='.......')
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

_args = parser.parse_args()

# Entry point
def main(args):
    print(f'len(sys.argv): {len(sys.argv)}')
    return EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main(_args))
