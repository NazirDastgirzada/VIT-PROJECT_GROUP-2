import sqlite3
from datetime import datetime

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
def db_insert_user(email, username, password):
    # Check if the username already exists
    existing_users = db_fetch_users_by_username(username)
    if existing_users:
        print("Username already exists. Please choose a different username.")
        return
    # If the username does not exist, insert the new user
    query = "INSERT INTO users (email, username, password) VALUES (?, ?, ?)"
    values = (email, username, password)
    _db_execute_query(query, values)

# Func: insert book to database
def db_insert_book(book_title, author, pages, genre, quantity_added, added_by):
    existing_books = db_fetch_books(book_title=book_title, author=author)

    if existing_books:
        book_id, current_quantity = existing_books[0][0], existing_books[0][5]
        new_quantity = current_quantity + quantity_added
        _update_book_quantity(book_id, new_quantity)
        _insert_book_instances(book_id, quantity_added, added_by)
        return f"{quantity_added} instance(s) of '{book_title}' were added to the library."
    else:
        book_id = _insert_new_book(book_title, author, pages, genre, quantity_added)
        _insert_book_instances(book_id, quantity_added, added_by)
        return f"{quantity_added} instance(s) of '{book_title}' were added to the library."

def _update_book_quantity(book_id, new_quantity):
    update_query = "UPDATE books SET quantity = ? WHERE book_id = ?"
    update_values = (new_quantity, book_id)
    _db_execute_query(update_query, update_values)

def _insert_book_instances(book_id, quantity_added, added_by):
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for _ in range(quantity_added):
        instance_query = "INSERT INTO book_instance (title_id, availability, date_added, added_by) VALUES (?, 1, ?, ?)"
        instance_values = (book_id, date_added, added_by)
        _db_execute_query(instance_query, instance_values)

def _insert_new_book(book_title, author, pages, genre, quantity_added):
    query = "INSERT INTO books (book_title, author, pages, genre, quantity) VALUES (?, ?, ?, ?, ?)"
    values = (book_title, author, pages, genre, quantity_added)
    _db_execute_query(query, values)
    return _db_execute_select_query("SELECT last_insert_rowid()")[0][0]


# Func: fetch users by username
def db_fetch_users_by_username(username):
    query = "SELECT * FROM users WHERE username = ?"
    result = _db_execute_select_query(query, (username,))
    return result

# Func: fetch books by variable parameters
def db_fetch_books(**kwargs):
    # Construct the base query
    query = "SELECT * FROM books WHERE "
    conditions = []

    # Build the WHERE clause based on the provided search parameters
    for key, value in kwargs.items():
        conditions.append(f"{key} = '{value}'")

    if conditions:
        query += " AND ".join(conditions)

    # Execute the query and return the results
    return _db_execute_select_query(query)



# query_ = "SELECT * FROM books WHERE name LIKE ?"

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