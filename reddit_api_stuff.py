# add reddit saved posts to sqlite3 database

import requests
import os
import json
import time
from datetime import datetime
import sqlite3

conn = sqlite3.connect('reddit_saved.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS reddit_saved (id text unique, dated datetime DEFAULT CURRENT_TIMESTAMP)')

### YOUR API CREDENTIALS ###
secret_token = ''
personal_use_script = ''
username = ''
password = ''
user_agent = 'B0t/0.0.2 by /u/{}' .format(username)
####################


auth = requests.auth.HTTPBasicAuth(personal_use_script, secret_token)
data = {'grant_type': 'password', 'username': username, 'password': password}
headers = {'User-Agent': user_agent}

if os.path.isfile('token.txt'):
    token_file = open('token.txt', 'r', encoding='utf8')
    token = token_file.read()
    token_file.close()
else:
    token = 'blah'
    token_file = open('token.txt', 'w', encoding='utf8')
    token_file.write(token)
    token_file.flush()
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
        tables = []
        entries = []
        for item2 in item['data']:
            tables.append(str(item2))
            entries.append(str(item['data'][item2]))
            if item2 == 'id':
                pass
            else:
                sql = 'ALTER TABLE reddit_saved ADD {} text' .format(item2)
            try:
                cur.execute(sql)
                cur.connection.commit()
            except Exception:
                pass
                #print('duplicate column')

        table2 = ', '.join(tables)
        entries3 = tuple(entries)
        nr = '?,' * len(entries3)
        nr2 = str(nr)[:-1]
        sql2 = 'insert into reddit_saved ({}) VALUES ({})' .format(table2, nr2)
        try:
            cur.execute(sql2, (entries3))
            cur.connection.commit()
        except Exception:
            print('Duplicate detected - skipping')
        print(entries3)


    if data['data']['after']:
        after = data['data']['after']
        payload = {'after': after, 'count': '50'}
        time.sleep(2)
        print(payload)
        get_url(url, payload)
    

url = 'https://oauth.reddit.com/user/{}/saved' .format(username)
payload = {'count': '50'}

get_url(url, payload)
