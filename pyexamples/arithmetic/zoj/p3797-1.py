# -*- coding: utf-8 -*-

import p3797


def get_permutation_count(a):
    """ 获取字符串的可能个数, P7.2.1.2 Algorithm L.
    -> 个数，可能的排列列表
    :param a: 升序字符列表, 其中的元素可重复。
    """
    count = 1
    n = len(a)
    result = [''.join(a)]
    while True:
        j = n - 1
        while a[j - 1] >= a[j]:
            j -= 1
        if j == 0:
            break
        l = n
        while a[j - 1] >= a[l - 1]:
            l -= 1
        count += 1
        a[j - 1], a[l - 1] = a[l - 1], a[j - 1]
        # result.append(''.join(a))
        k = j + 1
        l = n
        a[k - 1: l] = sorted(a[k - 1: l])
    return count, result


# print get_permutation_count(['A', 'B', 'C', 'D'])
# print p3797.get_possible_str_count({'A': 1, 'B': 1, 'C': 1, 'D': 1}, 4)
# print get_permutation_count(['A', 'B', 'B', 'D'])
# print p3797.get_possible_str_count({'A': 1, 'B': 2, 'D': 1}, 4)
# print get_permutation_count(['A', 'B', 'B', 'C', 'C', 'C', 'D'])
print get_permutation_count([chr(i + ord('A')) for i in range(9)])

# print p3797.C(360, 2)
