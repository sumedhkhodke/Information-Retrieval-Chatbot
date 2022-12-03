import numpy as np
from typing import List
import gradio as gr

from fastapi import FastAPI
import random
import gradio as gr
app = FastAPI()
@app.get("/")
def read_main():
    return {"message": "This is the parent app"}

def do1(inp):
    return inp+' aaaaa'

def chat(message, history):
    history = history or []
    response = do1(message)
    history.append((message, response))
    message = gr.Textbox(label="Enter your message below",placeholder='Hi, how\'s it going?',lines=1,max_lines=4)
    return history, history#,message

def clear(message,history):
    state = gr.State()
    history=[]
    message = gr.Textbox(label="Enter your message below",placeholder='Hi, how\'s it going?',lines=1,max_lines=4)
    return history,history#,message

with gr.Blocks(css="footer {visibility: hidden}") as demo:
    with gr.Tab("Chatbot"):
        with gr.Column():
            with gr.Row():
                personality = gr.Dropdown(['Enthusiastic', 'Witty','Professional', 'Friendly', 'Caring'],value='Enthusiastic',label='Select a personality')
                faceted_key = gr.Dropdown(['None','Technology','Education','Healthcare','Politics','Environment'],value='None',label    ='Faceted search')
            chatbot = gr.Chatbot()
            message = gr.Textbox(label="Enter your message below",placeholder='Hi, how\'s it going?',lines=1,max_lines=4)
            state = gr.State()

            with gr.Row():
                submit_button = gr.Button("Submit")
                clear_button = gr.Button("Clear")
    with gr.Tab("Analytics"):
        gr.Markdown("Look at me...")
    with gr.Tab("Visualization"):
        gr.Markdown("Look at me...")
    # personality.click
    submit_button.click(chat, inputs=[message, state], outputs=[chatbot, state])
    clear_button.click(clear, inputs=[message, state], outputs=[chatbot, state])
# demo.launch()

app = gr.mount_gradio_app(app, demo, path="/TheCodeLinguists")