import sqlite3
import typer
from rich.console import console
from typing import Optional
from datetime import datetime

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

@app.command("sign_up")
def sign_up(user_name: str, password: str):
    """Sign up a new user."""
   
    cursor.execute("SELECT * FROM user WHERE user_name = ?", (user_name,))
    existing_user = cursor.fetchone()
    if existing_user:
        typer.echo("Error: Username already in use. Please choose another username.")
        return

   
    cursor.execute("INSERT INTO user (user_name, password) VALUES (?, ?)", (user_name, password))
    conn.commit()
    typer.echo(f"User {user_name} signed up successfully!")

@app.command("sign_in")
def sign_in(user_name: str, password: str):
    """Sign in a user."""
    cursor.execute("SELECT * FROM user WHERE user_name = ? AND password = ?", (user_name, password))
    user = cursor.fetchone()
    if user:
        typer.echo(f"Welcome back, {user_name}!")
    else:
        typer.echo("Error: Invalid username or password.")

@app.command("added_book")
def added_book(book_id, name, genre, username):
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO books (title, genre, date_added, username) VALUES (?, ?, ?, ?)', (title, genre, date_added, username))
conn.commit()

        