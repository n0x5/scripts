# instagrab.py - download images from instagram
#
# write the names of the user you want to download in 'users' list (user1, user2' etc)
# supports an unlimited amount of users
# only grabs latest images for now
# python instagrab.py

import re
from selenium import webdriver
import time
import sys
import os
import urllib.request
from urllib.request import FancyURLopener


users = ['user1', 'user2', 'user3', 'user4', 'user5']

class GrabIt(urllib.request.FancyURLopener):
        version = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
        def download_file(self, url, path):
                try:
                    urlretrieve = GrabIt().retrieve
                    urlretrieve(url, path)
                except Exception as e:
                    print(str(e))

def grab_img(user):
    grab1 = GrabIt()
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    url = 'https://www.instagram.com/'+user+'/'
    driver.get(url)
    elem = driver.find_elements_by_xpath('//*[@src]')

    for ii in elem:
        if 'https://scontent-' in ii.get_attribute('src'):
            content2 = ii.get_attribute('src')
            content3 = re.sub(r's\w\w\wx\w\w\w\/', '', content2, flags=re.IGNORECASE)
            content4 = re.sub(r'https:\/\/\w{8}-\w{4}-\w(.*)\/', '', content2, flags=re.IGNORECASE)
            content5 = re.sub(r'\?ig_cache_key=\w{26}(\S+)', '', content4, flags=re.IGNORECASE)
            endpoint = os.path.join(os.path.dirname(__file__), user, content5)
            print(endpoint)
            if not os.path.exists(user):
                os.makedirs(user)
            if os.path.isfile(endpoint):
                print('file exists - skipping')
            else:
                try:
                    time.sleep(4)
                    grab1.download_file(content3, endpoint)
                    print(content5)
                except Exception as e:
                    print(str(e))

for user in users:
    grab_img(user)

driver.quit()
