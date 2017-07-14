import os

rootdir = r'/root/mp3'

for subdir, dirs, files in os.walk(rootdir):
    for fn in files:
        if os.path.basename(subdir).lower()[4:10] not in fn.lower() and '.mp3' not in fn and '.message' not in fn and 'LABEL' not in fn:
            print(subdir.lower()+'\\'+fn)
            #os.remove(os.path.join(subdir, fn)) # Uncomment to delete matching files
