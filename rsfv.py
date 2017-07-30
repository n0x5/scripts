#!/usr/bin/env python3

# recursive sfv check

import sys
import os
import zlib

rootdir = r'/path/to/folder'
errors = 'errors.txt'

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if fn.endswith('.sfv'):
            sfvf = open(os.path.join(subdir, fn), 'r')
            sfver = open(os.path.join(rootdir, errors), 'w')
            for line in sfvf:
                sfv1 = line.split()[1].lower()
                sf1 = os.path.join(subdir, line.split()[0])
                sf = open(sf1,'rb').read()
                sf2 = format(zlib.crc32(sf), '08x')
                if ';' in sf1:
                    pass
                if sfv1 != sf2:
                    print('incorrect crc in {}' .format(sf1))
                    sfver.write('incorrect crc in {}' .format(sf1))
                else:
                    print('crc ok {} {}' .format(sfv1, sf2))
