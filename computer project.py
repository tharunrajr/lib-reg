from datetime import datetime, timedelta

class Library:
    def __init__(self, register_file, borrowing_file):
        self.books = {}
        self.borrowed_books = {}
        self.users = {}
        self.register_file = register_file
        self.borrowing_file = borrowing_file
        self.load_register()
        self.load_borrowing()
    def load_register(self):
        try:
            with open(self.register_file, 'r') as file:
                for line in file:
                    isbn, title, author = line.strip().split(',')
                    self.books[isbn] = {"title": title, "author": author}
        except FileNotFoundError:
            print("Register file not found. Starting with an empty library.")

    def load_borrowing(self):
        try:
            with open(self.borrowing_file, 'r') as file:
                for line in file:
                    user_name, isbn, due_date = line.strip().split(',')
                    self.borrowed_books[isbn] = (user_name, datetime.strptime(due_date, '%Y-%m-%d'))
                    if user_name in self.users:
                        self.users[user_name].append(isbn)
                    else:
                        self.users[user_name] = [isbn]
        except FileNotFoundError:
            print("Borrowing file not found. Starting with no borrowed books.")

    def save_register(self):
        with open(self.register_file, 'w') as file:
            for isbn, book in self.books.items():
                file.write(f"{isbn},{book['title']},{book['author']}\n")

    def save_borrowing(self):
        with open(self.borrowing_file, 'w') as file:
            for isbn, (user_name, due_date) in self.borrowed_books.items():
                file.write(f"{user_name},{isbn},{due_date.strftime('%Y-%m-%d')}\n")

    def add_book(self, title, author, isbn):
        if isbn not in self.books:
            self.books[isbn] = {"title": title, "author": author}
            self.save_register()
            print(f"Book '{title}' by {author} added to the library.")
        else:
            print("Book with the same ISBN already exists in the library.")

    def remove_book(self, isbn):
        if isbn in self.books:
            title = self.books[isbn]["title"]
            del self.books[isbn]
            self.save_register()
            print(f"Book '{title}' removed from the library.")
        else:
            print("Book with given ISBN not found in the library.")

    def display_all_books(self):
        if self.books:
            print("All books in the library:")
            for isbn, book in self.books.items():
                print(f"ISBN: {isbn}, Title: {book['title']}, Author: {book['author']}")
        else:
            print("No books in the library.")

    def search_book(self, title):
        found = False
        for isbn, book in self.books.items():
            if book["title"] == title:
                print(f"Book '{title}' found in the library - ISBN: {isbn}, Author: {book['author']}")
                found = True
        if not found:
            print(f"Book '{title}' not found in the library.")

    def borrow_book(self, isbn, user_name, days=14):
        if isbn in self.books:
            if isbn not in self.borrowed_books:
                due_date = datetime.now() + timedelta(days=days)
                self.borrowed_books[isbn] = (user_name, due_date)
                self.save_borrowing()
                if user_name in self.users:
                    self.users[user_name].append(isbn)
                else:
                    self.users[user_name] = [isbn]
                print(f"Book '{self.books[isbn]['title']}' borrowed by {user_name}.")
                print(f"Return by: {due_date.strftime('%Y-%m-%d')}")
            else:
                print("Book is already borrowed by someone else.")
        else:
            print("Book with given ISBN not found in the library.")

    def return_book(self, isbn, user_name):
        if isbn in self.books:
            if isbn in self.borrowed_books:
                if user_name in self.users and isbn in self.users[user_name]:
                    del self.borrowed_books[isbn]
                    self.users[user_name].remove(isbn)
                    self.save_borrowing()
                    print(f"Book '{self.books[isbn]['title']}' returned by {user_name}.")
                else:
                    print("This book is not borrowed by this user.")
            else:
                print("This book is not borrowed.")
        else:
            print("Book with given ISBN not found in the library.")

    def get_books_taken_by_user(self, user_name):
        if user_name in self.users:
            print(f"{user_name} has borrowed the following books:")
            for isbn in self.users[user_name]:
                print(f"ISBN: {isbn}, Title: {self.books[isbn]['title']}")
        else:
            print(f"{user_name} has not borrowed any books from the library.")

def main():
    library = Library("register.txt", "borrowing.txt")
    while True:
        print("\nLibrary Book Register Record System")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Display all books")
        print("4. Search for a book")
        print("5. Borrow a book")
        print("6. Return a book")
        print("7. Check books taken by a user")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter title of the book: ")
            author = input("Enter author of the book: ")
            isbn = input("Enter ISBN of the book: ")
            library.add_book(title, author, isbn)
        elif choice == "2":
            isbn = input("Enter ISBN of the book to remove: ")
            library.remove_book(isbn)
        elif choice == "3":
            library.display_all_books()
        elif choice == "4":
            title = input("Enter title of the book to search: ")
            library.search_book(title)
        elif choice == "5":
            isbn = input("Enter ISBN of the book to borrow: ")
            user_name = input("Enter your name: ")
            library.borrow_book(isbn, user_name)
        elif choice == "6":
            isbn = input("Enter ISBN of the book to return: ")
            user_name = input("Enter your name: ")
            library.return_book(isbn, user_name)
        elif choice == "7":
            user_name = input("Enter user's name to check their borrowed books: ")
            library.get_books_taken_by_user(user_name)
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
