import sys
from datetime import datetime
import json
import os
import praw, requests
from PIL import Image
import pytesseract
import numpy as np

if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe' #<-Change this for your system

subreddits = ['dankmemes', 'adviceanimals']

# The credentials below are linked to my (Stewart) reddit account, if you want
# to do any of your own research please generate your own (guide linked to from
# my RedditScrape.ipynb file)
_secret     = 'agAYm70wPBewuKbnCAnAWLiH0Zk'
_clientId   = 'GqTsEKnK6fI-rw'
_user_agent = 'windows:FindYourMeme:0.1'
r = praw.Reddit(client_id=_clientId, client_secret=_secret, user_agent=_user_agent)
image_extensions = ('.jpg', '.png', '.gif')

memeLimit = 50

def update_meme_data(memeData):

    newData = {}
    for subreddit in subreddits:

        subs = r.subreddit(subreddit).new(limit=memeLimit)
        start = datetime.now()
        updated = 0
        for sub in subs:

            if sub.id in memeData:
                break

            if not sub.url.endswith(image_extensions):
                continue

            skip = False
            try:
                image = Image.open(requests.get(sub.url, stream=True).raw)
            except OSError:
                print("Had an image read error")
                skip = True
            if skip:
                continue

            newData[sub.id] = {
                "title": sub.title,
                "url"  : sub.url,
                "plink": sub.permalink,
                "time" : sub.created_utc,
                "sub"  : subreddit,
                "rscore": sub.score,
                "upvote_ratio": sub.upvote_ratio,
                "over_18": sub.over_18
            }

            if sub.author:
                newData[sub.id]["posted_by"] = sub.author.name
            else:
                newData[sub.id]["posted_by"] = '[deleted]'

            im = image.convert('L')
            newData[sub.id]["image_text"] = pytesseract.image_to_string(im).replace('\n', ' ')

            newData[sub.id]['time_of_index'] = str(datetime.now())

            newData[sub.id]['format'] = ''

            updated += 1

        taken = (datetime.now() - start)
        if updated != 0:
            memeData.update(newData)
            print("Processed {} memes from {} in {}".format(updated, subreddit, taken))

    return newData
