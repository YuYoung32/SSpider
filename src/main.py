from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import xlwt
import sqlite3


def main():
    baseurl = "https://movie.douban.com/top250?start="
    savepathExcel = "../outData/outPutXls.xls"
    savepathDB = "../outData/outputDatabase.db"
    edition = "database"  # excel or database
    saveData(savepathExcel, savepathDB, edition, getData(baseurl))
    print("爬取完成")


# region 全局变量，正则表达式，指定模式
# 详情链接
findLink = re.compile(r'<a href="(.*?)">')  # 正则表达式，item链接
# 影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 忽略换行
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 一句话评价
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 影片相关内容
findDetail = re.compile(r'<p class="">(.*?)</p>', re.S)


# endregion


def askURL(url):
    """
    得到一个URL的网页内容
    @param url:
    @return: request html from the url
    """
    print("ask url...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
    }
    request = urllib.request.Request(url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def normalize(str):
    """
    规范化数据，去除句号，连续空格等
    Args:
        str: a string

    Returns: a normalized string

    """
    str = str.replace("。", "")  # 去除中文句号
    str = str.replace(u"\xa0", " ")  # 去除连续不可分割空格 NBSP /xa0
    str = str.replace("<br/>", "")  # 去除<br/>
    str = str.replace("\n", "")  # 去除/n
    str = re.sub(" +", " ", str)  # 替换连续不可分割空格
    return str.strip()


def putIntoList(link, imgSrc, titles, rating, judgeNum, inq, detail):
    """
    把几个信息存入到一个列表里
    Args:
        link:
        imgSrc:
        titles:
        rating:
        judgeNum:
        inq:
        detail:

    Returns: a integrated list

    """
    data = []

    data.append(link)

    data.append(imgSrc)

    if len(titles) == 2:  # 目的： 不需要别名
        ctitle = titles[0]  # 中文名
        data.append(ctitle)
        otitle = titles[1].replace("/", "")  # 外文名
        data.append(normalize(otitle))
    else:
        data.append(titles[0])
        data.append(" ")

    data.append(rating)

    data.append(judgeNum)

    if len(inq) != 0:  # 可能不存在一句话评价
        data.append(normalize(inq[0]))
    else:
        data.append(" ")

    data.append(normalize(detail))

    return data


def getData(baseurl):
    """
    获取数据
    Args:
        baseurl:

    Returns: a 2-dimension datalist(film_amount * data_item)

    """
    datalist = []
    # 共10*25条
    cnt = 0
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)
        # 解析html
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', {"class": "item"}):
            cnt = cnt + 1
            print("get data item" + str(cnt))
            item = str(item)
            # print(item) #测试节点1，能够输出单个item
            link = re.findall(findLink, item)[0]  # 找到每部影片唯一的详情链接
            imgSrc = re.findall(findImgSrc, item)[0]
            titles = re.findall(findTitle, item)
            rating = re.findall(findRating, item)[0]
            judgeNum = re.findall(findJudge, item)[0]
            inq = re.findall(findInq, item)
            detail = re.findall(findDetail, item)[0]

            data = putIntoList(link, imgSrc, titles, rating, judgeNum, inq, detail)
            datalist.append(data)
    # print(datalist)  # 测试点2，打印所有数据
    return datalist


def initDatabase(savePathDB):
    """
    初始化数据库，在指定位置创建数据库，并建表
    Args:
        savePathDB:

    """
    print("初始化数据库...")
    conn = sqlite3.connect(savePathDB)
    print("连接成功")
    cur = conn.cursor()
    initSql = """
        create table if not exists filmData(
            id integer primary key autoincrement,
            info_link text ,
            pic_link text ,
            ch_name varchar ,
            en_name varchar ,
            score numeric ,
            rated integer ,
            introduction text,
            info text
        )
    """
    cur.execute(initSql)
    conn.commit()
    conn.close()
    print("初始化完成")


def saveData(savePathExcel, savePathDB, edition, datalist):
    """
    保存数据到excel或database
    Args:
        savePathExcel:
        datalist:
        edition: a string: "excel" or "database"

    """
    if edition == "excel":
        book = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)  # 可以覆写
        col = ("详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
        for i in range(0, 8):
            sheet.write(0, i, col[i])
        for i in range(0, 250):
            data = datalist[i]  # 一部电源的信息
            for j in range(0, 8):
                sheet.write(i + 1, j, data[j])
        print("save ...")
        book.save(savePathExcel)  # 保存文件
        print("saved! file path: " + savePathExcel)
    elif edition == "database":
        initDatabase(savePathDB)
        conn = sqlite3.connect(savePathDB)
        cur = conn.cursor()
        cnt = 0
        for data in datalist:  # 取出一行
            for index in range(len(data)):  # 对一行中的每一个数据项操作
                data[index] = '"' + data[index] + '"'  # 把一个数据项整个转换成数据库的字符串形式，"item"
                datastr = ",".join(data)  # 列表中的元素用','相连，连接成一个字符串
            insertSql = '''
            insert into filmData
            (info_link, pic_link, ch_name, en_name, score, rated, introduction, info)
            values(%s)''' % datastr
            cur.execute(insertSql)
            conn.commit()
            cnt = cnt + 1
            print("insert into item" + str(cnt))
        cur.close()
        conn.close()

    else:
        print("failed! the wrong edition!")


if __name__ == '__main__':
    main()
