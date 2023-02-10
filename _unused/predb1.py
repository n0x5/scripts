import mysql.connector
import os
from tqdm import tqdm
import sqlite3
import datetime
import pymysql

sect = 'xvid'
conn = sqlite3.connect('divxpre.db' .format(sect))
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists divxpre 
            (release text unique, timeaddedunix int, timeaddedread text, section text, group_name text)''' .format(sect))



db_name = 'allpres'
db_host = 'localhost'
db_user = ''
db_password = ''


sql = 'select * from predb.allpres where rel_section like "%{}%" order by rel_time asc' .format(sect)

conn = pymysql.connect(host=db_host, user=db_user, passwd=db_password, charset ='utf8')
cursor = conn.cursor()
cursor.execute(sql)


lst = []

for item in cursor:
    stuff = item[1], item[6], datetime.datetime.utcfromtimestamp(item[6]).strftime('%Y-%m-%d'), item[3], item[2]
    cur.execute('insert or ignore into divxpre (release, timeaddedunix, timeaddedread, section, group_name) VALUES (?,?,?,?,?)' .format(sect), (stuff))
    cur.connection.commit()
    print(stuff)

cursor.close()
mydb.close()
