# instagrab.py - download images from instagram
#
# write the names of the user you want to download in 'users' list (user1, user2' etc)
# supports unlimited amount of users
# python instagrab.py

import re
import requests
import json
import urllib.request
from urllib.request import FancyURLopener
import os
import time
from tqdm import tqdm


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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
        }
    url = 'https://www.instagram.com/'+user+'/?__a=1'
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    files = data['graphql']['user']['edge_owner_to_timeline_media']['edges']

    for item in files:
        full_url = item['node']['display_url']
        filenm = os.path.basename(full_url)
        endpoint1 = os.path.join(os.path.dirname(__file__), user, user+'_'+filenm)
        time.sleep(1)
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

for user in tqdm(users):
    print(user)
    grab_img(user)
