import gradio as gr
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
# plt.switch_backend('agg')
import pandas as pd

import seaborn
seaborn.set()

import sys
sys.path.append("../retrieval/")
from Database import Database
db = Database()

def run_query(db, sql_query):
    db.mycursor.execute(sql_query)
    records = db.mycursor.fetchall()
    return records

def show_relevance_by_topic():
    sql_query = "SELECT selected_topic, AVG(user_feedback) FROM IRProject4Table WHERE user_feedback IS NOT NULL AND selected_topic IS NOT NULL GROUP BY selected_topic"
    # sql_query = "SELECT selected_topic, user_feedback FROM IRProject4Table WHERE user_feedback IS NOT NULL AND selected_topic IS NOT NULL"
    records = run_query(db, sql_query)
    print(records)
    df = pd.DataFrame(records, columns=['topic', 'user_feedback'])
    # plt.bar(df['topic'], df['user_feedback'])
    fig = plt.figure(figsize=(5, 7))
    df.plot(kind='bar', legend=False, width=0.5, x='topic')
    plt.xticks(rotation=0, fontname='Arial Unicode MS')
    # plt.bar_label()
    plt.title('Retrieval Relevance per Topic', pad=15, fontsize=18, fontweight='bold', fontname='Arial Unicode MS')
    plt.xlabel('Topics', labelpad=12, size=15, fontname='Arial Unicode MS')
    plt.ylabel('% Relevance from user feedback', labelpad=12, size=15, fontname='Arial Unicode MS')
    fig.subplots_adjust(bottom=0.5)
    fig.show()
    return fig

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