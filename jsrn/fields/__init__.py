# -*- coding: utf-8 -*-
import copy
from jsrn import exceptions

__all__ = ('BooleanField', 'StringField', 'IntegerField', 'FloatField', 'ObjectField', 'ArrayField')


class NOT_PROVIDED:
    pass


class Field(object):
    default_error_messages = {
        'invalid_choice': u'Value %r is not a valid choice.',
        'null': u'This field cannot be null.',
        'blank': u'This field cannot be blank.',
        'unique': u'%(model_name)s with this %(field_label)s '
                  u'already exists.',
    }

    def __init__(self, verbose_name=None, name=None, required=True, null=True, default=NOT_PROVIDED,
                 error_messages=None):
        self.verbose_name, self.name = verbose_name, name
        self.required = required
        self.null = null
        self.default = default
        self.rel = False

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

    def set_attributes_from_name(self, name):
        if not self.name:
            self.name = name
        self.attname = self.get_attname()
        if self.verbose_name is None and self.name:
            self.verbose_name = self.name.replace('_', ' ')

    def contribute_to_class(self, cls, name):
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self)

    def get_attname(self):
        return self.name

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
        'invalid': u"'%s' value must be either True or False."
    }

    def to_python(self, value):
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

    def prep_value(self, value):
        if value is None:
            return None
        return bool(value)


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
        if isinstance(value, basestring) or value is None:
            return value
        return str(value)

    def prep_value(self, value):
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

    def prep_value(self, value):
        if value is None:
            return None
        return int(value)


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
            return dict(value)
        except (TypeError, ValueError):
            msg = self.error_messages['invalid']
            raise exceptions.ValidationError(msg)

    def prep_value(self, value):
        if value is None:
            return None
        return dict(value)


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

    def prep_value(self, value):
        if value is None:
            return None
        return list(value)
