import sys
import os
import time
import re
from urllib import request
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import ssl
import urllib.request



# このファイルがあるディレクトリ
dir_base = os.path.dirname(os.path.abspath(__file__))
proxy = request.ProxyHandler({
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
})
opener = request.build_opener(proxy)
request.install_opener(opener)
# def get_args():
#     parser = ArgumentParser()
#     parser.add_argument("ncode", type=str,
#                         help="N-code")
#     parser.add_argument("--reset", "-r", action="store_true",
#                         help="delete and refetch all parts")
#     args = parser.parse_args()
#     return args


def main():
    # args = get_args()
    # ncode = args.ncode
    # resetFlag = args.reset
    ncode = 'n9579io'
    resetFlag = True
    # ncodeのバリデーションチェック
    ncode = ncode.lower()
    if not re.match(r"n[0-9]{4}[a-z]{2}", ncode):
        print("1Incorrect N-code!!")
        sys.exit(1)

    # 全部分数を取得
    info_url = "https://ncode.syosetu.com/novelview/infotop/ncode/{}/".format(ncode)
    print(info_url)
    context = ssl.create_default_context(cafile="assets/ncode.syosetu.com.pem")
    # info_res = request.urlopen(info_url)
    try:
        info_res = request.urlopen(info_url,context=context)
    except Exception:
        print("2Incorrect N-code!!")
        sys.exit(1)
    soup = BeautifulSoup(info_res, "html.parser")
    pre_info = soup.select_one("#pre_info").text
    num_parts = int(re.search(r"全([0-9]+)部分", pre_info).group(1))

    # 小説を保存するディレクトリがなければ作成
    novel_dir = os.path.normpath(os.path.join(dir_base, "{}".format(ncode)))
    if not os.path.exists(novel_dir):
        os.mkdir(novel_dir)

    # すでに保存している部分番号のsetを取得
    re_part = re.compile(r"{}_([0-9]+).txt".format(ncode))
    existing_parts = {int(re_part.search(fn).group(1)) for fn in os.listdir(novel_dir)}

    # 新たに取得すべき部分番号のリストを生成
    # resetFlagがTrueならすべての部分を取得する
    if resetFlag:
        fetch_parts = list(range(1, num_parts + 1))
    else:
        fetch_parts = set(range(1, num_parts + 1)) - existing_parts
        fetch_parts = sorted(fetch_parts)

    num_fetch_rest = len(fetch_parts)
    for part in fetch_parts:
        # 作品本文ページのURL
        url = "https://ncode.syosetu.com/{}/{:d}/".format(ncode, part)

        res = request.urlopen(url)
        soup = BeautifulSoup(res, "html.parser")

        # CSSセレクタで本文を指定
        honbun = soup.select_one("#novel_honbun").text
        honbun += "\n"  # 次の部分との間は念のため改行しておく

        # 保存
        name = os.path.join(novel_dir, "{}_{:d}.txt".format(ncode, part))
        with open(name, "w", encoding="utf-8") as f:
            f.write(honbun)

        # 進捗を表示
        num_fetch_rest = num_fetch_rest - 1
        print("part {:d} downloaded (rest: {:d} parts)".format(
            part, num_fetch_rest))

        time.sleep(1)  # 次の部分取得までは1秒間の時間を空ける


if __name__ == "__main__":
    main()