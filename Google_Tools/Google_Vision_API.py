# Upload image to Google Vision for image recognition
# Scan a folder recursively or give path to single file and write .json info in same folder
# Need Desktop App oauth2 credentials.json file in same folder
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib requests
#
#
# Command line options:
#
# --file : Path to single file scan
# --folder : Recursive scan of a folder
# --write-tags : Will overwrite metadata in image file (need exiftool.exe on windows/exiftool on linux) (keeps date modified if possible)
# --no-json : Currently not enabled
#
# Example command:
# python .\Google_Vision_API.py --folder "F:\dev\Google_APIs\New folder (13)" --write-tags


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import requests
import json
import base64
import argparse
import mimetypes


parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=False)
parser.add_argument('--folder', type=str, required=False)
parser.add_argument('--score', action='store_const', const=0)
parser.add_argument('--write-tags', action='store_const', const=1)
parser.add_argument('--no-json', action='store_const', const=1)
args = parser.parse_args()
count = ['1']
lst = []
if os.name == 'nt':
    exepath = os.path.join(os.path.dirname(__file__), 'exiftool.exe')
else:
    exepath = os.path.join(os.path.dirname(__file__), 'exiftool')

def scan_folder(folder):
    for subdir, dirs, files in os.walk(folder):
        for fn in files:
            fullpath = os.path.join(subdir, fn)
            try:
                mime2 = mimetypes.guess_type(fullpath)
                if 'image' in mime2[0] and ('jpeg' in mime2[0] or 'png' in mime2[0] or 'tiff' in mime2[0]) and mime2[0] is not None:
                    single_image(fullpath)
            except TypeError:
                pass

def single_image(img):
    with open(img, 'rb') as img_file:
        string = base64.b64encode(img_file.read())

    body_post = json.dumps({
        "requests": [{
            "image": { "content": string.decode('utf-8') },
            "features": [
                { "type": "LABEL_DETECTION" },
                { "type": "SAFE_SEARCH_DETECTION" },
                { "type": "WEB_DETECTION" }
            ]
        }]
    })
    full_path = os.path.splitext(img)
    file3 = os.path.basename(img)
    file2 = os.path.splitext(file3)
    endpoint = full_path[0]+'.json'
    if not os.path.exists(endpoint):
        vision(body_post, img)
        count.append(img)
    else:
        with open(endpoint, 'r', encoding='utf-8') as jfile:
            j_str = jfile.read()
            parse_meta(j_str, img)

def vision(jdata, img):
    scopes = ['https://www.googleapis.com/auth/cloud-vision']
    creds = None

    if os.path.exists('vision_token.json'):
        creds = Credentials.from_authorized_user_file('vision_token.json', scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        with open('vision_token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('vision', 'v1', credentials=creds)
    token = service._http.credentials.token
    headers = {'Authorization': 'Bearer {}' .format(token)}
    url_post =  'https://vision.googleapis.com/v1/images:annotate'
    first_post = requests.post(url_post, headers=headers, data=jdata)
    print('{} API requests so far' .format(len(count)))
    parse_meta(first_post.text, img)
    full_path = os.path.splitext(img)
    file3 = os.path.basename(img)
    file2 = os.path.splitext(file3)
    endpoint = full_path[0]+'.json'
    with open(endpoint, 'w', encoding='utf-8') as token:
        token.write(first_post.text)

def parse_meta(data, path):
    data = json.loads(data)
    adult = data['responses'][0]['safeSearchAnnotation']['adult']
    violence = data['responses'][0]['safeSearchAnnotation']['violence']
    racy = data['responses'][0]['safeSearchAnnotation']['racy']
    labels = data['responses'][0]['labelAnnotations']
    labels2 = [[item['description'], item['score']] for item in labels]
    labels_text = [item['description'] for item in labels]
    web = data['responses'][0]['webDetection']
    web_labels = web['bestGuessLabels'][0]['label']
    try:
        web_similar = [item2['url'] for item2 in web['visuallySimilarImages']]
    except:
        web_similar = ''
    try:
        web_partial = [item2['url'] for item2 in web['partialMatchingImages']]
    except:
        web_partial = ''
    try:
        web_full = [item2['url'] for item2 in web['fullMatchingImages']]
    except:
        web_full = ''
    try:
        for item in web['webEntities']:
            try:
                lst.append((item['description']))
            except:
                pass

    except:
        web_ent = ''
    try:
        web_pages = [[item2['url'], item2['pageTitle']] for item2 in web['pagesWithMatchingImages']]
    except:
        web_pages = ''

    date_mod = os.path.getmtime(path)
    date_a = os.path.getatime(path)
    dates = date_a, date_mod
    labels_final = ', '.join(labels_text)
    web_labels_final = ', '.join(lst)
    try:
        labels_fin = web_labels+' '+labels_final+web_labels_final
    except:
        try:
            labels_fin = web_labels+labels_final
        except:
            labels_fin = labels_final
    if args.write_tags == 1:
        try:
            if os.name == 'nt':
                os.system('exiftool.exe -EXIF:UserComment="{}" "{}"' .format(labels_fin, path))
            else:
                os.system('./exiftool -EXIF:UserComment="{}" "{}"' .format(labels_fin, path))
        except Exception as e:
            pass
        try:
            if os.name == 'nt':
                os.system('exiftool.exe -EXIF:XPSubject="{}" "{}"' .format(labels_fin, path))
            else:
                os.system('./exiftool -EXIF:XPSubject="{}" "{}"' .format(labels_fin, path))
        except Exception as e:
            pass
        try:
            if os.name == 'nt':
                os.system('exiftool.exe -EXIF:XPTitle="{}" "{}"' .format(web_labels, path))
            else:
                os.system('./exiftool -EXIF:XPTitle="{}" "{}"' .format(web_labels, path))
        except Exception as e:
            pass
        try:
            if os.name == 'nt':
                os.system('exiftool.exe -XMP:Subject="{}" "{}"' .format(labels_fin, path))
            else:
                os.system('./exiftool -XMP:Subject="{}" "{}"' .format(labels_fin, path))
        except Exception as e:
            pass
        try:
            if os.name == 'nt':
                os.system('exiftool.exe -XMP:LastKeywordXMP="{}" "{}"' .format(labels_fin, path))
            else:
                os.system('./exiftool -XMP:LastKeywordXMP="{}" "{}"' .format(labels_fin, path))
        except Exception as e:
            pass

        os.utime(path, times=dates)
        print('Wrote metadata (\"{}...\") to {}' .format(labels_fin[0:20], path))
        if os.path.exists(path+'_original'):
            os.remove(path+'_original')

    else:
        print('Wrote json only (\"{}...\") to {}' .format(labels_fin[0:20], path))

if not os.path.exists('credentials.json'):
    print('Need a Desktop App credentials.json OAuth file from https://console.developers.google.com/')

if args.file != None:
    single_image(args.file)

if args.folder != None:
    scan_folder(args.folder)

if args.folder == None and args.file == None:
    print('Scan a folder recursively with --folder')
    print('Or a single file with --file')

