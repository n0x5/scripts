# Simple less useful script to add bookmarks to an sqlite database from exported chrome html bookmarks file
# link is UNIQUE so no duplicate bookmarks (if the url is _exactly_ identical)

import re
from bs4 import BeautifulSoup
import sqlite3
import os
import time
import calendar
import datetime

conn = sqlite3.connect('bookmarks.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists bookmarks 
            (link text unique, timeaddedunix text, timeaddedread text, desctitle text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')

bmarks = r'bookmarks_8_12_20.html'

i = open(bmarks, 'r', encoding='utf8')
soup = BeautifulSoup(i, "html.parser")

links = soup.find_all('a')

for link in links:
    link_final = link['href']
    t_added = link['add_date']
    t_read_i = int(link['add_date'])
    t_readable = datetime.datetime.utcfromtimestamp(t_read_i).strftime('%Y-%m-%d')
    t_desc = link.get_text()
    print(t_desc)
    try:
        cur.execute('INSERT INTO bookmarks (link, timeaddedunix, timeaddedread, desctitle) VALUES (?,?,?,?)', (link_final, t_added, str(t_readable), t_desc))
        cur.connection.commit()
    except Exception as e:
        print(e)
