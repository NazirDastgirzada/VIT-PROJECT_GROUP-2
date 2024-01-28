import sqlite3


conn = sqlite3.connect('library.db')
cursor = conn.cursor()


# Create the sessions table
cursor.execute('CREATE TABLE IF NOT EXISTS sessions (session_id TEXT, username TEXT)')

# Function for user sign-in
def sign_in(username: str, password: str):
    # Check the validity of the username and password
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    if cursor.fetchone() is not None:
        # Generate a unique session ID
        session_id = generate_session_id()
        
        # Store the session ID and username in the sessions table
        cursor.execute('INSERT INTO sessions VALUES (?, ?)', (session_id, username))
        conn.commit()
        
        print("Sign-in successful. Session ID:", session_id)
    else:
        print("Invalid username or password.")

# Function for user sign-out
def sign_out(session_id):
    # Delete the session ID from the sessions table
    cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
    conn.commit()



def add_book(book_id, author, page, added_by, date_added, genre, quantity,  ):
    # Connect to the database
    conn = sqlite3.connect('library.db')
    
    # Create a cursor
    cursor = conn.cursor()
    
    # Execute INSERT statement to add book data into the table
    cursor.execute("INSERT INTO books (book_id, author, page, added_by, date_added, genre, quantity,) VALUES (?, ?, ?)", (title, author, year))
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()



    

