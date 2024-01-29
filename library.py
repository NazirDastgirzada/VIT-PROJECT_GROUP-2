import typer
import library_functions as lf
app = typer.Typer()

# Define the starting screen command
@app.command()
def start():
    typer.echo("Welcome to the Library Program!")
    typer.echo("Choose an option:")
    typer.echo("1. Sign Up")
    typer.echo("2. Sign In")
    typer.echo("3. Sign Out")
    # typer.echo("4. Add a new book")
    # typer.echo("5. Borrow a book")
    # typer.echo("6. Return a book")
    typer.echo("7. Exit")

@app.command()
def sign_up(email: str, username: str, password: str):
    """
    Sign up a new user with the provided email, username, and password.
    """
    lf.user_sign_up(email, username, password)
    typer.echo(f"User '{username}' registered successfully.")


@app.command()
def sign_in(username: str, password: str):
    """
    Sign in with the provided username and password.
    """
    if lf.user_sign_in(username, password):
        typer.echo("Sign-in successful!")
    else:
        typer.echo("Sign-in failed. Please check your credentials.")

@app.command()
def sign_out():
    """
    Sign out of the current session.
    """
    typer.echo("You have signed out successfully.")

@app.command()
def sign_in(username: str, password: str):
    """
    Sign in with the provided username and password.
    """
    if lf.user_sign_in(username, password):
        typer.echo("Sign-in successful!")
    else:
        typer.echo("Sign-in failed. Please check your credentials.")

@app.command()
def sign_out():
    """
    Sign out of the current session.
    """
    lf.sign_out()
    typer.echo("You have signed out successfully.")


if __name__ == "__main__":
    app()

# # db connection function
# def db_connection():
#     connection = sqlite3.connect('library.db')
#     return connection

# # function: sign-up
# user = "osamah"
# pw = "whatever"
# def sign_up(username: str, password: str):
#     connection = db_connection()
#     cursor = connection.cursor()
#     # cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
#     connection.commit()
#     print("User signed up successfully!")
#     print(username)
#     print(password)
#     connection.close()

# sign_up(user,pw)



# # function: sign in

# # finction: sign out

# # fucntion: add book

# # function: borrow book

# # function: return Book

# # function: mark Read

# # function: favorite book

# # function: my books

# # function: statistics


