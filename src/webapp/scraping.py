import sys
from datetime import datetime
import json
import os
import praw, requests
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe' #<-Change this for your system
import numpy as np

subreddit = 'dankmemes'

# The credentials below are linked to my (Stewart) reddit account, if you want
# to do any of your own research please generate your own (guide linked to from
# my RedditScrape.ipynb file)
_secret     = 'agAYm70wPBewuKbnCAnAWLiH0Zk'
_clientId   = 'GqTsEKnK6fI-rw'
_user_agent = 'windows:FindYourMeme:0.1'
r = praw.Reddit(client_id=_clientId, client_secret=_secret, user_agent=_user_agent)
image_extensions = ('.jpg', '.png', '.gif')

memeLimit = 100

def update_meme_data(memeData):

    subs = r.subreddit(subreddit).new(limit=memeLimit)

    start = datetime.now()
    updated = 0
    newData = {}
    for sub in subs:

        if sub.id in memeData:
            break

        if not sub.url.endswith(image_extensions):
            continue

        newData[sub.id] = {
            "title": sub.title,
            "url"  : sub.url,
            "plink": sub.permalink,
            "time" : sub.created_utc,
            "sub"  : subreddit
        }

        im = Image.open(requests.get(sub.url, stream=True).raw)
        newData[sub.id]["imText"] = pytesseract.image_to_string(im).replace('\n', ' ')

        updated += 1

    taken = (datetime.now() - start)
    if updated != 0:
        memeData.update(newData)
        print("Processed {} memes in {}".format(updated, taken))

        data = json.dumps(memeData)
        with open("memes.dat", 'w') as f:
            f.write(data)

    return newData
