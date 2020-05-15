import flickrapi
import urllib.request
from PIL import Image
import csv
import sys

print('hello')
l = sys.argv
# print(l)
n = int(l[1])
resize = False
lst = []
b = False
with open('t2_train_link.txt', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=' ')
    for row in read:
    	ss= row[0]
    	id_ = ss.rfind('/')
    	img_id = ss[id_+1:]
    	lst.append(img_id)
    
# print(lst)
print('File read.')
# Flickr api access key 
flickr=flickrapi.FlickrAPI('c6a2c45591d4973ff525042472446ca2', '202ffe6f387ce29b', cache=True)
i  = 0
j = 950
dk = 305613
for ele in lst[int(dk*n/50) + 950:int(dk*(n+1)/50)]:
# for ele in lst:
	j+=1
	try :
		pic = flickr.photos_getSizes(photo_id = ele)
	except:
		print('not found image')
		i+=1
		continue
	sizes_iter = pic.iter('size')

	for size in sizes_iter:
	    #check if its original size
	    if size.attrib['label'] == 'Large Square':
		    u = (size.attrib['source'])

	fname = 'hello/' + str(ele) + '.jpg'
	try :
		urllib.request.urlretrieve(u, fname)
	except:
		i+=1
		print('not found size')
		continue

	if resize:
		image = Image.open(fname) 
		image = image.resize((256, 256), Image.ANTIALIAS)
		image.save(fname)
	print(j)

print("Images downloaded.")
print(i)