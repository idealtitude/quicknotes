# -*- coding: utf-8 -*-

"""
These series of classes are used for all file streams related operations.
"""

import os

from typing import Union, Any
import json

EXISTS   : int = 1
READABLE : int = 2
WRITABLE : int = 4
ISFILE   : int = 8

class File:
    """Base class for managing files."""
    def __init__(self, file_path: str)->None:
        self.current_file: Union[str, None]
        self.file_content: Union[str, list[str]]


class StandardFile(File):
    """Implementation for basic files."""
    def __init__(self, file_path: str)->None:
        super().__init__(file_path)

class JSONFile(File):
    """Implementation for json files."""
    def __init__(self, file_path: str)->None:
        super().__init__(file_path)
