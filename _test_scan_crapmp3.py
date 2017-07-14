import os

rootdir = r'/mp3/path'

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if os.path.basename(subdir).lower()[4:10] not in fn.lower() and '.mp3' not in fn and '.message' not in fn and 'LABEL' not in fn:
            print(subdir.lower()+'\\'+fn)
