import library_db_operations as dbo
import sqlite3

# Func: to register a new user
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

# Func: for a user to sign in
def user_sign_in(username, password):
    try:
        user = dbo.db_fetch_user(username=username)
        if user and user[0][3] == password:
            user_id = user[0][0]
            if dbo.db_user_signed_in(user_id):
                print(f"User {username} is already signed in.")
                return True
            else:
                dbo.db_session_start(user_id)
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
# Func: for a user to sign out
def user_sign_out(username):
    try:
        if dbo.db_user_signed_in(username):  # Check if the user is signed in
            user = dbo.db_fetch_user(username=username)
            if user:
                user_id = user[0][0]
                dbo.db_session_end(user_id)
                print(f"Goodbye, {username}! You have been signed out.")
                return True
            else:
                print("User not found.")
                return False
        else:
            print("You are not signed in.")  # Inform the user they need to sign in
            return False
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
        return False
    except Exception as e:
        print(f"An error occurred during sign-out: {str(e)}")
        return False
    
# ============================================================
#Func: add a new book to the library
def add_book(book_title, author, pages, genre_names, quantity_added, added_by):
    try:
        if dbo.db_user_signed_in(added_by):  # Check if the user is signed in
            message = dbo.db_book_insert(book_title, author, pages, genre_names, quantity_added, added_by)
            print(message)
        else:
            print("Please sign in to add a book.")
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
        return False
    except Exception as e:
        print(f"Error adding book '{book_title}': {str(e)}")

# =================================================================
#Func: search books by title, author, genres and date_added
        # decide the number of results that you want to see
        # pick the order in which you wish your results to appear in 
def search_books(user_id, book_title=None, author=None, genres=None, date_added=None, limit=None, order_by=None, order_dir="ASC"):
    try:
        if not dbo.db_user_signed_in(user_id):
            print("Please sign in to search for books.")
            return None

        books = dbo.db_search_books(book_title, author, genres, date_added, limit, order_by, order_dir)
        return books
    except Exception as e:
        print(f"Error searching for books: {str(e)}")
        return None

# Function to handle borrowing a book
def borrow_book(user_id, book_id):
    try:
        if dbo.db_user_signed_in(user_id):  # Check if the user is signed in
            dbo.db_book_borrow(user_id, book_id)
            print("Book borrowed successfully!")
        else:
            print("Please sign in to borrow a book.")
    except Exception as e:
        print(f"Error borrowing book: {str(e)}")

# Function to handle returning a book
def return_book(user_id, book_id):
    try:
        if dbo.db_user_signed_in(user_id):  
            dbo.db_book_return(user_id, book_id)
            print("Book returned successfully!")
        else:
            print("Please sign in to return books.")
    except Exception as e:
        print(f"Error returning book: {str(e)}")

# Function to handle marking a book as read
def mark_book_read(user_id, book_id):
    try:
        if dbo.db_user_signed_in(user_id):  
            dbo.db_book_read(user_id, book_id)
            print("Book marked as read successfully!")
        else:
            print("Please sign in to mark books as read.")
    except Exception as e:
        print(f"Error marking book as read: {str(e)}")

# Function to handle marking a book as favorite
def mark_book_favorite(user_id, book_id):
    try:
        if dbo.db_user_signed_in(user_id):  
            dbo.db_book_favorite(user_id, book_id)
            print("Book marked as favorite successfully!")
        else:
            print("Please sign in to mark books as favorite.")
    except Exception as e:
        print(f"Error marking book as favorite: {str(e)}")
