from jsrn import exceptions
from jsrn.resources import create_resource_from_dict
from jsrn.fields import Field

__all__ = ('ObjectAs', 'ArrayOf',)


class ObjectAs(Field):
    default_error_messages = {
        'invalid': u"Must be a object of type ``%r``.",
    }

    def __init__(self, of, **kwargs):
        try:
            of._meta
        except AttributeError:
            raise TypeError("``%r`` is not a valid type for a related field." % of)
        self.of = of

        super(ObjectAs, self).__init__(**kwargs)

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, self.of):
            return value
        if isinstance(value, dict):
            return create_resource_from_dict(value, self.of._meta.resource_name)
        msg = self.error_messages['invalid'] % self.of
        raise exceptions.ValidationError(msg)


class ArrayOf(ObjectAs):
    default_error_messages = {
        'invalid': u"Must be a list of ``%r`` objects.",
        'null': u"List cannot contain null entries.",
    }

    def __init__(self, of, **kwargs):
        kwargs.setdefault('default', list)
        super(ArrayOf, self).__init__(of, **kwargs)

    def to_python(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            super_to_python = super(ArrayOf, self).to_python

            values = []
            errors = {}
            for idx, obj in enumerate(value):
                error_key = str(idx)

                # Null is not a valid entry in a list.
                if obj is None:
                    errors[error_key] = [self.error_messages['null']]
                    continue

                try:
                    values.append(super_to_python(obj))
                except exceptions.ValidationError, ve:
                    errors[error_key] = ve.error_messages

            if errors:
                raise exceptions.ValidationError(errors)

            return values
        msg = self.error_messages['invalid'] % self.of
        raise exceptions.ValidationError(msg)

