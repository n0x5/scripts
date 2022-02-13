# Wiki2sql
# Convert wikia .xml to sqlite db


import xml.etree.ElementTree as ET
import os
import re
import sqlite3
from tqdm import tqdm

xmlfile = 'residentevil_pages_current.xml'

tree = ET.parse(xmlfile)
root = tree.getroot()

db_name = xmlfile.replace('_pages_current.xml', '.db')
db_name2 = db_name.replace('.db', '')
conn = sqlite3.connect(db_name)
cur = conn.cursor()
sql3 = r'CREATE TABLE IF NOT EXISTS {} (title text, content text, dated datetime DEFAULT CURRENT_TIMESTAMP)' .format(db_name2)
cur.execute(sql3)

items = ([''])


for elem in tqdm(root.iter()):
    try:
        stuff1 = elem.text.split(':')[0]
    except Exception as e:
        items = ([''])
        stuff1 = elem.text

    if '/}title' in elem.tag and elem.text is not None and stuff1 not in items:
        filestrip = re.sub(r'[\;*?!<>|\/:"\\\]\[]', '', elem.text)
        fname = (os.path.join(filestrip+'.html'))
        title = re.sub('[/:"]', '', elem.text)
        file3 = str(xmlfile).replace('.', '_')
        if not os.path.exists(file3):
            os.makedirs(file3)
        try:
            pass
            #print(fname)
        except Exception as e:
            print(str(e))

    if '/}text' in elem.tag and elem.text is not None:
        
        links = re.sub(r'\[\[(.+?)\]\]', r'<a href="\1.html">\1</a>', elem.text)
        links2 =  re.sub(r'[][]', '', links)
        if 'File:' in links:
            links2 = re.sub(r'\[\[File:(.*?)\|.+\]\]', r'<img width="250px" src="images/\1" />', elem.text.replace('_', ' '))
        if ':' in links2:
            links2 = re.sub(r':', r'', links2)
        if '#' in links2:
            links2 = re.sub(r'#[\w\s\|\_\:\-]+', r'', links2)
        if '|' in links2:
            links2 = re.sub(r'[\|][\w\s\|\_\:\-]+', r'', links2)
        stuff = title, links2
        cur.execute('insert into {} (title, content) VALUES (?,?)' .format(db_name2), (stuff))
        cur.connection.commit()
        #print(stuff)
