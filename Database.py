import mysql.connector


class Database:
    

    def __init__(self):
        # self.mydb = mysql.connector.connect(host="localhost",user="pradhaneva94",password='')
        # # print("self.mydb: ", self.mydb)
        
        # self.mycursor = self.mydb.cursor()
        
        # self.mycursor.execute("CREATE DATABASE IRProject4Database")

        self.mydb = mysql.connector.connect(host="localhost",user="pradhaneva94",password='', database="IRProject4Database")
        self.mycursor = self.mydb.cursor()
        # self.mycursor = self.mydb.cursor()
        # self.mycursor.execute("CREATE TABLE IRProject4Table (id INT AUTO_INCREMENT PRIMARY KEY, session_id VARCHAR(255), question TEXT(65535), answer TEXT(65535), classifier VARCHAR(255), classifier_probability VARCHAR(255), top_ten_retrieved TEXT(65535), user_feedback VARCHAR(255), total_retrieved VARCHAR(255))")

        self.mycursor.execute("SHOW TABLES")
        for x in self.mycursor:
            print(x)
            
        self.table_name = "IRProject4Table"
    
    
    
    def insert_into(self, column_name, column_value):

        sql = "INSERT INTO " + self.table_name + " (" + column_name +") VALUES (%s)"
        val = column_value
        self.mycursor.execute(sql, val)

        self.mydb.commit()

        print(self.mycursor.rowcount, "record inserted.")
        print("1 record inserted, ID:", self.mycursor.lastrowid)



    def retrieve_from(self, session_id):

        sql = "SELECT * FROM " + self.table_name + " WHERE session_id = %s"
        adr = session_id

        self.mycursor.execute(sql, adr)

        myresult = self.mycursor.fetchall()

        for x in myresult:
            print(x)
            
        return x
    
    def drop_id(self, id):
        sql = "DELETE FROM " + self.table_name + " WHERE id = " + id

        self.mycursor.execute(sql)

        self.mydb.commit()

        print(self.mycursor.rowcount, "record(s) deleted")
        return
    
    def drop_all(self, id):
        return
    
    def update_column_by_id(self, column, value, id):
        
        sql = "UPDATE customers SET "+ column +" = "+ value +" WHERE id = " + id

        self.mycursor.execute(sql)

        self.mydb.commit()

        print(self.mycursor.rowcount, "record(s) affected")
    
    def only_fetch_all(self):
        sql = "SELECT * FROM IRProject4Database"

        self.mycursor.execute(sql)

        myresult = self.mycursor.fetchall()

        for x in myresult:
            print(x)
            
        return x
    
    def insert_row(self, session_id, question, answer, classifier, classifier_probability, top_ten_retrieved, user_feedback, total_retrieved):

        sql = "INSERT INTO " + self.table_name + " (session_id, question, answer, classifier, classifier_probability, top_ten_retrieved, user_feedback, total_retrieved) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = [session_id, question, answer, classifier, classifier_probability, top_ten_retrieved, user_feedback, total_retrieved]
        self.mycursor.execute(sql, val)

        self.mydb.commit()

        # print(self.mycursor.rowcount, "record inserted.")
        # print("1 record inserted, ID:", self.mycursor.lastrowid)
        return
            
if __name__ == "__main__":
    
    Database_Project4 = Database()
    # val = ["session_id1", "question1", "answer1", "classifier1", "classifier_probability1", "top_ten_retrieved1", "user_feedback1", "total_retrieved1"]

    Database_Project4.insert_row("session_id1", "question1", "answer1", "classifier1", "classifier_probability1", "top_ten_retrieved1", "user_feedback1", "total_retrieved1")
    # Database_Project4.retrieve_from()
