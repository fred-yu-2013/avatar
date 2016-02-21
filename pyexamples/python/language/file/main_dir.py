# -*- coding: utf-8 -*-
import glob


def example1():
    """
    列出通配符匹配的文件
    :return:
    """
    print glob.glob('d:/d*')  # ['d:/desktop', 'd:/devtools', 'd:/download']
    print glob.glob('asdfkl')  # []

    print sorted(glob.glob('d:/d*'), reverse=True)  # ['d:/download', 'd:/devtools', 'd:/desktop']

if __name__ == '__main__':
    example1()
