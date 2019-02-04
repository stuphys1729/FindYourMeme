import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('test.db')
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
)''')

with open("memes.json", 'r') as f:
    memeData = json.loads(f.read())

conn.commit()

for key, meme in memeData.items():
    c.execute('''
        INSERT OR REPLACE INTO memes VALUES(?,?,?,?,?,?,?)
    ''', (key, meme['title'], meme['url'], meme['plink'], meme['time'], meme['sub'], meme['image_text']
    ))

conn.commit()

for row in c.execute("SELECT * FROM memes"):
    print(row)

# c.execute("DELETE FROM memes WHERE id='abcde'")

conn.commit()
conn.close()
