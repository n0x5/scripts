import re
import time
import sys
import os
import json
import urllib.request
from urllib.request import FancyURLopener
from random import randint
import requests

class GrabIt(urllib.request.FancyURLopener):
    version = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
    def download_file(self, url, path):
            try:
                urlretrieve = GrabIt().retrieve
                urlretrieve(url, path)
            except Exception as e:
                print(str(e))

headers = {
    'User-Agent': 'Mozilla/9.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/10300101 Firefox/50.0'
}


fn = open('New Text Document.txt', 'r')
grab1 = GrabIt()
for line in fn:
    line2 = re.sub('\?.+', '', str(line))
    print(line2)
    grab1.download_file(line2, os.path.basename(line2).strip('\n')+'.jpg')
