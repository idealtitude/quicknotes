# -*- coding: utf-8 -*-

"""
These series of classes are used for all file streams related operations.
"""

import os

from typing import Union, Any, Optional
import json

EXISTS   : int = 1
READABLE : int = 2
WRITABLE : int = 4
ISFILE   : int = 8

class File:
    """Base class for managing files."""
    def __init__(self, file_path: str)->None:
        self.current_file: Union[str, None] = file_path if self.file_exists(file_path) else None
        self.file_content: Union[str, list[str]]

    def file_exists(self, file_path: str)->bool:
        if os.path.exists(file_path):
            return True
        return False

    def is_readable(self, file_path: str)->bool:
        return os.access(file_path, os.R_OK)

    def is_writable(self, file_path: str)->bool:
        return os.access(file_path, os.W_OK)

    def is_file(self, file_path: str)->bool:
        if os.path.isfile(file_path):
            return True
        return False

    def file_checks(self, file_path: str, checks: int)->dict[str, Union[None, bool]]:
        """
        Operate different checks on given file.

            Parameters:
                file_path (str)     path of the file to check
                checks    (integer) A value between 1 and 7
                                    1 -> Check if ftarget exists
                                    2 -> Check if file is readable
                                    4 -> Check if file is writable
                                    8 -> Check if is file or directory

            Returns:
                checks_result (dict) A dicionnary corresponding to the various checks
                `{"exists": bool, "perms": [bool, bool], "isfile": bool}`
        """

        checks_result: dict[str, Union[None, bool]] = {
            "exists": None,
            "readable": None,
            "writable": None,
            "isfile": None
        }

        # all check
        bitmask: list[int] = [1, 2, 4, 8]
        for i in bitmask:
            b = i & checks
            if b == 1:
                checks_result["exists"] = self.file_exists(file_path)
                continue
            if b == 2:
                checks_result["readable"] = self.is_readable(file_path)
                continue
            if b == 4:
                checks_result["writable"] = self.is_writable(file_path)
                continue
            if b == 8:
                checks_result["isfile"] = self.is_file(file_path)
                continue

        return checks_result

    def get_content(self, file_path: str, output: str = "string")->Union[str, list[str]]:
        res: Union[str, list[str]]

        with open(file_path, 'r') as fd:
            if output == "string":
                res = fd.read()
            elif output == "list":
                res = fd.readlines()

        return res

    def set_content(self, file_path: str, content: str = "string", mode: str = 'w')->None:
        with open(file_path, mode) as fd:
            if content == "string" and isinstance(content, str):
                fd.write(content)
            elif content == "list" and isinstance(content, list):
                for line in content:
                    fd.write(line +'\n')

    def update_current_file(self, file_path: str)->None:
        self.current_file = file_path

    def update_file_content(self, file_content: Union[str, list[str]])->None:
        self.file_content = file_content


class StandardFile(File):
    """Implementation for basic files."""
    def __init__(self, file_path: str)->None:
        super().__init__(file_path)

class JSONFile(File):
    """Implementation for basic files."""
    def __init__(self, file_path: str)->None:
        super().__init__(file_path)

    def get_json(self, file_path: str)->Any:
        with open(file_path, 'r') as fd:
            return json.load(fd)

    def write_jcontent(self, file_path: str, content: Any)->None:
        with open(file_path, 'w') as fd:
            json.dump(fd, content)

    def json2obj(self, content: Any)->Any:
        return json.loads(content)

    def obj2json(self, content: object)->Any:
        return json.dumps(content)
