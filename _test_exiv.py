# pip3 install py3exiv2 (linux only)

import pyexiv2

fullpath = r'/mnt/f/archive/_personal/camera/2010/DSC_1078.JPG'

ex2 = pyexiv2.ImageMetadata(fullpath)
ex2.read()

for item in ex2:
    print(ex2[item].key, ex2[item].value)