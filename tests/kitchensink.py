# -*- coding: utf-8 -*-
"""
Do load/dump tests on known valid and invalid documents.
"""
import os
import unittest
import jsrn
from jsrn import exceptions

FIXTURE_PATH_ROOT = os.path.join(os.path.dirname(__file__), "fixtures")


class Author(jsrn.Resource):
    name = jsrn.StringField()


class Publisher(jsrn.Resource):
    name = jsrn.StringField()


class Book(jsrn.Resource):
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


class KitchenSinkTestCase(unittest.TestCase):
    def test_dumps_with_valid_data(self):
        book = Book(title="Consider Phlebas", num_pages=471, rrp=19.50, genre="sci-fi", fiction=True)
        book.publisher = Publisher(name="Macmillan")
        book.authors.append(Author(name="Iain M. Banks"))

        actual = jsrn.dumps(book, pretty_print=False)
        expected = '{"publisher": {"name": "Macmillan", "$": "kitchensink.Publisher"}, "num_pages": 471, ' \
                   '"$": "kitchensink.Book", "title": "Consider Phlebas", "fiction": true, ' \
                   '"authors": [{"name": "Iain M. Banks", "$": "kitchensink.Author"}], "genre": "sci-fi", "rrp": 19.5}'

        self.assertEqual(expected, actual)

    def test_dumps_with_invalid_data(self):
        book = Book(title="Consider Phlebas", num_pages=471, rrp=19.50, genre="space opera", fiction=True)
        book.publisher = Publisher(name="Macmillan")
        book.authors.append(Author(name="Iain M. Banks"))

        with self.assertRaises(exceptions.ValidationError):
            jsrn.dumps(book)

    def test_load_valid_data(self):
        book = jsrn.load(file(os.path.join(FIXTURE_PATH_ROOT, "book-valid.json")))

        self.assertEqual("Consider Phlebas", book.title)

    def test_load_invalid_data(self):
        with self.assertRaises(exceptions.ValidationError):
            jsrn.load(file(os.path.join(FIXTURE_PATH_ROOT, "book-invalid.json")))
