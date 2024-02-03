import sqlite3
from library_db_operations import *
from S1 import *
from tabulate import tabulate
import random
from faker import Faker
import string

fake = Faker()

def get_connection():
    return sqlite3.connect('library.db')
"""========================================================"""
"""TESTING THE SIGN UP PROCESS
THE FUNCTION WILL TAKE AN INTEGER
IT WILL THEN SIGN THE NUMBER IT WAS GIVEN OF NEW USERS"""
def add_mock_users(num_users=50):
    # open database connectoin
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Generate and insert mock data for users
        for _ in range(num_users):
            email = fake.email()
            username = fake.user_name()
            password = fake.password()
            
            # Insert mock user data into the users table
            cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                           (email, username, password))
        
        # Commit the changes
        conn.commit()
        print(f"{num_users} mock users added successfully!")
    
    except sqlite3.Error as e:
        # Rollback changes if there's an error
        conn.rollback()
        print(f"Error adding mock users: {e}")
    
    finally:
        # close database connection
        conn.close()
"""--------------------------------"""
"""CALLING THE FUNCTION
UNCOMMENT TO ACTIVATE"""
# Test the function
# add_mock_users()
"""========================================================"""
"""TESTING THE SIGN IN PROCESS
THE FUNCTION WILL SIGN IN '35' RANDOM REGISTERED USERS"""
# Connect to the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Function to get a list of (username, password) tuples from the database
def get_user_credentials():
    cursor.execute("SELECT username, password FROM users")
    user_credentials = cursor.fetchall()
    return user_credentials
"""--------------------------------"""
# Function to randomly select 35 user credentials
def select_random_users():
    user_credentials = get_user_credentials()
    return random.sample(user_credentials, 15)
"""--------------------------------"""
# Attempt to sign in the randomly selected users
def sign_in_random_users():
    random_users = select_random_users()
    for username, password in random_users:
        user_sign_in(username, password)  # Call the user_sign_in function
"""--------------------------------"""
"""CALLING THE FUNCTION
UNCOMMENT TO ACTIVATE"""
# Call the function to sign in random users
sign_in_random_users()

# Close the database connection
conn.close()

"""========================================================"""
"""TESTING SIGN OUT FUNCTION
SIGNING OUT ALL ONLINE USERS"""
# open database connnetion
conn = get_connection()
cursor = conn.cursor()
# Function to fetch online users
def get_online_users():
    cursor.execute("SELECT users.username FROM user_sessions JOIN users ON user_sessions.user_id = users.user_id")
    online_users = cursor.fetchall()
    return [user[0] for user in online_users]
"""-------------------------------"""
# Function to sign out all online users
def sign_out_all_online_users():
    online_users = get_online_users()
    for user in online_users:
        user_sign_out(user)
"""--------------------------------"""
"""CALLING THE FUNCTION
UNCOMMENT TO ACTIVATE"""
# Call the function to sign out all online users
# sign_out_all_online_users()

# close database connection
conn.close()

"""========================================================"""
"""TESTING ADD BOOK PROCESS
THE FUNCTION WILL TAKE AN INTEGER NUMBER
IT WILL THEN ADD THAT NUMBER OF BOOKS WITH RANDOMIZED DATA"""
# open database connectoin
conn = get_connection()
cursor = conn.cursor()
"""--------------------------------"""
# Function to generate random book titles
def generate_book_title():
    return ' '.join(fake.words(nb=random.randint(1, 3))).title()
"""--------------------------------"""
# Function to generate random author names
def generate_author_name():
    return fake.name()
"""--------------------------------"""
# Function to generate random genres
def generate_genres():
    genres = ['Fiction', 'Non-fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Thriller', 'Romance', 'Horror', 'Biography', 'History']
    num_genres = random.randint(1, 3)
    return random.sample(genres, num_genres)
"""--------------------------------"""
# Function to generate random number of pages
def generate_pages():
    return random.randint(100, 1000)
"""--------------------------------"""
# Function to generate random user IDs from the database
def get_random_user_id():
    cursor.execute("SELECT user_id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    return random.choice(user_ids)
"""--------------------------------"""
# Function to add books to the database
def add_books(num_books):
    for _ in range(num_books):
        book_title = generate_book_title()
        author = generate_author_name()
        genres = ', '.join(generate_genres())
        pages = generate_pages()
        added_by = get_random_user_id()
        
        try:
            # Insert the book into the database using the add_book function
            add_book(book_title, author, pages, genres, 1, added_by)
            print(f"Book '{book_title}' by {author} added to the database.")
        except Exception as e:
            print(f"Error adding book '{book_title}': {e}")
"""--------------------------------"""
"""CALLING THE FUNCTION
# UNCOMMENT TO ACTIVATE"""
# Add around 200 books to the database
# add_books(50)

# close database connection
conn.close()

"""=========================================================="""

def db_fetch_user1(username=None, email=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if username and email:
            query = """
                SELECT u.*, 
                       CASE WHEN s.is_active = 1 THEN 'Online' ELSE 'Offline' END AS status
                FROM users u
                LEFT JOIN user_sessions s ON u.user_id = s.user_id
                WHERE username = ? OR email = ?
            """
            params = (username, email)
        elif username:
            query = """
                SELECT u.*, 
                       CASE WHEN s.is_active = 1 THEN 'Online' ELSE 'Offline' END AS status
                FROM users u
                LEFT JOIN user_sessions s ON u.user_id = s.user_id
                WHERE username = ?
            """
            params = (username,)
        elif email:
            query = """
                SELECT u.*, 
                       CASE WHEN s.is_active = 1 THEN 'Online' ELSE 'Offline' END AS status
                FROM users u
                LEFT JOIN user_sessions s ON u.user_id = s.user_id
                WHERE email = ?
            """
            params = (email,)
        else:
            return None

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
        return None
    finally:
        conn.close()


# users = db_fetch_user1(username='umorgan')

# print(users)


def search_users1(username=None, email=None, status=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT u.username, u.email
            FROM users u
            """
        conditions = []
        params = []

        if username:
            conditions.append("u.username = ?")
            params.append(username)
        if email:
            conditions.append("u.email = ?")
            params.append(email)
        if status:
            if status.lower() == 'online':
                query += """
                LEFT JOIN user_sessions s ON u.user_id = s.user_id 
                WHERE s.is_active = 1
                """
            elif status.lower() == 'offline':
                query += """
                LEFT JOIN user_sessions s ON u.user_id = s.user_id 
                WHERE s.is_active = 0 OR s.is_active IS NULL
                """
            # If status is not 'online' or 'offline', ignore status filter

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
        return None
    finally:
        conn.close()


# users = search_users1(username='majd')

# print(users)

# Test the search_users function
# def test_search_users():
#     # Test case 1: Search users by username
#     username = "example_user"
#     users_by_username = search_users(username=username)
#     print("Users found by username:", users_by_username)

#     # Test case 2: Search users by user_id
#     user_id = 1
#     users_by_id = search_users(user_id=user_id)
#     print("Users found by user_id:", users_by_id)

#     # Test case 3: Search users by email
#     email = "example@example.com"
#     users_by_email = search_users(email=email)
#     print("Users found by email:", users_by_email)

# # Execute the function call to test search_users
# users = search_users(username='majd')

# print(users)
        
# results = search_books(genres="Fantasy")
# print(results)