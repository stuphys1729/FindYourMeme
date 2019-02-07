import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn_m = sqlite3.connect('memes.db')
conn_n = sqlite3.connect('new_memes.db')

conn_m.row_factory = dict_factory
conn_n.row_factory = dict_factory

cm = conn_m.cursor()
cn = conn_n.cursor()

cn.execute('''
            CREATE TABLE IF NOT EXISTS memes(
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

for record in cm.execute("SELECT * FROM memes").fetchall():
    # TODO get the datetime field and add to db as unixepoch
    print(record)
