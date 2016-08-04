#!/usr/bin/env python

# Create a list of movies in a folder
# It uses currently active directory so cd into the folder
# then run ./list-html-movies.py and it will make a html file
# in the same folder

import os
import time
import re

today = time.strftime("__%m_%Y_%H_%M_%S")

cwd = os.getcwd()
os.chdir(cwd)
number = 0

fname = 'list_{}_{}.html' .format(os.path.basename(cwd), today)
hfile = open(fname, 'a')
hfile.write('<!DOCTYPE html><html><body><h2><a href="{}">{} List</a></h2><ta'
            'ble class="sortable" style="width:100%"><script src="sorttable.'
            'js"></script>' .format(fname, os.path.basename(cwd)))
hfile.write('<tr><th style="text-align:left">Release</th><th style="text-ali'
            'gn:left">Group</th><th style="text-align:left">Genre</th><th st'
            'yle="text-align:left">Format</th></tr>\n')

def imdburl(fn):
    filn2 = open(fn, "r")
    for iurls in filn2:
        if "http" in iurls.lower():
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\\'
                              '),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', iurls)
            urls23 = "[]".join(urls)
            if "imdb" in urls23:
                return urls23
            else:
                return ""

def store(title, grp, genre):
    print('{} - {} - {} - {} - {}'
          .format(basenm2, file6, genrs(file2), file7, number), imdburl(file2))
    hfile.write('<tr><td><a href="{}">{}</a></td>  <td>{}</td> <td>{}</td><t'
                'd>{}</td></tr>\n'
                .format(imdburl(file2), basenm2, file6, genrs(file2), file7))

def genrs(fn):
    genrelist = (["romance", "comedy", "animation", "mystery", "documentary", "crime", "family", "sport", 
                "biography", "history", "western", "sci-fi", "horror", "adventure", "drama", "fantasy", "thriller", "action"])
    filn = open(fn, "r")
    for genres in filn:
        if "genre" in genres.lower():
            output = [item.title() for item in genrelist if item in genres.lower()]
            return(", ".join(repr(e).replace("'", "") for e in output))

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.endswith(".nfo"):
            try:
                file2 = os.path.join(subdir, fn)
                basenm2 = os.path.basename(os.path.join(subdir))
                file6 = "[]".join(basenm2.split('-')[-1:])
                file7 = "[]".join(basenm2.split('.')[-1:]).split('-')[0]
                if ('cd1' not in file2.lower() and 'cd2' not in file2.lower()
                        and 'sample' not in file2.lower() and 'vobsub'
                        not in file2.lower() and 'subs' not in file2.lower()):
                    store(basenm2, file6, genrs(file2))
                    number += 1
            except:
                pass
hfile.write('<div class="total" style="font-weight:bold;">Total number'
            ' of items: {} </br></br></div>' .format(number))
hfile.write('</table>\n</body>\n</html>')
hfile.close()
