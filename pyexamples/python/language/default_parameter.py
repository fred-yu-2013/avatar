# -*- coding: utf-8 -*-


a = []

def test_default_list(datas=[]):
    datas.append(3)
    return datas


print id(test_default_list())
print id(test_default_list())
print id(a)
