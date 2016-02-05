#!/usr/bin/env python

import os
import datetime
import time
from mutagen.id3 import ID3

today = time.strftime("__%m_%Y_%H_%M_%S")

cwd = os.getcwd()
os.chdir(cwd)
number = 1
fname = 'list_{}_{}.html' .format(os.path.basename(cwd), today)
b = open( fname, 'a' )
b.write('<!DOCTYPE html><html><body><h2><a href="{}">{} List</a></h2><table class="sortable" style="width:100%"><script src="sorttable.js"></script>' .format(fname, os.path.basename(cwd)))
b.write('<tr><th style="text-align:left">Release</th><th style="text-align:left">Group</th><th style="text-align:left">Genre</th><th style="text-align:left">Format</th></tr>\n')

def store(title, grp, genre):
    print ("(\"{}\" \"{}\" \"{}\" \"{}\")" .format(basenm2, file6, sf, number))
    b.write("<tr><td>{}</td>  <td>{}</td> <td>{}</td></tr>\n" .format(basenm2, file6, sf))


for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.startswith("01") or fn.startswith("101") or fn.startswith("a_") or fn.startswith("a-"):
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
b.write("<div class=\"total\" style=\"font-weight:bold;\">Total number of items: {} </br></br></div>" .format(number))
b.write("</table>\n</body>\n</html>")
b.close()
