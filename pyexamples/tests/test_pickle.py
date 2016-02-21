# -*- coding: utf-8 -*-

"""可以用来将Python对象存储为文件。"""

__author__ = 'Fred'

import pickle


def add(a, b):
    return a + b


def main():
    print __doc__
    with open('../examples/pickle_data.txt', 'w') as f:
        pickle.dump(add, f)
    with open('../examples/pickle_data.txt', 'r') as f:
        func = pickle.load(f)
    print func(100, 100)

main()
