# Download a whole website from internet web archive
# Example command:
# python webarchive.py next-episode.net --download
#
# Also supports subfolders:
# python webarchive.py next-episode.net/movies --download
#
# Show only number of results: 
# python webarchive.py next-episode.net --pages
#


import requests
import json
import os
import argparse
import time
import html

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('--pages', action='store_const', const=1)
parser.add_argument('--download', action='store_const', const=1)
args = parser.parse_args()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/49.0'
    }


url_pages = r'http://web.archive.org/cdx/search/cdx?url={}&matchType=prefix&output=json&filter=statuscode:200&collapse=urlkey&fl=timestamp,mimetype,original,urlkey&limit=1000&page=0&showNumPages=true' .format(args.url)



def show_pages():
    r = requests.get(url_pages, headers=headers)
    print('Number of pages: {}, which is about {} results' .format(r.text.strip(), int(r.text.strip()) * 1000))

def download_pages():
    rcount = requests.get(url_pages, headers=headers)
    dl_folder = args.url.replace('/', '_')
    if not os.path.exists(dl_folder):
        os.makedirs(dl_folder)
    for item in range(int(rcount.text.strip())):
        print('Downloading page {} of {} total pages' .format(item, rcount.text.strip()))
        url = r'http://web.archive.org/cdx/search/cdx?url={}&matchType=prefix&output=json&filter=statuscode:200&collapse=urlkey&fl=timestamp,mimetype,original,urlkey&limit=1000&page={}' .format(args.url, item)
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)

        for item_url in data:
            if 'urlkey' not in item_url:
                dl_url = 'https://web.archive.org/web/'+item_url[0]+'if_/'+item_url[2]
                with open('{}_urls.txt' .format(dl_folder), 'a', encoding='utf-8') as fn2:
                    fn2.write(dl_url+'\n')
                url_file = item_url[3].split(')/')

                if url_file is not None:
                    endpoint = os.path.join(os.path.dirname( __file__ ), dl_folder.replace('/', '_'), url_file[1].replace('"', '').replace('\\', '').replace('/', ''))
                    print(dl_url)
                    if not os.path.exists(endpoint) and 'text/html' in item_url[1]:
                        try:
                            r_dl = requests.get(dl_url, headers=headers)
                            with open(endpoint, 'w', encoding='utf-8') as fn:
                                fn.write(r_dl.text)
                                time.sleep(1)
                        except Exception as e:
                            print(e)
                            print('skipping', dl_url)
                    if not os.path.exists(endpoint) and 'image' in item_url[1]:
                        try:
                            r_dl = requests.get(dl_url, headers=headers)
                            with open(endpoint, 'wb') as fn:
                                fn.write(r_dl.content)
                                time.sleep(1)
                        except Exception as e:
                            print(e)
                            print('skipping', dl_url)

if args.pages == 1:
    show_pages()

if args.download == 1 and 'http' not in args.url:
    download_pages()

if 'http' in args.url:
    print("Don't put http:// or https:// in url. https://en.wikipedia.org should be en.wikipedia.org")

