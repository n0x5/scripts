# Internet archive collection downloader with title and date metadata filename


import requests
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }


video_list = []

def get_items(s_url):
    r = requests.get(s_url, headers=headers)
    txt = json.loads(r.text)
    items = txt['items']
    for item in items:
        video_list.append(item['identifier'])
    if 'cursor' in txt:
        print('getting next page', txt['cursor'])
        s_url = r'https://archive.org/services/search/v1/scrape?q=collection%3Ag4video-web&count=10000&cursor={}' .format(txt['cursor'])
        get_items(s_url)

s_url = r'https://archive.org/services/search/v1/scrape?q=collection%3Ag4video-web&count=10000'

get_items(s_url)


for item3 in reversed(video_list):
    m_url = 'https://archive.org/metadata/{}' .format(item3)
    r2 = requests.get(m_url, headers=headers)
    m_txt = json.loads(r2.text)
    meta = m_txt['metadata']
    title = meta['title'].replace(':', '').replace('?', '').replace('/', '').replace('"', '')
    try:
        date = meta['date']
    except Exception:
        pass
    try:
        final_name = title+'_'+date+'.mp4'
    except Exception:
        final_name = title+'.mp4'
    download_url = 'https://archive.org/download/{}' .format(item3)
    files = m_txt['files']
    if not os.path.isfile(final_name):
        try:
            for item_file in files:
                if 'h.264' in item_file['format']:
                    download_url_final = download_url+'/'+item_file['name']
                    print(download_url_final)
                    print('Downloading: ', download_url_final)
                    r = requests.get(download_url_final, headers=headers)
                    with open(final_name, 'wb') as fn:
                        fn.write(r.content)
                    print(final_name)
        except Exception as e:
            print(final_name, 'failed', str(e))
    else:
        print('Skipping', final_name)

