import re
import time
import urllib.request
import requests
from bs4 import BeautifulSoup


def get_info1(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    info1 = soup.find('div', attrs={'class': 'contact-right'})
    info2 = soup.find_all('div', attrs={'class': 'contact-block'})
    info3 = soup.find_all('div', attrs={'class': 'contact-info'})
    address = info1.find('div', attrs={'class': 'contact-info'}).get_text().split('\n')

    for line in info3:
        try:
            h51 = line.find('h5').get_text(strip=True)
            leder = line.find('p').get_text().split('\n')[1].strip()
            epost = line.find('a', href=re.compile('mailto')).get_text(strip=True)
            tlf = line.find('a', href=re.compile('tel')).get_text(strip=True)
            csvfile = open('k_barnehager.csv', 'a')
            csvfile.write(leder+','+h51+','+epost+','+tlf+','+address[2]+','+address[3].replace(',', '')+'\n')
            print(leder, h51, epost, tlf, address[2], address[3].replace(',', ''))
        except:
            pass


url = r'https://www.k.no/var/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")


blist = soup.find('ul', attrs={'class': 'kindergartens clearfix'})
blist4 = blist.find_all('h2', attrs={'class': 'title kindergarten-title'})

for item4 in blist4:
    url2 = item4.find('a')
    print('getting info for -> '+url2['href'])
    info7 = get_info1(url2['href'])
    time.sleep(1)

