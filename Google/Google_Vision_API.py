# Upload image to Google Vision for image recognition
# Supports RAW files as well as .jpg/gif/png/etc
# Scan a folder recursively or give path to single file and write .json info in same folder
# Need Desktop App oauth2 credentials.json file in same folder
# pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib requests rawpy pillow
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
import rawpy
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=False)
parser.add_argument('--folder', type=str, required=False)
parser.add_argument('--score', action='store_const', const=0)
parser.add_argument('--write-tags', action='store_const', const=1)
parser.add_argument('--no-json', action='store_const', const=1)
args = parser.parse_args()
os.system('')
color = {
    'HEADER': '\033[95m',
    'ENDCOLOR': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'INVERSE': '\033[7m',
    'GRAY_BRIGHT': '\033[90m',
    'BLUE_BRIGHT': '\033[94m',
    'GREEN_BRIGHT': '\033[92m',
    'RED_BRIGHT': '\033[91m',
    'YELLOW_BRIGHT': '\033[93m',
    'MAGENTA_BRIGHT': '\033[95m',
    'CYAN_BRIGHT': '\033[96m',
    'WHITE_BRIGHT': '\033[97m',
    'RED_DIM': '\033[31m',
    'GREEN_DIM': '\033[32m',
    'YELLOW_DIM': '\033[33m',
    'BLUE_DIM': '\033[34m',
    'MAGENTA_DIM': '\033[35m',
    'CYAN_DIM': '\033[36m',
    'WHITE_DIM': '\033[37m',
    'BLACKBG_BRIGHT': '\033[100m',
    'REDBG_BRIGHT': '\033[101m',
    'GREENBG_BRIGHT': '\033[102m',
    'YELLOWBG_BRIGHT': '\033[103m',
    'BLUEBG_BRIGHT': '\033[104m',
    'MAGBG_BRIGHT': '\033[105m',
    'CYANBG_BRIGHT': '\033[106m',
    'WHITEBG_BRIGHT': '\033[107m',
}
count = ['1']
lst = []
lst_o2 = []

def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)

def scan_folder(folder):
    for subdir, dirs, files in os.walk(folder):
        for fn in files:
            fullpath = os.path.join(subdir, fn)
            try:
                mime2 = mimetypes.guess_type(fullpath)
                if 'image' in mime2[0] and ('jpeg' in mime2[0] or 'png' in mime2[0] or 'tiff' in mime2[0]) and mime2[0] is not None or fn.endswith('jpg'):
                #if fn.endswith('jpg') or fn.endswith('jpeg') or fn.endswith('jpg') or fn.endswith('tif') or fn.endswith('png'):
                    single_image(fullpath)
                if 'image' in mime2[0] and 'jpeg' not in mime2[0] and 'png' not in mime2[0] and 'tiff' not in mime2[0] and 'gif' not in mime2[0]:
                    single_image_raw(fullpath)
            except TypeError:
                pass

def single_image_raw(img):
    try:
        raw = rawpy.imread(img)
        string1 = raw.postprocess()
        string = Image.fromarray(string1.astype('uint8'), 'RGB')
        buffered = BytesIO()
        string.save(buffered, format='JPEG')
        img_str = base64.b64encode(buffered.getvalue())
        body_post = json.dumps({
            "requests": [{
                "image": { "content": img_str.decode('utf-8') },
                "features": [
                    { "type": "LABEL_DETECTION" },
                    { "type": "SAFE_SEARCH_DETECTION" },
                    { "type": "WEB_DETECTION" },
                    { "type": "FACE_DETECTION" },
                    { "type": "LANDMARK_DETECTION" },
                    { "type": "OBJECT_LOCALIZATION" }
                ]
            }]
        })
        full_path = os.path.splitext(img)
        file3 = os.path.basename(img)
        file2 = os.path.splitext(file3)
        endpoint = full_path[0]+'.json'
        endpoint_jpg = full_path[0]+'_TEMP'
        string.save(endpoint_jpg, format='JPEG')
        if not os.path.exists(endpoint) and '_objects.jpg' not in img:
            vision(body_post, img)
            count.append(img)
        else:
            with open(endpoint, 'r', encoding='utf-8') as jfile:
                j_str = jfile.read()
                parse_meta(j_str, img)
    except Exception as e:
        print(e)

def single_image(img):
    with open(img, 'rb') as img_file:
        string = base64.b64encode(img_file.read())

    body_post = json.dumps({
        "requests": [{
            "image": { "content": string.decode('utf-8') },
            "features": [
                { "type": "LABEL_DETECTION" },
                { "type": "SAFE_SEARCH_DETECTION" },
                { "type": "WEB_DETECTION" },
                { "type": "FACE_DETECTION" },
                { "type": "LANDMARK_DETECTION" },
                { "type": "OBJECT_LOCALIZATION" }
            ]
        }]
    })
    full_path = os.path.splitext(img)
    file3 = os.path.basename(img)
    file2 = os.path.splitext(file3)
    endpoint = full_path[0]+'.json'
    if not os.path.exists(endpoint) and '_objects.jpg' not in img:
        vision(body_post, img)
        count.append(img)
    else:
        try:
            with open(endpoint, 'r', encoding='utf-8') as jfile:
                j_str = jfile.read()
                parse_meta(j_str, img)
        except FileNotFoundError:
            pass

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
    print(r'{} API requests so far' .format(len(count)))
    full_path = os.path.splitext(img)
    file3 = os.path.basename(img)
    file2 = os.path.splitext(file3)
    endpoint = full_path[0]+'.json'
    with open(endpoint, 'w', encoding='utf-8', errors='backslashreplace') as token:
        token.write(first_post.text)

    parse_meta(first_post.text, img)

def parse_meta(data, path):
    data = json.loads(data)
    adult = data['responses'][0]['safeSearchAnnotation']['adult']
    violence = data['responses'][0]['safeSearchAnnotation']['violence']
    racy = data['responses'][0]['safeSearchAnnotation']['racy']
    labels = data['responses'][0]['labelAnnotations']
    labels2 = [[item['description'], item['score']] for item in labels]
    labels_text = [item['description'] for item in labels]
    web = data['responses'][0]['webDetection']
    web_labels = web['bestGuessLabels'][0]['label'].title()
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
    web_labels_final = remove_non_ascii(', '.join(lst))
    try:
        labels_fin = web_labels+', '+labels_final+web_labels_final
    except:
        try:
            labels_fin = web_labels+labels_final
        except:
            labels_fin = labels_final

    full_path = os.path.splitext(path)
    file3 = os.path.basename(path)
    file2 = os.path.splitext(file3)
    endpoint_jpeg = full_path[0]+'_TEMP'
    mime2 = mimetypes.guess_type(path)
    labels_dupe = ', '.join(set(labels_fin.split(', ')))
    try:
        if os.path.exists(endpoint_jpeg) and os.name == 'nt':
            command_raw2 = 'exiftool.exe -Sep ", " -EXIF:UserComment="{}" -EXIF:XPSubject="{}" -EXIF:XPTitle="{}" -XMP:Subject="{}" -XMP:LastKeywordXMP="{}" -XMP:Label="{}" "{}"' \
                .format(labels_dupe, labels_final, web_labels, labels_dupe, labels_final, labels_dupe, endpoint_jpeg)
            os.system(command_raw2)
    except Exception:
        pass

    if args.write_tags == 1 and 'image' in mime2[0] and ('jpeg' in mime2[0] or 'png' in mime2[0] or 'tiff' in mime2[0]):
        if os.name == 'nt':
            command = 'exiftool.exe -Sep ", " -EXIF:UserComment="{}" -EXIF:XPSubject="{}" -EXIF:XPTitle="{}" -XMP:Subject="{}" -XMP:LastKeywordXMP="{}" -XMP:Label="{}" "{}"' \
                    .format(labels_dupe, labels_final, web_labels, labels_dupe, labels_final, labels_dupe, path)
        else:
            command_unix = '{} -EXIF:UserComment="{}" -EXIF:XPSubject="{}" -EXIF:XPTitle="{}" -XMP:Subject="{}" -XMP:LastKeywordXMP="{}" -XMP:Label="{}" "{}"' \
                    .format(os.path.join(os.path.dirname( __file__ ), 'exiftool'), labels_dupe, labels_final, web_labels, labels_dupe, labels_final, labels_dupe, path)

        try:
            if os.name == 'nt':
                os.system(command)
            else:
                os.system(command_unix)
        except Exception as e:
            pass

        os.utime(path, times=dates)
        print('Wrote metadata {}(\"{}...\"){} to {}' .format(color['GRAY_BRIGHT'], labels_final[0:20], color['ENDCOLOR'], path))
        if os.path.exists(path+'_original'):
            os.remove(path+'_original')

        full_path = os.path.splitext(path)
        file3 = os.path.basename(path)
        file2 = os.path.splitext(file3)
        endpoint = full_path[0]+'.xmp'
        if os.name == 'nt':
            os.system('exiftool.exe -tagsfromfile "{}" "{}"' .format(path, endpoint))
        else:
            cmd1 = os.path.join(os.path.dirname( __file__ ), 'exiftool -tagsfromfile {} {}' .format(path, endpoint))
            os.system(cmd1)
        print('Created XMP at {}' .format(endpoint))
        if os.path.exists(endpoint+'_original'):
            os.remove(endpoint+'_original')

    else:
        print('Wrote json only (\"{}{}{}...\") to {}{}{}' .format(color['GREEN_DIM'], labels_final[0:20], color['ENDCOLOR'], color['WHITE_DIM'], path, color['ENDCOLOR']))
        full_path = os.path.splitext(path)
        file3 = os.path.basename(path)
        file2 = os.path.splitext(file3)
        endpoint = full_path[0]+'.xmp'
        
        if os.name == 'nt' and os.path.exists(endpoint_jpeg):
            os.system('exiftool.exe -tagsfromfile {} {}' .format(endpoint_jpeg, endpoint))
        else:
            cmd1 = os.path.join(os.path.dirname( __file__ ), 'exiftool -tagsfromfile "{}" "{}"' .format(endpoint_jpeg, endpoint))
            os.system(cmd1)
        print('Created XMP at {}' .format(endpoint))
        os.remove(endpoint_jpeg)
        if os.path.exists(endpoint+'_original'):
            os.remove(endpoint+'_original')

    try:
        objects = data['responses'][0]['localizedObjectAnnotations']
        lst_obj = []
        for item in objects:
            lst_obj.append([item['name'], item['boundingPoly']['normalizedVertices']])

        detect_objects(lst_obj, path)
    except Exception:
        print('no objects detected')
        pass

def detect_objects(objects, path):
    pillow_img = Image.open(path)
    w, h = pillow_img.size
    for item in objects:
        obj_name = item[0]
        vertices = item[1]
        position = (vertices[0]['x'] * w, vertices[0]['y'] * h)

        shape1 = [(vertices[0]['x'] * w, vertices[0]['y'] * h), ((vertices[3]['x'] * w, vertices[3]['y'] * h))]
        shape2 = [(vertices[2]['x'] * w, vertices[2]['y'] * h), ((vertices[1]['x'] * w, vertices[1]['y'] * h))]
        shape3 = [(vertices[0]['x'] * w, vertices[0]['y'] * h), ((vertices[1]['x'] * w, vertices[1]['y'] * h))]
        shape4 = [(vertices[2]['x'] * w, vertices[2]['y'] * h), ((vertices[3]['x'] * w, vertices[3]['y'] * h))]

        img1 = ImageDraw.Draw(pillow_img)  
        img1.line(shape1, fill='red', width = 0)
        img1.line(shape2, fill='red', width = 0)
        img1.line(shape3, fill='red', width = 0)
        img1.line(shape4, fill='red', width = 0)
        draw = ImageDraw.Draw(pillow_img)
        font = ImageFont.truetype('ARIAL.TTF', 30)
        draw.text(position, obj_name, font=font, fill='red')

    full_path = os.path.splitext(path)
    endpoint_obj = full_path[0]+'_objects'+'.jpg'
    if '_objects.jpg' not in path:
        pillow_img.save(endpoint_obj, format='JPEG', subsampling=0, quality=85)

if not os.path.exists('credentials.json'):
    print('Need a Desktop App credentials.json OAuth file from https://console.developers.google.com/')

if args.file != None:
    single_image(args.file)

if args.folder != None:
    scan_folder(args.folder)

if args.folder == None and args.file == None:
    print('Scan a folder recursively with --folder')
    print('Or a single file with --file')



