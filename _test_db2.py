import os
import sqlite3
import re

connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'moviesim2.db'))
cursor = connection.cursor()
cursor.execute("select release, grp, genre, format, imdb, title, director, mainactors, infogenres, inforest, infosummary from movies")
results = [(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10]) for item in cursor.fetchall()]

connection2 = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'moviesim2new2.db'))
cursor2 = connection2.cursor()
cursor2.execute('''CREATE TABLE movies 
            (release text unique, grp text, genre text, format text, imdb text, title text, director text, 
            mainactors text, infogenres text, inforest text, infosummary text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')


for item2 in results:
    urls = re.findall(r'\d{7}', str(item2[4]))
    urls23 = "[]".join(urls)
    print('INSERT INTO movies (release, grp, genre, format, imdb, title, director, mainactors, infogenres, inforest, infosummary) VALUES (?,?,?,?,?,?,?,?,?,?,?)', 
                (item2[0], item2[1], item2[2], item2[3], 'https://www.imdb.com/title/tt'+urls23, str(item2[5]).strip(), item2[6], item2[7], item2[8], item2[9], item2[10]))
    cursor2.execute('INSERT INTO movies (release, grp, genre, format, imdb, title, director, mainactors, infogenres, inforest, infosummary) VALUES (?,?,?,?,?,?,?,?,?,?,?)', 
                (item2[0], str(item2[1]).strip(), str(item2[2]).strip(), item2[3], 'https://www.imdb.com/title/tt'+urls23, str(item2[5]).strip(), str(item2[6]).strip().replace(',', ''), item2[7], item2[8], item2[9], item2[10]))
    cursor2.connection.commit()

