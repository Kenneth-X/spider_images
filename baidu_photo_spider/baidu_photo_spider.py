# -*- encoding: utf-8 -*-
# Filename         :baidu_photo_spider.py
# Description      :
# Time             :2021/09/09 11:06:28
# Author           :王睿彪
# Email            :robin.wang@nio.com
# Version          :1.0

"""根据搜索词下载百度图片"""
from logging import log
import os
import re
from typing import List, Tuple
from urllib.parse import quote
from logger import logger

import requests

from conf import *


def get_page_urls(page_url: str, headers: dict) -> Tuple[List[str], str]:
    """获取当前翻页的所有图片的链接
    Args:
        page_url: 当前翻页的链接
        headers: 请求表头
    Returns:
        当前翻页下的所有图片的链接, 当前翻页的下一翻页的链接
    """
    if not page_url:
        return [], ''
    try:
        html = requests.get(page_url, headers=headers)
        html.encoding = 'utf-8'
        html = html.text
    except IOError as e:
        # print(e)
        logger.error(e)
        return [], ''
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    next_page_url = re.findall(re.compile(r'<a href="(.*)" class="n">下一页</a>'), html, flags=0)
    next_page_url = 'http://image.baidu.com' + next_page_url[0] if next_page_url else ''
    return pic_urls, next_page_url


def down_pic(pic_urls: List[str], max_download_images: int, Storage_path, initial_number) -> None:
    """给出图片链接列表，下载所有图片
    Args:
        pic_urls: 图片链接列表
        max_download_images: 最大下载数量
    """
    pic_urls = pic_urls[:max_download_images]
    for i, pic_url in enumerate(pic_urls):
        try:
            pic = requests.get(pic_url, timeout=15)
            image_output_path = Storage_path + label_name + "_" + str(initial_number + i + 1).zfill(6) + '.jpg'
            with open(image_output_path, 'wb') as f:
                f.write(pic.content)
                logger.info('成功下载第%s张图片: %s' % (str(initial_number + i + 1), str(pic_url)))
                # print('成功下载第%s张图片: %s' % (str(initial_number + i + 1), str(pic_url)))
        except IOError as e:
            logger.error('下载第%s张图片时失败: %s' % (str(initial_number + i + 1), str(pic_url)))
            logger.error(e)
            # print('下载第%s张图片时失败: %s' % (str(initial_number + i + 1), str(pic_url)))
            # print(e)
            continue


if __name__ == '__main__':
    url_init = url_init_first + quote(keyword, safe='/')
    all_pic_urls = []
    page_urls, next_page_url = get_page_urls(url_init, headers)
    all_pic_urls.extend(page_urls)

    page_count = 0  # 累计翻页数

    # 获取图片链接
    while 1:
        page_urls, next_page_url = get_page_urls(next_page_url, headers)
        page_count += 1
        logger.info('正在获取第%s个翻页的所有图片链接' % str(page_count))
        # print('正在获取第%s个翻页的所有图片链接' % str(page_count))
        if next_page_url == '' and page_urls == []:
            logger.info(('已到最后一页，共计%s个翻页' % page_count))
            # print('已到最后一页，共计%s个翻页' % page_count)
            break
        all_pic_urls.extend(page_urls)
        if len(all_pic_urls) >= max_download_images:
            logger.info('已达到设置的最大下载数量%s' % max_download_images)
            # print('已达到设置的最大下载数量%s' % max_download_images)
            break

    down_pic(list(set(all_pic_urls)), max_download_images, Storage_path, initial_number)
