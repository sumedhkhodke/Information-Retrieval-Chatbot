# test
# app.mount(CUSTOM_PATH, gradio_app)

from fastapi import FastAPI
import random
import gradio as gr
app = FastAPI()
@app.get("/")
def read_main():
    return {"message": "This is the parent app"}

# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
# def predict(input, history=[]):
#     # tokenize the new input sentence
#     new_user_input_ids = tokenizer.encode(input + tokenizer.eos_token, return_tensors='pt')

#     # append the new user input tokens to the chat history
#     bot_input_ids = torch.cat([torch.LongTensor(history), new_user_input_ids], dim=-1)

#     # generate a response 
#     history = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id).tolist()

#     # convert the tokens to text, and then split the responses into lines
#     response = tokenizer.decode(history[0]).split("<|endoftext|>")
#     response = [(response[i], response[i+1]) for i in range(0, len(response)-1, 2)]  # convert to tuples of list
#     return response, history

# gr.Interface(fn=predict,
#              inputs=["text", "state"],
#              outputs=["chatbot", "state"]).launch()
# chatbot = gr.Chatbot().style(color_map=("green", "pink"))
# demo = gr.Interface(
#     chat,
#     ["text", "state"],
#     [chatbot, "state"],
#     allow_flagging="never",
# )
# if __name__ == "__main__":
#     demo.launch(share=True)
# Then run `uvicorn run:app` from the terminal and navigate to http://localhost:8000/TheCodeLinguists.

def chat(message, history):
    history = history or []
    message = message.lower()
    if message.startswith("how many"):
        response = str(random.randint(1, 10))
    elif message.startswith("how"):
        response = random.choice(["Great", "Good", "Okay", "Bad"])
    elif message.startswith("where"):
        response = random.choice(["Here", "There", "Somewhere"])
    else:
        response = "Yes"
    history.append((message, response))
    return history, history

chatbot = gr.Chatbot().style(color_map=("blue", "blue"))
demo = gr.Interface(
    chat,
    ["text", "state"],
    [chatbot, "state"],
    allow_flagging="never",
    css="footer {visibility: hidden}"
)
app = gr.mount_gradio_app(app, demo, path="/TheCodeLinguists")
