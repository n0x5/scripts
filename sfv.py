#!/usr/bin/env python

# Creates .sfv file for all mp3 and flac in folder

import sys
import os
import zlib

cwd = os.getcwd()
os.chdir(cwd)
b = open("this.sfv", 'w' )

def crc32(file2):
    sf = open(file2,'rb').read()
    sf2 = format(zlib.crc32(sf), '08x')
    print("{} is {}" .format(fn, sf2))
    b.write("{} {}\n" .format(fn, sf2))

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.endswith(".mp3") or fn.endswith(".flac"):
            try:
                crc32(os.path.join(subdir, fn))
            except:
                pass
