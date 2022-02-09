# Wiki2sql
# Convert wikia .xml to sqlite db


import xml.etree.ElementTree as ET
import os
import re
import sqlite3

xmlfile = 'stargate_pages_current.xml'

tree = ET.parse(xmlfile)
root = tree.getroot()

db_name = xmlfile.replace('_pages_current.xml', '.db')
conn = sqlite3.connect(db_name)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS stargate (title text, content text, dated datetime DEFAULT CURRENT_TIMESTAMP)')

items = ([''])


for elem in root.iter():
    try:
        stuff1 = elem.text.split(':')[0]
    except Exception as e:
        items = (['File:', 'User talk:', 'User blog:', 'User:'])
        stuff1 = elem.text

    if '/}title' in elem.tag and elem.text is not None and stuff1 not in items:
        filestrip = re.sub(r'[\;*?!<>|\/:"\\\]\[]', '', elem.text)
        fname = (os.path.join(filestrip+'.html'))
        title = re.sub('[/:"]', '', elem.text)
        file3 = str(xmlfile).replace('.', '_')
        if not os.path.exists(file3):
            os.makedirs(file3)
        try:
            print(fname)
        except Exception as e:
            print(str(e))

    if '/}text' in elem.tag and elem.text is not None:
        
        links = re.sub(r'\[\[(.+?)\]\]', r'<a href="\1.html">\1</a>', elem.text)
        links2 =  re.sub(r'[][]', '', links)
        if 'File:' in links:
            links2 = re.sub(r'\[\[File:(.*?)\|.+\]\]', r'<img width="250px" src="images/\1" />', elem.text)
        if ':' in links2:
            links2 = re.sub(r':', r'', links2)
        if '#' in links2:
            links2 = re.sub(r'#[\w\s\|\_\:\-]+', r'', links2)
        if '|' in links2:
            links2 = re.sub(r'[\|][\w\s\|\_\:\-]+', r'', links2)
        stuff = title, links2
        cur.execute('insert into stargate (title, content) VALUES (?,?)', (stuff))
        cur.connection.commit()
        print(stuff)
