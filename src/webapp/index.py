import pysolr
import json
from .scraping import update_meme_data
import os

solr = pysolr.Solr("http://localhost:8983/solr/test_core", timeout=10)

def test_results():
    return memeData

def solr_search(query):
    return solr.search('title:' + query).docs

def setup_collection():

    if os.path.isfile('memes.json'):
        with open("memes.json", 'r') as f:
            memeData = json.loads(f.read())

        data = [ {
            "id": id,
            "title": memeData[id]['title'],
            "url": memeData[id]['url'],
            "image_text": memeData[id]['imText']
        } for id in memeData]

        solr.add(data, commit=True)

    else:
        memeData = {}

    newData = update_meme_data(memeData)

    data = [ {
        "id": id,
        "title": memeData[id]['title'],
        "url": memeData[id]['url'],
        "image_text": memeData[id]['imText']
    } for id in newData]

    solr.add(data, commit=True)
