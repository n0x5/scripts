#!/usr/bin/env python

import sys
import os
import subprocess

cwd = os.getcwd()
os.chdir(cwd)

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.endswith(".wav"):
            try:
                fn2 = os.path.join(fn)
                subprocess.call('lame -V0 "{}"' .format(fn2))
            except:
                pass
