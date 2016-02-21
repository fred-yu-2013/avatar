# -*- coding: utf-8 -*-

import copy
import p3797

chars = []
for i in range(10):
    chars.append(str(i))
for i in range(ord('A'), ord('Z') + 1):
    chars.append(chr(i))
print chars


def increase_one(t):
    for k, v in t.items():
        if v >= 10:
            continue
        tmp = copy.deepcopy(t)
        tmp[k] = v + 1
        return tmp
    return None


def get_table_possible_count(t):
    if len(t) == 1:
        return
    ch_count = reduce(lambda x, y: x + y, map(lambda x: x[1], t.items()))
    if ch_count < 1:
        return
    for i in range(2, ch_count + 1):
        # print t
        count = p3797.get_possible_str_count(t, i)
        if count < 10 ** 18:
            print p3797.get_key(t, i) + ':' + str(count)


def get_char_tables(chars):
    tables = []
    keys = []
    t = {}
    for ch in chars:
        t[ch] = 1
    get_table_possible_count(t)
    tables.append(t)
    tmp = t
    while True:
        tmp = increase_one(tmp)
        if not tmp:
            break
        key = ''.join(map(str, sorted(map(lambda x: x[1], tmp.items()))))
        if not key in keys:
            keys.append(key)
            get_table_possible_count(tmp)
            tables.append(tmp)
    return tables

array = []
for i in range(1, 37):
    # print i
    sub_chars = chars[:i]
    # print sub_chars
    tables = get_char_tables(sub_chars)
    # print tables
    array.extend(tables)

# print array
