#!/usr/bin/env python

import sys
import os
import zlib

cwd = os.getcwd()
os.chdir(cwd)
b = open("this.sfv", 'w' )

def crc32(file2):
    sf = open(file2,'rb').read()
    sf = format(zlib.crc32(sf), '08x')
    print("{} is {}" .format(fn, sf))
    b.write("{} {}\n" .format(fn, sf))

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.endswith(".mp3") or fn.endswith(".flac"):
            try:
                file2 = os.path.join(subdir, fn)
                crc32(file2)
            except:
                pass
