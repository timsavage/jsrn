# -*- coding: utf-8 -*-
import copy
from jsrn import exceptions

__all__ = ('BooleanField', 'StringField', 'IntegerField', 'FloatField', 'ObjectField', 'ArrayField')


class NOT_PROVIDED:
    pass


class Field(object):
    """
    Base class for all fields.
    """
    default_validators = []
    default_error_messages = {
        'invalid_choice': u'Value %r is not a valid choice.',
        'null': u'This field cannot be null.',
    }

    def __init__(self, verbose_name=None, verbose_name_plural=None, name=None, max_length=None, required=True, null=True, always_include=True,
                 default=NOT_PROVIDED,  choices=None, help_text='', validators=[], error_messages=None):
        """
        Initialisation of a Field.

        :param verbose_name: Display name of field.
        :param verbose_name_plural: Plural display name of field.
        :param name: Name of field in serialised form.
        :param max_length: Maximum length of a string.
        :param required: This field is required in to be set to a none empty value.
        :param null: This value can be null.
        :param always_include: Always include this value in serialised form (even if null).
        :param default: Default value for this field.
        :param choices: Collection of valid choices for this field.
        :param help_text: Help text to describe this field when generating a schema.
        :param validators: Additional validators, these should be a callable that takes a single value.
        :param error_messages: Dictionary that overrides error messages (or providers additional messages for custom
            validation.
        """
        self.verbose_name, self.verbose_name_plural = verbose_name, verbose_name_plural
        self.name = name
        self.max_length, self.required = max_length, required
        self.null, self.always_include = null, always_include
        self.default, self.choices = default, choices
        self.help_text = help_text

        self.validators = self.default_validators + validators

        messages = {}
        for c in reversed(self.__class__.__mro__):
            messages.update(getattr(c, 'default_error_messages', {}))
        messages.update(error_messages or {})
        self.error_messages = messages

    def __deepcopy__(self, memodict):
        # We don't have to deepcopy very much here, since most things are not
        # intended to be altered after initial creation.
        obj = copy.copy(self)
        memodict[id(self)] = obj
        return obj

    def set_attributes_from_name(self, attname):
        if not self.name:
            self.name = attname
        self.attname = attname
        if self.verbose_name is None and self.name:
            self.verbose_name = self.name.replace('_', ' ')
        if self.verbose_name_plural is None and self.verbose_name:
            self.verbose_name_plural = "%ss" % self.verbose_name

    def contribute_to_class(self, cls, name):
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self)

    def to_python(self, value):
        """
        Converts the input value into the expected Python data type, raising
        django.core.exceptions.ValidationError if the data can't be converted.
        Returns the converted value. Subclasses should override this.
        """
        return value

    def run_validators(self, value):
        pass

    def validate(self, value, model_instance):
        pass

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python and validate are propagated. The correct value is
        returned if no error is raised.
        """
        value = self.to_python(value)
        self.validate(value, model_instance)
        self.run_validators(value)
        return value

    def prep_value(self, value):
        """
        Prepare value for saving into JSON structure.
        """
        return value

    def has_default(self):
        """
        Returns a boolean of whether this field has a default value.
        """
        return self.default is not NOT_PROVIDED

    def get_default(self):
        """
        Returns the default value for this field.
        """
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        return None

    def value_from_object(self, obj):
        """
        Returns the value of this field in the given model instance.
        """
        return getattr(obj, self.attname)

    def value_for_object(self, obj, value):
        """
        Assign a value to an object
        """
        setattr(obj, self.attname, value)


class BooleanField(Field):
    default_error_messages = {
        'invalid': u"'%s' value must be either True or False."
    }

    def to_python(self, value):
        if value is None:
            return None
        if value in (True, False):
            # if value is 1 or 0 than it's equal to True or False, but we want
            # to return a true bool for semantic reasons.
            return bool(value)
        if isinstance(value, basestring):
            lvalue = value.lower()
            if lvalue in ('t', 'true', 'yes', 'on', '1'):
                return True
            if lvalue in ('f', 'false', 'no', 'off', '0'):
                return False
        msg = self.error_messages['invalid'] % str(value)
        raise exceptions.ValidationError(msg)


class StringField(Field):
    def to_python(self, value):
        if isinstance(value, basestring) or value is None:
            return value
        return str(value)


class FloatField(Field):
    default_error_messages = {
        'invalid': u"'%s' value must be a float.",
    }

    def to_python(self, value):
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            msg = self.error_messages['invalid'] % value
            raise exceptions.ValidationError(msg)


class IntegerField(Field):
    default_error_messages = {
        'invalid': u"'%s' value must be a integer.",
    }

    def to_python(self, value):
        if value is None:
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            msg = self.error_messages['invalid'] % value
            raise exceptions.ValidationError(msg)


class ObjectField(Field):
    default_error_messages = {
        'invalid': u"Must be a dict.",
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("default", dict())
        super(ObjectField, self).__init__(**kwargs)

    def to_python(self, value):
        if value is None:
            return value
        try:
            val = dict(value)
            val.pop("$", None)  # Ensure that any $ items are cleaned out
            return val
        except (TypeError, ValueError):
            msg = self.error_messages['invalid']
            raise exceptions.ValidationError(msg)


class ArrayField(Field):
    default_error_messages = {
        'invalid': u"Must be a list.",
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("default", list())
        super(ArrayField, self).__init__(**kwargs)

    def to_python(self, value):
        if value is None:
            return value
        try:
            return list(value)
        except (TypeError, ValueError):
            msg = self.error_messages['invalid']
            raise exceptions.ValidationError(msg)
