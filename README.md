Library Book Register Record System
Overview
The Library Book Register Record System is a Python-based application designed to manage a library's book inventory and borrowing records. It utilizes SQLite, a lightweight and self-contained SQL database engine, to store and retrieve data. The system provides functionalities for adding, removing, displaying, searching, borrowing, and returning books, as well as checking borrowed books by users. This ensures efficient management of library resources and tracking of borrowed books.

Features
Add a Book:

Functionality: Allows librarians to add new books to the library database.
Input: Book title, author, and ISBN.
Process: Inserts the book details into the books table.
Output: Confirmation message indicating the book has been added.
Remove a Book:

Functionality: Enables librarians to remove books from the library database.
Input: ISBN of the book.
Process: Deletes the book from the books table and any related borrowing records from the borrowed_books table.
Output: Confirmation message indicating the book has been removed.
Display All Books:

Functionality: Displays all the books currently in the library database.
Process: Fetches and lists all books from the books table.
Output: List of books with ISBN, title, and author.
Search for a Book:

Functionality: Allows users to search for books by title.
Input: Book title (or part of it).
Process: Searches the books table using a LIKE query to match titles.
Output: List of matching books with ISBN, title, and author.
Borrow a Book:

Functionality: Enables users to borrow books from the library.
Input: ISBN of the book and user name.
Process: Checks if the book is available, then inserts a borrowing record into the borrowed_books table with a due date.
Output: Confirmation message with the book title and due date.
Return a Book:

Functionality: Allows users to return borrowed books.
Input: ISBN of the book and user name.
Process: Deletes the corresponding record from the borrowed_books table.
Output: Confirmation message indicating the book has been returned.
Check Books Taken by a User:

Functionality: Lists all books currently borrowed by a specific user.
Input: User name.
Process: Fetches and lists all books borrowed by the user from the borrowed_books table.
Output: List of borrowed books with ISBN, title, and due date.
Exit:

Functionality: Exits the application.
Database Schema
Books Table (books):

Columns:
isbn: TEXT PRIMARY KEY
title: TEXT NOT NULL
author: TEXT NOT NULL
Borrowed Books Table (borrowed_books):

Columns:
isbn: TEXT PRIMARY KEY
user_name: TEXT NOT NULL
due_date: TEXT NOT NULL
Foreign Key: isbn references books(isbn)
Implementation
The system is implemented in Python and uses the sqlite3 library for database operations.
The main functionalities are encapsulated within the Library class.
The main function provides a user-friendly command-line interface for interacting with the library system.
Usage
Run the script using Python:
sh
Copy code
python library_system.py
Follow the on-screen menu to perform various operations.
This project aims to provide a simple yet effective solution for library management, ensuring that librarians can easily manage book inventories and track borrowed books.
