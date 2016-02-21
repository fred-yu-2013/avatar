# -*- coding: utf-8 -*-

import sys

table_cache = {}


def P(m, n):
    count = 1
    while n > 0:
        count *= m
        m -= 1
        n -= 1
    return count


def C(m, n):
    s = 1
    for i in range(n + 1):
        s *= n
    return P(m, n) / s


def get_key(t, n):
    # > 0.86 ms
    # return '-'.join(map(str, sorted(map(lambda x: x[1], t.items())))) + '-' + str(n)
    # return ''.join(map(lambda x: '%X' % x, sorted(t.values()))) + '-' + str(n)
    # > 0.78 ms
    return tuple(sorted(t.values()) + [n])


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
    # if not has_duplicated_char(t):
    #     return P(len(t.keys()), n)
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


def get_possible_str_count_by_range(t, min_n, max_n):
    """ Get possible string count by char table and range. """
    count = 0
    for i in range(min_n, max_n + 1):
        count += get_possible_str_count(t, i)
    return count


def get_table(l):
    # ['2', '2', '1'] -> { '2': 2, '1': 1 }
    t = {}
    for item in l:
        if item not in t:
            t[item] = 1
        else:
            t[item] += 1
    return t


def get_count(r_list, min_n, max_n):
    t = get_table(r_list)
    return get_possible_str_count_by_range(t, min_n, max_n)


###############################################################
## Permutation


permutation_cache = {}

c, d = None, None

import utils
counter = utils.Counter()


def get_permutation_key(l, n):
    # [2, 1], 2 -> 21-2
    # > 0.64 m
    # return tuple(sorted(l) + [n])
    # > 0.63 m
    return tuple(l + [n])


def permutation(n, m, num_list, key):
    # print n, m, num_list

    # counter.increase()

    if m == 0:
        return 1

    if m == 1:
        return n

    # if n > 10 and m > 10:
    # key = get_permutation_key(num_list, m)
    if key in permutation_cache:
        return permutation_cache[key]

    global c, d

    # c, d = [0] * (m + 10 + 1), [[0] * (m + 1)] * (m + 1)
    # c, d = [0] * (m + 10 + 1), [[j for i in range(m + 1)] for j in range(m + 1)]

    if d is None:
        import utils
        tr = utils.TimeRecorder()
        d_len = 36
        d = [[j for i in range(d_len + 1)] for j in range(d_len + 1)]
        d[1][1], d[1][0] = 1, 1
        for i in range(2, d_len + 1):
            d[i][0] = 1
            for j in range(1, i):
                d[i][j] = d[i - 1][j - 1] + d[i - 1][j]
            d[i][i] = 1
        # tr.record()
        # print d

    if c is None:
        c = [0] * (36 + 10 + 1)

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

    # if n > 10 and m > 10:
    permutation_cache[key] = c[m]

    return c[m]


def get_chars_info(l):
    # ['2', '2', '1'] -> 2, [2, 1]
    t = {}
    for item in l:
        if item not in t:
            t[item] = 1
        else:
            t[item] += 1
    return len(t.keys()), t.values()


count_cache = {}


def get_count_key(l, min_n, max_n):
    # [2, 1], 2, 3 -> [1, 2, 2, 3]
    # > 0.76 m
    # return tuple(sorted(l) + [min_n, max_n])
    # > 0.79 m
    return tuple(l + [min_n, max_n])


def get_count2(r_list, min_n, max_n):
    n, num_list = get_chars_info(r_list)

    key = get_count_key(num_list, min_n, max_n)
    if key in count_cache:
        return count_cache[key]

    count = 0
    for i in range(min_n, max_n + 1):
        count += permutation(n, i, num_list, get_permutation_key(r_list, i))

    count_cache[key] = count

    return count


def get_right_list(l, left):
    res = l[:]
    for ch in left:
        for i in range(len(res)):
            if ch == res[i]:
                del res[i]
                break
    return res


def get_next_char(l, ch):
    res = None
    for c in l:
        if ch > c and (not res or res < c):
            res = c
    return res


def get_next_char_by_sorted(l, ch):
    # l MUST reverse sorted.
    for c in l:
        if ch > c:
            return c
    return None


def replace_next_char(l, ch):
    res = None
    index = None
    for i in range(len(l)):
        if ch > l[i] and (index is None or l[index] < l[i]):
            index = i
    if index >= 0:
        res = l[index]
        l[index] = ch
    return res


def get_first_index(l):
    return len(l) - 1


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

    # # > 0.63 m
    # # right_list = get_right_list(src, t[:index + 1])
    # # > 0.51 m
    # right_list = t[index + 1:]
    # ch = get_next_char(right_list, t[index])
    # t[index] = ch
    # # > 0.51 m
    # # t[index + 1:] = sorted(get_right_list(src, t[:index + 1]), reverse=reverse)
    # # > 0.48 m
    # t[index + 1:] = get_right_list(src, t[:index + 1])

    # > 0.38 m
    t[index + 1:] = sorted(t[index + 1:], reverse=True)
    ch = t[index]
    match_index = None
    for i in range(index + 1, len(t)):
        if ch > t[i] and (match_index is None or t[match_index] < t[i]):
            match_index = i
    if match_index is not None:
        t[index] = t[match_index]
        t[match_index] = ch


def left_move(src, t, index):
    if index == 0:
        return index
    gap = 0
    while t[index - gap - 1] == t[index]:
        gap += 1
    return index - gap


def find3(src, t, m, l):
    if m == 1:
        return

    index = get_first_index(src)

    while index >= 0:
        # print t, m, index

        # counter.increase()

        min_n = 0 if l - (index + 1) < 0 else l - (index + 1)
        max_n = len(src) - (index + 1)
        # import utils
        # tr = utils.TimeRecorder()
        count = get_count2(t[index + 1:], min_n, max_n)
        # tr.record()

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


def main():
    is_char = False
    char_lines = 0
    t, m, l = [], 0, 0
    m = 0
    # for line in sys.stdin:
    f = open('p3797.in')
    for line in iter(f.readline, ''):
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
            find3(t, result, m, l)
            if not result:
                print -1
            else:
                print ''.join(result)
            # return
            is_char = False
            char_lines = 0
            t, m, l = [], 0, 0

if __name__ == '__main__':
    import utils
    tr = utils.TimeRecorder()
    for i in range(1):
        main()
        tr.record()
        counter.record()

    # print get_possible_str_count({'A': 3, 'B': 4, 'C': 5}, 7)
    # print permutation(3, 7, [3, 4, 5])
    # print get_chars_info(['2', '2', '1'])


