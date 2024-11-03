'''
遇到问题没人解答？小编创建了一个Python学习交流QQ群：778463939
寻找有志同道合的小伙伴，互帮互助,群里还有不错的视频学习教程和PDF电子书！
'''
import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent


class GetProxyIP(object):
    def __init__(self):
        self.url = 'https://www.xicidaili.com/nn/'
        self.proxies = {
            'http': 'http://163.204.247.219:9999',
            'https': 'http://163.204.247.219:9999'}

    # 随机生成User-Agent
    def get_random_ua(self):
        ua = UserAgent()  # 创建User-Agent对象
        useragent = ua.random
        return useragent

    # 从西刺代理网站上获取随机的代理IP
    def get_ip_file(self, url):
        headers = {'User-Agent': self.get_random_ua()}
        html = requests.get(url=url, proxies=self.proxies, headers=headers, timeout=5).content.decode('utf-8', 'ignore')
        parse_html = etree.HTML(html)
        tr_list = parse_html.xpath('//tr')  # 基准xpath，匹配每个代理IP的节点对象列表

        for tr in tr_list[1:]:
            ip = tr.xpath('./td[2]/text()')[0]
            port = tr.xpath('./td[3]/text()')[0]
            self.test_proxy_ip(ip, port)  # 测试ip:port是否可用

    # 测试抓取的代理IP是否可用
    def test_proxy_ip(self, ip, port):
        proxies = {
            'http': 'http://{}:{}'.format(ip, port),
            'https': 'https://{}:{}'.format(ip, port), }
        test_url = 'http://www.baidu.com/'
        try:
            res = requests.get(url=test_url, proxies=proxies, timeout=8)
            if res.status_code == 200:
                print(ip, ":", port, 'Success')
                with open('proxies.txt', 'a') as f:
                    f.write(ip + ':' + port + '\n')
        except Exception as e:
            print(ip, port, 'Failed')

    def main(self):
        for i in range(1, 1001):
            url = self.url.format(i)
            self.get_ip_file(url)
            time.sleep(random.randint(5, 10))


if __name__ == '__main__':
    spider = GetProxyIP()
    spider.main()
