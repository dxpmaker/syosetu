
import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent
from requests import Session
import socks
import socket
from concurrent.futures import ThreadPoolExecutor
#https://api.openproxylist.xyz/socks4.txt
#https://api.openproxylist.xyz/socks5.txt
class GetProxyIP():
    def __init__(self):
        self.socks4 = 'https://api.openproxylist.xyz/socks4.txt'
        self.socks5 = 'https://api.openproxylist.xyz/socks5.txt'
        self.socks4List = self.getToList(self.socks4)
        # self.socks5List = self.getToList(self.socks5)

    def getToList(self,url):
        list = requests.get(url,timeout=2)
        # print(self.parse_ip_port(list.text))
        return self.filter(self.parse_ip_port(list.text))
    def filter(self,list):
        # print(list)
        threadPool = ThreadPoolExecutor(max_workers=50, thread_name_prefix="test_")

        for i in list:
            # print(i)
            try:
                threadPool.map( self.check_proxy,[i["ip"],i["port"]]) # 这是运行一次test的参数，众所周知map可以让test执行多次，即一个[]代表一个参数，一个参数赋予不同的值即增加[]的长度如从[1]到[1,2,3]
            except Exception as e:
                print(e)
            # if self.check_proxy(i["ip"],i["port"]):
            #     list.delete(i)
        return list

    def check_proxy(self,ip, port):
        try:
            # 设置重连次数
            requests.adapters.DEFAULT_RETRIES = 3
            # IP = random.choice(IPAgents)
            session = Session()
            session.proxy = {
                "http":f"socks4//{ip}:{port}",
                'https':f'socks4://{ip}:{port}'
            }

            # thisIP = "".join(IP.split(":")[0:1])
            # print(thisIP)
            res = requests.get(url="https://icanhazip.com/", timeout=10)
            proxyIP = res.text
            print(proxyIP,ip)
            if (proxyIP == f"{ip}"):
                print(f"IP:{ip}:{port}有效！")
                if self.get_ip_info(ip).get == 'CN':#访问外国网站
                    return False
                return True
            else:
                print(f"IP:{ip}:{port}无效！ 错误地址1")
                return False
        except Exception as e:
            print(f"IP:{ip}:{port}无效 错误地址2！{e}")
            return False

    def get_ip_info(self,ip_address):
        url = f'https://ipinfo.io/{ip_address}/json'
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def parse_ip_port(self,text):
        ip_port_list = text.splitlines()  # 按行分割文本
        result = []
        for item in ip_port_list:
            if item.strip():  # 忽略空行
                ip, port = item.split(':')  # 按冒号分割 IP 和端口
                result.append({'ip': ip.strip(), 'port': port.strip()})  # 创建字典并添加到结果列表

        return result
def dome():

    session = Session()
    ip="100.1.53.24"
    port=5678
    # socks.set_default_proxy(socks.SOCKS4, ip, port)
    # socket.socket = socks.socksocket
    res = requests.get(url="http://icanhazip.com/", timeout=2,proxies={"https://":f"{ip}:{port}"})
    proxyIP = res.text
    print(proxyIP, ip)
    if (proxyIP == f"{ip}"):
        print(True)
if __name__ == '__main__':
    # server = GetProxyIP()
    # 示例 IP 地址
    dome()
    # ip_address = '8.8.8.8'  # Google 的公共 DNS 服务器
    # info = GetProxyIP.get_ip_info(ip_address)
    #
    # if info:
    #     print(f"IP 地址: {info.get('ip')}")
    #     print(f"城市: {info.get('city')}")
    #     print(f"地区: {info.get('region')}")
    #     print(f"国家: {info.get('country')}")
    #     print(f"邮政编码: {info.get('postal')}")
    #     print(f"位置: {info.get('loc')}")
    # else:
    #     print("无法获取 IP 地址信息")