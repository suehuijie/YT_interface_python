#!/usr/bin/env python
# _*_coding:utf-8_*_
import sys

import allure
import os
import sys

from common.execSql import ExecSql
from common.logs import Log
from common.readData import ReadData
from common.readFile import ReadFile


class BasicLogic(object):
    log = Log()
    url_data = ReadFile().read_urlfile()
    sql_exec = ExecSql('mysql_yt')
    sql_exec_basic = ExecSql('mysql_basic')
    sql = ReadData().read_sqlfile()
    update_data = ReadData().read_updatedata()

class TestSingleOrder(BasicLogic):
    test_data = ReadData().read_testdata()

    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    @allure.story("单票下单接口")
    def test_addr_add(self, yt_headers):
        pass


class TestWaybillManage(BasicLogic):
    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def test_waybill_add(self):
        pass

    def test_111(self):
        # p = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
        # print(p)
        # if p not in sys.path:
        #     sys.path.append(p)
        print(sys.path)
