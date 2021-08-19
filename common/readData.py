#!/usr/bin/env python
# _*_coding:utf-8 _*_
import os
import yaml
from common.logs import Log


class ReadData(object):
    log = Log()

    def __init__(self):
        self.sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testdata/sql.yaml')
        self.testdata_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testdata/testdata.yaml')
        self.updatedata_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testdata/updatedata.yaml')


    def read_sqlfile(self):
        try:
            with open(self.sql_path, 'r') as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
        except Exception as e:
            self.log.error("读sql_yaml文件报错{}".format(e))

    def read_testdata(self):
        try:
            with open(self.testdata_path, 'r') as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
        except Exception as e:
            self.log.error("读testdata_yaml文件报错{}".format(e))

    def read_updatedata(self):
        try:
            with open(self.updatedata_path, 'r') as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
        except Exception as e:
            self.log.error("读updayedata_yaml文件报错{}".format(e))


if __name__=='__main__':
    test = ReadData().read_updatedata()
    print(test['api']['role_auth'])