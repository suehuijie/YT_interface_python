#!/usr/bin/env python
# _*_coding:utf-8_*_
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

import pytest
from common.login import Login


@pytest.fixture(scope='session')
def yt_headers():
    """
    登录获取token更新headers
    :return:
    """
    token = Login().yt_login('易通')['data']['accessToken']
    auth = 'Bearer ' + token
    headers = {"content-type": "application/json",
               "authorization": auth}
    return headers

@pytest.fixture(scope='session')
def userId():
    userId = Login().yt_login('易通')['data']['userId']
    return userId
