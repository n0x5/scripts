import re
from bs4 import BeautifulSoup
import sqlite3
import os

conn = sqlite3.connect('imdb_scrape_database.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE companies 
            (title text, company text, year text, moviemeter text, budget text, coid text, imdbid text, role text, 
             dated datetime DEFAULT CURRENT_TIMESTAMP)''')

rootdir = os.path.join(os.path.dirname(__file__), 'html')

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        i2 = os.path.join(subdir, fn)
        i = open(i2, 'r')
        soup = BeautifulSoup(i, "html.parser")
        company2 = boxoffice = soup.find('title').get_text(strip=True)
        company = company2.replace(' - IMDbPro', '')
        table1 = soup.find('div', attrs={'id': 'filmography'})

        lis = table1.find_all({'li': 'class'})

        for item in lis:
            try:
                title = item.find('span', attrs={'class': 'display-title'}).get_text(strip=True)
                year = item.find('span', attrs={'class': 'year'}).get_text(strip=True)
                moviemeter = item.find('span', attrs={'class': 'moviemeter'}).get_text(strip=True)
                budget = item.find('span', attrs={'class': 'budget'}).get_text(strip=True)
                role = item.find('span', attrs={'class': 'collapsed'}).get_text(strip=True)
                coid1 = item.find('span', attrs={'class': 'expanded'})
                coid2 = re.findall(r'\d{7}', str(coid1))
                coid = "[]".join(coid2)
                imdb1 = item.find('span', attrs={'class': 'display-title'})
                imdb2 = re.findall(r'\d{7}', str(imdb1))
                imdbid = "[]".join(imdb2)
                print(title, company, year.replace('â€“', ' - '), moviemeter, budget, coid, imdbid, role)
                cur.execute('INSERT INTO companies (title, company, year, moviemeter, budget, coid, imdbid, role) VALUES (?,?,?,?,?,?,?,?)', 
                        (title, company, year, moviemeter, budget, coid, imdbid, role))
                cur.connection.commit()
               
            except AttributeError as e:
                print('None')


cur.close()
