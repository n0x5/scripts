# pip install warcio
# warc to sqlite converter
# puts html documents in sqlite and writes images to disk in "images" folder

from warcio.archiveiterator import ArchiveIterator
import time
import os
from tqdm import tqdm
import re
import sqlite3

# 'content_stream', 'content_type', 'digest_checker', 'format', 'http_headers', 'length', 'payload_length', 'raw_stream', 'rec_headers', 'rec_type']
if not os.path.exists('images'):
    os.makedirs('images')

conn = sqlite3.connect('xbox360_warc.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE if not exists warc
            (id text, title text, body text)''')

lst = []

for subdir, dirs, files in os.walk(r'F:\dev\xbox360gamespy\war'):
    for fn in files:
        fpath = os.path.join(subdir, fn)
        with open(fpath, 'rb') as stream:
            for record in tqdm(ArchiveIterator(stream)):
                try:
                    if record.rec_type == 'response' and 'text/html' in record.http_headers['Content-Type'] and '200 OK' in str(record.http_headers):
                        try:
                            body = record.raw_stream.read().decode('UTF-8')
                            try:
                                title1 = re.search(r'<title>(.+?)<\/title>', body)
                                title = title1.group(1)
                                id_article = record.rec_headers['WARC-Target-URI']
                            except Exception:
                                id_article = record.rec_headers['WARC-Target-URI']
                                title = ''
                            stuff = id_article, title, body
                            if '' in title:
                                lst.append(stuff)
                            if len(lst) == 500:
                                cur.executemany('insert into warc (id, title, body) VALUES (?,?,?)', (lst))
                                cur.connection.commit()
                                lst = []
                        except Exception as e:
                            pass
                    if record.rec_type == 'response' and 'image/' in record.http_headers['Content-Type'] and '200 OK' in str(record.http_headers):
                        try:
                            fn = record.rec_headers['WARC-Target-URI'].split('/')[-1]
                            with open(os.path.join('images', '{}' .format(fn)), 'wb') as binary_file:
                                binary_file.write(record.raw_stream.read())
                        except Exception as e:
                            pass
                except Exception as e:
                    pass

        cur.executemany('insert into warc (id, title, body) VALUES (?,?,?)', (lst))
        cur.connection.commit()


