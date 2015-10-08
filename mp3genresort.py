#!/usr/bin/env python

import shutil
import os
import errno
from mutagen.id3 import ID3

rootdir = 'F:\python\mp3'


for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".mp3"):
            try:
                file2 = os.path.join(subdir, file)
                audio = ID3(file2)
                sf = format(audio['TCON'].text[0])
                path2 = os.path.join(subdir)
                rootdir2 = 'F:\python\mp3\{}' .format(sf)
                if not os.path.exists(rootdir2): os.makedirs(rootdir2)
                basenm2 = os.path.basename(path2)
                basen3 = path2, os.path.join(rootdir2, basenm2)
                shutil.move(path2, os.path.join(rootdir2, basenm2))
            except:
                pass
