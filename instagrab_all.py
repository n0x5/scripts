# instagrabALL.py - download all images from instagram user

import re
from selenium import webdriver
import time
import sys
import itertools
import os
import urllib.request
from urllib.request import FancyURLopener
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


users = (['user1', 'user2'])

class GrabIt(urllib.request.FancyURLopener):
        version = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
        def download_file(self, url, path):
                try:
                    self.urlretrieve = GrabIt().retrieve
                    self.urlretrieve(url, path)
                except Exception as e:
                    print(str(e))


def grab_img(user):
    grab1 = GrabIt()
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    driver = Chrome(chrome_options=options)
    url = 'https://www.instagram.com/'+user+'/'
    driver.get(url)
    driver.implicitly_wait(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/section/div/a').click();
        driver.implicitly_wait(2)
    except:
        pass
    driver.find_element_by_xpath("//a[text()[contains(.,'Load more')]]").click();
    driver.implicitly_wait(5)
    for _ in itertools.repeat(None, 100):
        driver.implicitly_wait(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    driver.implicitly_wait(5)
    elem = driver.find_elements_by_xpath('//*[@src]')

    for ii in elem:
        if 'https://scontent' in ii.get_attribute('src'):
            content2 = ii.get_attribute('src')
            content3 = re.sub(r's\w\w\wx\w\w\w\/', '', content2, flags=re.IGNORECASE)
            content7 = re.sub(r'\w{3}\.\w{2}\/', '', content3, flags=re.IGNORECASE)
            content6 = re.sub(r'\w{0,4}\.\d{0,4}\.\d{0,4}\.\d{0,5}\/', '', content7, flags=re.IGNORECASE)
            content4 = re.sub(r'https:\/\/\w{8}\S+\w{4}-\w(.*)\/', '', content2, flags=re.IGNORECASE)
            content5 = re.sub(r'\?ig_cache_key=\w+(\S+)', '', content4, flags=re.IGNORECASE)
            content10 = re.sub(r'\/vp\/\w+\/\w+', '', content6, flags=re.IGNORECASE)
            endpoint = os.path.join(os.path.dirname(__file__), user, content5)
            endpoint1 = os.path.join(os.path.dirname(__file__), user, user+'_'+content5)
            if not os.path.exists(user):
                os.makedirs(user)
            if os.path.isfile(endpoint) or os.path.isfile(endpoint1):
                print('file exists - skipping')
            else:
                try:
                    grab1.download_file(content10, endpoint1)
                    print(content5)
                except Exception as e:
                    print(str(e))

    driver.quit()

for user in users:
    grab_img(user)
