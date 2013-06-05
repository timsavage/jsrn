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
    items = jsrn.ArrayOfType(BaseElement)


class Layer(jsrn.Resource):
    css_class = jsrn.StringField()
    items = jsrn.ArrayOfType(BaseElement)


class Page(jsrn.Resource):
    title = jsrn.StringField()
    width = jsrn.IntegerField(default=768)
    height = jsrn.IntegerField(default=1024)
    style = StyleField()
    css_includes = jsrn.ArrayField()
    layers = jsrn.ArrayOfType(Layer)


p = Page()
p.title = "EEK"
p.name = "123"
p.layers.append(Layer(css_class="MoveInFromTop"))

out = jsrn.dumps(p)
print out

p2 = jsrn.loads(out)

print p2._meta.resource_name
print len(p2.layers)

p2.full_clean()
