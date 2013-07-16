# -*- coding: utf-8 -*-
import os
import unittest
import jsrn
from jsrn.csv_parse import ResourceReader

FIXTURE_PATH_ROOT = os.path.join(os.path.dirname(__file__), "fixtures")


class Book(jsrn.Resource):
    title = jsrn.StringField(name="Title")
    num_pages = jsrn.IntegerField(name="Num Pages")
    rrp = jsrn.FloatField(name="RRP")
    genre = jsrn.StringField(name="Genre", choices=(
        ('sci-fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('others', 'Others'),
    ))
    author = jsrn.StringField(name="Author")
    publisher = jsrn.StringField(name="Publisher")


class CsvResourceReaderTestCase(unittest.TestCase):
    def test_items(self):
        with open(os.path.join(FIXTURE_PATH_ROOT, "libary-valid.csv")) as f:
            books = [book for book in ResourceReader(f, Book)]

        print books
