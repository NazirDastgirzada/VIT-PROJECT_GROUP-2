
import sqlite3
from datetime import datetime

import typer

app = typer.Typer()

# Define the starting screen command as callback and set it to invoke without command
@app.callback(invoke_without_command=True)
def start():
    typer.echo("Welcome to the Library Program!")
    typer.echo("Choose an option:")
    typer.echo("1. Sign Up")
    typer.echo("2. Sign In")
    typer.echo("3. Donate Book")
    typer.echo("4. Borrow Book")
    typer.echo("5. Return Book")
    typer.echo("6. Mark Book as Read")
    typer.echo("7. Mark Book as Favorite")
    typer.echo("8. Search for Books")
    typer.echo("9. Sign Out")

if __name__ == "__main__":
    app()


import sqlite3
import faker
import random

# Initialize Faker generator
fake = faker.Faker()

def add_mock_users(num_users=50):
    # Connect to the database
    conn = sqlite3.connect('library.db')
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
        # Close the connection
        conn.close()

# Test the function
add_mock_users()






# def get_connection():
#     return sqlite3.connect('library.db')
# # --------------------------
# # Func: insert user to database
# def db_insert_user(email, username, password):
#     conn = sqlite3.connect('your_database.db')
#     cursor = conn.cursor()
#     try:
#         # Insert the new user into the database
#         query = "INSERT INTO users (email, username, password) VALUES (?, ?, ?)"
#         values = (email, username, password)
#         cursor.execute(query, values)
#         conn.commit()
#     except sqlite3.Error as e:
#         conn.rollback()
#         raise e
#     finally:
#         conn.close()
# # ------------------------------------------------------------    
# # Func: search and fetch user from database
# def db_fetch_user(username=None, email=None):
#     conn = sqlite3.connect('your_database.db')
#     cursor = conn.cursor()
#     try:
#         if username and email:
#             query = "SELECT * FROM users WHERE username = ? OR email = ?"
#             params = (username, email)
#         elif username:
#             query = "SELECT * FROM users WHERE username = ?"
#             params = (username,)
#         elif email:
#             query = "SELECT * FROM users WHERE email = ?"
#             params = (email,)
#         else:
#             return None

#         cursor.execute(query, params)
#         rows = cursor.fetchall()
#         return rows
#     except sqlite3.Error as e:
#         print(f"Database error occurred: {str(e)}")
#         return None
#     finally:
#         conn.close()
# # Function to register a new user
# def user_sign_up(email, username, password):
#     try:
#         # Check if the email already exists
#         if dbo.db_fetch_user(email=email):
#             print("There is already an account registered with this email address! If you lost your password, please contact us to reset it.")
#             return False

#         # Check if the username already exists
#         if db_fetch_user(username=username):
#             print("Username already exists. Please choose a different username.")
#             return False

#         # Insert the new user into the database
#         db_insert_user(email, username, password)
#         print(f"User '{username}' registered successfully.")
#         return True
#     except sqlite3.Error as e:
#         print(f"Database error occurred: {str(e)}")
#         return False
#     except Exception as e:
#         print(f"Error occurred during user sign-up: {str(e)}")
#         return False
# # ------------------------------------------------------------    
# # Function to register a new user
# def user_sign_in(username, password):
#     try:
#         user = db_fetch_user(username=username)
#         if user and user[0][3] == password:
#             print(f"Sign-in successful! Welcome back {user[0][2]}!")
#             return True
#         else:
#             print("Sign-in failed. Please check your credentials and try again.")
#             return False
#     except sqlite3.Error as e:
#         print(f"Database error occurred: {str(e)}")
#         return False
#     except Exception as e:
#         print(f"An error occurred during sign-in: {str(e)}")
#         return False
# # =======================================================


# # Func: get database connection
# def get_connection():
#      return sqlite3.connect('library.db')





# def add_book(book_title, author, pages, genre_names, quantity_added, added_by):
#     try:
#         print(type(added_by))
#         message = db_book_insert(book_title, author, pages, genre_names, quantity_added, added_by)
#         print(message)
#     except sqlite3.Error as e:
#         print(f"Database error occurred: {str(e)}")
#         return False
#     except Exception as e:
#         print(f"Error adding book '{book_title}': {str(e)}")
# # -----------------------------
# # Func: execute INSERT queries
# Title = "to there"
# Author = "Bringer"
# Page_number = 139
# Genres = "Action, Adventure, Science, Scifi, Geography"
# Quantity = 3
# Added_by = 2
# add_book(Title, Author, Page_number, Genres, Quantity, 1)

# def get_connection():
#     return sqlite3.connect('library.db')


# def db_book_insert(book_title, author, pages, genre_names, quantity_added, added_by):
#     conn = get_connection()
#     cursor = conn.cursor()

#     try:
#         # Convert quantity_added and added_by to integers
#         quantity_added = int(quantity_added)
#         added_by = int(added_by)
        
#         existing_books = db_books_fetch(book_title=book_title, author=author)

#         if existing_books:
#             book_id, current_quantity = existing_books[0][0], existing_books[0][4]
#             new_quantity = current_quantity + quantity_added
#             cursor.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))
#         else:
#             cursor.execute("INSERT INTO books (book_title, author, pages, quantity) VALUES (?, ?, ?, ?)", (book_title, author, pages, quantity_added))
#             book_id = cursor.lastrowid

#             genre_ids = []
#             for genre_name in genre_names.split(','):
#                 genre_id = _db_genre_fetch_or_create(genre_name.strip(), cursor)
#                 if genre_id:
#                     genre_ids.append(genre_id)

#             for genre_id in genre_ids:
#                 db_book_genre_relation_update(book_id, genre_id, cursor)

#         _db_book_insert_instances(book_id, quantity_added, added_by, cursor)
#         conn.commit()
#         return f"{quantity_added} instance(s) of '{book_title}' were added to the library."
#     except sqlite3.Error as e:
#         conn.rollback()
#         raise e
#     finally:
#         conn.close()



# def _db_book_insert_instances(book_id, quantity_added, added_by, cursor):
#     try:
#         date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         instance_query = "INSERT INTO book_instance (book_title_id, availability, date_added, added_by) VALUES (?, 1, ?, ?)"
#         instance_values = (book_id, date_added, added_by)
#         for _ in range(quantity_added):
#             cursor.execute(instance_query, instance_values)
#     except sqlite3.Error as e:
#         print(f"Error inserting book instance: {e}")
# # Func: execute SELECT queries
# def db_books_fetch(**kwargs):
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Construct the base query
#     query = "SELECT * FROM books WHERE "
#     conditions = []

#     # Build the WHERE clause based on the provided search parameters
#     for key, value in kwargs.items():
#         conditions.append(f"{key} = ?")

#     if conditions:
#         query += " AND ".join(conditions)

#     # Execute the query with parameters and return the results
#     cursor.execute(query, tuple(kwargs.values()))
#     rows = cursor.fetchall()

#     conn.close()
#     return rows

# def _db_genre_fetch_or_create(genre_name, cursor):
#     query = "SELECT genre_id FROM genres WHERE genre_name = ?"
#     cursor.execute(query, (genre_name,))
#     result = cursor.fetchone()
#     if result:
#         return result[0]
#     else:
#         try:
#             cursor.execute("INSERT INTO genres (genre_name) VALUES (?)", (genre_name,))
#             return cursor.lastrowid
#         except sqlite3.Error as e:
#             print(f"Error inserting genre: {e}")

# # Func: execute INSERT queries
# def db_book_genre_relation_update(book_id, genre_ids, cursor):
#     try:
#         query = "INSERT INTO book_genres (book_id, genre_id) VALUES (?, ?)"
#         if isinstance(genre_ids, list):
#             for genre_id in genre_ids:
#                 cursor.execute(query, (book_id, genre_id))
#         else:
#             cursor.execute(query, (book_id, genre_ids))
#     except sqlite3.Error as e:
#         print(f"Error inserting book-genre relation: {e}")


# def search_books(book_title=None, author=None, genres=None, limit=None, order_by=None):
#     conn = sqlite3.connect('library.db')
#     cursor = conn.cursor()

#     # Base query
#     query = "SELECT b.book_id, b.book_title, b.author, b.pages, b.quantity, " \
#             "GROUP_CONCAT(g.genre_name, ', ') AS genres " \
#             "FROM books b " \
#             "LEFT JOIN book_genres bg ON b.book_id = bg.book_id " \
#             "LEFT JOIN genres g ON bg.genre_id = g.genre_id "

#     # Constructing WHERE clause
#     conditions = []
#     params = []

#     if book_title:
#         conditions.append("b.book_title LIKE ?")
#         params.append(f"%{book_title}%")
#     if author:
#         conditions.append("b.author LIKE ?")
#         params.append(f"%{author}%")
#     if genres:
#         genres_conditions = " OR ".join(["g.genre_name LIKE ?" for _ in genres])
#         conditions.append(f"({genres_conditions})")
#         params.extend([f"%{genre}%" for genre in genres])

#     if conditions:
#         query += "WHERE " + " AND ".join(conditions)

#     # Grouping
#     query += " GROUP BY b.book_id"

#     # Ordering
#     if order_by:
#         query += f" ORDER BY {order_by}"

#     # Limiting results
#     if limit:
#         query += f" LIMIT {limit}"

#     try:
#         cursor.execute(query, params)
#         books = cursor.fetchall()
#         return books
#     except sqlite3.Error as e:
#         print(f"Error searching for books: {e}")
#         return None
#     finally:
#         conn.close()


# Test case for search_books function
# def test_search_books():
#     from pprint import pprint

#     # Test with different combinations of parameters
#     print("Searching books by title 'Harry Potter':")
#     pprint(search_books(book_title='Harry Potter'))

#     print("\nSearching books by author 'J.K. Rowling':")
#     pprint(search_books(author='J.K. Rowling'))

#     print("\nSearching books by genre 'Fantasy':")
#     pprint(search_books(genres=['Fantasy']))

#     print("\nSearching books by multiple genres:")
#     pprint(search_books(genres=['Fantasy', 'Adventure']))

#     print("\nSearching books with limit and order by pages:")
#     pprint(search_books(limit=5, order_by='pages'))

#     print("\nSearching books with title 'Lord of the Rings' and author 'Tolkien':")
#     pprint(search_books(book_title='Lord of the Rings', author='Tolkien'))

#     print("\nSearching books with genre 'Mystery' and order by quantity:")
#     pprint(search_books(genres=['Mystery'], order_by='quantity'))

# if __name__ == "__main__":
#     test_search_books()


# Title = "Brouth to there"
# Author = "Bringer"
# Page_number = 199
# Genres = "Action"
# Quantity = 3
# Added_by = 1
# add_book(Title, Author, Page_number, Genres, Quantity, 1)