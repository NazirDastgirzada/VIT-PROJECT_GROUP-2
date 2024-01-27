import sqlite3

conn = sqlite3.connect('library.db')

c = conn.cursor()

c.execute("""CREATE TABLE book_instance (
	instance_id integer PRIMARY KEY AUTOINCREMENT,
	book_id integer,
	availability integer
);
""")

c.execute("""CREATE TABLE user (
	user_id integer PRIMARY KEY AUTOINCREMENT,
	username text,
	password text
);""")

c.execute("""CREATE TABLE book (
	book_id integer,
	name text,
	author text,
	pages integer,
	genre text,
	quantity integer,
	date_added datetime,
	added_by integer
);""")

c.execute("""CREATE TABLE borrowed_books (
	borrow_id integer,
	user_id integer,
	book_instance_id integer,
	borrow_date datetime
);""")

c.execute("""CREATE TABLE read_books (
	read_id integer,
	user_id integer,
	book_instance_id integer,
	read_date datetime
);""")

c.execute("""CREATE TABLE favorite_books (
	favorite_id integer PRIMARY KEY AUTOINCREMENT,
	user_id integer,
	book_id integer,
	favorite_date datetime
);""")

conn.commit()
conn.close()
