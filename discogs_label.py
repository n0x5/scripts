# Recursively scan flac folders and get label/format from discogs 
# based on FLAC 'Artist' and 'Album' meta tags and write info to a file
# named '<Label_name>.label' in album directory

import shutil
import os
from mutagen.id3 import ID3
from mutagen.flac import FLAC
import requests
import re
from bs4 import BeautifulSoup
import time
import sqlite3
from random import randint
import json
import traceback

cwd = r'F:\archive\FLAC\Air'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}

for subdir, dirs, files in os.walk(cwd):
    f = 0
    for fn in files:
        if fn.endswith('.flac'):
            while f < 1:
                try:
                    f += 1
                    file2 = os.path.join(subdir, fn)
                    audio = FLAC(file2)
                    album = audio['album']
                    artist = audio['artist']
                    artist_f = artist[0].replace(' ', '+')
                    album_f = album[0].replace(' ', '+')
                    bing_query = 'https://www.bing.com/search?q={}+{}+site:discogs.com+master&search=&form=QBLH' .format(artist_f, album_f)
                    response = requests.get(bing_query, headers=headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    lists2 = soup.find_all('a', href=re.compile(r'discogs.com\/master'))
                    url_disc = lists2[0]['href']
                    response = requests.get(url_disc, headers=headers)
                    soup = BeautifulSoup(response.text, "html.parser")
                    info2 = soup.find_all('tr', attrs={'data-object-type': 'release'})

                    e = 0
                    for item in info2:
                        while e < 1:
                            e += 1
                            format = item.find('span', attrs={'class': 'format'}).text.strip()
                            title = item.find('td', attrs={'class': 'title'}).text.strip()
                            label = item.find('a', href=re.compile(r'discogs.com\/label')).text.strip()
                            catno = item.find('td', attrs={'class': 'catno has_header'}).text.strip()
                            country = item.find('td', attrs={'class': 'country has_header'}).text.strip()
                            year = item.find('td', attrs={'class': 'year has_header'}).text.strip()
                    with open(os.path.join(subdir, '{}.label' .format(label)), 'w') as sfver:
                        sfver.write('Label: '+label+'\n')
                        sfver.write('Format: '+format+'\n')
                        sfver.write('Country: '+country+'\n')
                        sfver.write('Year: '+year+'\n')
                        sfver.write('Cat No.: '+catno+'\n')

                    print(subdir, label, catno, country, year)
                    time.sleep(10)
                except Exception as e:
                    print(e)
                    pass
