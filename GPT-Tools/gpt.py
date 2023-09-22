# GPT / OpenAI API for the command line
#
# Commands:
#
# Translate:
# python gpt.py --translate --file "F:\movie.mp4" --start 00:00:00 --end 00:40:00
#
# Image generation from prompt or prompt in file:
#
# python gpt.py --img --name otter3 --prompt "Majestic eagle icon in military cyber style"
# python gpt.py --img --name otter3 --file prompt.txt
#
# Misc:
#
# python .\gpt.py --p --prompt "write a python script to hack the planet"
# python .\gpt.py --p --file ".\prompt.txt"
#
# python .\gpt.py --simple "alien mathematics"
#
# python gpt.py --img --name grunge1 --prompt "abstract picture of something"
#



import os
import requests
import json
import time
import base64
import sqlite3
from PIL import Image
import io
import argparse
import subprocess
from bs4 import BeautifulSoup
import re
from urllib.parse import urlencode

with open('config.txt', 'r') as file:
    token3 = json.load(file)
    token = token3['api_key']

parser = argparse.ArgumentParser()
parser.add_argument('--img', action='store_const', const=1)
parser.add_argument('--translate', action='store_const', const=1)
parser.add_argument('--p', action='store_const', const=1)
parser.add_argument('--simple', type=str, required=False)
parser.add_argument('--name', type=str, required=False)
parser.add_argument('--prompt', type=str, required=False)
parser.add_argument('--file', type=str, required=False)
parser.add_argument('--start', type=str, required=False)
parser.add_argument('--end', type=str, required=False)
parser.add_argument('--lang', type=str, required=False)
args = parser.parse_args()




def prompt_basic(query=None):
    conn = sqlite3.connect('gpt.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE if not exists prompt_suggestions
        (main_question text, question text, answer text, followup text)''')
    headers = {'Authorization': 'Bearer {}' .format(token), 'Content-Type': 'application/json'}
    payload = json.dumps({
    'model': 'gpt-4',
    #'temperature': 0,
    'messages': [
        {
            'role': 'system',
            'content': 'you are a helpful assistant.'
        },
        {
            'role': 'user',
            'content': query
        }
    ]
    })

    url = 'https://api.openai.com/v1/chat/completions'
    res = requests.post(url, headers=headers, data=payload)
    json_data = json.loads(res.content)
    response = json_data['choices'][0]['message']['content']
    print(response)


    with open('prompt_basic.txt', 'a') as file:
        file.write(query)
        file.write(response)
        file.write('\n##############################################\n\n')



def simple(query=None):
    conn = sqlite3.connect('gpt.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE if not exists prompt_suggestions
        (main_question text, question text, answer text, followup text, followupanswer text, keywords text)''')
    headers = {'Authorization': 'Bearer {}' .format(token), 'Content-Type': 'application/json'}
    query_full = "i'm a high scool student and i want to learn all the basics of how {} works. can you suggest 10 prompts i can give chatgpt to learn all the basics \
                 and a 1 sentence answer to each question then ask a relevant followup question to each answer and then list the 5 main relevant keywords for the \
                 answers and followup questions in a comma delimited list?" .format(query)
    headers = {'Authorization': 'Bearer {}' .format(token), 'Content-Type': 'application/json'}
    payload = json.dumps({
    'model': 'gpt-4',
    #'temperature': 0,
    'messages': [
        {
            'role': 'system',
            'content': '''
Prompt system instructions
'''
        },
        {
            'role': 'user',
            'content': query_full
        }
    ]
    })

    url = 'https://api.openai.com/v1/chat/completions'
    res = requests.post(url, headers=headers, data=payload)
    json_data = json.loads(res.content)
    response = json_data['choices'][0]['message']['content']
    dbres = re.split(r'\n\n', response)
    for item in dbres:
        try:
            item2 = re.split(r'\n', item)
            try:
                stuff = query, str(item2[0]), str(item2[1]), str(item2[2]), str(item2[3]), str(item2[4])
            except:
                stuff = query, str(item2[0]), str(item2[1]), str(item2[2]), '', str(item2[4])
            cur.execute('insert into prompt_suggestions (main_question, question, answer, followup, followupanswer, keywords) VALUES (?,?,?,?,?,?)', (stuff))
            cur.connection.commit()
            print(stuff)
        except Exception as e:
            print(e)

    with open('prompt_suggestions.txt', 'a') as file:
        file.write(query)
        file.write(response)
        file.write('\n##############################################\n\n')


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
    image = Image.open(io.BytesIO(base64.b64decode(img_data)))

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
                cmd = 'ffmpeg -y -ss {} -i {} -t {} -vn -ar 44100 -ac 2 -b:a 56k {}' .format(args.start, filename, args.end, file3)
                print(cmd)
                proc = subprocess.Popen(cmd, cwd=cwd, shell=False)
                output, errors = proc.communicate(timeout=950)
                file_size = os.path.getsize(file3)
                print('clip {} created, sending to API' .format(file3))
                headers = {'Authorization': 'Bearer {}' .format(token)}
                url = 'https://api.openai.com/v1/audio/translations'


            else:
                print('file {} not found' .format(filename))

            if os.path.exists(file3):
                if file_size <= 25000000:
                    with open(file3, 'rb') as file:
                        payload = {'model': 'whisper-1', 'response_format': 'srt', 'prompt': 'continue timestamp from 00:50:00,000'}
                        files = {'file': ('file.mp3', file, 'audio/mpeg')}
                        res = requests.post(url, data=payload, files=files, headers=headers)
                        print(res.text)
                        print('Translated text:\n======================')
                        with open(os.path.basename(file3)+'.txt', 'a') as file_txt:
                            file_txt.write(res.text)
                else:
                    print('Clip too long, make it shorter')
    except Exception as e:
        print(e)


if args.translate == 1:
    if args.file == 1:
        filename = args.file
        timestamp_start = args.star
        timestamp_duration = args.end
        if args.lang:
            lang = args.lang
        else:
            lang = None
        translate(filename, timestamp_start, timestamp_duration, lang)
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
        print('Image made')


if args.simple != None:
    simple(args.simple)

if args.p == 1:
    if args.file != None:
        prompt2 = args.file
        f2 = open(prompt2)
        prompt = f2.read()
        f2.close()
        prompt_basic(prompt)
    else:
        if args.prompt != None:
            prompt_basic(args.prompt)


import datetime

def shift_subtitles(filename, shift_time):
    with open(filename, 'r') as file:
        lines = file.readlines()

    shift_time = datetime.timedelta(hours=shift_time[0], minutes=shift_time[1], seconds=shift_time[2])
    new_lines = []
    for line in lines:
        split_line = line.split(' --> ')
        if len(split_line) == 2:
            start_time_str, end_time_str = split_line
            start_time = datetime.datetime.strptime(start_time_str, '%H:%M:%S,%f')
            end_time = datetime.datetime.strptime(end_time_str.strip(), '%H:%M:%S,%f')
            start_time += shift_time
            end_time += shift_time
            new_line = start_time.strftime('%H:%M:%S,%f')[:-3] + ' --> ' + end_time.strftime('%H:%M:%S,%f')[:-3] + '\n'
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(new_lines)


shift_subtitles('movie.mp4_clip.mp3', (0, 40, 00))

