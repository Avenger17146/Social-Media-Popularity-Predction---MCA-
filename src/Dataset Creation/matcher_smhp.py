from os import listdir
from os.path import isfile, join
import csv
import pandas as pd
from bisect import bisect_left
import sys
import time
import numpy as np
import pickle


def binary_search(a, x, lo=0, hi=None):  # can't use a to specify default for hi
    hi = hi if hi is not None else len(a)  # hi defaults to len(a)   
    pos = bisect_left(a, x, lo, hi)  # find insertion position
    return pos if pos != hi and a[pos] == x else -1 

lst = []
df = pd.read_csv('pre_final.csv', low_memory = False,names =['sno','uid','pid','ispublic','mediastatus','title','mediatype','postdate','latitude','geoaccuracy','longitude','popularity', 'img_id','category','subcategory','concept','pathalias','alltags'])
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
del df['sno']
lst = df.values.tolist()
print(len(lst))
b = False

timer = ['%Y', '%m', '%d' ,'%H']
vecs = [12, 13, 14, 15, 16]

for id, ss in enumerate(lst):
    if not b:
        b = True
        continue

    # encoding
    ss[1] = int(ss[1])
    if (ss[2] == "None"):
        ss[2] = 0
    else:
        ss[2] = 1

    if (ss[3] == 'ready'):
        ss[3] = 1
    else :
        ss[3] = 0

    if (ss[5] == 'photo'):
        ss[5] = 1
    else :
        ss[5] = 0

    t = int(float(ss[6]))

    for tt in timer:
        val = int(time.strftime(tt, time.localtime(t)))
        ss.append(val)

    # vector processing.
    for kk in vecs:
        ele = ss[kk]
        string = ele[1:-1]
        nums = string.split()
        sist = [np.float(x) for x in nums]
        ss.extend(sist)

    del ss[6]


del lst[0]
print(len(lst))

print("file read.")
# extract pids from the csv
unsorted_pix = [int(i[1]) for i in lst]
lst.sort(key=lambda x : x[1])
pix = [int(i[1]) for i in lst]


df1 = df[['img_id','pid']]
img_id_pid = df1.values.tolist()
del img_id_pid[0]
img_id = list()

img_id2pid = dict()
for k in img_id_pid:
    k[0] = int(k[0])
    img_id.append(k[0])
    k[1] = int(k[1])
    img_id2pid[k[0]] = k[1]


# pickle.dump(img_id2pid, open('img2pid.p', 'wb'))
# sys.exit()
pids = []
mypath = './capvec/'
vex = [1, 2]
lister = list()

for f in listdir(mypath):
    print(f)
    df = pd.read_csv(mypath + f)
    del df['sno']

    lst1 = df.values.tolist()
    del lst1[0]
    removal = list()
    for ii, ll in enumerate(lst1):
        try:
            ll[0] = int(ll[0])
        except:
            continue

        idx = binary_search(img_id, ll[0])
        if idx == -1:
            removal.append(ii)
            continue
        pass

    removal.sort(reverse = True)
    for i in removal:  
        del lst1[i] 
    
    dds = list()
    for ss in lst1:
        ssd = list()
        try:
            ss[0] = int(ss[0])
        except:
            continue

        ssd.append(ss[0])
        for kk in vex:
            ele = ss[kk]
            string = ele[1:-1]
            nums = string.split()
            sist = [np.float(x) for x in nums]
            ssd.extend(sist)
        dds.append(ssd)

    lister.extend(dds)

some_list = list()
for ii, j in enumerate(lister):
    idx = binary_search(pix, img_id2pid[j[0]])
    if idx == -1:
        # print(img_id2pid[j[0]])
        sys.exit()
    ist = list()
    ist = lst[idx]
    ss = j
    del ss[0]
    ist.extend(ss)
    # print(len(ist))
    some_list.append(ist)

with open('matched_output.csv', 'w', newline='') as myfile:
	for some in some_list:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		wr.writerow(some)

print(len(some_list[0]))
print('file created.')
