__author__ = 'Fred'
# -*- encoding: utf-8 -*-

import traceback


class Exception1(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


def do():
    raise Exception1('do()')


def main():
    """
    测试Exception的执行顺序
    1.except语句类似于if语句，处理了一个后，就处理另一个。
    2.
    """
    try:
        do()
    except Exception1, e:
        print 'Exception1', str(e)
        print traceback.format_exc()
    except Exception, e:
        print 'Exception', str(e)

main()
