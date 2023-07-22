# Create static HTML gallery of a folder with thumbnails
# python create_html_gallery.py C:\folder\gallery

import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('folder')
args = parser.parse_args()
upload = args.folder

thmbs = os.path.join(upload, 'thumbs')
lst = []
html_file2 = []
if not os.path.exists(thmbs):
    os.makedirs(thmbs)

for subdir, dirs, files in os.walk(upload):
    for fn in files:
        if not fn.startswith('thumb_'):
            thmb_file = os.path.join(thmbs, 'thumb_'+fn)
            full_file = os.path.join(subdir, fn)
            if not os.path.exists(thmb_file):
                try:
                    width = 150
                    im = Image.open(full_file)
                    widthper = (width/float(im.size[0]))
                    heightsize = int((float(im.size[1])*float(widthper)))
                    size = width, heightsize
                    im2 = im.resize(size, Image.LANCZOS)
                    im2.save(thmb_file, 'JPEG', quality=90)
                    html_file2 = '<div class="image"><a href="{}"><img src="thumbs/thumb_{}" /></a><center>{}<br>—<br>{}x{}</center></div> '.format(fn, fn, fn, im.size[0], im.size[1])
                    lst.append(html_file2)
                    print(full_file, im.size[0], im.size[1])
                except Exception as e:
                    print(e)
print(len(lst))
html_file = '''
<html>
<head>
<meta content='IE=EmulateIE7' http-equiv='X-UA-Compatible'/>
<meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
<link href='https://website.com' rel='canonical'/>
<meta content='Atlas, archiving, cyberspace' property='og:description'/>
<link rel='stylesheet' href='style.css' media='all' />
<title>{} gallery</title>
</head>
<body>
<div id="content">
<h1>{} ({} images)</h1>
''' .format(os.path.basename(upload), os.path.basename(upload), len(lst))

final = '\n'.join(lst)
print(final)
with open(os.path.join(upload, 'index.html'), 'w') as file:
    file.write('''
{}\n
{}
</content>
</body>
</html>
''' .format(html_file, final))

css_file = '''.image {
width: 150px;
float: left;
height: 309px;
margin: 9px;
background-color: #ffdbdb;
word-break: break-word;
padding: 13px;
}'''

with open(os.path.join(upload, 'style.css'), 'w') as file2:
    file2.write(css_file)
