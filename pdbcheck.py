import os
import re
import pymysql
import subprocess


conn = pymysql.connect(host='', user='', passwd='', charset ='utf8')
cur = conn.cursor()
cur.execute("USE predb2")

cwd = r'/path/to/rls'

for subdir, dirs, files in os.walk(cwd):
    rls = os.path.basename(subdir)
    try:
        lmatch = cur.execute("select rel_name from predb.allpres WHERE rel_name like '{}'" .format(rls))
        if lmatch > 0:
            pass
        else:
            lmatch2 = cur.execute("select rel_name from predb2.allpres WHERE rel_name like '{}'" .format(rls))
            if lmatch2 > 0:
                pass
            else:
                if not 'web-201' in rls.lower():
                    print('NO MATCH for ->', rls)
    except:
        pass

cur.close()
conn.close()
