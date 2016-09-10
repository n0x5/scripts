#!/usr/bin/env python

# Create a list of mp3s in a folder
# It uses currently active directory so cd into the folder
# then run ./listmp3.py and it will make a html file in the same folder

import os
import time
from mutagen.id3 import ID3

today = time.strftime("__%m_%Y_%H_%M_%S")

number = 1
fname = 'list_{}_{}.html' .format(os.path.basename(os.getcwd()), today)
fnam = open(fname, 'a')
fnam.write('<!DOCTYPE html><html><body><h2><a href="{}">{} List</a></h2><tab'
           'le class="sortable" style="width:100%"><script src="sorttable.js">'
           '</script>' .format(fname, os.path.basename(os.getcwd())))
fnam.write('<tr><th style="text-align:left">Release</th><th style="text-ali'
           'gn:left">Group</th><th style="text-align:left">Genre</th><th '
           'style="text-align:left">Format</th></tr>\n')

def store(title, grp, genre):
    print('{} {} {} {}' .format(basenm2, file6, sf, number))
    fnam.write('<tr><td>{}</td>  <td>{}</td> <td>{}</td></tr>\n'
               .format(basenm2, file6, sf))


for subdir, dirs, files in os.walk(os.getcwd()):
    for fn in files:
        if (fn.startswith("01") or fn.startswith("101") or fn.startswith("a_")
                or fn.startswith("a-")):
            try:
                file2 = os.path.join(subdir, fn)
                audio = ID3(file2)
                sf = format(audio['TCON'].text[0])
                basenm2 = os.path.basename(os.path.join(subdir))
                file6 = "[]".join(basenm2.split('-')[-1:])
                file7 = "[]".join(basenm2.split('.')[-1:]).split('-')[0]
                store(basenm2, file6, sf)
                number += 1
            except:
                pass
fnam.write('<div class="total" style="font-weight:bold;">Total number of items'
           ': {} </br></br></div>' .format(number))
fnam.write("</table>\n</body>\n</html>")
fnam.close()