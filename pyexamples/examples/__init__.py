# -*- coding: utf-8 -*-

"""
一些实际应用的例子，其下按功能分类。
"""

import linecache
line_number = 0
line_number += 1
print linecache.getline("input.txt", line_number)


class Foo():
    def __init__(self):
        self.a = 3

foo = Foo()
print dir(foo)
print getattr(foo, 'a')
# print getattr(foo, 'b')
print hasattr(foo, 'c')
