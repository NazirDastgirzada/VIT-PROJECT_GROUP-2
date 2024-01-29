import sqlite3
from tabulate import tabulate
# ----------------
conn = sqlite3.connect('library.db')
c = conn.cursor()
# Insert data into the user table
# for i in range(2):
#     c.execute(f"INSERT INTO users (username, password) VALUES ('reader{i}', 'goodpass{i}')")


# c.execute("INSERT INTO users VALUES (3, user3, pass3)")
# user = "user3"
# password = "pass3"
# c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, password))


# c.execute("INSERT INTO users (username, password) VALUES ('john_doen', 'password1234')")


# display all data in table
# c.execute("select * from users")
# rows = c.fetchall()
# columns = [desc[0] for desc in c.description]
# print(tabulate(rows, headers=columns, tablefmt='grid'))


c.execute("PRAGMA table_info(books)")
columns = c.fetchall()
column_names = [column[1] for column in columns]
# Print column names
print("Column Names:")
for name in column_names:
    print(name)

# existing_books = c.execute("SELECT * FROM books WHERE book_title = 'book2';")
# c.fetchone()
# book_id = existing_books[0][0] 

# Commit changes and close the connection
conn.commit()
conn.close()
#--------------------

