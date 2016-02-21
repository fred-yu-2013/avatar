# -*- coding: utf-8 -*-

from struct import *

def example1():
    s = pack('hhl', 1, 2, 3)
    print type(s), s  # 'str'
    print unpack('>hhl', '\x00\x01\x00\x02\x00\x00\x00\x03')  # (1, 2, 3)

if __name__ == '__main__':
    example1()
