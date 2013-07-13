# -*- coding: utf-8 -*-
import copy
import six
from jsrn import exceptions, registration
from jsrn.exceptions import ValidationError
from jsrn.fields import NOT_PROVIDED


RESOURCE_TYPE_FIELD = '$'
META_OPTION_NAMES = ('name', 'name_space', 'verbose_name', 'verbose_name_plural', 'abstract', 'doc_group', )


class ResourceOptions(object):
    def __init__(self, meta):
        self.meta = meta
        self.parents = []
        self.fields = []
        self.virtual_fields = []

        self.name = None
        self.name_space = None
        self.verbose_name = None
        self.verbose_name_plural = None
        self.abstract = False
        self.doc_group = None

    def contribute_to_class(self, cls, name):
        cls._meta = self
        self.name = cls.__name__

        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                if name.startswith('_'):
                    del meta_attrs[name]
            for attr_name in META_OPTION_NAMES:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))

            # Any leftover attributes must be invalid.
            if meta_attrs != {}:
                raise TypeError("'class Meta' got invalid attribute(s): %s" % ','.join(meta_attrs.keys()))
        del self.meta

        if not self.verbose_name:
            self.verbose_name = self.name.replace('_', ' ').strip('_ ')
        if not self.verbose_name_plural:
            self.verbose_name_plural = self.verbose_name + 's'

    def add_field(self, field):
        self.fields.append(field)
        if hasattr(self, '_field_cache'):
            del self._field_cache

        if hasattr(self, '_name_map'):
            del self._name_map

    def add_virtual_field(self, field):
        self.virtual_fields.append(field)

    @property
    def resource_name(self):
        """
        Full name of resource including namespace (if specified)
        """
        if self.name_space:
            return "%s.%s" % (self.name_space, self.name)
        else:
            return self.name

    @property
    def parent_resource_names(self):
        """
        List of parent resource names.
        """
        if not hasattr(self, '_parent_resource_names'):
            self._parent_resource_names = [p._meta.resource_name for p in self.parents]
        return self._parent_resource_names

    def __repr__(self):
        return '<Options for %s>' % self.resource_name


class ResourceBase(type):
    """
    Metaclass for all Resources.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(ResourceBase, cls).__new__

        # attrs will never be empty for classes declared in the standard way
        # (ie. with the `class` keyword). This is quite robust.
        if name == 'NewBase' and attrs == {}:
            return super_new(cls, name, bases, attrs)

        parents = [b for b in bases if isinstance(b, ResourceBase) and not (b.__name__ == 'NewBase'
                                                                            and b.__mro__ == (b, object))]
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
        base_meta = getattr(new_class, '_meta', None)

        new_class.add_to_class('_meta', ResourceOptions(meta))
        if not abstract:
            # Namespace is inherited
            if not new_class._meta.name_space and base_meta:
                new_class._meta.name_space = base_meta.name_space

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
                    raise Exception('Local field %r in class %r clashes with field of similar name from '
                                    'base class %r' % (field.attname, name, base.__name__))
            for field in parent_fields:
                new_class.add_to_class(field.attname, copy.deepcopy(field))

            new_class._meta.parents.append(base)

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


class Resource(six.with_metaclass(ResourceBase)):
    def __init__(self, **kwargs):
        for field in iter(self._meta.fields):
            try:
                val = kwargs.pop(field.attname)
            except KeyError:
                val = field.get_default()
            setattr(self, field.attname, val)

        if kwargs:
            raise TypeError("'%s' is an invalid keyword argument for this function" % list(kwargs)[0])

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    def __str__(self):
        return '%s resource' % self.__class__.__name__

    def extra_attrs(self, attrs):
        """
        Called during deserialisation of data if there are any extra fields defined in the document.

        This allows the resource to decide how to handle these fields. By default they are ignored.
        """
        pass

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
                setattr(self, f.attname, f.clean(raw_value))
            except ValidationError as e:
                errors[f.name] = e.messages

        if errors:
            raise ValidationError(errors)


def create_resource_from_dict(obj, resource_name=None):
    """
    Create a resource from a dict object.
    """
    assert isinstance(obj, dict)

    # Get the correct resource name
    document_resource_name = obj.pop(RESOURCE_TYPE_FIELD, resource_name)
    if not (document_resource_name or resource_name):
        raise exceptions.ValidationError("Resource not defined.")

    resource_type = registration.get_resource(document_resource_name)
    if not resource_type:
        raise exceptions.ValidationError("Resource `%s` is not registered." % document_resource_name)

    # Check if we have an inherited type.
    if resource_name and not (resource_name == document_resource_name or
                              resource_name in resource_type._meta.parent_resource_names):
        raise exceptions.ValidationError(
            "Expected resource `%s` does not match resource defined in JSRN document `%s`." % (
                resource_name, document_resource_name))

    errors = {}
    attrs = {}
    for f in resource_type._meta.fields:
        value = obj.pop(f.name, NOT_PROVIDED)
        try:
            attrs[f.attname] = f.clean(value)
        except exceptions.ValidationError as ve:
            errors[f.name] = ve.error_messages

    if errors:
        raise exceptions.ValidationError(errors)

    new_resource = resource_type(**attrs)
    if obj:
        new_resource.extra_attrs(obj)
    new_resource.full_clean()
    return new_resource
