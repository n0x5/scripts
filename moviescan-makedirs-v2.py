#!/usr/bin/env python

import os

cwd = os.getcwd()
os.chdir(cwd)
rootdir = cwd

def store(title, grp, genre):
    print ("{} {}" .format(genrs(file2), rating(file2)))
    os.makedirs(file3+'__'+'Rating__'+rating(file2))

def genrs(fn):
    filn = open(fn, "r")
    for genres in filn:
        if 'genre' in genres.lower():
            genres2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-'
            output = [l for l in genres if l in genres2]
            return("".join(output).replace("GENRE", ""))

def rating(fn):
    filn = open(fn, "r")
    for ratings in filn:
        if 'rating' in ratings.lower():
            ratings2 = '0123456789,./'
            outpt = [l for l in ratings if l in ratings2]
            return("".join(outpt).replace("/", "__Votes__").lstrip('.').rstrip('.'))

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if fn.endswith(".nfo"):
            try:
                file2 = os.path.join(subdir, fn)
                basenm2 = os.path.basename(os.path.join(subdir))
                file3 = os.path.join(subdir, genrs(file2))
                file6 = "[]".join(basenm2.split('-')[-1:])
                file7 = file6.split('-')[0]
                store(basenm2, file6, genrs(file2))
            except:
                pass
