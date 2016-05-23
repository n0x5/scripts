import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import argparse
from time import mktime
from datetime import datetime
import calendar
import urllib.request

def crdate(datestr):
    return time.strptime(datestr, '%Y-%m-%d')

parser=argparse.ArgumentParser()
parser.add_argument('subreddit')
parser.add_argument('tstamp1', type=crdate)
parser.add_argument('tstamp2', type=crdate)
args=parser.parse_args()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}

dt1 = calendar.timegm(args.tstamp1)
dt2 = calendar.timegm(args.tstamp2)
url = "https://www.reddit.com/r/{}/search?q=timestamp%3A{}..{}&restrict_sr=on&sort=new&t=all&limit=30&syntax=cloudsearch" .format(args.subreddit, dt1, dt2)
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

for link in soup.findAll(string=re.compile("i.imgur.com")):
    print(link)
    urllib.request.urlretrieve(link, link[-11:])
