# -*- coding: utf-8 -*-

import sys
import copy

NO_RESULT = '-1'

table_cache = {}


def P(m, n):
    count = 1
    while n > 0:
        count *= m
        m -= 1
        n -= 1
    return count


def get_key(t, n):
    return '-'.join(map(str, sorted(map(lambda x: x[1], t.items())))) + '-' + str(n)


def has_duplicated_char(t):
    for _, c in t.items():
        if c > 1:
            return True
    return False


def get_possible_str_count(t, n):
    """ Get possible string count by char table t and string length n. """
    if n == 0 or not t:
        return 1
    key = get_key(t, n)
    if key in table_cache:
        return table_cache[key]
    if not has_duplicated_char(t):
        return P(len(t.keys()), n)
    count = 0
    for ch, ch_count in t.items():
        if ch_count == 1:
            del t[ch]
        else:
            t[ch] = ch_count - 1
        count += get_possible_str_count(t, n - 1)
        t[ch] = ch_count
    table_cache[key] = count
    return count


def get_possible_str_count2(t, n):
    # print 'get_possible_str_count2', t, n
    if n == 0 or not t:
        return 1
    if n == 1:
        return len(t.keys())
    if n > reduce(lambda x, y: x + y, map(lambda x: x[1], t.items())):
        return 0

    key = get_key(t, n)
    if key in table_cache:
        return table_cache[key]
    if not has_duplicated_char(t):
        return P(len(t.keys()), n)

    count = 0
    stack = []
    tmp_t = copy.deepcopy(t)
    remain_keys = tmp_t.keys()
    while True:
        # print '-' * 40
        # print stack
        # print remain_keys, tmp_t, n
        if n == 1:
            count += len(tmp_t.keys())
            remain_keys, ch, tmp_t = stack.pop()
            n += 1
        else:
            if not has_duplicated_char(t):
                count += P(len(t.keys()), n)
                continue

            if not remain_keys and not stack:
                break

            if not remain_keys:
                key = get_key(tmp_t, n)
                if key in table_cache:
                    count += table_cache[key]
                    continue

                remain_keys, ch, tmp_t, count = stack.pop()
                n += 1
                continue
            tmp_t2 = copy.deepcopy(tmp_t)
            ch = remain_keys.pop()
            ch_count = tmp_t[ch]
            if ch_count == 1:
                del tmp_t[ch]
            else:
                tmp_t[ch] = ch_count - 1
            stack.append((remain_keys, ch, tmp_t2))
            remain_keys = tmp_t.keys()
            n -= 1
    # print 'count', count

    table_cache[key] = count

    return count


def get_possible_str_count_by_range(t, min_n, max_n):
    """ Get possible string count by char table and range. """
    count = 0
    for i in range(min_n, max_n + 1):
        count += get_possible_str_count(t, i)
    return count


def get_str(t, m, l, ch_count):
    if m <= 0 or ch_count <= 0:
        return ''
    for ch in sorted(t.keys(), reverse=True):
        ch_c = t[ch]
        if ch_c == 1:
            del t[ch]
        else:
            t[ch] = ch_c - 1
        count = get_possible_str_count_by_range(t, 0 if l <= 1 else l - 1, ch_count - 1)
        result = None
        if m <= count:
            result = ch + get_str(t, m, 0 if l <= 1 else l - 1, ch_count - 1)
        t[ch] = ch_c
        if result is not None:
            return result
        m -= count
    return ''


def main():
    is_char = False
    char_lines = 0
    t, m, l = {}, 0, 0
    m = 0
    for line in sys.stdin:
    # f = open('p3797.in')
    # for line in iter(f.readline, ''):
        if not is_char:
            char_lines, m, l = map(int, line.split())
            is_char = True
        else:
            char, count = line.split()
            t[char] = int(count)
            char_lines -= 1
        if char_lines == 0:
            # global table_cache
            # table_cache = {}
            ch_count = reduce(lambda x, y: x + y, map(lambda x: x[1], t.items()))
            if l > ch_count:
                print NO_RESULT
            else:
                result = get_str(t, m, l, ch_count)
                if not result:
                    print NO_RESULT
                else:
                    print result
            # print table_cache
            is_char = False
            char_lines = 0
            t, m, l = {}, 0, 0

for i in range(10):
    import utils
    tr = utils.TimeRecorder()
    main()
    tr.record()

# main()

# print '>>>' + str(get_possible_str_count({'I': 1, 'P': 1, 'C': 5}, 3))
# print '>>>' + str(get_possible_str_count2({'I': 1, 'P': 1, 'C': 5}, 3))
