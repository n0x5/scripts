# Wiki2html 
#
# Convert a wikimedia/wikia .xml to html files
# where the title of the article is the name of the file
# 
# Some formatting is removed, internal wiki links converted to <a href, a <pre> tag is added, 
# and a style.css file is linked to automatically that you can customize 
# 
# there will be bugs but it works ok on lostpedia
# also excluded a bunch of non-content sections like Template and User talk
# if there is a "hfile not defined" exception error, remove all the items from
# the items list and then readd one by one

import xml.etree.ElementTree as ET
import os
import re

xmlfile = 'your.xml'

tree = ET.parse(xmlfile)
root = tree.getroot()
items = (['User talk', 'File', 'User blog comment', 'User'])

for elem in root.iter():
    if '/}title' in elem.tag and elem.text is not None and elem.text.split(':')[0] not in items:
        filestrip = re.sub(r'[\;*?!<>|/:"]', '', elem.text)
        fname = (os.path.join(filestrip+'.html'))
        title = re.sub('[/:"]', '', elem.text)
        file3 = str(xmlfile).replace('.', '_')
        if not os.path.exists(file3):
            os.makedirs(file3)
        try:
            hfile = open(file3+'/'+fname, mode='w', encoding='utf8')
            print(fname)
            hfile.write('<h1>'+title+'</h1>')
        except Exception as e:
            print(str(e))

    if '/}text' in elem.tag and elem.text is not None:
        links = re.sub(r'(\[\[(\S+\s{0,5}\w+){0,3}\]\])', r'<a href="\1.html">\1</a>', elem.text)
        links2 =  re.sub(r'[][]', '', links)
        if ':' in links2:
            links2 = re.sub(r':', r'', links2)
        if '#' in links2:
            links2 = re.sub(r'#[\w\s\|\_\:\-]+', r'', links2)
        if '|' in links2:
            links2 = re.sub(r'[\|][\w\s\|\_\:\-]+', r'', links2)
        hfile.write('<link rel="stylesheet" href="style.css" type="text/css" media="screen" />')
        hfile.write('<pre>')
        hfile.write(links2)
