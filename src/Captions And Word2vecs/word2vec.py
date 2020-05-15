# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from nltk.tokenize import sent_tokenize, word_tokenize 
import warnings 
  
warnings.filterwarnings(action = 'ignore') 
  
import gensim 
from gensim.models import Word2Vec 
import pandas as pd


def do() : 
    file=pd.read_csv("vocabulary.csv")

    vocab=file.iloc[3:,3:4]

    s=vocab.to_string(index = False)

    f=s.replace(" ", "")
    f=f.replace("\n", " ")
    # print(f)
    #GFG KA CODE HAI YE
    data = [] 
    for i in sent_tokenize(f): 
        temp = [] 
        
        for j in word_tokenize(i): 
            temp.append(j.lower()) 
    
        data.append(temp)
        
    model = Word2Vec(data, size=100, window=5, min_count=1)
    return model

x  = do()
# y=model['on']
# x=model.similarity('on', 'in')