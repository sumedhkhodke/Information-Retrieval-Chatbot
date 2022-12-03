

import gradio as gr
from typing import List;
inp = 'fdsf'
def chatbot1(inp: List[str]):
  ... # gets the response from chatbot 1 given a list of the previous conversation
  return inp+'a'

# def chatbot2(inp: List[str]):
#   ... # gets the response from chatbot 2 given a list of the previous conversation
#   return inp+'b'

# def chatbot3(inp: List[str]):
#   ... # gets the response from chatbot 3 given a list of the previous conversation
#   return inp+'c'
  

def chat(inp1: str, state: List[List[str]] = [[]]):
  if inp1:
    response = chatbot1(inp1)
    state[0].append((inp1, response))
  
  outputs = []
  for s in state:
    html = "<div class='chatbot'>"
    for user_msg, resp_msg in s:
        html += f"<div class='user_msg'>{user_msg}</div>"
        html += f"<div class='resp_msg'>{resp_msg}</div>"
    html += "</div>"
    outputs.append(html)
  return outputs, state
    
iface = gr.Interface(chat, ["text", "state"], ["html", "state"], css="""
    .chatbox {display:flex;flex-direction:column}
    .user_msg, .resp_msg {padding:4px;margin-bottom:4px;border-radius:4px;width:80%}
    .user_msg {background-color:cornflowerblue;color:white;align-self:start}
    .resp_msg {background-color:lightgray;align-self:self-end}
""")

iface.launch()