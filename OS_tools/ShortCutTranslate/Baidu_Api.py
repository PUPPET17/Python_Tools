import http.client
import hashlib
import urllib
import random
import json

def baidu_translate(q, from_lang, to_lang, appid, secret_key):
    """
    使用百度翻译API进行文本翻译
    """
    # 构建请求的URL
    http_client = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secret_key
    m1 = hashlib.md5()
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        # 发送HTTP请求
        http_client = http.client.HTTPConnection('api.fanyi.baidu.com')
        http_client.request('GET', myurl)
        # 获取响应
        response = http_client.getresponse()
        json_response = response.read().decode('utf-8')
        result = json.loads(json_response)
        return result
    except Exception as e:
        print(e)
    finally:
        if http_client:
            http_client.close()

# 使用示例
appid = ''  # 替换为你的APP ID
secret_key = ''  # 替换为你的密钥

text_to_translate = "Hello World"
from_lang = 'en'
to_lang = 'zh'

result = baidu_translate(text_to_translate, from_lang, to_lang, appid, secret_key)
print(result)