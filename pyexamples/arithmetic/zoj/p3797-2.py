# -*- coding: utf-8 -*-

import p3797


cache = {'1': 2}


def get_chars(l):
    # [ '2', '2', '1' ] -> [ '2', '1']
    return sorted(list(set(l)), reverse=True)


# def remove_char(l, ch):
#     # [ '3', '2', '2' ], '2' -> [ '3', '2']
#     for i in range(len(l)):
#         if l[i] == ch:
#             del l[i]
#             return l
#     return l


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
    # print t, r_list, min_n, len(r_list)
    return p3797.get_possible_str_count_by_range(t, min_n, max_n)


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


def find(src, t, m, l, index):
    # print src, t, m, l, index
    if m == 1:
        return

    if index < 0:
        del t[:]
        return

    if index == len(src) - 1:
        t.pop()
        m -= 1
        if m == 1:
            return
        find(src, t, m, l, index - 1)
        return

    # get possible chars.
    chars = get_chars(src[index + 1:])
    for i in range(len(chars)):
        if t[index] == chars[i]:
            continue
        del t[index + 1:]
        t[index] = chars[i]
        # r_list = remove_char(src[index:], chars[i])
        r_list = get_right_list(src, t)
        # print t, r_list, m
        min_n = 0 if l - (index + 1) < 0 else l - (index + 1)
        # count = get_count(r_list[:], min_n)  # TODO:
        count = get_count(r_list[:], 0)  # TODO:
        # print '>>>', count
        if m > count:
            m -= count
            if m == 1:
                return
        else:
            m -= 1
            t.extend(r_list)
            find(src, t, m, l, len(src) - 1)
            return

    # index elem is not selected.
    if index + 1 > l:
        t.pop()
        m -= 1
        if m == 1:
            return

    print '>>', t, m, index - 1
    find(src, t, m, l, index - 1)


def find2(src, t, m, l, index):
    if m == 1:
        return

    while index >= 0:
        if index == len(src) - 1:
            index -= 1
            del t[index + 1:]
            m -= 1
            if m == 1:
                return
            continue

        # get possible chars.
        chars = get_chars(src[index + 1:])
        for i in range(len(chars)):
            if t[index] == chars[i]:
                continue
            del t[index + 1:]
            t[index] = chars[i]
            r_list = get_right_list(src, t)
            min_n = 0 if l - (index + 1) < 0 else l - (index + 1)
            count = get_count(r_list[:], min_n)  # TODO:
            if m > count:
                m -= count
                if m == 1:
                    return
            else:
                m -= 1
                if m == 1:
                    return
                t.extend(r_list)
                index = len(src) - 1
                continue

        # index elem is not selected.
        if index + 1 > l:
            index -= 1
            t.pop()
            m -= 1
            if m == 1:
                return

        # index -= 1
        # del t[index + 1:]

    del t[:]

""" [Pseudo code]:
if m == 1: return

# index = len(src) - 1
index = find first index by m and src.

while index >= 0:
    # t[index + 1:] is reverse-sorted.
    # len(t) == len(src)
    # t[index] can decrease or not remove or remove.

    if t[index] can not remove:
        index = find_prev_decrease_index(src, t, index)
        if index < 0:
            clear t
            return
        # decrease t[index] and make right reverse-sorted: SEE below.
        m--
        if m == 1:
            return
        index = len(src) - 1
        continue

    right_list = s - t[:index + 1]
    count = get the count of right_list.
    if m - count >= 1:
        # decrease t[index] and make right reverse-sorted.
        right_list = s - t[:index + 1]
        t[index] = find_next(right_list, ch)
        t[:index] = reverse_sorted(s - t[:index + 1])

        m -= count
        if m == 1:
            return
    else:  # m < count + 1
        # try remove t[index] to t[0]
        tmp_index = len(src) - 1
        removed_count = 0
        while tmp_index > index and t[tmp_index] can remove:
            removed_count += 1
            if m - removed_count == 1:
                del t[tmp_index + 1:]
                return
            tmp_index--

        index++

del t[:]
"""

""" [Pseudo code 2]:
if m == 1: return

# index = len(src) - 1
index = find first index by m and src.

while index >= 0:
    # t[index + 1:] is reverse-sorted.
    # len(t) == len(src)
    # t[index] can decrease or not remove or remove.

    right_list = s - t[:index + 1]
    count = get_count(right_list)
    if m - count < 1:
        try remove right chars.
        index++
    else:
        m -= count
        if t[index] can decrease:
            decrease t[index] and make right list reverse-sorted.
        else:
            index = find prev decrease-able
            if index < 0: return
            decrease t[index] and make right list reverse-sorted.
            if t[index] can remove:
                m--
                if m == 1:
                    return

del t[:]
"""

def get_first_index(l):
    return len(l) - 1


def get_status(src, t, l, index):
    # -> 1: decrease, 0: not remove, -1: remove
    right_list = get_right_list(src, t[:index + 1])
    # print t, index
    ch = get_next_char(right_list, t[index])
    if ch is not None:
        return 1
    return -1 if index + 1 > l else 0


def find_prev_decrease_index(src, t, l, index):
    for i in range(index, -1, -1):
        if get_status(src, t, l, i) > 0:
            return i
    return -1


def decrease_and_right_reverse_sorted(src, t, index, reverse=True):
    # t[index] MUST can decrease.
    right_list = get_right_list(src, t[:index + 1])
    ch = get_next_char(right_list, t[index])
    t[index] = ch
    t[index + 1:] = sorted(get_right_list(src, t[:index + 1]), reverse=reverse)


def left_move(src, t, index):
    if index == 0:
        return index
    gap = 0
    while t[index - gap - 1] == t[index]:
        gap += 1
    return index - gap


def find3bak(src, t, m, l):
    if m == 1:
        return

    index = get_first_index(src)

    while index >= 0:
        # print t, m, index

        right_list = get_right_list(src, t[:index + 1])
        min_n = 0 if l - (index + 1) < 0 else l - (index + 1)
        max_n = len(src) - (index + 1)
        count = get_count(right_list, min_n, max_n)

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
                index = find_prev_decrease_index(src, t, l, index)
                if index < 0:
                    del t[:]
                    return
                decrease_and_right_reverse_sorted(src, t, index)
                if status < 0:
                    m -= 1
                    if m == 1:
                        return

    del t[:]


def find3(src, t, m, l):
    if m == 1:
        return

    index = get_first_index(src)

    while index >= 0:
        # print t, m, index

        right_list = get_right_list(src, t[:index + 1])
        min_n = 0 if l - (index + 1) < 0 else l - (index + 1)
        max_n = len(src) - (index + 1)
        count = get_count(right_list, min_n, max_n)

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
    main()
    tr.record()


