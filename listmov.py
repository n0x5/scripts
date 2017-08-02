#!/usr/bin/env python

# Create a list of movies in a folder
# It uses currently active directory so cd into the folder
# then run ./list-html-movies.py and it will make a html file
# in the same folder

import os
import requests
import re
from bs4 import BeautifulSoup
import time

today = time.strftime("__%m_%Y_%H_%M_%S")

cwd = r'/path/to/movies'
number = 0

fname = 'list_{}_{}.html' .format(os.path.basename(cwd), today)
hfile = open(fname, 'a')
hfile.write(""" 
<!DOCTYPE html>
<html>
    <body>
        <h2><a href="{}">{} List</a></h2>
            <table class="sortable" style="width:100%"><script src="sorttable.js"></script>
            <tr><th style="text-align:left">Release</th><th style="text-align:left">Group</th><th style="text-align:left">Genre</th>
            <th style="text-align:left">Format</th></tr>\n"""
.format(fname, os.path.basename(cwd)))


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

def store(title, grp, genre, imdb_info):
    print('{} - {} - {} - {} - {} - {} - {}' .format(basenm2, file6, genrs(file2), file7, number, imdburl(file2), imdb_info))
    hfile.write("""
            <tr><td class="release"><a href="{}" class="imdb">{}</a></td><td class="group">{}</td> <td class="genre">{}</td><td class="format">{}</td></tr>\n"""
                .format(imdburl(file2), basenm2, file6, genrs(file2), file7))

def genrs(fn):
    genrelist = (["romance", "comedy", "animation", "mystery", "documentary", "crime", "family", "sport", 
                "biography", "history", "western", "sci-fi", "horror", "adventure", "drama", "fantasy", "thriller", "action"])
    filn = open(fn, "r")
    for genres in filn:
        if "genre" in genres.lower():
            output = [item.title() for item in genrelist if item in genres.lower()]
            return(", ".join(repr(e).replace("'", "") for e in output))

def get_info(url):
    info = []
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find('h1', attrs={'itemprop': 'name'})
    genre = [genre1.get_text() for genre1 in soup.find_all('span', attrs={'itemprop': 'genre'})]
    director = soup.find('span', attrs={'itemprop': 'director'})
    main_actors2 = [main_actors.get_text() for main_actors in soup.find_all('span', attrs={'itemprop': 'actors'})]

    actor_table = soup.find('table', attrs={'class': 'cast_list'})
    rest_actors = [rest_actors1.get_text() for rest_actors1 in actor_table.find_all('span', attrs={'itemprop': 'name'})]

    info.append(title.get_text())
    for line2 in genre:
        info.append(line2)
    info.append(director.get_text())
    for line in main_actors2:
        info.append(line.replace(',', ''))
    for line3 in rest_actors:
        info.append(line3)
    return info


for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.endswith(".nfo"):
            try:
                file2 = os.path.join(subdir, fn)
                basenm2 = os.path.basename(os.path.join(subdir))
                file6 = "[]".join(basenm2.split('-')[-1:])
                file7 = "[]".join(basenm2.split('.')[-1:]).split('-')[0]
                banned = ['cd1', 'cd2', 'sample', 'vobsub', 'subs', 'proof', 'prooffix', 'syncfix']
                url = imdburl(file2)
                imdb_info = get_info(url)
                if basenm2.lower().split(' ')[0] not in banned:
                    store(basenm2, file6, genrs(file2), imdb_info)
                    number += 1
                    time.sleep(30)
            except Exception as e:
                print(e)

hfile.write("""
        <div class="total" style="font-weight:bold;">Total number of items: {} </br></br></div>
        </table>
    </body>
</html>""" .format(number))
hfile.close()
