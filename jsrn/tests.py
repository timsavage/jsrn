# -*- coding: utf-8 -*-
import jsrn


class Test(jsrn.Resource):
    pass


test = Test()
print test._meta.resource_name

