# resize all images in a folder that ends with .jpg
# provide an optional folder (else uses current working dir)
# and provide a base width to resize to (e.g. '1500')

from PIL import Image
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('folder', nargs='?', default=os.getcwd())
parser.add_argument('width')
args = parser.parse_args()

new_width = int(args.width)
cwd = args.folder

def resize(image, cwd, new_width):
    im = Image.open(str(os.path.join(cwd, image))).convert('RGB')
    widthper = (new_width/float(im.size[0]))
    heightsize = int((float(im.size[1])*float(widthper)))
    size = new_width, heightsize
    im2 = im.resize(size, Image.LANCZOS)
    quality_val = 100
    thumbs2 = os.path.join(cwd, 'resized_'+str(new_width)+'_'+image)
    if not os.path.exists(thumbs2): 
        im2.save(thumbs2, "JPEG", quality=quality_val)
        print(str(image)+' resized to -> '+str(new_width)+'x'+str(heightsize))


for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if fn.endswith(".jpg") or fn.endswith(".jpeg"):
            resize(fn, cwd, new_width)
