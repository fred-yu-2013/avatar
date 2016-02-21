# -*- coding: utf-8 -*-
# 默认采用ascii编码，设置后，默认则为utf-8编码。

import binascii
# import bitarray
import sys


def strbin(s):
    return ''.join(format(ord(i),'0>8b') for i in s)


def strhex(s):
    h=""
    for x in s:
        h=h+(hex(ord(x)))[2:]
    return "0x"+h

# 字符串的默认编码，用作decode, encode等函数的编码参数的默认值。
print 'sys.getdefaultencoding()', sys.getdefaultencoding()

# Windows系统的默认编码，用作从Windows获取环境变量等值的时候的编码。
print 'sys.getfilesystemencoding()', sys.getfilesystemencoding()

# '你', unicode: 4F60, gbk: C4E3, utf-8: e4bda0
# 默认编码是utf-8, 在文件头定义。
s = '你'  # utf-8
print 's', strhex(s)

s2 = u'你'  # unicode
print 's2', strhex(s2)

# decode, encode的基准是unicode编码
s3 = s.decode('utf-8')  # utf-8 -> unicode
print 's.decode', strhex(s3)
s3 = str.decode(s, 'utf-8')  # utf-8 -> unicode
print 'str.decode(s)', strhex(s3)

s3 = s2.encode('utf-8')  # unicode -> utf-8
print 's2.decode', strhex(s3)
# s3 = str.encode(s2, 'utf-8')  # 参数错误，必须是str对象
s3 = unicode.encode(s2, 'utf-8')  # unicode -> utf-8
print 'unicode.decode(s2)', strhex(s3)

# 要变成其它格式，则需要先变成unicode
s3 = s.decode('utf-8').encode('gbk')  # utf-8 -> unicode -> gbk
print 's.decode.encode', strhex(s3)

s3 = unicode(s, 'utf-8')  # = s.decode('utf-8'), 第二个参数默认是ascii
print 'unicode(s)', strhex(s3)
