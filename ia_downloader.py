# Internet archive collection downloader with title and date metadata filename
# pip install internetarchive

import internetarchive
import time
import requests
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

search = internetarchive.search_items(query='collection:g4video-web')

for item in search.iter_as_items():
    title = item.metadata.get('title').replace(':', '').replace('?', '').replace('/', '')
    try:
        try:
            date = item.metadata.get('date')
        except:
            date = item.metadata.get('year')
        final_name = title+'_'+date+'.mp4'
    except Exception:
        final_name = title+'.mp4'
    download_url = item.urls.download
    if not os.path.isfile(final_name):
        try:
            for item_file in item.files:
                if 'h.264' in item_file['format']:
                    download_url_final = download_url+'/'+item_file['name']
                    print('Downloading: ', download_url_final)
                    r = requests.get(download_url_final, headers=headers)
                    with open(final_name, 'wb') as fn:
                        fn.write(r.content)
                    print(download_url_final)
        except Exception as e:
            print(final_name, 'failed', str(e))
    else:
        print('Skipping', final_name)
