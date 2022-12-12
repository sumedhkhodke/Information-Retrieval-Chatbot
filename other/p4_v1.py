# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 00:03:30 2022

@author: prane
"""

import requests
import json

core_name="Final"
ip="34.125.24.152"

url=f"http://{ip}:8983/solr/{core_name}/query?"

inp = input("enter query:\n")

r=requests.get(url+"fl=speaker2,score&indent=true&q.op=OR&q=speaker1:"+inp+"&rq={!rerank reRankQuery=$rqq reRankDocs=100 reRankWeight=5}&rqq=(speaker2:"+inp+")&rows=100")
#r=requests.get(url+"fl=id,parent_body,body,score&indent=true&q.op=OR&q=parent_body:"+inp+"&rows=10")

ids=[]
try:
    for x in r.json()['response']['docs']:
        print(x['body'])
        print(x['score'])
        ids.append(x['id'])
except:
    print("no records found")
