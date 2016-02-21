# -*- coding: utf-8 -*-


class TimeRecorder():
    def __init__(self):
        import time
        self.__start = time.clock()
        self.__cur = self.__start

    def record(self):
        import time
        print time.clock() - self.__cur
        self.__cur = time.clock()


class Counter():
    def __init__(self):
        self.__count = 0

    def increase(self):
        self.__count += 1

    def record(self):
        print self.__count
