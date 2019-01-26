import pysolr
import json

solr = pysolr.Solr("http://localhost:8983/solr/test_core", timeout=10)

with open("memes.dat", 'r') as f:
    memeData = json.loads(f.read())

data = [ {
    "id": id,
    "title": memeData[id]['title'],
    "url": memeData[id]['url'],
    "image_text": memeData[id]['imText']
} for id in memeData]

solr.add(data, commit=True)

def test_results():
    return memeData

def solr_search(query):
    return solr.search('title:' + query).docs
