from selenium import webdriver
import time
import sys

driver = webdriver.PhantomJS()
htt = 'http://'
url2 = sys.argv[1]
url = htt + url2
today = time.strftime("__%m_%Y_%H_%M")

driver.get(url)
driver.get_screenshot_as_file('screen_{1}_{0}.jpg' .format(today, url2))

driver.quit()
