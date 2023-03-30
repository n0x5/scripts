# rename image files in a folder with the "date taken" exif metadata in filename.

import time
import os
import pyexiv2
import shutil

cwd = r'/mnt/c/image_folder'


for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        fullpath = os.path.join(subdir, fn)
        subfolder = os.path.basename(os.path.join(subdir))
        try:
            ex2 = pyexiv2.ImageMetadata(fullpath)
            ex2.read()
            date_orig = ex2['Exif.Photo.DateTimeOriginal'].value
            date_orig_form = str(date_orig).replace('-', '_').replace(' ', '__').replace(':', '_')+'__'+fn
            rootdir2 = os.path.join(cwd, fn)
            path_dest = os.path.join(cwd, date_orig_form)
            print(path_dest)
            shutil.move(rootdir2, path_dest)

        except Exception as e:
            print(e)
            pass
