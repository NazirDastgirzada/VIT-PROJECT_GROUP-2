import sqlite3

def get_connection(): 
    return sqlite3.connect('library.db')

conn = get_connection()
c = conn.cursor()

# Users table with constraints on the username and email columns
# The constraints also help in heving both columns become indexed
c.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE CHECK (email LIKE '%@%.%'),
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    CONSTRAINT email_unique UNIQUE (email),
    CONSTRAINT username_unique UNIQUE (username)
)""")

# Books table with composite unique constraint
# The composite constraint helps in having both columns become indexed
c.execute("""CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT NOT NULL,
    author TEXT NOT NULL,
    pages INTEGER,
    quantity INTEGER,
    first_added_date DATETIME DEFAULT CURRENT_TIMESTAMP, -- New column to track the first time a book entered the library
    CONSTRAINT title_author_unique UNIQUE (book_title, author) -- Ensure uniqueness of title and author combination
)""")

# Create the book_instance table
c.execute("""CREATE TABLE IF NOT EXISTS book_inventory (
    copy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    availability INTEGER NOT NULL DEFAULT 1, -- 1 for available, 0 for unavailable
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    added_by INTEGER,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (added_by) REFERENCES users(user_id)
    )""")

# Genres table
c.execute("""CREATE TABLE IF NOT EXISTS genres (
    genre_id INTEGER PRIMARY KEY,
    genre_name TEXT NOT NULL UNIQUE
)""")

# Book_Genres table (for many-to-many relationship between books and genres)
c.execute("""CREATE TABLE IF NOT EXISTS book_genres (
    book_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id),
    PRIMARY KEY (book_id, genre_id)
)""")

# Borrowed Books table
c.execute("""CREATE TABLE IF NOT EXISTS borrowed_books (
    borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
)""")

# Read Books table
c.execute("""CREATE TABLE IF NOT EXISTS read_books (
    read_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    read_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
)""")

# Favorite Books table
c.execute("""CREATE TABLE IF NOT EXISTS favorite_books (
    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    favorite_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
)""")

# Interactions Junction Table (for many-to-many relationship between users and books)
c.execute("""CREATE TABLE IF NOT EXISTS user_book_interactions (
    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    interaction_type TEXT NOT NULL, -- e.g., 'borrowed', 'read', 'favorite'
    interaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS user_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT UNIQUE, -- Unique session token
    sign_in_time DATETIME NOT NULL,
    sign_out_time DATETIME,
    is_active INTEGER DEFAULT 1, -- 1 for active, 0 for inactive
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)""")

# -----------------------------------------
# Define the new column name
# new_column_name = 'title_id'

# # Define the old column name
# old_column_name = 'book_id'

# # Define the SQL statement to rename the column
# sql_query = f"ALTER TABLE book_instance RENAME COLUMN {old_column_name} TO {new_column_name};"
# c.execute(sql_query)
# -----------------------------------------
# Adding a column to an existing table
# sql_query = "ALTER TABLE users ADD COLUMN email TEXT"
# c.execute(sql_query)
# -----------------------------------------
# sql_query= "ALTER TABLE users MODIFY COLUMN email TEXT NOT NULL;"
# c.execute()
# -----------------------------------------
# sql_query = "DROP TABLE users;"
# c.execute(sql_query)
# -----------------------------------------
# Commit changes and close connection
conn.commit()
conn.close()
