import os
import re
import pymysql
import argparse
import subprocess
import time
import zlib

conn = pymysql.connect(host='', user='', passwd='', charset ='utf8')
cur = conn.cursor()
cur.execute("USE sfv")

cwd = r'/path/to/rls'
erlist = []

def sfvdb(subdir):
    rls = os.path.basename(subdir)
    try:
        lmatch = cur.execute("select cast(uncompress(rel_sfv) as char) from sfv WHERE rel_name like '{}'" .format(rls))
        results = [item[0] for item in cur.fetchall()]
        if lmatch > 0:
            results2 = [item for item in results]
            for item3 in results2:
                sfvdb = item3.split('\n')

            return sfvdb
    except:
        return 'None'

for subdir, dirs, files in os.walk(cwd):
    sfvdata = sfvdb(subdir.lower().replace('\cd1', '').replace('\cd2', ''))
    fname = os.path.join(cwd, 'errors.txt')
    for fn in files:
        if fn.endswith('.sfv'):
            print(subdir)
            try:
                for line in sfvdata:
                    try:
                        sfv1 = line.split()[1].lower()
                        sfv2 = line.split()[0].lower()
                        sf1 = os.path.join(subdir, line.split()[0])
                    except Exception as e:
                        pass
                    if not sfv2.startswith(';'):
                        try:
                            sf = open(sf1,'rb').read()
                        except:
                            erlist.append(sf1)
                            print('not found', sf1)
                            pass

                        sf2 = format(zlib.crc32(sf), '08x')
                        if sfv1 != sf2:
                            erlist.append(sf1)
                            hfile = open(fname, 'a')
                            hfile.write(sf1+'\n')
                            hfile.flush()
                            hfile.close()
                            print('wrong crc', sf1)
                        else:
                            print('crc ok {} {} {}' .format(sfv1, sf2, sf1))
                            pass
                    else:
                        pass
            except: 
                print('sfv not in db for', subdir)
                pass


cur.close()
conn.close()
