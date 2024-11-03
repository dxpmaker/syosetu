import random
import requests


class BaiduSpider(object):
    def __init__(self):
        self.url = 'https://ncode.syosetu.com/novelview/infotop/ncode/n0927a'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.flag = 1

    def get_proxies(self):
        with open('proxies.txt', 'r') as f:
            result = f.readlines()                  # 读取所有行并返回列表
        proxy_ip = random.choice(result)[:-1]       # 获取了所有代理IP
        L = proxy_ip.split(':')
        proxy_ip = {
            'http': 'http://{}:{}'.format(L[0], L[1]),
            'https': 'https://{}:{}'.format(L[0], L[1])
        }
        return proxy_ip

    def get_html(self):
        proxies = self.get_proxies()
        if self.flag <= 3:
            try:
                html = requests.get(url=self.url, proxies=proxies, headers=self.headers, timeout=5).text
                print(html)
            except Exception as e:
                print('Retry')
                self.flag += 1
                self.get_html()


if __name__ == '__main__':
    spider = BaiduSpider()
    spider.get_html()
