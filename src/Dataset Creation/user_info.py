import flickrapi
import csv
import sys
import pandas as pd
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

# format ["ispro", "pro_badge", "description", "firstdatetaken"(6cols), "photoscount"]


print('hello')
l = sys.argv
print(l)
n = int(l[1])
resize = False
lst = []
b = False
with open('t2_train_link.txt', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=' ')
    for row in read:
    	ss= row[0]
    	uid = ss.split('/')[-2]
    	pid = int(ss.split('/')[-1])
    	lst.append((uid, pid))
    
# print(lst)
print('File read.')
# Flickr api access key 
flickr=flickrapi.FlickrAPI('c6a2c45591d4973ff525042472446ca2', '202ffe6f387ce29b', cache=True)
i  = 0
j = 950
dk = 305613
cnt = 1

result = list()
for el in lst[int(dk*n/50):int(dk*(n+1)/50)]:
# for el in lst:
	j+=1
	print(cnt)
	cnt += 1
	ele = el[0]
	pid = el[1]
	try :
		# pic = flickr.photos_getSizes(photo_id = ele)
		xml = flickr.people.getInfo(user_id = ele)
	except:
		print('not found info')
		i+=1
		continue

	ss = list()
	ss.append(pid)

	if xml is None:
		continue

	for elem in xml.iter():
		if (elem.tag == 'firstdatetaken'):
			dt = elem.text
			if dt is not None:
				ss.append(int(dt[0:4]))
				ss.append(int(dt[5:7]))
				ss.append(int(dt[8:10]))
				ss.append(int(dt[11:13]))
				ss.append(int(dt[14:16]))
				ss.append(int(dt[17:19]))
			else:
				for i in range(6):
					ss.append(0)
		elif (elem.tag == 'count'):
			if elem.text is not None:
				ss.append(int(elem.text))
			else:
				ss.append(0)
		elif (elem.tag == 'description'):
			if elem.text is not None:
				ss.append(elem.text)
			else:
				ss.append("")
		elif (elem.tag == 'person'):
			vals = elem.attrib
			if vals is not None:
				if vals['ispro'] is not None:
					ss.append(int(vals['ispro']))
				else :
					ss.append(0)

				if 'pro_badge' in vals:
					ss.append(vals['pro_badge'])
				else:
					ss.append(0)
			else:
				ss.append(0)
				ss.append(0)
	# print(ss)
	result.append(ss)
	# break

# , columns = ["pid", "ispro", "pro_badge", "description", "fd_1", "fd_2", "fd_3", "fd_4", "fd_5", "fd_6", "photoscount"]
df = pd.DataFrame(result)
df.to_csv("./info/" + str(n) + ".csv")
print("finished")
