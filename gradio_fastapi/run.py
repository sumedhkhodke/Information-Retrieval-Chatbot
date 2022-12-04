from fastapi import FastAPI
import random
import numpy as np
from typing import List
import gradio as gr
import os, sys
import uuid
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../retrieval/')
import bot

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

    def do1(inp):
        response=inp['query_text'] +' aaaaa'
        return response

    def get_session(state, session_id):
        return uuid.uuid4() if state is None else session_id

    def chat(message, state, personality, faceted_key):
        state = state or []
        session_id='239843d9-741e-11ed-8648-e02be9d57d03' 
        session_id = get_session(state,session_id)
        dic={}
        dic['query_text']=message
        dic['personality']=personality
        dic['faceted_key']=faceted_key
        dic['session_key']=session_id
        dic['chat_history']=state
        if state is []: context_flag=True
        else: context_flag=False
        response = classObj.process_query(session_id,message,faceted_key,personality,context_flag)
        # response = do1(dic)
        
        bot_response=response['answer']
        response_id=response['query_id']
        explain=response['explain']
        state.append((message, bot_response))
        return state, state, response_id#,explain

    def clear(message, state, personality, faceted_key):
        state = gr.State()
        state=[]
        return state, state

    def feedback(feedback,q_id):
        dic1={}
        dic1['feedback']=feedback
        dic1['q_id']=q_id
        dic1['session_id']=session_id
        classObj.update_feedback(q_id,feedback)
        # ~ = do2(dic1)
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
                    # feedback_button_11, feedback_radio, feedback_button, feedback_button_12 = gr.Columns(4)
                    feedback_button_11 = gr.Button("Send feedback",visible=False)
                    feedback_radio=gr.Radio(label='Was the last response of the chatbot relevant?',choices=["Satisfactory","Not satisfactory"])
                    feedback_button = gr.Button("Send feedback")
                    feedback_button_12 = gr.Button("Send feedback",visible=False)
        with gr.Tab("Analytics"):
            gr.Markdown("Look at me...")

        with gr.Tab("Visualization"):
            gr.Markdown("Look at me...")
        # q_id_placeholder_component = gr.Textbox(visible=False)
        # explainability = gr.Textbox(visible=False)
        submit_button.click(chat, inputs=[message, state, personality, faceted_key], outputs=[chatbot, state])#,q_id_placeholder_component,explainability])
        clear_button.click(clear, inputs=[message, state, personality, faceted_key], outputs=[chatbot, state])
        feedback_button.click(feedback, inputs=[feedback_radio])#, q_id_placeholder_component])
    # demo.launch()
    app = gr.mount_gradio_app(app, demo, path="/TheCodeLinguists")

except Exception as E:
    print(E)
    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))