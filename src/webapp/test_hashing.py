import hashlib
from os.path import expanduser
from PIL import Image
import requests
from io import BytesIO
import index

m = hashlib.md5()
img = open(expanduser('~')+'/Pictures/deleted-imgur.png', 'rb').read()
m.update(img)
print(m.hexdigest())

new_img = Image.open(BytesIO(requests.get('https://i.redd.it/epi43xbrie521.jpg').content)).tobytes()
m.update(new_img)
print(m.hexdigest())

print(m.hexdigest() == index.delete_hash)

print(index.is_deleted('https://i.redd.it/epi43xbrie521.jpg'))
