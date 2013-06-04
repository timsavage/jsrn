
class ResourceField(object):
    def __init__(self, of, name=None, related_name=None):
        try:
            of._meta
        except AttributeError:
            pass
        self.of, self.name = of, name
        self.related_name = related_name
        self.rel = True


class ResourceArrayField(object):
    def __init__(self, of, name=None, related_name=None):
        try:
            of._meta
        except AttributeError:
            pass
        self.of, self.name = of, name
        self.related_name = related_name
        self.rel = True
