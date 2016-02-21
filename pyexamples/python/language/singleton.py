"""
http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
"""

# Method 1: A decorator


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class MyClass():
    pass


# Method 2: A base class


class Singleton2(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class MyClass2(Singleton2):
    pass


# Method 3: A metaclass


class Singleton3(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton3, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


#Python2
class MyClass3():
    __metaclass__ = Singleton3


if __name__ == '__main__':
    m1 = MyClass()
    m2 = MyClass()
    assert(m1 == m2)
    m21 = MyClass2()
    m22 = MyClass2()
    assert(m21 == m22)
    m31 = MyClass3()
    m32 = MyClass3()
    assert(m31 == m32)
