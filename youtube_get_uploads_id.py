# python3 get_uploads_id.py https://www.youtube.com/user/CNN
# python3 get_uploads_id.py https://www.youtube.com/channel/UCupvZG-5ko_eiXAupbDfxWw
# python3 get_uploads_id.py https://www.youtube.com/CNN

import json
import urllib.request
import requests
import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('channel')
args = parser.parse_args()


url1 = 'https://www.googleapis.com/youtube/v3/'



api_key = ''


list_of_videos = []

def get_id_by_username_search(user_name_search):
    url = url1+'search?part=id%2Csnippet&maxResults=1&q={}&type=channel&key={}' .format(user_name_search, api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    for item in data['items']:
        channel_id = item['snippet']['channelId']
        title = item['snippet']['title']
        get_info_id(channel_id)

def get_id_by_channel_id(user_name):
    url = url1+'channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={}&key={}' .format(user_name, api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    for item in data['items']:
        channel_id = item['id']
        title = item['snippet']['title']
        get_info_id(channel_id)


def get_info_id(user_id):
    def get_url(url2):
        print(url2)
        response = requests.get(url2)
        data = json.loads(response.text)
        for item in data['items']:
            #print(item)
            channel_id = item['id']
            name = item['snippet']['title']
            description = item['snippet']['description']
            p_id = item['contentDetails']['relatedPlaylists']['uploads']
            viewcount = item['statistics']['viewCount']
            try:
                subcount = item['statistics']['subscriberCount']
            except:
                subcount = 'Hidden'
            date_established = item['snippet']['publishedAt']
            videocount = item['statistics']['videoCount']
            try:
                customurl = item['snippet']['customUrl']
            except:
                customurl = 'Null'
            chanid = 'https://www.youtube.com/channel/'
            print('')
            print('============')
            print('Channel ID:', chanid+channel_id)
            print('Name:', name)
            print('Custom url:', customurl)
            print('Created:', date_established.replace('T', ' ').replace('Z', ' '))
            try:
                print('Description:', description)
            except:
                print('Description:', description.encode("utf-8"))
            print('-----------------')
            print('Uploads playlist ID:', p_id)
            print('-----------------')
            print('Statistics: View Count: {}, Subscriber count: {}, Video count: {}' .format(viewcount, subcount, videocount))
            print('============')
            print('')
            url_id = url1+'channels?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}' .format(p_id, api_key)
        else:
            pass


    url_id = url1+'channels?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}' .format(user_id, api_key)
    get_url(url_id)


if '/channel/' in args.channel:
    channel2 = args.channel.split('/')
    channelid = channel2[4]
    get_info_id(channelid)

if '/channel/' not in args.channel and '/c/' not in args.channel and '/user/' not in args.channel:
    channel2 = args.channel.split('/')
    nameid = channel2[3]
    try:
        get_id_by_channel_id(nameid)
    except KeyError:
        get_id_by_username_search(nameid)

if '/c/' in args.channel:
    channel2 = args.channel.split('/')
    nameid = channel2[4]
    try:
        get_id_by_channel_id(nameid)
    except KeyError:
        get_id_by_username_search(nameid)

if '/user/' in args.channel and '/channel/' not in args.channel and '/c/' not in args.channel:
    channel2 = args.channel.split('/')
    nameid = channel2[4]
    try:
        get_id_by_channel_id(nameid)
    except KeyError:
        get_id_by_username_search(nameid)


