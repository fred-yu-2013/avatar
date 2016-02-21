# -*- coding: utf-8 -*-

import sys


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    for i in range(len(lines) // 3):
        index = i * 3
        print '    X( %s ) // 0x%s' % (lines[index + 2], lines[index])

main()
