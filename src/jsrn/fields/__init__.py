# -*- coding: utf-8 -*-
import copy
import six
from jsrn import exceptions
from jsrn.validators import EMPTY_VALUES, MaxLengthValidator, MinValueValidator, MaxValueValidator

__all__ = ('BooleanField', 'StringField', 'IntegerField', 'FloatField', 'ObjectField', 'ArrayField')


class NOT_PROVIDED:
    pass


class Field(object):
    """
    Base class for all fields.
    """
    default_validators = []
    default_error_messages = {
        'invalid_choice': 'Value %r is not a valid choice.',
        'null': 'This field cannot be null.',
        'blank': 'This field cannot be blank.',
    }

    def __init__(self, verbose_name=None, verbose_name_plural=None, name=None, required=True,
                 blank=False, null=False, default=NOT_PROVIDED, choices=None, help_text='', validators=[],
                 error_messages=None):
        """
        Initialisation of a Field.

        :param verbose_name: Display name of field.
        :param verbose_name_plural: Plural display name of field.
        :param name: Name of field in JSON form.
        :param required: This value must be defined in a loaded file.
        :param blank: This value can be a non empty value.
        :param null: This value can be null.
        :param default: Default value for this field.
        :param choices: Collection of valid choices for this field.
        :param help_text: Help text to describe this field when generating a schema.
        :param validators: Additional validators, these should be a callable that takes a single value.
        :param error_messages: Dictionary that overrides error messages (or providers additional messages for custom
            validation.
        """
        self.verbose_name, self.verbose_name_plural = verbose_name, verbose_name_plural
        self.name = name
        self.required = required
        self.blank, self.null = blank, null
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

    def __repr__(self):
        """
        Displays the module, class and name of the field.
        """
        path = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        name = getattr(self, 'name', None)
        if name is not None:
            return '<%s: %s>' % (path, name)
        return '<%s>' % path

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
        if value in EMPTY_VALUES:
            return

        errors = []
        for v in self.validators:
            try:
                v(value)
            except exceptions.ValidationError as e:
                if hasattr(e, 'code') and e.code in self.error_messages:
                    message = self.error_messages[e.code]
                    if e.params:
                        message = message % e.params
                    errors.append(message)
                else:
                    errors.extend(e.messages)
        if errors:
            raise exceptions.ValidationError(errors)

    def validate(self, value):
        if self.choices and value not in EMPTY_VALUES:
            for option_key, option_value in self.choices:
                if value == option_key:
                    return
            msg = self.error_messages['invalid_choice'] % value
            raise exceptions.ValidationError(msg)

        if value in EMPTY_VALUES and not self.required:
            return

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'])

        if not self.blank and value in EMPTY_VALUES:
            raise exceptions.ValidationError(self.error_messages['blank'])

    def clean(self, value):
        """
        Convert the value's type and run validation. Validation errors
        from to_python and validate are propagated. The correct value is
        returned if no error is raised.
        """
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value

    def to_json(self, value):
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


class BooleanField(Field):
    default_error_messages = {
        'invalid': "'%s' value must be either True or False."
    }

    def to_python(self, value):
        if value is None:
            return None
        if value in (True, False):
            # if value is 1 or 0 than it's equal to True or False, but we want
            # to return a true bool for semantic reasons.
            return bool(value)
        if isinstance(value, six.string_types):
            lvalue = value.lower()
            if lvalue in ('t', 'true', 'yes', 'on', '1'):
                return True
            if lvalue in ('f', 'false', 'no', 'off', '0'):
                return False
        msg = self.error_messages['invalid'] % str(value)
        raise exceptions.ValidationError(msg)


class StringField(Field):
    def __init__(self, max_length=None, **kwargs):
        super(StringField, self).__init__(**kwargs)
        if max_length is not None:
            self.validators.append(MaxLengthValidator(max_length))

    def to_python(self, value):
        if isinstance(value, six.string_types) or value is None:
            return value
        return str(value)


class ScalarField(Field):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        super(ScalarField, self).__init__(**kwargs)
        if min_value is not None:
            self.validators.append(MinValueValidator(min_value))
        if max_value is not None:
            self.validators.append(MaxValueValidator(max_value))


class FloatField(ScalarField):
    default_error_messages = {
        'invalid': "'%s' value must be a float.",
    }

    def to_python(self, value):
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            msg = self.error_messages['invalid'] % value
            raise exceptions.ValidationError(msg)


class IntegerField(ScalarField):
    default_error_messages = {
        'invalid': "'%s' value must be a integer.",
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
        'invalid': "Must be a dict.",
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("default", dict)
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
        'invalid': "Must be a list.",
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("default", list)
        super(ArrayField, self).__init__(**kwargs)

    def to_python(self, value):
        if value is None:
            return value
        try:
            return list(value)
        except (TypeError, ValueError):
            msg = self.error_messages['invalid']
            raise exceptions.ValidationError(msg)
