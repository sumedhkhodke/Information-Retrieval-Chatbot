# Save results
import pandas as pd

import sys
sys.path.append("../retrieval/")
from Database import Database

db = Database()

def run_query(db, sql_query):
    db.mycursor.execute(sql_query)
    records = db.mycursor.fetchall()
    return records
    
def save_data():
    sql_query = "SELECT selected_topic, AVG(user_feedback) FROM IRProject4Table WHERE user_feedback IS NOT NULL AND selected_topic IS NOT NULL GROUP BY selected_topic"
    # sql_query = "SELECT selected_topic, user_feedback FROM IRProject4Table WHERE user_feedback IS NOT NULL AND selected_topic IS NOT NULL"
    records = run_query(db, sql_query)
    df = pd.DataFrame(records, columns=['topic', 'user_feedback'])
    df.to_csv("relevance_by_topic.csv", sep="\t", index=False)

    sql_query = "SELECT classifier, AVG(user_feedback) FROM IRProject4Table WHERE user_feedback IS NOT NULL AND classifier IS NOT NULL GROUP BY classifier"
    records = run_query(db, sql_query)
    df = pd.DataFrame(records, columns=['Retrieval Index', 'user_feedback'])
    df.to_csv("relevance_by_database.csv", sep="\t", index=False)

    sql_query = "SELECT session_id, AVG(user_feedback) FROM IRProject4Table WHERE user_feedback IS NOT NULL AND session_id IS NOT NULL GROUP BY session_id"
    records = run_query(db, sql_query)
    df = pd.DataFrame(records, columns=['session_id', 'user_feedback'])
    df.to_csv("relevance_by_user.csv", sep="\t", index=False)

    return


if __name__ == '__main__':

    save_data()
    db.mydb.close()
