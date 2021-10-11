# -*- encoding: utf-8 -*-
# Filename         :baidu_photo_spider.py
# Description      :
# Time             :2021/09/09 11:06:28
# Author           :王睿彪
# Email            :robin.wang@nio.com
# Version          :1.0

"""爬虫相关配置"""
import os

# 关键词, 改为你想输入的词即可, 相当于在百度图片里搜索一样
keyword = "车位 积水"

label_name = "waterpool"


# 图片存储位置
Storage_path = '/Users/xt.xie/Documents/temp/' + label_name + "/"
if not os.path.exists(Storage_path):
    os.mkdir(Storage_path)

# 初始数字
initial_number = 0
# 最大下载数量
max_download_images = 5000

# 下列内容一般不需要修改
# 固定网址格式
url_init_first = 'https://image.baidu.com/search/flip?tn=baiduimage&word='

# 表头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.192 Safari/537.36'
}
