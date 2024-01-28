import sqlite3

def get_connection(): 
    return sqlite3.connect('library.db')


conn = get_connection()
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    author TEXT,
    pages INTEGER,
    genre TEXT,
    quantity INTEGER
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS book_instance (
    instance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    availability INTEGER,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    added_by INTEGER,
    FOREIGN KEY (book_id) REFERENCES book(book_id),
    FOREIGN KEY (added_by) REFERENCES user(user_id)
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS borrowed_books (
    borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_instance_id INTEGER,
    borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (book_instance_id) REFERENCES book_instance(instance_id)
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS read_books (
    read_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    read_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id)
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS favorite_books (
    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    favorite_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id)
    )""")

conn.commit()
conn.close()
