# simple script to read .mbox file to sqlite database

import mailbox
import sqlite3
import time
import datetime

conn = sqlite3.connect('emails.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE if not exists emails
            (sender text, subject text, date_stamp text, u_stamp text, message text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')

for message in mailbox.mbox('All mail Including Spam and Trash.mbox'):
    try:
        subject = message['subject']
        sender = message['from']
        date = message['date']
        u_stamp = datetime.datetime.strptime(message['date'], '%a, %d %b %Y %H:%M:%S %z')
        if message.is_multipart():
            content = ''.join(part.get_payload(decode=True) for part in message.get_payload())
        else:
            content = message.get_payload(decode=True)
        print(sender, subject, date, u_stamp, content)
        cur.execute('insert into emails (sender, subject, date_stamp, u_stamp, message) VALUES (?,?,?,?,?)', (sender, subject, date, u_stamp, content))
        cur.connection.commit()
    except:
        pass

cur.close()
