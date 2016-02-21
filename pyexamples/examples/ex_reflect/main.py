# -*- coding: utf-8 -*-
import sys


class SomeClass():
    def __init__(self, x):
        self.x = x
    def caller(self):
        return special_func(self.x)

def special_func(x):
    callingframe = sys._getframe(1)
    print 'My caller is the %r function in a %r class' % (
        callingframe.f_code.co_name,
        callingframe.f_locals['self'].__class__.__name__)

class ReflectF:
    def __init__(self):
        pass

    @staticmethod
    def example():
        """
        作用
        1.从被调用函数中获取，调用者信息
        """
        SomeClass(1).caller()

if __name__ == '__main__':
    ReflectF.example()

    d = {'ab': 'def'}
    if 'abc' in d:
        pass
