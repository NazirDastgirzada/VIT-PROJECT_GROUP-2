import sqlite3
import library_db_operations
from tabulate import tabulate
import random

# ----------------
conn = sqlite3.connect('library.db')
c = conn.cursor()


# Insert data into the user table
# for i in range(15):
#     c.execute(f"INSERT INTO users (username, password) VALUES ('reader{i}', 'password{i}')")


# display all data in table
# c.execute("select * from users")
# rows = c.fetchall()
# columns = [desc[0] for desc in c.description]
# print(tabulate(rows, headers=columns, tablefmt='grid'))

# Print column names
# c.execute("PRAGMA table_info(books)")
# columns = c.fetchall()
# column_names = [column[1] for column in columns]
# print("Column Names:")
# for name in column_names:
#     print(name)

# #------------------------------------------------------------------------------------
# Define genre options
genres = ['Fantasy', 'Action', 'Romance', 'Drama', 'Horror', 'Sci-fi', 'History']

# Get user IDs from the 'users' table
c.execute("SELECT user_id FROM users")
user_ids = [row[0] for row in c.fetchall()]

# Add 20 books to the database
for i in range(1, 21):
    book_title = f"Book{i}"
    author = f"Author{i}"
    pages = random.randint(100, 400)
    genre = random.choice(genres)
    added_by = random.choice(user_ids)

    # Insert the book into the 'books' table
    c.execute("INSERT INTO books (book_title, author, pages, genre, quantity) VALUES (?, ?, ?, ?, ?)",
              (book_title, author, pages, genre, 1))
    
    # Insert the book instance into the 'book_instance' table
    c.execute("INSERT INTO book_instance (book_id, availability, added_by) VALUES (?, ?, ?)",
              (c.lastrowid, 1, added_by))
# --------------------------------------------------------------------------------------------------------


# Func: delete all data from a table
# c.execute("DELETE from book_instance")

# Commit changes and close the connection
conn.commit()
conn.close()
#--------------------

