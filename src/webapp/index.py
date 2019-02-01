import pysolr
import hashlib
from PIL import Image
import requests
from io import BytesIO

solr = pysolr.Solr("http://localhost:8983/solr/test_core", timeout=10)
delete_hash = '45172ac97d574bfd34a1005262a23169'
m = hashlib.md5()

def test_results():
    return [
        ["https://i.redd.it/epi43xbrie521.jpg", "its a simple spell but quite unbreakable", 0],
        ["https://i.redd.it/eg49qet98e521.jpg", "evolution dude fuck off", 1],
        ["https://i.redd.it/ncz4jbefif521.jpg", "link young toon lonk", 2],
    ]

def solr_search(query):
    return solr.search('title:' + query).docs

def is_deleted(url):
    # Load url, convert to bytes, load as image and get bytes of that
    img = Image.open(BytesIO(requests.get(url).content)).tobytes()
    m.update(img)
    print(m.hexdigest())
    print(hashlib.md5(img).hexdigest())

    if m.hexdigest() == delete_hash:
        return True, m.hexdigest()

    return False, m.hexdigest()
