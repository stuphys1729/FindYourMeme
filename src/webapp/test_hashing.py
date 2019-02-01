import hashlib
from os.path import expanduser
from PIL import Image
import requests
from io import BytesIO
import index

no_imgur = 'https://i.imgur.com/Z3Do8Dx.png'
no_reddit = 'https://i.redd.it/epi43xbrie521.jpg'

m = hashlib.md5()
img = open(expanduser('~')+'/Pictures/deleted-imgur.png', 'rb').read()
m.update(img)
print(m.hexdigest())

new_img = Image.open(BytesIO(requests.get('https://i.redd.it/epi43xbrie521.jpg').content)).tobytes()
m.update(new_img)
print(m.hexdigest())

print(m.hexdigest() == index.delete_hash)

print(index.is_deleted('https://i.redd.it/epi43xbrie521.jpg'))
print(index.is_deleted('https://i.imgur.com/Z3Do8Dx.png'))

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

print(md5(expanduser('~')+'/Pictures/deleted-imgur.png'))

import time

t0 = time.time()

img1 = Image.open(expanduser('~')+'/Pictures/deleted-imgur.png')
img2 = Image.open(BytesIO(requests.get('https://i.redd.it/epi43xbrie521.jpg').content))

print(list(img1.getdata()) == list(img2.getdata()))
print(img1 == img2)

print(time.time() - t0)

img1 = Image.open(expanduser('~')+'/Pictures/deleted-imgur2.png')
img2 = Image.open(BytesIO(requests.get(no_imgur).content))

print(list(img1.getdata()) == list(img2.getdata()))
print(img1 == img2)
