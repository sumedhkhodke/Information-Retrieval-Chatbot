import gradio as gr


def chat(message, history):
    history = history or []
    history.append((message, message))
    return history, history


block = gr.Blocks()


with block:
    chatbot = gr.Chatbot()
    message = gr.Textbox()
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chat, inputs=[message, state], outputs=[chatbot, state])


block.launch()