import typer
import pwinput
import library_functions as lf
from tabulate import tabulate

app = typer.Typer()


# Define the starting screen command
@app.command()
def start():
    typer.echo("Welcome to the Library Program!")
    typer.echo("Choose an option:")
    typer.echo("1. Sign Up")
    typer.echo("2. Sign In")
    typer.echo("3. Donate Book")
    typer.echo("4. Borrow Book")
    typer.echo("5. Return Book")
    typer.echo("6. Mark Book as Read")
    typer.echo("7. Mark Book as Favorite")
    typer.echo("8. Search for Books")
    typer.echo("9. Sign Out")

@app.command()
def sign_up():
    """
    To sign-up please enter your email, username, and password.
    """
    email = typer.prompt("Enter your email address:")
    username = typer.prompt("Enter your username:")
    password = typer.prompt("Enter your password:")
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

@app.command()
def borrow():
    """
    Borrow a book from the library.
    """
    user_id = typer.prompt("Enter your user ID:")
    book_id = typer.prompt("Enter the ID of the book you want to borrow:")
    lf.borrow_book(user_id, book_id)

@app.command()
def return_book():
    """
    Return a book to the library.
    """
    user_id = typer.prompt("Enter your user ID:")
    book_id = typer.prompt("Enter the ID of the book you want to return:")
    lf.return_book(user_id, book_id)

@app.command()
def mark_read():
    """
    Mark a book as read.
    """
    user_id = typer.prompt("Enter your user ID:")
    book_id = typer.prompt("Enter the ID of the book you want to mark as read:")
    lf.mark_book_read(user_id, book_id)

@app.command()
def mark_favorite():
    """
    Mark a book as favorite.
    """
    user_id = typer.prompt("Enter your user ID:")
    book_id = typer.prompt("Enter the ID of the book you want to mark as favorite:")
    lf.mark_book_favorite(user_id, book_id)

@app.command()
def search():
    """
    Search for books in the library database.
    """
    book_title = typer.prompt("Enter book title (leave empty to skip):", default="")
    author = typer.prompt("Enter author (leave empty to skip):", default="")
    genres = typer.prompt("Enter genres (comma-separated, leave empty to skip):", default="")
    limit = typer.prompt("Enter limit for search results (leave empty to skip):", default="")
    order_by = typer.prompt("Enter order by (leave empty to skip):", default="")

    # Search for books based on the provided criteria
    books = lf.search_books(book_title, author, genres, limit, order_by)

    if books:
        # Convert search results to a tabulated format
        headers = ["Title", "Author", "Pages", "Genres"]
        table_data = [[book[1], book[2], book[3], book[5]] for book in books]  # Assuming the order of fields in the search results
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        
        # Print the tabulated search results
        typer.echo(table)
    else:
        typer.echo("No books found matching the criteria.")

app.command("start")


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


