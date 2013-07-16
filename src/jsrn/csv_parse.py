# -*- coding: utf-8 -*-
"""
Parse CSV files into JSRN Resources
"""
import csv
from jsrn.resources import create_resource_from_dict


class ResourceReader(csv.DictReader):
    def __init__(self, f, resources, *args, **kwargs):
        self.resources = resources
        csv.DictReader.__init__(self, f, *args, **kwargs)

    def next(self):
        d = csv.DictReader.next(self)
        return create_resource_from_dict(d, self.resources._meta.resource_name)
