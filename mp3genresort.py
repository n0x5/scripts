#!/usr/bin/env python

import shutil
import os
from mutagen.id3 import ID3

cwd = os.getcwd()
os.chdir(cwd)

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.startswith("01") or fn.startswith("101") or fn.startswith("a_") or fn.startswith("a-"):
            try:
                file2 = os.path.join(subdir, fn)
                audio = ID3(file2)
                sf = format(audio['TCON'].text[0])
                path2 = os.path.join(subdir)
                basenm2 = os.path.basename(path2)
                basenm4 = os.path.basename(os.path.join(subdir))
                file6 = "[]".join(basenm4.split('-')[-1:])
                rootdir2 = os.path.join(cwd,'Genres', sf)
                rootdir3 = os.path.join(cwd,'Groups', file6)
                basen3 = path2, os.path.join(rootdir2, basenm2)
                if not os.path.exists(rootdir2): os.makedirs(rootdir2)
                if not os.path.exists(rootdir3): os.makedirs(rootdir3)
                shutil.copytree(path2, os.path.join(rootdir2, basenm2), copy_function=os.symlink)
                shutil.copytree(path2, os.path.join(rootdir3, basenm2), copy_function=os.symlink)
            except:
                pass
