# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 21:21:29 2022

@author: prane
"""

import json
import pickle
import requests
import re
from configs import HOST, PORT
import numpy as np
import functools
# from Database import Database

from classifier_infer import classifyQuery, rare_terms, DESM, entities, continuity

ENTS=['EVENT','FAC','LANGUAGE','GPE','LANGUAGE','LAW','LOC', 'NORP', 'ORG', 'PERSON', 'PRODUCT', 'WORK_OF_ART']

DEFAULT_RESPONSES = {
    'professional': "Sorry, I didn't get that",
    'witty': "Oh, that's too much for my pea sized brain to process",
    'caring': "Sorry, what do you mean?",
    'friendly': "Sorry, what do you mean?",
    'enthusiastic': "Sorry, I couldn't understand that, would you mind asking something else or elaborating?",
}

qa={}
qa['what'] = ['you heard right','please expand your query','yeah!','pay attention','slow on the uptake?']
qa['how'] = ['pure chance','there\'s always a way','just like I said','I don\'t know','wish I knew how']
qa['where'] = ['somewhere over the rainbow','right there', 'neither here nor there','in a galaxy far away']
qa['why'] = ['I find myself in the dark','it\'s obvious, isn\'t it?','damned if I knew']
qa['when'] = ['just then','a long long time ago','time is a consrtuct']

# DB = Database()
class Chatbot():
    def __init__(self,context=[],personality='enthusiatic'):
        self.personality=personality
        self.context=context
        self.topk=50
        self.topic=''
        self.prevq=''
        self.rt=[]
        self.entities=[]
        # self.db = Database()
    
    def update_feedback(self,q_id,feedback):
        # DB.update_feedback_by_id(q_id,feedback)
        pass
    
    def parse_response(self, resp):
        results = []
        num_docs_found = 0
        try:
            num_docs_found = resp.json()['response']['numFound']
            for x in resp.json()['response']['docs']:
                results.append(x)
        except Exception as e:
            print(e)
            pass
        
        return {'total_retrieved': num_docs_found, 'docs':results}
    
    def update_context(self,q_text):
        bt=[]
        self.ents=entities(q_text)
        for k,v in self.ents.items():
            if v in ENTS:
                bt.append(k)
        self.context=bt
        
    def update_scores(self,q_text, resp):
        desm=[]
        for doc in resp:
            desm.append(DESM(q_text, doc['body']))
        bm25=np.array([x['score'] for x in resp])
        # print(bm25)
        bm25=(bm25-np.min(bm25))/(np.max(bm25)-np.min(bm25))

        # print(bm25)
        # print(desm)

        scores=list(0.3*(np.array(desm)+0.7*bm25))
        for i in range(len(resp)):
            resp[i]['score']=scores[i]
            resp[i]['desm_score'] = desm[i]
            resp[i]['bm25_score'] = bm25[i]
        resp=list(sorted(resp, key=lambda x:x['score']))
        # resp['desm_score'] = desm
        # resp['bm25_score'] = bm25
        return resp
    
    def formulate_query(self, core_name, q_text, reddit_topic_filter, bot_personality):
        solr_url = f"http://{HOST}:{PORT}/solr/{core_name}/query?defType=edismax&"
        if 'cc' == core_name.strip().lower():
            bot_personality = bot_personality.strip().lower()
            req_url = solr_url+"fl=id,question,"+bot_personality+",score&indent=true&q.op=OR&q=question:("+q_text+")&rows=1"
        else:
            self.rt=rare_terms(q_text)
            rt=functools.reduce(lambda a,b: a+' '+b, self.rt)
            ents=entities(q_text)
            bt=[]
            for k,v in ents.items():
                if v in ENTS:
                    bt.append(k)
            if self.topic == reddit_topic_filter:
                bt=bt+self.context
            elif continuity(self.prevq,q_text):
                bt=bt+self.context
            if reddit_topic_filter:
                # what are the valid topics we have in the data??
                # Politics, Environment, Education, Techonology, Healthcare
                reddit_topic_filter = reddit_topic_filter.strip().title()
                req_url = solr_url+"fl=id,parent_body,body,score&indent=true&q.op=OR&q=("+q_text+")&qf=parent_body&fq=topic:"+reddit_topic_filter+"&bq=parent_body:("+rt+")*3&rq={!rerank reRankQuery=$rqq reRankDocs="+str(self.topk)+" reRankWeight=5}&rqq={!func}sum("
                for x in bt:
                    req_url+="query({!edismax qf=body v='"+x+"'}),"
                #req_url[-1]=""
                req_url+="query({!edismax qf=body v='"+rt+"''}))&rows="+str(self.topk)
            else:
                req_url = solr_url+"fl=id,parent_body,body,score&indent=true&q.op=OR&q=("+q_text+")&qf=parent_body&bq=parent_body:("+rt+")*3&rq={!rerank reRankQuery=$rqq reRankDocs="+str(self.topk)+" reRankWeight=5}&rqq={!func}sum("
                for x in bt:
                    req_url+="query({!edismax qf=body v='"+x+"'}),"
                #req_url[-1]=""
                req_url+="query({!edismax qf=body v='"+rt+"'}))&rows="+str(self.topk)
        return req_url
    
    def search_index(self,core_name, q_text, reddit_topic_filter, bot_personality):
        self.personality=bot_personality
        
        url=self.formulate_query(core_name, q_text, reddit_topic_filter, bot_personality)
        
        # if 'cc' == core_name.strip().lower():
        #     bot_personality = bot_personality.strip().lower()
        #     req_url = solr_url+"fl=id,question,"+bot_personality+",score&indent=true&q.op=OR&q=question:("+q_text+")&rows=1"
        # else:
        #     rt=rare_terms(q_text)
        #     rt=functools.reduce(lambda a,b: a+' '+b, rt)
        #     if self.topic == reddit_topic_filter:
        #         rt=rt+' '+self.context
        #     elif continuity(self.prevq,q_text):
        #         rt=rt+' '+self.context
        #     if reddit_topic_filter:
        #         # what are the valid topics we have in the data??
        #         # Politics, Environment, Education, Techonology, Healthcare
        #         reddit_topic_filter = reddit_topic_filter.strip().title()
        #         req_url = solr_url+"fl=id,parent_body,body,score&indent=true&q.op=OR&q=parent_body:"+q_text+"&fq=topic:"+reddit_topic_filter+"&rq={!rerank reRankQuery=$rqq reRankDocs=10 reRankWeight=2}&rqq=body:("+rt+")&rows="+str(self.topk)
        #     else:
        #         req_url = solr_url+"fl=id,parent_body,body,score&indent=true&q.op=OR&q=parent_body:("+q_text+")&rq={!rerank reRankQuery=$rqq reRankDocs=10 reRankWeight=2}&rqq=body:("+rt+")&rows="+str(self.topk)
        print(url)
        resp = requests.get(url)
        results = self.parse_response(resp)
        self.update_context(q_text)
        self.prevq=q_text
        self.topic = reddit_topic_filter
        
        return results
    
    def fetch_answer_from_resp(self,resp, bot_personality):
        if not resp['docs']:
            return DEFAULT_RESPONSES[bot_personality]
        if 'body' in resp['docs'][-1]:
            return resp['docs'][-1]['body']
        return resp['docs'][0][self.personality]
    
    def process_query(self, session_id, query_text, reddit_topic_filter=None, bot_personality='enthusiastic', reset_context=False):
        """
            reddit_topic_filter: str from Politics, Healthcare, Education, Environment, Technology
            bot_personality: str from witty, enthusiastic, professional, friendly, caring
            k: int -> max num of documents to return from query result (for analytics)
            returns: dict
                    {
                        'answer' -> chatbot response selected from docs,
                        'explain' -> {'index_queried':, 'classifier_prob': , 'rare_terms_boosted': , 'entities_boosted': , 'context_terms_boosted': 'top_docs_retrieved': }
                        'query_id' -> populated from db after saving.
                    }
        """

        # Flush context based on session
        if reset_context:
            self.context = []
        bot_personality = bot_personality.lower()
        cc_class_thresh = 0.5
        class_pred = classifyQuery(query_text)
        if class_pred == 'UNKNOWN' or class_pred <= cc_class_thresh:
            core_name = 'Reddit'
        else:
            core_name = 'CC'
        
        resp = self.search_index(core_name, query_text, reddit_topic_filter, bot_personality)
        resp['class_pred'] = class_pred

        # return only top k documents...
        resp['docs'] = resp['docs'][:self.topk]
        
        if core_name == 'Reddit':
            resp['docs'] = self.update_scores(query_text,resp['docs'])
        
        resp['answer'] = self.fetch_answer_from_resp(resp, bot_personality)

        # SAVE TO DB  
        # desm_score = None if not resp['docs'] else resp['docs'][0]['desm_score']
        # bm25_score = None if not resp['docs'] else resp['docs'][0]['bm25_score']
        # resp['query_id'] = DB.insert_row(session_id=session_id, question=query_text, 
        # answer=resp['answer'], classifier=(resp['class_pred'] > cc_class_thresh).astype(int),
        #  classifier_probability=resp['class_pred'], top_ten_retrieved=resp['docs'], total_retrieved=resp['total retrieved'],
        # selected_topic=reddit_topic_filter, selected_bot_personality = bot_personality)
        resp['query_id'] = 42
        resp['explain'] = {'index_queried': 'Reddit' if core_name.lower() == 'reddit' else 'Chitchat', 
        'classifier_prob': resp['class_pred'], 'rare_terms_boosted': self.rt, 'entities_boosted': self.entities,
        'context_terms_boosted': self.context, 'top_docs_retrieved': resp['docs']}

        return {'query_id': resp['query_id'], 'answer': resp['answer'], 'explain': resp['explain']}


def main():
    bot=Chatbot()
    while True:
        inp_text = input('enter query:')
        if inp_text.lower().strip() == 'q':
            break
        
        # if len(inp_text) == 1 and inp_text in qa.keys():
        #     resp['answer']=np.random.choice(qa[inp_text])
        #ipdb.set_trace()
        resp = bot.process_query("", inp_text)
        # print(results)
        # print(resp['class_pred'])
        print(resp['answer'])

    return


if __name__ == '__main__':
    main()