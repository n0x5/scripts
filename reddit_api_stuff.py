import requests
import os
import json
import time
from datetime import datetime


### YOUR API CREDENTIALS ###
secret_token = ''
personal_use_script = ''
username = ''
password = ''
user_agent = 'nuB0t/0.0.2 by /u/{}' .format(username)
####################


auth = requests.auth.HTTPBasicAuth(personal_use_script, secret_token)
data = {'grant_type': 'password', 'username': username, 'password': password}
headers = {'User-Agent': user_agent}

token_file = open('token.txt', 'r', encoding='utf8')
token = token_file.read()
token_file.close()

headers = {**headers, **{'Authorization': 'bearer {}' .format(token)}}
res2 = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

if res2.status_code == 401:
    print('getting new token')
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    token_file2 = open('token.txt', 'w', encoding='utf8')
    token = res.json()['access_token']
    headers = {**headers, **{'Authorization': 'bearer {}' .format(token)}}
    token_file2.write(token)
    token_file2.flush()
    token_file2.close()


def get_url(url, payload):
    res = requests.get(url, headers=headers, params=payload)
    data = json.loads(res.text)
    for item in data['data']['children']:
        print('################ ENTRY ####################')
        for item2 in item['data']:
            print(item2, ':', item['data'][item2])

    if data['data']['after']:
        after = data['data']['after']
        payload = {'after': after, 'count': '50'}
        print(payload)
        get_url(url, payload)
        time.sleep(1)

url = 'https://oauth.reddit.com/user/{}/saved' .format(username)
payload = {'count': '50'}

get_url(url, payload)
