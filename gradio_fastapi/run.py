from fastapi import FastAPI
import random
import numpy as np
from typing import List
import gradio as gr
import os, sys
import uuid
import sys
from functools import partial
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.append(os.getcwd()+'/../retrieval/')
sys.path.append(os.getcwd()+'/../analytics/')
import visualize as vu 
import bot
from Database import Database

DB = Database()
try:
    app = FastAPI()
    classObj = bot.Chatbot()
    

    @app.get("/")
    def read_main():
        return {"message": "This is the parent app"}

    session_id='239843d9-741e-11ed-8648-e02be9d57d03'    
    class Button_(gr.Button):
        def click(self, *args, **kwargs):
            super().click(*args, **{**kwargs, **dict(inputs=None, outputs=None)})

    def get_session(state):
        return str(uuid.uuid4())

    def chat(session_id, message, state, personality, faceted_key):
        state=state or []
        if state==[]: 
            session_id = get_session(state)
        dic={}
        dic['query_text']=message
        dic['personality']=personality
        dic['faceted_key']=faceted_key
        dic['session_key']=session_id
        dic['chat_history']=state
        if state is []: context_flag=1
        else: context_flag=0
        response = classObj.process_query(DB, session_id,message,faceted_key,personality,context_flag)
        bot_response=response['summary']
        response_id=response['query_id']
        explain=response['explain']
        index_queried = explain['index_queried']
        classifier_prob = np.round(explain['classifier_prob'])
        rare_terms_boosted = explain['rare_terms_boosted']
        entities_boosted = explain['entities_boosted']
        context_terms_boosted = explain['context_terms_boosted']
        top_terms = explain['top_docs_retrieved']
        top_terms_text=""
        if top_terms:
            leng= len(top_terms)
            for i in top_terms:
                top_terms_text = top_terms_text+'[ '
                for k,j in i.items():
                    top_terms_text = top_terms_text+f'{k} : {j}\t'
                top_terms_text = top_terms_text+' ]'
                if i!=top_terms[-1]:
                    top_terms_text = top_terms_text+','
                    top_terms_text = top_terms_text+f'\n'
        state.append((message, bot_response))
        explain_text=f'Query : {message} \n Response : {bot_response} \n Index searched : {index_queried} \n Classifier probability for searched index : {classifier_prob} \n Rare terms boosted : {rare_terms_boosted} \n Entities boosted : {entities_boosted} \n Context terms boosted : {context_terms_boosted} \n Top retrieved docs : {top_terms_text}'
        return state, state,explain_text,response_id,session_id

    def clear(message, state, personality, faceted_key):
        state = gr.State()
        state=[]
        return state, state

    def feedback(feedback,q_id):
        if q_id=='': return "You need to use the chatbot to get a response to provide its feedback."
        feedback_dict={'Satisfactory':1,'Not satisfactory':0}
        feedback=feedback_dict[feedback]
        # bot.update_feedback(DB, q_id,feedback)
        return None

    def reset_personality_dropdown():
        return gr.Dropdown.update(['Enthusiastic', 'Witty','Professional', 'Friendly', 'Caring'],label='Select a personality',value='Enthusiastic')

    def reset_faceted_key_dropdown():
        return gr.Dropdown(['None','Technology','Education','Healthcare','Politics','Environment'],label='Faceted search',value='None')


    with gr.Blocks(css="footer {visibility: hidden}") as demo:
        gr.Markdown("""
        <p style="text-align:center">Chatbot by TheCodeLinguists</p>
        """)
        with gr.Tab("Chatbot"):
            with gr.Column():
                with gr.Row():
                    personality = gr.Dropdown(['Enthusiastic', 'Witty','Professional', 'Friendly', 'Caring'],label='Select a personality',value='Enthusiastic')
                    faceted_key = gr.Dropdown(['None','Technology','Education','Healthcare','Politics','Environment'],label='Faceted search',value='None')
                chatbot = gr.Chatbot()
                message = gr.Textbox(label="Enter your message below",placeholder='Hi, how\'s it going?',lines=1,max_lines=4)
                state = gr.State()

                with gr.Row():
                    submit_button = gr.Button("Submit")
                    clear_button = gr.Button("Clear")
                with gr.Row():
                    feedback_button_11 = gr.Button("Send feedback",visible=False)
                    feedback_radio=gr.Radio(label='Was the last response of the chatbot relevant?',choices=["Satisfactory","Not satisfactory"])
                    feedback_button = gr.Button("Send feedback")
                    feedback_button_12 = gr.Button("Send feedback",visible=False)
        with gr.Tab("Analytics"):
            # gr.Markdown("Analytics of the retrieved response")
            explainability = gr.Textbox(label="Detailed analytics for the chatbot's last response",lines=15)

        with gr.Tab("Visualizations"):
            gr.Markdown("Understanding the IR model")
            # srbt = partial(vu.show_relevance_by_topic, DB)
            # srbd = partial(vu.show_relevance_by_database, DB)
            # srbu = partial(vu.show_relevance_by_user, DB)

            # srbt()
            # srbd()
            # srbu()
            # plot1 = gr.Plot(srbt)
            # plot2 = gr.Plot(srbd)
            # plot3 = gr.Plot(srbu)

            rel_path_word_clouds = "./word_clouds_2/"
            plot1 = gr.Image(label='Relevance of responses by Topic', value=rel_path_word_clouds + 'srbt.png',shape=(5,7)).style(height=560, width=750)
            plot2 = gr.Image(label='Relevance of responses by Database Queried', value=rel_path_word_clouds + 'srbd.png',shape=(5,7)).style(height=560, width=750)
            plot3 = gr.Image(label='Relevance of responses as judged by Users', value=rel_path_word_clouds + 'srbu.png',shape=(5,7)).style(height=560, width=750)

            plot4 = gr.Image(label='WordCloud for topic - Education',value=rel_path_word_clouds + 'word_cloud_edu_2.png',shape=(10,10)).style(height=560, width=750)
            plot4 = gr.Image(label='WordCloud for topic - Healthcare',value=rel_path_word_clouds + 'word_cloud_health_2.png',shape=(10,10)).style(height=560, width=750)
            plot4 = gr.Image(label='WordCloud for topic - Environment',value=rel_path_word_clouds + 'word_cloud_env_2.png',shape=(10,10)).style(height=560, width=750)
            plot4 = gr.Image(label='WordCloud for topic - Politics',value=rel_path_word_clouds + 'word_cloud_poli_3.png',shape=(10,10)).style(height=560, width=750)
            plot4 = gr.Image(label='WordCloud for topic - Technology',value=rel_path_word_clouds + 'word_cloud_tech_2.png',shape=(10,10)).style(height=560, width=750)
            # plot4 = gr.Plot(vu.show_wordcloud_by_Education)
            # plot5 = gr.Plot(vu.show_wordcloud_by_Healthcare)
            # plot6 = gr.Plot(vu.show_wordcloud_by_Environment)
            # plot7 = gr.Plot(vu.show_wordcloud_by_Politics)
            # plot8 = gr.Plot(vu.show_wordcloud_by_Technology)
        q_id_placeholder_component = gr.Textbox(visible=False)
        session_id =  gr.Textbox(visible=False,value=None)
        submit_button.click(chat, inputs=[session_id,message, state, personality, faceted_key], outputs=[chatbot, state,explainability,q_id_placeholder_component,session_id])
        clear_button.click(clear, inputs=[message, state, personality, faceted_key], outputs=[chatbot, state])
        feedback_button.click(feedback, inputs=[feedback_radio, q_id_placeholder_component])
    # demo.launch()
    app = gr.mount_gradio_app(app, demo, path="/TheCodeLinguists")

except Exception as E:
    print(E)
    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
