#!/usr/bin/env python

# Search gamespot for games not released on PC:
#
# Command: 'console.py #' where # is the page number


import requests
import bs4
from bs4 import BeautifulSoup
import argparse
import urllib.request


parser=argparse.ArgumentParser()
parser.add_argument('page')
args=parser.parse_args()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}

url = 'http://www.gamespot.com/new-games/?sort=date&game_filter_type%5Bplatform%5D=94&game_filter_type%5BminRating%5D=&game_filter_type%5BtimeFrame%5D=&game_filter_type%5BstartDate%5D=&game_filter_type%5BendDate%5D=&game_filter_type%5Btheme%5D=&game_filter_type%5Bregion%5D=1&game_filter_type%5Bletter%5D=&page={}' .format(args.page) 
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

gameslist = soup.find('section', attrs={'class': 'editorial river'})

def title(game):
    for title in row.find_all('div', class_="media-body") or row:
        for title2 in title.find_all('h3', class_="media-title") or row:
            return(title2.get_text(' ', strip=True))

def systems(game):
    for systems in row.find_all('ul', class_="system-list") or row:
        if 'PC' not in systems.text:
            return(systems.get_text(' ', strip=True))
        else:
            return(None)

for row in gameslist.find_all('div', class_="media-body") or row:
    if systems(row) is not None:
        b = open('console.txt', 'a' )
        b.write('{}  {}\n' .format(title(row), systems(row)))

b.close()
