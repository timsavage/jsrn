import json
from jsrn.resources import Resource
from jsrn.fields import *
from jsrn.fields.related import *

__version__ = 0.1


def load(fp, *args, **kwargs):
    """
    Load a from a JSON encoded file.
    """
    return loads(fp.read(), *args, **kwargs)


def loads(s, resource_name=None):
    """
    Load from a JSON encoded string.
    """
    from encoding import build_object_graph
    return build_object_graph(json.loads(s), resource_name)


def dump(resource, fp, pretty_print=False):
    """
    Dump to a JSON encoded file.
    """
    from encoding import JSRNEncoder
    return json.dump(resource, fp, cls=JSRNEncoder, indent=4 if pretty_print else None)


def dumps(resource, pretty_print=True):
    """
    Dump to a JSON encoded string.
    """
    from encoding import JSRNEncoder
    return json.dumps(resource, cls=JSRNEncoder, indent=4 if pretty_print else None)
