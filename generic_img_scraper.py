import re
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import urllib.request
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url')
args = parser.parse_args()

class GrabIt(urllib.request.FancyURLopener):
        version = ('Mozilla/6.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/53.0.2526.111 Safari/547.36')
        def download_file(self, url, path):
                try:
                    self.urlretrieve = GrabIt().retrieve
                    self.urlretrieve(url, path)
                except Exception as e:
                    print(str(e))

grab1 = GrabIt()
options = ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
driver = Chrome(chrome_options=options)
driver.get(args.url)
html = driver.page_source
soup = BeautifulSoup(html)
for img in soup.findAll('a', href=re.compile('.(.jpg|.png|.gif)')):
    img2 = img['href']
    imgbase = os.path.basename(img2)
    endpoint = os.path.join(os.path.dirname(__file__), imgbase)
    if os.path.isfile(endpoint):
        print('file exists - skipping')
    grab1.download_file(img2, endpoint)
    print(img2)
    time.sleep(1)

driver.close()
