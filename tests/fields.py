# -*- coding: utf-8 -*-
import unittest
from jsrn import fields
from jsrn.exceptions import ValidationError


class ObjectValue(object):
    pass


class FieldTestCase(unittest.TestCase):
    def test_error_messages_no_overrides(self):
        target = fields.Field()

        self.assertDictEqual({
            'invalid_choice': u'Value %r is not a valid choice.',
            'null': u'This field cannot be null.',
            'blank': u'This field cannot be blank.',
        }, target.error_messages)

    def test_error_messages_override_add(self):
        target = fields.Field(error_messages={
            'null': u'Override',
            'other': u'Other Value',
        })

        self.assertDictEqual({
            'invalid_choice': u'Value %r is not a valid choice.',
            'null': u'Override',
            'blank': u'This field cannot be blank.',
            'other': u'Other Value',
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


class BooleanFieldTestCase(unittest.TestCase):
    def test_to_python_bool_value(self):
        target = fields.BooleanField()
        self.assertTrue(target.to_python(True))
        self.assertFalse(target.to_python(False))

    def test_to_python_true_string(self):
        target = fields.BooleanField()
        self.assertTrue(target.to_python("t"))
        self.assertTrue(target.to_python("True"))
        self.assertTrue(target.to_python("yes"))
        self.assertTrue(target.to_python("ON"))
        self.assertTrue(target.to_python("1"))

    def test_to_python_false_string(self):
        target = fields.BooleanField()
        self.assertFalse(target.to_python("f"))
        self.assertFalse(target.to_python("False"))
        self.assertFalse(target.to_python("no"))
        self.assertFalse(target.to_python("OFF"))
        self.assertFalse(target.to_python("0"))

    def test_to_python_other_values(self):
        target = fields.BooleanField()

        with self.assertRaises(ValidationError):
            target.to_python(23424)

        with self.assertRaises(ValidationError):
            target.to_python("Value")
