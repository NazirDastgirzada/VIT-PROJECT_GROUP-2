import sqlite3
from datetime import datetime
# allow only public functions to be exported (functions that don't start with _)
__all__ = ['public_function']

# Func: get database connection
def get_connection():
    return sqlite3.connect('library.db')

# Func: execute SELECT queries
def _db_execute_select_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Func: execute INSERT, UPDATE, DELETE queries
def _db_execute_query(query, values=None):
    conn = get_connection()
    cursor = conn.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()





# Func: insert user to database
def db_insert_user(username, password):
    # Check if the username already exists
    existing_users = db_fetch_users_by_username(username)
    if existing_users:
        print("Username already exists. Please choose a different username.")
        return
    # If the username does not exist, insert the new user
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    values = (username, password)
    _db_execute_query(query, values)

# Func: insert book to database
def db_insert_book(book_title, author, pages, genre, quantity, added_by):
    # Check if the book title already exists
    conn = get_connection()
    existing_books = db_fetch_books_by_title(book_title)
    if existing_books:
        book_id = existing_books[0][0]  # Get the book_id of the existing book
        # Insert book instances into the book_instance table
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _ in range(quantity):
            instance_query = "INSERT INTO book_instance (book_id, availability, date_added, added_by) VALUES (?, 1, ?, ?)"
            instance_values = (book_id, date_added, added_by)
            _db_execute_query(instance_query, instance_values)
        # Update the quantity of the book in the books table
        update_query = "UPDATE books SET quantity = quantity + ? WHERE book_id = ?"
        update_values = (quantity, book_id)
        _db_execute_query(update_query, update_values)
        print(f"{quantity} instance(s) of '{book_title}' added to the library.")
    else:
        # Insert the new book into the books table
        query = "INSERT INTO books (book_title, author, pages, genre, quantity) VALUES (?, ?, ?, ?, ?)"
        values = (book_title, author, pages, genre, quantity)
        _db_execute_query(query, values)
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        book_id = c.lastrowid  # Get the ID of the newly inserted book
        # Insert book instances into the book_instance table
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _ in range(quantity):
            instance_query = "INSERT INTO book_instance (book_id, availability, date_added, added_by) VALUES (?, 1, ?, ?)"
            instance_values = (book_id, date_added, added_by)
            _db_execute_query(instance_query, instance_values)
        conn.commit()
        conn.close()
        print(f"{quantity} instance(s) of '{book_title}' were added to the library.")




def db_fetch_users_by_username(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    result = _db_execute_select_query(query)
    return result

def db_fetch_books_by_title(book_title):
    query = f"SELECT * FROM books WHERE book_title = '{book_title}'"
    result = _db_execute_select_query(query)
    return result


query_ = "SELECT * FROM books WHERE name LIKE ?"

# /* func #5: search by author */
# SELECT * FROM book WHERE author LIKE '%search_term%';

# /* func #6-1 search recently-added books */
# SELECT * FROM book ORDER BY date_added DESC LIMIT 5;

# /* func #6-2 search recently added books by genre */
# SELECT * FROM book WHERE genre = 'specified_genre' ORDER BY date_added DESC LIMIT 5;

# /* func #7-1 search most read books: */
# SELECT book.*, COUNT(read_books.read_id) AS read_count 
# FROM book 
# LEFT JOIN read_books ON book_instance.book_id = read_books.book_instance_id 
# GROUP BY book.book_id 
# ORDER BY read_count DESC 
# LIMIT 10;

# /* func #7-1 search most read books by genre: */
# SELECT book.*, COUNT(read_books.read_id) AS read_count 
# FROM book 
# LEFT JOIN read_books ON book_instance.book_id = read_books.book_instance_id 
# WHERE book.genre = 'specified_genre' 
# GROUP BY book.book_id 
# ORDER BY read_count DESC 
# LIMIT 10;

# /* func #8-1 search most favorite books: */
# SELECT book.*, COUNT(favorite_books.favorite_id) AS favorite_count 
# FROM book 
# LEFT JOIN favorite_books ON book_instance.book_id = favorite_books.book_instance_id 
# GROUP BY book.book_id 
# ORDER BY favorite_count DESC 
# LIMIT 10;

# /* func #8-2 search most favorite books by genre: */
# SELECT book.*, COUNT(favorite_books.favorite_id) AS favorite_count 
# FROM book 
# LEFT JOIN favorite_books ON book_instance.book_id = favorite_books.book_instance_id 
# WHERE book.genre = 'specified_genre' 
# GROUP BY book.book_id 
# ORDER BY favorite_count DESC 
# LIMIT 10;

# /* func #9 search most read genres: */
# SELECT book.genre, COUNT(read_books.read_id) AS read_count 
# FROM book 
# LEFT JOIN read_books ON book_instance.book_id = read_books.book_instance_id 
# GROUP BY book.genre 
# ORDER BY read_count DESC 
# LIMIT 5;

# /* func #10 search most read authors: */
# SELECT book.author, COUNT(read_books.read_id) AS read_count 
# FROM book 
# LEFT JOIN read_books ON book_instance.book_id = read_books.book_instance_id 
# GROUP BY book.author 
# ORDER BY read_count DESC 
# LIMIT 3;