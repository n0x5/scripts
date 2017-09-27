import os
import re
import pymysql
import argparse
import subprocess
from mutagen.id3 import ID3
import sqlite3


parser = argparse.ArgumentParser()
parser.add_argument('year')
parser.add_argument('day')
args = parser.parse_args()

cwd = r'/jail/ftpd/site/MP3/{}/{}/' .format(args.year, args.day)

conn = pymysql.connect(host='', user='', passwd='', charset ='utf8')
cur = conn.cursor()
cur.execute("USE db")


#conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'residentadvisor.db'))
#cur = conn.cursor()



dirnames = os.listdir(cwd)


def genre1(fpath):
    fn = os.path.basename(path1)
    try:
        audio = ID3(path1)
        genre = format(audio['TCON'].text[0])
        return genre
    except:
        pass


for dr in dirnames:
    try:
        dirlist = os.listdir(os.path.join(cwd, dr))
    except:
        pass
    print(dr)
    label_list = []
    genre_list = []
    for fn in dirlist:
        rls = os.path.basename(dr)
        path1 = os.path.join(cwd, rls, fn)
        dirn = path1.split('/')
        date = dirn[-3]
        year = dirn[-4]
        if fn.endswith('.mp3') and not genre_list:
            genre2 = (genre1(path1))
            genre_list.append(genre2)
        else:
            genre2 = 'None'
        if '[LABEL' in fn:
            rmatch = re.match(r'\[LABEL\]\-(.+)\-\[LABEL\]', fn)
            label33 = rmatch.group(1)
            fn2 = fn.lower()
            lmatch = cur.execute("select label from db.labels WHERE UPPER(label) ='{}'" .format(label33.upper()))
            if lmatch > 0:
                print('match ->'+label33)
                label2 = label33
                label_list.append(label2)
            else:
                label2 = ['None']

    try:
        label = label_list[0]
        genre = genre_list[0]
        labelrest = label[1:].lower()
        labelcap = label[0].upper()
        label3 = labelcap+labelrest
        print(label3)
        labeldir = '/jail/glftpd/site/sorted/label/residentadvisor'
        if not os.path.exists(os.path.join(labeldir, year, date, genre, label3)):
            os.makedirs(os.path.join(labeldir, year, date, genre, label3))
        os.chmod(os.path.join(labeldir, year, date, genre), 0o777)
        os.chmod(os.path.join(labeldir, year, date, genre, label3), 0o777)
        cmd1 = 'ln -s /site/MP3/{}/{}/{} /jail/glftpd/site/sorted/label/residentadvisor/{}/{}/{}/{}/{}' .format(year, date, \
                rls.replace('(', '\(').replace(')', '\)').replace('&', '\&'), year, date, genre.replace(' ', '\ ').replace('&', '\&'), \
                label3.replace(' ', '\ ').replace('&', '\&'), rls.replace('(', '\(').replace(')', '\)').replace('&', '\&'))
        print(cmd1)
        subprocess.call(cmd1, shell=True)

    except Exception as e:
        pass
