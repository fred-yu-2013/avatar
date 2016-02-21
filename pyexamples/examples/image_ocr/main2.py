# -*- coding: utf-8 -*-

import Image
import ImageChops
import pytesseract
from pytesseract import image_to_string


class ImageF:
    def __init__(self):
        pass

    def to_str(self):
        """
        处理图片，然后OCR
        """
        name = 'test.png'
        img = Image.open(name)

        img = self.__resize(img)

        # 灰度
        img2 = img.convert('L')
        # img2.save('l-' + name)

        # 去杂色
        table = []
        for i in range(256):
            if i == 135 - 1:
                table.append(0)   # 1, 白色, 0, 黑色
            else:
                table.append(1)  # 黑色

        out = img2.point(table, '1')
        out.save('dst-' + name)

        # 转成字符串
        text = image_to_string(out)
        print text

    def to_str2(self):
        """
        处理图片，然后OCR
        """
        name = 'appcaptcha.png'
        img = Image.open(name)

        # img = self.__resize(img)

        # 灰度
        img2 = img.convert('L')
        img2.save('bak2.png')

        # 去杂色
        table = []
        for i in range(256):
            # 1, 白色, 0, 黑色
            if i < 240:
                table.append(0)
            else:
                table.append(1)  # 黑色

        img3 = img2.point(table, '1')
        img3.save('bak3.png')

        img3 = self.__resize(img3)

        # 转成字符串
        text = image_to_string(img3)
        print text

    def __resize(self, img):
        size = img.size
        ratio = 1.5
        width = int(size[0] * ratio)
        height = int(size[1] * ratio)
        out = img.resize((width, height))
        out.save('resize.png')
        return out

    def compare(self):
        src_img = Image.open('mei_price_numbers.png')
        x_gap = 7
        img_width_1 = 7
        img_width_2 = 4
        img_height = 13
        num_imgs = []
        for i in range(11):
            x = i * x_gap
            if i == 10:
                num_img = src_img.crop((x, 0, img_width_2, img_height))
            else:
                num_img = src_img.crop((x, 0, img_width_1, img_height))



img = ImageF()
# img.to_str()
img.to_str2()
