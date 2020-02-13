from library.patron import Patron
from library.library_db_interface import Library_DB
from library.ext_api_interface import Books_API

class Library:

    def __init__(self):
        self.db = Library_DB()
        self.api = Books_API()

    ############################################################################
    ################################ API METHODS ###############################
    ############################################################################

    def is_ebook(self, book):
        ebooks = self.api.get_ebooks(book)
        book = book.lower()
        for ebook in ebooks:
            if book == ebook['title'].lower():
                return True
        return False

    def get_ebooks_count(self, book):
        ebooks = self.api.get_ebooks(book)
        ebook_count = 0
        for ebook in ebooks:
            ebook_count += ebook['ebook_count']
        return ebook_count

    def is_book_by_author(self, author, book):
        results = self.api.books_by_author(author)
        for result in results:
            if book.lower() == result.lower():
                return True
        return False

    def get_languages_for_book(self, book):
        books_info = self.api.get_book_info(book)
        lang_set = set()
        for book in books_info:
            if 'language' in book:
                lang_set.update(book['language'])
        return lang_set

    ############################################################################
    ################################# DB METHODS ###############################
    ############################################################################

    def register_patron(self, fname, lname, age, memberID):
        patron = Patron(fname, lname, age, memberID)
        return self.db.insert_patron(patron)

    def is_patron_registered(self, patron):
        reg_patron = self.db.retrieve_patron(patron.get_memberID())
        if reg_patron:
            return True
        return False

    def borrow_book(self, book, patron):
        patron.add_borrowed_book(book.lower())
        self.db.update_patron(patron)

    def return_borrowed_book(self, book, patron):
        patron.return_borrowed_book(book.lower())
        self.db.update_patron(patron)

    def is_book_borrowed(self, book, patron):
        borrowed_books = patron.get_borrowed_books()
        return book.lower() in borrowed_books
