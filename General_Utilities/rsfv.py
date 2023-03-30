# recursive sfv check

import sys
import os
import zlib

rootdir = r'/path/to/folder'

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
                        with open(os.path.join(rootdir, 'errors.txt'), 'a') as sfver:
                            sfver.write(sf1+'\n')
                        print('incorrect crc in {}' .format(sf1))
                    else:
                        print('crc ok {} {} {}' .format(sfv1, sf2, sf1))
                else:
                    pass
