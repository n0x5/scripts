### Upload image/folder recursively to Google Vision AI for image recognition
## 1000 requests / month for free
Scans a folder recursively or give path to single file and write .json info in same folder
If a json file exists already it will not make a request to the API.
Supports RAW files as well as .jpg/gif/png/etc
#### I recommend using the .exe file if you are on windows, nothing needed to install

### Setup guide
0) Click "Code" -> "Downoad Zip" in the top right of the reposity, unzip files to a folder (keep exiftool there).
1) Go to https://cloud.google.com/vision and enable the api (need billing/credit card)
2) Go to https://console.developers.google.com/
2) Click 'Credentials' in left side menu
3) Create "create credentials" - > "OAuth client ID"
4) Select "Desktop app" in "Application type". Use any name you want, mine is "Desktop client 1"
5) Go back to the Credentials main page and click the Download OAuth client link to the left of the "Desktop client 1" in the list.
6) The .json file downloads in browser, so just rename it to "credentials.json" and place it in the unzipped folder with Vision_API_V2.py/exe and then run it with --file to a single file to initiate.
7) The browser will open to a Google page to authorize the app to access the account, click accept etc. Finished.

### Setup guide for python:
If you don't want to use the executable and you don't have Python you have to go to www.python.org, download the latest version, then run the following command:
#### pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib requests rawpy
    
After this you should follow the earlier guide to setup Google OAuth.

Command line options:
--file : Path to single file scan
--folder : Recursive scan of a folder
--write-tags : Will overwrite metadata in image file (need exiftool.exe on windows/exiftool on linux) (keeps date modified if possible)

Example command:
#### python .\Google_Vision_API.py --folder "F:\dev\Google_APIs\New folder (13)" --write-tags

#### Screenshot:
![alt text](https://raw.githubusercontent.com/n0x5/scripts/master/Google_Tools/raw.png)
