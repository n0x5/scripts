### GPT / OpenAI API for the command line
### 
### Commands:
###
### Translation from a video file (need FFMPEG):
###
### python gpt.py --translate --file "F:\gpt\Movie Name (2012).mp4" --start 00:11:13 --end 00:00:15
### _File paths with spaces in the path/file name need quotes as shown above_

### Image generation from prompt or prompt in file:
###
### python gpt.py --img --name otter3 --prompt "Majestic eagle icon in military cyber style"
### python gpt.py --img --name otter3 --file prompt.txt


import os
import requests
import json
import time
import base64
from tqdm import tqdm
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import io
import argparse
import subprocess


with open('config.txt', 'r') as file:
    token3 = json.load(file)
    token = token3['api_key']

parser = argparse.ArgumentParser()
parser.add_argument('--img', action='store_const', const=1)
parser.add_argument('--translate', action='store_const', const=1)
parser.add_argument('--name', type=str, required=False)
parser.add_argument('--prompt', type=str, required=False)
parser.add_argument('--file', type=str, required=False)
parser.add_argument('--start', type=str, required=False)
parser.add_argument('--end', type=str, required=False)
parser.add_argument('--lang', type=str, required=False)
args = parser.parse_args()


def image(filename=None, prompt=None):
    filename = os.path.join(os.getcwd(), filename)
    headers = {'Authorization': 'Bearer {}' .format(token), 'Content-Type': 'application/json'}
    payload = json.dumps({
    'prompt': prompt,
    'n': 1,
    'size': '1024x1024',
    'response_format': 'b64_json'
    })

    url = 'https://api.openai.com/v1/images/generations'
    res = requests.post(url, headers=headers, data=payload)
    json_data = json.loads(res.content)
    img_data = json_data['data'][0]['b64_json']
    created = json_data['created']
    image = Image.open(BytesIO(base64.b64decode(img_data)))

    if filename != None:
        digit = 1
        filename2 = filename+'_'+str(digit)+'.png'
        if os.path.exists(filename2):
            while os.path.exists(filename2):
                digit += 1
                filename2 = filename+'_'+str(digit)+'.png'

    else:
        filename2 = str(created)+'.png'
        image.save(filename2, format='PNG')

    image.save(filename2, format='PNG')

def translate(filename=None, timestamp_start=None, timestamp_duration=None, lang=None):
    try:
        cwd = os.getcwd()
        filename = args.file
        filename2 = os.path.basename(filename)
        timestamp_start = timestamp_start
        timestamp_duration = timestamp_duration
        lang = args.lang

        if filename:
            file3 = filename+'_clip.mp3'
            if os.path.exists(filename):
                print('Encoding portion of file {}' .format(filename))
                cmd = 'ffmpeg -y -ss {} -i {} -t {} -vn -ar 44100 -ac 2 -b:a 192k {}' .format(args.start, filename, args.end, file3)
                proc = subprocess.Popen(cmd, cwd=cwd, shell=False)
                output, errors = proc.communicate(timeout=950)
                file_size = os.path.getsize(file3)
                print('clip {} created, sending to API' .format(file3))
                headers = {'Authorization': 'Bearer {}' .format(token)}
                url = 'https://api.openai.com/v1/audio/translations'
                payload = {'model': 'whisper-1'}
            else:
                print('file {} not found' .format(filename))

            if os.path.exists(file3):
                if file_size <= 25000000:
                    with open(file3, 'rb') as file:
                        files = {'file': ('file.mp3', file, 'audio/mpeg')}
                        res = requests.post(url, data=payload, files=files, headers=headers)
                        json_data = json.loads(res.content)
                        txt = json_data['text']
                        print('Translated text:\n======================')
                        print(txt)
                        with open(os.path.basename(file3)+'.txt', 'a') as file_txt:
                            file_txt.write('\n\n##########################\n\n')
                            file_txt.write(txt)
                else:
                    print('Clip too long, make it shorter')
    except:
        print('Please provide file with --file')

if args.translate == 1:
    if args.file == 1:
        filename = args.file
        timestamp_start = args.star
        timestamp_duration = args.end
        if args.lang:
            lang = args.lang
        else:
            lang = None
        translate(filename, timestamp_start, timestamp_duration, land)
    else:
        translate()

if args.img == 1:
    try:
        filename = args.name
    except:
        filename = None

    if args.prompt != None:
        prompt = args.prompt
        image(filename, prompt)

    if args.file != None:
        prompt2 = args.file
        f2 = open(prompt2)
        prompt = f2.read()
        f2.close()
        if len(prompt) <= 1000:
            image(filename, prompt)
        else:
            print('Prompt too long ({}/1000 characters). Please make it under 1000 characters.' .format(len(prompt)))

    else:
        print('Please provide a prompt')


