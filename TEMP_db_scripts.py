import sqlite3
from library_db_operations import *
from tabulate import tabulate
import random

# ----------------
conn = sqlite3.connect('library.db')
c = conn.cursor()

#------------------------------------------------------------------------------------
# Insert data into the user table
# for i in range(20):
#     c.execute(f"INSERT INTO users (email, username, password) VALUES ('user{i}@email.com','user{i}', 'password{i}')")
#------------------------------------------------------------------------------------
# display all data in table
# c.execute("select * from book_instance")
# rows = c.fetchall()
# columns = [desc[0] for desc in c.description]
# print(tabulate(rows, headers=columns, tablefmt='grid'))
#------------------------------------------------------------------------------------
# Print column names in a table
# c.execute("PRAGMA table_info(books)")
# columns = c.fetchall()
# column_names = [column[1] for column in columns]
# print("Column Names:")
# for name in column_names:
#     print(name)
# --------------------------------------------------------------------------------------------------------
# Define genre options
genres = ['Fantasy', 'Action', 'Romance', 'Drama', 'Horror', 'Sci-fi', 'History']

# Get user IDs from the 'users' table
c.execute("SELECT user_id FROM users ORDER BY user_id")
user_ids = [row[0] for row in c.fetchall()]
print(user_ids)

# Add 20 books to the database
# for i in range(20):
#     book_title = f"Book{i}"
#     author = f"Author{i}"
#     pages = random.randint(100, 400)
#     genre = random.choice(genres)
#     added_by = random.choice(user_ids)

#     # Check if a book with the same title and author already exists
#     c.execute("SELECT book_id, quantity FROM books WHERE book_title = ? AND author = ?", (book_title, author))
#     existing_book = c.fetchone()

#     if existing_book:
#         # Book already exists, increase quantity by 1
#         (book_id, quantity) = existing_book
#         new_quantity = quantity + 1
#         c.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))

#         # Check availability and update if necessary
#         c.execute("SELECT availability FROM book_instance WHERE title_id = ?", (book_id,))
#         availability = c.fetchone()[0]
#         if availability == 0:
#             c.execute("UPDATE book_instance SET availability = 1 WHERE title_id = ?", (book_id,))
#     else:
#         # Book does not exist, insert into books table
#         c.execute("INSERT INTO books (book_title, author, pages, genre, quantity) VALUES (?, ?, ?, ?, ?)",
#                   (book_title, author, pages, genre, 1))
#         conn.commit()  # Commit the transaction to get the book_id

#         # Fetch the book_id for the newly inserted book based on title and author
#         c.execute("SELECT book_id FROM books WHERE book_title = ? AND author = ?", (book_title, author))
#         book_id = c.fetchone()[0]

#     # Insert the book instance into the 'book_instance' table
#     c.execute("INSERT INTO book_instance (title_id, availability, added_by) VALUES (?, ?, ?)",
#               (book_id, 1, added_by))
#     conn.commit()  # Commit the transaction


# Func: delete all data from a table
# c.execute("DELETE from book_instance")

# Commit changes and close the connection
conn.commit()
conn.close()
#--------------------

