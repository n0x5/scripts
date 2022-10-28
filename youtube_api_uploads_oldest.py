# command: python3 download_yt.py <uploads_playlistid>
# example: python3 download_yt.py UUcD1pbEB9HNFIVwJih_ZWAA 
import json
import urllib.request
import requests
import subprocess
import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('channel')
args = parser.parse_args()


uploads_playlistid = args.channel


api_key = ''

search_word = ''

list_of_videos = []


def get_url(url2, perpage):
    print(url2)
    response = requests.get(url2)
    data = json.loads(response.text)
    totalresults = data['pageInfo']['totalResults']
    for item in data['items']:
        title = item['snippet']['title']
        date = item['snippet']['publishedAt']
        description = item['snippet']['description']
        thumbnail = item['snippet']['thumbnails']['medium']['url']
        position = item['snippet']['position']
        yt_id = item['snippet']['resourceId']['videoId']
        channel_name = item['snippet']['channelTitle']
        if search_word.lower() in title.lower():
            list_of_videos.append([yt_id, title, date, description, thumbnail, position, channel_name])
    if 'nextPageToken' in data:
        perpage += 50
        print('getting page', data['nextPageToken'], perpage, totalresults)
        url2 = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&pageToken={}&playlistId={}&key={}' .format(data['nextPageToken'], uploads_playlistid, api_key)
        get_url(url2, perpage)
    else:
        pass

    return list_of_videos, channel_name

perpage = 50
url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={}&key={}' .format(uploads_playlistid, api_key)

info = get_url(url, perpage)

channel_name1 = info[1].replace(' ', '_')
channel_name = re.sub(r'[\;*?!<>|/:"]', '', channel_name1)
print(channel_name)



for item in reversed(list_of_videos):
    with open('{}.html' .format(item[6]), 'a', encoding='utf8') as fp:
        fp.write('<div class="video"><img src="{}" /><a href="https://www.youtube.com/watch?v={}">{}</a> - {} - {} </div>' .format(item[4], item[0], item[1], item[2], item[3]))
print('Wrote html file')

