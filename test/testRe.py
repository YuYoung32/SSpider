"""
正则表达式的应用，用来判断字符串否符合一定的标准
"""
import re

pat = re.compile("AA")
str = "aasdAAABBAADD"
m = pat.search(str)
m = re.search("asd", str)
m = re.findall("a", str)
m = re.findall("[a-z]", str)

m = re.sub("a", "A", str)  # 在str中用A替换a
print(m)
