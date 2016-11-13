# Wiki2html 
#
# Convert a wikimedia/wikia .xml to html files
# where the title of the article is the name of the file
# 
# Some formatting is removed, no internal wiki links work, a <pre> tag is added, 
# and a style.css file is linked to automatically that you can
# customize 
# 
# there will be bugs but it works ok on lostpedia
# also excluded a bunch of non-content sections like Template and User talk

import xml.etree.ElementTree as ET
import os
import re
import traceback

tree = ET.parse('your.xml')
root = tree.getroot()
items = (['Category:', 'User talk:', 'Template:', 'User:', 'Shadowrun talk:', 'File:', 'Talk:', 
          'Shadowrun Wiki:', 'User blog:', 'User blog comment:'])

for elem in root.iter():
    if ('export-0.6/}title' in elem.tag and elem.text is not None and items not in elem.text.split(':')[0]):
        filestrip = re.sub(r'[\;*?!<>|/:"]', '', elem.text)
        fname = (os.path.join(filestrip.strip().replace(' ', '_')+'.html'))
        title = re.sub('[/:"]', '', elem.text)
        try:
            hfile = open(fname, 'ab')
            print(fname)
            hfile.write('<h1>'.encode('utf8')+title.encode('utf8')+'</h1>'.encode('utf8'))
        except Exception as e:
            print(str(e))

    if 'export-0.6/}text' in elem.tag and elem.text is not None:
        hfile.write('<link rel="stylesheet" href="style.css" type="text/css" media="screen" />'.encode('utf8'))
        hfile.write('<pre>'.encode('utf8'))
        hfile.write(elem.text.replace('[', '<b>').replace(']', '</b>').replace('\'', '').encode('utf8'))
