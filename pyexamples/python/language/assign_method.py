# -*- coding: utf-8 -*-

""" 本例子演示了成员函数可以当作普通函数赋值给一个变量，调用变量就好象调用了成员函数一样。
"""


class A(object):
    def __init__(self):
        self.name = 'A'

    def a(self):
        print self.name


class B(object):
    def __init__(self):
        self.__a = A()
        self.a = self.__a.a


def main():
    b = B()
    b.a()
    c = b.a
    c()

if __name__ == '__main__':
    main()
