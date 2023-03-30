from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import requests
import json
import time
import base64


userid = 'USER@gmail.com'

scopes = ['https://mail.google.com/']
creds = None

if os.path.exists('gmail_token.json'):
    creds = Credentials.from_authorized_user_file('gmail_token.json', scopes)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', scopes)
        creds = flow.run_local_server(port=0)
    with open('gmail_token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('gmail', 'v1', credentials=creds)
    token = service._http.credentials.token
    headers = {'Authorization': 'Bearer {}' .format(token)}

    url4 = 'https://gmail.googleapis.com/gmail/v1/users/{}/messages?q=network' .format(userid)
    res = requests.get(url4, headers=headers)
    data = json.loads(res.text)
    for item in data['messages']:
        msg = 'https://gmail.googleapis.com/gmail/v1/users/{}/messages/{}' .format(userid, item['id'])
        res2 = requests.get(msg, headers=headers)
        data2 = json.loads(res2.text)
        for item2 in data2['payload']['parts']:
            body = base64.urlsafe_b64decode(item2['body']['data'])
            print(body)
        time.sleep(5)


except Exception as e:
    print(e)

