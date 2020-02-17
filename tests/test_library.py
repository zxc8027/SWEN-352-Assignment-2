"""
Luis Gutierrez

Tests the library module.
"""
import unittest
from unittest.mock import MagicMock

from library import library


def MockPatronBookList(self, borrowed_books):
  library.Patron.borrowed_books = MagicMock(return_value=borrowed_books)

class test_Library(unittest.TestCase):
  """
  Set up for unit test
  """
  def setUp(self):
    self.CuT = library.Library()

    #Mock Books_API methods (get_ebooks(book), books_by_author(author), get_book_info(book)
    library.Books_API.get_ebooks = MagicMock(return_value = [{"title":"Test title","ebook_count":2}])
    library.Books_API.books_by_author = MagicMock(return_value = ["Book01","Book02","Book03"])
    library.Books_API.get_book_info = MagicMock(return_value = [{"title": "Test title", "publisher": "Test publisher", "language": ["eng","fre","ger"]}])

    #Mock Library_DB methods (insert_patron(), retrieve_patron(), update_patron())
    library.Library_DB.insert_patron = MagicMock(return_value = 1)


  """
  Tests the is_ebook method, with book in ebooks
  """
  def test_is_ebook_success(self):
    self.assertTrue(self.CuT.is_ebook("Test title"),"'Test title' should be in ebooks")

  """
  Tests the is_ebook method, with book not in ebooks
  """
  def test_is_ebook_fail(self):
    self.assertFalse(self.CuT.is_ebook("Title Not In ebooks"), "'Title Not in ebooks' should not be in ebooks")

  """
  Tests the get_ebooks_count method
  """
  def test_get_ebooks_count(self):
    self.assertEqual(self.CuT.get_ebooks_count("Test title"),2,"ebook count should be 2")

  """
  Tests the is_book_by_author method with book on authors book list
  """
  def test_is_book_by_author_success(self):
    self.assertTrue(self.CuT.is_book_by_author("TestAuthor","Book02"), "Book02 should be in author's book list")

  """
  Tests the is_book_by_author method with book not on authors book list
  """
  def test_is_book_by_author_fail(self):
    self.assertFalse(self.CuT.is_book_by_author("TestAuthor","Book04"), "Book04 should not be in author's book list")

  """
  Tests the get_languages_for_book method 
  """
  def test_get_languages_for_book(self):
    self.assertEquals(self.CuT.get_languages_for_book("Test title"),{"eng","fre","ger"},"Book languages should include eng, fre, ger")

  """
  Tests the register_patron method
  """
  def test_register_patron(self):
    self.assertEqual(self.CuT.register_patron("Kevin","Smith",24,1),1,"MemberID should be one")

  """
  Tests the is_patron_registered method true
  """
  def test_is_patron_registered_true(self):
    library.Library_DB.retrieve_patron = MagicMock(return_value=library.Patron("Kevin", "Smith", 24, 1))
    self.assertTrue(self.CuT.is_patron_registered(library.Patron("Kevin", "Smith", 24, 1)))

  """
  Tests the is_patron_registered method false
  """
  def test_is_patron_registered_false(self):
    library.Library_DB.retrieve_patron = MagicMock(return_value=None)
    self.assertFalse(self.CuT.is_patron_registered(library.Patron("Kevin", "Smith", 24, 1)))

  """
  Tests the borrow_book method
  """
  def test_borrow_book(self):
    #library.Patron.borrowed_books = MagicMock(return_value=[])
    #MockPatronBookList(self,[])
    patron = library.Patron("FirstName", "LastName", 24, 1)
    book = "Book01"
    self.CuT.borrow_book(book,patron)
    self.assertEquals(patron.get_borrowed_books(),["book01"])

  """
  Tests the return_borrowed_book method
  """
  def test_return_borrowed_book(self):
    #library.Patron = MagicMock()
    #library.Patron.borrowed_books = ["book01"]
    #library.Patron.get_borrowed_books = ["book01"]
    #library.Patron.borrowed_books = MagicMock(return_value=["book01"])
    #patron = MagicMock()
    #MockPatronBookList(self, ["book01"])
    #mockPatron = MagicMock()
    #mockPatron.add_borrowed_book.return_value = ["book01"]
    patron = library.Patron("FirstName", "LastName", 24, 1)
    book = "Book01"
    self.CuT.borrow_book(book,patron)
    self.CuT.return_borrowed_book(book,patron)
    self.assertEquals(patron.get_borrowed_books(), [])

  """
  Tests the is_book_borrowed with book in patron's borrowed book list
  """
  def test_is_book_borrowed(self):
    patron = library.Patron("FirstName", "LastName", 24, 1)
    borrowed_book = "Book03"
    library.Patron.get_borrowed_books = MagicMock(return_value=["book01","book02","book03"])
    self.assertTrue(self.CuT.is_book_borrowed(borrowed_book,patron),"Book03 should be in Patron's book list")