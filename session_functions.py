import sqlite3
from datetime import datetime
import library_db_operations as dbo
import library_functions as lf
import uuid
import json
import os

# Define the file path for session tokens
SESSION_FILE_PATH = 'session_tokens.json'

def load_session_tokens():
    """
    Load session tokens from the JSON file.
    If the file doesn't exist, create an empty one.
    """
    try:
        with open(SESSION_FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_session_tokens(session_tokens):
    """
    Save session tokens to the JSON file.
    """
    try:
        with open(SESSION_FILE_PATH, 'w') as f:
            json.dump(session_tokens, f)
    except Exception as e:
        print(f"Error saving session tokens: {str(e)}")

def is_valid_session(session_token):
    """
    Check if a session token is valid.
    """
    session_tokens = load_session_tokens()
    return session_token in session_tokens

def check_existing_session(username):
    """
    Check if the user has an active session and return the session token if available.
    If the user is not signed in, return None.
    """
    try:
        return dbo.db_get_session_token(username)
    except Exception as e:
        print(f"Error while checking existing session: {str(e)}")
        return None

def get_user_id_from_session(session_token):
    """
    Retrieve the user ID associated with the session token.
    """
    try:
        session_tokens = load_session_tokens()
        return session_tokens.get(session_token)
    except Exception as e:
        print(f"Error retrieving user ID from session: {str(e)}")
        return None

"""TEMPORARY FIX, THE ORIGINAL FUNCTION BELOW AS COMMENT"""
def get_session_token():
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # Fetch the session token associated with the user
        cursor.execute("""SELECT session_token
                FROM user_sessions
                ORDER BY session_id DESC
                LIMIT 1;""")
        
        session_token = cursor.fetchone()

        if session_token:
            return session_token[0]  # Return the session token
        else:
            return None  # User has no active session
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()


# def get_session_token():
    # try:
    #     # Get the directory of the current script
    #     current_directory = os.path.dirname(os.path.abspath(__file__))
    #     # Construct the full file path
    #     session_file_path = os.path.join(current_directory, "session_tokens.json")
    #     session_tokens = {}
    #     with open(session_file_path, 'r') as f:
    #         session_tokens = json.load(f)
    #     user_id = lf.fetch_user_id_current()  # You need to implement this function
    #     session_token = session_tokens.get((str(user_id)))

    #     return session_token
    # except FileNotFoundError:
    #     print("Session tokens file not found.")
    #     return None
    # except Exception as e:
    #     print(f"Error retrieving session token: {str(e)}")
    #     return None