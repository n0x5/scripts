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

conn = sqlite3.connect('boxofficemojo-new3.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists boxoffice
            (title text, theaters int, theatersopen int, gross text, distributor text, release_date text,
             year int, rl_id text unique, dated datetime DEFAULT CURRENT_TIMESTAMP)''')


#url = r'https://www.boxofficemojo.com/year/{}/?grossesOption=calendarGrosses&sort=releaseDate' .format(args.year)
#url = r'https://www.boxofficemojo.com/year/{}/?sort=releaseDate&releaseScale=wide&grossesOption=totalGrosses' .format(args.year)

url = r'https://www.boxofficemojo.com/year/{}/?grossesOption=totalGrosses&releaseScale=all&sort=releaseDate' .format(args.year)

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table2 = soup.find('div', attrs={'class': 'a-section imdb-scroll-table-inner'})

table3 = table2.find_all('tr')

for table in table3:
    title = table.find('td', attrs={'class': 'a-text-left mojo-field-type-release mojo-cell-wide'})
    theaters = table.find_all('td', attrs={'class': 'a-text-right mojo-field-type-positive_integer'})
    theatersopen = table.find_all('td', attrs={'class': 'a-text-right mojo-field-type-positive_integer'})
    gross = table.find('td', attrs={'class': 'a-text-right mojo-field-type-money mojo-estimatable'})
    release_date = table.find('td', attrs={'class': 'a-text-left mojo-field-type-date mojo-sort-column a-nowrap'})
    distributor = table.find('td', attrs={'class': 'a-text-left mojo-field-type-studio'})
    b_id = table.find('a', href=re.compile('\d+'))
    box_id2 = re.search(r'\/release\/rl(\d+)\/', str(b_id))

    try:
        theaters_final = int(theaters[0].get_text().replace(',', ''))
    except:
        theaters_final = '-'
    try:
        theatersopen_final = int(theatersopen[1].get_text().replace(',', ''))
    except:
        theatersopen_final = '-'
    try:
        gross_final = gross.get_text()
    except:
        gross_final = '-'

    try:
        stuff = title.get_text(), int(args.year), theaters_final, theatersopen_final, gross_final, release_date.get_text(), distributor.get_text().replace('\n\n', ''), box_id2.group(1)
        print(stuff)
        cur.execute('INSERT INTO boxoffice (title, year, theaters, theatersopen, gross, release_date, distributor, rl_id) VALUES (?,?,?,?,?,?,?,?)', (stuff))
        cur.connection.commit()
    except Exception as e:
        print(e)
        pass
