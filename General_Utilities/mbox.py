# simple script to read .mbox file to sqlite database

import mailbox
from email.parser import BytesParser
from email.policy import default
import sqlite3
import time
import datetime
import tqdm


conn = sqlite3.connect('alt_tv_startrek_voyager.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE if not exists emails
            (sender text, subject text, date_stamp text, u_stamp text, message text, thread text)''')

lst = []
for message in tqdm.tqdm(mailbox.mbox('alt.tv.star-trek.voyager.mbox', factory=BytesParser(policy=default).parse)):
    try:
        subject = message['subject']
        sender = message['from']
        date = message['date']
        try:
            thread_id = message['X-Google-Thread'].split(',')[1]
        except Exception:
            thread_id = 'Null'
        try:
            u_stamp = datetime.datetime.strptime(message['date'], '%a, %d %b %Y %H:%M:%S %z')
        except:
            try:
                u_stamp = datetime.datetime.strptime(message['date'], '%Y/%m/%d')
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
        stuff = str(sender), str(subject), str(date), str(u_stamp), content, thread_id
        lst.append(stuff)
        if len(lst) == 2000:
            cur.executemany('insert into emails (sender, subject, date_stamp, u_stamp, message, thread text) VALUES (?,?,?,?,?,?)', (lst))
            cur.connection.commit()
            lst = []
    except Exception as e:
        print(e)

cur.executemany('insert into emails (sender, subject, date_stamp, u_stamp, message, thread) VALUES (?,?,?,?,?,?)', (lst))
cur.connection.commit()

cur.close()


