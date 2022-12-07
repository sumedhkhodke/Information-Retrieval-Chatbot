import gradio as gr
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')

from .. import retrieval.configs

def show_relevance_by_topic():
    objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    y_pos = np.arange(len(objects))
    performance = [10,8,6,4,2,1]

    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Usage')
    plt.title('Programming language usage')
    return plt

with gr.Blocks() as demo:
    with gr.Row():
        text1 = gr.Textbox(label="t1")
        slider2 = gr.Textbox(label="s2")
        drop3 = gr.Dropdown(["a", "b", "c"], label="d3")
    with gr.Row():
        with gr.Column(scale=1, min_width=600):
            text1 = gr.Textbox(label="prompt 1")
            text2 = gr.Textbox(label="prompt 2")
            inbtw = gr.Button("Between")
            text4 = gr.Textbox(label="prompt 1")
            text5 = gr.Textbox(label="prompt 2")
        with gr.Column(scale=2, min_width=600):
            # img1 = gr.Image(show_relevance_by_topic)
            btn = gr.Button("Go").style(full_width=True)
            map = gr.Plot(show_relevance_by_topic)




demo.launch()