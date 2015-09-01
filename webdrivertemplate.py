from selenium import webdriver
import time
import sys


driver = webdriver.PhantomJS()
htt = 'http://'

url2 = sys.argv[1]
url = htt + url2

driver.get(url)
##### CODE HERE

driver.quit()
