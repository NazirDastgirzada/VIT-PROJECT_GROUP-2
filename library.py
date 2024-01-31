import typer
import pwinput
import library_functions as lf

app = typer.Typer(
    short_help="Welcome to the Library Program!"
)

# Define the starting screen command
@app.command()
def start():
    typer.echo("Welcome to the Library Program!")
    typer.echo("Choose an option:")
    typer.echo("1. Sign Up")

@app.command()
def sign_up():
    """
    To sign-up please enter your email, username, and password.
    """
    email = typer.prompt("Enter your email address:")
    username = typer.prompt("Enter your username:")
    password = pwinput.pwinput("Enter your password:")
    lf.user_sign_up(email, username, password)

@app.command()
def sign_in():
    """
    Sign in with the provided username and password.
    """
    username = typer.prompt("Enter your username:")
    password = pwinput.pwinput("Enter your password:")
    lf.user_sign_in(username, password)

@app.command()
def sign_out():
    """
    Sign out of the current session.
    """
    typer.echo("You have signed out successfully.")

@app.command()
def donate_book():
    """
    Donate books to the library.
    """
    typer.echo("Please enter the information of the book:")
    book_title = typer.prompt("Title: ")
    author = typer.prompt("Author: ")
    pages = typer.prompt("Page number: ")
    genre_names = typer.prompt("Genre(s): ")
    quantity_added = typer.prompt("Quantity: ")
    added_by = typer.prompt("Added by: ")  # This will be automatic later
    lf.add_book(book_title, author, pages, genre_names, quantity_added, added_by)

# Add a default command for the application
@app.callback()
def main():
    pass

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


