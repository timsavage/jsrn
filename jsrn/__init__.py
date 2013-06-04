import json
from resources import Resource
from fields import *

__version__ = 0.1


def load(fp):
    """
    Load a from a JSON encoded file.
    """
    return loads(fp.read())


def loads(s):
    """
    Load from a JSON encoded string.
    """
    from encoding import JSRNDecoder
    return json.loads(s, cls=JSRNDecoder)


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
