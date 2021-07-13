import sqlite3
import os


connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'movies44.db'))
cursor = connection.cursor()


def pages(lastvalue):
    cursor.execute('select release, director from movies where release > ? order by release limit 8', (lastvalue,))
    results = [(item[0], item[1]) for item in cursor.fetchall()]
    lastvalue = results[7][0]
    firstvalue = results[0][0]
    print(results)
    try:
        pages(lastvalue)
    except:
        cursor.execute('select release, director from movies where release > ? order by release limit 8', (firstvalue,))
        results = [(item[0], item[1]) for item in cursor.fetchall()]
        print(results)

pages('007.Die.Another.Day.PROPER.DVDRiP.XviD-DEiTY')
