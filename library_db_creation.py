import sqlite3

def get_connection(): 
    return sqlite3.connect('library.db')


conn = get_connection()
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT  NOT NULL UNIQUE CHECK (email LIKE '%@%'),
    username TEXT UNIQUE,
    password TEXT
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT,
    author TEXT,
    pages INTEGER,
    genre TEXT,
    quantity INTEGER
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS book_instance (
    book_instance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_id INTEGER,
    availability INTEGER,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    added_by INTEGER,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (added_by) REFERENCES users(user_id)
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS borrowed_books (
    borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_instance_id INTEGER,
    borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_instance_id) REFERENCES book_instance(book_instance_id)
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS read_books (
    read_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    read_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS favorite_books (
    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    favorite_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
    )""")

# -----------------------------------------
# Define the new column name
new_column_name = 'title_id'

# Define the old column name
old_column_name = 'book_id'

# Define the SQL statement to rename the column
sql_query = f"ALTER TABLE book_instance RENAME COLUMN {old_column_name} TO {new_column_name};"
c.execute(sql_query)
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
conn.commit()
conn.close()
