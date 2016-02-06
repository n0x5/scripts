#!/usr/bin/env python

import os
import datetime
import time

today = time.strftime("__%m_%Y_%H_%M_%S")

cwd = os.getcwd()
os.chdir(cwd)
number = 1
fname = 'list_{}_{}.html' .format(os.path.basename(cwd), today)
b = open( fname, 'a' )
b.write('<!DOCTYPE html><html><body><h2><a href="{}">{} List</a></h2><table class="sortable" style="width:100%"><script src="sorttable.js"></script>' .format(fname, os.path.basename(cwd)))
b.write('<tr><th style="text-align:left">Release</th><th style="text-align:left">Group</th><th style="text-align:left">Genre</th><th style="text-align:left">Format</th></tr>\n')

def store(title, grp, genre):
    print ("(\"{}\" \"{}\" \"{}\" \"{}\" \"{}\")" .format(basenm2, file6, genrs(file2), file7, number))
    b.write("<tr><td>{}</td>  <td>{}</td> <td>{}</td><td>{}</td></tr>\n" .format(basenm2, file6, genrs(file2), file7))

def genrs(fn):
    filn = open(fn, "r")
    for genres in filn:
        if "genre" in genres.lower():
            if "horror" in genres.lower():
                return 'Horror'
            elif "animation" in genres.lower():
                return 'Animation'
            elif "documentary" in genres.lower():
                return 'Documentary'
            elif "family" in genres.lower():
                return 'Family'
            elif "sport" in genres.lower():
                return 'Sport'
            elif "biography" in genres.lower():
                return 'Biography'
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
                store(basenm2, file6, genrs(file2))
                number += 1
            except:
                pass
b.write("<div class=\"total\" style=\"font-weight:bold;\">Total number of items: {} </br></br></div>" .format(number))
b.write("</table>\n</body>\n</html>")
b.close()
