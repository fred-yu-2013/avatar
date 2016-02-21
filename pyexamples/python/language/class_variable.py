# -*- coding: utf-8 -*-


class Foo():
    cls_var = 1

    def __init__(self):
        self.ins_var = 2

        print locals(self)
        print globals(self)


foo = Foo()
