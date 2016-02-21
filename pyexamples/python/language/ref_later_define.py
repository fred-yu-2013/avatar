# -*- coding: utf-8 -*-

""" 无法引用后面定义的变量或函数，但可以在函数中调用，应为函数执行的时候，已经知道该定义了。
"""


def main():
    foo()


def foo():
    print 'hello'


main()

