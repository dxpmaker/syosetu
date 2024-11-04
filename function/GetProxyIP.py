
import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent

#https://api.openproxylist.xyz/socks4.txt
#https://api.openproxylist.xyz/socks5.txt

class GetProxyIP():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chro'
                      'me/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400'
    }
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
        for i in list:
            print(i)
            if self.check_proxy(i["ip"],i["port"]):
                list.delete(i)
        return list

    def check_proxy(self,ip, port):
        try:
            # 设置重连次数
            requests.adapters.DEFAULT_RETRIES = 3
            # IP = random.choice(IPAgents)
            proxy = f"http://{ip}:{port}"
            # thisIP = "".join(IP.split(":")[0:1])
            # print(thisIP)
            res = requests.get(url="http://icanhazip.com/",headers=self.headers, timeout=10, proxies={"http": proxy})
            proxyIP = res.text
            if (proxyIP == proxy):
                print(f"代理IP:{ip}:{port}有效！")
                if self.get_ip_info(ip).get == 'CN':#访问外国网站
                    return False
                return True
            else:
                print(f"代理IP:{ip}:{port}无效！ 错误地址1")
                return False
        except Exception as e:
            print(f"{e}")
            print(f"代理IP:{ip}:{port}无效 错误地址2！")
        return False

    def get_ip_info(self,ip_address):
        url = f'https://ipinfo.io/{ip_address}/json'
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def parse_ip_port(self,text):
        # 文本中每一行包含一个 IP 及其端口号，以��号分隔。
        ip_port_list = text.splitlines()  # 按行分割文本
        result = []
        for item in ip_port_list:
            if item.strip():  # 忽略空行
                ip, port = item.split(':')  # 按冒号分割 IP 和端口
                result.append({'ip': ip.strip(), 'port': port.strip()})  # 创建字典并添加到结果列表

        return result
def dome():

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chro'
                      'me/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400'
    }
    proxies = {
        "http": "http://185.132.242.212:8083",
        "https": "https://185.132.242.212:8083",
    }
    try:
        response = requests.get("https://icanhazip.com/", proxies=proxies, timeout=10,headers=headers,verify=False)  # 增加超时时间
        print(response.text)
    except requests.exceptions.ProxyError as e:
        print("Proxy error:", e)
    except requests.exceptions.Timeout as e:
        print("Timeout error:", e)
if __name__ == '__main__':
    # server = GetProxyIP()
    dome()
    # 示例 IP 地址
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