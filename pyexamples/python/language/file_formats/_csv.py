# -*- coding: utf-8 -*-

""" 本例子演示了如何操作csv格式的文件。
"""

import csv


def foo():
    """ b和非b的区别：在处理buffer时，是否当作字符来处理。
    """
    with open('output.txt', 'w') as f:
        f.write('A')
        f.write('\x03')
        f.flush()
    with open('output.txt', 'ab') as f:
        f.write('A')
        f.write('\x03')
        f.flush()


def foo2():
    with open('output.txt', 'wb') as f:
        # quotechar, 就是当单个元素中包含delimiter时， 需要用quotechar包起来。
        # quoting，表示包起来的方式。
        writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_ALL)
        writer.writerow(['Spam'] * 5 + ['Baked Beans'])
        writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        # print ['Spam'] * 5 + ['Baked Beans']  # 拼成一个list
    with open('output.txt', 'rb') as f:
        reader = csv.reader(f, delimiter=' ', quotechar='|')
        for row in reader:
            print ','.join(row)

if __name__ == '__main__':
    # foo()
    foo2()
