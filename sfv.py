#!/usr/bin/env python
# Python SFV Creator sfv.py <file> 
import sys
import binascii

filename = sys.argv[1]

def crc32(filename):
    sf = open(filename,'rb').read()
    sf = hex(binascii.crc32(sf) % (1<<32)).replace('0x', '')
    print ('{}' .format(sf))

crc32(filename)
