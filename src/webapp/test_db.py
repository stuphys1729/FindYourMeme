import sqlite3
import json

conn = sqlite3.connect('test.db')
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
    ''', (
    key
    , meme['title']
    , meme['url']
    , meme['plink']
    , meme['time']
    , meme['sub']
    , meme['imText']
    ))
    # print('==')
    # print(key, meme)


conn.commit()

for row in c.execute("SELECT * FROM memes"):
    print(row)

c.execute("DELETE FROM memes WHERE id='abcde'")

conn.commit()
