import re
import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import os
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions
import json

number = 10
#emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-mpnet-base-v2')

client = chromadb.PersistentClient(path='wikivecs1')
collection = client.get_or_create_collection('wiki', metadata={"hnsw:space": "cosine"})


sql_db = r'F:\dev\wikitv.db'
conn = sqlite3.connect(sql_db)
cur = conn.cursor()

sql = 'select title, content from wikitv'
results = cur.execute(sql)

for item in tqdm(results):
    string = item[1]
    collection.add(documents=['{}' .format(string)], metadatas=[{'source': 'wiki-tv'}], ids=[item[0]],)

results = collection.query(
    query_texts = ['a tv show episode where aliens take over washington dc'],
    n_results = number,
    # where={'metadata_field': 'is_equal_to_this'}, # optional filter
    # where_document={'$contains':'search_string'}  # optional filter
)


for item in range(0, number):
    stuff = results['ids'][0][item], results['distances'][0][item]
    print(stuff)

