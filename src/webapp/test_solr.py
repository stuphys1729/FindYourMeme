import pysolr
import json

solr = pysolr.Solr("http://localhost:8983/solr/test_core", timeout=10)

# solr.add([
#     {
#         "id": "doc_1",
#         "title": "A very small test document about elmo",
#     },
#     {
#         "id": "doc_3",
#         "title": "How about another test",
#     },
#     {
#         "id": "doc_2",
#         "title": "The Banana: Tasty or Dangerous?",
#         "_doc": [
#             { "id": "child_doc_1", "title": "peel" },
#             { "id": "child_doc_2", "title": "seed" },
#         ]
#     },
# ],  commit=True)
with open("memes.dat", 'r') as f:
    memeData = json.loads(f.read())

data = [ {
    "id": id,
    "title": memeData[id]['title'],
    "url": memeData[id]['url'],
    "image_text": memeData[id]['imText']
} for id in memeData]

solr.add(data, commit=True)

results = solr.search('title:funny')
print("Saw {0} result(s).".format(len(results)))

print(results.docs)

# for result in results:
#     # print("The title is '{0}'.".format(result['title']))
#     print(result)

# results = solr.search('*', **{
#     'hl': 'true',
#     'hl.fragsize': 10,
# })

# print("Saw {0} result(s).".format(len(results)))

# for result in results:
#     # print("The title is '{0}'.".format(result['title']))
#     print(result)

# import urllib3

# http = urllib3.PoolManager()

# connection = http.request('GET', 'http://localhost:8983/solr/test_core/select?q=banana&wt=python')
# print(connection.read())
