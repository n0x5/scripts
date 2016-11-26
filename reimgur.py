#!/usr/bin/env python

# Retrieve Imgur+
#
# Download all images on a subreddit from imgur.com/i.redd.it/reddituploads
#
# BRAND NEW 26 NOVEMBER 2016
#
# - Names the files after reddit title of post
# - Several fixes for edgecases of weird chars etc
# - adds imgur unique ID to filename
#
# reimgur.py 'subreddit' start year-month-day end year-month-day e.g.
# 'reimgur.py pics 2015-01-01 2015-01-10'
#
# can also change the 'hot' text in the url to 'new', 'controversial' and so on

import re
import time
import argparse
import calendar
import urllib.request
from urllib.request import FancyURLopener
import os
import requests
from bs4 import BeautifulSoup
import itertools

def crdate(datestr):
    return calendar.timegm(time.strptime(datestr, '%Y-%m-%d'))

parser = argparse.ArgumentParser()
parser.add_argument('subreddit')
parser.add_argument('tstamp1', type=crdate)
parser.add_argument('tstamp2', type=crdate)
args = parser.parse_args()

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                   ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
}

url = ('https://www.reddit.com/r/%s/search?q=timestamp%%3A%s..%s&restrict_sr=on&sort=hot&t=all&limit=60&syntax=cloudsearch'
       % (args.subreddit, args.tstamp1, args.tstamp2))

class GrabIt(urllib.request.FancyURLopener):
    version = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
    def download_file(self, url, path):
            try:
                urlretrieve = GrabIt().retrieve
                urlretrieve(url, path)
            except Exception as e:
                print(str(e))

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
grab1 = GrabIt()
cont = soup.find('div', attrs={'class': 'contents'})

def title(contentz):
    for title2 in contentz.find_all('a', class_="search-title may-blank") or contentz:
        return title2.get_text(' ', strip=True)

def single(contentz):
    for link in contentz.find_all('a', class_="search-link may-blank") or contentz:
        return link.text

print("searching", url)

for contentz in cont.find_all('div', class_=" search-result search-result-link has-thumbnail no-linkflair ") or contentz:
    print(title(contentz), single(contentz))
    title2 = title(contentz)
    link2 = single(contentz)
    if 'i.imgur.com' in link2:
        if os.path.isfile(title2.replace(' ', '_')+'_'+link2[-11:]):
            print('file exists - skipping')
        else:
            grab1.download_file(link2, title2.replace(' ', '_')+'_'+link2[-11:])
            print(title2.replace(' ', '_')+'_'+link2[-11:])

    if 'imgur.com/a' in link2 or 'https://imgur.com/' in link2:
        number = 0
        response2 = requests.get(link2, headers=headers)
        soup2 = BeautifulSoup(response2.text, "html.parser")
        for linkalb2 in soup2.findAll('a', href=re.compile('\/\/i.imgur.com\/\w{7}(.jpg)')):
            number += 1
            link3 = linkalb2['href']
            print(title2.replace(' ', '_')+'_'+str(number)+'_'+link3[-11:])
            if os.path.isfile(title2.replace(' ', '_')+'_'+str(number)+'_'+link3[-11:]):
                print('file exists - skipping')
            else:
                grab1.download_file('http:'+link3, title2.replace(' ', '_')+'_'+str(number)+'_'+link3[-11:])
                print(title2.replace(' ', '_')+'_'+str(number)+'_'+link3[-11:])

    if 'i.redd.it' in link2:
        grab1.download_file(link2, title2.replace(' ', '_')+'_'+link2[17:].replace('/', '_'))
        print(link2[17:])

    if 'i.reddituploads.com' in link2:
        grab1.download_file(link2, title2.replace(' ', '_')+'_redditup_'+link2[-17:].replace('/', '_')+'.jpg')
        print(link2[17:]+'.jpg')
