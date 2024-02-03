import typer
import pwinput
import library_functions as lf
import session_functions as sf
from tabulate import tabulate

app = typer.Typer()


# Define the starting screen command and set it to invoke automatically
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
def search(available_only: bool = False):
    """
    Search for books in the library database.
    """
    book_title = typer.prompt("Enter book title (leave empty to skip):", default="")
    author = typer.prompt("Enter author (leave empty to skip):", default="")
    genres = typer.prompt("Enter genres (comma-separated, leave empty to skip):", default="")
    limit = typer.prompt("Enter limit for search results (leave empty to skip):", default="")
    order_by = typer.prompt("Enter order by (leave empty to skip):", default="")

    # Search for books based on the provided criteria
    books = lf.search_books(book_title, author, genres, limit, order_by, available_only=available_only)

    if books:
        # Convert search results to a tabulated format
        headers = ["Title", "Author", "Pages", "Genres", "Availability"]
        table_data = [[book[1], book[2], book[3], book[5], book[6]] for book in books] 
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        
        # Print the tabulated search results
        typer.echo(table)
    else:
        typer.echo("No books found matching the criteria.")

@app.command()
def donate_book():
    """
    Donate books to the library.
    """
    # Fetch the session token from wherever it's stored 
    session_token = sf.get_session_token() 
    
    if session_token:
        typer.echo("Please enter the information of the book:")
        book_title = typer.prompt("Title: ")
        author = typer.prompt("Author: ")
        pages = typer.prompt("Page number: ")
        genre_names = typer.prompt("Genre(s): ")
        quantity_added = typer.prompt("Quantity: ")

        lf.add_book(book_title, author, pages, genre_names, quantity_added, session_token)
    else:
        typer.echo("Please sign in to donate a book.")

@app.command()
def borrow_book():
    """
    Borrow a book from the library.
    """
    # Fetch the session token
    session_token = sf.get_session_token()

    if session_token:
        book_id = typer.prompt("Enter the ID of the book you want to borrow: ")
        lf.borrow_book(session_token, book_id)
    else:
        typer.echo("Please sign in to borrow a book.")

@app.command()
def return_book():
    """
    Return a borrowed book to the library.
    """
    # Fetch the session token
    session_token = sf.get_session_token()

    if session_token:
        book_id = typer.prompt("Enter the ID of the book you want to return: ")
        lf.return_book(session_token, book_id)
    else:
        typer.echo("Please sign in to return a book.")

@app.command()
def mark_read():
    """
    Mark a book as read.
    """
    # Fetch the session token
    session_token = sf.get_session_token()

    if session_token:
        book_id = typer.prompt("Enter the ID of the book you want to mark as read: ")
        lf.mark_book_read(session_token, book_id)
    else:
        typer.echo("Please sign in to mark a book as read.")

@app.command()
def mark_favorite():
    """
    Mark a book as favorite.
    """
    # Fetch the session token
    session_token = sf.get_session_token()

    if session_token:
        book_id = typer.prompt("Enter the ID of the book you want to mark as favorite: ")
        lf.mark_book_favorite(session_token, book_id)
    else:
        typer.echo("Please sign in to mark a book as favorite.")

@app.command()
def profile(user_id: int):
    try:
        typer.echo("Retrieving user profile...")
        profile_details = lf.my_profile(user_id)
        if profile_details:
            # Convert profile details to a tabulated format
            headers = ["Attribute", "Value"]
            table_data = [[key.capitalize(), str(value)] for key, value in profile_details.items()]
            table = tabulate(table_data, headers=headers, tablefmt="grid")

            # Print the tabulated profile details
            typer.echo(table)
        else:
            typer.echo("No profile details found for the user.")
    except Exception as e:
        typer.echo(f"Error retrieving profile: {str(e)}")

@app.command()
def display_statistics(user_id: int):
    """
    Display user statistics.
    """
    try:
        typer.echo("Retrieving user statistics...")
        statistics = lf.user_statistics(user_id)
        if statistics:
            headers = ["Statistic", "Value"]
            table_data = [
                ["Books Read", statistics[0]],
                ["Authors Read", statistics[1]],
                ["Genres Read", statistics[2]],
                ["Total Pages Read", statistics[3]]
            ]
            table = tabulate(table_data, headers=headers, tablefmt="grid")
            typer.echo(table)
        else:
            typer.echo("No statistics found for the user.")
    except Exception as e:
        typer.echo(f"Error retrieving statistics: {str(e)}")

@app.command()
def sign_out():
    """
    Sign out of the current session.
    """
    # To be implemented based on the session management system
    session_token = sf.get_session_token() 
    lf.user_sign_out(session_token)
    typer.echo("You have signed out successfully.")


if __name__ == "__main__":
    app()
