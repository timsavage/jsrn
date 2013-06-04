import json
import encoding
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
    return json.loads(s, cls=encoding.JSRNDecoder)


def dump(doc, fp, pretty_print=False):
    """
    Dump to a JSON encoded file.
    """
    json.dump(doc, fp, cls=encoding.JSRNEncoder, indent=4 if pretty_print else None)


def dumps(doc, pretty_print=True):
    """
    Dump to a JSON encoded string.
    """
    json.dumps(doc, cls=encoding.JSRNEncoder, indent=4 if pretty_print else None)
