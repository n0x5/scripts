#!/usr/bin/env python

import shutil
import os
import datetime
import pymysql

rootdir = 'I:\\path\\to\\movies'
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
        if "genre".lower() in genres.lower():
            if "horror".lower() in genres.lower():
                return ('Horror')
            elif "sci-fi".lower() in genres.lower():
                return ('Sci-Fi')
            elif "drama".lower() in genres.lower():
                return ('Drama')
            elif "fantasy".lower() in genres.lower():
                return ('Fantasy')
            elif "thriller".lower() in genres.lower():
                return ('Thriller')
            elif "comedy".lower() in genres.lower():
                return ('Comedy')
            elif "action".lower() in genres.lower():
                return ('Action')
    filn.close()

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if fn.endswith(".nfo"):
            try:
                file2 = os.path.join(subdir, fn)
                path2 = os.path.join(subdir)
                basenm2 = os.path.basename(path2)
                file4 = basenm2.split('-')
                file5 = file4[-1:]
                file6 = "[]".join(file5)
                store(basenm2, file6, genrs(file2))
                                
            except:
                pass

b.write("</table>")
b.close()
