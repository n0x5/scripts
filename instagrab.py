# instagrab.py - download images from instagram
#
# write the name of the user you want to download in USER_NAME_HERE
# python instagrab.py
# only grabs latest / first page images so far

import re
from selenium import webdriver
import time
import sys
import urllib.request
from urllib.request import FancyURLopener

user = 'USER_NAME_HERE'

class GrabIt(urllib.request.FancyURLopener):
        version = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
        def download_file(self, url, path):
                try:
                    urlretrieve = GrabIt().retrieve
                    urlretrieve(url, path)
                except Exception as e:
                    print(str(e))

grab1 = GrabIt()
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
url = 'https://www.instagram.com/'+user+'/'

driver.get(url)
elem = driver.find_elements_by_xpath('//*[@src]')

for ii in elem:
    if 'https://scontent-' in ii.get_attribute('src'):
        content2 = ii.get_attribute('src')
        content3 = re.sub(r's\w\w\wx\w\w\w\/', '', content2, flags=re.IGNORECASE)
        content4 = re.sub(r'https:\/\/\w{8}-\w{4}-\w(.*)\/', '', content2, flags=re.IGNORECASE)
        content5 = re.sub(r'\?ig_cache_key=\w{26}(\S+)', '', content4, flags=re.IGNORECASE)
        time.sleep(4)
        grab1.download_file(content3, content5)
        print(content5)

driver.quit()
