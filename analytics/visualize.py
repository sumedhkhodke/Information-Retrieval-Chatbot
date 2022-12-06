import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

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

    return

def show_relevance_by_database():
    # sql_query = "SELECT classifier, AVG(user_feedback) FROM IRProject4Database WHERE user_feedback IS NOT NULL GROUP BY classifier"
    sql_query = "SELECT classifier, AVG(user_feedback) FROM IRProject4Table WHERE user_feedback IS NOT NULL AND classifier IS NOT NULL GROUP BY classifier"
    records = run_query(db, sql_query)
    df = pd.DataFrame(records, columns=['Retrieval Index', 'user_feedback'])
    df.loc[:, 'Retrieval Index'] = df['Retrieval Index'].map({'1': 'Chitchat', '0': 'Reddit'})

    fig = plt.figure(figsize=(5, 7))
    df.plot(kind='bar', legend=False, width=0.3, x='Retrieval Index')
    plt.xticks(rotation=0, fontname='Arial Unicode MS')
    # plt.bar_label()
    plt.title('Retrieval Relevance per Database', pad=15, fontsize=18, fontweight='bold', fontname='Arial Unicode MS')
    plt.xlabel('Database', labelpad=10, size=15, fontname='Arial Unicode MS')
    plt.ylabel('% Relevance from user feedback', labelpad=12, size=15, fontname='Arial Unicode MS')
    fig.subplots_adjust(bottom=0)
    fig.show()

    return

def show_relevance_by_user():
    # "SELECT classifier, AVG(user_feedback) FROM IRProject4Table WHERE user_feedback IS NOT NULL AND classifier IS NOT NULL GROUP BY classifier"
    sql_query = "SELECT session_id, AVG(user_feedback) FROM IRProject4Table WHERE user_feedback IS NOT NULL and session_id IS NOT NULL GROUP BY session_id"
    records = run_query(db, sql_query)
    df = pd.DataFrame(records, columns=['session_id', 'user_feedback'])
    
    df_new = pd.cut(df['user_feedback'], bins=[0, 0.3, 0.5, 0.75, 1],
    labels=['irrelevant', 'somewhat relevant', 'relevant', 'highly relevant'])
    pie_df = (df_new.value_counts()/len(df)).to_frame().reset_index()
    pie_df = pie_df.rename(columns={'index': 'Relevance Judgement'})

    pie_df = pie_df.iloc[pd.Index(pie_df['Relevance Judgement']).get_indexer(['highly relevant','relevant','somewhat relevant', 'irrelevant'])].reset_index(drop=True)
    
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(aspect="equal"))

    recipe = pie_df['Relevance Judgement']
    data = pie_df['user_feedback']

    wedges, texts, _ = ax.pie(data, wedgeprops=dict(width=0.4), startangle=100, autopct='%.0f%%',
    pctdistance=0.8, textprops={'fontsize': 10, 'color': 'white', 'fontweight': 'heavy','fontname': 'Arial Unicode MS'},
    counterclock=False)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-", color='black'),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(recipe[i], xy=(x, y), xytext=(1.1*np.sign(x), 1.2*y),
                    horizontalalignment=horizontalalignment, **kw)

    ax.legend(['rel > 0.75', '0.5 > rel > 0.75', '0.3 > rel > 0.5', '0.0 > rel > 0.3'], loc='center left', bbox_to_anchor=[-0.8, 0.95])
    plt.title('User Relevance Assessment', pad=15, fontsize=18, fontweight='bold', fontname='Arial Unicode MS')
    fig.show()
    
    return


def show_wordcloud_by_topic():

    relative_path = "./"
    rel_path_word_clouds = "word_clouds_2/"

    plt.title('Education')
    img1 = mpimg.imread(relative_path + rel_path_word_clouds + 'word_cloud_edu_2.png')
    plt.axis('off')
    imgplot1 = plt.imshow(img1)
    plt.show()

    plt.title('Healthcare')
    img2 = mpimg.imread(relative_path + rel_path_word_clouds + 'word_cloud_health_2.png')
    plt.axis('off')
    imgplot2 = plt.imshow(img2)
    plt.show()

    plt.title('Environment')
    img3 = mpimg.imread(relative_path + rel_path_word_clouds + 'word_cloud_env_2.png')
    plt.axis('off')
    imgplot3 = plt.imshow(img3)
    plt.show()

    plt.title('Politics')
    img4 = mpimg.imread(relative_path + rel_path_word_clouds + 'word_cloud_poli_3.png')
    plt.axis('off')
    imgplot4 = plt.imshow(img4)
    plt.show()

    plt.title('Technology')
    img5 = mpimg.imread(relative_path + rel_path_word_clouds + 'word_cloud_tech_2.png')
    plt.axis('off')
    imgplot5 = plt.imshow(img5)
    plt.show()

    return

# df = pd.DataFrame([['Technology', 0.75],
# ['Healthcare', 0.65],
# ['Politics', 0.85],
# ['Education', 0.45],
# ['Environment', 0.5]], columns=['topic', 'user_feedback'])

# df = pd.DataFrame([['Reddit', 0.65],
# ['Chitchat', 0.75]], columns=['Retrieval Index', 'user_feedback'])

# df = pd.DataFrame([['1axR', 0.2],
# ['7x6r', 0.4],
# ['aris', 0.6],
# ['178r', 0.8],
# ['kr51', 0.3],
# ['xnw1', 0.5],
# ['xn61', 0.7]]
# , columns=['session_id', 'user_feedback'])

# sql_query = "SELECT topic, meta FROM IRProject4Database"
# records = run_query(db, sql_query)
# filter records by extracting total retrieved

# for rec in records:
#     rec['total_retrieved'] = rec['meta']['total_retrieved']

# topic_docs_df = pd.DataFrame(records, columns=['topic', 'total_retrieved'])

# topic_docs_df = pd.DataFrame([['Technology', 70],
#   ['Healthcare', 20],
#    ['Technology', 30],
#     ['Healthcare', 65],
#     'Technology', 50]])


# TEST ALL VIZ
# show_relevance_by_topic()
# show_relevance_by_database()
# show_relevance_by_user()
# show_wordcloud_by_topic()