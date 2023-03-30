# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import requests
import json


string = '<p></p><a href="imgtest.jpg">Hey there</a>'

post_title = 'Second post'

body_post = json.dumps({
    'title': post_title,
    'content': string
})

blogid = ''

scopes = ['https://www.googleapis.com/auth/blogger']
creds = None

if os.path.exists('blogger_token.json'):
    creds = Credentials.from_authorized_user_file('blogger_token.json', scopes)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
        creds = flow.run_local_server(port=0)
    with open('blogger_token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('blogger', 'v3', credentials=creds)
    token = service._http.credentials.token
    headers = {'Authorization': 'Bearer {}' .format(token)}
    url4 = 'https://www.googleapis.com/blogger/v3/blogs/{}/posts' .format(blogid)
    res = requests.get(url4, headers=headers)
    data = json.loads(res.text)
    print('Making a test post!')
    url_post =  'https://www.googleapis.com/blogger/v3/blogs/{}/posts' .format(blogid)
    first_post = requests.post(url4, headers=headers, data=body_post)
    print(first_post, first_post.text)

except Exception as e:
    print(e)

