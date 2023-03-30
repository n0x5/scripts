# rename image files in a folder with the "date modified" in filename.

import time
import os
import shutil


cwd = r'/mnt/c/image_folder'


for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        fullpath = os.path.join(subdir, fn)
        subfolder = os.path.basename(os.path.join(subdir))
        try:
            fn2 = time.strftime('%Y_%m_%d__%H_%M_%S', time.gmtime(os.path.getmtime(fullpath)))+'__'+fn
            path_dest = os.path.join(cwd, fn2)
            print(path_dest)
            shutil.move(fullpath, path_dest)

        except Exception as e:
            print(e)
            pass
