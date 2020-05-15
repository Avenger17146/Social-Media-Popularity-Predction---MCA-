from os import listdir
from os.path import isfile, join
import csv

lst = []
b = False
with open('PHOTOURL.csv', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=' ')
    for row in read:
    	# skip first
    	if not b:
    		b = True
    		continue

    	ss = str(row[0]).split(',')
    	ss[0] = int(ss[0])

    	id = ss[2].rfind('/')
    	img_id = ss[2][id+1:]
    	ss[2] = img_id
    	lst.append(ss)

print(len(lst))

print("file read.")
# extract pids from the csv
# pix = [int(i[0]) for i in lst]
lst.sort(key=lambda x : x[0])
# print(lst)


# print(pix)
mypath = './hello/'
pids = [int(f[:-4]) for f in listdir(mypath) if isfile(join(mypath, f))]

some_list = list()
for j in pids:
	some_list.append(lst[j - 1])


b = False
with open('matched_output.csv', 'w', newline='') as myfile:
	for some in some_list:
		if not b:
			b = True
			pel = ['pid', 'uid','url','logviews','year','month','day',	'hour_index',	'commentcount',	'haspeople',	'titlelen'	,'deslen',	'tagcount',	'avgview',	'groupcount',	'avgmembercount']
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			wr.writerow(pel)


		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		wr.writerow(some)

print('file created.')