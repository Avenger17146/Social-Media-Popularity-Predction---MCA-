import flickrapi
import urllib.request
from PIL import Image
import csv


resize = False
lst = []
b = False
with open('PHOTOURL.txt', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=' ')
    for row in read:
    	t = list()
    	# skip first
    	if not b:
    		b = True
    		continue

    	ss = row[0].split('\t')
    	pid = ss[0]
    	uid = ss[1]
    	img_url = ss[2]

    	id = img_url.rfind('/')
    	img_id = img_url[id+1:]

    	t.append(pid)
    	t.append(uid)
    	t.append(img_id)
    	lst.append(t)
    

print('File read.')
# Flickr api access key 
flickr=flickrapi.FlickrAPI('c6a2c45591d4973ff525042472446ca2', '202ffe6f387ce29b', cache=True)

for ele in lst[:10]:
	pic = flickr.photos_getSizes(photo_id = ele[2])
	sizes_iter = pic.iter('size')

	for size in sizes_iter:
	    #check if its original size
	    if size.attrib['label'] == 'Large Square':
		    u = (size.attrib['source'])

	fname = 'hello/' + str(ele[0]) + '.jpg'
	urllib.request.urlretrieve(u, fname)

	if resize:
		image = Image.open(fname) 
		image = image.resize((256, 256), Image.ANTIALIAS)
		image.save(fname)


print("Images downloaded.")