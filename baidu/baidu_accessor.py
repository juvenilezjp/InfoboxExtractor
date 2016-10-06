# coding=utf-8

import re
import pymysql
from pymongo import MongoClient
from bson import ObjectId

from baidu.baidu_praser import *


class MysqlFetcher:
    def __init__(self, host, user, pwd, db, tbl):
        self._conn = pymysql.connect(host=host,
                                     user=user,
                                     password=pwd,
                                     db=db)
        self._tbl = tbl

    def fetch(self, start, num):
        sql = "select ID, detailPageId, detailPageUrl, crawlTime from `" + self._tbl + "` limit %s, %s"
        self._conn.ping(True)
        res = []
        with self._conn.cursor() as cursor:
            n = cursor.execute(sql, (start, num))
            for (id, obj_id, url, t) in cursor:
                res.append((id, obj_id, url, t))
        return res


class MysqlPoster:
    def __init__(self, host, user, pwd, db, tbl):
        self._conn = pymysql.connect(host=host,
                                     user=user,
                                     password=pwd,
                                     db=db)
        self._tbl = tbl

    def post_select(self, start, num):
        sql = "select ID, detailPageId, detailPageUrl, crawlTime from `" + self._tbl + "` limit %s, %s"
        self._conn.ping(True)
        res = []
        with self._conn.cursor() as cursor:
            n = cursor.execute(sql, (start, num))
            for (id, obj_id, url, t) in cursor:
                res.append((id, obj_id, url, t))
        return res

    def post_insert(self, content):
        sql = "insert into`" + self._tbl + "`ID, detailPageId, detailPageUrl, crawlTime" + content

        return


class MongoFetcher:
    def __init__(self, addr, db, coll):
        client = MongoClient(addr)
        self._coll = client[db][coll]

    def fetch(self, obj_id):
        return self._coll.find_one({"_id": ObjectId(obj_id)})


class PageError(Exception):
    pass


if __name__ == "__main__":
    mysql_host = "192.168.120.90"
    mysql_user = "root"
    mysql_pwd = "123456"
    mysql_db = "knowledge_base"
    mysql_tbl = "baidu_baike"
    mongo_addr = "mongodb://wsp:wsp123456@192.168.120.90:27017"
    mongo_db = "knowledge_base"
    mongo_coll = "baidu_baike"
    check_reg = re.compile(rb"\xe7\x99\xbe\xe5\xba\xa6\xe7\x99\xbe\xe7\xa7\x91")
    mysql_fetcher = MysqlFetcher(mysql_host, mysql_user, mysql_pwd, mysql_db, mysql_tbl)
    mongo_fetcher = MongoFetcher(mongo_addr, mongo_db, mongo_coll)
    bad = 0
    cur = 0

    # mysql分页查询开始页码
    page_start = 0
    # mysql分页查询结束页码
    page_end = 3
    # 每页的记录的数量
    page_num = 1

    page = page_start
    while page < page_end:
        # print("page:", page)
        for (id, obj_id, url, t) in mysql_fetcher.fetch(page * page_num, page_num):
            cur += 1
            try:
                print(url)
                obj = mongo_fetcher.fetch(obj_id)
                if not check_reg.search(obj["body"]):
                    raise PageError()
                html = obj["body"].decode("utf-8", errors="ignore")
                # print(html)
                # 处理页面html
                # print(html)
                entity = Page('x', html)
                xx, yy = entity.get_infobox()
                if len(xx) != 0:
                    print(entity.get_title(), entity.get_tags(), entity.get_infobox())
                    # print(entity.get_title())

            except PageError:
                bad += 1
        page += 1
    print("bad pages:", bad)
