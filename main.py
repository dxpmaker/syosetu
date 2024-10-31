import sys
import os
import time
import re
from urllib import request
from urllib import parse
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import ssl

dir_base = os.path.dirname(os.path.abspath(__file__))
def main():
    #https://dev.syosetu.com/man/api/
    #n码逻辑为
    params = {
        'lim': 500,
        'out': 'json',
        'st': 2000,
        'order':'ncodedesc'#ncodeasc 这个属性疑似是正序排列但是未在官方文档
    }
    proxy = request.ProxyHandler({
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    })
    opener = request.build_opener(proxy)
    request.install_opener(opener)
    query_string = parse.urlencode(params)
    info_url = f"https://api.syosetu.com/novelapi/api/?{query_string}"
    print(info_url)
    #取消ssl验证
    context = ssl.SSLContext()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    response = request.urlopen(info_url,context=context)
    content = response.read().decode('utf-8')
    print(content)
main()