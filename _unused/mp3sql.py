#!/usr/bin/env python

import os
from datetime import datetime
import calendar
import pymysql
import hashlib
from functools import partial
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

rootdir = '/mp3/folder'

conn = pymysql.connect(host ='', user ='', passwd = '', db= 'DBname', charset ='utf8')
cur = conn.cursor()
cur.execute("USE DBname")



def store_fileinfo_in_db(unixtime, basenm2, fileb, fsize, hashd):
    sql = ("INSERT INTO fileinfo (`time`, `release`, `filename`, `filesize`, `hash`) "
           "VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")" .format(unixtime, basenm2, fileb, fsize, hashd))
    print(sql)
    cur.execute (sql)
    cur.connection.commit()

def store_id3_in_db(unixtime, basenm2, genre, year, samplerate, bitratemode, bitrate, bitmode):
    sql2 = ("INSERT INTO id3c (`Time`, `Release`, `Genre`, `Year`, `Samplerate`, `Channels`, `Bitrate`, `Bitratemode`) "
            "VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")" 
            .format(unixtime, basenm2, genre, year, samplerate, bitratemode, bitrate, bitmode))
    print(sql2)
    cur.execute(sql2)
    cur.connection.commit()


def md5sum(file2):
    with open(file2, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

def get_fileinfo(subdir, fn):
    file2 = os.path.join(subdir, fn)
    fsize = os.path.getsize(file2)
    path2 = os.path.join(subdir)
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    hashd = md5sum(file2)
    basenm2 = os.path.basename(path2)
    fileb = os.path.basename(file2)
    if not fn.endswith('.message') and not fn.endswith('.m3u'):
        store_fileinfo_in_db(unixtime, basenm2, fileb, fsize, hashd)

def get_id3_audio_info(subdir, fn):
    if fn.startswith("01") or fn.startswith("101") or fn.startswith("a"):
        file2 = os.path.join(subdir, fn) 
        audio = ID3(file2)
        audio2 = MP3(file2)
        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        path2 = os.path.join(subdir)
        basenm2 = os.path.basename(path2)
        genre = format(audio['TCON'].text[0]).replace(' ', '_').replace('&', 'and').replace('+', '_').replace('/', '_')
        year2 = format(audio["TDRC"].text[0])
        year = year2[:4]
        bitrate2 = audio2.info.bitrate
        bitrate3 = str(bitrate2)
        bitrate = bitrate3[:3]
        samplerate = audio2.info.sample_rate
        channelsi = audio2.info.channels
        bitratemode = audio2.info.mode
        bitmode2 = audio2.info.bitrate_mode
        bitmode3 = str(bitmode2)
        bitmode = bitmode3[-3:]
        rootdir2 = os.path.join(rootdir, year)

        if bitratemode == 0:
            bitratemode = 'Stereo'
        elif bitratemode == 1:
            bitratemode = 'Joint-Stereo'
        elif bitratemode == 2:
            bitratemode = 'Dual-Channel'
        elif bitratemode == 3:
            bitratemode = 'Mono'
 
        if bitmode == 'OWN':
            bitmode = 'CBR'
        store_id3_in_db(unixtime, basenm2, genre, year, samplerate, bitratemode, bitrate, bitmode)

def run_main():
    for subdir, dirs, files in os.walk(rootdir):
        for fn in files:
            try:
                get_fileinfo(subdir, fn)
                get_id3_audio_info(subdir, fn)
            except Exception as e:
                print(str(e))

run_main()

cur.close()
conn.close()
