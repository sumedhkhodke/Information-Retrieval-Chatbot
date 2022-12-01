# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 10:32:04 2022

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

core_name="IRF22P1"
ip="34.162.187.148"

url=f"http://{ip}:8983/solr/{core_name}/query?q=is_submission:true&rows=2500"

r = requests.get(url)
stopwords=stopwords.words('english')
punctuation=list(punctuation)
punctuation.append("’")

tv = gd.load('glove-twitter-100')

cdocs=[]
labels=[]
for x in r.json()['response']['docs']:
    tokenvecs=[]
    if x['selftext']:
        y = re.sub(r'\n',' ',x['selftext'].lower())
    else:
        y = re.sub(r'\n',' ',x['title'].lower())
    y=word_tokenize(y)
    tokens=[token for token in y if token not in stopwords and token not in punctuation]
    for z in tokens:
        try:
            v=tv.get_vector(z)
            v=v/np.linalg.norm(v)
            tokenvecs.append(v)
        except:
            pass
        
    if len(tokens)>1:
        labels.append(0)
        cdocs.append(np.mean(tokenvecs,axis=0))

'''
core_name="Final"
url=f"http://{ip}:8983/solr/{core_name}/query?q=prompt:*&rows=250000"

r = requests.get(url)
prompts=[]
for x in r.json()['response']['docs']:
    prompts.append(x['prompt'])
ps=list(set(prompts))
for x in ps[:2368]:
    tokenvecs=[]
    y = re.sub(r'\n',' ',x.lower())
    y=word_tokenize(y)
    tokens=[token for token in y if token not in stopwords and token not in punctuation]
    for z in tokens:
        try:
            v=tv.get_vector(z)
            v=v/np.linalg.norm(v)
            tokenvecs.append(v)
        except:
            pass
        
    if len(tokens)>1:
        labels.append(1)
        cdocs.append(np.mean(tokenvecs,axis=0))
'''  
ip='34.125.24.152'
core_name="CC"
url=f"http://{ip}:8983/solr/{core_name}/query?q=question:*&rows=25000"

r = requests.get(url)
prompts=[]
for x in r.json()['response']['docs']:
    prompts.append(x['question'])
ps=list(set(prompts))
count=0
for x in ps:
    tokenvecs=[]
    y = re.sub(r'\n',' ',x.lower())
    y=word_tokenize(y)
    tokens=[token for token in y if token not in stopwords and token not in punctuation]
    for z in tokens:
        try:
            v=tv.get_vector(z)
            v=v/np.linalg.norm(v)
            tokenvecs.append(v)
        except:
            pass
        
    if len(tokens)>1:
        count+=1
        labels.append(1)
        cdocs.append(np.mean(tokenvecs,axis=0))
        if count == 2368:
            break
#cdocuments=[TaggedDocument(doc, ids) for ids, doc in cdocs.items()]
#model=Doc2Vec(cdocuments, vector_size=100, window=7, min_count=3, workers=4, epochs=100)

X=cdocs[:2000]+cdocs[2368:4368]
y=labels[:2000]+labels[2368:4368]
lr=LogisticRegression(random_state=0)
lr.fit(X,y)


def classifyQuery(q):
    qe=[]
    y=word_tokenize(q)
    t=[z for z in y if z not in stopwords and z not in punctuation]
    for x in t:
        try:
            qv=tv.get_vector(x)
            qv=qv/np.linalg.norm(qv)
            qe.append(qv)
        except:
            pass
    lr.predict(np.mean(qe,axis=0).reshape((1,100)))