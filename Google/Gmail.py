# Gmail API to sqlite3 database
# change userid to yourusername@gmail.com
# Need credentials.json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import requests
import json
import time
import base64
from tqdm import tqdm
import sqlite3

conn = sqlite3.connect('gmail_api.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists gmail
        (id_msg text unique, labelids text, threadid text, snippet text, recipient text, from_sender text, subject text, date_sent text, body text, internaldate int, json_data text)''')

userid = 'USER@gmail.com'

scopes = ['https://mail.google.com/']
creds = None

if os.path.exists('gmail_token.json'):
    creds = Credentials.from_authorized_user_file('gmail_token.json', scopes)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
        creds = flow.run_local_server(port=0)
    with open('gmail_token.json', 'w') as token:
        token.write(creds.to_json())

def parse(nextpage=None):
    try:
        service = build('gmail', 'v1', credentials=creds)
        token = service._http.credentials.token
        headers = {'Authorization': 'Bearer {}' .format(token)}
        payload = {'pageToken': nextpage}
        url4 = 'https://gmail.googleapis.com/gmail/v1/users/{}/messages/' .format(userid)
        if nextpage:
            res = requests.get(url4, headers=headers, params=payload)
        else:
            res = requests.get(url4, headers=headers)
        data = json.loads(res.text)
        for item in tqdm(data['messages']):
            try:
                msg = 'https://gmail.googleapis.com/gmail/v1/users/{}/messages/{}' .format(userid, item['id'])
                res2 = requests.get(msg, headers=headers)
                data2 = json.loads(res2.content)
                data3 = res2.text
                threadid = data2['threadId']
                id_msg = data2['id']
                labelids = str(data2['labelIds'])
                snippet = data2['snippet']
                internaldate = data2['internalDate']

                try:
                    body = base64.urlsafe_b64decode(data2['payload']['parts'][1]['body']['data'])
                except Exception:
                    for item2 in data2['payload']['parts']:
                        body += base64.urlsafe_b64decode(item2['body']['data'])

                for item3 in data2['payload']['headers']:
                    if 'To' in item3['name']:
                        to = item3['value']
                    if 'From' in item3['name']:
                        from_sender = item3['value']
                    if 'Subject' in item3['name']:
                        subject = item3['value']
                    if 'Date' in item3['name']:
                        date = item3['value']
                stuff = id_msg, labelids, threadid, snippet, to, from_sender, subject, date, body, int(internaldate), str(data3)
                stuff2 = id_msg, labelids, threadid, snippet, to, from_sender, subject, date, int(internaldate)
                cur.execute('insert or ignore into gmail (id_msg, labelids, threadid, snippet, recipient, from_sender, subject, date_sent, body, internaldate, json_data) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (stuff))
                cur.connection.commit()
                print(stuff2)
            except Exception as e:
                print(e)
                pass

        nextpage = data['nextPageToken']
        if 'nextPageToken' in data:
            parse(nextpage)

    except Exception as e:
        print(e)

parse()

