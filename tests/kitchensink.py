# -*- coding: utf-8 -*-
"""
Do load/dump tests on known valid and invalid documents.
"""
import os
import unittest
import sys
import jsrn
from jsrn import exceptions

FIXTURE_PATH_ROOT = os.path.join(os.path.dirname(__file__), "fixtures")


class Author(jsrn.Resource):
    name = jsrn.StringField()


class Publisher(jsrn.Resource):
    name = jsrn.StringField()


class LibraryBook(jsrn.Resource):
    class Meta:
        abstract = True
        name_space = "library"


class Book(LibraryBook):
    title = jsrn.StringField()
    num_pages = jsrn.IntegerField()
    rrp = jsrn.FloatField()
    fiction = jsrn.BooleanField()
    genre = jsrn.StringField(choices=(
        ('sci-fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('others', 'Others'),
    ))
    authors = jsrn.ArrayOf(Author)
    publisher = jsrn.ObjectAs(Publisher)


class Library(jsrn.Resource):
    name = jsrn.StringField()
    books = jsrn.ArrayOf(LibraryBook)


class KitchenSinkTestCase(unittest.TestCase):
    @unittest.skipIf(sys.version_info[0] > 2, "Disabled as Python 2 and Python 3 appear to output result differently. "
                                              "This test needs a better way of determining a positive outcome.")
    def test_dumps_with_valid_data(self):
        book = Book(title="Consider Phlebas", num_pages=471, rrp=19.50, genre="sci-fi", fiction=True)
        book.publisher = Publisher(name="Macmillan")
        book.authors.append(Author(name="Iain M. Banks"))

        library = Library(name="Public Library", books=[book])

        actual = jsrn.dumps(library, pretty_print=False)
        expected = '{"books": [' \
                   '{"publisher": {"name": "Macmillan", "$": "Publisher"}, "num_pages": 471, ' \
                   '"$": "library.Book", "title": "Consider Phlebas", "fiction": true, ' \
                   '"authors": [{"name": "Iain M. Banks", "$": "Author"}], "genre": "sci-fi", "rrp": 19.5}], ' \
                   '"name": "Public Library", "$": "Library"}'

        self.assertEqual(expected, actual)

    def test_full_clean_invalid_data(self):
        book = Book(title="Consider Phlebas", num_pages=471, rrp=19.50, genre="space opera", fiction=True)
        book.publisher = Publisher(name="Macmillan")
        book.authors.append(Author(name="Iain M. Banks"))

        library = Library(name="Public Library", books=[book])

        with self.assertRaises(exceptions.ValidationError):
            library.full_clean()

    def test_load_valid_data(self):
        library = jsrn.load(open(os.path.join(FIXTURE_PATH_ROOT, "book-valid.json")))

        self.assertEqual("Consider Phlebas", library.books[0].title)

    def test_load_invalid_data(self):
        with self.assertRaises(exceptions.ValidationError):
            jsrn.load(open(os.path.join(FIXTURE_PATH_ROOT, "book-invalid.json")))
