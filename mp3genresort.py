#!/usr/bin/env python

import shutil
import os
import errno
from mutagen.id3 import ID3

rootdir = 'J:\\archive\mp3\mp3-2'


for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if fn.endswith(".mp3"):
            try:
                file2 = os.path.join(subdir, fn)
                audio = ID3(file2)
                sf = format(audio['TCON'].text[0])
                path2 = os.path.join(subdir)
                rootdir2 = os.path.join(rootdir, sf)
                if not os.path.exists(rootdir2): os.makedirs(rootdir2)
                basenm2 = os.path.basename(path2)
                basen3 = path2, os.path.join(rootdir2, basenm2)
                shutil.copytree(path2, os.path.join(rootdir2, basenm2), copy_function=os.symlink)
            except:
                pass
