# -*- coding: utf-8 -*-
__author__ = 'Fred'


class MyClass():
    def __init__(self):
        self.counter = 100


obj = MyClass()
print obj.counter

# del后无法添加
# del obj.counter
# AttributeError: MyClass instance has no attribute 'counter'
# print obj.counter

obj.name = 'John'
obj.id = 5
print obj.id

# 可以通过__dict__属性添加
obj.__dict__['name'] = 'Fred'
print obj.name



class Employee():
    """
    此类可在外面增加成员变量
    """
    pass

john = Employee()
john.name = 'John Doe'

# 删除后，仍然可以添加
del john.name
john.name = 'John Doe'

class B:
    pass
class C(B):
    pass
class D(C):
    pass
for c in [B, C, D]:
    try:
        raise c()
    except D:
        print "D"
    except C:
        print "C"
    except B:
        print "B"

for c in [B, C, D]:
    try:
        raise c()
    except B:
        print "B"
    except C:
        print "C"
    except D:
        print "D"
