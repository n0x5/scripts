# Grab Google cache pages from a site: search
#
# python google_cache.py website.com
#
# 1/31/2018

import re
import requests
from bs4 import BeautifulSoup
import time
from random import randint
import argparse
import urllib.request
from urllib.request import FancyURLopener
import os

parser = argparse.ArgumentParser()
parser.add_argument('site')
args = parser.parse_args()

class GrabIt(urllib.request.FancyURLopener):
    version = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
    def download_file(self, url, path):
            try:
                urlretrieve = GrabIt().retrieve
                urlretrieve(url, path)
            except Exception as e:
                print(str(e))

def dl(i, site):

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/49.0'
        }

    url = 'https://www.google.com/search?safe=off&q=site%3A{}&num=50&start={}' .format(args.site, i)

    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    result_table = soup.find('div', attrs={'class': 'srg'})
    grab1 = GrabIt()

    def title2(table2):
        for title in table2.find_all('h3', class_="r"):
            return title.get_text()

    def link2(table2):
        for title in table2.find_all('a'):
            return title['href']

    def cache2(table2):
        for title in table2.find_all('a', attrs={'class': 'fl'}):
            if 'webcache' in title['href']:
                return title['href']
            else:
                return 'None'

    for table2 in result_table.find_all('div', class_="g") or table2:
        title3 = re.sub(r'[\;*?!<>|/:"]', '', title2(table2))
        number = randint(122223, 99500322)
        print('file exists')
        grab1.download_file(cache2(table2), title3+'.html'+str(number))
        print(title3, link2(table2), cache2(table2))
        rand_int = randint(4, 11)
        time.sleep(rand_int)


for i in range(0, 900, 50):
    print(i)
    dl(i, args.site)
    rand_int = randint(4, 11)
    time.sleep(rand_int)
