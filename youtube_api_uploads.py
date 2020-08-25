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


streams_directory = r'G:\yt_live'



uploads_playlistid = args.channel

download_root = r'C:\video'


api_key = ''

search_word = ''

list_of_videos = []


def get_url(url2):
    print(url2)
    response = requests.get(url2)
    data = json.loads(response.text)
    for item in data['items']:
        title = item['snippet']['title']
        yt_id = item['snippet']['resourceId']['videoId']
        channel_name = item['snippet']['channelTitle']
        if search_word.lower() in title.lower():
            list_of_videos.append(yt_id)
            try:
                print(yt_id, title)
            except:
                print(yt_id, title.encode("utf-8"))
    if 'nextPageToken' in data:
        print('getting page', data['nextPageToken'])
        url2 = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=25&pageToken={}&playlistId={}&key={}' .format(data['nextPageToken'], uploads_playlistid, api_key)
        get_url(url2)
    else:
        pass

    return list_of_videos, channel_name

url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=25&playlistId={}&key={}' .format(uploads_playlistid, api_key)

info = get_url(url)

channel_name1 = info[1].replace(' ', '_')
channel_name = re.sub(r'[\;*?!<>|/:"]', '', channel_name1)
print(channel_name)

download_directory = os.path.join(download_root, channel_name)
if not os.path.exists(download_directory): 
    os.makedirs(download_directory)

list_of_local = []



for subdir, dirs, files in os.walk(download_root):
    for fn2 in files:
        list_of_local.append(fn2)


for fn3 in list_of_local:
    for fn4 in list_of_videos:
        if fn4 in fn3 and not fn3.endswith('.part') and not fn3.endswith('.ytdl') and not fn3.endswith('.webp') and not fn3.endswith('.jpg'):
            list_of_videos.remove(fn4)

print('new videos/videos you dont have')
print('======')
for item1 in list_of_videos:
    print(item1)
print('======')

for item3 in list_of_videos:
    video_final = 'https://www.youtube.com/watch?v={}' .format(item3)
    if os.name == 'nt':
        proc = subprocess.Popen(['youtube-dl', '--write-all-thumbnails', '--match-filter', '!is_live', '{}' .format(video_final)], cwd=download_directory, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        proc = subprocess.Popen(['youtube-dl --match-filter !is_live {}' .format(video_final)], cwd=download_directory, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        print('RUNNING YOUTUBE-DL:')
        print('###############')
        output, errors = proc.communicate(timeout=950)
        print('|||', output.decode("utf-8"))
        print('///', errors.decode("utf-8"))
        print('###############')
        if 'skipping' in str(output).lower():
            if not os.path.exists(streams_directory): 
                os.makedirs(streams_directory)
            print(item3, 'video is a live stream, capturing separately')
            file_format = r'%(title)s-%(id)s.%(ext)s'
            final_cmd = 'start cmd /k youtube-dl -o "{}" {}' .format(streams_directory+'\\'+file_format, video_final)
            final_cmd2 = "gnome-terminal -e 'youtube-dl -o {} {}'" .format(streams_directory+'\\'+file_format, video_final)
            if os.name == 'nt':
                os.system(final_cmd)
            else:
                os.system(final_cmd2)
        if 'error' in str(errors).lower() and not 'premiere' in str(errors).lower():
            with open(os.path.join(download_root, 'errors.txt'), 'a') as error_file:
                print('unable to download:', video_final, 'logged to errors.txt')
                error_file.write(video_final+'\n')

    except Exception as e:
        print(e)
        proc.kill()
        output, errors = proc.communicate()


print('all videos downloaded / no new videos')
