##
## Download fandom.com wiki to sqlite
##
## Command python fandom_api_to_sqlite.py <wiki name> (sub domain portion of fandom.com) (--OPTIONS)
## You need to specify each option to download, omitting an option skips that download (like --download-pages)
## Example for https://matrix.fandom.com: python fandom_api_to_sqlite.py matrix --download-images --download-pages --download-categories
##

import sqlite3
import requests
import json
import argparse
import os
import time
from lxml import etree
from io import BytesIO
import re


parser = argparse.ArgumentParser()
parser.add_argument('wiki')
parser.add_argument('--download-images', action='store_const', const=1)
parser.add_argument('--download-pages', action='store_const', const=1)
parser.add_argument('--download-categories', action='store_const', const=1)
args = parser.parse_args()


wiki_name = args.wiki
delay = 1

sql_db = os.path.join(os.path.dirname( __file__ ), '{}.db' .format(wiki_name))
conn = sqlite3.connect(sql_db)
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists `{}`
        (title text unique, content text)''' .format(wiki_name))

headers = {
'User-Agent': 'Firefox'
}



def get_rels(url):
    print(url)
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    pages = data['query']['allpages']
    lst3 = []
    lst = []
    for item in pages:
        lst3.append(str(item['pageid']))

    lst2 = '|'.join(lst3)
    url2 = 'https://{}.fandom.com/api.php?action=query&pageids={}&export=wikitext&format=json' .format(wiki_name, lst2)
    response2 = requests.get(url2, headers=headers)
    data2 = json.loads(response2.text)
    wiki_text = data2['query']['export']['*']
    context = etree.iterparse(BytesIO(wiki_text.encode('UTF-8')), tag='{http://www.mediawiki.org/xml/export-0.11/}page')
    for event, elem in context:
        tree = etree.tostring(elem, encoding='utf-8').decode()
        if ('<ns>0</ns>' in tree or '<ns>14</ns>' in tree or '<ns>10</ns>' in tree) and '#redirect' not in tree.lower():
            try:
                title1 = re.search('<title>(.+)<\/title>', str(tree), flags=re.DOTALL)
                text = re.search('<text .*">(.+)<\/text>', str(tree), flags=re.DOTALL)
                title = title1.group(1)
                try:
                    content = text.group(1)
                except:
                    content = ''
                stuff = title, content
                lst.append(stuff)
                if len(lst) == 50:
                    cur.executemany('insert or ignore into `{}` (title, content) VALUES (?,?)' .format(wiki_name), (lst))
                    cur.connection.commit()
                    lst = []

            except Exception as e:
                print(e)

        elem.clear()

        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]

    del context

    cur.executemany('insert or ignore into `{}` (title, content) VALUES (?,?)' .format(wiki_name), (lst))
    cur.connection.commit()

    time.sleep(delay)

    if 'continue' in data:
        apcont = data['continue']['apcontinue']
        if 'apnamespace=14' in str(url):
            url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50&apcontinue={}&apnamespace=14' .format(wiki_name, apcont)
        else:
            url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50&apcontinue={}' .format(wiki_name, apcont)
        get_rels(url)


if args.download_pages == 1:
    url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50' .format(wiki_name)
    get_rels(url)


if args.download_categories == 1:
    url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50&apnamespace=14' .format(wiki_name)
    get_rels(url)


############## IMAGES  ############

def dl_images(url_img):
    response = requests.get(url_img, headers=headers)
    data = json.loads(response.text)
    pages = data['query']['allimages']
    for item in pages:
        name = item['name']
        title = item['title']
        url = item['url']
        timestamp = item['timestamp']
        name = re.sub(r'[\;*?!<>|/:"]', '', str(name))
        print(name)
        endpoint = os.path.join('{}_images' .format(wiki_name), name)
        if not os.path.exists(endpoint):
            r = requests.get(url, headers=headers)
            try:
                with open(endpoint, 'wb') as cover_jpg:
                    cover_jpg.write(r.content)
            except Exception as e:
                print(e)
            stuff = name, title, timestamp
            cur.execute('insert or ignore into `{}_images` (name, title, timestamp) VALUES (?,?,?)' .format(wiki_name), (stuff))
            cur.connection.commit()
            time.sleep(delay)
    if 'continue' in data:
        aicont = data['continue']['aicontinue']
        url_img = 'https://{}.fandom.com/api.php?action=query&list=allimages&format=json&export=wikitext&ailimit=500&aicontinue={}' .format(wiki_name, aicont)
        dl_images(url_img)

if args.download_images == 1:
    cur.execute('''CREATE TABLE if not exists {}_images
        (name text, title text, timestamp text)''' .format(wiki_name))
    os.makedirs('{}_images' .format(wiki_name), exist_ok=True)
    url_img = 'https://{}.fandom.com/api.php?action=query&list=allimages&format=json&export=wikitext&ailimit=500' .format(wiki_name)
    dl_images(url_img)
