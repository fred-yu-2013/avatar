__author__ = 'Fred'
#encoding=utf-8

"""
此文件的编码为：UTF-8无BOM（通过notepad++查看）
鼠标在那个测试函数上，运行(ctrl+shift+f10)那个测试函数
"""

import unittest
import codecs
import datetime
from threading import Thread, Event


class TestEncoding(unittest.TestCase):
    def setUp(self):
        pass

    def test_chinese(self):
        print u'中文', repr(u'中文')
        print u'ABC', repr(u'ABC')
        print 'ABC', repr('ABC')

    def test_chinese_file_write(self):
        # 必须使用codecs库生成utf-8无BOM格式的文件，并且可以直接输出中文。
        with codecs.open('test_coding4.log', 'w', 'utf-8') as f:
            f.write(u'中文')

    def test_chinese_dict(self):
        names = dict()
        names[u'中文键'] = u'中文内容'
        print names.get(u'中文键', '')
        self.assertEqual(names.get(u'中文键', ''), u'中文内容')


class TestThread(unittest.TestCase):
    @staticmethod
    def thread_main(test_thread):
        print 'i am in a lib_thread.', repr(test_thread)

    def test_thread(self):
        thr = Thread(target=TestThread.thread_main, args=(self, ))
        thr.start()
        thr.join()


class TestValues(unittest.TestCase):
    def test_datetime_format(self):
        print datetime.datetime.now().strftime("%Y-%m-%d")  # out: '2014-03-05'
        print datetime.datetime.now().strftime("%H:%M:%S")  # out: '14:16:21'

    def test_float(self):
        print float('%0.2f' % 1.0005)  # out: '1.0'
        print float('%0.2f' % 0.0005)  # out: '0.0'
        print float('%0.2f' % 1234.0005)  # out: '1234.0'

if __name__ == '__main__':
    unittest.main(verbosity=3)

    # suite = unittest.TestLoader().loadTestsFromTestCase(TestEncoding)
    # unittest.TextTestRunner(verbosity=3).run(suite)