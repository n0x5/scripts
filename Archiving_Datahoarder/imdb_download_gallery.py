import os
import requests
import re
from bs4 import BeautifulSoup
import time
import sqlite3
from random import randint
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url')
args = parser.parse_args()

def get_info(url):
    headers = {
    'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('title')
    table = soup.find('script', type=re.compile(r'ld\+json'))

    try:
        data = json.loads(table.string)
    except:
        data = json.loads(table.get_text())

    json_data = json.dumps(data)
    for item in data['image']:
        print(item)
        file_url = item['url']
        filename = os.path.basename(file_url)
        if not os.path.exists(filename):
            r = requests.get(file_url, headers=headers)
            with open(filename, 'wb') as cover_jpg:
                cover_jpg.write(r.content)

        file_url = item['contentUrl']
        filename = os.path.basename(file_url)
        if not os.path.exists(filename):
            print('contenturl not exist')
            r = requests.get(file_url, headers=headers)
            with open(filename, 'wb') as cover_jpg:
                cover_jpg.write(r.content)

info = get_info(args.url)

