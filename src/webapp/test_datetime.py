import sqlite3

conn_m = sqlite3.connect('memes.db')
conn_n = sqlite3.connect('new_memes.db')

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
        )''')
