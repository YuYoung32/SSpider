"""
Tag标签
Navigable标签内容字符串
BeautifulSoup整个文档
Comment注释
"""
import re

from bs4 import BeautifulSoup

file = open("./testBs4.html", "rb")
html = file.read()
bs = BeautifulSoup(html, "html.parser")

print(bs.title)  # 找到第一个标签
print(bs.a)
print(type(bs.title))  # 类型
print(bs)  # 整个文档
print(bs.title.string)  # 内容
print(bs.title.attrs)  # 属性

# 使用规则
# match a string
t_list = bs.find_all("a")
# match a regular
t_list = bs.find_all(re.compile("a"))
# use a function
def name_exist(tag):
    return tag.hasattr("name")
t_list = bs.find_all(name_exist)

# 使用参数
t_list = bs.find_all(id="head")
t_list = bs.find_all(text=["", ""])
t_list = bs.find_all(text=re.compile("\d"))
t_list = bs.find_all("a", limit=3)

# CSS选择器
t_list = bs.select('title')  # 标签
t_list = bs.select('.')  # 类名
t_list = bs.select('#')  # id
t_list = bs.select("a[class = '']")  # 属性
t_list = bs.select("head > title")  # 子标签
t_list = bs.select(". ~ . ")  # 兄弟标签
