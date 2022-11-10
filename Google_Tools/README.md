### Upload image/folder recursively to Google Vision AI for image recognition
#### Supports RAW files with XMP creation.

Scans a folder recursively or give path to single file and write .json info in same folder
If a json file exists already it will not make a request to the API.
Supports RAW files as well as .jpg/gif/png/etc
#### I recommend using the .exe file if you are on windows, nothing needed to install

### Setup guide
0) Download the zip https://github.com/n0x5/scripts/releases/download/google_vision_v3/Vision_API_V3.zip unzip files to a folder (keep exiftool there).
2) Go to https://cloud.google.com/vision and enable the api (need billing/credit card)
3) Go to https://console.developers.google.com/
4) Click 'Credentials' in left side menu
5) Create "create credentials" - > "OAuth client ID"
6) Select "Desktop app" in "Application type". Use any name you want, mine is "Desktop client 1"
7) Go back to the Credentials main page and click the Download OAuth client link to the left of the "Desktop client 1" in the list.
8) The .json file downloads in browser, so just rename it to "credentials.json" and place it in the unzipped folder with Vision_API_V2.py/exe and then run it with --file to a single file to initiate.
9) The browser will open to a Google page to authorize the app to access the account, click accept etc. Finished.

### Setup guide for python:
If you don't want to use the executable and you don't have Python you have to go to www.python.org, download the latest version, then run the following command:
#### pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib requests rawpy pillow
    
After this you should follow the earlier guide to setup Google OAuth.

Command line options:

#### --file : Path to single file scan

#### --folder : Recursive scan of a folder

#### --write-tags : Will overwrite metadata in image file (need exiftool.exe on windows/exiftool on linux) (keeps date modified if possible)

Example command:
#### python .\Google_Vision_API.py --folder "F:\dev\Google_APIs\New folder (13)" --write-tags

#### Screenshot:
![alt text](https://raw.githubusercontent.com/n0x5/scripts/master/Google_Tools/raw2.jpg)
