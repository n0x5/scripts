import re
import time
import urllib.request
import requests
from bs4 import BeautifulSoup
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('year')
args = parser.parse_args()

conn = sqlite3.connect('boxofficemojo.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE boxoffice 
            (title text, worldwide text, domestic text, domesticper text, overseas text, overseasper text, studio text, 
             year text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')


url = r'http://www.boxofficemojo.com/yearly/chart/?view2=worldwide&yr={}&p=.htm' .format(args.year)

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

info3 = soup.find_all('tr')

for item in info3:
    try:
        tdtab = item.find_all('td')
        title = tdtab[1].get_text()
        studio = tdtab[2].get_text()
        worldwide = tdtab[3].get_text()
        domestic = tdtab[4].get_text()
        domesticper = tdtab[5].get_text()
        overseas = tdtab[6].get_text()
        overseasper = tdtab[7].get_text()
        print(title, worldwide, domestic, domesticper, overseas, overseasper, studio, args.year)
        cur.execute('INSERT INTO boxoffice (title, worldwide, domestic, domesticper, overseas, overseasper, studio, year) VALUES (?,?,?,?,?,?,?,?)', 
                (title, worldwide, domestic, domesticper, overseas, overseasper, studio, args.year))
        cur.connection.commit()
    except:
        pass

