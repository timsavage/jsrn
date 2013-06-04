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


b = Block()
b.text = "EEK"
b.name = "123"

print jsrn.dumps(b)

print b._meta.resource_name

