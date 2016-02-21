# -*- coding: utf-8 -*-

import sys


def make_instruction(ins, vals, a_remain, a, b_remain, b, n):
    # do not step into.
    if (a_remain, b_remain) in vals:
        yield []
        return

    vals.append((a_remain, b_remain))

    # success
    if a_remain == n or b_remain == n:
        yield ['success']
        return

    def try_next(ins_temp, cur_ins, a_r_temp, b_r_temp):
        ins_temp.append(cur_ins)
        for item in make_instruction(ins_temp, vals, a_r_temp, a, b_r_temp, b, n):
            yield cur_ins + item

    # empty
    for item in try_next(ins[:], ['empty A'], 0, b_remain):
        yield item
    for item in try_next(ins[:], ['empty B'], a_remain, 0):
        yield item

    # fill
    for item in try_next(ins[:], ['fill A'], a, b_remain):
        yield item
    for item in try_next(ins[:], ['fill B'], a_remain, b):
        yield item

    def remain_by_pour(l_remain, r_remain, r):
        """ left -> right
        """
        return l_remain - (r - r_remain) if l_remain - (r - r_remain) > 0 else 0, \
            r_remain + l_remain if r_remain + l_remain < r else r

    # pour
    for item in try_next(ins[:], ['pour A B'], *remain_by_pour(a_remain, b_remain, b)):
        yield item
    for item in try_next(ins[:], ['pour B A'], *tuple(reversed(remain_by_pour(b_remain, a_remain, a)))):
        yield item


def compute(a, b, n):
    if n == 0:
        return ['success']
    if n == a:
        return ['fill A', 'success']
    if n == b:
        return ['fill B', 'success']
    for item in make_instruction([], [], 0, a, 0, b, n):
        if item and item[-1] == 'success':
            return item


def main():
    for line in sys.stdin:
        parts = map(int, line.split())
        output = compute(*parts)
        for item in output:
            print item

main()
# print compute(3, 5, 4)
