import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import re
import time


cwd = r'Z:\archive\xvid\2016'


conn = sqlite3.connect('movies44.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE if not exists box_imdb
            (rlid text, imdbid text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')

def imdburl(fn):
    filn2 = open(fn, 'r')
    for line in filn2:
        if "imdb.com/" in line.lower():
            urls = re.findall(r'\d{6,10}', line)
            urls23 = "[]".join(urls)
    return 'https://www.boxofficemojo.com/title/tt'+urls23

def get_info(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('div', attrs={'class': 'a-section mojo-gutter'})
    lists = table.find('a', href=re.compile('\/release'))
    imdb_id = re.search(r'(tt\d{6,12})', url)
    try:
        rl_id = re.search(r'(rl\d{7,12})', str(lists['href']))
        stuff = rl_id.group(1), imdb_id.group(1)
        print(stuff)
        cur.execute('INSERT INTO box_imdb (rlid, imdbid) VALUES (?,?)', (stuff))
        cur.connection.commit()
    except:
        lists = table.find('a', href=re.compile('\/releasegroup'))
        response2 = requests.get('https://www.boxofficemojo.com'+lists['href'], headers=headers)
        soup2 = BeautifulSoup(response2.text, "html.parser")
        table2 = soup2.find('div', attrs={'class': 'a-section a-spacing-none mojo-gutter'})
        lists2 = table2.find('a', href=re.compile('\/release'))
        rl_id2 = re.search(r'(rl\d{7,12})', str(lists2['href']))
        stuff2 = rl_id2.group(1), imdb_id.group(1)
        print('Original: ', stuff2)
        cur.execute('INSERT INTO box_imdb (rlid, imdbid) VALUES (?,?)', (stuff2))
        cur.connection.commit()
    finally:
        pass


for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.endswith(".nfo"):
            try:
                file2 = os.path.join(subdir, fn)
                basenm2 = os.path.basename(os.path.join(subdir))
                url = imdburl(file2)
                print(fn, url)
                imdb_id3 = re.search(r'(tt\d{6,12})', url)
                cur.execute('select exists(select 1 from box_imdb where imdbid=? LIMIT 1)', (imdb_id3.group(1),))
                record = cur.fetchone()
                if record[0] == 1:
                    print('Movie already exists', imdb_id3)
                else:
                    get_info(url)
                    time.sleep(2)

            except Exception as e:
                print(e)
