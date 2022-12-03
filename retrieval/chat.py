import json
import pickle
import requests

from configs import HOST, PORT
from classifier_infer import classifyQuery
# import ipdb

from Database import Database
database = Database()

def process_query(query_text, reddit_topic_filter=None, bot_personality='enthusiastic', k=10):
    """
        reddit_topic_filter: str from Politics, Healthcare, Education, Environment, Technology
        bot_personality: str from witty, enthusiastic, professional, friendly, caring
        k: int -> max num of documents to return from query result (for analytics)
        returns: dict
                {
                    'class_pred': float -> represents prob of querying chitchat dataset 
                    'total_docs_retrieved' -> from the query (for analytics)
                    'docs' -> list of dict containing the retrieved results
                }
    """
    
    cc_class_thresh = 0.7
    class_pred = classifyQuery(query_text)
    if class_pred == 'UNKNOWN' or class_pred < cc_class_thresh:
        core_name = 'REDDIT'
    else:
        core_name = 'CHITCHAT'
    
    resp = search_index(core_name, query_text, reddit_topic_filter, bot_personality)
    resp['class_pred'] = class_pred

    # return only top k documents...
    resp['docs'] = resp['docs'][:k]

    return resp

def search_index(core_name, q_text, reddit_topic_filter, bot_personality):
    solr_url = f"http://{HOST}:{PORT}/solr/{core_name}/query?"

    # ipdb.set_trace()
    if 'chitchat' == core_name.strip().lower():
        bot_personality = bot_personality.strip().lower()
        req_url = solr_url+"fl=id,question,"+bot_personality+",score&indent=true&q.op=OR&q=question:"+q_text+"&rq={!rerank reRankQuery=$rqq reRankDocs=100 reRankWeight=5}&rqq=("+bot_personality+":"+q_text+")&rows=100"
    else:
        if reddit_topic_filter:
            # what are the valid topics we have in the data??
            # Politics, Environment, Education, Techonology, Healthcare
            reddit_topic_filter = reddit_topic_filter.strip().title()
            req_url = solr_url+"fl=id,parent_body,body,score&indent=true&q.op=OR&q=parent_body:"+q_text+"&fq=topic:"+reddit_topic_filter+"&rq={!rerank reRankQuery=$rqq reRankDocs=10 reRankWeight=5}&rqq=(body:"+q_text+")&rows=10"
        else:
            req_url = solr_url+"fl=id,parent_body,body,score&indent=true&q.op=OR&q=parent_body:"+q_text+"&rq={!rerank reRankQuery=$rqq reRankDocs=10 reRankWeight=5}&rqq=(body:"+q_text+")&rows=10"
    
    # print(req_url)
    resp = requests.get(req_url)
    results = parse_response(resp)

    return results


def parse_response(resp):
    results = []
    num_docs_found = 0
    try:
        # print(resp.json())
        num_docs_found = resp.json()['response']['numFound']

        for x in resp.json()['response']['docs']:
            results.append(x)
            # results.append({'score': x['score'], 'body': x['body'], 'id': x['id']})
            # print(x)
    except:
        # raise 
        pass
    
    return {'total_retrieved': num_docs_found, 'docs':results}


def main():
    bot_personalities = ['witty', 'enthusiastic', 'professional', 'friendly', 'caring']
    while True:
        inp_text = input('enter query:')
        if inp_text.lower().strip() == 'q':
            break

        # ipdb.set_trace()
        resp = process_query(inp_text)
        # print(results)
        print(resp['class_pred'])
        if resp['docs']:
            top_res = resp['docs'][0]
            if 'body' in top_res:
                print(top_res['body'])
            else:
                p = set(bot_personalities).intersection(set(top_res.keys())).pop()
                print(top_res[p])
                
    core_name = ''
    if resp['class_pred'] == 'UNKNOWN' or resp['class_pred'] < 0.7:
        core_name = 'Reddit'
    else:
        core_name = 'CC'
                
    top_ten_json = json.dumps(resp['docs'])
                        
    database.insert_row("0", inp_text, answer, core_name, str(resp['class_pred']), "", "None", resp['total_retrieved'])


    return


if __name__ == '__main__':
    main()



