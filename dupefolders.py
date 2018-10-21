#!/usr/bin/env python3

# find duplicate folders

import os


rootdir = r'/folder/path'
erlist = []
fname = os.path.join(rootdir, 'dupes.txt')

for subdir, dirs, files in os.walk(rootdir):
    erlist.append(subdir)

for dupes in erlist:
    for subdir, dirs, files in os.walk(rootdir):
        dir3 = os.path.basename(subdir)
        dir4 = os.path.basename(dupes)
        if dir3 == dir4 and dupes != subdir:
            print(subdir, dupes)
            hfile = open(fname, 'a')
            hfile.write('location 1:'+subdir+'     location 2:'+dupes+'\n')
            hfile.flush()
            hfile.close()
