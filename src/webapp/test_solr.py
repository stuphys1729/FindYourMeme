import pysolr

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
solr.add([
    {
        "id": "1",
        "title": "Haha a funny meme",
        "url": "https://i.redd.it/eg49qet98e521.jpg",
        "image_text": "evolution dude fuck off"
    }
],  commit=True)

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
