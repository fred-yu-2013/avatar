# -*- coding: utf-8 -*-

import requests
import urllib
import httplib
import json

url = 'http://testauth.paopaoyun.com:8080/auth/api/auth/relayServerManager/token'
values = {'serialNo': '6ca1000b4f10e8a1', '_action': 'create'}
headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(values), headers=headers)
# r = requests.put(url, params=json.dumps(values), headers=headers)
# r = requests.put(url, data=values, headers=headers)
# print dir(r)
print r.status_code
print r.text
print type(r.text)
content = json.loads(r.text)
print content.keys()

# conn = httplib.HTTPConnection('testauth.paopaoyun.com',8080)
# body = urllib.urlencode(values)
# conn.request('POST', '/auth/api/auth/relayServerManager/token', body, headers)
# r = conn.getresponse()
# print r.read()

