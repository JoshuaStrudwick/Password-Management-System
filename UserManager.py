import hashlib
import sqlite3
from DatabaseManager import *

class UserManager:

    def __init__(self, db_manager, password_manager, encryption_manager):  # constructor to create a UserManager instance
        self.db_manager = db_manager
        self.password_manager = password_manager
        self.encryption_manager = encryption_manager

    # function to create an account in the database

    def createaccount(self, username, password, confirm_psw):

        if len(username) < 5:  # check to see if username is less than 5 characters
            return False  # return false
        elif self.db_manager.check_username_exists(username):  # if statement to see if the username already exists in the database
            return False  # return false
        else:
            pass

        if len(password) < 5:  # if statement to see password is less than 5 characters
            return False  # return false
        else:
            pass

        if confirm_psw == password:  # if statement ot see if password and confirm password match
            password = password.encode()  # encode the password to a byte sequence
            psw_hashed = hashlib.md5(password).hexdigest()

            """
            md5 - Message Digest 5 - generates a hash value based on password
            .hexdigest() - converts output of md5 and gets the hexadecimal representation of the hash in string format
            """

            self.db_manager.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, psw_hashed))  # uses cursor(basically a pointer in database) to execute a INSERT query to put the new account details into the users table in the database
            self.db_manager.conn.commit()  # calls on the connection between database and commits the change permantly into the databse
            return True  # returns true if complete
    
    # function that logs a user into the system and returns the users id if complete

    def acclogin(self, login_username, login_password):

            login_password = login_password.encode()  # emcodes the login password to a byte sequence
            hashed_pw = hashlib.md5(login_password).hexdigest()

            """
            md5 - Message Digest 5 - generates a hash value based on password
            .hexdigest() - converts output of md5 and gets the hexadecimal representation of the hash in string format
            """

            self.db_manager.cursor.execute("SELECT id FROM users WHERE username = ? AND password_hash = ?", (login_username, hashed_pw)) # uses cursor(basically a pointer in database) to execute a SELECT query to check the database to see if the username and password are in the users table
            user = self.db_manager.cursor.fetchone()  # returns the user id of the user, fetchone() retrives next row of query result and returns one row at a time

            if user:  # if user exists
                return user[0]  # return the users unique ID
            else:
                return None  # retunr None if dosent exist