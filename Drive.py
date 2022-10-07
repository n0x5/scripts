from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import requests
import json


scopes = ['https://www.googleapis.com/auth/drive']
creds = None

if os.path.exists('drive_token.json'):
    creds = Credentials.from_authorized_user_file('drive_token.json', scopes)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', scopes)
        creds = flow.run_local_server(port=0)
    with open('drive_token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('drive', 'v3', credentials=creds)
    token = service._http.credentials.token
    headers = {'Authorization': 'Bearer {}' .format(token)}
    url4 = 'https://www.googleapis.com/drive/v3/files'
    res = requests.get(url4, headers=headers)
    data = json.loads(res.text)
    print(res.text)


except Exception as e:
    print(e)

