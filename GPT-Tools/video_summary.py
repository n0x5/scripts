# Summarize videos from youtube and other sites downloaded with yt-dlp
# create a config.txt file following the template in the github repo and fill in API key
# Command:
# 
# python summary_video.py https://www.youtube.com/watch?v=WqkXif816-8
#

import os
import requests
import io
import argparse
import subprocess
import re
import datetime
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument('url')
args = parser.parse_args()

url = args.url

with open('config.txt', 'r') as file:
    token3 = json.load(file)
    token = token3['api_key']



def gen_stuff(file3, timestamp):
    with open(file3, 'rb') as file:
        headers = {'Authorization': 'Bearer {}' .format(token)}
        payload = {'model': 'whisper-1', 'response_format': 'text'}
        files = {'file': ('file.mp3', file, 'audio/mpeg')}
        url = 'https://api.openai.com/v1/audio/translations'
        res = requests.post(url, data=payload, files=files, headers=headers)

        with open('scribe.txt', 'w') as file_txt:
            file_txt.write(res.text)

    with open('scribe.txt', 'r') as file44:
        query_full = file44.read()

    headers = {'Authorization': 'Bearer {}' .format(token), 'Content-Type': 'application/json'}
    payload = json.dumps({
    'model': 'gpt-3.5-turbo',
    'messages': [
        {
            'role': 'system',
            'content': '''Summarize text.
    '''
        },
        {
            'role': 'user',
            'content': '''
    Summarize the following text in1 sentence. List the top 5 keywords of the topics in the text in a comma-delimited list within parentheses. Use the following steps to generate the response:

    Here are examples of a response:
    `<Summary text> (<comma delimited list of keywords>)
    The hosts talk about linux and macos. (linux, macos, computers)
    CPU's and motherboards are mentioned. (cpu, motherboards, hardware)
    The hosts talk about bill gates and windows. (bill gates, windows, software, operating systems)
    `
    The text:
    {}
    ''' .format(query_full)
        }
    ]
    })

    url = 'https://api.openai.com/v1/chat/completions'
    res = requests.post(url, headers=headers, data=payload)
    print(res.text)
    json_data = json.loads(res.content)
    response = json_data['choices'][0]['message']['content']
    print(timestamp+' '+response)
    with open('{}.txt', 'a') as file_resp:
        file_resp.write(str(timestamp)+' '+response+'\n\n')

def shift_subtitles(shift_time, timestamp):
    shift_time = datetime.timedelta(hours=shift_time[0], minutes=shift_time[1], seconds=shift_time[2])
    start_time = datetime.datetime.strptime(timestamp, '%H:%M:%S,%f')
    start_time += shift_time
    timestamp = start_time.strftime('%H:%M:%S,%f')[:-3]
    return timestamp

upload = r'video_summaries'
timestamp = '00:00:00,000'

if not os.path.exists('video_summaries'):
    os.makedirs('video_summaries')

filestrip = re.sub(r'[\;*?!<>|/:\."=]', '', str(url))


cwd_final = os.path.join(os.path.dirname( __file__ ), 'video_summaries', filestrip)
if not os.path.exists(cwd_final):
    os.makedirs(cwd_final)
cwd = os.chdir(cwd_final)
cmd = 'yt-dlp -f 139 {}' .format(url)
os.system(cmd)

time.sleep(1)

for subdir, dirs, files in os.walk(cwd_final):
    for fn in files:
        if '.m4a' in fn:
            os.chdir(subdir)
            cmd_spl = r'ffmpeg -i "{}" -c copy -map 0 -segment_time 00:10:00 -f segment output%03d.mp4' .format(os.path.join(subdir, fn))
            os.system(cmd_spl)


for subdir, dirs, files in os.walk(cwd_final):
    for fn in files:
        if 'output' in fn:
            final_path = os.path.join(subdir, fn)
            if 'output000' in fn:
                timestamp = '00:00:00,000'
            else:
                timestamp = shift_subtitles((0, 10, 00,000), timestamp)
            gen_stuff(final_path, timestamp)
            print(timestamp, final_path)

