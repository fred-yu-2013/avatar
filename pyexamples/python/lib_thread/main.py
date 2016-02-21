# -*- coding: utf-8 -*-

import threading
import time


class Work(threading.Thread):
    """ 定义自己的线程执行体。
    1.只要实现__init__和run即可。
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print 'Do sth in Work.'
            time.sleep(2)


def main():
    work = Work()
    work.start()

if __name__ == '__main__':
    main()
    while True:
        print 'After main()'
        time.sleep(2)
