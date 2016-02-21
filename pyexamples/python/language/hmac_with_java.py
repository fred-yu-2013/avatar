# -*- coding: utf-8 -*-

import hmac
from hashlib import sha1
import binascii


def compute_hmac():
    """
    key: unsigned char key[16]={0xb0,0x5c,0xb6,0xe7,0xff,0xfb,0xbd,0x0d,0xfd,0xbc,0x10,0xc9,0xf4,0x29,0xa0,0x3b};
    msg: char *p = "this is hmacsha1 test";
    result: b30e55f37ea5a4eef7ce0ba0d67230498fa438ba
    """
    key = '\xb0\x5c\xb6\xe7\xff\xfb\xbd\x0d\xfd\xbc\x10\xc9\xf4\x29\xa0\x3b'
    msg = 'this is hmacsha1 test'
    h = hmac.new(key, msg, sha1)
    result = h.digest()
    print result, type(result)
    print binascii.b2a_hex(result)
    assert binascii.b2a_hex(result) == 'b30e55f37ea5a4eef7ce0ba0d67230498fa438ba'

    key = '123456'
    msg = '123456'
    h = hmac.new(key, msg, sha1)
    result = h.digest()
    print result
    print binascii.b2a_hex(result), len(result)


if __name__ == '__main__':
    compute_hmac()

