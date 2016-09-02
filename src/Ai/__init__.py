#!/usr/bin/env python3
"""
This script automatically imports all modules of this package.
You can simply insert a .py file into the directory and it will be imported 
"""


from pathlib import Path
from os.path import abspath


path_of_this_file = abspath(__file__)

path_of_directory = path_of_this_file[:-11]

p = Path(str(path_of_directory))

#all files (their paths) inside this folder that end with .py
modules = list(p.glob('*.py'))

#get last part of the  path and cut .py from it
modules = [str(module).split("/")[-1][:-3] for module in modules]


__all__ = modules

#deleting references to hide them from the importing file
del Path
del abspath
del path_of_this_file
del path_of_directory
del p
del modules

from . import *
