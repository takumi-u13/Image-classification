from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os
import time
import sys

#API infomation
api_key = ''
secret_key = ''

wait_time = 1

#create new folder
object_name = sys.argv[1]
if not os.path.exists(object_name):
	os.mkdir(object_name) 

save_dir = './' + object_name

flickr = FlickrAPI(api_key, secret_key, format='parsed-json')
result = flickr.photos.search(
	text=object_name,
	per_page=400,
	media='photos',
	sort='relevance',
	safe_search=1,
	extras='url_q, licence'
    )

photos = result['photos']
pprint(photos)


for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    file_path = save_dir + '/' + photo['id'] + '.jpg'
    if os.path.exists(file_path):
        continue
    urlretrieve(url_q, file_path)
    time.sleep(wait_time)
