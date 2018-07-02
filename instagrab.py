# instagrab.py - download images from instagram
#
# write the names of the user you want to download in 'users' list (user1, user2' etc)
# supports unlimited amount of users
# python instagrab.py

import re
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import sys
import os
import json
import urllib.request
from urllib.request import FancyURLopener
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


users = ['user1', 'user2', 'user3', 'user4', 'user5']


class GrabIt(urllib.request.FancyURLopener):
        version = ('Mozilla/6.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/53.0.2526.111 Safari/547.36')
        def download_file(self, url, path):
                try:
                    self.urlretrieve = GrabIt().retrieve
                    self.urlretrieve(url, path)
                except Exception as e:
                    print(str(e))

def grab_img(user):
    grab1 = GrabIt()
    headers = {
        'User-Agent': 'Mozilla/9.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/10300101 Firefox/50.0'
    }
    
    url = 'https://www.instagram.com/'+user+'/'
    html = requests.get(url, headers=headers)
    time.sleep(0.9)
    soup = BeautifulSoup(html.text, "html.parser")
    print(user)
    table1 = soup.find('body')
    table = table1.find('script', type=re.compile('text/javascript'))
    json1 = table.get_text().replace('window._sharedData = ', '')[:-1]
    data = json.loads(json1)
    files = data['entry_data']['ProfilePage']
    for item in files:
        full_url2 = item['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for item3 in full_url2:
            full_url = item3['node']['display_url']
            filenm = os.path.basename(full_url)
            endpoint1 = os.path.join(os.path.dirname(__file__), user, user+'_'+filenm)
            time.sleep(2)
            if not os.path.exists(user):
                    os.makedirs(user)
            if os.path.isfile(endpoint1):
                print('file {} exists - skipping' .format(endpoint1))
            else:
                try:
                    grab1.download_file(full_url, endpoint1)
                    print(full_url)
                except Exception as e:
                    print(str(e))


#users = list(reversed(users))

for user in tqdm(users):
    r_int = randint(9, 20)
    time.sleep(r_int)
    print(user)
    try:
        grab_img(user)
    except:
        print('no file')
        pass


