# join multiple video files with ffmpeg concat
# paths are relative to current working directory
# ffjoin.py clip1.mp4 clip2.mp4 clip4.mp4


import sys
import os
import subprocess
import argparse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs="+")

args = parser.parse_args()

print(args.files)
fname = 'clipmerg1.txt'
hfile = open(fname, 'w')

for fn in args.files:
    hfile.write("file '.\{}'\n" .format(fn))

hfile.flush()
hfile.close()

ffcmd = 'ffmpeg -f concat -safe 0 -i {} -c copy output2.mp4' .format(fname)
print(ffcmd)
subprocess.call(ffcmd)
