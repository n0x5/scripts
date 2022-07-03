#!/usr/bin/env python3

# find duplicate folders

import os


rootdir = r'/path/folder'
erlist = []
fname = os.path.join(rootdir, 'dupes.txt')

for subdir, dirs, files in os.walk(rootdir):
    erlist.append(subdir)

for dupes in erlist:
    for dupes2 in erlist:
        dir3 = os.path.basename(dupes2)
        dir4 = os.path.basename(dupes)
        if dir3 == dir4 and dupes != dupes2:
            print(dupes2, dupes)
            hfile = open(fname, 'a')
            hfile.write('location 1:'+dupes+'     location 2:'+dupes2+'\n')
            hfile.flush()
            hfile.close()
