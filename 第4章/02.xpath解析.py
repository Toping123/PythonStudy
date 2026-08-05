import requests
from requests import Response
from lxml import etree

"""
语法	说明
//div	                    全局查找所有 div，不限层级
/div	                    从根节点直接找 div
./a	                        当前节点下的 a 标签（相对路径）
@class="xxx"	            属性匹配 [@class="list"]
contains(@class,"xxx")	    类包含，适合多 class：//div[contains(@class,"item")]
text()	                    获取标签内部文本
@href	                    获取 href 属性值
//li[1]	                    取第 1 个 li（xpath 下标从 1 开始，不是 0！）
//li[last()]	            最后一个 li
"""


def request(url) -> Response:
    """
    请求
    :param url: 请求地址url
    :return: 请求结果
    """
    res = requests.get(url)
    # print(f"请求结果：{res.text}")
    return res


def xpath_parse() -> list:
    """
    xpath解析xml数据
    :return: 解析后的List
    """
    res = request("https://www.tiobe.com/tiobe-index/")
    tree = etree.HTML(res.text)
    column_list = []
    tops = tree.xpath("//*[@id='top20']/thead/tr/th/text()")
    column_list.append(tops)
    rows = tree.xpath("//*[@id='top20']/tbody/tr")
    for row in rows:
        row_list = []
        for td in row.xpath("td"):
            row_list.append(td.text)
        column_list.append(row_list)
    return column_list


if __name__ == "__main__":
   colum_list =  xpath_parse()
   for item in colum_list:
       print(item)
