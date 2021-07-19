import urllib.request
import urllib.parse
import urllib.error

# 获取一个get
# request = urllib.request.urlopen("https://www.baidu.com")
# print(request.read().decode('utf-8'))

# 获取一个post
# data = bytes(urllib.parse.urlencode({"keyv": "valuev"}), encoding='utf-8')
# request = urllib.request.urlopen("http://httpbin.org/post", data=data)
# print(request.read().decode('utf-8'))

# 超时处理
# try:
#     request = urllib.request.urlopen("http://httpbin.org/get", timeout=1)
#     print(request.read().decode('utf-8'))
# except urllib.error.URLError as e:
#     print("Time out.")

# # request属性
# request = urllib.request.urlopen("http://httpbin.org/get")
# print(request.status)  # 状态码
# print(request.getheaders())  # 头部信息全部
# print(request.getheader("Server"))  # 头部信息的Server

# 伪装成浏览器改变headers
# 构造一个对象
# url = "http://httpbin.org/post"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
# }
# data = bytes(urllib.parse.urlencode({"name": "abc"}), encoding='utf-8')
# req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
# # 发送请求
# response = urllib.request.urlopen(req)
# print(response.read().decode('utf-8'))

# 伪装后访问douban.com
url = "https://www.douban.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
}
req = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))

