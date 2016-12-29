#!/usr/bin/env python

# Search gamespot for games not released on PC
#
# Command: 'console.py #' where # is the page number
#
# Automatic paging version

import re
import requests
from bs4 import BeautifulSoup
import time
from random import randint


wsite = open('console_exclusives_X360.html', 'a')
wsite.write('<!DOCTYPE html><html><body><table class="sortable" style="wid'
            'th:100%"><script src="sorttable.js"></script>')
wsite.write('<tr><th style="text-align:left">Title</th><th style="text-ali'
            'gn:left">Systems</th><th style="text-align:left">Date</th></tr>\n')

def dl(i, wsite):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }


    url = 'http://www.gamespot.com/new-games/?sort=date&game_filter_type%5Bplatform%5D=111&game_filter_type%5BminRating%5D=&game_filter_type%5BtimeFrame%5D=&game_filter_type%5BstartDate%5D=&game_filter_type%5BendDate%5D=&game_filter_type%5Btheme%5D=&game_filter_type%5Bregion%5D=1&___game_filter_type%5Bdevelopers%5D=&___game_filter_type%5Bpublishers%5D=&game_filter_type%5Bletter%5D=&page={}' .format(str(i))
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    gameslist = soup.find('section', attrs={'class': 'editorial river'})


    def title(row):
        for title2 in row.find_all('h3', class_="media-title") or row:
            return title2.get_text(' ', strip=True)

    def rlsdate(row):
        for dat2 in row.find_all('time', class_="media-date") or row:
            dat3 = dat2.get_text(' ', strip=True)
            dat4 = re.search(r'\w{3}\W*.\d,\s\d{4}', dat3)
            if dat4 is not None:
                return dat4.group(0)
            else:
                return 'None'

    def systems(row):
        for systems in row.find_all('ul', class_="system-list") or row:
            if 'PC' not in systems.text:
                return systems.get_text(' ', strip=True)
            else:
                return None

    for row in gameslist.find_all('div', class_="media-body") or row:
        if systems(row) is not None:
            print(title(row), systems(row), rlsdate(row))
            wsite.write(('<tr><td class="title">{}</td> <td class="systems">{}'
                         '</td><td class="rlsdate">{}</td></tr>\n') .format(title(row), systems(row), rlsdate(row)))


for i in range(1, 237):
    dl(i, wsite)
    r_int = randint(20, 130)
    time.sleep(r_int)


wsite.write("</table>\n</body>\n</html>")
wsite.close()
