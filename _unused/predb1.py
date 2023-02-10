import mysql.connector
import os
from tqdm import tqdm
import sqlite3
import datetime

sect = 'divx'
conn = sqlite3.connect('{}pre.db' .format(sect))
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists {}pre 
            (release text unique, timeaddedunix int, timeaddedread text, section text, group_name text)''' .format(sect))

db_name = 'allpres'
db_host = 'localhost'
db_user = ''
db_password = ''

mydb = mysql.connector.connect(
host=db_host,
user=db_user,
password=db_password
)

cursor = mydb.cursor()
sql = 'select * from predb2.allpres where rel_section like "%{}%" order by rel_time asc' .format(sect)
cursor.execute(sql)

lst = []

for item in cursor:
    stuff = item[1], item[6], datetime.datetime.utcfromtimestamp(item[6]).strftime('%Y-%m-%d'), item[3], item[2]
    cur.execute('insert or ignore into {}pre (release, timeaddedunix, timeaddedread, section, group_name) VALUES (?,?,?,?,?)' .format(sect), (stuff))
    cur.connection.commit()
    print(stuff)

cursor.close()
mydb.close()
