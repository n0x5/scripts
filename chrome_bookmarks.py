# Simple less useful script to add bookmarks to an sqlite database from exported chrome html bookmarks file
# link is UNIQUE so no duplicate bookmarks (if the url is _exactly_ identical)

import re
from bs4 import BeautifulSoup
import sqlite3
import os
import time
import calendar
import time
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('bfile')
args = parser.parse_args()

conn = sqlite3.connect('bookmarks2.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists bookmarks 
            (link text unique, timeaddedunix text, timeaddedread text, desctitle text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')


bmarks = os.path.join(os.path.dirname(__file__), args.bfile)
i = open(bmarks, 'r', encoding='utf8')
soup = BeautifulSoup(i, "html.parser")

links = soup.find_all('a')

for link in tqdm(links):
    link_final2 = link['href']
    if 'instagram.com' in link_final2:
        link_final = re.sub(r'\?hl\=\w{2}', '', link_final2)
    else:
        link_final = link_final2
    t_added = link['add_date']
    t_read_i = int(link['add_date'])
    t_readable = time.strftime('%Y-%m-%d', time.gmtime(t_read_i))
    t_desc = link.get_text()
    try:
        cur.execute('INSERT INTO bookmarks (link, timeaddedunix, timeaddedread, desctitle) VALUES (?,?,?,?)', (link_final, t_added, str(t_readable), t_desc))
        cur.connection.commit()
    except Exception as e:
        print(e)