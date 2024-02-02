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
        cursor.execute(query, (email, username, password))
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


def db_session_start(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sign_in_time = datetime.now()
        cursor.execute("INSERT INTO user_sessions (user_id, sign_in_time) VALUES (?, ?)", (user_id, sign_in_time))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error starting session: {str(e)}")

def db_session_end(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sign_out_time = datetime.now()
        cursor.execute("UPDATE user_sessions SET sign_out_time = ?, is_active = 0 WHERE user_id = ? AND is_active = 1", (sign_out_time, user_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error ending session: {str(e)}")

def db_user_signed_in(user_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT is_active FROM user_sessions WHERE user_id = ? AND is_active = 1", (user_id,))
        session = cursor.fetchone()
        return session is not None
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
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
# Func: add book copies to the "book_inventory" database
def _db_book_insert_instances(book_id, quantity_added, added_by, cursor):
    try:
        current_time = datetime.now()
        instances_data = [(book_id, 1, current_time, added_by) for _ in range(quantity_added)]
        cursor.executemany("INSERT INTO book_inventory (book_id, availability, date_added, added_by) VALUES (?, ?, ?, ?)", instances_data)
    except sqlite3.Error as e:
        # Handle the error appropriately, e.g., logging or raising an exception
        print(f"Error inserting book instances: {e}")
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

# Func: borrow-book database queries/actions
def db_book_borrow(user_id, book_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Update book availability to 0 (unavailable) for the borrowed copy
        cursor.execute("UPDATE book_inventory SET availability = 0 WHERE book_id = ? AND availability = 1 LIMIT 1", (book_id,))
        
        # Record the borrow interaction
        db_record_interaction(user_id, book_id, 'borrowed', cursor)

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Func: user-returns-a-book database queries/actions
def db_book_return(user_id, book_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Update book availability to 1 (available) for the returned copy
        cursor.execute("UPDATE book_inventory SET availability = 1 WHERE book_id = ? AND availability = 0", (book_id,))
        
        # Record the return interaction
        db_record_interaction(user_id, book_id, 'returned', cursor)

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Func: user-marks-a-book-as-read database queries/actions
def db_book_read(user_id, book_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Record the read interaction
        db_record_interaction(user_id, book_id, 'read', cursor)

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Func: user-marks-a-book-as-favorite database queries/actions
def db_book_favorite(user_id, book_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Record the favorite interaction
        db_record_interaction(user_id, book_id, 'favorite', cursor)

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Func: any user-book interaction database queries/actions
def db_record_interaction(user_id, book_id, interaction_type, cursor):
    try:
        interaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO user_book_interactions (user_id, book_id, interaction_type, interaction_date) VALUES (?, ?, ?, ?)",
                       (user_id, book_id, interaction_type, interaction_date))
    except sqlite3.Error as e:
        print(f"Error recording interaction: {e}")

import sqlite3

def db_search_books(book_title=None, author=None, genres=None, date_added=None, limit=None, order_by=None, order_dir="ASC"):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Base query
    query = "SELECT b.book_id, b.book_title, b.author, b.pages, b.quantity, " \
            "GROUP_CONCAT(g.genre_name, ', ') AS genres " \
            "FROM books b " \
            "LEFT JOIN book_genres bg ON b.book_id = bg.book_id " \
            "LEFT JOIN genres g ON bg.genre_id = g.genre_id "

    # Constructing WHERE clause
    conditions = []
    params = []

    if book_title:
        conditions.append("b.book_title LIKE ?")
        params.append(f"%{book_title}%")
    if author:
        conditions.append("b.author LIKE ?")
        params.append(f"%{author}%")
    if genres:
        genres_conditions = " OR ".join(["g.genre_name LIKE ?" for _ in genres])
        conditions.append(f"({genres_conditions})")
        params.extend([f"%{genre}%" for genre in genres])
    if date_added:
        conditions.append("date_added = ?")
        params.append(date_added)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Grouping and ordering
    query += " GROUP BY b.book_id"

    # Ordering
    if order_by:
        query += f" ORDER BY {order_by} {order_dir}"

    # Limiting results
    if limit:
        query += f" LIMIT {limit}"

    try:
        cursor.execute(query, params)
        books = cursor.fetchall()
        return books
    except sqlite3.Error as e:
        print(f"Error searching for books: {e}")
        return None
    finally:
        conn.close()
