import library_db_operations as dbo
import sqlite3

# Function to register a new user
def user_sign_up(email, username, password):
    try:
        if dbo.db_fetch_user(email=email):
            print("An account with this email already exists.")
            return False

        if dbo.db_fetch_user(username=username):
            print("Username already exists. Please choose a different one.")
            return False

        dbo.db_insert_user(email, username, password)
        print(f"User '{username}' registered successfully.")
        return True
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
        return False
    except Exception as e:
        print(f"Error occurred during user sign-up: {str(e)}")
        return False
# ------------------------------------------------------------    

# Function to register a new user
def user_sign_in(username, password):
    try:
        user = dbo.db_fetch_user(username=username)
        if user and user[0][3] == password:
            print(f"Sign-in successful! Welcome back {user[0][2]}!")
            return True
        else:
            print("Sign-in failed. Please check your credentials and try again.")
            return False
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
        return False
    except Exception as e:
        print(f"An error occurred during sign-in: {str(e)}")
        return False

# ------------------------------------------------------------    

#Func: Add a new book to the library
def add_book(book_title, author, pages, genre_names, quantity_added, added_by):
    try:
        message = dbo.db_book_insert(book_title, author, pages, genre_names, quantity_added, added_by)
        print(message)
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
        return False
    except Exception as e:
        print(f"Error adding book '{book_title}': {str(e)}")

