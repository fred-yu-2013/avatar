# -*- coding: utf-8 -*-

import linecache
import os
import sys
sys.path.append(os.getcwd())
line_number = 0
line_number += 1
print linecache.getline("input.txt", line_number)
# print os.getcwd()
# print os.stat('input.txt')
# with open('input.txt') as f:
#     for line in iter(f.readline, ''):
#         print line


def mirror(s):
    mir = {'b': 'd', 'd': 'b', 'o': 'o', 'p': 'q',
           'q': 'p', 'v': 'v', 'w': 'w', 'x': 'x'}
    if not set(s).issubset(mir.keys()):
        return 'INVALID'
    return ''.join(map(lambda x: mir[x], s[::-1]))

print mirror("vow")
print mirror("wood")
print mirror("bed")

