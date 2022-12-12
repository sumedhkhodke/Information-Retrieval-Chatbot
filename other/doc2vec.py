# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 21:03:10 2022

@author: prane
"""
import json
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

with open ("merged.json","r",encoding="utf-8") as f:
    data=json.load(f)

dl=data['data']

docs={}
for i in range(len(dl)):
    if dl[i]['is_submission']:
        s=dl[i]['title'] if not dl[i]['selftext'] else dl[i]['selftext']
        re.sub(r'\n',' ',s)
        re.sub(r'[\!"#$%&\*+,-./:;<=>?@^_`()|~=]','',s)
        s=re.findall(r'\b\w+\b', s)
        if len(s)>1:
            docs[dl[i]['id']] = s
    else:
        c=dl[i]['body']
        re.sub(r'\n',' ',c)
        re.sub(r'[\!"#$%&\*+,-./:;<=>?@^_`()|~=]','',c)
        c=re.findall(r'\b\w+\b', c)
        if len(c)>1:
            docs[dl[i]['id']] = c

documents=[TaggedDocument(doc, ids) for ids, doc in docs.items()]
model=Doc2Vec(documents, vector_size=100, window=7, min_count=3, workers=4, epochs=100)


