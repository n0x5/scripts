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
from random import randint
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
    time.sleep(0.2)
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
            time.sleep(0.1)
            full_url = 'https://instagram.com/p/'+item3['node']['shortcode']
            html2 = requests.get(full_url, headers=headers)
            soup2 = BeautifulSoup(html2.text, "html.parser")
            table2 = soup2.find('body')
            table3 = table2.find('script', type=re.compile('text/javascript'))
            json2 = table3.get_text().replace('window._sharedData = ', '')[:-1]
            data2 = json.loads(json2)
            files2 = data2['entry_data']['PostPage']
            for item2 in files2:
                full_url_disp = item2['graphql']['shortcode_media']['display_url']
                filenm2 = os.path.basename(full_url_disp)
                filenm = re.search(r'(\S+\.jpg)', filenm2)
                endpoint1 = os.path.join(os.path.dirname(__file__), user, user+'_'+filenm.group(1))
                time.sleep(0.2)
                if not os.path.exists(user):
                        os.makedirs(user)
                if os.path.isfile(endpoint1):
                    print('file {} exists - skipping' .format(endpoint1))
                else:
                    try:
                        grab1.download_file(full_url_disp, endpoint1)
                        print(full_url_disp)
                    except Exception as e:
                        print(str(e))

            for item5 in files2:
                try:
                    full_url_edgecar = item5['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
                    for item4 in full_url_edgecar:
                        full_url_disp = item4['node']['display_url']
                        filenm2 = os.path.basename(full_url_disp)
                        filenm = re.search(r'(\S+\.jpg)', filenm2)
                        endpoint1 = os.path.join(os.path.dirname(__file__), user, user+'_'+filenm.group(1))
                        time.sleep(0.2)
                        if not os.path.exists(user):
                                os.makedirs(user)
                        if os.path.isfile(endpoint1):
                            print('file {} exists - skipping' .format(endpoint1))
                        else:
                            try:
                                grab1.download_file(full_url_disp, endpoint1)
                                print(full_url_disp)
                            except Exception as d:
                                print(str(d))
                except Exception as e:
                    pass

users = list(reversed(users))

for user in tqdm(users):
    r_int = randint(9, 20)
    time.sleep(r_int)
    print(user)
    try:
        grab_img(user)
    except Exception as e:
        print(str(e))

