import sqlite3
import datetime
import bcrypt

# db connection function
def db_connection():
    connection = sqlite3.connect('library.db')
    return connection

# function: sign-up
user = "osamah"
password = "whatever"
def sign_up(username: str, password: str):
    connection = db_connection()
    cursor = connection.cursor()
    # cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
    connection.commit()
    print("User signed up successfully!")
    print(username)
    print(password)
    connection.close()

sign_up(user,password)



# function: sign in

# finction: sign out

# fucntion: add book

# function: borrow book

# function: return Book

# function: mark Read

# function: favorite book

# function: my books

# function: statistics
