import pysolr
import json
from .scraping import update_meme_data
import os
import sqlite3
import time

solr = pysolr.Solr("http://localhost:8983/solr/test_core", timeout=10)
memeData = {}

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def fetch_meme(meme_id):
    with sqlite3.connect('test.db') as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()
        result = c.execute("SELECT * FROM memes WHERE id=?", (meme_id,)).fetchone()
        conn.commit()

    return result

def write_meme(meme):
    with sqlite3.connect('test.db') as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()
        result = c.execute('''
            INSERT OR REPLACE INTO memes VALUES(?,?,?,?,?,?,?)''',
            (meme['id'], meme['title'], meme['url'], meme['plink'], meme['time'], meme['sub'], meme['image_text']))
        conn.commit()

    return result

def solr_search(query):
    if query == "*":
        return solr.search("*", **{
            'rows': '100'
        })

    return solr.search('title:' + query).docs

def setup_collection():
    while True:
        time.sleep(60)
        print("Scraping...")
        if os.path.isfile('memes.json'):
            with open("memes.json", 'r') as f:
                memeData = json.loads(f.read())

            data = [ {
                "id": id,
                "title": memeData[id]['title'],
                "url": memeData[id]['url'],
                "image_text": memeData[id]['image_text']
            } for id in memeData]

            solr.add(data, commit=True)

        else:
            memeData = {}

        newData = update_meme_data(memeData)

        data = [ {
            "id": id,
            "title": memeData[id]['title'],
            "url": memeData[id]['url'],
            "image_text": memeData[id]['image_text']
        } for id in newData]

        solr.add(data, commit=True)
        solr.commit()
