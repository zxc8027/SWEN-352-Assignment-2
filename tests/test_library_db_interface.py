from unittest.mock import MagicMock
import unittest
from library import library_db_interface
from tests_data import test_library_db_interface


class test_LibraryDB(unittest.TestCase):

    def setUp(self):
        self.lib = library_db_interface.Library_DB()
        library_db_interface.Patron = MagicMock()
        library_db_interface.Patron.add_borrowed_book.return_value = None
        library_db_interface.Patron.get_borrowed_books.return_value = ['Book']
        library_db_interface.Patron.return_borrowed_book.return_value = None
        library_db_interface.Patron.get_fname.return_value = 'First'
        library_db_interface.Patron.get_lname.return_value = 'Last'
        library_db_interface.Patron.get_age.return_value = 14
        library_db_interface.Patron.get_memberID = MagicMock(return_value=123)
        self.p = library_db_interface.Patron

    def tearDown(self) -> None:
        self.lib.close_db()
        library_db_interface.os.remove('db.json')

    """
        test for inserting a patron covering duplicate patron, no person
    """
    def test_insertPatron(self):
        self.assertEqual(None, self.lib.insert_patron(None))
        self.assertEqual(self.lib.get_patron_count(), 0, 'There are not 0 patrons in the database')
        self.lib.insert_patron(self.p)
        self.p.get_memberID.assert_called()
        self.p.get_age.assert_called_once()
        self.p.get_fname.assert_called_once()
        self.p.get_lname.assert_called_once()
        self.assertEqual(self.lib.get_patron_count(), 1, 'There should be 1 patron in the database')
        self.lib.insert_patron(self.p)
        self.p.get_memberID.assert_called()
        self.p.get_age.assert_called()
        self.p.get_fname.assert_called()
        self.p.get_lname.assert_called()
        self.assertEqual(self.lib.get_patron_count(), 1, 'There should be 1 patron in the database')

    """
        testing retrieving patrons getting one, getting 2 of them
    """
    def test_get_all_patrons(self):
        self.lib.insert_patron(self.p)
        self.assertEqual(self.lib.get_patron_count(), 1, 'There should be 1 patron in the database')
        self.p.get_memberID.assert_called()
        self.p.get_age.assert_called_once()
        self.p.get_fname.assert_called_once()
        self.p.get_lname.assert_called_once()
        self.p.get_fname = MagicMock(return_value='Test')
        self.p.get_memberID = MagicMock(return_value=1234)
        self.lib.insert_patron(self.p)
        self.assertEqual(self.lib.get_patron_count(), 2, 'There should be 2 patrons in the database')
        self.assertEqual(test_library_db_interface.EXPECTED, self.lib.get_all_patrons())

    """
        testing updating patrons updating first name and last name,
        testing attempting a none with none
    """
    def test_update_patron(self):
        self.lib.insert_patron(self.p)
        self.assertEqual(self.lib.get_patron_count(), 1, 'There should be 1 patron in the database')
        self.p.get_memberID.assert_called()
        self.p.get_age.assert_called_once()
        self.p.get_fname.assert_called_once()
        self.p.get_lname.assert_called_once()
        self.p.get_fname = MagicMock(return_value='Test')
        self.p.get_lname = MagicMock(return_value='LastName')
        self.lib.update_patron(self.p)
        self.assertEqual(test_library_db_interface.UPDATED, self.lib.get_all_patrons())
        self.assertEqual(self.lib.get_patron_count(), 1, 'There should be 1 patron in the database')
        self.assertEqual(None, self.lib.update_patron(None))

    """
        test retrieve patron existing in the database
        test a non existent person in the database that it returns None
    """
    def test_retrieve_patron(self):
        self.lib.insert_patron(self.p)
        self.assertEqual(self.lib.get_patron_count(), 1, 'There should be 1 patron in the database')
        patron = self.lib.retrieve_patron(123)
        self.assertEqual(None, self.lib.retrieve_patron(0))
