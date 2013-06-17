try:
    import simplejson as json
except ImportError:
    import json
from jsrn.resources import Resource
from jsrn.fields import *
from jsrn.fields.composite import *

__version__ = "0.2.0"


def load(fp, *args, **kwargs):
    """
    Load a from a JSON encoded file.

    See ``loads`` for a complete explanation of other parameters and operation of this method.
    """
    return loads(fp.read(), *args, **kwargs)


def loads(s, resource=None):
    """
    Load from a JSON encoded string.

    If a ``resource`` value is supplied it is used as the base resource for the supplied JSON. I one is not supplied a
    resource type field ``$`` is used to obtain the type represented by the dictionary. A ``ValidationError`` will be
    raised if either of these values are supplied and not compatible. It is valid for a type to be supplied in the file
    to be a child object from within the inheritance tree.

    :param s: String to load and parse.
    :param resource: A resource instance or a resource name to use as the base for creating a resource.
    """
    from jsrn.encoding import build_object_graph
    if isinstance(resource, Resource):
        resource_name = resource._meta.resource_name
    else:
        resource_name = resource
    return build_object_graph(json.loads(s), resource_name)


def dump(resource, fp, pretty_print=False):
    """
    Dump to a JSON encoded file.

    :param resource: The root resource to dump to a JSON encoded file.
    :param fp: The rile pointer that represents the output file.
    :param pretty_print: Pretty print the output, ie apply newline characters and indentation.
    """
    from jsrn.encoding import JSRNEncoder
    return json.dump(resource, fp, cls=JSRNEncoder, indent=4 if pretty_print else None)


def dumps(resource, pretty_print=True):
    """
    Dump to a JSON encoded string.

    :param resource: The root resource to dump to a JSON encoded file.
    :param pretty_print: Pretty print the output, ie apply newline characters and indentation.
    """
    from jsrn.encoding import JSRNEncoder
    return json.dumps(resource, cls=JSRNEncoder, indent=4 if pretty_print else None)
