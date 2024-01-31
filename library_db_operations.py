import sqlite3
from datetime import datetime


# Func: get database connection
def get_connection():
    return sqlite3.connect('library.db')
# --------------------------
# Func: insert user to database
def db_insert_user(email, username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
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
    conn = get_connection()
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
# ------------------------------------------------------------    
# Func: add book titles to the "books" database
def db_book_insert(book_title, author, pages, genre_names, quantity_added, added_by):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Convert quantity_added and added_by to integers
        quantity_added = int(quantity_added)
        added_by = int(added_by)
        
        existing_books = db_books_fetch(book_title=book_title, author=author)

        if existing_books:
            book_id, current_quantity = existing_books[0][0], existing_books[0][4]
            new_quantity = current_quantity + quantity_added
            cursor.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))
        else:
            cursor.execute("INSERT INTO books (book_title, author, pages, quantity) VALUES (?, ?, ?, ?)", (book_title, author, pages, quantity_added))
            book_id = cursor.lastrowid

            genre_ids = []
            for genre_name in genre_names.split(','):
                genre_id = _db_genre_fetch_or_create(genre_name.strip(), cursor)
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
# ------------------------------------------------------------    
# Func: add book copies to the "book_instance" database
def _db_book_insert_instances(book_id, quantity_added, added_by, cursor):
    try:
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        instance_query = "INSERT INTO book_instance (book_title_id, availability, date_added, added_by) VALUES (?, 1, ?, ?)"
        instance_values = (book_id, date_added, added_by)
        for _ in range(quantity_added):
            cursor.execute(instance_query, instance_values)
    except sqlite3.Error as e:
        print(f"Error inserting book instance: {e}")
# ------------------------------------------------------------    
# Func: search for and fetch books by modular arguments from the database
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
# ----------------------------------------------------------
# Func: check if newly added genres are in the genre database, if not, add them to database
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
# ------------------------------------------------------------    
# Func: add book-genre relationship too "book_genres" database (many to many)
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