#!/usr/bin/env python

import shutil
import os
import datetime
import pymysql

from mutagen.id3 import ID3

rootdir = 'K:\\archive\\mp3\\_LABELS'


conn = pymysql.connect(host ='127.0.0.1', user ='', passwd = '', db= 'mysql', charset ='utf8')
cur = conn.cursor()
cur.execute("USE NordDB")

def store(headline, grp, genre):
    cur.execute ("INSERT INTO music1 (headline, grp, genre) VALUES (\"{}\" , \"{}\" , \"{}\")" .format(basenm2, file6, sf))
    cur.connection.commit()
    

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if fn.startswith("01"):
            try:
                file2 = os.path.join(subdir, fn)
                audio = ID3(file2)
                sf = format(audio['TCON'].text[0])
                path2 = os.path.join(subdir)
                rootdir2 = os.path.join(rootdir, sf)
                basenm2 = os.path.basename(path2)
                file4 = basenm2.split('-')       
                file5 = file4[-1:]
                file6 = "[]".join(file5)
                store (basenm2, file6, sf)     
            except:
                pass
 
cur.close()
conn.close()
