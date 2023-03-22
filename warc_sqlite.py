# pip install warcio
# warc to sqlite converter
# puts html documents in sqlite and writes images to disk in "images" folder
# --html writes html files to disk as well
#
# Example: python .\warc_sqlite2.py F:\dev\warcscript\sacredtexts --html
#

from warcio.archiveiterator import ArchiveIterator
import time
import os
from tqdm import tqdm
import re
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('folder')
parser.add_argument('--html', action='store_const', const=1)
args = parser.parse_args()

site1 = args.folder


if not os.path.exists('{}_images' .format(site1)):
    os.makedirs('{}_images' .format(site1))

conn = sqlite3.connect('{}_warc.db' .format(site1))
cur = conn.cursor()

cur.execute('''CREATE TABLE if not exists warc
            (id text unique, title text, body text)''')

lst = []

for subdir, dirs, files in os.walk(r'{}' .format(site1)):
    for fn in files:
        fpath = os.path.join(subdir, fn)
        with open(fpath, 'rb') as stream:
            try:
                for record in tqdm(ArchiveIterator(stream)):
                    try:
                        if record.rec_type == 'response' and 'text/html' in record.http_headers['Content-Type'] and '200 OK' in str(record.http_headers):
                            try:
                                body = record.raw_stream.read().decode('UTF-8')
                                if args.html == 1:
                                    if not os.path.exists('{}_html' .format(site1)):
                                        os.makedirs('{}_html' .format(site1))
                                    fn = record.rec_headers['WARC-Target-URI'].split('/')[-1]
                                    with open(os.path.join('{}_html' .format(os.path.basename(site1)), '{}' .format(fn)), 'wb') as binary_file1:
                                        binary_file1.write(body)
                                try:
                                    title1 = re.search(r'<title>(.+?)<\/title>', body, re.IGNORECASE)
                                    title = title1.group(1)
                                    id_article = record.rec_headers['WARC-Target-URI']
                                except Exception:
                                    id_article = record.rec_headers['WARC-Target-URI']
                                    title = ''
                                stuff = id_article, title, body
                                if '' in title:
                                    lst.append(stuff)
                                if len(lst) == 50:
                                    cur.executemany('insert or ignore into warc (id, title, body) VALUES (?,?,?)', (lst))
                                    cur.connection.commit()
                                    lst = []
                            except Exception as e:
                                pass
                        if record.rec_type == 'response' and 'image/' in record.http_headers['Content-Type'] and '200 OK' in str(record.http_headers):
                            try:
                                fn = record.rec_headers['WARC-Target-URI'].split('/')[-1]
                                with open(os.path.join('{}_images' .format(os.path.basename(site1)), '{}' .format(fn)), 'wb') as binary_file:
                                    binary_file.write(record.raw_stream.read())
                            except Exception as e:
                                pass
                    except Exception as e:
                        pass
            except:
                pass

        cur.executemany('insert or ignore into warc (id, title, body) VALUES (?,?,?)', (lst))
        cur.connection.commit()


