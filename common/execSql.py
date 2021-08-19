#!/usr/bin/env python
# _*_coding:utf-8 _*_
import pymysql as pymysql
from common.logs import Log
from common.readFile import ReadFile


class ExecSql(object):
    """
    执行sql语句类
    """
    log = Log()

    def __init__(self, db):
        """
        初始化mysql配置,并连接
        """
        self.sql_conf = ReadFile().read_envfile()[u'易通'][db]

        host = self.sql_conf['host']
        user = self.sql_conf['user']
        password = self.sql_conf['password']
        db = self.sql_conf['db']
        port = self.sql_conf['port']
        charset = self.sql_conf['charset']

        try:
            self.conn = pymysql.connect(host=host,
                                        user=user,
                                        password=password,
                                        db=db,
                                        port=port,
                                        charset=charset)
            # 创建一个游标对象
            self.cur = self.conn.cursor()
        except Exception as e:
            self.log.error("连接数据库失败：{}".format(e))

    def select_one(self, sql):
        """
        查询sql语句返回的第一条数据
        :param sql:
        :return:
        """
        self.cur.execute(sql)
        return self.cur.fetchone()

    def select_all(self, sql):
        """
        查询sql语句返回的所有数据
        :param sql:
        :return:
        """
        self.cur.execute(sql)
        return self.cur.fetchall()

    def update(self, sql):
        """
        增删改操作的方法
        :param sql:
        :return:
        """
        self.cur.execute(sql)
        self.conn.commit()

if __name__=='__main__':
    db = ExecSql('mysql_yt')

    sql = "select count(id) FROM t_basic_address WHERE user_id = 500000560"

    # print(db.select_all(sql))
    # print(db.select_all(sql)[0])
    #
    # print(db.select_one(sql))
    # print(db.select_one(sql)[0])

    print(db.select_one(sql))