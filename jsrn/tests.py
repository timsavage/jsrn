# -*- coding: utf-8 -*-
import jsrn


class Test(jsrn.Resource):
    name = jsrn.StringField()


class StyleField(jsrn.ObjectField):
    pass


class BaseElement(jsrn.Resource):
    name = jsrn.StringField()
    x = jsrn.IntegerField()
    y = jsrn.IntegerField()
    width = jsrn.IntegerField(required=False)
    height = jsrn.IntegerField(required=False)
    z_index = jsrn.IntegerField(required=False)
    style = StyleField()

    class Meta:
        abstract = True


class Block(BaseElement):
    text = jsrn.StringField()


class Image(BaseElement):
    src = jsrn.StringField()


class Group(BaseElement):
    items = jsrn.ArrayField()


class Layer(jsrn.Resource):
    css_class = jsrn.StringField()
    items = jsrn.ArrayField()


class Page(jsrn.Resource):
    title = jsrn.StringField()
    width = jsrn.IntegerField(default=768)
    height = jsrn.IntegerField(default=1024)
    style = StyleField()
    css_includes = jsrn.ArrayField()
    layers = jsrn.ArrayField()


b = Block()
b.text = "EEK"
b.name = "123"

print jsrn.dumps(b)

b.full_clean()

print b._meta.resource_name

