# scan a local folder for imgur files then rename to title from imgur page
# if the title doesn't exist on imgur the file is renamed with a '_' in front

import re
import time
import os
import shutil
#import urllib.request
#from urllib.request import FancyURLopener
import requests
from bs4 import BeautifulSoup

cwd = r'/path/to/folder'

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                   ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
}

def title(contentz):
    for title2 in contentz.find_all('h1', class_="post-title"):
        return title2.get_text('', strip=True)

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.endswith(".jpg") or fn.endswith(".gif"):
            if re.match(r'\w{7}.jpg$', fn) is not None:
                fn2 = re.match(r'(\w{7}).jpg$', fn)
                url = 'https://imgur.com/'+fn2.group(1)
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")
                filestrip = re.sub(r'[\;*?!<>|/:"]', '', str(title(soup)))
                if title(soup) is not None:
                    print(fn, 'rename to ->', title(soup)+'_'+fn)
                    shutil.move(os.path.join(cwd, fn), os.path.join(cwd, filestrip+'_'+fn))
                time.sleep(2)
