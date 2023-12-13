# Script to automatically scan images and describe them with llamafile created by justine
#
# Change 'cwd' to the directory you want to scan. add .exe to end of llamafile on windows (maybe not needed but i did)
# add llamafile to PATH
#
# https://justine.lol/oneliners/
# wget https://huggingface.co/jartine/llava-v1.5-7B-GGUF/resolve/main/llava-v1.5-7b-q4-main.llamafile
#
# on windows download these two for GPU inference (much faster, around 2-5 secs on 4070):
# https://visualstudio.microsoft.com/vs/community/
# https://developer.nvidia.com/cuda-downloads
#
# add "cl.exe" to PATH (C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\bin\Hostx64\x64\) on mine


import subprocess
import os
import re
import sqlite3

conn = sqlite3.connect('image_llama.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists images
        (filename text, filepath text, description text, keywords text)''')

cwd = r'F:\archive\_personal\camera\2014'

for subdir, dirs, files in os.walk(cwd):
    for fn in files:
        if  '.jpg' in fn.lower():
            full = os.path.join(subdir, fn)
            cur.execute('select exists(select 1 from images where filepath = ? LIMIT 1)', (full,))
            record = cur.fetchone()
            if record[0] == 1:
                print('DB entry already exists', full)
            else:
                proc = subprocess.Popen(['llava-v1.5-7b-q4-main.llamafile.exe', '--image', '{}' .format(fn), '--temp', '0', '-p', '$### User: List the keywords of the subjects, people, persons, objects, clothing and atmosphere and colors in this image in a comma-delimited list (,). \
                                        Then on a new line create a paragraph of describing description of the subjects, motifs, background, objects, atmosphere and colors in the image.\n### Assistant:', '--silent-prompt', '-ngl', '35'], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print('###############', fn)
                output, errors = proc.communicate(timeout=950)
                result = output.decode("utf-8").strip()
                try:
                    res2 = result.split('\n\n')
                    keywords = res2[0]
                except:
                    keywords = ''
                try:
                    res2 = result.split('\n\n')
                    desc = res2[1]
                except:
                    desc = result
                stuff = fn, full, desc, keywords
                cur.execute('insert or ignore into images (filename, filepath, description, keywords) VALUES (?,?,?,?)', (stuff))
                cur.connection.commit()
                print('Added {} to db' .format(stuff))
