__author__ = 'Fred'
#coding=utf-8

import unittest
from model import *


class TestProperties(unittest.TestCase):
    def test_dict(self):
        p = Properties()
        p[u'姓名'] = u'张三'
        self.assertEqual(p[u'姓名'], u'张三')
        self.assertEqual(p.id, -1)
        self.assertEqual(p.index, -1)
