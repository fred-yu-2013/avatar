# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import re


def example1():
    # #　例子
    # doc = ['<html><head><title>Page title</title></head>',
    #    '<body><p id="firstpara" align="center">This is paragraph <b>one</b>.',
    #    '<p id="secondpara" align="blah">This is paragraph <b>two</b>.',
    #    '</html>']
    # soup = BeautifulSoup(''.join(doc))

    # 单个字符串
    doc = '<html><head><title>Page title</title></head>' +\
       '<body><p id="firstpara" align="center">This is paragraph <b>one</b>.' +\
       '<p id="secondpara" align="blah">This is paragraph <b>two</b>.' +\
       '</html>'
    soup = BeautifulSoup(doc)

    prettify = soup.prettify()
    name = soup.contents[0].name

    # 查找，并操作查找到的结果
    head = soup.find('head')  # 获取单个子节点
    title = head.title  # 获取标签名称
    title_name = title.name
    # 必须不包含子标签，否则为None，此时可以考虑去text的属性
    title_content = title.string  # 获取内容

    body = soup.find('body')
    ps = body.findAll('p')  # 获取多个子节点
    for p in ps:
        p_id = p['id']  # 获取属性
        pass

    p_by_attr = soup.find('p', attrs={'id': 'firstpara'})  # 按属性查找（为什么不用unicode？）
    p_id = p_by_attr['id']

    pass


if __name__ == '__main__':
    example1()
