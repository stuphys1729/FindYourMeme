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
# Connect to reddit and download the subreddit front page
_secret     = 'agAYm70wPBewuKbnCAnAWLiH0Zk'# You will need to get your own credentials to put here
_clientId   = 'GqTsEKnK6fI-rw'# and here, see link above.
_user_agent = 'windows:FindYourMeme:0.1'
r = praw.Reddit(client_id=_clientId, client_secret=_secret, user_agent=_user_agent)
image_extensions = ('.jpg', '.png', '.gif')

memeLimit = 100

def update_meme_data(memeData):

    subs = r.subreddit(subreddit).new(limit=memeLimit)

    start = datetime.now()
    updated = 0
    for sub in subs:

        if sub.id in memeInfo:
            break

        if not sub.url.endswith(image_extensions):
            continue

        memeData[sub.id] = {
            "title": sub.title,
            "url"  : sub.url,
            "plink": sub.permalink,
            "time" : sub.created_utc
        }

        im = Image.open(requests.get(sub.url, stream=True).raw)
        memeInfo[sub.id]["imText"] = pytesseract.image_to_string(im).replace('\n', ' ')

        updated += 1

    taken = (datetime.now() - start)
    if updated != 0:
        print("Processed {} memes in {}".format(updated, taken))

        data = json.dumps(memeData)
        with open("memes.dat", 'w') as f:
            f.write(data)
