# -*- coding: utf-8 -*-

import re


def get_one():
    to_find = re.compile("cat|fish|dog")
    search_str = "blah fish cat dog haha"
    match_obj = to_find.search(search_str)
    the_index = match_obj.start()  # produces 5, the index of fish
    which_word_matched = match_obj.group()  # "fish"

    match_obj = re.search('id/([0-9]+)', 'http://piao.huo.com/cinema/cinemaInfo/id/2489')
    which_word_matched = match_obj.group(1)
    # results = match_obj.group('id')
    pass

    # 测试任意字符

    match_obj = re.search(r'cinema/(.+)', 'http://sh.nuomi.com/cinema/22e11407bd4cd9add5b74e15')
    print match_obj.group(1)

    # 测试单词长度

    match_obj = re.search(r'([0-9]+\.[0-9]+)', 'ABC12.56DEF')
    print match_obj.group(1)

    # 测试单词或

    match_obj = re.search(r'[cinema|shop]/(.+)', 'http://sh.nuomi.com/cinema/22e11407bd4cd9add5b74e15')
    print match_obj.group(1)
    match_obj = re.search(r'[cinema|shop]/([0-9]+)', 'http://sh.nuomi.com/shop/22e11407bd4cd9add5b74e15')
    print match_obj.group(1)

    # 测试失败情况

    match_obj = re.search('##(.+)##', '##abc##')
    print match_obj.group(1)
    match_obj = re.search('##(.+)##', 'abc')
    # print match_obj.group(1)  # 'NoneType' object has no attribute 'group'


if __name__ == '__main__':
    get_one()
