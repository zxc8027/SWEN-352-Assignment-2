import re

class InvalidNameException(Exception):
    pass

class Patron:

    def  __init__(self, fname, lname, age, memberID):
        if re.search('\d', fname) or re.search('\d', lname):
            raise InvalidNameException("Name should not contain numbers")
        self.fname = fname
        self.lname = lname
        self.age = age
        self.memberID = memberID
        self.borrowed_books = []

    def add_borrowed_book(self, book):
        book = book.lower()
        if book in self.borrowed_books:
            return
        self.borrowed_books.append(book)

    def get_borrowed_books(self):
        return self.borrowed_books

    def return_borrowed_book(self, book):
        book = book.lower()
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def  __eq__(self, other):
            return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_fname(self):
        return self.fname

    def get_lname(self):
        return self.lname

    def get_age(self):
        return self.age

    def get_memberID(self):
        return self.memberID
