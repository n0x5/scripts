#!/usr/bin/env python
import sys
import zlib

filename = sys.argv[1]

def crc32(filename):
    sf = open(filename,'rb').read()
    sf = format(zlib.crc32(sf), '08x')
    print ('{}' .format(sf))

crc32(filename)
