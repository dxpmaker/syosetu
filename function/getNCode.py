import sys
import os
import threading
import time
import re
from pickle import PROTO
from urllib import request
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import ssl
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from urllib import parse
import json
from fake_useragent import UserAgent
import requests

from function.file import get_dir, write_log, input_SQL
from function.getFunction import get

def get_body(ncode):
    # 示例 N-code 和重置标志
    ncode = ncode.lower()

    # 获取小说信息
    info_url = f"https://ncode.syosetu.com/novelview/infotop/ncode/{ncode}/"


    try:
        soup = BeautifulSoup(get(info_url), "html.parser")
        pre_info = soup.select_one("#pre_info").text
    except Exception:
        print(f"获取 N-code:{ncode} 信息失败")
        write_log("nocode.txt",info_url)
        return None
    try:
        num_parts = int(re.search(r"全([0-9]+)エピソード", pre_info).group(1))
        get_list(num_parts, ncode)
    except Exception:
        try:
            get_one(ncode)  # 文章是短篇小说
        except Exception:
            write_log("ErrorNCode", info_url)
            print(f"请求失败疑似n码{ncode}不存在",ncode)
            return None
    try:
        save_ncode(ncode,soup)
    except Exception:
        write_log("type",info_url)

def get_one(ncode):
    print('获取短篇')
    novel_dir = get_dir(ncode)
    info_url = f"https://ncode.syosetu.com/{ncode}/"
    res = get(info_url)
    soup = BeautifulSoup(res, "html.parser")
    # 将内容保存到文件
    write_file(soup,novel_dir,f"{ncode}.txt")
    # 显示进度
    print(f"下载完成")
def get_list(num_parts, ncode):
    novel_dir = get_dir(ncode)
    # 获取已存在的部分编号
    re_part = re.compile(rf"{ncode}_([0-9]+).txt")
    existing_parts = {int(re_part.search(fn).group(1)) for fn in os.listdir(novel_dir) if re_part.search(fn)}
    # 确定需要获取的部分
    fetch_parts = list(range(1, num_parts + 1)) if True else sorted(
        set(range(1, num_parts + 1)) - existing_parts)
    num_fetch_rest = len(fetch_parts)
    for part in fetch_parts:
        # 构建小说部分的 URL
        info_url = f"https://ncode.syosetu.com/{ncode}/{part}/"
        try:
            res = get(info_url)
            soup = BeautifulSoup(res, "html.parser")
            write_file(soup,novel_dir,f"{ncode}_{part}.txt")
            # 显示进度
            num_fetch_rest -= 1
            print(f"第 {part} 部下载完成（剩余: {num_fetch_rest} 部）")
            time.sleep(1)  # 在下一次请求前等待 1 秒
        except Exception as e:
            print(f"获取第 {part} 部时出错: {e}")
            write_log("list",info_url)
def write_file(soup,novel_dir,txt_name):
    novel_body = soup.find(class_='p-novel__body')
    if novel_body:
        # 清空标签，只保留文本
        for tag in novel_body.find_all(True):  # True 代表所有标签
            tag.unwrap()  # 移除标签但保留其内容
        # 获取文本内容
        cleaned_text = novel_body.get_text()
        name = os.path.join(novel_dir, txt_name)
        with open(name, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
    else:
        raise Exception('保存失败')
def save_ncode(ncode,soup):
    table =soup.select_one("#noveltable1")
    headers = [th.text for th in table.find_all('th')]
    rows = [ncode]
    for row in table.find_all('tr'):  # 跳过表头行
        cols = [td.text for td in row.find_all('td')]
        rows.append(cols[0].replace('\n', ''))
    input_SQL(rows)

if __name__ == "__main__":
    get_body("N0927A")
    # getBody("N7455IY")