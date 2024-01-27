import sqlite3


# -----------------
# Connect to the database
connection = sqlite3.connect('library.db')
cursor = connection.cursor()

# Insert data into the user table
# for i in range(5):
#     cursor.executemany(f"INSERT INTO user VALUES ('user{i}', 'pass{i}')")

# cursor.execute("INSERT INTO user VALUES ('user1', 'pass1')")


# display all data in table
cursor.execute("select * From user")

# Commit changes and close the connection
connection.commit()
connection.close()
#--------------------

