import library_db_operations as dbo
import random

# Function to register a new user
def user_sign_up(email, username, password):
    try:
        # Insert the new user into the database
        dbo.db_insert_user(email, username, password)
        print(f"User '{username}' registered successfully.")
    except Exception as e:
        print(f"Error occurred during user sign-up: {str(e)}")

def user_sign_in(username: str, password: str) -> bool:
    """
    Sign in the user with the provided username and password.
    Returns True if sign-in is successful, False otherwise.
    """
    # Check if the user exists in the database
    user = dbo.db_fetch_users_by_username(username)

    if not user:
        print("User does not exist. Please register first.")
        return False

    user = user[0]
    if user[3] != password:
        print("Incorrect password. Please try again.")
        return False

    print(f"Welcome back, {username}!")
    return True

def add_book(book_title, author, pages, genre, quantity_added, added_by):
    try:
        message = dbo.db_insert_book(book_title, author, pages, genre, quantity_added, added_by)
        print(message)
    except Exception as e:
        print(f"Error adding book '{book_title}': {str(e)}")


# conn = sqlite3.connect('library.db')
# cursor = conn.cursor()

# @app.command("sign_up")
# def sign_up(user_name: str, password: str):
#     """Sign up a new user."""
   
#     cursor.execute("SELECT * FROM user WHERE user_name = ?", (user_name,))
#     existing_user = cursor.fetchone()
#     if existing_user:
#         typer.echo("Error: Username already in use. Please choose another username.")
#         return

   
#     cursor.execute("INSERT INTO user (user_name, password) VALUES (?, ?)", (user_name, password))
#     conn.commit()
#     typer.echo(f"User {user_name} signed up successfully!")

# @app.command("sign_in")
# def sign_in(user_name: str, password: str):
#     """Sign in a user."""
#     cursor.execute("SELECT * FROM user WHERE user_name = ? AND password = ?", (user_name, password))
#     user = cursor.fetchone()
#     if user:
#         typer.echo(f"Welcome back, {user_name}!")
#     else:
#         typer.echo("Error: Invalid username or password.")

# @app.command("added_book")
# def added_book(book_id, name, genre, username):
#     date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     cursor.execute('INSERT INTO books (title, genre, date_added, username) VALUES (?, ?, ?, ?)', (title, genre, date_added, username))
#     conn.commit()

        