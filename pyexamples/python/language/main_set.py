# -*- coding: utf-8 -*-

def example():
    """
    测试
    1.是否在set中
    """
    s = set()
    s.add(1)
    print 1 in s

class Example2:
    def __init__(self):
        self.a = 1

    def __eq__(self, other):
        return self.a == other.a

    def __hash__(self):
        return self.a

def example2():
    """
    测试对象添加到set中
    1.同时定义__eq__和__hash__
    :return:
    """
    s = set()
    s.add(Example2())
    s.add(Example2())
    print hash('abc') == hash('abc')
    print s

if __name__ == '__main__':
    # example()
    example2()
