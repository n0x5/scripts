import json
import urllib.request
import requests
import subprocess
import os
import re


download_directory = r'C:\youtube_archive'

uploads_playlistid = 'UUBMvc6jvuTxH6TNo9ThpYjg' # ubisoft id

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/49.0'
    }

api_key = ''

list_of_videos = []

def get_url(url2):
    response = requests.get(url2, headers=headers)
    data = json.loads(response.text)
    for item in data['items']:
        title = item['snippet']['title']
        yt_id = item['snippet']['resourceId']['videoId']
        list_of_videos.append(yt_id)
        print(yt_id, title)
    if 'nextPageToken' in data:
        print('getting page', data['nextPageToken'])
        url2 = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=25&pageToken={}&playlistId={}&key={}' .format(data['nextPageToken'], uploads_playlistid, api_key)
        get_url(url2)
    else:
        pass

    return list_of_videos

url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=25&playlistId={}&key={}' .format(uploads_playlistid, api_key)
get_url(url)

list_of_local = []

for subdir, dirs, files in os.walk(download_directory):
    for fn2 in files:
        list_of_local.append(fn2)

for fn3 in list_of_local:
    for fn4 in list_of_videos:
        if fn4 in fn3:
            list_of_videos.remove(fn4)

print('new videos/videos you dont have')
print('======')
for item1 in list_of_videos:
    print(item1)
print('======')

for item3 in list_of_videos:
    video_final = 'https://www.youtube.com/watch?v={}' .format(item3)
    print(video_final)
    subprocess.run(['youtube-dl', '{}' .format(video_final)], cwd=download_directory)

print('all videos downloaded / no new videos')
