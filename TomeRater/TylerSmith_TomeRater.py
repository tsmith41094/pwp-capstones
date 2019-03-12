class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("User email has been updated.")

    def __repr__(self):
        return "User: {name} \nemail: {email} \nBooks read: {num_of_books}".format(name = self.name, email = self.email, num_of_books = len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.get_email

    def read_book(self, book, rating=None):
        if rating != None:
            if rating >= 0 and rating <= 4:
                self.books[book] = rating
            else:
                print("Invalid Rating")
        else:
            self.books[book] = rating

    def get_average_rating(self):
        total = 0
        number_of_books_rated = 0
        for book in self.books:
            if self.books[book] != None:
                total += self.books[book]
                number_of_books_rated += 1
        return total/number_of_books_rated

class Book:
    def __init__(self, title, isbn, price=None):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("{title}'s ISBN has been updated".format(title = self.title))

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        total = 0
        for rating in self.ratings :
            total += rating
        if len(self.ratings) > 0:
            return total/len(self.ratings)
        else:
            return total

    def __repr__(self):
        return "{title}".format(title = self.title)

    def	__hash__(self):
        return	hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn, price=None):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price=None):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)

class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn, price=None):
        isbns = []
        for book in self.books:
            isbns.append(book.isbn)
        if isbn not in isbns:
            new_book = Book(title, isbn, price)
            self.books[new_book] = 0
            return new_book
        else:
            print("Book already exists with that ISBN!")

    def create_novel(self, title, author, isbn, price=None):
        isbns = []
        for book in self.books:
            isbns.append(book.isbn)
        if isbn not in isbns:
            new_novel = Fiction(title, author, isbn, price)
            self.books[new_novel] = 0
            return new_novel
        else:
            print("Book already exists with that ISBN!")

    def create_non_fiction(self, title, subject, level, isbn, price=None):
        isbns = []
        for book in self.books:
            isbns.append(book.isbn)
        if isbn not in isbns:
            new_non_fiction = Non_Fiction(title, subject, level, isbn, price)
            self.books[new_non_fiction] = 0
            return new_non_fiction
        else:
            print("Book already exists with that ISBN!")

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users:
            user = self.users.get(email, None)
            user.read_book(book, rating)
            if book not in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1
                if rating != None:
                    book.add_rating(rating)
        else:
            print("No user with {email}!".format(email = email))

    def add_user(self, name, email, user_books=None):
        if "@" in email and (email[-4:] == ".com" or email[-4:] == ".edu" or email[-4:] == ".org"):
            if email not in self.users:
                new_user = User(name, email)
                self.users[email] = new_user
                if user_books != None:
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("User already exists!")
        else:
            print("Invalid email!")

    def change_isbn(self, book, isbn):
        temp_value = self.books[book]
        self.books.pop(book, "Invalid book!")
        book.set_isbn(isbn)
        self.books[book] = temp_value

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def print_prices(self):
        for book in self.books:
            if book.price != None:
                print("{}: ${}".format(book.title, book.price))
            else:
                print("{}: Price not available".format(book.title))

    def most_read_book(self):
        highest_count = 0
        most_read = ""
        for book in self.books:
            if self.books[book] > highest_count:
                highest_count = self.books[book]
                most_read = book
        return most_read

    def highest_rated_book(self):
        highest_rating = 0
        top_book = ""
        for book in self.books:
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
                top_book = book
        return top_book

    def most_positive_user(self):
        highest_avg = 0
        most_positive = ""
        for email in self.users:
            avg_rating = self.users[email].get_average_rating()
            if self.users[email].get_average_rating() > highest_avg:
                highest_avg = self.users[email].get_average_rating()
                most_positive = self.users[email].name
        return most_positive

    def get_n_most_read_books(self, n):
        frequencies = []
        top_n_books = []
        for frequency in self.books.values():
            frequencies.append(frequency)
        frequencies.sort(reverse=True)
        top_n = frequencies[:n]
        for number in top_n:
            for book in self.books:
                if self.books[book] == number:
                    top_n_books.append([book, self.books[book]])
        return top_n_books

    def get_n_most_prolific_readers(self, n):
        read_counts = []
        top_n_readers = []
        for reader in self.users.values():
            read_counts.append(len(reader.books))
        read_counts.sort(reverse=True)
        top_n_most_prolific = read_counts[:n]
        for number in top_n_most_prolific:
            for reader in self.users.values():
                if len(reader.books) == number and [reader.name, len(reader.books)] not in top_n_readers:
                    top_n_readers.append([reader.name, len(reader.books)])
        return top_n_readers

    def get_n_most_expensive_books(self, n):
        prices = []
        n_most_expensive_books = []
        for book in self.books:
            if book.price != None:
                prices.append(book.price)
        prices.sort(reverse=True)
        highest_n_prices = prices[:n]
        for price in highest_n_prices:
            for book in self.books:
                if book.price == price and [book.title, book.price] not in n_most_expensive_books:
                    n_most_expensive_books.append([book.title, book.price])
        return n_most_expensive_books

    def get_worth_of_user(self, user_email):
        total = 0
        if user_email in self.users:
            for book in self.users[user_email].books:
                if book.price != None:
                    total += book.price
            return "{} has read ${} worth of books!".format(self.users[user_email].name, total)
        else:
            print("Invalid email!")

    def __eq__(self, other):
        return self.books.keys() == other.books.keys() and self.users.keys() == other.users.keys()

    def __repr__(self):
        users = []
        catalog = []
        for user in self.users.values():
            users.append(user.name)
        for book in self.books:
            catalog.append(book.title)
        return "Users: {} \nCatalog: {}".format(users, catalog)
