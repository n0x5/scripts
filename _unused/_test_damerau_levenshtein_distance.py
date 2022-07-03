#!/usr/bin/env python3

# template to check string similarity / edit distance between names of files in a folder

import re
import sys
import os
import shutil
from pyxdameraulevenshtein import damerau_levenshtein_distance

cwd = r'/folder/path'

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        for fn2 in files:
            fn1 = fn.lower()
            fn3 = fn2.lower()
            if damerau_levenshtein_distance(fn1, fn3) < 5 and fn1 != fn3:
                print(fn, fn2)
