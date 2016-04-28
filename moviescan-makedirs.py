#!/usr/bin/env python


import os

cwd = os.getcwd()
os.chdir(cwd)
rootdir = cwd

def store(title, grp, genre):
    print ("{} {}" .format(genrs(file2), rating(file2)))
    os.makedirs(file3+'__'+'Rating__'+rating(file2))

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

def rating(fn):
    filn = open(fn, "r")
    for ratings in filn:
        if 'rating' in ratings.lower():
            ratings2 = '0123456789,./'
            outpt = [l for l in ratings if l in ratings2]
            return("".join(outpt).replace("/", "__Votes__").lstrip('.').rstrip('.'))

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if fn.endswith(".nfo"):
            try:
                file2 = os.path.join(subdir, fn)
                basenm2 = os.path.basename(os.path.join(subdir))
                file3 = os.path.join(subdir, genrs(file2))
                file6 = "[]".join(basenm2.split('-')[-1:])
                file7 = file6.split('-')[0]
                store(basenm2, file6, genrs(file2))
            except:
                pass
