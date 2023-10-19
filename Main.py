import customtkinter as ctk
from PasswordManager import *
from UserManager import *

# this function will login a user if the details are correct and match a record in the database

def login_button_pressed(ausermanager, username, password, error_message):

    if username == "" or password == "":  # if statement used to check if the user has not filled in all fields
        error_message.configure(frame, text="Please fill out all fields!", text_color = "red")  # print error message to user
        error_message.pack()

    else:  # if all fields filled in
        id = UserManager.acclogin(ausermanager, username, password)  # get the id of the user who has logged in

        if (id == None):  # if statement to check if details do not match a record
            error_message.configure(frame, text="These login details are incorrect!", text_color = "red")  # print error message to user
            error_message.pack()

        else:  # if details match a record
            clear_frame()  # clear widgets from screen
            label_text.set("Password Manager")  # set the title of the page
            ctk.CTkLabel(frame, textvariable=label_text, font=("", 18)).pack(pady=10, padx=10)  # print the title of the page
            ctk.CTkButton(frame, text="Log Out", command=lambda:back_to_login_page(error_message), width = 10, height=30).place(x= 10, y =10)  # log out button
            ctk.CTkButton(frame, text="Store a password", command=lambda:store_password_page(id, password)).pack(pady=30, padx=10)  # button that will take the user to a page that allows the user to store their passwords
            ctk.CTkButton(frame, text="Retrieve a password", command=lambda:retrieve_password_page(id, password)).pack(pady=30, padx=10)  # button to take the user to a page to retrieve previously stored passwords


# this function produces the page that allows the user to store a password

def store_password_page(id, mstr_password):

    clear_frame()  # clear widgets from screen
    ctk.CTkButton(frame, text="Back", command=lambda:back_logged_page(id, mstr_password), width = 10, height=30).place(x= 10, y =10)  # back button that returns user to the previous page
    ctk.CTkLabel(frame, text="Store a Password:", font=("", 18)).pack(pady=10, padx=10)  # print the title of the page
    service_entry = ctk.CTkEntry(frame, placeholder_text="Service")  # entry box that allows the user to enter the service they want to store a password on
    service_entry.pack(pady=5, padx=10)  # print the entry box to the user
    username_entry = ctk.CTkEntry(frame, placeholder_text="Username")  # entry box that allows the user to enter the username they want to store a password on
    username_entry.pack(pady=5, padx=10)  # print the entry box to the user
    password_entry = ctk.CTkEntry(frame, placeholder_text="Password")  # entry box that allows the user to enter the password they want to store
    password_entry.pack(pady=5, padx=10)  # print the entry box to the user
    ctk.CTkButton(frame, text="Generate a password", command=lambda:generate_password(pwordmanager, password_entry)).pack(pady=5, padx=10)  # button that generates a random password and inserts it into password entry box
    ctk.CTkButton(frame, text="Submit", command=lambda:submit_store_password(pwordmanager, id, service_entry.get(), username_entry.get(), password_entry.get(), mstr_password, err_message)).pack(pady=5, padx=10)  # button that stores the password in the database (encrypted)
    err_message = ctk.CTkLabel(frame, text="")  # error message layout

# this function will handle submitting the password that was entered in the store_password_page function

def submit_store_password(apasswordmanager, user_id, service, username, password, master_password, err_message):
    
    if service == "" or username == "" or password == "":  # if statement used to check if any of the entry boxes are left blank
        err_message.configure(frame, text="Fill Out All Fields!", text_color = "red")  # error message
        err_message.pack()
    else:  # if all fields filled out
        result = PasswordManager.store_password(apasswordmanager, user_id, service, username, password, master_password)  # store the password in the database (result = true if successfully stored)
        if result:  # if statement if password and details successfully stored in the database
            err_message.configure(frame, text="Successfully Stored!", text_color = "green")  # completion message
            err_message.pack()
        else:  # if statement if password and details failed to be stored in the database
            err_message.configure(frame, text="Failed to Stored!", text_color = "red")  # error message
            err_message.pack()

# this function produces a page related to retrieving a stored password

def retrieve_password_page(id, password):

    clear_frame()  # clears all the widgets of the previous page
    ctk.CTkButton(frame, text="Back", command=lambda:back_logged_page(id, password), width = 10, height=30).place(x= 10, y =10)  # back button
    ctk.CTkLabel(frame, text="Retrieve a Password:", font=("", 18)).pack(pady=10, padx=10)  # prints page title
    service = ctk.CTkEntry(frame, placeholder_text="Service")  # entry box for the services the user wants to retrive details on
    service.pack(pady=5, padx=10)
    usrnm = ctk.CTkEntry(frame, placeholder_text="Username")  # entry box for the usernames the user wants to retrive details on
    usrnm.pack(pady=5, padx=10)
    psw = ctk.CTkEntry(frame, placeholder_text="Password")  # entry box for the passwords the user wants to retrive details on
    psw.pack(pady=5, padx=10)
    ctk.CTkButton(frame, text="Submit", command=lambda:returned_password_page(service.get(), usrnm.get(), psw.get(), id, password, wrong1)).pack(pady=5, padx=10)  # button that submits the details and takes the user to a page returning the valid results
    wrong1 = ctk.CTkLabel(frame, text="")  # error message layout

# this function will produce a page to the user that returns the details based on the info put in entry boxes of the function retrieve_password_page

def returned_password_page(service, usernm, psw, username, password, wrong):

    if service == "" and usernm == "" and psw == "":  # if statement to check if all fields are left blank
        wrong.configure(frame, text="Please fill out one field", text_color="red")  # error message
        wrong.pack()

    else:  # if a field has data input
        
        list = PasswordManager.retrieve_passwords(pwordmanager, username, password)  # retrieve all the stored passwords of the user and put them into a list

        correct_list = []
        correct_service = ""
        correct_username = ""
        correct_password = ""

        for items in list:  # for statement to go through the list of all user passwords

            if items[0] == service or items[1] == usernm or items[2] == psw:  # check to see if any of the details match the search criteria
                if items[0] != "" and items[1] != "" and items[2] != "":  # if statement to ensure no blank stored details are passed through
                    correct_list.append([items[0], items[1], items[2]])  # append all valid details to a new list

        if correct_list:  # if statement to check if there are any valid records
            clear_frame()  # clear widgets of previous page
            length_of_list = len(correct_list)  # get the length of valid records
            correct_service = "Service: " + correct_list[0][0]  # print out first valid record
            correct_username = "Username: " + correct_list[0][1]
            correct_password = "Password: " + correct_list[0][2]
            current_display = 1  # create a count

            ctk.CTkButton(frame, text="Back", command=lambda:back_logged_page(username, password), width=10, height=30).place(x= 10, y =10)  # back button
            ctk.CTkLabel(frame, text="Account Details:", font=("", 18)).pack(pady=10, padx=10)  # print page title
            ctk.CTkLabel(frame, text=correct_service).pack(pady=5, padx=10)  # print first records service
            ctk.CTkLabel(frame, text=correct_username).pack(pady=5, padx=10)  # print first records username
            ctk.CTkLabel(frame, text=correct_password).pack(pady=5, padx=10)   # print first records password
            ctk.CTkButton(frame, text="Change Password", command=lambda:change_password(username, correct_service, correct_username, password)).pack(pady=5, padx=10)  # button that allows user to change current viewed records password

            if length_of_list >= (current_display+1):  # if statement to check if there are multiple valid records

                ctk.CTkButton(frame, text="Next Record", command=lambda:next_retrieve(correct_list, length_of_list, current_display, no_next, username, password)).pack(pady=5, padx=10)  # next button that takes user to next valid record
            
            no_next = ctk.CTkButton(frame, text="")  # error message layout
        
        else:
            wrong.configure(frame, text="No Records Found!", text_color = "red")  # error message
            wrong.pack()

# this function will take the user to the next valid record

def next_retrieve(list, length, current, error_message,id,mst_psw):
    clear_frame()  # clear previous pages widgets
    current += 1  # increase counter

    c_service = ""
    c_username = ""
    c_password = ""

    if current > length:  # if statement to see if there are no more records
        error_message.configure("There are no other records stored!", text_color = "red")  # error message
        error_message.pack()
    else:
        c_service = "Service: " + list[(current-1)][0]  # get next users details
        c_username = "Username: " + list[(current-1)][1]
        c_password = "Password: "+ list[(current-1)][2]
        ctk.CTkButton(frame, text="Back", command=lambda:back_logged_page(id, mst_psw), width=10, height=30).place(x= 10, y =10)  # back button
        ctk.CTkLabel(frame, text="Account Details:",font=("", 18)).pack(pady=10, padx=10)  # print page title
        ctk.CTkLabel(frame, text=c_service).pack(pady=5, padx=10)  # output next details
        ctk.CTkLabel(frame, text=c_username).pack(pady=5, padx=10)
        ctk.CTkLabel(frame, text=c_password).pack(pady=5, padx=10)
        ctk.CTkButton(frame, text="Change Password", command=lambda:change_password(id, c_service, c_username, mst_psw)).pack(pady=5, padx=10)  # button to change current users password

        if length >= (current+1):  # if statement to check if there is another record after this

            ctk.CTkButton(frame, text="Next Record", command=lambda:next_retrieve(list, length, current, error_message, id,mst_psw)).pack(pady=5, padx=10)  # button that teakes user to next valid record
        
        if current > 1:  # if statement to check if there is a record before this one

            ctk.CTkButton(frame, text="Previous Record", command=lambda:previous_retrieve(list, length, current, error_message, id,mst_psw)).pack(pady=5, padx=10)  # button to take user to previous valid record

# function that takes the user to the previous valid record based on entry boxes of the retrieve a password page

def previous_retrieve(list, length, current, error_message, id,mst_psw):

    clear_frame()  # clears the widgets of previous page
    current -= 1  # decrease counter

    c_service = ""
    c_username = ""
    c_password = ""

    if current > length:  # checks if there are no records after this
        error_message.configure("There are no other records stored!", text_color = "red")  # error message
        error_message.pack()
    else:
        c_service = "Service: " + list[(current-1)][0]  # gets the previous valid details
        c_username = "Username: " + list[(current-1)][1]
        c_password = "Password: " + list[(current-1)][2]
        ctk.CTkButton(frame, text="Back", command=lambda:back_logged_page(id, mst_psw), width = 10, height = 30).place(x= 10, y =10)  # back button
        ctk.CTkLabel(frame, text="Account Details:", font=("", 18)).pack(pady=10, padx=10)  # prints page title
        ctk.CTkLabel(frame, text=c_service).pack(pady=5, padx=10)  # prints the previous valid details
        ctk.CTkLabel(frame, text=c_username).pack(pady=5, padx=10)
        ctk.CTkLabel(frame, text=c_password).pack(pady=5, padx=10)
        ctk.CTkButton(frame, text="Change Password", command=lambda:change_password(id, c_service, c_username, mst_psw)).pack(pady=5, padx=10)  # button to change current viewed details password

        if length >= (current+1):  # if to check if there is a record after this

            ctk.CTkButton(frame, text="Next Record", command=lambda:next_retrieve(list, length, current, error_message, id,mst_psw)).pack(pady=5, padx=10)  # display next record button
        
        if current > 1:  # checks to see if there is a record before this

            ctk.CTkButton(frame, text="Previous Record", command=lambda:previous_retrieve(list, length, current, error_message, id,mst_psw)).pack(pady=5, padx=10)  # display previous record button

# function that allows the user to change a specific records stored password

def change_password(user_id, service, username, master_password):

    clear_frame()  # clear previous pages widgets
    ctk.CTkButton(frame, text="Back", command=lambda:back_logged_page(user_id, master_password), width=10, height=30).place(x= 10, y =10)  # back button
    ctk.CTkLabel(frame, text="Change Password", font=("",18)).pack(pady=10,padx=10)  # title of the page printed
    ctk.CTkLabel(frame, text=service).pack(pady=5, padx=10)  # print the service of the password you want to change
    ctk.CTkLabel(frame, text=username).pack(pady=5, padx=10)  # print the username of the password you want to change
    new_psw = ctk.CTkEntry(frame, placeholder_text="Password")  # entry field for the user to input their new password
    new_psw.pack(pady=5, padx=10)
    ctk.CTkButton(frame, text="Change Password", command=lambda:change_psw(user_id, service, username, new_psw.get(), master_password)).pack(pady=5, padx=10)  # button to change the password in the database

# this function handles changing the password of a reord

def change_psw(user_id, service, username, new_psw, master_password):
    result = False
    result = PasswordManager.change_password(pwordmanager, user_id, service, username, new_psw, master_password)  # change the password in the database if successful return true
    if result:  # if true
        ctk.CTkLabel(frame, text="Password Updated!", text_color = "green").pack()  # print completion message
    else:  # else
        ctk.CTkLabel(frame, text="Password Failed To Update!", text_color = "red").pack()  # print error message

# function to handle generating a password

def generate_password(apasswordmanager, password_entry):

    password = PasswordManager.gen_password(apasswordmanager)  # returns a randomly generated password
    password_entry.delete(0, 'end')  # clear the entry box
    password_entry.insert(0, password)  # put the newly generated password in the entry box
    
# function that takes the user to the password management screen

def back_logged_page(id, password):

    clear_frame()  # clear the widgets of the previous page
    label_text.set("Password Manager")  # set title of page
    ctk.CTkLabel(frame, textvariable=label_text, font=("", 18)).pack(pady=10, padx=10) # print title of the page 
    ctk.CTkButton(frame, text="Log Out", command=lambda:back_to_login_page(error_message),width=10, height=30).place(x= 10, y =10)  # log out button
    ctk.CTkButton(frame, text="Store a password", command=lambda:store_password_page(id, password)).pack(pady=30, padx=10)  # button to take a user to page to store a password
    ctk.CTkButton(frame, text="Retrieve a password", command=lambda:retrieve_password_page(id, password)).pack(pady=30, padx=10)  # button to take a user to page to retrieve password details

# this function logs a user out

def back_to_login_page(error_message):

    clear_frame()  # clears the widgets of the previous page
    ctk.CTkLabel(frame, text="Login:",font=("", 18)).pack(pady=5, padx=10)  # print the page title
    lgn_username = ctk.CTkEntry(frame, placeholder_text="Username")  # entry box for user to input username
    lgn_username.pack(pady=5, padx=10)

    lgn_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*")  # entry box for user to input account password
    lgn_password.pack(pady=5, padx=10)

    ctk.CTkButton(frame, text="Login", command=lambda:login_button_pressed(usermanager, lgn_username.get(), lgn_password.get(), error_message)).pack(pady=5, padx=10)  # button to login a user
    ctk.CTkButton(frame, text="Create an Account", command=lambda:create_account_page(usermanager)).pack(pady=5, padx=10)  # button to take user to create account page
    error_message = ctk.CTkLabel(frame, text="")

# function to clear a page of widgets

def clear_frame():
    for widget in frame.winfo_children():  # for lopp to remove all widgets on the page
        widget.destroy()  # remove current widget


# page that allows the user to create a new account

def create_account_page(ausermanager):

    clear_frame()  # clear all widgets from the previous page
    ctk.CTkLabel(frame, text="Create Account:", font=("", 18)).pack(pady=10, padx=10)  # print page title

    create_acc_username = ctk.CTkEntry(frame, placeholder_text="Username")  # entry for the users account username
    create_acc_username.pack(pady=5, padx=10)

    create_acc_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*")  # entry for the users account password
    create_acc_password.pack(pady=5, padx=10)
    
    create_acc_cfmpassword = ctk.CTkEntry(frame, placeholder_text="Confirm Password", show="*")  # entry for the user to confirm account password
    create_acc_cfmpassword.pack(pady=5, padx=10)

    ctk.CTkButton(frame, text="Create", command=lambda:handle_create_account(ausermanager, create_acc_username.get(), create_acc_password.get(), create_acc_cfmpassword.get(), label_error)).pack(pady=5, padx=10)  # button that handles create the account based on the input data
    ctk.CTkButton(frame, text="Back", command=lambda:back_to_login_page(error_message),width=10,height=30).place(x= 10, y =10)  # back button
    label_error = ctk.CTkLabel(frame, text="")  # error message layout

# function that handles creating a new users account

def handle_create_account(ausermanager, username_entry, password_entry, confirm_password_entry, label_error):
    result = UserManager.createaccount(ausermanager, username_entry, password_entry, confirm_password_entry)  # attempts to create account in database returns true if complete

    if result:  # if account created
        label_error.configure(frame, text="Account Created!", text_color = "green")  # print completion message
        label_error.pack()
    else:  # if account couldnt be created
        label_error.configure(frame, text="Couldn't Create Account!", text_color = "red")  # print error message
        label_error.pack()

ctk.set_appearance_mode("dark")  # set the application to dark mode
ctk.set_default_color_theme("green")  # set application theme to green

database = DatabaseManager("PasswordManagementSystem")  # greate a DatabaseManager instance called PasswordManagementSystem
database.create_user_table()  # create a table to store accounts
database.create_password_table()  # create a table to store passwords
encryption = EncryptionManager()  # create an EncryptionManager instance
pwordmanager = PasswordManager(database, encryption)  # create a PasswordManager instance
usermanager = UserManager(database, pwordmanager, encryption)  # create a UserManager instance

root = ctk.CTk()  # create application
root.title("Password Manager")  # set title of application
root.geometry("720x480")  # set size of application

frame = ctk.CTkFrame(master=root)  # set the frame of the application
frame.pack(pady=20, padx=60, fill="both", expand=True)  # pack the frame into application

label_text = ctk.StringVar()  # create a label string variable

ctk.CTkLabel(frame, text="Login:", font=("", 18)).pack(pady=5)  # print title of login page
lgn_username = ctk.CTkEntry(frame, placeholder_text="Username")  # entry box for user to enter account username
lgn_username.pack(pady=5, padx=10)

lgn_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*")  # entry box for user to enter account password
lgn_password.pack(pady=5, padx=10)

ctk.CTkButton(frame, text="Login", command=lambda:login_button_pressed(usermanager, lgn_username.get(), lgn_password.get(), error_message)).pack(pady=5, padx=10)  # login button to login a user to the system
ctk.CTkButton(frame, text="Create an Account", command=lambda:create_account_page(usermanager)).pack(pady=5, padx=10)  # create account button to take user to page to create a new account
error_message = ctk.CTkLabel(frame, text="")  # error message layout

root.mainloop()  # run the application