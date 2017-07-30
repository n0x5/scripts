#!/usr/bin/env python3

# recursive sfv check

import sys
import os
import zlib

rootdir = r'/path/to/folder'
erlist = []

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if fn.endswith('.sfv'):
            sfvf = open(os.path.join(subdir, fn), 'r')
            for line in sfvf:
                try:
                    sfv1 = line.split()[1].lower()
                    sfv2 = line.split()[0].lower()
                    sf1 = os.path.join(subdir, line.split()[0])
                except Exception as e:
                    pass
                if not sfv2.startswith(';'):
                    try:
                        sf = open(sf1,'rb').read()
                    except:
                        print('file not found or corrupt', sf1)
                        pass
                    sf2 = format(zlib.crc32(sf), '08x')
                    if sfv1 != sf2:
                        erlist.append(sf1)
                        print('incorrect crc in {}' .format(sf1))
                    else:
                        print('crc ok {} {} {}' .format(sfv1, sf2, sf1))
                else:
                    pass

with open(os.path.join(rootdir, 'errors.txt'), 'w') as sfver:
    for line in erlist:
        print(line)
        sfver.write(line+'\n')

