# just a script to convert raw to tif, only to have the capability
# if other raw software is not available at the time

import os
import rawpy
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

img = args.file
endpoint1 = os.path.splitext(img)

raw = rawpy.imread(img)
string1 = raw.postprocess()
string = Image.fromarray(string1.astype('uint8'), 'RGB')
endpoint = endpoint1[0]+'.tif'
print(endpoint)
string.save(endpoint, format='TIFF')
