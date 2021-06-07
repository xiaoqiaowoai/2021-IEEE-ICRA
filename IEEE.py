#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author: kouguozhao
# DateTime: 2021-6-5 14:30:57

"""
此程序用于爬取 2021 IEEE International Conference on Robotics and Automation (ICRA) 上的论文，并对其根据关键词分类
https://ras.papercept.net/conferences/conferences/ICRA21/program/ICRA21_ProgramAtAGlanceWeb.html

环境：python3.6
依赖包：
    requests
    beautifulsoup4
    pyquery
    lxml
"""


import requests
from bs4 import BeautifulSoup


urls = [
    "https://ras.papercept.net/conferences/conferences/ICRA21/program/ICRA21_ContentListWeb_1.html",
    "https://ras.papercept.net/conferences/conferences/ICRA21/program/ICRA21_ContentListWeb_2.html",
    "https://ras.papercept.net/conferences/conferences/ICRA21/program/ICRA21_ContentListWeb_3.html"
]
keyword = {
    "视觉":[
        "view",
        "vision",
        "visual"
],
    "检测":[
        "detection",
        "detect"
        "test",
        "inspection",
        "inspect",
        "testing"
    ],
    "分割":[
        "segmentation",
        "segment",
        "split",
        "splitting"
    ],
    "领域自适应":[
        "adaptive",
        "adaptation",
        "adaption"
    ],
    "迁移学习":[
        "transfer learning"
    ]

}


def classify_paper(title):
    title = str.lower(title)
    for category,values in keyword.items():
        for key_value in values:
            if key_value in title:
                return category
    return ""


def txt_wt(file, values):
    pass


def clear_txt():
    """
    清空存储文本内容
    :return:
    """
    for path in keyword:
        open("%s.txt" % path, "w").close()
    return 1


def get_request(url):
    """
        获得response
    :param url: 网址
    :return: 返回一个response
    """
    return requests.get(url)


def get_bsobj(resp):
    """
     将网页源码构造成BeautifulSoup对象，方便操作
    :return:
    """
    return BeautifulSoup(resp.content,'lxml')


if __name__ == '__main__':
    clear_txt()
    for url in urls:
        resp = get_request(url)
        bsobj = get_bsobj(resp)
        table_list = bsobj.find_all('table', "trk")

        # 遍历每一个table
        for tb in table_list:
            # 首先看会议标题，依据标题分类
            awardSessionName = str(tb.find_all("b")[1].string)  # 获取当前table的会议标题
            print("找到会议标题:" + awardSessionName)
            # 找到合适分类，输出内容
            category = classify_paper(awardSessionName)
            if category is not "":
                print("\033[0;32;40m会议：%s  -----  符合匹配！！！！,包含论文如下：\033[0m" % awardSessionName)
            path = ""
            titles = tb.find_all("tr", "pHdr")
            # 遍历论文并输出
            for paper_title in titles:
                title_element = paper_title.next_sibling.next_sibling # 获得标题节点，节点后有空格所以多一次向后寻找兄弟节点
                paper_title = str(title_element.string)
                # 判断会议题目是否符合
                if category is not "":

                    path = category
                    print("\033[0;32;40m论文：%s\033[0m" % paper_title)
                # 判断论文标题是否符合
                elif classify_paper(paper_title) is not "":
                    path = classify_paper(paper_title)
                    print("\033[0;32;40m论文：%s  -----  符合匹配！！！！\033[0m" % paper_title)
                else:
                    continue
                f = open("%s.txt" % path, "a+", encoding="utf-8")
                f.write("论文标题：" + str(paper_title) + "\n")
                paper_author_element = title_element.next_sibling.next_sibling.next_sibling.next_sibling
                f.write("-------" + "作者姓名" + "--------------" + "学习工作单位" + "-------\n")
                while (paper_author_element):
                    if paper_author_element.has_attr('class'):
                        break
                    paper_author_info = paper_author_element.stripped_strings

                    for s in paper_author_info:
                        f.write("-------" + str(s) + "-------")

                    paper_author_element = paper_author_element.next_sibling.next_sibling
                    f.write("\n")

                f.write("\n")
                f.close()

    print("\033[0;32;40mOK！！！！！！！\033[0m")
