# -*- coding: utf-8 -*-

"""
测试with和对象合作
"""


class A:
    def __enter__(self):
        print 'A.__enter__(), return "hello"'
        return "hello"  # 返回给with作为as参数

    def __exit__(self, exc_type, exc_val, exc_tb):
        print self, exc_type, exc_val, exc_tb


def example1():
    with A() as a:  # 调用的是A()的__enter__，其返回值付给a，结束后调用A()的__exit__
        print a
        # raise Exception('world')


if __name__ == '__main__':
    example1()
