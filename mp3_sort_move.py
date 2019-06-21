#!/usr/bin/env python3

# Move to sorted genre folders based on id3 tags


import shutil
import os
from mutagen.id3 import ID3

#cwd = os.getcwd()
#os.chdir(cwd)
cwd = r'/folder/path'



for subdir, dirs, files in os.walk(cwd):
    f = 0
    for fn in files:
        if fn.endswith('.mp3'):
            while f < 1:
                try:
                    f += 1
                    file2 = os.path.join(subdir, fn)
                    audio = ID3(file2)
                    sf = format(audio['TCON'].text[0])
                    path2 = os.path.join(subdir)
                    basenm2 = os.path.basename(path2)
                    basenm4 = os.path.basename(os.path.join(subdir))
                    file6 = "[]".join(basenm4.split('-')[-1:])
                    rootdir2 = os.path.join(cwd, sf)
                    path_dest = os.path.join(rootdir2, basenm2)
                    if sf in path2:
                        print('exists', basenm2, sf)
                        continue
                    if not sf in path2:
                        print(basenm2+' moved to->'+sf)
                        if not os.path.exists(rootdir2): os.makedirs(rootdir2)
                        if not os.path.exists(path_dest): shutil.move(path2, path_dest)
                except Exception as e:
                    print(e)
