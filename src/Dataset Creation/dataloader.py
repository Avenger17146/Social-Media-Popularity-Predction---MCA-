import pandas as pd 
from nltk.tokenize import sent_tokenize, word_tokenize 
import warnings 
warnings.filterwarnings(action = 'ignore') 
import gensim 
from gensim.models import Word2Vec 
import numpy as np 


df = pd.read_csv('t2_train_data.csv', sep=' ', encoding ='latin1', names =[ "uid", "pid", "category", "subcategory", "concept", "pathalias", "ispublic", "mediastatus", "title", "mediatype", "alltags", "postdate", "latitude", "geoaccuracy", "longitude"])  
y = pd.read_csv('t2_train_label.csv', sep=' ', encoding ='latin1', names=['popularity'])
df['popularity'] = y['popularity']

df_url = pd.read_csv('t2_train_link.csv', encoding ='latin1', header = None)
list_url = [k[0] for k in df_url.values.tolist()]

img_id = list()
for ii, ss in enumerate(list_url):
    id_ = int(ss.split('/')[-1])
    img_id.append(id_)

# print(img_id)
df['img_id'] = img_id

df = df.dropna()
# print(df)

def w2v(f) :
    model = Word2Vec(f, size=20, window=5, min_count=1)
    return model

print('cat start')
col=[]
x = pd.unique(df['category'])
for i in x :
    col.append([i])
ans = w2v(col)
col=[]
for i in df['category']:
    col.append(ans[i])
df = df.drop('category',axis=1)
df['category'] = col
print('cat end')

print('subcat start')
col=[]
x = pd.unique(df['subcategory'])
for i in x :
    col.append([i])
ans = w2v(col)
col=[]
for i in df['subcategory']:
    col.append(ans[i])
df = df.drop('subcategory',axis=1)
df['subcategory'] = col

print('conc start')
col=[]
x = pd.unique(df['concept'])
for i in x :
    col.append([i])
ans = w2v(col)
col=[]
for i in df['concept']:
    col.append(ans[i])
df = df.drop('concept',axis=1)
df['concept'] = col

print('path start')
col=[]
x = pd.unique(df['pathalias'])
for i in x :
    col.append([i])
ans = w2v(col)
col=[]
for i in df['pathalias']:
    col.append(ans[i])
df = df.drop('pathalias',axis=1)
df['pathalias'] = col

print('all start')
col=[]
f =[]
x = df['alltags']
for i in x :
    for j in i.split(' '):
        col.append(j)
coll = set(col)
for i in coll :
    f.append([i])
# print(f)
ans = w2v(f)
coll=[]
for nug in x:
    ris  = np.zeros(20)
    count  = 0
    for goo in nug.split(' ') : 
        # print(goo)
        count+=1
        lol = ans[goo]
        ris+= np.array(lol)
    ris/= count
    coll.append(ris)
df = df.drop('alltags',axis=1)
df['alltags'] = coll


df.to_csv('pre_final.csv')
