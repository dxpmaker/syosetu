import json
import os
from urllib import request
from urllib import parse
import ssl

import requests

dir_base = os.path.dirname(os.path.abspath(__file__))
#获取最后的n码
def getOver():
    # https://dev.syosetu.com/man/api/
    params = {
        'lim': 1,
        'out': 'json',
        'st': 1,
        'order': 'ncodeasc'  # ncodeasc 这个属性疑似是正序排列但是未在官方文档
    }
    print = {}
    query_string = parse.urlencode(params)
    info_url = f"https://api.syosetu.com/novelapi/api/?{query_string}"
    content = json.loads(get(info_url))
    print["ncodeasc"] = content[1]["ncode"]
    params['order'] = 'ncodedesc'
    query_string = parse.urlencode(params)
    info_url = f"https://api.syosetu.com/novelapi/api/?{query_string}"
    content = json.loads(get(info_url))
    print["ncodedesc"] = content[1]["ncode"]
    return print
# 创建User-Agent对象
def get_random_ua():
    # ua = UserAgent()
    # headers = ua.random
    # return {'User-Agent':headers}
    return {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
# your spider code
def get(url,retry_count = 5):
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={"http": "http://{}".format(proxy)},headers=get_random_ua())
            # 使用代理访问
            return html
        except Exception as e:
            retry_count -= 1
            print(f'url: {e}')

    # 删除代理池中代理
    delete_proxy(proxy)
    return None
def getDome(info_url,retry_count = 5):
    while retry_count > 0:
        try:
            req = requests.get(info_url, headers=get_random_ua())
            return req.text
        except Exception as e:
            print(f"{e}")