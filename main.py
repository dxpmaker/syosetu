import sys
import os
import time
import re
from urllib import request
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import ssl

dir_base = os.path.dirname(os.path.abspath(__file__))
def main():
    params = {
        'param1': 'value1',
        'out': 'json',
        'param3': 'value3'
    }
    proxy = request.ProxyHandler({
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    })
    opener = request.build_opener(proxy)
    request.install_opener(opener)
    info_url = f"https://api.syosetu.com/novelapi/api/"
    #取消ssl验证
    context = ssl.SSLContext()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    response = request.urlopen(info_url,context=context)
    content = response.read().decode('utf-8')
    print(content)
main()