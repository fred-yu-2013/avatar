__author__ = 'Fred'
#encoding=utf-8

"""
The log system.
"""

import os
import codecs
import platform


class _Log():
    LOG_FILE = 'yisu_sell.log'

    def __init__(self):
        parent = os.path.dirname(os.path.realpath(__file__))
        parent = os.path.dirname(parent)
        if 'Linux' in platform.system():
            parent = '/mnt/run'
        self._file = codecs.open(os.path.join(parent, _Log.LOG_FILE), 'w', 'utf-8')

    def _out(self, out_str):
        self._file.write(out_str + '\n')
        self._file.flush()
        print out_str

    def d(self, msg):
        self._out('[D] %s' % msg)

    def e(self, msg):
        self._out('[E] %s' % msg)

    def __del__(self):
        self._file.close()

log = _Log()