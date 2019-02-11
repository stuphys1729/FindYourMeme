import pysolr
import json
from .scraping import update_meme_data
import os
import sqlite3
import time
from datetime import datetime

core_name = "meme_data"
db_name = "memes.db"

solr = pysolr.Solr("http://localhost:8983/solr/" + core_name, timeout=10)
memeData = {}

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_db():
    with sqlite3.connect(db_name) as conn:
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
                , rscore INTEGER
                , upvote_ratio REAL
                , over_18 TEXT
                , time_of_index TEXT
                , format TEXT
        )''')
        conn.commit()

    print("Database created successfully")

def fetch_meme(meme_id):
    result = None

    with sqlite3.connect(db_name) as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()
        result = c.execute("SELECT * FROM memes WHERE id=?", (meme_id,)).fetchone()
        conn.commit()

    return result

def write_meme(meme):
    result = None

    with sqlite3.connect(db_name) as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()

        result = c.execute('''
            INSERT OR REPLACE INTO memes VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (meme['id'], meme['title'], meme['url'], meme['plink'], meme['time'], meme['sub'], meme['image_text'], meme['posted_by'], meme['rscore'], meme['upvote_ratio'], meme['over_18'], meme['time_of_index'], meme['format']))
        conn.commit()

    return result

def write_memes_batch(meme_list):
    result = None

    with sqlite3.connect('memes.db') as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()

        result = c.executemany('''
            INSERT OR REPLACE INTO memes VALUES(?,?,?,?,datetime(?),?,?,?,?,?,?,datetime(?),?)''',
            meme_list)
        conn.commit()

    return result


def update_meme(meme):
    result = None

    with sqlite3.connect(db_name) as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()

        result = c.execute('''
            UPDATE memes SET rscore=:rscore, upvote_ratio=:upvote_ratio, time_of_index=datetime(:time_of_index) WHERE id=:id''',
            {'id': meme['id'], 'rscore': meme['rscore'], 'upvote_ratio': meme['upvote_ratio'], 'time_of_index': meme['time_of_index'] })
        conn.commit()

    return result


def update_memes_batch(meme_list):
    result = None

    with sqlite3.connect('memes.db') as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()

        result = c.executemany('''
            UPDATE memes SET rscore=:rscore, upvote_ratio=:upvote_ratio, time_of_index=datetime(:time_of_index) WHERE id=:id''',
            meme_list)
        conn.commit()

    return result


def solr_search(query, no_terms, page_no, time_since, nsfw, subreddits):
    if query == "*" or len(query.strip()) == 0:
        search_query = "*:*"
    else:
        search_query = "_text_:" + query

    timerange = ""

    if len(time_since) > 0:
        timerange = "time:[NOW" + time_since + " TO NOW]"

    if len(subreddits) > 0:
        for sub in subreddits:
            search_query += " AND sub:'%s'" % sub

    if len(nsfw) == 1:
        if nsfw[0] == "1":
            search_query += ' AND over_18:1'
        elif nsfw[0] == "none":
            # No safe search
            pass
    else:
        search_query += " AND over_18:0"

    start = str(page_no*no_terms)
    sort = "sum(if(gt(abs(product(rscore,sub(product(2,upvote_ratio),1))) ,1),abs(product(rscore,sub(product(2,upvote_ratio),1))) ,1),div(time,43200)) desc"

    print(search_query)

    return solr.search(search_query, **{
        "rows": str(no_terms)
        , "start": start
        , "sort": sort
        , "fq": timerange
    }).docs

def setup_collection():
    print("Scraping...")
    # , 'adviceanimals'
    subreddits = ['dankmemes', 'meirl', 'memes', 'prequelmemes', 'wholesomememes', 'dankchristianmemes', 'lotrmemes', 'sequelmemes']
    for subreddit in subreddits:
        newData = update_meme_data(subreddit, is_id_in_db)
        add_memes(newData)
    print("Finised scraping.")

def add_memes(source_dict):

    update_list = []
    write_list  = []
    update_data = []

    for meme_id, meme_data in source_dict.items():
        if is_id_in_db(meme_id):
            update_list.append({
                "id": meme_id,
                "rscore": meme_data['rscore'],
                "upvote_ratio": meme_data['upvote_ratio'],
                "time_of_index": meme_data['time_of_index']
            })
        else:
            write_list.append({
                "id": meme_id,
                "title": meme_data['title'],
                "url": meme_data['url'],
                "plink": meme_data['plink'],
                "time": datetime.utcfromtimestamp(float(meme_data['time'])).strftime('%Y-%m-%d %H:%M:%S'),
                "sub": meme_data['sub'],
                "image_text": " " + meme_data['image_text'],
                "posted_by": meme_data['posted_by'],
                "rscore": meme_data['rscore'],
                "upvote_ratio": meme_data['upvote_ratio'],
                "over_18": meme_data['over_18'],
                "time_of_index": meme_data['time_of_index'],
                "format": meme_data['format']
            })
    print("Writing {} new memes to database".format(len(write_list)))
    print("Updating {} existing memes in the database".format(len(update_list)))

    write_tuples = [tuple(d.values()) for d in write_list]
    if write_tuples != []:
        write_memes_batch(write_tuples)
    if update_list != []:
        update_memes_batch(update_list)

    sync_solr_with_db()

def sync_solr_with_db():
    solr.delete(q="*:*")

    with sqlite3.connect(db_name) as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()

        results = c.execute('SELECT * FROM memes').fetchall()
        solr.add(results, commit=True)

def is_id_in_db(meme_id):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()

        if len(c.execute("SELECT * FROM memes WHERE id = ?", (meme_id,)).fetchall()) > 0:
            return True

        return False
