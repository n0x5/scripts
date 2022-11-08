# Upload image to Google Vision for image recognition
# Scan a folder recursively or give path to single file and write .json info in same folder
# Need Desktop App oauth2 credentials.json file in same folder
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import requests
import json
import base64
import argparse
import mimetypes


parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=False)
parser.add_argument('--folder', type=str, required=False)
args = parser.parse_args()
count = ['1']

def scan_folder(folder):
    for subdir, dirs, files in os.walk(folder):
        for fn in files:
            fullpath = os.path.join(subdir, fn)
            mime2 = mimetypes.guess_type(fullpath)
            if 'image' in mime2[0]:
                single_image(fullpath)

def single_image(img):
    with open(img, 'rb') as img_file:
        string = base64.b64encode(img_file.read())

    body_post = json.dumps({
        "requests": [{
            "image": { "content": string.decode('utf-8') },
            "features": [
                { "type": "LABEL_DETECTION" },
                { "type": "SAFE_SEARCH_DETECTION" },
                { "type": "WEB_DETECTION" }
            ]
        }]
    })
    full_path = os.path.splitext(img)
    file3 = os.path.basename(img)
    file2 = os.path.splitext(file3)
    endpoint = full_path[0]+'.json'
    if not os.path.exists(endpoint):
        vision(body_post, img)
        count.append(img)
    else:
        print('json file {} already exists!' .format(endpoint))

def vision(jdata, img):
    scopes = ['https://www.googleapis.com/auth/cloud-vision']
    creds = None

    if os.path.exists('vision_token.json'):
        creds = Credentials.from_authorized_user_file('vision_token.json', scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        with open('vision_token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('vision', 'v1', credentials=creds)
    token = service._http.credentials.token
    headers = {'Authorization': 'Bearer {}' .format(token)}
    url_post =  'https://vision.googleapis.com/v1/images:annotate'
    first_post = requests.post(url_post, headers=headers, data=jdata)
    print(first_post.text)
    print('{} API requests so far' .format(len(count)))
    full_path = os.path.splitext(img)
    file3 = os.path.basename(img)
    file2 = os.path.splitext(file3)
    endpoint = full_path[0]+'.json'
    with open(endpoint, 'w', encoding='utf-8') as token:
        token.write(first_post.text)


if args.file != None:
    single_image(args.file)

if args.folder != None:
    scan_folder(args.folder)

if args.folder == None and args.file == None:
    print('Scan a folder recursively with --folder')
    print('Or a single file with --file')

