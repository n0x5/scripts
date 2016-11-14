# Wiki2html 
#
# Convert a wikimedia/wikia .xml to html files
# where the title of the article is the name of the file
# 
# Some formatting is removed, internal links work, a <pre> tag is added, 
# and a style.css file is linked to automatically that you can
# customize 
# 
# there will be bugs but it works ok on lostpedia
# also excluded a bunch of non-content sections like Template and User talk

import xml.etree.ElementTree as ET
import os
import re

tree = ET.parse('your.xml')
root = tree.getroot()
items = (['Category', 'User talk', 'Template', 'User', 'Shadowrun talk', 'File', 'Talk', 
          'Shadowrun Wiki', 'User blog', 'User blog comment', 'Contributor'])

for elem in root.iter():
    if 'export-0.6/}title' in elem.tag and elem.text is not None and elem.text.split(':')[0] not in items:
        filestrip = re.sub(r'[\;*?!<>|/:"]', '', elem.text)
        fname = (os.path.join(filestrip+'.html'))
        title = re.sub('[/:"]', '', elem.text)
        try:
            hfile = open(fname, mode='w', encoding='utf8')
            print(fname)
            hfile.write('<h1>'+title+'</h1>')
        except Exception as e:
            print(str(e))

    if 'export-0.6/}text' in elem.tag and elem.text is not None:
        links = re.sub(r'(\[\[(\S+\s{0,5}\w+){0,3}\]\])', r'<a href="\1.html">\1</a>', elem.text)
        links2 =  re.sub(r'[][]', '', links)
        hfile.write('<link rel="stylesheet" href="style.css" type="text/css" media="screen" />')
        hfile.write('<pre>')
        hfile.write(links2)
