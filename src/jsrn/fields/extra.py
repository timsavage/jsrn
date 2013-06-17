# -*- coding: utf-8 -*-
import datetime
import six
from jsrn import validators
from jsrn.fields import Field


class DateField(Field):
    default_error_messages = {
        'invalid': "Invalid date value."
    }

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, six.string_types):
            pass  # TODO: Parse string to date
        if isinstance(value, datetime.date):
            return value
        if isinstance(value, datetime.datetime):
            return value.date()

    def to_json(self, value):
        if value is None:
            return None
        if isinstance(value, datetime.date):
            return value.isoformat()
        if isinstance(value, datetime.datetime):
            return value.date().isoformat()


class TimeField(Field):
    default_error_messages = {
        'invalid': "Invalid time value."
    }

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, six.string_types):
            pass  # TODO: Parse string to time
        if isinstance(value, datetime.date):
            return value
        if isinstance(value, datetime.datetime):
            return value.date()

    def to_json(self, value):
        if value is None:
            return None
        if isinstance(value, datetime.date):
            return value.isoformat()
        if isinstance(value, datetime.datetime):
            return value.date().isoformat()


class DateTimeField(Field):
    default_error_messages = {
        'invalid': "Invalid date/time value."
    }

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, six.string_types):
            pass  # TODO: Parse string to datetime
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)

    def to_json(self, value):
        if value is None:
            return None
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day).isoformat()
