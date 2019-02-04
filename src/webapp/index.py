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

def create_db():
    with sqlite3.connect('memes.db') as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS memes(
                id PRIMARY KEY
                , title TEXT
                , url TEXT
                , plink TEXT
                , time TEXT
                , sub TEXT
                , image_text TEXT
                , posted_by TEXT
                , score INTEGER
                , upvote_ratio REAL
                , over_18 TEXT
        )''')
        conn.commit()

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
            INSERT OR REPLACE INTO memes VALUES(?,?,?,?,?,?,?,?,?,?)''',
            (meme['id'], meme['title'], meme['url'], meme['plink'], meme['time'], meme['sub'], meme['image_text'], meme['posted_by'], meme['score'], meme['upvote_ratio'], meme['over_18']))
        conn.commit()

    return result

def solr_search(query):
    if query == "*":
        return solr.search("*", **{
            'rows': '100'
        })

    return solr.search('title:' + query).docs

def setup_collection():
    # TODO this is gonna have to change given that new data is being added
    while True:
        time.sleep(10)
        print("Scraping...")

        # if os.path.isfile('memes.json'):
        #     with open("memes.json", 'r') as f:
        #         memeData = json.loads(f.read())

        #     add_to_solr(memeData)

        # else:
        #     memeData = {}

        newData = update_meme_data(memeData)

        add_to_solr(newData)

def add_to_solr(source_dict):
    data = [{
        "id": meme_id,
        "title": meme_data['title'],
        "url": meme_data['url'],
        "image_text": meme_data['image_text'],
        "posted_by": meme_data['posted_by'],
        "score": meme_data['score'],
        "upvote_ratio": meme_data['upvote_ratio'],
        "over_18": meme_data['over_18']
    } for meme_id, meme_data in source_dict.items()]

    # TODO add to both solr and db
    solr.add(data, commit=True)
