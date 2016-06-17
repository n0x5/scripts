#!/usr/bin/env python

# Create a list of movies in a folder
# It uses currently active directory so cd into the folder
# then run ./list-html.movies.py and it will make a html file in the same folder

import os
import datetime
import time
import re

today = time.strftime("__%m_%Y_%H_%M_%S")

cwd = os.getcwd()
os.chdir(cwd)
number = 1

fname = 'list_{}_{}.html' .format(os.path.basename(cwd), today)
b = open( fname, 'a' )
b.write('<!DOCTYPE html><html><body><h2><a href="{}">{} List</a></h2><table class="sortable" style="width:100%"><script src="sorttable.js"></script>' .format(fname, os.path.basename(cwd)))
b.write('<tr><th style="text-align:left">Release</th><th style="text-align:left">Group</th><th style="text-align:left">Genre</th><th style="text-align:left">Format</th></tr>\n')

def imdburl(fn):
    filn2 = open(fn, "r")
    for iurls in filn2:
        if "http" in iurls.lower():
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', iurls)
            urls23 = "[]".join(urls)
            if "imdb" in urls23:
                return urls23
            else:
                return ""

def store(title, grp, genre):
    print ("(\"{}\" \"{}\" \"{}\" \"{}\" \"{}\")" .format(basenm2, file6, genrs(file2), file7, number), imdburl(file2))
    b.write("<tr><td><a href=\"{}\">{}</a></td>  <td>{}</td> <td>{}</td><td>{}</td></tr>\n" .format(imdburl(file2), basenm2, file6, genrs(file2), file7))

def genrs(fn):
    filn = open(fn, "r")
    for genres in filn:
        if "genre" in genres.lower():
            if "horror" in genres.lower():
                return 'Horror'
            elif "animation" in genres.lower():
                return 'Animation'
            elif "mystery" in genres.lower():
                return 'Mystery'
            elif "documentary" in genres.lower():
                return 'Documentary'
            elif "crime" in genres.lower():
                return 'Crime'
            elif "family" in genres.lower():
                return 'Family'
            elif "sport" in genres.lower():
                return 'Sport'
            elif "biography" in genres.lower():
                return 'Biography'
            elif "history" in genres.lower():
                return 'History'
            elif "western" in genres.lower():
                return 'Western'
            elif "sci-fi" in genres.lower():
                return 'Sci-Fi'
            elif "adventure" in genres.lower():
                return 'Adventure'
            elif "romance" in genres.lower():
                return 'Romance'
            elif "drama" in genres.lower():
                return 'Drama'
            elif "fantasy" in genres.lower():
                return 'Fantasy'
            elif "thriller" in genres.lower():
                return 'Thriller'
            elif "comedy" in genres.lower():
                return 'Comedy'
            elif "action" in genres.lower():
                return 'Action'

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.endswith(".nfo"):
            try:
                file2 = os.path.join(subdir, fn)
                basenm2 = os.path.basename(os.path.join(subdir))
                file6 = "[]".join(basenm2.split('-')[-1:])
                file7 = "[]".join(basenm2.split('.')[-1:]).split('-')[0]
                if "cd1" not in file2.lower() and "cd2" not in file2.lower() and "sample" not in file2.lower() and "vobsub" not in file2.lower() and "subs" not in file2.lower():
                    store(basenm2, file6, genrs(file2))
                    number += 1
            except:
                pass
b.write("<div class=\"total\" style=\"font-weight:bold;\">Total number of items: {} </br></br></div>" .format(number))
b.write("</table>\n</body>\n</html>")
b.close()
