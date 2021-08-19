# _*_coding:utf-8_*_
import requests
from common.logs import Log
from common.readFile import ReadFile


class Login:
    """
    登录
    """
    log = Log()


    def __init__(self):
        self.env_data = ReadFile().read_envfile()[u'易通']
        self.url = self.env_data['url']
        self.headers = self.env_data['headers']
        self.param = self.env_data['param']

    def yt_login(self, project):
        """
        登录
        :return:
        """
        try:
            if project == u'易通':
                result = requests.post(url=self.url, headers = self.headers, json=self.param)
            elif project == 'lxk_a':
                pass
            return result.json()
        except Exception as e:
            self.log.error("登录报错{}".format(e))

if __name__ == '__main__':
    a = Login()
    r = a.yt_login('易通')['data']
    print(r)