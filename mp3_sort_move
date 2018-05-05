#!/usr/bin/env python3

# Move to sorted genre folders based on id3 tags

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
                rootdir2 = os.path.join(cwd, sf)
                path_dest = os.path.join(rootdir2, basenm2)
                print(path2, path_dest)
                if not os.path.exists(rootdir2): os.makedirs(rootdir2)
                if not os.path.exists(path_dest): shutil.move(path2, path_dest)
            except:
                pass
