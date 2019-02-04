import json

with open("oldmemes.json", 'r') as f:
    memeData = json.loads(f.read())

newData = {
    meme_id: {
        "title": meme_data['title'],
        "url": meme_data['url'],
        "image_text": meme_data['imText'],
        "time" : meme_data['time'],
        "sub"  : meme_data['sub'],
        "plink": meme_data['plink']
    }
    for meme_id, meme_data in memeData.items()}

with open("memes.json", 'w') as f:
    json.dump(newData, f)
