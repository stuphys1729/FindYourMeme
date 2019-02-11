import sys
from datetime import datetime
import json
import os
import praw, requests
from PIL import Image
import pytesseract
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import imutils
import pickle
import cv2
import os

if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe' #<-Change this for your system

# The credentials below are linked to my (Stewart) reddit account, if you want
# to do any of your own research please generate your own (guide linked to from
# my RedditScrape.ipynb file)
_secret     = 'agAYm70wPBewuKbnCAnAWLiH0Zk'
_clientId   = 'GqTsEKnK6fI-rw'
_user_agent = 'windows:FindYourMeme:0.1'
r = praw.Reddit(client_id=_clientId, client_secret=_secret, user_agent=_user_agent)
image_extensions = ('.jpg', '.png', '.gif')

memeLimit = 1000
model = None
mlb = None
modelPath = 'multiAdviceAnimals.h5'
labelPath = 'mlbAA.pickle'

def update_meme_data(subreddit, db_check_fn):

    newData = {}

    subs = r.subreddit(subreddit).hot(limit=memeLimit)
    start = datetime.now()
    updated = 0
    for sub in subs:

        if db_check_fn(sub.id):
            # Only need to update these fields
            newData[sub.id] = {
                "rscore": sub.score,
                "upvote_ratio": sub.upvote_ratio,
                "time_of_index": str(datetime.now())
            }
            continue

        if not sub.url.endswith(image_extensions):
            continue

        skip = False
        try:
            image = Image.open(requests.get(sub.url, stream=True).raw)
        except OSError:
            print("Had an image read error")
            skip = True

        try:
            im = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        except cv2.error:
            print("Had an image convertion error")
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

        greyIm = image.convert('L')
        newData[sub.id]["image_text"] = pytesseract.image_to_string(greyIm).replace('\n', ' ')

        newData[sub.id]['time_of_index'] = str(datetime.now())

        # pre-process the image for classification
        im = cv2.resize(im, (96, 96))
        im = im.astype("float") / 255.0
        im = img_to_array(im)
        im = np.expand_dims(im, axis=0)

        # load the trained convolutional neural network and the multi-label
        # binarizer
        global model
        global mlb
        if model == None:
            print("[INFO] loading network...")
            model = load_model(modelPath)
            mlb = pickle.loads(open(labelPath, "rb").read())

        proba = model.predict(im)[0]
        idx = np.argsort(proba)[::-1][0]
        pred = mlb.classes_[idx]

        if proba[idx] > 0.97:
            newData[sub.id]["format"] = mlb.classes_[idx].replace('-', ' ')
            print("Assigning class {} to meme {} with probability {}".format(pred, sub.url, proba[idx]))
        else:
            newData[sub.id]['format'] = ''

        updated += 1

    taken = (datetime.now() - start)
    if updated != 0:
        print("Processed {} memes from {} in {}".format(updated, subreddit, taken))

    return newData
