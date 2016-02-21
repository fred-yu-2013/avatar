# -*- coding: utf-8 -*-

import random


def password_random(length):
    chs = []

    for i in range(26):
        chs.append(chr(ord('a') + i))
        chs.append(chr(ord('A') + i))
        if i < 10:
            chs.append(chr(ord('0') + i))

    # print chs

    password_chs = []

    for i in range(length):
        password_chs.append(chs[random.randint(0, len(chs) - 1)])

    return ''.join(password_chs)

if __name__ == '__main__':
    lens = [8, 12, 16, 20, 24]
    for l in lens:
        print 'Password with length %d: \t%s' % (l, password_random(l))
