import mysql.connector
from configs import DB_HOST

mydb = mysql.connector.connect(host=DB_HOST,user="backend",password='p4')
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IRProject4Database")
mydb = mysql.connector.connect(host=DB_HOST,user="backend",password='p4', database='IRProject4Database')
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IRProject4Table (id INT AUTO_INCREMENT PRIMARY KEY, session_id VARCHAR(255), question TEXT(65535), answer TEXT(65535), classifier VARCHAR(255), classifier_probability VARCHAR(255), top_ten_retrieved MEDIUMTEXT, user_feedback VARCHAR(255), total_retrieved VARCHAR(255), DESM_score VARCHAR(255), selected_topic VARCHAR(255), selected_bot_personality VARCHAR(255), meta TEXT(65535))")