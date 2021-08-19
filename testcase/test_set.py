#!/usr/bin/env python
# _*_coding:utf-8_*_
import datetime
import pytest
import requests
import allure

from common.execSql import ExecSql
from common.logs import Log
from common.readData import ReadData
from common.readFile import ReadFile


@pytest.mark.usefixtures('yt_headers')
@pytest.mark.usefixtures('userId')

class BasicLogic(object):
    log = Log()
    url_data = ReadFile().read_urlfile()
    sql_exec = ExecSql('mysql_yt')
    sql_exec_basic = ExecSql('mysql_basic')
    sql = ReadData().read_sqlfile()
    update_data = ReadData().read_updatedata()


@allure.feature("API设置")
class TestAPI(BasicLogic):

    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    @allure.story("查询api数据接口")
    def test_api_list(self, yt_headers, userId):
        res_db = self.sql_exec.select_one(self.sql['api']['list'].format(userId))
        self.log.info("查询sql数据结果为{}".format(res_db))

        response = requests.post(url=self.url_data['api']['list_api'],
                                 headers=yt_headers)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['apiKey'] == res_db[0]
        assert response.json()['apiToken'] == res_db[1]

    @allure.story("更新api数据接口")
    def test_api_update(self, yt_headers):
        response = requests.put(url=self.url_data['api']['update_api'],
                                 headers = yt_headers)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200


@allure.feature("地址管理")
class TestAddress(BasicLogic):

    test_data = ReadData().read_testdata()

    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    @allure.story("新增地址接口")
    @allure.title("用例标题：{title}")
    @pytest.mark.parametrize("test_input, expected, title", test_data['set']['address_data'])
    def test_addr_add(self, test_input, expected, title, yt_headers, userId):
        addrcount_before = self.sql_exec.select_one(self.sql['address']['count'].format(userId))
        self.log.info("新增地址前，查询sql数据结果为{}".format(addrcount_before[0]))

        response = requests.post(url=self.url_data['address']['add_addr'],
                                 headers = yt_headers,
                                 json=test_input)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        addrcount_after = self.sql_exec.select_one(self.sql['address']['count'].format(userId))
        self.log.info("新增地址后，查询sql数据结果为{}".format(addrcount_after[0]))

        assert response.json()['message'] == expected['message']
        assert response.json()['status'] == expected['status']
        if response.json()['status'] == 200 and response.json()['message'] == 'OK':
            assert int(addrcount_after[0]) == int(addrcount_before[0]) + 1

    @allure.title("修改地址接口")
    def test_addr_update(self, yt_headers, userId):
        id = self.sql_exec.select_one(self.sql['address']['id'].format(userId))[0]
        data = self.update_data['set']['address_data']
        data['id'] = id
        print(data)

        response = requests.post(url=self.url_data['address']['update_addr'],
                                 headers = yt_headers,
                                 json=data)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200


    @allure.title("删除地址接口")
    def test_addr_delete(self, yt_headers, userId):

        data_list = self.sql_exec.select_all(self.sql['address']['id'].format(userId))
        data = {"userIds": [userId]}
        id_list = []
        for i in range(0, len(data_list)):
            id_list.append(str(data_list[i][0]))
        data["ids"] = id_list

        response = requests.post(url=self.url_data['address']['delete_addr'],
                                 headers = yt_headers,
                                 json=data)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200


@allure.feature("店铺管理")
class TestShop(BasicLogic):
    test_data = ReadData().read_testdata()

    def setup_class(self):
        pass

    def teardown_class(self):
        self.sql_exec.update(self.sql['shop']['clear'])

    @allure.story("新增店铺接口")
    @allure.title("用例标题：{title}")
    @pytest.mark.parametrize("test_input, expected, title", test_data['set']['shop_data'])
    def test_shop_add(self, test_input, expected, title, yt_headers, userId):
        addrcount_before = self.sql_exec.select_one(self.sql['shop']['count'].format(userId))
        self.log.info("新增店铺前，查询sql数据结果为{}".format(addrcount_before[0]))

        response = requests.post(url=self.url_data['shop']['add_shop'],
                                 headers = yt_headers,
                                 json=test_input)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        addrcount_after = self.sql_exec.select_one(self.sql['shop']['count'].format(userId))
        self.log.info("新增地址后，查询sql数据结果为{}".format(addrcount_after[0]))

        assert response.json()['message'] == expected['message']
        assert response.json()['status'] == expected['status']
        assert int(addrcount_after[0]) == int(addrcount_before[0]) + 1


    @allure.story("修改店铺接口")
    def test_shop_update(self, yt_headers, userId):
        shopId = self.sql_exec.select_one(self.sql['shop']['id'].format(userId))[0]
        data = self.update_data['set']['shop_data']
        data['shopId'] = shopId

        response = requests.post(url=self.url_data['shop']['update_shop'],
                                 headers = yt_headers,
                                 json=data)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200

    def test_shop_status(self, yt_headers, userId):
        shopId = self.sql_exec.select_one(self.sql['shop']['id'].format(userId))[0]
        shop_status = bool(self.sql_exec.select_one(self.sql['shop']['status'].format(shopId))[0])

        if shop_status == False:
            data = {"shopId": shopId, "isDisabled": 1}
            response = requests.post(url=self.url_data['shop']['update_shop'],
                                 headers = yt_headers,
                                 json=data)
        else:
            data = {"shopId": shopId, "isDisabled": 0}
            response = requests.post(url=self.url_data['shop']['update_shop'],
                                 headers = yt_headers,
                                 json=data)

        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200

    def test_shop_list(self, yt_headers, userId):

        totalCount = self.sql_exec.select_one(self.sql['shop']['count'].format(userId))
        shopinfo = self.sql_exec.select_all(self.sql['shop']['shopinfo'].format(userId))

        response = requests.post(url=self.url_data['shop']['list_shop'],
                                 headers = yt_headers,
                                 json={"pageNum":1,"pageSize":10})
        print(response.json())

        shop_data = response.json()['data']['result']
        print(shopinfo)
        print(shop_data)


@allure.feature("角色管理")
class TestRole(BasicLogic):

    test_data = ReadData().read_testdata()

    def setup_class(self):
        pass

    def teardown_class(self):
        role_id = self.sql_exec.select_all(self.sql['role']['id'])
        roleId_list = []
        for i in role_id:
            for j in i:
                roleId_list.append(j)
        roleId_tuple = tuple(roleId_list)
        # 给元祖添加一个元祖，避免只有一个元素时，构造的sql语句失败
        roleId_tuple = roleId_tuple + ('sue',)

        # 清理角色数据
        self.sql_exec.update(self.sql['role']['clear_role'])

        # 清理授权数据
        self.sql_exec.update(self.sql['role']['clear_permission'].format(roleId_tuple))

    @allure.story("新增角色接口")
    @allure.title("用例标题：{title}")
    @pytest.mark.parametrize("test_input, expected, title", test_data['set']['role_data'])
    def test_role_add(self, test_input, expected, title, yt_headers):
        count_before = self.sql_exec.select_one(self.sql['role']['count'])[0]
        self.log.info("新增角色前，查询sql数据结果为{}".format(count_before))

        response = requests.post(url=self.url_data['role']['add_role'],
                                 headers = yt_headers,
                                 json=test_input)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        # case_count = len(test_input)
        count_after = self.sql_exec.select_one(self.sql['role']['count'])[0]
        self.log.info("新增角色后，查询sql数据结果为{}".format(count_before))

        assert response.json()['message'] == expected['message']
        assert response.json()['status'] == expected['status']
        assert int(count_after) == int(count_before) + 1

    @allure.story("角色名称修改接口")
    def test_role_update(self, yt_headers):
        roleId = self.sql_exec.select_one(self.sql['role']['id'])[0]
        data = self.update_data['set']['role_data']
        data['id'] = roleId

        response = requests.post(url=self.url_data['role']['update_role'],
                                 headers=yt_headers,
                                 json=data)

        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200


    @allure.story("角色授权接口")
    def test_role_auth(self, yt_headers):

        roleId = self.sql_exec.select_one(self.sql['role']['id'])[0]
        data = self.update_data['set']['role_auth']
        data['roleId'] = roleId

        response = requests.post(url=self.url_data['role']['auth_role'],
                                 headers = yt_headers,
                                 json=data)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200

    def test_role_list(self, yt_headers):
        pass

@allure.feature("用户管理")
class TestUser(BasicLogic):

    test_data = ReadData().read_testdata()

    def setup_class(self):
        pass

    def teardown_class(self):
        userId = self.sql_exec.select_all(self.sql['user']['id'])

        userId_list = []
        for i in userId:
            for j in i:
                userId_list.append(j)
        userId_tuple = tuple(userId_list)
        userId_tuple = userId_tuple + ('sue',)

        self.sql_exec.update(self.sql['user']['clear_user'])
        self.sql_exec.update(self.sql['user']['clear_relate'].format(userId_tuple))
        self.sql_exec_basic.update(self.sql['user']['clear_userdata'].format(userId_tuple))

    @allure.story("新增用户信息接口")
    @allure.title("用例标题：{title}")
    @pytest.mark.parametrize("test_input, expected, title", test_data['set']['user_data'])
    def test_user_add(self, test_input, expected, title, yt_headers):

        count_before = self.sql_exec.select_one(self.sql['user']['count'])[0]
        self.log.info("新增子账号前，查询sql数据结果为{}".format(count_before))


        response = requests.post(url=self.url_data['user']['add_user'],
                                 headers = yt_headers,
                                 json=test_input)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        count_after = self.sql_exec.select_one(self.sql['user']['count'])[0]
        self.log.info("新增子账号后，查询sql数据结果为{}".format(count_after))

        assert response.json()['message'] == expected['message']
        assert response.json()['status'] == expected['status']
        if response.json()['status'] == 200 and response.json()['message'] == 'OK':
            assert int(count_after) == int(count_before) + 1


    @allure.story("修改用户信息接口")
    def test_user_update(self, yt_headers):
        userInfo = self.sql_exec.select_one(self.sql['user']['userinfo'])

        data = self.update_data['set']['user_data']
        data['id'] = userInfo[0]
        data['username'] = userInfo[1]
        data['updateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = requests.post(url=self.url_data['user']['update_user'],
                                 headers=yt_headers,
                                 json=data)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200

    @allure.story("启用禁用下级账号")
    def test_user_status(self, yt_headers):
        userInfo = self.sql_exec.select_one(self.sql['user']['userinfo'])
        data = self.update_data['set']['user_data_status']
        data['id'] = userInfo[0]
        data['username'] = userInfo[1]
        data['updateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        user_status = bool(userInfo[2])
        if user_status == True:
            data['isEnabled'] = 0
            response = requests.post(url=self.url_data['user']['update_user'],
                                     headers=yt_headers,
                                     json=data)
        else:
            response = requests.post(url=self.url_data['user']['update_user'],
                                     headers=yt_headers,
                                     json=data)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200

    @allure.story("查看下级账号")
    def test_subuser(self):
        pass

    @allure.story("用户信息查询接口")
    def test_user_list(self):
        pass

@allure.feature("个人信息")
class TestPerson(BasicLogic):
    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    @allure.story("查看个人信息接口")
    def test_person_info(self, yt_headers):
        response = requests.get(url=self.url_data['person']['list_info'],
                                     headers=yt_headers,)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200
        assert response.json()['data']['username'] == 'SUE_ZK04'

    @allure.story("修改个人信息接口")
    def test_person_update(self, yt_headers):

        data = self.update_data['set']['person_info']
        response = requests.post(url=self.url_data['person']['update_info'],
                                     headers=yt_headers,
                                 json=data)
        self.log.info("接口响应数据结果为{}".format(response.json()))

        assert response.json()['message'] == 'OK'
        assert response.json()['status'] == 200