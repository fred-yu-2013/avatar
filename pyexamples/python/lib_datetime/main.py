# -*- coding: utf-8 -*-

"""
Doc: https://docs.python.org/2/library/datetime.html
"""
from datetime import datetime


class DatetimeF:
    def __init__(self):
        pass

    @staticmethod
    def example1():
        # 解析
        d1 = datetime.strptime('2015-12-18 10:47:23', '%Y-%m-%d %H:%M:%S')
        print d1
        d2 = datetime.strptime('15-12-18 10:47:23', '%y-%m-%d %H:%M:%S')
        print d2
        d3 = datetime.now()
        print d3.strftime('%Y-%m-%d %H:%M:%S')  # 2015-12-18 10:55:38
        print d3.strftime('%y-%m-%d %H:%M:%S')  # 15-12-18 10:55:38

        # 时间戳转时间
        print datetime.fromtimestamp(1450882200)

if __name__ == '__main__':
    DatetimeF.example1()
