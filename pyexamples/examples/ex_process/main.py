# -*- coding: utf-8 -*-

import multiprocessing

import time
import copy_reg
import types


def my_exam1_work1():
    name = multiprocessing.current_process().name
    print my_exam1_work1.__name__, name


def my_exam1_work2(num):
    name = multiprocessing.current_process().name
    print my_exam1_work2.__name__, num, name


def my_exam1_work3(num):
    name = multiprocessing.current_process().name
    print my_exam1_work2.__name__, num, name
    time.sleep(2)


# class ProcessExamExam4:
#     def __init__(self):
#         pass
#
#     def work(self, num):
#         print my_exam1_work2.__name__, num


class ProcessExam:
    def __init__(self):
        pass

    @staticmethod
    def exam1():
        """
        函数作为入口，启动进程
        :return:
        """
        jobs = []
        for i in range(5):
            p = multiprocessing.Process(target=my_exam1_work1)
            jobs.append(p)
            p.start()

    @staticmethod
    def exam2():
        """
        函数作为入口，启动进程
        :return:
        """
        jobs = []
        for i in range(5):
            p = multiprocessing.Process(name='my_worker', target=my_exam1_work2, args=(i,))
            jobs.append(p)
            p.start()

    @staticmethod
    def exam3():
        """
        函数作为入口，启动进程
        :return:
        """
        jobs = []
        for i in range(2):
            p = multiprocessing.Process(target=my_exam1_work3, args=(i,))
            p.daemon = True
            jobs.append(p)
            p.start()

        # jobs[0].join()  # 等待子进程结束

        # jobs[0].terminate()  # 终结进程
        # jobs[0].join()  # 等待Kill结束

        # jobs[0].exitcode  # 进程入口函数的返回值

        time.sleep(5)  # 主线程退出之前，会将daemon进程关掉


def process_pool_exam_exam1_worker(x):
    return x*x


class ProcessPoolExamExam2Param:
    def __init__(self, param1):
        self.param1 = param1


# 进程池
class ProcessPoolExam:
    def __init__(self):
        pass

    @staticmethod
    def exam1():
        pool = multiprocessing.Pool(processes=4)              # start 4 worker processes

        result = pool.apply_async(process_pool_exam_exam1_worker, [10])    # evaluate "f(10)" asynchronously
        print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
        print pool.map(process_pool_exam_exam1_worker, range(10))          # prints "[0, 1, 4,..., 81]"

    def exam2worker(self, param):
        print self.exam2worker.__name__
        param.param1 *= param.param1
        return param

    def exam2worker_callback(self, param):
        print self.exam2worker_callback.__name__
        print param.param1

    def exam2(self):
        """
        作用：
        1. 进程入口、参数、返回值是类函数。
        2. 进程通过回调通知本进程执行结果。
        """
        pool = multiprocessing.Pool(processes=4)
        pool.apply_async(self.exam2worker,
                         args=[ProcessPoolExamExam2Param(10)],
                         callback=self.exam2worker_callback)
        pool.close()
        pool.join()
        # time.sleep(5)


# def _pickle_method(method):
#     func_name = method.im_func.__name__
#     obj = method.im_self
#     cls = method.im_class
#     return _unpickle_method, (func_name, obj, cls)
#
# def _unpickle_method(func_name, obj, cls):
#     for cls in cls.mro():
#         try:
#             func = cls.__dict__[func_name]
#         except KeyError:
#             pass
#         else:
#             break
#     return func.__get__(obj, cls)
#
# copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

# 解决 "Can't pickle ..." 的问题

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)

if __name__ == '__main__':
    # My.exam1()
    # My.exam2()
    # ProcessExam.exam3()

    # ProcessPoolExam.exam1()
    # print range(10)

    ProcessPoolExam().exam2()


