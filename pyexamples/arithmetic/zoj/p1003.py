# -*- coding: utf-8 -*-

import sys


def parse_lines(line_handler):
    for line in sys.stdin:
        print line_handler(line.strip())


def __get_factors(value, cur_values=[]):
    """ int -> [[], ...], factors MUST not in cur_values.
    """
    max_value = value / 2
    max_value = max_value if max_value < 100 else 100
    for i in range(2, max_value):
        if not i in cur_values and (value % i) == 0:
            cur = cur_values[:]
            cur.append(i)
            for item in __get_factors(value / i, cur):
                yield [i] + item
    if not value in cur_values:
        yield [value]


def get_factors(value):
    return filter(lambda x: x and not any(map(lambda y: y > 100, x)), list(__get_factors(value)))


def judge_scores(left, right):
    """ Return valid one.
    """
    if left == right:
        return left
    higher = left if left > right else right
    lower = left if left < right else right
    h_fac = get_factors(higher)
    l_fac = get_factors(lower)
    if not h_fac and not l_fac:
        return higher
    elif not h_fac:
        return lower
    elif not l_fac:
        return higher
    is_all_intersection = True
    for h in h_fac:
        for l in l_fac:
            if not set(h).intersection(set(l)):
                is_all_intersection = False
                break
        if not is_all_intersection:
            break
    return higher if not is_all_intersection else lower


def line_handler(line):
    parts = map(int, line.split())
    return judge_scores(parts[0], parts[1])

parse_lines(line_handler)
