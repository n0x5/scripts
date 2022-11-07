# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import requests
import json
import base64

with open('Weihnachtsgeschichte_1.jpg', 'rb') as img_file:
    string = base64.b64encode(img_file.read())

body_post = json.dumps({
  "requests": [
    {
      "image": { "content": string.decode('utf-8')},
        "features": [
            { "type": "LABEL_DETECTION" },
            { "type": "SAFE_SEARCH_DETECTION" },
            { "type": "IMAGE_PROPERTIES" },
            { "type": "WEB_DETECTION" }
        ]
    }
  ]
})

def vision(jdata):
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
    first_post = requests.post(url_post, headers=headers, data=body_post)
    print(first_post.text)
    data = json.loads(first_post.text)
    adult = data['responses'][0]['safeSearchAnnotation']['adult']
    violence = data['responses'][0]['safeSearchAnnotation']['violence']
    racy = data['responses'][0]['safeSearchAnnotation']['racy']
    labels = data['responses'][0]['labelAnnotations']
    labels2 = [[item['description'], item['score']] for item in labels]
    web = data['responses'][0]['webDetection']
    web_labels = web['bestGuessLabels'][0]['label']
    web_urls = [item2['url'] for item2 in web['visuallySimilarImages']]
    results = labels2, web_labels, web_urls
    return results

result = vision(body_post)
print(result)
