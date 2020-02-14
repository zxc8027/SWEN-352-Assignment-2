"""
Zachary Cook

Tests the ext_api_interface module.
"""

import requests
import unittest
from unittest.mock import MagicMock
from library import ext_api_interface

"""
Mock class for requests.
"""
class MockRequests:
    """
    Creates a mock requests module.
    """
    def __init__(self):
        self.ConnectionError = requests.ConnectionError
        self.errorResponses = []
        self.validResponses = {}

    """
    Fakes sending a network request.
    Delays are not simulated.
    """
    def get(self,url):
        # Return a response or error.
        if url in self.validResponses.keys():
            return self.validResponses[url]
        elif url in self.errorResponses:
            raise requests.ConnectionError()

        # Throw an error.
        raise RuntimeError("\"" + url + "\" is not set up to return a value.")

    """
    Sets a request URL's response with a given response table
    (from JSON) and status code.
    """
    def setResponse(self,url,statusCode,responseData):
        mockResponse = requests.Response()
        mockResponse.status_code = statusCode
        mockResponse.json = MagicMock(return_value=responseData)
        self.validResponses[url] = mockResponse

    """
    Sets a request URL to throw an error.
    """
    def setError(self,url):
        self.errorResponses.append(url)

"""
Tests for methods of the Books_API class.
"""
class test_Books_API(unittest.TestCase):
    """
    Sets up the unit test.
    """
    def setUp(self):
        # Set up the mock requests.
        self.mockRequests = MockRequests()
        ext_api_interface.requests = self.mockRequests

        # Create the component under testing.
        self.CuT = ext_api_interface.Books_API()
        self.CuT.API_URL = "http://mock.domain"

    """
    Tests the make_request method.
    """
    def test_make_request(self):
        # Set URLs as returning various responses.
        self.mockRequests.setResponse("http://test.domain/page1",200,{"status":"success"})
        self.mockRequests.setResponse("http://test.domain/page2",404,{"status":"not found"})
        self.mockRequests.setError("http://test.domain/page3")

        # Assert making requests returns the expected results.
        self.assertEqual(self.CuT.make_request("http://test.domain/page1"),{"status":"success"})
        self.assertIsNone(self.CuT.make_request("http://test.domain/page2"))
        self.assertIsNone(self.CuT.make_request("http://test.domain/page3"))

    """
    Tests the is_book_available method with an available book.
    """
    def test_is_book_available_true(self):
        # Set the response.
        self.mockRequests.setResponse(self.CuT.API_URL + "?q=TestBook",200,{"docs":"String"})

        # Assert the book is available.
        self.assertTrue(self.CuT.is_book_available("TestBook"))

    """
    Tests the is_book_available method with an unavailable book.
    """
    def test_is_book_available_false(self):
        # Set the response.
        self.mockRequests.setResponse(self.CuT.API_URL + "?q=TestBook",200,{"docs":""})

        # Assert the book is not
        # available.
        self.assertFalse(self.CuT.is_book_available("TestBook"))

    """
    Tests the is_book_available method with an HTTP error.
    """
    def test_is_book_available_http_error(self):
        # Set the response.
        self.mockRequests.setResponse(self.CuT.API_URL + "?q=TestBook",404,{"error":"not found"})

        # Assert the book is not available.
        self.assertFalse(self.CuT.is_book_available("TestBook"))

    """
    Tests the is_book_available method with a connection error.
    """
    def test_is_book_available_connection_error(self):
        # Set the response.
        self.mockRequests.setError(self.CuT.API_URL + "?q=TestBook")

        # Assert the book is not available.
        self.assertFalse(self.CuT.is_book_available("TestBook"))

    """
    Tests the books_by_author method with books.
    """
    def test_books_by_author_non_empty(self):
        # Set the response.
        self.mockRequests.setResponse(self.CuT.API_URL + "?author=TestAuthor",200,{"docs": [{"title_suggest":"Title 1"},{"title_suggest":"Title 2"}]})

        # Assert the list of titles is correct.
        self.assertEqual(self.CuT.books_by_author("TestAuthor"),["Title 1","Title 2"])

    """
    Tests the books_by_author method with no books.
    """
    def test_books_by_author_empty(self):
        # Set the response.
        self.mockRequests.setResponse(self.CuT.API_URL + "?author=TestAuthor",200,{"docs": []})

        # Assert the list of titles is correct.
        self.assertEqual(self.CuT.books_by_author("TestAuthor"),[])

    """
    Tests the books_by_author method with an error.
    """
    def test_books_by_author_error(self):
        # Set the response.
        self.mockRequests.setError(self.CuT.API_URL + "?author=TestAuthor")

        # Assert the list of titles is correct.
        self.assertEqual(self.CuT.books_by_author("TestAuthor"),[])

    """
    Tests the get_book_info method with books.
    """
    def test_get_book_info_books_found(self):
        # Set the responses.
        self.mockRequests.setResponse(self.CuT.API_URL + "?q=TestBook1",200,{"docs":[{"title":"Test title 1","publisher":"Test publisher","publish_year":"2000","language":"en-us","other_data":"other data"}]})
        self.mockRequests.setResponse(self.CuT.API_URL + "?q=TestBook2",200,{"docs": [{"title": "Test title 2"},{"title": "Test title 3"}]})

        # Assert the books are correct.
        self.assertEqual(self.CuT.get_book_info("TestBook1"),[{"title":"Test title 1","publisher":"Test publisher","publish_year":"2000","language":"en-us"}])
        self.assertEqual(self.CuT.get_book_info("TestBook2"),[{"title": "Test title 2"},{"title": "Test title 3"}])

    """
    Tests the get_book_info method with no books.
    """
    def test_get_book_info_no_book_found(self):
        # Set the responses.
        self.mockRequests.setResponse(self.CuT.API_URL + "?q=TestBook",200,{"docs":[]})

        # Assert the books are correct.
        self.assertEqual(self.CuT.get_book_info("TestBook"),[])

    """
    Tests the get_book_info method with an error.
    """
    def test_get_book_info_error(self):
        # Set the response.
        self.mockRequests.setError(self.CuT.API_URL + "?q=TestBook")

        # Assert the books are correct.
        self.assertEqual(self.CuT.get_book_info("TestBook"),[])

    """
    Tests the get_ebooks with a book found.
    """
    def test_get_ebooks_ebooks(self):
        # Set the response.
        self.mockRequests.setResponse(self.CuT.API_URL + "?q=TestBook",200,{"docs": [{"title":"Test title","ebook_count_i":1}]})

        # Assert the ebooks are correct.
        self.assertEqual(self.CuT.get_ebooks("TestBook"),[{"title":"Test title","ebook_count":1}])

    """
    Tests the get_ebooks with a non-ebook found.
    """
    def test_get_ebooks_no_ebooks(self):
        # Set the response.
        self.mockRequests.setResponse(self.CuT.API_URL + "?q=TestBook",200,{"docs": [{"title":"Test title","ebook_count_i":0}]})

        # Assert the ebooks are correct.
        self.assertEqual(self.CuT.get_ebooks("TestBook"),[])

    """
    Tests the get_ebooks with no books found.
    """
    def test_get_ebooks_no_books(self):
        # Set the response.
        self.mockRequests.setResponse(self.CuT.API_URL + "?q=TestBook",200,{"docs": []})

        # Assert the ebooks are correct.
        self.assertEqual(self.CuT.get_ebooks("TestBook"),[])

    """
    Tests the get_ebooks with an error.
    """
    def test_get_ebooks_error(self):
        # Set the response.
        self.mockRequests.setError(self.CuT.API_URL + "?q=TestBook")

        # Assert the ebooks are correct.
        self.assertEqual(self.CuT.get_ebooks("TestBook"),[])