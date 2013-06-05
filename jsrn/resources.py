# -*- coding: utf-8 -*-
import copy
from jsrn.exceptions import ValidationError
import registration

DEFAULT_NAMES = ('abstract',)


class ResourceOptions(object):
    def __init__(self, meta):
        self.meta = meta
        self.fields = []
        self.virtual_fields = []
        self.resource_name = None
        self.abstract = False
        self.serialized_name = ''

    def contribute_to_class(self, cls, name):
        cls._meta = self
        self.resource_name = cls.__name__

        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                if name.startswith('_'):
                    del meta_attrs[name]
            for attr_name in DEFAULT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))

            # Any leftover attributes must be invalid.
            if meta_attrs != {}:
                raise TypeError("'class Meta' got invalid attribute(s): %s" % ','.join(meta_attrs.keys()))
        else:
            pass
        del self.meta

    def add_field(self, field):
        self.fields.append(field)
        if hasattr(self, '_field_cache'):
            del self._field_cache

        if hasattr(self, '_name_map'):
            del self._name_map

    def add_virtual_field(self, field):
        self.virtual_fields.append(field)

    def __repr__(self):
        return '<Options for %s>' % self.resource_name


class ResourceBase(type):
    """
    Metaclass for all Resources.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(ResourceBase, cls).__new__

        parents = [b for b in bases if isinstance(b, ResourceBase)]
        if not parents:
            # If this isn't a subclass of Resource, don't do anything special.
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta

        new_class.add_to_class('_meta', ResourceOptions(meta))
        if not abstract:
            pass  # Placeholder for future code...

        # Bail out early if we have already created this class.
        r = registration.get_resource(new_class._meta.resource_name)
        if r is not None:
            return r

        # Add all attributes to the class.
        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        # All the fields of any type declared on this model
        new_fields = new_class._meta.fields + new_class._meta.virtual_fields
        field_attnames = set([f.attname for f in new_fields])

        for base in parents:
            if not hasattr(base, '_meta'):
                # Things without _meta aren't functional models, so they're
                # uninteresting parents.
                continue

            parent_fields = base._meta.fields
            # Check for clashes between locally declared fields and those
            # on the base classes (we cannot handle shadowed fields at the
            # moment).
            for field in parent_fields:
                if field.attname in field_attnames:
                    raise Exception('Local field %r in class %r clashes '
                                     'with field of similar name from '
                                     'base class %r' % (field.attname, name, base.__name__))
            for field in parent_fields:
                new_class.add_to_class(field.attname, copy.deepcopy(field))

        if abstract:
            return new_class

        # Register resource
        registration.register_resources(new_class)

        # Because of the way imports happen (recursively), we may or may not be
        # the first time this model tries to register with the framework. There
        # should only be one class for each model, so we always return the
        # registered version.
        return registration.get_resource(new_class._meta.resource_name)

    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class Resource(object):
    __metaclass__ = ResourceBase

    def __init__(self, **kwargs):
        for field in iter(self._meta.fields):
            try:
                val = kwargs.pop(field.attname)
            except KeyError:
                val = field.get_default()
            setattr(self, field.attname, val)

        if kwargs:
            raise TypeError("'%s' is an invalid keyword argument for this function" % list(kwargs)[0])

    def __getstate__(self):
        state = {}
        for f in self._meta.fields:
            val = f.serialize(self)
            # Ignore
            if val is None and not f.always_include:
                continue
            state[f.name] = val
        return state

    def __setstate__(self, state):
        for f in self._meta.fields:
            f.deserialize(self, state.get(f.name))

    def clean(self):
        """
        Chance to do more in depth validation.
        """
        pass

    def full_clean(self):
        """
        Calls clean_fields, clean on the resource and raises ``ValidationError``
        for any errors that occurred.
        """
        errors = {}

        try:
            self.clean_fields()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        try:
            self.clean()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)

    def clean_fields(self):
        errors = {}

        for f in self._meta.fields:
            raw_value = f.value_from_object(self)

            if f.null and raw_value is None:
                continue
            try:
                f.value_for_object(self, f.clean(raw_value, self))
            except ValidationError as e:
                errors[f.name] = e.messages

        if errors:
            raise ValidationError(errors)
