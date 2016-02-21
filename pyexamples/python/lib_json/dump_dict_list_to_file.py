# -*- coding: utf-8 -*-

import json

l = []
for i in range(5):
    d = dict(a=5, b=4, c=6, d='asdfsadf')
    l.append(d)
print l

json.dump( l, open('testing.json','w'), indent=0)
