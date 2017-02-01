# /usr/bin/env python
# coding=utf8

import http.client
import hashlib
import urllib.parse
import random
import json

appid = '20170107000035394'
secretKey = 'fm2Qmj34KveDrvTglZ0l'

httpClient = None
myurl = '/api/trans/vip/translate'
q = 'laptop'
fromLang = 'en'
toLang = 'zh'
salt = random.randint(32768, 65536)

sign = appid + q + str(salt) + secretKey
m1 = hashlib.md5()
m1.update(sign.encode('utf-8'))
sign = m1.hexdigest()
myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
    q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

try:
    httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)

    # response是HTTPResponse对象
    response = httpClient.getresponse()
    res = response.read().decode('utf-8')
    data = json.loads(res)
    print(data)
    print(data['trans_result'][0]['src'])
    print(data['trans_result'][0]['dst'])
except Exception:
    print('Exception')
finally:
    if httpClient:
        httpClient.close()
