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

    def clean(self, value):
        """
        Convert the value's type and run validation. Validation errors
        from to_python and validate are propagated. The correct value is
        returned if no error is raised.
        """
        value = self.to_python(value)
        return value


class ArrayOf(ObjectAs):
    default_error_messages = {
        'invalid': u"Must be a list of ``%r`` objects.",
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
                try:
                    values.append(super_to_python(obj))
                except exceptions.ValidationError, ve:
                    if hasattr(ve, 'message_dict'):
                        errors[str(idx)] = ve.message_dict
                    else:
                        errors[str(idx)] = ve.messages
            if errors:
                raise exceptions.ValidationError(errors)
            return values
        msg = self.error_messages['invalid'] % self.of
        raise exceptions.ValidationError(msg)

    def clean(self, value):
        """
        Convert the value's type and run validation. Validation errors
        from to_python and validate are propagated. The correct value is
        returned if no error is raised.
        """
        value = self.to_python(value)
        return value

