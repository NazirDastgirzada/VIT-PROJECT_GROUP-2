import sqlite3
from library_db_operations import *
from library_functions import *
from tabulate import tabulate
import random
from faker import Faker
import string



# conn = sqlite3.connect('library.db')
# cursor = conn.cursor()

# # Function to fetch online users
# def get_online_users():
#     cursor.execute("SELECT users.username FROM user_sessions JOIN users ON user_sessions.user_id = users.user_id")
#     online_users = cursor.fetchall()
#     return [user[0] for user in online_users]

# # Function to sign out all online users
# def sign_out_all_online_users():
#     online_users = get_online_users()
#     for user in online_users:
#         user_sign_out(user)

# # Call the function to sign out all online users
# sign_out_all_online_users()

# # Close the database connection
# conn.close()


fake = Faker()
# Connect to the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Function to generate random book titles
def generate_book_title():
    return ' '.join(fake.words(nb=random.randint(1, 3))).title()

# Function to generate random author names
def generate_author_name():
    return fake.name()

# Function to generate random genres
def generate_genres():
    genres = ['Fiction', 'Non-fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Thriller', 'Romance', 'Horror', 'Biography', 'History']
    num_genres = random.randint(1, 3)
    return random.sample(genres, num_genres)

# Function to generate random number of pages
def generate_pages():
    return random.randint(100, 1000)

# Function to generate random user IDs from the database
def get_random_user_id():
    cursor.execute("SELECT user_id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    return random.choice(user_ids)

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

# Add around 200 books to the database
add_books(50)

# Close the database connection
conn.close()

# ==========================================================

# SCENARIO TURN 35 USERS ONLINE
# Connect to the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Function to get a list of (username, password) tuples from the database
def get_user_credentials():
    cursor.execute("SELECT username, password FROM users")
    user_credentials = cursor.fetchall()
    return user_credentials

# Function to randomly select 35 user credentials
def select_random_users():
    user_credentials = get_user_credentials()
    return random.sample(user_credentials, 35)

# Attempt to sign in the randomly selected users
def sign_in_random_users():
    random_users = select_random_users()
    for username, password in random_users:
        user_sign_in(username, password)  # Call the user_sign_in function

# Call the function to sign in random users
# sign_in_random_users()

# Close the database connection
conn.close()


# def add_mock_users(num_users=50):
#     # Connect to the database
#     conn = sqlite3.connect('library.db')
#     cursor = conn.cursor()

#     try:
#         # Generate and insert mock data for users
#         for _ in range(num_users):
#             email = fake.email()
#             username = fake.user_name()
#             password = fake.password()
            
#             # Insert mock user data into the users table
#             cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
#                            (email, username, password))
        
#         # Commit the changes
#         conn.commit()
#         print(f"{num_users} mock users added successfully!")
    
#     except sqlite3.Error as e:
#         # Rollback changes if there's an error
#         conn.rollback()
#         print(f"Error adding mock users: {e}")
    
#     finally:
#         # Close the connection
#         conn.close()

# # Test the function
# add_mock_users()
# ----------------
# conn = sqlite3.connect('library.db')
# c = conn.cursor()
# mail = "mymail@email.com"
# un= "wonder"
# pw="13131414"
# user_sign_up(mail, un, pw)
#------------------------------------------------------------

# add_book("ZEN", "Mui",99 , ["Religion","Theology","Culture"], 4, 3)



#------------------------------------------------------------------------------------
# Insert data into the user table
# for i in range(20):
#     c.execute(f"INSERT INTO users (email, username, password) VALUES ('user{i}@email.com','user{i}', 'password{i}')")
#------------------------------------------------------------------------------------
# display all data in table
# c.execute("select * from users")
# rows = c.fetchall()
# columns = [desc[0] for desc in c.description]
# print(tabulate(rows, headers=columns, tablefmt='grid'))
#------------------------------------------------------------------------------------
# Print column names in a table
# c.execute("PRAGMA table_info(users)")
# columns = c.fetchall()
# column_names = [column[1] for column in columns]
# print("Column Names:")
# for name in column_names:
#     print(name)
# --------------------------------------------------------------------------------------------------------
# add books to the books and book_instance tables

# # Define genre options
# genres = ['Fantasy', 'Action', 'Romance', 'Drama', 'Horror', 'Sci-fi', 'History', 'Theology', 'philosophy','Entertainmainment', 'Sport']

# # Get user IDs from the 'users' table
# c.execute("SELECT user_id FROM users ORDER BY user_id")
# user_ids = [row[0] for row in c.fetchall()]
# print(user_ids)

# # Add 20 books to the database
# for i in range(20):
#     book_title = f"Book{i}"
#     author = f"Author{i}"
#     pages = random.randint(100, 400)
#     genre = random.choice(genres)
#     added_by = random.choice(user_ids)

# # Check if a book with the same title and author already exists
#     c.execute("SELECT book_id, quantity FROM books WHERE book_title = ? AND author = ?", (book_title, author))
#     existing_book = c.fetchone()

#     if existing_book:
#         # Book already exists, increase quantity by 1
#         (book_id, quantity) = existing_book
#         new_quantity = quantity + 1
#         c.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))

#         # Check availability and update if necessary
#         c.execute("SELECT availability FROM book_instance WHERE title_id = ?", (book_id,))
#         availability = c.fetchone()[0]
#         if availability == 0:
#             c.execute("UPDATE book_instance SET availability = 1 WHERE title_id = ?", (book_id,))
#     else:
#         # Book does not exist, insert into books table
#         c.execute("INSERT INTO books (book_title, author, pages, genre, quantity) VALUES (?, ?, ?, ?, ?)",
#                   (book_title, author, pages, genre, 1))
#         conn.commit()  # Commit the transaction to get the book_id

#         # Fetch the book_id for the newly inserted book based on title and author
#         c.execute("SELECT book_id FROM books WHERE book_title = ? AND author = ?", (book_title, author))
#         book_id = c.fetchone()[0]

#     # Insert the book instance into the 'book_instance' table
#     c.execute("INSERT INTO book_instance (title_id, availability, added_by) VALUES (?, ?, ?)",
#               (book_id, 1, added_by))
#     conn.commit()  # Commit the transaction


# Func: delete all data from a table
# c.execute("DELETE from book_instance")

# # Commit changes and close the connection
# conn.commit()
# conn.close()
#--------------------

