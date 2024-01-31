
import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect('library.db')
# --------------------------
# Func: insert user to database
def db_insert_user(email, username, password):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    try:
        # Insert the new user into the database
        query = "INSERT INTO users (email, username, password) VALUES (?, ?, ?)"
        values = (email, username, password)
        cursor.execute(query, values)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
# ------------------------------------------------------------    
# Func: search and fetch user from database
def db_fetch_user(username=None, email=None):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    try:
        if username and email:
            query = "SELECT * FROM users WHERE username = ? OR email = ?"
            params = (username, email)
        elif username:
            query = "SELECT * FROM users WHERE username = ?"
            params = (username,)
        elif email:
            query = "SELECT * FROM users WHERE email = ?"
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
# Function to register a new user
def user_sign_up(email, username, password):
    try:
        # Check if the email already exists
        if dbo.db_fetch_user(email=email):
            print("There is already an account registered with this email address! If you lost your password, please contact us to reset it.")
            return False

        # Check if the username already exists
        if db_fetch_user(username=username):
            print("Username already exists. Please choose a different username.")
            return False

        # Insert the new user into the database
        db_insert_user(email, username, password)
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
        user = db_fetch_user(username=username)
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
# =======================================================


# Func: get database connection
def get_connection():
     return sqlite3.connect('library.db')

def add_book(book_title, author, pages, genre_names, quantity_added, added_by):
    try:
        print(type(added_by))
        message = db_book_insert(book_title, author, pages, genre_names, quantity_added, added_by)
        print(message)
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
        return False
    except Exception as e:
        print(f"Error adding book '{book_title}': {str(e)}")
# -----------------------------
# Func: execute INSERT queries
import sqlite3

def get_connection():
    return sqlite3.connect('library.db')

def db_book_insert(book_title, author, pages, genre_names, quantity_added, added_by):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        existing_books = db_books_fetch(book_title=book_title, author=author)

        if existing_books:
            book_id, current_quantity = existing_books[0][0], existing_books[0][4]
            new_quantity = current_quantity + quantity_added
            cursor.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))
        else:
            cursor.execute("INSERT INTO books (book_title, author, pages, quantity) VALUES (?, ?, ?, ?)", (book_title, author, pages, quantity_added))
            book_id = cursor.lastrowid

            # Split Genres if it contains multiple genres, otherwise treat it as a single genre
            if ', ' in genre_names:
                genre_list = genre_names.split(', ')
            else:
                genre_list = [genre_names]

            genre_ids = []
            for genre_name in genre_list:
                genre_id = _db_genre_fetch_or_create(genre_name, cursor)
                if genre_id:
                    genre_ids.append(genre_id)

            for genre_id in genre_ids:
                db_book_genre_relation_update(book_id, genre_id, cursor)

        _db_book_insert_instances(book_id, quantity_added, added_by, cursor)
        conn.commit()
        return f"{quantity_added} instance(s) of '{book_title}' were added to the library."
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def _db_book_insert_instances(book_id, quantity_added, added_by, cursor):
    try:
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        instance_query = "INSERT INTO book_instance (book_title_id, availability, date_added, added_by) VALUES (?, 1, ?, ?)"
        instance_values = (book_id, date_added, added_by)
        for _ in range(quantity_added):
            cursor.execute(instance_query, instance_values)
    except sqlite3.Error as e:
        print(f"Error inserting book instance: {e}")
# Func: execute SELECT queries
def db_books_fetch(**kwargs):
    conn = get_connection()
    cursor = conn.cursor()

    # Construct the base query
    query = "SELECT * FROM books WHERE "
    conditions = []

    # Build the WHERE clause based on the provided search parameters
    for key, value in kwargs.items():
        conditions.append(f"{key} = ?")

    if conditions:
        query += " AND ".join(conditions)

    # Execute the query with parameters and return the results
    cursor.execute(query, tuple(kwargs.values()))
    rows = cursor.fetchall()

    conn.close()
    return rows

def _db_genre_fetch_or_create(genre_name, cursor):
    query = "SELECT genre_id FROM genres WHERE genre_name = ?"
    cursor.execute(query, (genre_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        try:
            cursor.execute("INSERT INTO genres (genre_name) VALUES (?)", (genre_name,))
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting genre: {e}")

# Func: execute INSERT queries
def db_book_genre_relation_update(book_id, genre_ids, cursor):
    try:
        query = "INSERT INTO book_genres (book_id, genre_id) VALUES (?, ?)"
        if isinstance(genre_ids, list):
            for genre_id in genre_ids:
                cursor.execute(query, (book_id, genre_id))
        else:
            cursor.execute(query, (book_id, genre_ids))
    except sqlite3.Error as e:
        print(f"Error inserting book-genre relation: {e}")

Title = "Brouth to there"
Author = "Bringer"
Page_number = 199
Genres = "Action"
Quantity = 3
Added_by = 1
add_book(Title, Author, Page_number, Genres, Quantity, 1)

















# # Func: get database connection
# def get_connection():
#     return sqlite3.connect('library.db')

# # Func: execute SELECT queries
# def _db_execute_select_query(query, params=None):
#     conn = get_connection()
#     cursor = conn.cursor()
#     if params:
#         cursor.execute(query, params)
#     else:
#         cursor.execute(query)
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# # Func: execute INSERT, UPDATE, DELETE queries
# def _db_execute_query(query, values=None):
#     conn = get_connection()
#     cursor = conn.cursor()
#     if values:
#         cursor.execute(query, values)
#     else:
#         cursor.execute(query)
#     conn.commit()
#     conn.close()


# def add_book(book_title, author, pages, genre_names, quantity_added, added_by):
#     try:
#         message = db_book_insert(book_title, author, pages, genre_names, quantity_added, added_by)
#         print(message)
#     except sqlite3.Error as e:
#         print(f"Database error occurred: {str(e)}")
#         return False
#     except Exception as e:
#         print(f"Error adding book '{book_title}': {str(e)}")

# def db_book_insert(book_title, author, pages, genre_names, quantity_added, added_by):
#     # Check if the book already exists
#     existing_books = db_books_fetch(book_title=book_title, author=author)

#     if existing_books:
#         # Update the quantity of existing book
#         book_id, current_quantity = existing_books[0][0], existing_books[0][4]
#         new_quantity = current_quantity + quantity_added
#         _db_book_update_quantity(book_id, new_quantity)
#     else:
#         # Insert the new book
#         book_id = db_book_new_insert(book_title, author, pages, quantity_added)

#         # Handle genres
#         genre_ids = []
#         for genre_name in genre_names:
#             genre_id = _db_genre_fetch_or_create(genre_name)
#             if genre_id:
#                 genre_ids.append(genre_id)

#         # Associate book with genres
#         for genre_id in genre_ids:
#             db_book_genre_relation_update(book_id, genre_id)

#     # Insert book instances
#     _db_book_insert_instances(book_id, quantity_added, added_by)
#     return f"{quantity_added} instance(s) of '{book_title}' were added to the library."

# def db_book_new_insert(book_title, author, pages, quantity_added):
#     query = "INSERT INTO books (book_title, author, pages, quantity) VALUES (?, ?, ?, ?)"
#     values = (book_title, author, pages, quantity_added)
#     _db_execute_query(query, values)

#     # Retrieve the book_id of the newly inserted book
#     book_id = db_books_fetch(book_title=book_title, author=author)[0][0]
#     return book_id

# def db_books_fetch(**kwargs):
#     # Construct the base query
#     query = "SELECT * FROM books WHERE "
#     conditions = []

#     # Build the WHERE clause based on the provided search parameters
#     for key, value in kwargs.items():
#         conditions.append(f"{key} = ?")

#     if conditions:
#         query += " AND ".join(conditions)

#     # Execute the query and return the results
#     results = _db_execute_select_query(query, tuple(kwargs.values()))

#     # Return None if no records are found
#     if not results:
#         return None
#     else:
#         return results

# def _db_book_update_quantity(book_id, new_quantity):
#     update_query = "UPDATE books SET quantity = ? WHERE book_id = ?"
#     update_values = (new_quantity, book_id)
#     _db_execute_query(update_query, update_values)

# def _db_book_insert_instances(book_id, quantity_added, added_by):
#     date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     instance_query = "INSERT INTO book_instance (book_title_id, availability, date_added, added_by) VALUES (?, 1, ?, ?)"
#     instance_values = (book_id, date_added, added_by)
#     for _ in range(quantity_added):
#         _db_execute_query(instance_query, instance_values)


# def _db_genre_fetch_or_create(genre_name):
#     # Check if the genre already exists
#     query = "SELECT genre_id FROM genres WHERE genre_name = ?"
#     result = _db_execute_select_query(query, (genre_name,))
#     if result:
#         return result[0][0]
#     else:
#         # If the genre doesn't exist, insert it and retrieve its ID
#         insert_query = "INSERT INTO genres (genre_name) VALUES (?)"
#         _db_execute_query(insert_query, (genre_name,))
#         # Retrieve the genre_id of the newly inserted genre
#         genre_id_query = "SELECT genre_id FROM genres WHERE genre_name = ?"
#         genre_id_result = _db_execute_select_query(genre_id_query, (genre_name,))
#         if genre_id_result:
#             return genre_id_result[0][0]
#         else:
#             # If for some reason genre_id cannot be retrieved, return None
#             return None



# def db_book_genre_relation_update(book_id, genre_ids):
#     try:
#         query = "INSERT INTO book_genres (book_id, genre_id) VALUES (?, ?)"
#         if isinstance(genre_ids, list):
#             for genre_id in genre_ids:
#                 _db_execute_query(query, (book_id, genre_id))
#         else:
#             _db_execute_query(query, (book_id, genre_ids))
#     except sqlite3.Error as e:
#         print(f"Error inserting book-genre relation: {e}")


# def db_book_genre_relation_update(book_id, genre_id):
#     query = "INSERT INTO book_genres (book_id, genre_id) VALUES (?, ?)"
#     _db_execute_query(query, (book_id, genre_id))

# add_book("ZEN", "Mui",99 , ["Religion","Theology","Culture"], 4, 1)





# ------------------------------------USER TESTING-----------------------------
# import sqlite3
# from datetime import datetime

# def get_connection():
#     return sqlite3.connect('library.db')

# def add_book(book_title, author, pages, genre, quantity_added, added_by):
#     try:
#         message = db_insert_book(book_title, author, pages, genre, quantity_added, added_by)
#         print(message)
#     except sqlite3.Error as e:
#         print(f"Database error occurred: {str(e)}")
#         return False
#     except Exception as e:
#         print(f"Error adding book '{book_title}': {str(e)}")

# def db_insert_book(book_title, author, pages, genre, quantity_added, added_by):
#     existing_books = db_fetch_books(book_title=book_title, author=author)

#     if existing_books:
#         book_id, current_quantity = existing_books[0][0], existing_books[0][5]
#         new_quantity = current_quantity + quantity_added
#         _update_book_quantity(book_id, new_quantity)
#         _insert_book_instances(book_id, quantity_added, added_by)
#         return f"{quantity_added} instance(s) of '{book_title}' were added to the library."
#     else:
#         book_id = _insert_new_book(book_title, author, pages, genre, quantity_added)
#         _insert_book_instances(book_id, quantity_added, added_by)
#         return f"{quantity_added} instance(s) of '{book_title}' were added to the library."

# def db_fetch_books(**kwargs):
#     # Construct the base query
#     query = "SELECT * FROM books WHERE "
#     conditions = []

#     # Build the WHERE clause based on the provided search parameters
#     for key, value in kwargs.items():
#         conditions.append(f"{key} = '{value}'")

#     if conditions:
#         query += " AND ".join(conditions)

#     # Execute the query and return the results
#     return _db_execute_select_query(query)

# def _update_book_quantity(book_id, new_quantity):
#     update_query = "UPDATE books SET quantity = ? WHERE book_id = ?"
#     update_values = (new_quantity, book_id)
#     _db_execute_query(update_query, update_values)

# def _insert_book_instances(book_id, quantity_added, added_by):
#     date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     for _ in range(quantity_added):
#         instance_query = "INSERT INTO book_instance (book_title_id, availability, date_added, added_by) VALUES (?, 1, ?, ?)"
#         instance_values = (book_id, date_added, added_by)
#         _db_execute_query(instance_query, instance_values)

# def _insert_new_book(book_title, author, pages, genre, quantity_added):
#     query = "INSERT INTO books (book_title, author, pages, genre, quantity) VALUES (?, ?, ?, ?, ?)"
#     values = (book_title, author, pages, genre, quantity_added)
#     _db_execute_query(query, values)
#     return _db_execute_select_query("SELECT last_insert_rowid()")[0][0]


# def _db_execute_select_query(query, params=None):
#     conn = get_connection()
#     cursor = conn.cursor()
#     if params:
#         cursor.execute(query, params)
#     else:
#         cursor.execute(query)
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# # Func: execute INSERT, UPDATE, DELETE queries
# def _db_execute_query(query, values=None):
#     conn = get_connection()
#     cursor = conn.cursor()
#     if values:
#         cursor.execute(query, values)
#     else:
#         cursor.execute(query)
#     conn.commit()
#     conn.close()

