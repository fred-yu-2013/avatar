# -*- coding: utf-8 -*-

"""
图片转文字的库，需要安装pytesseract库

    - easy_install.exe pytesseract

Hello

    - https://pypi.python.org/pypi/pytesseract
    - http://www.cnblogs.com/way_testlife/archive/2011/04/20/2022997.html
    - http://effbot.org/zone/pil-comparing-images.htm

"""
import math
import operator

# from PIL import Image

import Image
import ImageChops

import pytesseract

# # OCR
#
# img = Image.open(r'C:\Python27\Lib\site-packages\pytesseract-0.1.6-py2.7.egg\pytesseract\test.png')
# img.load()
# img.split()
#
# print pytesseract.image_to_string(img)
# # print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))

# 比较图片

def img_diff(img1, img2):
    """
    比较图片内容差多少，0.0表示完全一样
    :param img1:
    :param img2:
    :return:
    """
    h1 = img1.histogram()
    h2 = img2.histogram()

    rms = math.sqrt(reduce(operator.add,
        map(lambda a,b: (a-b)**2, h1, h2)) / len(h1))
    return rms

def equal(im1, im2): # 图片是否相当，似乎没用
    return ImageChops.difference(im1, im2).getbbox() is None

# def rmsdiff(im1, im2):
#     "Calculate the root-mean-square difference between two images"
#
#     h = ImageChops.difference(im1, im2).histogram()
#
#     # calculate rms
#     return math.sqrt(reduce(operator.add,
#             map(lambda h, i: h*(i**2), h, range(256))
#         ) / (float(im1.size[0]) * im1.size[1]))

img1 = Image.open("test.png")
img2 = Image.open("test2.png")
img3 = Image.open("test-crop.png")

# print equal(img, img3)
# print rmsdiff(img, img3)

bbox = (0, 0, 20, 20)
working_slice1 = img1.crop(bbox)  # 裁剪出新的Image对象，原始对象不变
working_slice1_1 = img1.crop(bbox)
# working_slice.save("test-crop.png")
working_slice2 = img2.crop((20, 0, 20, 20))

# working_slice.load()
# working_slice2.load()

# print equal(working_slice, working_slice2)

print img_diff(img1, img2)  # 0.0
print img_diff(img1, working_slice2)  # 210.45902214
print img_diff(img1, working_slice1)  # 193.450252003
print img_diff(working_slice1, working_slice1_1)  # 0.0

