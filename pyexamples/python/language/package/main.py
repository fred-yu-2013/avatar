__author__ = 'Fred'
# -*- coding: utf-8 -*-

# 相对路径的import必须在一个package中。
import relative_import.A.A


def main():
    """
    本例演示了：
    1.如何在package中使用相对路径import module.
    """
    # package中多了个__path__属性
    print dir(relative_import)
    for prop in dir(relative_import):
        print '%s:%s' % (prop, relative_import.__dict__[prop])

if __name__ == '__main__':
    main()