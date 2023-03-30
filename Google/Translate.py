from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import requests
import json
import time
import re
import sqlite3
from tqdm import tqdm

table = 'table_name'

conn = sqlite3.connect('db_name.db')
cur = conn.cursor()
cur.execute('CREATE TABLE if not exists {} (eng_title text unique, ja_title text, photographer text, year text)' .format(table))

scopes = ['https://www.googleapis.com/auth/cloud-platform']
creds = None


if os.path.exists('translate_token.json'):
    creds = Credentials.from_authorized_user_file('translate_token.json', scopes)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
        creds = flow.run_local_server(port=0)
    with open('translate_token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('translate', 'v2', credentials=creds)
    token = service._http.credentials.token
    headers = {'Authorization': 'Bearer {}' .format(token)}
    url_post =  'https://translation.googleapis.com/language/translate/v2'
    with open('lst.txt', 'r', encoding='utf8') as fp:
        for line in tqdm(fp):
            language = 'ja'
            body_post = json.dumps({
                'source': language,
                'target': 'en',
                'q': line
            })
            
            first_post = requests.post(url_post, headers=headers, data=body_post)
            resu = json.loads(first_post.text)
            try:
                translated = resu['data']['translations'][0]['translatedText']
            except:
                translated = ''
            try:
                year2 = re.search(r'(\d{4})', line)
                year = year2.group(1)
            except:
                year = ''
            stuff = translated, line, '', year
            cur.execute('insert or ignore into {} (eng_title, ja_title, photographer, year) VALUES (?,?,?,?)' .format(table), (stuff))
            cur.connection.commit()
            print(stuff)

except Exception as e:
    print(e)

