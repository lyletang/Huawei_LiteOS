# coding=utf8
import http.client
import hashlib
import urllib.parse
import random
import json
import codecs

appid, secretKey = '20170107000035394', 'fm2Qmj34KveDrvTglZ0l'
fromLang, toLang = 'en', 'zh'
translate_api_url = '/api/trans/vip/translate'


def translate_call(query_word):
    httpClient = None
    data = None
    salt = random.randint(32768, 65536)
    sign = appid + query_word + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    myurl = translate_api_url + '?appid=' + appid + '&q=' + urllib.parse.quote(
        query_word) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        res = response.read().decode('utf-8')
        data = json.loads(res)
        # print(data['trans_result'][0]['src'])
        # print(data['trans_result'][0]['dst'])
    except Exception:
        print('Exception')
    finally:
        if httpClient:
            httpClient.close()
    return data['trans_result'][0]['dst']


def normalize_label_list(line):
    line = line.replace('\t', ' ')
    l = line.split('\n')
    l.pop()
    ll = l[0].split(' ')
    number = ll.pop(0)
    label_str = ' '.join(ll)
    label_list = label_str.split(',')
    return label_list


def normalize_translated_word(word, translated_word):
    str = "%s\t%s\n" % (word, translated_word)
    return str


if __name__ == '__main__':
    results = []
    print('开始调用百度翻译API')
    with open('inception/imagenet_synset_to_human_label_map.txt') as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            label_list = normalize_label_list(line)
            for label in label_list:
                label = label.replace(' ', '')
                translated_word = translate_call(label)
                results.append(normalize_translated_word(label, translated_word))
                # print(normalize_translated_word(label, translated_word))
                # print(label, translated_word)
            i += 1
            print('Processing ' + str(i) + '...')
    print('翻译完成')

    print('')

    print('开始写入文件')
    with codecs.open('inception/imagenet_synset_to_human_label_map_zh.txt', "w", "utf-8") as f:
        i = 0
        for result in results:
            f.write(result)
            i += 1
            print('Processing ' + str(i) + '...')
    print('写入完成')
