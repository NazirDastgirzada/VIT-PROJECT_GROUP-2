import sqlite3
import library_db

# ----------------
conn = library_db.get_connection()
c = conn.cursor()
# Insert data into the user table
# for i in range(5):
# cursor.executemany(f"INSERT INTO users VALUES ('user{i}', 'pass{i}')")

# cursor.execute("INSERT INTO users (username, password) VALUES (zen, abc);")

# display all data in table
c.execute("select * from users")
print(c.fetchall())
# Commit changes and close the connection
conn.commit()
conn.close()
#--------------------

