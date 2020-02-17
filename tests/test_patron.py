"""
Zachary Cook

Tests the patron module.
"""

import unittest
from library import patron
from library.patron import InvalidNameException

"""
Tests for methods of the Patron class.
"""
class test_Patron(unittest.TestCase):
    """
    Sets up the test case.
    """
    def setUp(self):
        # Create the component under testing.
        self.CuT = patron.Patron("John","Doe",21,0)

    """
    Test an error is thrown for a name with numbers.
    """
    def test_constructor_with_numbers(self):
        # Assert an error is thrown for the first name containing a number.
        with self.assertRaises(InvalidNameException):
            patron.Patron("John 2","Doe",21,0)

        # Assert an error is thrown for the last name containing a number.
        with self.assertRaises(InvalidNameException):
            patron.Patron("John","Doe 2",21,0)

    """
    Tests the getters not in other tests.
    """
    def test_getters(self):
        # Test the getters return the values from the constructor.
        self.assertEqual(self.CuT.get_fname(),"John","First name isn't correct.")
        self.assertEqual(self.CuT.get_lname(),"Doe","Last name isn't correct.")
        self.assertEqual(self.CuT.get_age(),21,"Age isn't correct.")
        self.assertEqual(self.CuT.get_memberID(),0,"Member id isn't correct.")

    """
    Tests the add_borrowed_book method.
    """
    def test_add_borrowed_book(self):
        # Add 2 books and assert it was added.
        self.CuT.add_borrowed_book("Book 1")
        self.CuT.add_borrowed_book("Book 2")
        self.assertEqual(self.CuT.get_borrowed_books(),["book 1","book 2"],"Books list is incorrect.")

        # Add duplicate books and assert they aren't added.
        self.CuT.add_borrowed_book("Book 1")
        self.CuT.add_borrowed_book("BOOK 2")
        self.assertEqual(self.CuT.get_borrowed_books(),["book 1","book 2"],"Books list is incorrect.")

    """
    Tests the return_borrowed_book method with a book.
    """
    def test_return_borrowed_book_with_book(self):
        # Add 2 books.
        self.CuT.add_borrowed_book("Book 1")
        self.CuT.add_borrowed_book("Book 2")

        # Return a book and assert it was removed.
        self.CuT.return_borrowed_book("BOOK 1")
        self.assertEqual(self.CuT.get_borrowed_books(),["book 2"],"Books list is incorrect.")

    """
    Tests the return_borrowed_book method without a book.
    """
    def test_return_borrowed_book_without_book(self):
        # Add 2 books.
        self.CuT.add_borrowed_book("Book 1")
        self.CuT.add_borrowed_book("Book 2")

        # Return a book and assert it was removed.
        self.CuT.return_borrowed_book("BOOK 3")
        self.assertEqual(self.CuT.get_borrowed_books(), ["book 1","book 2"], "Books list is incorrect.")

    """
    Tests the equals method.
    """
    def test_equals(self):
        # Assert the object being equals.
        self.assertTrue(self.CuT == self.CuT,"Patron isn't equal to itself.")
        self.assertTrue(self.CuT == patron.Patron("John","Doe",21,0),"Patron isn't equal to match.")
        self.assertFalse(self.CuT == patron.Patron("Jane","Doe",21,0),"Patron equals different first name.")
        self.assertFalse(self.CuT == patron.Patron("John","Foo",21,0),"Patron equals different last name.")
        self.assertFalse(self.CuT == patron.Patron("John","Doe",20,0),"Patron equals different age.")
        self.assertFalse(self.CuT == patron.Patron("John","Doe",21,1),"Patron equals different member id.")

    """
    Tests the not equals method.
    """
    def test_not_equals(self):
        # Assert the object being equals.
        self.assertFalse(self.CuT != self.CuT,"Patron is equal to itself.")
        self.assertFalse(self.CuT != patron.Patron("John","Doe",21,0),"Patron is equal to match.")
        self.assertTrue(self.CuT != patron.Patron("Jane","Doe",21,0),"Patron doesn't equal different first name.")
        self.assertTrue(self.CuT != patron.Patron("John","Foo",21,0),"Patron doesn't equal different last name.")
        self.assertTrue(self.CuT != patron.Patron("John","Doe",20,0),"Patron doesn't equal different age.")
        self.assertTrue(self.CuT != patron.Patron("John","Doe",21,1),"Patron doesn't equal different member id.")