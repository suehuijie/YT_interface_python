#!/usr/bin/env python
# _*_coding:utf-8 _*_
import io
import os
import yaml
from common.logs import Log


class ReadFile(object):
    log = Log()

    def __init__(self):
        self.env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/uat.yaml')
        self.url_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/url.yaml')

    def read_envfile(self):
        try:
            with open(self.env_path, 'r') as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
        except Exception as e:
            self.log.error("读uat_yaml文件报错{}".format(e))

    def read_urlfile(self):
        try:
            with open(self.url_path, 'r') as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
        except Exception as e:
            self.log.error("读url_yaml文件报错{}".format(e))



if __name__=='__main__':
    test = ReadFile()
    # print(test.read_Envfile())
    # print(test.read_Urlfile())
    #

