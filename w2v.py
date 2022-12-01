# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 20:25:26 2022

@author: prane
"""

import gensim.downloader as gd
from gensim.models import Word2Vec
import json
from functools import reduce
import re
import numpy as np

with open ("merged.json","r",encoding="utf-8") as f:
    data=json.load(f)

dl=data['data']

sub_idx=[]
subs=[]
comments=[]
c_idx=[]
for i in range(len(dl)):
    if dl[i]['is_submission']:
        sub_idx.append(i)
        subs.append(dl[i]['title']) if not dl[i]['selftext'] else subs.append(dl[i]['selftext'])
    else:
        c_idx.append(i)
        comments.append(dl[i]['body'])

subs=reduce(lambda a,b:a+b,subs)
comments=reduce(lambda a,b:a+b,comments)

whole_text=subs[0]+comments[0]

lines=whole_text.strip("\n")

sentences = []
for line in lines:
    # remove punctuation
    line = re.sub(r'[\!"#$%&\*+,-./:;<=>?@^_`()|~=]','',line).strip()
    # tokenizer
    tokens = re.findall(r'\b\w+\b', line)
    if len(tokens) > 1:
        sentences.append(tokens)

reddit_vec = Word2Vec(
            sentences,
            min_count=3,   # Ignore words that appear less than this
            vector_size=100,       # Dimensionality of word embeddings
            sg = 1,        # skipgrams
            window=7,      # Context window for words during training
            epochs=100)       # Number of epochs training over corpus

tv = gd.load('glove-twitter-100')

def score(doc,q):
    docv=[]
    for x in doc:
        docv.append((reddit_vec.wv.get_vector(x)/np.linalg.norm(reddit_vec.wv.get_vector(x))).tolist())
    docv=np.array(docv)
    docv=np.mean(docv,axis=0)
    add=0
    for x in q:
        add+=(np.dot(np.transpose(reddit_vec.wv.get_vector(x)),docv)/(np.linalg.norm(reddit_vec.wv.get_vector(x))*np.linalg.norm(docv)))
    add=add/len(q)
    return add

def score_pretrained(doc,q):
    docv=[]
    for x in doc:
        x=x.lower()
        docv.append((tv.get_vector(x)/np.linalg.norm(tv.get_vector(x))).tolist())
    docv=np.array(docv)
    docv=np.mean(docv,axis=0)
    add=0
    for x in q:
        add+=(np.dot(np.transpose(tv.get_vector(x)),docv)/(np.linalg.norm(tv.get_vector(x))*np.linalg.norm(docv)))
    add=add/len(q)
    return add