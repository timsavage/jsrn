# -*- coding: utf-8 -*-
import json
import registration
import resources


class JSRNEncoder(json.JSONEncoder):
    """
    Encoder for JSRN resources.
    """
    def default(self, o):
        if isinstance(o, resources.Resource):
            state = o.__getstate__()
            state['$'] = o._meta.resource_name
            return state
        return super(JSRNEncoder, self)


def _parse_class(obj):
    """
    Uses recursion to process a dict or list and convert into resource objects.
    """
    if isinstance(obj, dict):
        for k, v in obj.iteritems():
            obj[k] = _parse_class(v)

        resource_name = obj.pop('$', None)
        if resource_name:
            resource_type = registration.get_resource(resource_name)
            if resource_type:
                new_resource = resource_type()
                new_resource.__setstate__(obj)
                return new_resource
            else:
                raise TypeError("Unknown resource: %s" % resource_name)

    elif isinstance(obj, list):
        map(_parse_class, obj)

    return obj


class JSRNDecoder(json.JSONDecoder):
    """
    Decoder for JSRN encoded resources.
    """
    def decode(self, *args, **kwargs):
        return _parse_class(super(JSRNDecoder, self).decode(*args, **kwargs))
