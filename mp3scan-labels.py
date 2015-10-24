#!/usr/bin/env python

import shutil
import os
import datetime
import pymysql
import itertools

rootdir = 'S:\\archive\\mp3\\'
labelfile = 'F:\\python\\labels.txt'

conn = pymysql.connect(host ='127.0.0.1', user ='', passwd = '', db= 'mysql', charset ='utf8')
cur = conn.cursor()
cur.execute("USE DBname")

def store(title, grp, label):
    cur.execute ("INSERT INTO table (title, grp, label) VALUES (\"{}\" , \"{}\", \"{}\")" .format(basenm2, file6, labels(file2)))
    cur.connection.commit()

def labels(fn):
    with open(file2, "r") as f, open(labelfile, "r") as g:
        labels = [line.strip().lower().replace(".", " ").replace(" ", "") for line in g.readlines()]
        nfos = [line.strip().lower().replace(".", " ").replace("/", "").replace("|", "").replace("\\", "").replace("_", "").replace(":", "").replace("!", " ").replace("label", " ").replace(" ", "") for line in f.readlines()]
        outpt = [item for item in labels if item in nfos]
        return ( ", ".join( str(e) for e in outpt ) )

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if fn.endswith(".nfo"):
            try:
                file2 = os.path.join(subdir, fn)
                path2 = os.path.join(subdir)
                basenm2 = os.path.basename(path2)
                file4 = basenm2.split('-')       
                file5 = file4[-1:]
                file6 = "[]".join(file5) 
                store(basenm2, file6, labels(file2))
            except:
                pass
 
cur.close()
conn.close()
