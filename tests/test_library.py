"""
Luis Gutierrez

Tests the library module.
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
from library.library import Library
from library.patron import Patron
from library import library_db_interface

class test_Library(unittest.TestCase):

  def tearDown(self) -> None:
    self.lib.close_db()
    library_db_interface.os.remove('db.json')

  """
  Tests the is_ebook method, with book in ebooks
  """
  @patch('library.library.Books_API')
  def test_is_ebook_success(self, mockBooksAPI):
    CuT = Library()
    mockBooksAPI_instance = mockBooksAPI.return_value
    mockBooksAPI_instance.get_ebooks.return_value = [{"title":"Title","ebook_count":2}]
    self.assertTrue(CuT.is_ebook("Title"),"'Test title' should be in ebooks")

  """
  Tests the is_ebook method, with book not in ebooks
  """
  @patch('library.library.Books_API')
  def test_is_ebook_fail(self, mockBooksAPI):
    CuT = Library()
    mockBooksAPI_instance = mockBooksAPI.return_value
    mockBooksAPI_instance.get_ebooks.return_value = [{"title": "Title", "ebook_count": 2}]
    self.assertFalse(CuT.is_ebook("Title_Not_In_ebooks"), "'Title_Not_in_ebooks' should not be in ebooks")

  """
  Tests the get_ebooks_count method
  """
  @patch('library.library.Books_API')
  def test_get_ebooks_count(self, mockBooksAPI):
    CuT = Library()
    mockBooksAPI_instance = mockBooksAPI.return_value
    mockBooksAPI_instance.get_ebooks.return_value = [{"title": "Title", "ebook_count": 2}]
    self.assertEqual(CuT.get_ebooks_count("Test title"),2,"ebook count should be 2")

  """
  Tests the is_book_by_author method with book on authors book list
  """
  # Library.Books_API.books_by_author = MagicMock(return_value = ["Book01","Book02","Book03"])
  @patch('library.library.Books_API')
  def test_is_book_by_author_success(self, mockBooksAPI):
    CuT = Library()
    mockBooksAPI_instance = mockBooksAPI.return_value
    mockBooksAPI_instance.books_by_author.return_value = ["Book01","Book02","Book03"]
    self.assertTrue(CuT.is_book_by_author("TestAuthor","Book02"), "Book02 should be in author's book list")

  """
  Tests the is_book_by_author method with book not on authors book list
  """
  @patch('library.library.Books_API')
  def test_is_book_by_author_fail(self, mockBooksAPI):
    CuT = Library()
    mockBooksAPI_instance = mockBooksAPI.return_value
    mockBooksAPI_instance.books_by_author.return_value = ["Book01", "Book02", "Book03"]
    self.assertFalse(CuT.is_book_by_author("TestAuthor","Book04"), "Book04 should not be in author's book list")

  """
  Tests the get_languages_for_book method 
  """
  # Library.Books_API.get_book_info = MagicMock(return_value = [{"title": "Test title", "publisher": "Test publisher", "language": ["eng","fre","ger"]}])
  @patch('library.library.Books_API')
  def test_get_languages_for_book(self, mockBooksAPI):
    CuT = Library()
    mockBooksAPI_instance = mockBooksAPI.return_value
    mockBooksAPI_instance.get_book_info.return_value = [{"title": "Test title", "publisher": "Test publisher", "language": ["eng","fre","ger"]}]
    self.assertEqual(CuT.get_languages_for_book("Test title"),{"eng","fre","ger"},"Book languages should include eng, fre, ger")

  """
  Tests the register_patron method
  """
  @patch('library.library.Library_DB')
  def test_register_patron(self, mockLibraryDB):
    CuT = Library()
    patron_inserted = Patron("Kevin","Smith",24,1)
    mockLibraryDB_instance = mockLibraryDB.return_value
    mockLibraryDB_instance.insert_patron.return_value = patron_inserted.get_memberID()
    self.assertEqual(CuT.register_patron("Kevin","Smith",24,1),1,"MemberID should be one")
    mockLibraryDB_instance.insert_patron.assert_called_once()

  """
  Tests the is_patron_registered method true
  """
  @patch('library.library.Library_DB')
  def test_is_patron_registered_true(self, mockLibraryDB):
    CuT = Library()
    patron = Patron("Kevin", "Smith", 24, 1)
    mockLibraryDB_instance = mockLibraryDB.return_value
    mockLibraryDB_instance.retrieve_patron.return_value = patron
    self.assertTrue(CuT.is_patron_registered(patron))

  """
  Tests the is_patron_registered method false
  """
  @patch('library.library.Library_DB')
  def test_is_patron_registered_false(self, mockLibraryDB):
    CuT = Library()
    patron = Patron("Kevin", "Smith", 24, 1)
    mockLibraryDB_instance = mockLibraryDB.return_value
    mockLibraryDB_instance.retrieve_patron.return_value = None
    self.assertFalse(CuT.is_patron_registered(patron))

  """
  Tests the borrow_book method
  """
  @patch('library.library.Patron')
  @patch('library.library.Library_DB')
  def test_borrow_book(self,mockLibraryDB,mockPatron):
    book = "Book01"
    CuT = Library()
    mockLibraryDB_instance = mockLibraryDB.return_value
    mockPatron_instance = mockPatron.return_value
    CuT.borrow_book(book,mockPatron_instance)
    mockLibraryDB_instance.update_patron.assert_called_once()
    mockPatron_instance.add_borrowed_book.assert_called_once()

  """
  Tests the return_borrowed_book method
  """
  @patch('library.library.Patron')
  @patch('library.library.Library_DB')
  def test_return_borrowed_book(self,mockLibraryDB,mockPatron):
    book = "book01"
    CuT = Library()
    mockLibraryDB_instance = mockLibraryDB.return_value
    mockPatron_instance = mockPatron.return_value
    CuT.return_borrowed_book(book,mockPatron_instance)
    mockLibraryDB_instance.update_patron.assert_called_once()
    mockPatron_instance.return_borrowed_book.assert_called_once()

  """
  Tests the is_book_borrowed with book in patron's borrowed book list
  """
  @patch('library.library.Patron')
  def test_is_book_borrowed(self, mockPatron):
    CuT = Library()
    mockPatron_instance = mockPatron.return_value
    mockPatron_instance.get_borrowed_books.return_value = ["book1","book2","book3"]
    borrowed_book = "Book3"
    self.assertTrue(CuT.is_book_borrowed(borrowed_book,mockPatron_instance),"Book03 should be in Patron's book list")