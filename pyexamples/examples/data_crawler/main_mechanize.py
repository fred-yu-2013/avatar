#coding:utf-8
__author__ = 'Fred'

"""
本文件演示了如何抓取到http://piao.huo.com/的电影名称列表
"""

import mechanize
from BeautifulSoup import BeautifulSoup
import urllib2


br = mechanize.Browser()
response = br.open("http://piao.huo.com/")
# print br.title()
print response.geturl()
# print response.info()  # headers
# print response.read()  # body
# print response.code

# for link in br.links():
#     # print link.url
#     print link.url

# url= 'http://piao.huo.com/'
# page = urllib2.urlopen(url)
# soup = BeautifulSoup(page.read())

htmlTxt = response.read()
# print htmlTxt

soup = BeautifulSoup(htmlTxt)
# soup.
rank = soup.find("div", {"class": "mv_clum2"})
# print rank.name
# print rank

mitems = soup.findAll('li', {"class": "clearfix"})
# print mitems[0].name
# print mitems[0].next
# print mitems[0].contents[1]

for item in mitems:
    # print '>>>>>>>>>>>>>> li'
    # print item.name
    divs = item.findAll('div')
    # print divs[0].find['a', ]
    print divs[0].a['title']