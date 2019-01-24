import pysolr

solr = pysolr.Solr("http://localhost:8983/solr/test_core", timeout=10)

def test_results():
    return [
        ["https://i.redd.it/epi43xbrie521.jpg", "its a simple spell but quite unbreakable", 0],
        ["https://i.redd.it/eg49qet98e521.jpg", "evolution dude fuck off", 1],
        ["https://i.redd.it/ncz4jbefif521.jpg", "link young toon lonk", 2],
    ]

def solr_search(query):
    return solr.search('title:' + query).docs
