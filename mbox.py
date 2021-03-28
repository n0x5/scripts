# simple script to read .mbox file to sqlite database

import mailbox
import sqlite3


conn = sqlite3.connect('emails.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE if not exists emails
            (sender text, subject text, date_stamp text, message text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')

for message in mailbox.mbox('All mail Including Spam and Trash.mbox'):
    try:
        subject = message['subject']
        sender = message['from']
        date = message['date']
        if message.is_multipart():
            content = ''.join(part.get_payload(decode=True) for part in message.get_payload())
        else:
            content = message.get_payload(decode=True)
        print(sender, subject, date, content)
        cur.execute('insert into emails (sender, subject, date_stamp, message) VALUES (?,?,?,?)', (sender, subject, date, content))
        cur.connection.commit()
    except:
        pass

cur.close()
