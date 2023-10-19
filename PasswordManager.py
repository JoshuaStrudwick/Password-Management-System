from DatabaseManager import *
from EncryptionManager import *
import secrets


class PasswordManager:

    def __init__(self, db_manager, encryption_manager):  # constuctor to create a PasswordManager instance
        self.db_manager = db_manager
        self.encryption_manager = encryption_manager

    # function to encrypt and store password and associated details in the database

    def store_password(self, user_id, service, username, password, master_password):
        key = self.encryption_manager.generate_encryption_key(user_id, master_password)  # generate a symmetrical encryption key

        encrypted_password = key.encrypt(password.encode()).decode()  # encrypts the password byte sequences and then returns it as a string

        self.db_manager.cursor.execute('INSERT INTO passwords (user_id, service, username, password_encrypted) VALUES (?, ?, ?, ?)',(user_id, service, username, encrypted_password))  # insert encryped password and details into the passwords table of the database
        self.db_manager.conn.commit()  # commit to the database
        return True  # return true if complete

    # function to retrive a password from the database

    def retrieve_passwords(self, user_id, master_password):
        key = self.encryption_manager.generate_encryption_key(user_id, master_password)  #  # generate a symmetrical encryption key for decryption in this case

        self.db_manager.cursor.execute('SELECT service, username, password_encrypted FROM passwords WHERE user_id = ?', (user_id,))  # select all stored passwords for a specific user
        password_records = self.db_manager.cursor.fetchall()  # fetchall records

        decrypted_passwords = []  # empty list to store decrypted passwords
        for record in password_records:  # for loop to go through all records in password records
            service, username, encrypted_password = record  # record = service username encrypted password
            decrypted_password = key.decrypt(encrypted_password.encode()).decode()  # decrypt the encrypted password using the symmetrical key generated aboce and return the password as a string
            decrypted_passwords.append((service, username, decrypted_password))  # append the record with the decrypted password to the list

        return decrypted_passwords  # return the decrypted passwords

    # function to generate a random password
        
    def gen_password(self):
        length = 16  # length of random password

        password = secrets.token_hex(length // 2)  # secrets generates a cryptographically secure random string, .token_hex generates a random hexadecimal base-16 string , hex 4 bits so need to divide length by 2

        return password[:length]  # return password up to length
    
    # function to change a specific records password

    def change_password(self, user_id, service, username, new_password, master_password):

        key = self.encryption_manager.generate_encryption_key(user_id, master_password)  # generate encryption and decryption key
        encrypted_password = key.encrypt(new_password.encode()).decode()  # encrypt the new password using above key and return in string format

        self.db_manager.cursor.execute('UPDATE passwords SET password_encrypted = ? WHERE user_id = ? AND service = ? AND username = ?', (encrypted_password, user_id, service, username))  # update record in the database with the encrypted password
        self.db_manager.conn.commit()  # commit to database
        return True  # return true if complete