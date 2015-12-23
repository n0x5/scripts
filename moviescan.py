#!/usr/bin/env python

import shutil
import os
import datetime

rootdir = 'F:\\archive\\xvid-old-DONE'
fname = 'xvidgenres.html'
b = open( fname, 'a' )
b.write("<!DOCTYPE html><html><body><h2>Movie List</h2><table class=\"sortable\" style=\"width:100%\"><script src=\"sorttable.js\"></script>")
b.write("<tr><th style=\"text-align:left\">Release</th><th style=\"text-align:left\">Group</th><th style=\"text-align:left\">Genre</th></tr>")
b.write("<tr>")

def store(title, grp, genre):
    print ("(\"{}\" \"{}\" \"{}\")" .format(basenm2, file6, genrs(file2)))
    b.write("<tr><td>{}</td>  <td>{}</td> <td>{}</td></tr>\n" .format(basenm2, file6, genrs(file2)))

def genrs(fn):
    filn = open(fn, "r")
    for genres in filn:
        if "genre" in genres.lower():
            if "horror" in genres.lower():
                return 'Horror'
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
    filn.close()

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if fn.endswith(".nfo"):
            try:
                file2 = os.path.join(subdir, fn)
                basenm2 = os.path.basename(os.path.join(subdir))
                file6 = "[]".join(basenm2.split('-')[-1:])
                store(basenm2, file6, genrs(os.path.join(subdir, fn)))
            except:
                pass

b.write("</table>")
b.close()
