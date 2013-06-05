from jsrn import exceptions, registration
from jsrn.resources import Resource
from jsrn.fields import Field

__all__ = ('ObjectOfType', 'ArrayOfType',)


class ObjectOfType(Field):
    default_error_messages = {
        'invalid': u"Must be a object of type ``%r``.",
    }

    def __init__(self, of, **kwargs):
        try:
            of._meta
        except AttributeError:
            raise TypeError("``%r`` is not a valid type for a related field.")
        self.of = of

        super(ObjectOfType, self).__init__(**kwargs)

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, self.of):
            return value
        if isinstance(value, dict):
            return self.of(**value)

        msg = self.error_messages['invalid'] % self.of
        raise exceptions.ValidationError(msg)

    def clean(self, value, model_instance=None):
        """
        Convert the value's type and run validation. Validation errors
        from to_python and validate are propagated. The correct value is
        returned if no error is raised.
        """
        value = self.to_python(value)
        if value is not None:
            value.full_clean()
        return value

    def _deserialize(self, value):
        if isinstance(value, dict):
            resource_name = value.pop("$", None)
            specified_resource_name = self.of._meta.resource_name
            if resource_name != specified_resource_name:
                if not self.of._meta.abstract:
                    raise TypeError("Invalid resource type, expected `%s` got `%s`" % (
                        specified_resource_name, resource_name))
                else:
                    # TODO: validate that the specified resource is actually inherited off abstract
                    resource_type = registration.get_resource(resource_name)
            else:
                resource_type = self.of

            new_obj = resource_type()
            new_obj.__setstate__(value)
            return new_obj
        return value

    def deserialize(self, obj, value):
        """
        De-serialize value into object.
        """
        self.value_for_object(obj, self._deserialize(value))


class ArrayOfType(ObjectOfType):
    default_error_messages = {
        'invalid': u"Must be a list of ``%r`` objects.",
    }

    def __init__(self, of, **kwargs):
        kwargs.setdefault('default', list())
        super(ArrayOfType, self).__init__(of, **kwargs)

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, list):
            super_to_python = super(ArrayOfType, self).to_python
            return [super_to_python(i) for i in value]

        msg = self.error_messages['invalid'] % self.of
        raise exceptions.ValidationError(msg)

    def clean(self, value, model_instance=None):
        """
        Convert the value's type and run validation. Validation errors
        from to_python and validate are propagated. The correct value is
        returned if no error is raised.
        """
        value = self.to_python(value)
        if value is not None:
            for item in value:
                item.full_clean()
        return value

    def deserialize(self, obj, value):
        """
        De-serialize value into object.
        """
        if isinstance(value, list):
            value = [self._deserialize(i) for i in value]
        self.value_for_object(obj, value)
