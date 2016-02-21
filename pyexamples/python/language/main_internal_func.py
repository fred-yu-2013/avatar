# -*- coding: utf-8 -*-

"""
Docs: https://docs.python.org/2/library/functions.html
"""


def example():
    # classmethod(), 修饰类函数，比staticmethod多一个self参数

    print cmp(1, 2)

    print divmod(30, 7)

    print list(enumerate(['a', 'b', 'c']))  # [(0, 'a'), (1, 'b'), (2, 'c')]

    print eval('30 + 5')  # 35

    # filter example: http://www.thegeekstuff.com/2014/05/python-filter-and-list/

    # format -> value.format(): https://docs.python.org/2/library/string.html#formatspec

    # memoryview objects allow Python code to access the internal data of an object that supports the buffer protocol without copying. Memory is generally interpreted as simple bytes.
    # https://docs.python.org/2/library/stdtypes.html#typememoryview
    print memoryview('abc')

    print hex(ord(u'你'))  # 0x4f60, unicode编码

if __name__ == '__main__':
    example()
