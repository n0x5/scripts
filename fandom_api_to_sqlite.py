##
## Download fandom.com wiki to sqlite
##
## Command python fandom_api_to_sqlite.py <wiki name> (sub domain portion of fandom.com)
## Example for https://matrix.fandom.com: python fandom_api_to_sqlite.py matrix
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
args = parser.parse_args()

wiki_name = args.wiki
delay = 0

sql_db = os.path.join(os.path.dirname( __file__ ), '{}.db' .format(wiki_name))
conn = sqlite3.connect(sql_db)
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists {}
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
                    cur.executemany('insert or ignore into {} (title, content) VALUES (?,?)' .format(wiki_name), (lst))
                    cur.connection.commit()
                    lst = []

            except Exception as e:
                print(e)

        elem.clear()

        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]

    del context

    cur.executemany('insert or ignore into {} (title, content) VALUES (?,?)' .format(wiki_name), (lst))
    cur.connection.commit()

    time.sleep(delay)

    if 'continue' in data:
        apcont = data['continue']['apcontinue']
        if 'apnamespace=14' in str(url):
            url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50&apcontinue={}&apnamespace=14' .format(wiki_name, apcont)
        if 'apnamespace=10' in str(url):
            url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50&apcontinue={}&apnamespace=10' .format(wiki_name, apcont)
        else:
            url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50&apcontinue={}' .format(wiki_name, apcont)
        get_rels(url)
        time.sleep(delay)

url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50' .format(wiki_name)

get_rels(url)

url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50&apnamespace=14' .format(wiki_name)
get_rels(url)

url = 'https://{}.fandom.com/api.php?action=query&list=allpages&format=json&export=wikitext&aplimit=50&apnamespace=10' .format(wiki_name)
get_rels(url)