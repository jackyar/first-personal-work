# @coding:utf-8
# @author:jackyar
# @time:2021.02.20

'''
    抓取腾讯视频《在一起》中的评论信息
    腾讯视频的评论是通过ajax异步加载生成，通过过滤器和简单抓包发现其中的规律
    评论信息的url地址中cursor字段和尾部数字串发生改变, 通过页面数据的last字段获取下一cursor的值

    把页面数据的源码字符串做简单处理后，转从python字典数据类型，并提取信息
    最后将信息保存到文件，交由word_count.py做分词处理
'''
import requests
from requests.exceptions import RequestException
import re
import json
import time

def get_page(base_url, cursor, tail): # 获取页面源代码
    url = base_url.format(str(cursor), str(tail))
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
    }
    response = requests.get(url, headers=header)
    source = response.content.decode()
    try:
        if response.status_code == 200:
            return source
        return response.status_code
    except RequestException:
        return None

def parse_page(source): # 解析构造出来的json页面
    string_json = re.search('.*?\((.*)\)', source, re.S).group(1) # 提取中间符合json格式的字符串
    source_json = json.loads(string_json) # 将网页源码字符串转成json格式
    items = source_json.get("data").get("oriCommList") # 获取包含评论的部分
    buff_list = list()
    for item in items:
        buff_list.append(item.get("content"))
    write_to_local(buff_list)
    return source_json.get("data").get("last")

def write_to_local(buff_list):
    with open('../data/video-comments.txt', 'a', encoding='utf-8') as file:
        for item in buff_list:
            print("SPIDER -CRWAL TENCENT COMMENT @ITEM: " + item)
            file.write(item)

def main():
    base_url = 'https://video.coral.qq.com/varticle/5963120294/comment/v2?' \
          'callback=_varticle5963120294commentv2&orinum=10&oriorder=o&pageflag=1' \
          '&cursor={}&scorecursor=0&orirepnum=2&reporder=o&' \
          'reppageflag=1&source=132&_={}'

    cursor = 6716721678028090367
    tail = 1613808784355
    while True:
        source = get_page(base_url, cursor, tail)
        cursor = parse_page(source)
        tail += 1
        time.sleep(2)  # 为确保程序安全运行，选择爬取一页后延时2秒

if __name__ == '__main__':
    main()