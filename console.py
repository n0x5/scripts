#!/usr/bin/env python

# Search gamespot for games not released on PC
# Default section is PS2 but can be changed to any or none
#
# Command: 'console.py #' where # is the page number

import requests
import bs4
from bs4 import BeautifulSoup
import argparse



parser=argparse.ArgumentParser()
parser.add_argument('page')
args=parser.parse_args()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}

b = open('console.html', 'a' )
b.write('<!DOCTYPE html><html><body><table class="sortable" style="width:100%"><script src="sorttable.js"></script>')
b.write('<tr><th style="text-align:left">Title</th><th style="text-align:left">Systems</th></tr>\n')


url = 'http://www.gamespot.com/new-games/?sort=date&game_filter_type%5Bplatform%5D=94&game_filter_type%5BminRating%5D=&game_filter_type%5BtimeFrame%5D=&game_filter_type%5BstartDate%5D=&game_filter_type%5BendDate%5D=&game_filter_type%5Btheme%5D=&game_filter_type%5Bregion%5D=1&game_filter_type%5Bletter%5D=&page={}' .format(args.page) 
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

gameslist = soup.find('section', attrs={'class': 'editorial river'})


def title(game):
    for title2 in row.find_all('h3', class_="media-title") or row:
        return(title2.get_text(' ', strip=True))

def systems(game):
    for systems in row.find_all('ul', class_="system-list") or row:
        if 'PC' not in systems.text:
            return(systems.get_text(' ', strip=True))
        else:
            return(None)

for row in gameslist.find_all('div', class_="media-body") or row:
    if systems(row) is not None:
        print(title(row), systems(row))
        b.write("<tr><td class=\"title\">{}</td> <td class=\"systems\">{}</td></tr>\n" .format(title(row), systems(row)))

b.write("</table>\n</body>\n</html>")
b.close()
