# sort images into name folders based on exif
# need db of names


import re
import time
import os
from datetime import datetime
import sqlite3
from PIL import Image
import pyexiv2
from tqdm import tqdm
import shutil
#from gi.repository import GExiv2

cwd = r'/mnt/c//pictures'


def getname(fullpath, ex6):
    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'celeblist.db'))
    cursor = connection.cursor()
    cursor.execute("select celebname from celebslist")
    results = [item[0] for item in cursor.fetchall()]
    filn = os.path.basename(fullpath)
    celeb_list = []

    for adds2 in results:
        adds3 = adds2.split(' ')
        try:
            name1 = adds3[0]
            name2 = adds3[1]
        except Exception as e:
            pass
        if name1.lower() in filn.lower() and name2.lower() in filn.lower():
            celeb_list.append(name1+' '+name2)
            return celeb_list

def getname_exif(fullpath, ex6):
    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'celeblist.db'))
    cursor = connection.cursor()
    cursor.execute("select celebname from celebslist")
    results = [item[0] for item in cursor.fetchall()]
    filn = os.path.basename(fullpath)
    celeb_list = []

    for adds2 in results:
        adds3 = adds2.split(' ')
        try:
            name1 = adds3[0]
            name2 = adds3[1]
        except Exception as e:
            pass

        if name1.lower() in str(ex6).lower() and name2.lower() in str(ex6).lower() \
            and name1.lower() not in filn.lower() and name2.lower() not in filn.lower():
            celeb_list.append(name1+' '+name2)
            return celeb_list



for subdir, dirs, files in os.walk(cwd):
    for fn in tqdm(files):
        fullpath = os.path.join(subdir, fn)
        subfolder = os.path.basename(os.path.join(subdir))
        if 'thumbs' not in subfolder and 'New folder (2' in subfolder:
            try:
                imh = Image.open(fullpath).size
                ims3 = time.strftime('%Y_%m_%d', time.gmtime(os.path.getmtime(fullpath)))
                ex2 = pyexiv2.ImageMetadata(fullpath)
                ex2.read()
                ex4 = [str(ex2[item]) for item in ex2.iptc_keys]
                ex5 = [str(ex2[item]) for item in ex2.exif_keys]
                ex6 = ex4, ex5
                celebname = getname(fullpath, ex6)
                if not celebname:
                    celebname = getname_exif(fullpath, ex6)

            except Exception as e:
                print(e)
                pass
            imh2 = re.sub('[(/:)"]', '', str(imh).replace(', ', 'x'))
            swidth = imh2.split('x')

            try:
                rootdir_celeb = os.path.join(cwd, 'celeb_archive', celebname[0])
                if not os.path.exists(rootdir_celeb): os.makedirs(rootdir_celeb)
                rootdir_dest = os.path.join(cwd, 'celeb_archive', celebname[0], ims3+'_'+fn.replace(' ', '_'))
                print(rootdir_dest)
                if not os.path.exists(rootdir_dest): shutil.move(fullpath, rootdir_dest)
                
            except Exception as e:
                #print(e)
                pass
