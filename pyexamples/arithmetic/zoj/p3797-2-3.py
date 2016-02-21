# -*- coding: utf-8 -*-

import sys

# 324ms
DEBUG = True


class Permutation():
    def __init__(self, n, max_num):
        self.__c = [0] * (n + max_num + 1)
        d = [[j for i in range(n + 1)] for j in range(n + 1)]
        d[1][1], d[1][0] = 1, 1
        for i in range(2, n + 1):
            d[i][0] = 1
            for j in range(1, i):
                d[i][j] = d[i - 1][j - 1] + d[i - 1][j]
            d[i][i] = 1
        self.__d = d
        self.__cache_by_range = {}

    def get_count(self, n, num_list, m):
        """ n element with nums in num_list, select m to get permutation count.
        """

        if m == 0:
            return 1

        if m == 1:
            return n

        c, d = self.__c, self.__d

        max_n = min(num_list[0], m)
        for i in range(max_n + 1):
            c[i] = d[m][i]
        if max_n <= m:
            for i in range(max_n + 1, m + 1):
                c[i] = 0
        for i in range(1, n):
            if num_list[i]:
                for j in range(m, -1, -1):
                    if c[j]:
                        for k in range(1, min(num_list[i], m - j) + 1):
                            c[k + j] += d[m - j][k] * c[j]

        return c[m]

    def get_count_by_range(self, n, num_list, min_m, max_m):
        key = self.__get_key_by_range(num_list, min_m, max_m)
        if key in self.__cache_by_range:
            return self.__cache_by_range[key]

        count = 0
        for i in range(min_m, max_m + 1):
            count += self.get_count(n, num_list, i)

        self.__cache_by_range[key] = count

        return count

    def __get_key_by_range(self, num_list, min_m, max_m):
        return tuple(sorted(num_list) + [min_m, max_m])


permutation = Permutation(36, 10)


def get_chars_info(l):
    # ['2', '2', '1'] -> 2, [2, 1]
    t = {}
    for item in l:
        if item not in t:
            t[item] = 1
        else:
            t[item] += 1
    return len(t.keys()), t.values()


def get_count2(r_list, min_n, max_n):
    n, num_list = get_chars_info(r_list)
    return permutation.get_count_by_range(n, num_list, min_n, max_n)


def get_status(src, t, l, index):
    # -> 1: decrease, 0: not remove, -1: remove
    cur_ch = t[index]
    last_index = None
    for i in range(index + 1, len(t)):
        if cur_ch > t[i] and (last_index is None or t[last_index] < t[i]):
            last_index = i
    if last_index is not None:
        return 1
    return -1 if index + 1 > l else 0


def find_prev_decrease_index(src, t, l, index):
    for i in range(index, -1, -1):
        if get_status(src, t, l, i) > 0:
            return i
    return -1


def decrease_and_right_reverse_sorted(src, t, index):
    # t[index] MUST can decrease.

    t[index + 1:] = sorted(t[index + 1:], reverse=True)
    ch = t[index]
    match_index = None
    for i in range(index + 1, len(t)):
        if ch > t[i] and (match_index is None or t[match_index] < t[i]):
            match_index = i
    if match_index is not None:
        t[index] = t[match_index]
        t[match_index] = ch


def find(src, t, m, l):
    if m == 1:
        return

    index = len(src) - 1

    while index >= 0:
        min_n = 0 if l - (index + 1) < 0 else l - (index + 1)
        max_n = len(src) - (index + 1)
        count = get_count2(t[index + 1:], min_n, max_n)

        if m - count < 1:
            # try remove t[index] to t[0]
            tmp_index = len(src) - 1
            removed_count = 0
            while tmp_index > index and get_status(src, t, l, tmp_index) < 0:
                removed_count += 1
                if m - removed_count == 1:
                    del t[tmp_index:]
                    return
                tmp_index -= 1
            index += 1
        else:
            status = get_status(src, t, l, index)
            if status > 0:
                m -= count
                decrease_and_right_reverse_sorted(src, t, index)
                if m == 1:
                    return
            else:
                m -= count
                if m == 1:
                    del t[index:]
                    return
                if status < 0:
                # Consider removable chars.
                    while index >= 0 and status < 0:
                        m -= 1
                        if m == 1:
                            del t[index:]
                            return
                        index -= 1
                        status = get_status(src, t, l, index)
                    if index < 0:
                        del t[:]
                        return
                # Change to previous decreasable position.
                index = find_prev_decrease_index(src, t, l, index)
                if index < 0:
                    del t[:]
                    return
                decrease_and_right_reverse_sorted(src, t, index)

    del t[:]


def handle_lines(line_iterator):
    is_char = False
    char_lines = 0
    t, m, l = [], 0, 0
    m = 0
    for line in line_iterator:
        if not is_char:
            char_lines, m, l = map(int, line.split())
            is_char = True
        else:
            char, count = line.split()
            for i in range(int(count)):
                t.append(char)
            char_lines -= 1
        if char_lines == 0:
            t = sorted(t, reverse=True)
            result = t[:]
            find(t, result, m, l)
            if not result:
                print -1
            else:
                print ''.join(result)
                # return
            is_char = False
            char_lines = 0
            t, m, l = [], 0, 0


def main():
    line_iterator = sys.stdin
    if DEBUG:
        line_iterator = iter(open('p3797.in').readline, '')
        import utils
        tr = utils.TimeRecorder()

    handle_lines(line_iterator)

    if DEBUG:
        tr.record()

if __name__ == '__main__':
    main()
