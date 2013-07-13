# -*- coding: utf-8 -*-
import unittest
import datetime
from jsrn import fields, datetimeutil
from jsrn.exceptions import ValidationError
from _fields_basic_helpers import create_simple_test_method


class ObjectValue(object):
    pass


class FieldTestCase(unittest.TestCase):
    def test_error_messages_no_overrides(self):
        target = fields.Field()

        self.assertDictEqual({
            'invalid_choice': 'Value %r is not a valid choice.',
            'null': 'This field cannot be null.',
            'blank': 'This field cannot be blank.',
            'required': 'This field is required.',
        }, target.error_messages)

    def test_error_messages_override_add(self):
        target = fields.Field(error_messages={
            'null': 'Override',
            'other': 'Other Value',
        })

        self.assertDictEqual({
            'invalid_choice': 'Value %r is not a valid choice.',
            'null': 'Override',
            'blank': 'This field cannot be blank.',
            'required': 'This field is required.',
            'other': 'Other Value',
        }, target.error_messages)

    def test_set_attributes_from_name(self):
        target = fields.Field()
        target.set_attributes_from_name("test_name")

        self.assertEqual("test_name", target.name)
        self.assertEqual("test_name", target.attname)
        self.assertEqual("test name", target.verbose_name)
        self.assertEqual("test names", target.verbose_name_plural)

    def test_set_attributes_from_name_with_name(self):
        target = fields.Field(name="init_name")
        target.set_attributes_from_name("test_name")

        self.assertEqual("init_name", target.name)
        self.assertEqual("test_name", target.attname)
        self.assertEqual("init name", target.verbose_name)
        self.assertEqual("init names", target.verbose_name_plural)

    def test_set_attributes_from_name_with_verbose_name(self):
        target = fields.Field(verbose_name="init Verbose Name")
        target.set_attributes_from_name("test_name")

        self.assertEqual("test_name", target.name)
        self.assertEqual("test_name", target.attname)
        self.assertEqual("init Verbose Name", target.verbose_name)
        self.assertEqual("init Verbose Names", target.verbose_name_plural)

    def test_has_default(self):
        target = fields.Field()

        self.assertFalse(target.has_default())

    def test_has_default_supplied(self):
        target = fields.Field(default="123")

        self.assertTrue(target.has_default())

    def test_get_default(self):
        target = fields.Field()

        self.assertIsNone(target.get_default())

    def test_get_default_supplied(self):
        target = fields.Field(default="123")

        self.assertEqual("123", target.get_default())

    def test_get_default_callable(self):
        target = fields.Field(default=lambda: "321")

        self.assertEqual("321", target.get_default())

    def test_value_from_object(self):
        target = fields.Field()
        target.set_attributes_from_name("test_name")

        an_obj = ObjectValue()
        setattr(an_obj, "test_name", "test_value")

        actual = target.value_from_object(an_obj)
        self.assertEqual("test_value", actual)



DATE_TIME_AWARE = datetime.datetime(2013, 7, 13, 16, 54, 46, 123000, datetimeutil.utc)
DATE_TIME_NAIVE = datetime.datetime(2013, 7, 13, 16, 54, 46, 123000)
DATE_TIME_STRING = "2013-07-13T16:54:46.123Z"
DATE_TIME_STRING_INVALID = "2013/07/13T16:54:46.123"

TO_PYTHON_TESTS = [
    (fields.BooleanField(), None, None),
    (fields.BooleanField(), True, True),
    (fields.BooleanField(), "t", True),
    (fields.BooleanField(), "True", True),
    (fields.BooleanField(), "yes", True),
    (fields.BooleanField(), "ON", True),
    (fields.BooleanField(), "1", True),
    (fields.BooleanField(), False, False),
    (fields.BooleanField(), "f", False),
    (fields.BooleanField(), "False", False),
    (fields.BooleanField(), "no", False),
    (fields.BooleanField(), "OFF", False),
    (fields.BooleanField(), "0", False),
    (fields.BooleanField(), 23424, ValidationError),
    (fields.BooleanField(), "Value", ValidationError),

    (fields.DateTimeField(assume_local=False), None, None),
    (fields.DateTimeField(assume_local=False), DATE_TIME_STRING, DATE_TIME_AWARE),
    (fields.DateTimeField(assume_local=False), DATE_TIME_AWARE, DATE_TIME_AWARE),
    (fields.DateTimeField(assume_local=False), DATE_TIME_STRING_INVALID, ValidationError),
    (fields.DateTimeField(assume_local=False), 2345, ValidationError),
]


class FieldToPythonTestCase(unittest.TestCase):
    pass

for idx, (field, value, expected) in enumerate(TO_PYTHON_TESTS):
    name, method = create_simple_test_method(field, "to_python", value, expected, idx)
    setattr(FieldToPythonTestCase, name, method)
