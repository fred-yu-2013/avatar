# -*- coding: utf-8 -*-

from multiprocessing import Pool, TimeoutError
import time
import os


def f(x):
    return x*x


def example1():
    """
    源自官网
    :return:
    """
    pool = Pool(processes=4)              # start 4 worker processes

    # print "[0, 1, 4,..., 81]"
    print pool.map(f, range(10))

    # print same numbers in arbitrary order
    for i in pool.imap_unordered(f, range(10)):
        print i

    # evaluate "f(20)" asynchronously
    res = pool.apply_async(f, (20,))      # runs in *only* one process
    print res.get(timeout=1)              # prints "400"

    # evaluate "os.getpid()" asynchronously
    res = pool.apply_async(os.getpid, ()) # runs in *only* one process
    print res.get(timeout=1)              # prints the PID of that process

    # launching multiple evaluations asynchronously *may* use more processes
    multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
    print [res.get(timeout=1) for res in multiple_results]

    # make a single worker sleep for 10 secs
    res = pool.apply_async(time.sleep, (10,))
    try:
        print res.get(timeout=1)
    except TimeoutError:
        print "We lacked patience and got a multiprocessing.TimeoutError"


def f2(x):
    print 'enter process {}({})'.format(os.getpid(), x)
    time.sleep(x)
    print 'leave process {}({})'.format(os.getpid(), x)
    return x*x


def example2():
    pool = Pool(processes=4)

    numbers = [ 5, 4, 3, 2, 6, 5.1, 4.1, 3.1, 2.1]
    multiple_results = [pool.apply_async(f2, (i, )) for i in numbers]
    while True:
        if all(map(lambda r: r.ready(), multiple_results)):
            break
    pool.terminate()
    pool.join()


if __name__ == '__main__':
    example2()
