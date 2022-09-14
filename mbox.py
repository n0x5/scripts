# simple script to read .mbox file to sqlite database

import mailbox
from email.parser import BytesParser
from email.policy import default
import sqlite3
import time
import datetime
import tqdm

conn = sqlite3.connect('alt_cyberpunk.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE if not exists emails
            (sender text, subject text, date_stamp text, u_stamp text, message text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')

lst = []
for message in tqdm.tqdm(mailbox.mbox('alt.cyberpunk.mbox', factory=BytesParser(policy=default).parse)):
    try:
        subject = message['subject']
        sender = message['from']
        date = message['date']
        try:
            u_stamp = datetime.datetime.strptime(message['date'], '%a, %d %b %Y %H:%M:%S %z')
        except:
            u_stamp = 'Null'
        if message.is_multipart():
            try:
                content = ''.join(part.get_payload(decode=False) for part in message.get_payload())
            except Exception:
                content = ''
        else:
            try:
                content = message.get_payload(decode=False)
            except Exception:
                content = ''
        stuff = str(sender), str(subject), str(date), str(u_stamp), content
        lst.append(stuff)
        if len(lst) == 500:
            cur.executemany('insert into emails (sender, subject, date_stamp, u_stamp, message) VALUES (?,?,?,?,?)', (lst))
            cur.connection.commit()
            lst = []
    except Exception as e:
        print(e)

cur.executemany('insert into emails (sender, subject, date_stamp, u_stamp, message) VALUES (?,?,?,?,?)', (lst))
cur.connection.commit()

cur.close()


