import sqlite3
from datetime import datetime as dt

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn_m = sqlite3.connect('memes.db')
conn_n = sqlite3.connect('new_memes.db')

conn_m.row_factory = dict_factory

cm = conn_m.cursor()
cn = conn_n.cursor()

cn.execute('''DROP TABLE memes''')
conn_n.commit()

cn.execute('''
            CREATE TABLE memes(
                id PRIMARY KEY
                , title TEXT
                , url TEXT
                , plink TEXT
                , time DATETIME
                , sub TEXT
                , image_text TEXT
                , posted_by TEXT
                , score INTEGER
                , upvote_ratio REAL
                , over_18 TEXT
                , time_of_index DATETIME
                , format TEXT
        )''')
conn_n.commit()

results = cm.execute("SELECT * FROM memes").fetchall()

for record in results:
    record.update((k, dt.utcfromtimestamp(float(v)).strftime('%Y-%m-%d %H:%M:%S')) for k, v in record.items() if k == "time")

results_tuples = [tuple(d.values()) for d in results]
print(len(results_tuples[0]))

cn.executemany('''INSERT OR REPLACE INTO memes
    VALUES(?,?,?,?,datetime(?),?,?,?,?,?,?,datetime(?),?)''',
    results_tuples)
conn_n.commit()
