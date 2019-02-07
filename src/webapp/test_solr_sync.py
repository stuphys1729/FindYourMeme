import pysolr
import sqlite3

solr = pysolr.Solr("http://localhost:8983/solr/test_core_2", timeout=10)
db = "new_memes.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

with sqlite3.connect(db) as conn:
    conn.row_factory = dict_factory
    c = conn.cursor()

    results = c.execute('SELECT * FROM memes').fetchall()
    solr.add(results, commit=True)
