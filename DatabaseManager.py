import sqlite3

class DatabaseManager:  # create DatabaseManager class

    def __init__(self, db_name):  # constructor to create a DatabaseManager instance
        self.db_name = db_name
        self.conn = sqlite3.connect("password_manager.db")
        self.cursor = self.conn.cursor()
    
    # function to create a users table in the database

    def create_user_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)  # define the schema of the table
        self.conn.commit()  # commit changes to database
    
    # function to create passwords table in the database

    def create_password_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password_encrypted TEXT NOT NULL
            )
        ''')  # define the schema of the table
        self.conn.commit()  # commit changes to the database
    
    # function to execute a custom query

    def execute_query(self, query, parameters=None):
        if parameters:  # check to see if there are parameters
            self.cursor.execute(query, parameters)  # execute query with parameters
        else:
            self.cursor.execute(query)  # execute query with no parameters
        self.conn.commit()  # commit changes to database

    # function to check if a username exists in the database

    def check_username_exists(self, username):
        self.cursor.execute("SELECT COUNT(*) FROM users where username = ?", (username,))  # execute a select query where the username = inputted username
        result = self.cursor.fetchone()[0]  # generates a count of how many times the username is in the table users

        if result > 0:  # if statement to see if there are matching results found in db
            return True  # return true if there are
        else:
            return False  # else return false

    # function to close the connection with the databse

    def close_connection(self):
        self.conn.close()  # close connection