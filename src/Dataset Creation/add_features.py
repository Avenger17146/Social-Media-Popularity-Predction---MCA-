import pandas as pd
import numpy as np
import sys
from bisect import bisect_left
import pickle
import csv


def binary_search(a, x, lo=0, hi=None):  # can't use a to specify default for hi
    hi = hi if hi is not None else len(a)  # hi defaults to len(a)   
    pos = bisect_left(a, x, lo, hi)  # find insertion position
    return pos if pos != hi and a[pos] == x else -1 

op_path = './full-data/matched_output.csv'
fe_path = './user_pre_final.csv'
p_path = './full-data/img2pid.p'

img2pid = pickle.load(open(p_path, 'rb'))

df1 = pd.read_csv(fe_path, header = None)
df2 = pd.read_csv(op_path, header = None)

list_features = df1.values.tolist()
list_op = df2.values.tolist()

# remove headers
del list_features[0]
del list_op[0]

# print(set([i[3] for i in list_features]))
# sys.exit()

lenlen = []
list_features2 = list()
# pre process
for ll in list_features:
    xx = int(ll[1])
    if xx not in img2pid:
    	continue

    ele = ll[11]
    string = ele[1:-1]
    nums = string.split()
    sist = [np.float(x) for x in nums]
    del ll[11]
    del ll[0]

    pc = list()

    for i, k in enumerate(ll):
    	if i == 2:
    		if (k == '0'):
    			pc.append(0)
    		elif (k == 'legacy'):
    			pc.append(1)
    		else:
    			pc.append(2)
    	elif i == 0:
    		pc.append(img2pid[xx])
    	else :
    		if isinstance(k, str):
    			pc.append(int(ll[i]))

    if (len(pc) == 2):
    	pc = []
    	for i, k in enumerate(ll):
    		if i == 2:
    			if (k == '0'):
    				pc.append(0)
    			elif (k == 'legacy'):
    				pc.append(1)
    			else:
    				pc.append(2)
    		elif i == 0:
    			pc.append(img2pid[xx])
    		else :
    			pc.append(int(ll[i]))

    pc.extend(sist)
    list_features2.append(pc)


list_op.sort(key=lambda x : x[1])

finder_list = [x[0] for x in list_features2]
total_list = [int(x[1]) for x in list_op]

# print(finder_list[:20])
# print(total_list[-20:])
# sys.exit()

final_list = list()
for i, f in enumerate(finder_list):
	idx = binary_search(total_list, f)

	if (idx == -1):
		continue

	features = list()
	features.extend(list_op[idx])
	features.extend(list_features2[i][1:])

	final_list.append(features)

# df = pd.DataFrame(final_list)
# df.to_csv('user_features_op.csv')

with open('user_features_opdes.csv', 'w', newline='') as myfile:
	for some in final_list:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		wr.writerow(some)

print('file created.')

# nums = []
cnt = 0
for kk in final_list:
	if len(kk) == 299:
		cnt = cnt + 1

print(cnt)

print(len(final_list))
print(len(final_list[0]))