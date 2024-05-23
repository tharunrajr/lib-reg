import mysql.connector
from datetime import datetime, timedelta

class Library:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='nopassword@26',
            database='LibraryDB'
        )
        self.cursor = self.conn.cursor()

    def add_book(self, title, author):
        query = "INSERT INTO Books (title, author) VALUES (%s, %s)"
        self.cursor.execute(query, (title, author))
        self.conn.commit()
        print(f"Book '{title}' by {author} added to the library.")

    def borrow_book(self, title, borrower, days):
        query = "SELECT id, is_borrowed FROM Books WHERE title = %s"
        self.cursor.execute(query, (title,))
        book = self.cursor.fetchone()
        if book and not book[1]:
            book_id = book[0]
            due_date = datetime.now().date() + timedelta(days=days)
            borrow_query = "INSERT INTO BorrowRecords (book_id, borrower, borrow_date, due_date) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(borrow_query, (book_id, borrower, datetime.now().date(), due_date))
            update_query = "UPDATE Books SET is_borrowed = %s WHERE id = %s"
            self.cursor.execute(update_query, (True, book_id))
            self.conn.commit()
            print(f"{borrower} borrowed '{title}'. It is due on {due_date}.")
        elif book:
            print(f"The book '{title}' is already borrowed.")
        else:
            print(f"The book '{title}' is not available in the library.")

    def return_book(self, title):
        query = "SELECT id FROM Books WHERE title = %s"
        self.cursor.execute(query, (title,))
        book = self.cursor.fetchone()
        if book:
            book_id = book[0]
            update_query = "UPDATE Books SET is_borrowed = %s WHERE id = %s"
            delete_query = "DELETE FROM BorrowRecords WHERE book_id = %s"
            self.cursor.execute(update_query, (False, book_id))
            self.cursor.execute(delete_query, (book_id,))
            self.conn.commit()
            print(f"The book '{title}' has been returned.")
        else:
            print(f"The book '{title}' is not currently borrowed.")

    def check_borrowed_books(self):
        query = """
        SELECT Books.title, Books.author, BorrowRecords.borrower, BorrowRecords.due_date
        FROM Books
        JOIN BorrowRecords ON Books.id = BorrowRecords.book_id
        WHERE Books.is_borrowed = TRUE
        """
        self.cursor.execute(query)
        borrowed_books = self.cursor.fetchall()
        if borrowed_books:
            print("Borrowed Books:")
            for book in borrowed_books:
                print(f"'{book[0]}' by {book[1]}, borrowed by {book[2]}, due on {book[3]}.")
        else:
            print("No books are currently borrowed.")

    def count_borrowed_books(self):
        query = "SELECT COUNT(*) FROM Books WHERE is_borrowed = TRUE"
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        return count

    def close(self):
        self.cursor.close()
        self.conn.close()

library = Library()
library.add_book("The Great Gatsby", "F. Scott Fitzgerald")
library.add_book("To Kill a Mockingbird", "Harper Lee")
library.add_book("1984", "George Orwell")

library.borrow_book("1984", "Alice", 14)
library.borrow_book("The Great Gatsby", "Bob", 7)

library.check_borrowed_books()
print(f"Total borrowed books: {library.count_borrowed_books()}")

library.return_book("1984")
library.check_borrowed_books()
print(f"Total borrowed books: {library.count_borrowed_books()}")

library.close()
