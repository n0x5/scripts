from datetime import datetime
import os
import sqlite3
from PIL import Image
import pyexiv2



cwd = r'/mnt/f/archive/_personal/camera/2013'

conn = sqlite3.connect('imagedb.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists images
             (file text, fullpath text unique, subfolder text, sizewidth int, sizeheight int, ftime int, exif text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')



def get_exif(path):
    exif2 = []
    ex2 = pyexiv2.ImageMetadata(path)
    ex2.read()
    for item in ex2:
        exif2.append([ex2[item].key, ex2[item].value])
    return exif2

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        fullpath = os.path.join(subdir, fn)
        subfolder = os.path.basename(os.path.join(subdir))
        try:
            image_size = Image.open(fullpath).size
            image_mtime = os.stat(fullpath)[8]
            image_mtime_readable = datetime.fromtimestamp(image_mtime)
            exif = get_exif(fullpath)
            sql = fn, fullpath, subfolder, image_size[0], image_size[1], image_mtime, str(exif)
            print(sql)
            cur.execute('insert into images (file, fullpath, subfolder, sizewidth, sizeheight, ftime, exif) VALUES (?,?,?,?,?,?,?)', (sql))
            cur.connection.commit()
        except Exception as e:
            print(e)


