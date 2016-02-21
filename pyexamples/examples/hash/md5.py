# -*- coding: utf-8 -*-
import hashlib

import datetime


def example1():
    m = hashlib.md5()
    m.update("Nobody inspects")
    print m.digest()
    print m.hexdigest()  # 字符串形式

def example2():
    # 1719416DD6ADB3A35FF385DF448C9088

    target = '1719416DD6ADB3A35FF385DF448C9088'

    sign_obj = r'&v=2015110401&t=1450850711&cinemaId=1012109&cityId=82&imei=&appkey=9&from=0123456789&appver=5.3.0&deviceid=ffffffff-fdbe-bb2d-678d-815f0033c587'
    sign_secrets = [
        '',
        'AB2ZVOnshYN6c9dr',
        "TFhNQ6KOOSPJc8ju",
        'zJwaQBQ553lHr6DfnX02WcJtZF',
        "dPT34E1friLt5WQg",
        'RUQ3RDM4MDU0ODIxMEJEMEJBQTgwQUJDMDQyQzMyOEVvMGFULWQ1R0NBNm01QkNvQ25NT1dGU29ZbnJB',
        "TFhNQ6KOOSPJc8ju",
        'DISCOVERY_H5_SHARE',
    ]

    for sign_secret in sign_secrets:
        src = sign_secret + sign_obj
        # src = src.upper()
        m = hashlib.md5()
        m.update(src.decode('utf-8'))
        #print src
        # print m.hexdigest()
        source_md5 = m.hexdigest().upper()
        print source_md5, 'vs', target
        if source_md5 == target:
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> OK, {}'.format(sign_secret)


chars = [ chr(ord('a') + i) for i in range(26)]
chars.extend([ chr(ord('A') + i) for i in range(26)])
chars.extend([ chr(ord('0') + i) for i in range(10)])
print chars

def is_valid_sign_secret(sign_secret):
    target = '1719416DD6ADB3A35FF385DF448C9088'
    sign_obj = sign_secret + r'v=2015110401&t=1450850711&cinemaId=1012109&cityId=82&imei=&appkey=9&from=0123456789&appver=5.3.0&deviceid=ffffffff-fdbe-bb2d-678d-815f0033c587'
    m = hashlib.md5()
    m.update(sign_obj)
    if m.hexdigest().upper() == '1719416DD6ADB3A35FF385DF448C9088':
        print sign_secret
        assert False

def example3(rstr=''):
    if len(rstr) > 32 - 1:
        return

    global chars, is_valid_sign_secret

    for c in chars:
        is_valid_sign_secret(rstr + c)
        example3(rstr + c)

    if not rstr.replace('a', ''):
        print rstr, datetime.datetime.now()


if __name__ == '__main__':
    # example1()
    example2()
    # example3()
