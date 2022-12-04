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
from configs import RETR_PATH
from sentence_transformers import SentenceTransformer, util
import spacy
import en_core_web_lg

stopwords=stopwords.words('english')
punctuation=list(punctuation)
punctuation.append("’")

print('loading glove embeddings')
tv = gd.load('glove-twitter-100')
print('loaded glove-twitter-100 embeddings!')

st = SentenceTransformer('all-mpnet-base-v2')

nlp=spacy.load("en_core_web_lg")

# weights = np.load('params.npy')

with open(RETR_PATH+'params_lem.pickle', 'rb') as f:
    model = pickle.load(f)

with open(RETR_PATH+'idf_data.pickle', 'rb') as f:
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
'''
def DESM(q, d):
    qt=word_tokenize(q)
    dt=word_tokenize(d)
    qt=[x for x in qt if x not in punctuation]
    dt=[x for x in dt if x not in punctuation]
    dv=np.zeros(100)
    score=0
    for x in dt:
        try:
            dv+=(tv.get_vector(x)/np.linalg.norm(tv.get_vector(x)))
        except:
            pass
    try:
        dv=dv/len(dt)
    except:
        pass
    for x in qt:
        try:
            score+=np.sum((tv.get_vector(x)/np.linalg.norm(tv.get_vector(x)))*dv)
        except:
            pass
    try:
        score=score/len(qt)
    except:
        pass        
    return score
'''
def entities(q):
    entities={}
    nes=nlp(q)
    for x in nes.ents:
        entities[x.text]=x.label_
    return entities

def continuity(q1,q2):
    qv=st.encode(q1)
    dv=st.encode(q2)
    score=util.cos_sim(qv,dv)     
    return abs(float(score[0][0])) >= 0.5

def DESM(q, d):
    qt=word_tokenize(q)
    dt=word_tokenize(d)
    qt=[x for x in qt if x not in stopwords and x not in punctuation]
    dt=[x for x in dt if x not in stopwords and x not in punctuation]
    qt=functools.reduce(lambda a,b: a+' '+b,qt)
    dt=functools.reduce(lambda a,b: a+' '+b,dt)
    qv=st.encode(qt)
    dv=st.encode(dt)
    score=util.cos_sim(qv,dv)     
    return float(score[0][0])

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
    