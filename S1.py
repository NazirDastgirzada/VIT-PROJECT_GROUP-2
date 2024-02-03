import sqlite3
from datetime import datetime
import library_db_operations as dbo
import uuid
import json
import os
import random
import library_functions as lf

# JSON file path to store session tokens
SESSION_FILE_PATH = 'session_tokens.json'

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the filename
SESSION_FILE_NAME = 'session_tokens.json'

# Construct the full file path
SESSION_FILE_PATH = os.path.join(current_directory, SESSION_FILE_NAME)

def load_session_tokens():
    try:
        with open(SESSION_FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty file
        with open(SESSION_FILE_PATH, 'w') as f:
            json.dump({}, f)  # Dump an empty dictionary to the file
        return {}  # Return an empty dictionary

    
# Save session tokens to the JSON file
def save_session_tokens(session_tokens):
    with open(SESSION_FILE_PATH, 'w') as f:
        json.dump(session_tokens, f)

# Function to check if a session token is valid
def is_valid_session(session_token):
    session_tokens = load_session_tokens()
    return session_token in session_tokens


def user_sign_in(username, password):
    try:
        # Check if the user credentials are correct
        if dbo.db_authenticate_user(username=username, password=password):
            user = dbo.db_user_internal_fetch(username=username)
            user_id = user[0][0]
            
            # Generate a unique session token
            session_token = str(uuid.uuid4())
            
            # Store the session token in the JSON file
            session_tokens = load_session_tokens()
            session_tokens[session_token] = user_id
            save_session_tokens(session_tokens)
            
            # Insert a new session record for the user
            dbo.db_session_start(user_id, session_token)
            return session_token
        else:
            print("Invalid username or password.")
            return None
    except Exception as e:
        print(f"An error occurred during sign-in: {str(e)}")
        return None
    
"""=========================="""
# Function to perform activities requiring sign-in
def perform_activity(session_token):
    if is_valid_session(session_token):
        # Proceed with the activity
        print("Activity performed successfully.")
    else:
        print("Invalid session token. Please sign in again.")
"""=========================="""  
def check_existing_session(username):
    """
    Check if the user has an active session and return the session token if available.
    If the user is not signed in, return None.
    """
    try:
        # Fetch the session token for the given username
        session_token = dbo.db_get_session_token(username)
        return session_token
    except Exception as e:
        print(f"Error while checking existing session: {str(e)}")
        return None



def get_random_session_token():
    try:
        with open(SESSION_FILE_PATH, 'r') as f:
            session_tokens = json.load(f)
            if session_tokens:
                random_token = random.choice(list(session_tokens.keys()))
                return random_token
            else:
                print("Session tokens file is empty.")
                return None
    except FileNotFoundError:
        print("Session tokens file not found.")
        return None
    except Exception as e:
        print(f"Error retrieving random session token: {str(e)}")
        return None

# Example usage
random_token = get_random_session_token()
if random_token:
    print("Random session token:", random_token)
else:
    print("Failed to retrieve a random session token.")

lf.add_book("The Great Gatsby", "F. Scott Fitzgerald", 218, "Classic, Fiction", 5)

# username = input("username: ")
# password = input("password: ")
# user_sign_in(username, password)
# if input("would you like to sign out? y/n: ") == "y":
#     print(session_context)
#     keys = list(session_context.keys())
#     user_sign_out(keys[-1])
# else:
#     "Great"
# user_sign_in(username, password)
# print(session_context.keys())
# print(session_context.values())

# print(session_context.keys())
# print(session_context.values())
# user_sign_in(username, password)
# session_token = "ce48d029-9beb-41cd-87e8-f9f77a5b7029"
# user_sign_out(session_token)
# keys = list(session_context.keys())
# values = list(session_context.values())
# key=keys[0]
# print(key)


# Function to borrow a book (example of an action that requires authentication)
# def borrow_book(session_token, book_title):
#     user_id = session_context.get(session_token)
#     if user_id:
#         # Your borrowing logic here, using the session token to authenticate
#         print(f"User {user_id} borrowing book '{book_title}' with session token '{session_token}'")
#     else:
#         print("Invalid session token.")

# Example usage
# if __name__ == "__main__":
#     # Simulate sign-ins for multiple users
#     user1_session_token = sign_in_user1("user1", "password1")
#     user2_session_token = sign_in_user1("user2", "password2")

#     # Borrow a book for each user
#     if user1_session_token:
#         borrow_book(user1_session_token, "Book 1 for User 1")
#     else:
#         print("User 1 sign-in failed.")

#     if user2_session_token:
#         borrow_book(user2_session_token, "Book 2 for User 2")
#     else:
#         print("User 2 sign-in failed.")



































# from session_management import Session_User
# import library_db_operations as dbo
# import sqlite3

# def user_sign_in(username, password):
#     # Define the session_user variable inside the function
#     session_user = Session_User()

#     try:
#         # Authenticate the user
#         if dbo.db_authenticate_user(username, password):
#             # If authentication succeeds and the user is not already signed in,
#             # fetch user details from the database
#             user = dbo.db_user_internal_fetch(username=username)
#             user_id = user[0][0]
#             # Check if the user is already signed in
#             if dbo.db_user_signed_in(user_id):
#                 print(f"User {username} is already signed in.")
#                 return True
#             else:
#                 # Start the session in the database
#                 dbo.db_session_start(user_id)
                
#                 # Sign in the user in the session_user object
#                 session_user.session_user_sign_in(username, user_id)
                
#                 print(f"Sign-in successful! Welcome back {user[0][2]}!")
#                 return True
#         else:
#             print("Sign-in failed. Please check your credentials and try again.")
#             return False
#     except sqlite3.Error as e:
#         print(f"Database error occurred: {str(e)}")
#         return False
#     except Exception as e:
#         print(f"An error occurred during sign-in: {str(e)}")
#         return False



# def user_sign_out():
#     try:
#         # Define the session_user variable inside the function
#         session_user = Session_User()

#         # Get the current user's username
#         current_username = session_user.get_current_user()

#         if current_username:
#             # Check if the current user is signed in
#             if session_user.is_user_signed_in():
#                 # Sign out the current user
#                 session_user.session_user_sign_out()
#                 print(f"Goodbye, {current_username}! You have been signed out.")
#                 return True
#             else:
#                 print("You are not signed in.") 
#                 return False
#         else:
#             print("No user is currently signed in.")
#             return False
#     except sqlite3.Error as e:
#         print(f"Database error occurred: {str(e)}")
#         return False
#     except Exception as e:
#         print(f"An error occurred during sign-out: {str(e)}")
#         return False

# username = "majd"
# password = "12344321"
# results = user_sign_in(username,password)
# print(results)