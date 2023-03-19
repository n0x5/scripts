# Git repo commit history to sqlite3
# Saves the body of commit history to a sqlite3 database
# Only saves unique versions of each file in the repo.
#
# Set 'repo_dir' folder to your local git repo path (does not work online repos atm)
# Change branch_name ("master", "main", etc)
# pip install gitpython

from git import Repo
import sqlite3
import os
import difflib
from tqdm import tqdm


repo_dir = r'F:\dev\GitHub-Desktop\Wordpress-Themes-Plugins'
branch_name = 'main'
repo = Repo(repo_dir)

repo_name = repo.remotes.origin.url.split('.git')[0].split('/')[-1]
repo_url = repo.remotes.origin.url


sql_db = os.path.join(os.path.dirname( __file__ ), '{}.db' .format(repo_name))
conn = sqlite3.connect(sql_db)
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists `{}`
        (hexsha text unique, repo_name text, repo_url text, item_name text, item_size text, item_type text, item_path text, author_name text,
        author_email text, authored_date int, content text unique)''' .format(repo_name))

lst = []

for item in tqdm(repo.heads[branch_name].commit.tree):
    data = item.data_stream.read()
    commits = repo.iter_commits('--all', paths=item.path)
    for item2 in commits:
        for item3 in item2.tree:
            sss = str(item3.data_stream.read().decode('UTF-8', errors='replace'))
            stuff = item2.hexsha, repo_name, repo_url, item.name, item.size, item.type, item.path, \
                    item2.author.name, item2.author.email, item2.authored_date, sss
            cur.execute('''insert or ignore into `{}` (hexsha, repo_name, repo_url, item_name, item_size, 
                        item_type, item_path, author_name, author_email, authored_date, content) VALUES (?,?,?,?,?,?,?,?,?,?,?)''' .format(repo_name), (stuff))
            cur.connection.commit()
            print(stuff)

