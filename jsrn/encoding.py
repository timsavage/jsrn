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


def build_object_graph(obj, resource_name=None):
    if isinstance(obj, dict):
        if not resource_name:
            resource_name = obj.pop("$", None)
        if resource_name:
            resource_type = registration.get_resource(resource_name)
            if resource_type:
                new_resource = resource_type()
                new_resource.__setstate__(obj)
                return new_resource
            else:
                raise TypeError("Unknown resource: %s" % resource_name)

    if isinstance(obj, list):
        return [build_object_graph(o, resource_name) for o in obj]

    return obj
