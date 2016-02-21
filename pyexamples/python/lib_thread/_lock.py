# -*- coding: utf-8 -*-

import threading


def foo():
    l = threading.Lock()
    # Lock支持with操作。
    with l:
        print 'hello'

foo()
