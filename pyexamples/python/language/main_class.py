# -*- coding: utf-8 -*-

# TODO: add codes here.


class A:
    count = 0

    def __init__(self):
        self.count += 1

    def __del__(self):
        # print '__del__'
        print A.__del__.__name__


def test_del():
    a = A()
    del a


def example():
    """
    测试类变量
    """
    a = A()
    a2 = A()
    print a.count  # 1
    print a2.count  # 1


class Example2Base:
    def __init__(self, *args, **kwargs):
        pass


class Example2(Example2Base):
    def __init__(self, *args, **kwargs):
        """
        演示了变参数的使用
        :rtype: object
        """
        Example2Base.__init__(self, *args, **kwargs)
        self.__a = '1234'
        self.__b = None

    @property
    def a(self):
        return self.__a


class PropertyCls:
    # 演示property的使用
    def __init__(self):
        self.__b = None

    def set_b(self, value):
        self.__b = value

    b = property(fset=set_b)

if __name__ == '__main__':
    # test_del()
    # example()
    # print Example2().a

    # ex = PropertyCls()
    # ex.b = 5
    # pass

    a = A()
    del a
