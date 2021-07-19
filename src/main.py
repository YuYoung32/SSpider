from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3


def main():
    baseurl = "https://movie.douban.com/top250?start="
    savepath = "../"  # todo

    datalist = getData(baseurl)
    saveData(savepath)


def getData(baseurl):
    """
    爬取网页
    @param baseurl:
    @return:
    """
    datalist = []
    return datalist


def saveData(savePath):
    """
    保存数据
    @param savePath:
    @return:
    """
    print("save ...")

if __name__ == "main":
    main()
