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
import functools
from nltk.tokenize import word_tokenize

# download once only if its not already 
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from string import punctuation
import gensim.downloader as gd
# from sklearn.linear_model import LogisticRegression
from scipy.special import expit
import pickle

stopwords=stopwords.words('english')
punctuation=list(punctuation)
punctuation.append("’")

print('loading glove embeddings')
tv = gd.load('glove-twitter-100')
print('loaded glove-twitter-100 embeddings!')


# weights = np.load('params.npy')
with open('params.pickle', 'rb') as f:
    model = pickle.load(f)

with open('idf_data.pickle', 'rb') as f:
    idf = pickle.load(f)

corpus_size = len(idf.keys())

# def classifyQuery(q):
#     qe=[]
#     y=word_tokenize(q)
#     t=[z for z in y if z not in stopwords and z not in punctuation]
#     for x in t:
#         try:
#             qv=tv.get_vector(x)
#             qv=qv/np.linalg.norm(qv)
#             qe.append(qv)
#         except:
#             pass
#     # print(qe)
#     if qe:
#         X = np.mean(qe,axis=0).reshape((1,100))

#         classifier_pred = expit(np.sum(weights * X))
        
#         return classifier_pred

#     return "UNKNOWN"

# DEBUG = False
def rare_terms(q_text):
    boost_terms=[]
    rt={}
    toks=word_tokenize(q_text)
    toks = [x for x in toks if x not in stopwords and x not in punctuation]
    for x in toks:
        try:
            rt[x]=corpus_size/idf[x]
        except:
            pass
    rt=dict(sorted(rt.items(), key=lambda item: item[1]))
    rt=list(rt.keys())[-2:]
    for x in rt:
        boost_terms.append([a for a,b in tv.most_similar(x, topn=3)])
    boost_terms=functools.reduce(lambda a,b: a+b, boost_terms)
    return boost_terms

def classifyQuery(q):
    qe=[]
    d=re.sub(r'\n',' ',q.lower())
    d=re.sub(r'[^a-zA-Z0-9\s-]','',d)
    y=word_tokenize(d)
    # if DEBUG:
    #     print('Tokens:', y)
    for x in y:
        try:
            qv=tv.get_vector(x)*corpus_size/idf[x]
            qv=tv.get_vector(x)*corpus_size/idf[x]
            qv=qv/np.linalg.norm(qv)
            qe.append(qv)
        except:
            pass
    if qe:
        X = np.mean(qe,axis=0).reshape((1,100))
        class_pred = float(model.predict_proba(X)[0][1])
        # print(class_pred)
        return class_pred

    return "UNKNOWN"
    