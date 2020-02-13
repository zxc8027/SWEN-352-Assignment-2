from library.patron import Patron
from tinydb import TinyDB, Query
import os

class Library_DB:

    DATABASE_FILE = 'db.json'

    def __init__(self):
        self.db = TinyDB(self.DATABASE_FILE)

    def insert_patron(self, patron):
        if not patron:
            return None
        if self.retrieve_patron(patron.get_memberID()): # patron already in db
            return None
        data = self.convert_patron_to_db_format(patron)
        id = self.db.insert(data)
        return id

    def get_patron_count(self):
        results = self.db.all()
        return len(results)

    def get_all_patrons(self):
        results = self.db.all()
        return results

    def update_patron(self, patron):
        if not patron:
            return None
        query = Query()
        data = self.convert_patron_to_db_format(patron)
        self.db.update(data, query.memberID == patron.get_memberID())

    def retrieve_patron(self, memberID):
        query = Query()
        # assuming no two people in the db have the same memberID
        results = self.db.search(query.memberID == memberID)
        if results:
            return Patron(results[0]['fname'], results[0]['lname'], results[0]['age'],
            results[0]['memberID'])
        return None

    def close_db(self):
        self.db.close()

    def convert_patron_to_db_format(self, patron):
        return {'fname': patron.get_fname(), 'lname': patron.get_lname(), 'age': patron.get_age(), 'memberID': patron.get_memberID(),
        'borrowed_books': patron.get_borrowed_books()}
