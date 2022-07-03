import os

path = r'F:\dev'

def scant(path):
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                statinfo = os.stat(entry.path)
                print('File: ', entry.path.encode('utf-8', 'replace').decode('ISO-8859-1'))
                print('Stats: ', statinfo)
            if entry.is_dir():
                print('Directory: ', entry.path)
                scant(entry.path)

scant(path)