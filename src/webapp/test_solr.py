import pysolr
import json

solr = pysolr.Solr("http://localhost:8983/solr/meme_data", timeout=10)

with open("memes.json", 'r') as f:
    memeData = json.loads(f.read())

# for key, meme in memeData.items():
#     solr.add([

#     ])
t_id = 'amem1w'
# print(memeData[t_id])

# solr.add([
#     {
#         "id": t_id
#         , "title": memeData[t_id]['title']
#         , "url": memeData[t_id]['url']
#         , "plink": memeData[t_id]['plink']
#         , "time": memeData[t_id]['time']
#         , "sub": memeData[t_id]['sub']
#         , "image_text": memeData[t_id]['imText']
#     }
# ], commit=True)

# for key in memeData:
#     t_id = key
#     print(memeData[t_id]['imText'])
#     solr.add([
#         {
#             "id": t_id
#             , "title": memeData[t_id]['title']
#             , "url": memeData[t_id]['url']
#             , "plink": memeData[t_id]['plink']
#             , "time": memeData[t_id]['time']
#             , "sub": memeData[t_id]['sub']
#             , "image_text": ' ' + memeData[t_id]['imText']
#         }
#     ], commit=True)

# print(len(solr.search('*').docs))

results = solr.search('*', **{
    'rows': '100'
}).docs

print(results)
