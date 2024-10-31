import sys
import os
import time
import re
from urllib import request
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import ssl
#非官方模拟请求
# 本文件所在的目录
dir_base = os.path.dirname(os.path.abspath(__file__))

# 设置代理（如果需要）
proxy = request.ProxyHandler({
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
})
opener = request.build_opener(proxy)
request.install_opener(opener)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

def main(s):
    # 示例 N-code 和重置标志
    ncode = 'n9579io'
    resetFlag = True

    # 验证 N-code 格式
    ncode = ncode.lower()
    if not re.match(r"n[0-9]{4}[a-z]{2}", ncode):
        print("N-code 不正确！！")
        sys.exit(1)

    # 获取小说信息
    info_url = f"https://ncode.syosetu.com/novelview/infotop/ncode/{ncode}/"
    print(info_url)

    # 创建 SSL 上下文；根据需要进行调整
    context = ssl.SSLContext()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    req = request.Request(info_url, headers=headers)
    info_res = request.urlopen(req, context=context)
    try:
        info_res = request.urlopen(req, context=context)
    except Exception:
        print("获取 N-code 信息失败")
        sys.exit(1)
    print(info_res)
    soup = BeautifulSoup(info_res, "html.parser")
    pre_info = soup.select_one("#pre_info").text
    print(pre_info)
    try:
        num_parts = int(re.search(r"全([0-9]+)エピソード", pre_info).group(1))

    except Exception:
        self.getOne()#文章可能是短篇小说
    slef.getList(num_parts)


if __name__ == "__main__":
    main()
def getOne():
    return
def getList(num_parts,ncode):
    # 如果小说目录不存在，则创建
    novel_dir = os.path.normpath(os.path.join(dir_base, ncode))
    if not os.path.exists(novel_dir):
        os.mkdir(novel_dir)

    # 获取已存在的部分编号
    re_part = re.compile(rf"{ncode}_([0-9]+).txt")
    existing_parts = {int(re_part.search(fn).group(1)) for fn in os.listdir(novel_dir) if re_part.search(fn)}

    # 确定需要获取的部分
    fetch_parts = list(range(1, num_parts + 1)) if resetFlag else sorted(set(range(1, num_parts + 1)) - existing_parts)

    num_fetch_rest = len(fetch_parts)
    for part in fetch_parts:
        # 构建小说部分的 URL
        url = f"https://ncode.syosetu.com/{ncode}/{part}/"
        print(url)
        try:
            res = request.urlopen(url, context=context)
            soup = BeautifulSoup(res, "html.parser")

            # 选择主要内容
            honbun = soup.select_one("#novel_honbun").text + "\n"  # 为分隔添加换行符

            # 将内容保存到文件
            name = os.path.join(novel_dir, f"{ncode}_{part}.txt")
            with open(name, "w", encoding="utf-8") as f:
                f.write(honbun)

            # 显示进度
            num_fetch_rest -= 1
            print(f"第 {part} 部下载完成（剩余: {num_fetch_rest} 部）")

            time.sleep(1)  # 在下一次请求前等待 1 秒
        except Exception as e:
            print(f"获取第 {part} 部时出错: {e}")
