# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import requests
import json



scopes = ['https://www.googleapis.com/auth/photoslibrary']
creds = None

if os.path.exists('photos_token.json'):
    creds = Credentials.from_authorized_user_file('photos_token.json', scopes)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
        creds = flow.run_local_server(port=0)
    with open('photos_token.json', 'w') as token:
        token.write(creds.to_json())


service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
token = service._http.credentials.token
headers = {'Authorization': 'Bearer {}' .format(token)}
url4 = 'https://photoslibrary.googleapis.com/v1/mediaItems'
res = requests.get(url4, headers=headers)
data = json.loads(res.text)
print(res.text)
