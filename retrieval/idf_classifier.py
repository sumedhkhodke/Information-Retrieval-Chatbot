# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 23:27:21 2022

@author: prane
"""

import numpy as np
import re
import requests
import json
import nltk
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from string import punctuation
#from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim.downloader as gd
from sklearn.linear_model import LogisticRegression
import pickle

punctuation=list(punctuation)
punctuation.append("’")

tops=[]

with open ("praneeth_dataset.json","r",encoding="utf-8") as f:
    data=json.load(f)
psubs=[]

for i in range(len(data['data'])):
    if data['data'][i]['is_submission']:
        if data['data'][i]['selftext']:
            d=re.sub(r'\n',' ',data['data'][i]['selftext'].lower())
            psubs.append(re.sub(r'[^a-zA-Z0-9\s-]','',d))
        else:
            d=re.sub(r'\n',' ',data['data'][i]['title'].lower())
            psubs.append(re.sub(r'[^a-zA-Z0-9\s-]','',d))

with open ("jay_dataset.json","r",encoding="utf-8") as f:
    data=json.load(f)
jsubs=[]
for i in range(len(data)):
    if data[i]['is_submission']:
        print(i)
        if 'selftext' in data[i].keys() and data[i]['selftext'] and data[i]['selftext'] != 'removed' and data[i]['selftext'] != 'deleted':
            d=re.sub(r'\n',' ',data[i]['selftext'].lower())
            jsubs.append(re.sub(r'[^a-zA-Z0-9\s-]','',d))
        elif 'title' in data[i].keys() and data[i]['title'] and data[i]['title'] != 'removed' and data[i]['title'] != 'deleted':
            d=re.sub(r'\n',' ',data[i]['title'].lower())
            jsubs.append(re.sub(r'[^a-zA-Z0-9\s-]','',d))

with open ("sumedh_dataset.json","r",encoding="utf-8") as f:
    data=json.load(f)
ssubs=[]
for i in range(len(data)):
    if data[i]['is_submission']:
        print(i)
        if 'selftext' in data[i].keys() and data[i]['selftext'] and data[i]['selftext'] != 'removed' and data[i]['selftext'] != 'deleted':
            d=re.sub(r'\n',' ',data[i]['selftext'].lower())
            ssubs.append(re.sub(r'[^a-zA-Z0-9\s-]','',d))
        elif 'title' in data[i].keys() and data[i]['title'] and data[i]['title'] != 'removed' and data[i]['title'] != 'deleted':
            d=re.sub(r'\n',' ',data[i]['title'].lower())
            ssubs.append(re.sub(r'[^a-zA-Z0-9\s-]','',d))
        
subs=psubs+jsubs+ssubs

with open ("refined_cc_personality.json","r",encoding="utf-8") as f:
    data=json.load(f)
prompts=[]
for i in range(len(data['data'])):
    d=re.sub(r'\n',' ',data['data'][i]['question'].lower())
    d=re.sub(r'[^a-zA-Z0-9\s-]','',d)
    prompts.append(d)


subtok=[]
for x in subs:
    subtok.append(word_tokenize(x))
promtok=[]
for x in prompts:
    promtok.append(word_tokenize(x))

toks=subtok+promtok

idf={}
for x in toks:
    for y in set(x):
        if y not in idf:
            idf[y]=1
        else:
            idf[y]+=1

with open('idf_data.pickle', 'wb') as f:
    pickle.dump(idf, f)

# tv = gd.load('glove-twitter-100')
# cdocs=[]
# labels=[]
# corpus_size=len(idf.keys())

# for x in subtok:
#     tokens=[]
#     for z in x:
#         try:
#             v=tv.get_vector(z)
#             v=v*corpus_size/idf[z]
#             v=v/np.linalg.norm(v)
#             tokens.append(v)
#         except:
#             pass
#     if len(tokens) > 0:
#         cdocs.append(list(np.mean(tokens,axis=0)))
#         labels.append(0)

# for x in promtok:
#     tokens=[]
#     for z in x:
#         try:
#             v=tv.get_vector(z)
#             v=v*corpus_size/idf[z]
#             v=v/np.linalg.norm(v)
#             tokens.append(v)
#         except:
#             pass
#     if len(tokens) > 0:
#         cdocs.append(list(np.mean(tokens,axis=0)))
#         labels.append(1)
    
# X=cdocs[:9000]+cdocs[-9000:]
# y=labels[:9000]+labels[-9000:]
# lr=LogisticRegression(random_state=0)
# lr.fit(X,y)


# def classifyQuery(q):
#     qe=[]
#     d=re.sub(r'\n',' ',q.lower())
#     d=re.sub(r'[^a-zA-Z0-9\s-]','',d)
#     y=word_tokenize(d)
#     for x in y:
#         try:
#             qv=tv.get_vector(x)*corpus_size/idf[x]
#             qv=tv.get_vector(x)*corpus_size/idf[x]
#             qv=qv/np.linalg.norm(qv)
#             qe.append(qv)
#         except:
#             pass
#     print(lr.predict(np.mean(qe,axis=0).reshape((1,100))))