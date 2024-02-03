import library_db_operations as dbo
import session_functions as sf
import sqlite3
import uuid
from datetime import datetime



def fetch_user_id_current():
    # Retrieve the session token for the current user
    session_token = sf.get_session_token()
    
    if session_token:
        # Assuming you have a function to get the user ID associated with the session token
        user_id = sf.get_user_id_from_session(session_token)
        return user_id
    else:
        # Handle the case where there is no session token (user not logged in)
        print("User not logged in.")
        return None
# Func: to register a new user
def user_sign_up(email, username, password):
    try:
        if dbo.db_user_internal_fetch(email=email):
            print("An account with this email already exists.")
            return False

        if dbo.db_user_internal_fetch(username=username):
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

# Func: for a user to sign in [Note: updated to use user sessions]
def user_sign_in(username, password):
    try:
        # Check if the user is already signed in
        existing_session_token = sf.check_existing_session(username)
        if existing_session_token:
            print(f"User {username} is already signed in.")
            return existing_session_token

        # Check if the user credentials are correct
        if dbo.db_authenticate_user(username=username, password=password):
            user = dbo.db_user_internal_fetch(username=username)
            user_id = user[0][0]
            
            # Generate a unique session token
            session_token = str(uuid.uuid4())
            
            # Store the session token in the JSON file
            session_tokens = sf.load_session_tokens()
            session_tokens[session_token] = user_id
            sf.save_session_tokens(session_tokens)
            # Insert a new session record for the user
            dbo.db_session_start(user_id, session_token)
            print(f"Sign-in successful! Welcome back {user[0][2]}!")
            return session_token
        else:
            print("Sign-in failed. Please check your credentials and try again.")
            return None
    except Exception as e:
        print(f"An error occurred during sign-in: {str(e)}")
        return None    


# ------------------------------------------------------------    
# Func: for a user to sign out
# Function to sign out a user and invalidate the session token
def user_sign_out(session_token):
    try:
        # Check if the session token exists in the session management system
        if sf.is_valid_session(session_token):
            # Invalidate the session token in the JSON file
            session_tokens = sf.load_session_tokens()
            session_tokens.pop(session_token, None)
            sf.save_session_tokens(session_tokens)
            # Update the session status in the database
            dbo.db_session_end(session_token)
            print("User signed out successfully.")
        else:
            print("Invalid session token. User may have already signed out or never signed in.")
    except Exception as e:
        print(f"An error occurred during sign-out: {str(e)}")

# ============================================================
#Func: add a new book to the library
def add_book(book_title, author, pages, genre_names, quantity_added, session_token):
    try:
        user_id = sf.get_user_id_from_session(session_token)
        if user_id:
            message = dbo.db_book_insert(book_title, author, pages, genre_names, quantity_added, user_id)
            print(message)
        else:
            print("Invalid session token. Please sign in.")
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
    except Exception as e:
        print(f"Error adding book '{book_title}': {str(e)}")


# =================================================================
#Func: search books by title, author, genres and date_added
        # decide the number of results that you want to see
        # pick the order in which you wish your results to appear in 
def search_books(user_id, book_title=None, author=None, genres=None, date_added=None, limit=None, order_by=None, order_dir="ASC", available_only=False):
    try:
        if not dbo.db_user_signed_in(user_id):
            print("Please sign in to search for books.")
            return None

        books = dbo.db_search_books(book_title, author, genres, date_added, limit, order_by, order_dir, available_only=available_only)
        return books
    except Exception as e:
        print(f"Error searching for books: {str(e)}")
        return None



# Function to handle borrowing a book
def borrow_book(session_token, book_id):
    try:
        user_id = sf.get_user_id_from_session(session_token)
        if user_id:
            borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dbo.db_book_borrow(user_id, book_id, borrow_date)
            print("Book borrowed successfully!")
        else:
            print("Please sign in to borrow a book.")
    except Exception as e:
        print(f"Error borrowing book: {e}")

# Function to handle returning a book
def return_book(user_id, book_id):
    try:
        session_token = sf.get_session_token()
        if session_token:
            if sf.is_valid_session(session_token):
                dbo.db_book_return(user_id, book_id)
                print("Book returned successfully!")
            else:
                print("Invalid session token. Please sign in.")
        else:
            print("Please sign in to return books.")
    except Exception as e:
        print(f"Error returning book: {e}")

# Function to handle marking a book as read
def mark_book_read(user_id, book_id):
    try:
        session_token = sf.get_session_token()
        if session_token:
            if sf.is_valid_session(session_token):
                dbo.db_book_read(user_id, book_id)
                print("Book marked as read successfully!")
            else:
                print("Invalid session token. Please sign in.")
        else:
            print("Please sign in to mark books as read.")
    except Exception as e:
        print(f"Error marking book as read: {e}")


# Function to handle marking a book as favorite
def mark_book_favorite(user_id, book_id):
    try:
        session_token = sf.get_current_session_token()
        if sf.is_valid_session(session_token):
            dbo.db_book_favorite(user_id, book_id)
            print("Book marked as favorite successfully!")
        else:
            print("Please sign in to mark books as favorite.")
    except Exception as e:
        print(f"Error marking book as favorite: {str(e)}")


def my_profile(user_id):
    try:
        if not dbo.db_user_signed_in(user_id):
            print("Please sign in to view your profile.")
            return None

        # Fetch user profile details
        profile_details = dbo.db_my_profile(user_id)

        # Display user profile details
        if profile_details:
            print("Your Profile Details:")
            for key, value in profile_details.items():
                print(f"{key.capitalize()}: {value}")
        else:
            print("No profile details found for the user.")

    except Exception as e:
        print(f"Error retrieving profile: {str(e)}")
        return None
    
# import typer
# from tabulate import tabulate
# import library_db_operations as dbo

def user_statistics(user_id):
    """
    Retrieve and process user statistics.
    """
    try:
        statistics = dbo.db_user_statistics(user_id)
        return statistics

    except Exception as e:
        print(f"Error retrieving user statistics: {str(e)}")
        return None