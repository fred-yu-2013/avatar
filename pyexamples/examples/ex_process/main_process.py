# -*- coding: utf-8 -*-
import os

import psutil

class ProcessExam:
    def __init__(self):
        pass

    @staticmethod
    def show_all_running_process():
        for proc in psutil.process_iter():
            if os.getpid() == proc.pid:
                print '>>>>>>>>>>>>>>>>>', proc.name(), proc.pid
            else:
                print proc.name(), proc.pid

if __name__ == '__main__':
    ProcessExam.show_all_running_process()
