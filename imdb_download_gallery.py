# download gallery from imdb
# example command: python imdb_download_gallery.py https://www.imdb.com/title/tt0478970/mediaindex/

import requests
import os
import argparse
from bs4 import BeautifulSoup
import re

parser = argparse.ArgumentParser()
parser.add_argument('url')
args = parser.parse_args()
url = args.url

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
rel1 = soup.find('div', attrs={'class': 'media_index_thumb_list'})
lists = rel1.find_all('img', src=re.compile(r'm.media-amazon.com'))
for item in lists:
    dl_url2 = item['src']
    final_url = re.sub(r'@(.+?).jpg', '@@._V1.jpg', dl_url2)
    r = requests.get(final_url, headers=headers)
    if len(r.content) == 9:
        final_url = re.sub(r'@(.+?).jpg', '@._V1.jpg', dl_url2)
        r = requests.get(final_url, headers=headers)
    fn = os.path.basename(final_url)
    with open(fn, 'wb') as cover_jpg:
        cover_jpg.write(r.content)
